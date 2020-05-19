from random import randint
from typing import Any, List

from gi.repository import Gdk, GLib, GObject, Gtk, Pango

from sublime.adapters import AdapterManager, api_objects as API, Result
from sublime.config import AppConfiguration
from sublime.ui import util
from sublime.ui.common.icon_button import IconButton
from sublime.ui.common.song_list_column import SongListColumn
from sublime.ui.common.spinner_image import SpinnerImage


class AlbumWithSongs(Gtk.Box):
    __gsignals__ = {
        "song-selected": (GObject.SignalFlags.RUN_FIRST, GObject.TYPE_NONE, (),),
        "song-clicked": (
            GObject.SignalFlags.RUN_FIRST,
            GObject.TYPE_NONE,
            (int, object, object),
        ),
    }

    def __init__(
        self,
        album: API.Album,
        cover_art_size: int = 200,
        show_artist_name: bool = True,
    ):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.album = album

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        artist_artwork = SpinnerImage(
            loading=False,
            image_name="artist-album-list-artwork",
            spinner_name="artist-artwork-spinner",
            image_size=cover_art_size,
        )
        # Account for 10px margin on all sides with "+ 20".
        artist_artwork.set_size_request(cover_art_size + 20, cover_art_size + 20)
        box.pack_start(artist_artwork, False, False, 0)
        box.pack_start(Gtk.Box(), True, True, 0)
        self.pack_start(box, False, False, 0)

        def cover_art_future_done(f: Result):
            artist_artwork.set_from_file(f.result())
            artist_artwork.set_loading(False)

        cover_art_filename_future = AdapterManager.get_cover_art_filename(
            album.cover_art, before_download=lambda: artist_artwork.set_loading(True),
        )
        cover_art_filename_future.add_done_callback(
            lambda f: GLib.idle_add(cover_art_future_done, f)
        )

        album_details = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        album_title_and_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # TODO (#43): deal with super long-ass titles
        album_title_and_buttons.add(
            Gtk.Label(
                label=album.name,
                name="artist-album-list-album-name",
                halign=Gtk.Align.START,
                ellipsize=Pango.EllipsizeMode.END,
            )
        )

        self.play_btn = IconButton(
            "media-playback-start-symbolic",
            "Play all songs in this album",
            sensitive=False,
        )
        self.play_btn.connect("clicked", self.play_btn_clicked)
        album_title_and_buttons.pack_start(self.play_btn, False, False, 5)

        self.shuffle_btn = IconButton(
            "media-playlist-shuffle-symbolic",
            "Shuffle all songs in this album",
            sensitive=False,
        )
        self.shuffle_btn.connect("clicked", self.shuffle_btn_clicked)
        album_title_and_buttons.pack_start(self.shuffle_btn, False, False, 5)

        self.play_next_btn = IconButton(
            "go-top-symbolic",
            "Play all of the songs in this album next",
            sensitive=False,
        )
        album_title_and_buttons.pack_start(self.play_next_btn, False, False, 5)

        self.add_to_queue_btn = IconButton(
            "go-jump-symbolic",
            "Add all the songs in this album to the end of the play queue",
            sensitive=False,
        )
        album_title_and_buttons.pack_start(self.add_to_queue_btn, False, False, 5)

        self.download_all_btn = IconButton(
            "folder-download-symbolic",
            "Download all songs in this album",
            sensitive=False,
        )
        self.download_all_btn.connect("clicked", self.on_download_all_click)
        album_title_and_buttons.pack_end(self.download_all_btn, False, False, 5)

        album_details.add(album_title_and_buttons)

        stats: List[Any] = [
            album.artist.name if show_artist_name and album.artist else None,
            album.year,
            album.genre.name if album.genre else None,
            util.format_sequence_duration(album.duration) if album.duration else None,
        ]

        album_details.add(
            Gtk.Label(
                label=util.dot_join(*stats), halign=Gtk.Align.START, margin_left=10,
            )
        )

        self.loading_indicator_container = Gtk.Box()
        album_details.add(self.loading_indicator_container)

        # cache status, title, duration, song ID
        self.album_song_store = Gtk.ListStore(str, str, str, str)

        self.album_songs = Gtk.TreeView(
            model=self.album_song_store,
            name="album-songs-list",
            headers_visible=False,
            margin_top=15,
            margin_left=10,
            margin_right=10,
            margin_bottom=10,
        )
        self.album_songs.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        # Song status column.
        renderer = Gtk.CellRendererPixbuf()
        renderer.set_fixed_size(30, 35)
        column = Gtk.TreeViewColumn("", renderer, icon_name=0)
        column.set_resizable(True)
        self.album_songs.append_column(column)

        self.album_songs.append_column(SongListColumn("TITLE", 1, bold=True))
        self.album_songs.append_column(SongListColumn("DURATION", 2, align=1, width=40))

        self.album_songs.connect("row-activated", self.on_song_activated)
        self.album_songs.connect("button-press-event", self.on_song_button_press)
        self.album_songs.get_selection().connect(
            "changed", self.on_song_selection_change
        )
        album_details.add(self.album_songs)

        self.pack_end(album_details, True, True, 0)

        self.update_album_songs(album.id)

    # Event Handlers
    # =========================================================================
    def on_song_selection_change(self, event: Any):
        if not self.album_songs.has_focus():
            self.emit("song-selected")

    def on_song_activated(self, treeview: Any, idx: Gtk.TreePath, column: Any):
        # The song ID is in the last column of the model.
        self.emit(
            "song-clicked",
            idx.get_indices()[0],
            [m[-1] for m in self.album_song_store],
            {},
        )

    def on_song_button_press(self, tree: Any, event: Gdk.EventButton) -> bool:
        if event.button == 3:  # Right click
            clicked_path = tree.get_path_at_pos(event.x, event.y)
            if not clicked_path:
                return False

            store, paths = tree.get_selection().get_selected_rows()
            allow_deselect = False

            def on_download_state_change(song_id: str):
                self.update_album_songs(self.album.id)

            # Use the new selection instead of the old one for calculating what
            # to do the right click on.
            if clicked_path[0] not in paths:
                paths = [clicked_path[0]]
                allow_deselect = True

            song_ids = [self.album_song_store[p][-1] for p in paths]

            # Used to adjust for the header row.
            bin_coords = tree.convert_tree_to_bin_window_coords(event.x, event.y)
            widget_coords = tree.convert_tree_to_widget_coords(event.x, event.y)

            util.show_song_popover(
                song_ids,
                event.x,
                event.y + abs(bin_coords.by - widget_coords.wy),
                tree,
                on_download_state_change=on_download_state_change,
            )

            # If the click was on a selected row, don't deselect anything.
            if not allow_deselect:
                return True

        return False

    def on_download_all_click(self, btn: Any):
        AdapterManager.batch_download_songs(
            [x[-1] for x in self.album_song_store],
            before_download=lambda _: self.update(),
            on_song_download_complete=lambda _: self.update(),
        )

    def play_btn_clicked(self, btn: Any):
        song_ids = [x[-1] for x in self.album_song_store]
        self.emit(
            "song-clicked", 0, song_ids, {"force_shuffle_state": False},
        )

    def shuffle_btn_clicked(self, btn: Any):
        song_ids = [x[-1] for x in self.album_song_store]
        self.emit(
            "song-clicked",
            randint(0, len(self.album_song_store) - 1),
            song_ids,
            {"force_shuffle_state": True},
        )

    # Helper Methods
    # =========================================================================
    def deselect_all(self):
        self.album_songs.get_selection().unselect_all()

    def update(self, force: bool = False):
        self.update_album_songs(self.album.id, force=force)

    def set_loading(self, loading: bool):
        if loading:
            if len(self.loading_indicator_container.get_children()) == 0:
                self.loading_indicator_container.pack_start(Gtk.Box(), True, True, 0)
                spinner = Gtk.Spinner(name="album-list-song-list-spinner")
                spinner.start()
                self.loading_indicator_container.add(spinner)
                self.loading_indicator_container.pack_start(Gtk.Box(), True, True, 0)

            self.loading_indicator_container.show_all()
        else:
            self.loading_indicator_container.hide()

    @util.async_callback(
        AdapterManager.get_album,
        before_download=lambda self: self.set_loading(True),
        on_failure=lambda self, e: self.set_loading(False),
    )
    def update_album_songs(
        self,
        album: API.Album,
        app_config: AppConfiguration,
        force: bool = False,
        order_token: int = None,
    ):
        song_ids = [s.id for s in album.songs or []]
        new_store = [
            [
                cached_status,
                util.esc(song.title),
                util.format_song_duration(song.duration),
                song.id,
            ]
            for cached_status, song in zip(
                util.get_cached_status_icons(song_ids), album.songs or []
            )
        ]

        song_ids = [song[-1] for song in new_store]

        self.play_btn.set_sensitive(True)
        self.shuffle_btn.set_sensitive(True)
        self.download_all_btn.set_sensitive(AdapterManager.can_batch_download_songs())

        self.play_next_btn.set_action_target_value(GLib.Variant("as", song_ids))
        self.add_to_queue_btn.set_action_target_value(GLib.Variant("as", song_ids))
        self.play_next_btn.set_action_name("app.add-to-queue")
        self.add_to_queue_btn.set_action_name("app.play-next")

        util.diff_song_store(self.album_song_store, new_store)

        # Have to idle_add here so that his happens after the component is rendered.
        self.set_loading(False)
