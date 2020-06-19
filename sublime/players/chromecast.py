import base64
import io
import logging
import mimetypes
import multiprocessing
import os
import socket
from datetime import timedelta
from typing import Any, Callable, Dict, Optional, Set, Tuple, Type, Union
from urllib.parse import urlparse
from uuid import UUID

from gi.repository import GLib

from sublime.adapters import AdapterManager
from sublime.adapters.api_objects import Song

from .base import Player, PlayerDeviceEvent, PlayerEvent

try:
    import pychromecast

    chromecast_imported = True
except Exception:
    chromecast_imported = False

try:
    import bottle

    bottle_imported = True
except Exception:
    bottle_imported = False

SERVE_FILES_KEY = "Serve Local Files to Chromecasts on the LAN"
LAN_PORT_KEY = "LAN Server Port Number"


class ChromecastPlayer(Player):
    name = "Chromecast"
    can_start_playing_with_no_latency = False

    @property
    def enabled(self) -> bool:
        return chromecast_imported

    @staticmethod
    def get_configuration_options() -> Dict[str, Union[Type, Tuple[str, ...]]]:
        if not bottle_imported:
            return {}
        return {SERVE_FILES_KEY: bool, LAN_PORT_KEY: int}

    def supported_schemes(self) -> Set[str]:
        schemes = {"http", "https"}
        if bottle_imported and self.config.get(SERVE_FILES_KEY):
            schemes.add("file")
        return schemes

    _timepos = 0.0

    def __init__(
        self,
        on_timepos_change: Callable[[Optional[float]], None],
        on_track_end: Callable[[], None],
        on_player_event: Callable[[PlayerEvent], None],
        player_device_change_callback: Callable[[PlayerDeviceEvent], None],
        config: Dict[str, Union[str, int, bool]],
    ):
        self.server_process = None
        self.config = config
        self.on_timepos_change = on_timepos_change
        self.on_track_end = on_track_end
        self.on_player_event = on_player_event

        if bottle_imported and self.config.get(SERVE_FILES_KEY):
            # TODO (#222): should have a mechanism to update this. Maybe it should be
            # determined every time we try and play a song.
            self.server_process = multiprocessing.Process(
                target=self._run_server_process,
                args=("0.0.0.0", self.config.get(LAN_PORT_KEY)),
            )
            self.server_process.start()

        if chromecast_imported:
            self._chromecasts: Dict[UUID, pychromecast.Chromecast] = {}
            self._current_chromecast: Optional[pychromecast.Chromecast] = None

            def discovered_callback(chromecast: pychromecast.Chromecast):
                self._chromecasts[chromecast.device.uuid] = chromecast
                player_device_change_callback(
                    PlayerDeviceEvent(
                        PlayerDeviceEvent.Delta.ADD,
                        type(self),
                        str(chromecast.device.uuid),
                        chromecast.device.friendly_name,
                    )
                )

            pychromecast.get_chromecasts(blocking=False, callback=discovered_callback)

    def set_current_device_id(self, device_id: str):
        self._current_chromecast = self._chromecasts[UUID(device_id)]
        self._current_chromecast.media_controller.register_status_listener(self)
        self._current_chromecast.register_status_listener(self)
        self._current_chromecast.wait()

    def new_cast_status(self, status: Any):
        self.on_player_event(
            PlayerEvent(
                PlayerEvent.EventType.VOLUME_CHANGE,
                volume=(status.volume_level * 100 if not status.volume_muted else 0),
            )
        )

        # This normally happens when "Stop Casting" is pressed in the Google
        # Home app.
        if status.session_id is None:
            self.on_player_event(
                PlayerEvent(PlayerEvent.EventType.PLAY_STATE_CHANGE, playing=False)
            )
            self.on_player_event(PlayerEvent(PlayerEvent.EventType.DISCONNECT))
            self.song_loaded = False

    time_increment_order_token = 0

    def new_media_status(self, status: Any):
        # Detect the end of a track and go to the next one.
        if (
            status.idle_reason == "FINISHED"
            and status.player_state == "IDLE"
            and self._timepos > 0
        ):
            self.on_track_end()
            return

        self.song_loaded = True

        self._timepos = status.current_time

        self.on_player_event(
            PlayerEvent(
                PlayerEvent.EventType.PLAY_STATE_CHANGE,
                playing=(status.player_state in ("PLAYING", "BUFFERING")),
            )
        )

        def increment_time(order_token: int):
            if self.time_increment_order_token != order_token or not self.playing:
                return

            self._timepos += 0.5
            self.on_timepos_change(self._timepos)
            GLib.timeout_add(500, increment_time, order_token)

        self.time_increment_order_token += 1
        GLib.timeout_add(500, increment_time, self.time_increment_order_token)

    def shutdown(self):
        if self.server_process:
            self.server_process.terminate()

        try:
            self._current_chromecast.disconnect()
        except Exception:
            pass

    _serving_song_id = multiprocessing.Array("c", 1024)  # huge buffer, just in case
    _serving_token = multiprocessing.Array("c", 16)

    def _run_server_process(self, host: str, port: int):
        app = bottle.Bottle()

        @app.route("/")
        def index() -> str:
            return """
            <h1>Sublime Music Local Music Server</h1>
            <p>
                Sublime Music uses this port as a server for serving music Chromecasts
                on the same LAN.
            </p>
            """

        @app.route("/s/<token>")
        def stream_song(token: str) -> bytes:
            if token != self._serving_token.value.decode():
                raise bottle.HTTPError(status=401, body="Invalid token.")

            song = AdapterManager.get_song_details(
                self._serving_song_id.value.decode()
            ).result()
            filename = AdapterManager.get_song_filename_or_stream(song)
            assert filename.startswith("file://")
            with open(filename[7:], "rb") as fin:
                song_buffer = io.BytesIO(fin.read())

            content_type = mimetypes.guess_type(filename)[0]
            bottle.response.set_header("Content-Type", content_type)
            bottle.response.set_header("Accept-Ranges", "bytes")
            return song_buffer.read()

        bottle.run(app, host=host, port=port)

    @property
    def playing(self) -> bool:
        if (
            not self._current_chromecast
            or not self._current_chromecast.media_controller
        ):
            return False
        return self._current_chromecast.media_controller.status.player_is_playing

    def get_volume(self) -> float:
        if self._current_chromecast:
            # The volume is in the range [0, 1]. Multiply by 100 to get to [0, 100].
            return self._current_chromecast.status.volume_level * 100
        else:
            return 100

    def set_volume(self, volume: float):
        if self._current_chromecast:
            # volume value is in [0, 100]. Convert to [0, 1] for Chromecast.
            self._current_chromecast.set_volume(volume / 100)

    def get_is_muted(self) -> bool:
        if not self._current_chromecast:
            return False
        return self._current_chromecast.volume_muted

    def set_muted(self, muted: bool):
        if not self._current_chromecast:
            return
        self._current_chromecast.set_volume_muted(muted)

    def play_media(self, uri: str, progress: timedelta, song: Song):
        assert self._current_chromecast
        scheme = urlparse(uri).scheme
        if scheme == "file":
            token = base64.b16encode(os.urandom(8))
            self._serving_token.value = token
            self._serving_song_id.value = song.id.encode()

            # If this fails, then we are basically screwed, so don't care if it blows
            # up.
            # TODO (#129): this does not work properly when on VPNs when the DNS is
            # piped over the VPN tunnel.
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            host_ip = s.getsockname()[0]
            s.close()

            uri = f"http://{host_ip}:{self.config.get(LAN_PORT_KEY)}/s/{token.decode()}"
            logging.info("Serving {song.name} at {uri}")

        cover_art_url = AdapterManager.get_cover_art_uri(song.cover_art, size=1000)
        self._current_chromecast.media_controller.play_media(
            uri,
            # Just pretend that whatever we send it is mp3, even if it isn't.
            "audio/mp3",
            current_time=progress.total_seconds(),
            title=song.title,
            thumb=cover_art_url,
            metadata={
                "metadataType": 3,
                "albumName": song.album.name if song.album else None,
                "artist": song.artist.name if song.artist else None,
                "trackNumber": song.track,
            },
        )

        # Make sure to clear out the cache duration state.
        self.on_player_event(
            PlayerEvent(
                PlayerEvent.EventType.STREAM_CACHE_PROGRESS_CHANGE,
                stream_cache_duration=0,
            )
        )
        self._timepos = progress.total_seconds()

    def pause(self):
        if self._current_chromecast and self._current_chromecast.media_controller:
            self._current_chromecast.media_controller.pause()

    def play(self):
        if self._current_chromecast and self._current_chromecast.media_controller:
            self._current_chromecast.media_controller.play()

    def seek(self, position: timedelta):
        if not self._current_chromecast:
            return

        do_pause = not self.playing
        self._current_chromecast.media_controller.seek(position.total_seconds())
        if do_pause:
            self.pause()

    def _wait_for_playing(self):
        pass
