import hashlib
import os
import pickle
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional

import yaml

from sublime.ui.state import UIState


class ReplayGainType(Enum):
    NO = 0
    TRACK = 1
    ALBUM = 2

    def as_string(self) -> str:
        return ['no', 'track', 'album'][self.value]

    @staticmethod
    def from_string(replay_gain_type: str) -> 'ReplayGainType':
        return {
            'no': ReplayGainType.NO,
            'disabled': ReplayGainType.NO,
            'track': ReplayGainType.TRACK,
            'album': ReplayGainType.ALBUM,
        }[replay_gain_type.lower()]


@dataclass
class ServerConfiguration:
    name: str = 'Default'
    server_address: str = 'http://yourhost'
    local_network_address: str = ''
    local_network_ssid: str = ''
    username: str = ''
    password: str = ''
    sync_enabled: bool = True
    disable_cert_verify: bool = False
    version: int = 0

    def migrate(self):
        self.version = 0

    def strhash(self) -> str:
        """
        Returns the MD5 hash of the server's name, server address, and
        username. This should be used whenever it's necessary to uniquely
        identify the server, rather than using the name (which is not
        necessarily unique).

        >>> sc = ServerConfiguration(
        ...     name='foo',
        ...     server_address='bar',
        ...     username='baz',
        ... )
        >>> sc.strhash()
        '6df23dc03f9b54cc38a0fc1483df6e21'
        """
        server_info = (self.name + self.server_address + self.username)
        return hashlib.md5(server_info.encode('utf-8')).hexdigest()


@dataclass
class AppConfiguration:
    servers: List[ServerConfiguration] = field(default_factory=list)
    current_server: int = -1
    cache_location: str = ''
    max_cache_size_mb: int = -1  # -1 means unlimited
    always_stream: bool = False  # always stream instead of downloading songs
    download_on_stream: bool = True  # also download when streaming a song
    song_play_notification: bool = True
    prefetch_amount: int = 3
    concurrent_download_limit: int = 5
    port_number: int = 8282
    version: int = 3
    serve_over_lan: bool = True
    replay_gain: ReplayGainType = ReplayGainType.NO
    filename: Optional[Path] = None

    @staticmethod
    def load_from_file(filename: Path) -> 'AppConfiguration':
        if filename.exists():
            with open(filename, 'r') as f:
                config = AppConfiguration(**yaml.load(f, Loader=yaml.CLoader))
        else:
            config = AppConfiguration()

        config.filename = filename
        return config

    def __post_init__(self):
        # Default the cache_location to ~/.local/share/sublime-music
        if not self.cache_location:
            path = Path(os.environ.get('XDG_DATA_HOME') or '~/.local/share')
            path = path.expanduser().joinpath('sublime-music').resolve()
            self.cache_location = path.as_posix()

        # Deserialize the YAML into the ServerConfiguration object.
        if (len(self.servers) > 0
                and type(self.servers[0]) != ServerConfiguration):
            self.servers = [ServerConfiguration(**sc) for sc in self.servers]

        self._state = None
        self._current_server_hash = None

    def migrate(self):
        for server in self.servers:
            server.migrate()
        self.version = 3
        self.state.migrate()

    @property
    def server(self) -> Optional[ServerConfiguration]:
        if 0 <= self.current_server < len(self.servers):
            return self.servers[self.current_server]

        return None

    @property
    def state(self) -> UIState:
        server = self.server
        if not server:
            return UIState()

        # If already retrieved, and the server hasn't changed, then return the
        # state. Don't use strhash because that is much more expensive of an
        # operation.
        if self._current_server_hash != hash(server) or self._state:
            self._current_server_hash = hash(server)
            if self.state_file_location.exists():
                try:
                    with open(self.state_file_location, 'rb') as f:
                        self._state = pickle.load(f)
                except Exception:
                    # Just ignore any errors, it is only UI state.
                    self._state = UIState()

        return self._state

    @property
    def state_file_location(self):
        server_hash = self.server.strhash()

        state_file_location = Path(
            os.environ.get('XDG_DATA_HOME') or '~/.local/share')
        state_file_location = state_file_location.expanduser().joinpath(
            'sublime-music', server_hash, 'state.pickle')

    def save(self):
        # Save the config as YAML.
        self.filename.parent().mkdir(parents=True, exist_ok=True)
        with open(self.filename, 'w+') as f:
            f.write(yaml.dump(asdict(self)))

        # Save the state for the current server.
        self.state_file_location.parent().mkdir(parents=True, exist_ok=True)
        with open(self.state_file_location, 'wb+') as f:
            pickle.dump(self.state, f)
