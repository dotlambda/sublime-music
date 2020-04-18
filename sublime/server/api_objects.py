"""
WARNING: AUTOGENERATED FILE
This file was generated by the api_object_generator.py
script. Do not modify this file directly, rather modify the
script or run it on a new API version.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from sublime.server.api_object import APIObject


@dataclass(frozen=True)
class AlbumInfo(APIObject):
    notes: List[str] = field(default_factory=list)
    musicBrainzId: List[str] = field(default_factory=list)
    lastFmUrl: List[str] = field(default_factory=list)
    smallImageUrl: List[str] = field(default_factory=list)
    mediumImageUrl: List[str] = field(default_factory=list)
    largeImageUrl: List[str] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class AverageRating(APIObject, float):
    pass


class MediaType(APIObject, Enum):
    MUSIC = 'music'
    PODCAST = 'podcast'
    AUDIOBOOK = 'audiobook'
    VIDEO = 'video'

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class UserRating(APIObject, int):
    pass


@dataclass(frozen=True)
class Child(APIObject):
    id: str
    isDir: bool
    title: str
    value: Optional[str] = None
    parent: Optional[str] = None
    album: Optional[str] = None
    artist: Optional[str] = None
    track: Optional[int] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    coverArt: Optional[str] = None
    size: Optional[int] = None
    contentType: Optional[str] = None
    suffix: Optional[str] = None
    transcodedContentType: Optional[str] = None
    transcodedSuffix: Optional[str] = None
    duration: Optional[int] = None
    bitRate: Optional[int] = None
    path: Optional[str] = None
    isVideo: Optional[bool] = None
    userRating: Optional[UserRating] = None
    averageRating: Optional[AverageRating] = None
    playCount: Optional[int] = None
    discNumber: Optional[int] = None
    created: Optional[datetime] = None
    starred: Optional[datetime] = None
    albumId: Optional[str] = None
    artistId: Optional[str] = None
    type: Optional[MediaType] = None
    bookmarkPosition: Optional[int] = None
    originalWidth: Optional[int] = None
    originalHeight: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class AlbumList(APIObject):
    album: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class AlbumID3(APIObject):
    id: str
    name: str
    songCount: int
    duration: int
    created: datetime
    value: Optional[str] = None
    artist: Optional[str] = None
    artistId: Optional[str] = None
    coverArt: Optional[str] = None
    playCount: Optional[int] = None
    starred: Optional[datetime] = None
    year: Optional[int] = None
    genre: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class AlbumList2(APIObject):
    album: List[AlbumID3] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class AlbumWithSongsID3(APIObject):
    id: str
    name: str
    songCount: int
    duration: int
    created: datetime
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None
    artist: Optional[str] = None
    artistId: Optional[str] = None
    coverArt: Optional[str] = None
    playCount: Optional[int] = None
    starred: Optional[datetime] = None
    year: Optional[int] = None
    genre: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Artist(APIObject):
    id: str
    name: str
    value: Optional[str] = None
    artistImageUrl: Optional[str] = None
    starred: Optional[datetime] = None
    userRating: Optional[UserRating] = None
    averageRating: Optional[AverageRating] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ArtistInfoBase(APIObject):
    biography: List[str] = field(default_factory=list)
    musicBrainzId: List[str] = field(default_factory=list)
    lastFmUrl: List[str] = field(default_factory=list)
    smallImageUrl: List[str] = field(default_factory=list)
    mediumImageUrl: List[str] = field(default_factory=list)
    largeImageUrl: List[str] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ArtistInfo(APIObject):
    similarArtist: List[Artist] = field(default_factory=list)
    value: Optional[str] = None
    biography: List[str] = field(default_factory=list)
    musicBrainzId: List[str] = field(default_factory=list)
    lastFmUrl: List[str] = field(default_factory=list)
    smallImageUrl: List[str] = field(default_factory=list)
    mediumImageUrl: List[str] = field(default_factory=list)
    largeImageUrl: List[str] = field(default_factory=list)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ArtistID3(APIObject):
    id: str
    name: str
    albumCount: int
    value: Optional[str] = None
    coverArt: Optional[str] = None
    artistImageUrl: Optional[str] = None
    starred: Optional[datetime] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ArtistInfo2(APIObject):
    similarArtist: List[ArtistID3] = field(default_factory=list)
    value: Optional[str] = None
    biography: List[str] = field(default_factory=list)
    musicBrainzId: List[str] = field(default_factory=list)
    lastFmUrl: List[str] = field(default_factory=list)
    smallImageUrl: List[str] = field(default_factory=list)
    mediumImageUrl: List[str] = field(default_factory=list)
    largeImageUrl: List[str] = field(default_factory=list)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ArtistWithAlbumsID3(APIObject):
    id: str
    name: str
    albumCount: int
    album: List[AlbumID3] = field(default_factory=list)
    value: Optional[str] = None
    coverArt: Optional[str] = None
    artistImageUrl: Optional[str] = None
    starred: Optional[datetime] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class IndexID3(APIObject):
    name: str
    artist: List[ArtistID3] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ArtistsID3(APIObject):
    ignoredArticles: str
    index: List[IndexID3] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Bookmark(APIObject):
    position: int
    username: str
    created: datetime
    changed: datetime
    entry: List[Child] = field(default_factory=list)
    value: Optional[str] = None
    comment: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Bookmarks(APIObject):
    bookmark: List[Bookmark] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ChatMessage(APIObject):
    username: str
    time: int
    message: str
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ChatMessages(APIObject):
    chatMessage: List[ChatMessage] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Directory(APIObject):
    id: str
    name: str
    child: List[Child] = field(default_factory=list)
    value: Optional[str] = None
    parent: Optional[str] = None
    starred: Optional[datetime] = None
    userRating: Optional[UserRating] = None
    averageRating: Optional[AverageRating] = None
    playCount: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Error(APIObject):
    code: int
    value: Optional[str] = None
    message: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Genre(APIObject):
    songCount: int
    albumCount: int
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Genres(APIObject):
    genre: List[Genre] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Index(APIObject):
    name: str
    artist: List[Artist] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Indexes(APIObject):
    lastModified: int
    ignoredArticles: str
    shortcut: List[Artist] = field(default_factory=list)
    index: List[Index] = field(default_factory=list)
    child: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class InternetRadioStation(APIObject):
    id: str
    name: str
    streamUrl: str
    value: Optional[str] = None
    homePageUrl: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class InternetRadioStations(APIObject):
    internetRadioStation: List[InternetRadioStation] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class JukeboxStatus(APIObject):
    currentIndex: int
    playing: bool
    gain: float
    value: Optional[str] = None
    position: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class JukeboxPlaylist(APIObject):
    currentIndex: int
    playing: bool
    gain: float
    entry: List[Child] = field(default_factory=list)
    value: Optional[str] = None
    position: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class License(APIObject):
    valid: bool
    value: Optional[str] = None
    email: Optional[str] = None
    licenseExpires: Optional[datetime] = None
    trialExpires: Optional[datetime] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Lyrics(APIObject):
    artist: Optional[str] = None
    value: Optional[str] = None
    title: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class MusicFolder(APIObject):
    id: int
    value: Optional[str] = None
    name: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class MusicFolders(APIObject):
    musicFolder: List[MusicFolder] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


class PodcastStatus(APIObject, Enum):
    NEW = 'new'
    DOWNLOADING = 'downloading'
    COMPLETED = 'completed'
    ERROR = 'error'
    DELETED = 'deleted'
    SKIPPED = 'skipped'

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class PodcastEpisode(APIObject):
    channelId: str
    status: PodcastStatus
    id: str
    isDir: bool
    title: str
    streamId: Optional[str] = None
    description: Optional[str] = None
    publishDate: Optional[datetime] = None
    value: Optional[str] = None
    parent: Optional[str] = None
    album: Optional[str] = None
    artist: Optional[str] = None
    track: Optional[int] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    coverArt: Optional[str] = None
    size: Optional[int] = None
    contentType: Optional[str] = None
    suffix: Optional[str] = None
    transcodedContentType: Optional[str] = None
    transcodedSuffix: Optional[str] = None
    duration: Optional[int] = None
    bitRate: Optional[int] = None
    path: Optional[str] = None
    isVideo: Optional[bool] = None
    userRating: Optional[UserRating] = None
    averageRating: Optional[AverageRating] = None
    playCount: Optional[int] = None
    discNumber: Optional[int] = None
    created: Optional[datetime] = None
    starred: Optional[datetime] = None
    albumId: Optional[str] = None
    artistId: Optional[str] = None
    type: Optional[MediaType] = None
    bookmarkPosition: Optional[int] = None
    originalWidth: Optional[int] = None
    originalHeight: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class NewestPodcasts(APIObject):
    episode: List[PodcastEpisode] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class NowPlayingEntry(APIObject):
    username: str
    minutesAgo: int
    playerId: int
    id: str
    isDir: bool
    title: str
    playerName: Optional[str] = None
    value: Optional[str] = None
    parent: Optional[str] = None
    album: Optional[str] = None
    artist: Optional[str] = None
    track: Optional[int] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    coverArt: Optional[str] = None
    size: Optional[int] = None
    contentType: Optional[str] = None
    suffix: Optional[str] = None
    transcodedContentType: Optional[str] = None
    transcodedSuffix: Optional[str] = None
    duration: Optional[int] = None
    bitRate: Optional[int] = None
    path: Optional[str] = None
    isVideo: Optional[bool] = None
    userRating: Optional[UserRating] = None
    averageRating: Optional[AverageRating] = None
    playCount: Optional[int] = None
    discNumber: Optional[int] = None
    created: Optional[datetime] = None
    starred: Optional[datetime] = None
    albumId: Optional[str] = None
    artistId: Optional[str] = None
    type: Optional[MediaType] = None
    bookmarkPosition: Optional[int] = None
    originalWidth: Optional[int] = None
    originalHeight: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class NowPlaying(APIObject):
    entry: List[NowPlayingEntry] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class PlayQueue(APIObject):
    username: str
    changed: datetime
    changedBy: str
    entry: List[Child] = field(default_factory=list)
    value: Optional[str] = None
    current: Optional[int] = None
    position: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Playlist(APIObject):
    id: str
    name: str
    songCount: int
    duration: int
    created: datetime
    changed: datetime
    allowedUser: List[str] = field(default_factory=list)
    value: Optional[str] = None
    comment: Optional[str] = None
    owner: Optional[str] = None
    public: Optional[bool] = None
    coverArt: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class PlaylistWithSongs(APIObject):
    id: str
    name: str
    songCount: int
    duration: int
    created: datetime
    changed: datetime
    entry: List[Child] = field(default_factory=list)
    value: Optional[str] = None
    allowedUser: List[str] = field(default_factory=list)
    comment: Optional[str] = None
    owner: Optional[str] = None
    public: Optional[bool] = None
    coverArt: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Playlists(APIObject):
    playlist: List[Playlist] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class PodcastChannel(APIObject):
    id: str
    url: str
    status: PodcastStatus
    episode: List[PodcastEpisode] = field(default_factory=list)
    value: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    coverArt: Optional[str] = None
    originalImageUrl: Optional[str] = None
    errorMessage: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Podcasts(APIObject):
    channel: List[PodcastChannel] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


class ResponseStatus(APIObject, Enum):
    OK = 'ok'
    FAILED = 'failed'

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class ScanStatus(APIObject):
    scanning: bool
    value: Optional[str] = None
    count: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class SearchResult(APIObject):
    offset: int
    totalHits: int
    match: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class SearchResult2(APIObject):
    artist: List[Artist] = field(default_factory=list)
    album: List[Child] = field(default_factory=list)
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class SearchResult3(APIObject):
    artist: List[ArtistID3] = field(default_factory=list)
    album: List[AlbumID3] = field(default_factory=list)
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Share(APIObject):
    id: str
    url: str
    username: str
    created: datetime
    visitCount: int
    entry: List[Child] = field(default_factory=list)
    value: Optional[str] = None
    description: Optional[str] = None
    expires: Optional[datetime] = None
    lastVisited: Optional[datetime] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Shares(APIObject):
    share: List[Share] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class SimilarSongs(APIObject):
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class SimilarSongs2(APIObject):
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Songs(APIObject):
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Starred(APIObject):
    artist: List[Artist] = field(default_factory=list)
    album: List[Child] = field(default_factory=list)
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Starred2(APIObject):
    artist: List[ArtistID3] = field(default_factory=list)
    album: List[AlbumID3] = field(default_factory=list)
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class TopSongs(APIObject):
    song: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class User(APIObject):
    username: str
    scrobblingEnabled: bool
    adminRole: bool
    settingsRole: bool
    downloadRole: bool
    uploadRole: bool
    playlistRole: bool
    coverArtRole: bool
    commentRole: bool
    podcastRole: bool
    streamRole: bool
    jukeboxRole: bool
    shareRole: bool
    videoConversionRole: bool
    folder: List[int] = field(default_factory=list)
    value: Optional[str] = None
    email: Optional[str] = None
    maxBitRate: Optional[int] = None
    avatarLastChanged: Optional[datetime] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Users(APIObject):
    user: List[User] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Version(APIObject, str):
    pass


@dataclass(frozen=True)
class AudioTrack(APIObject):
    id: str
    value: Optional[str] = None
    name: Optional[str] = None
    languageCode: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Captions(APIObject):
    id: str
    value: Optional[str] = None
    name: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class VideoConversion(APIObject):
    id: str
    value: Optional[str] = None
    bitRate: Optional[int] = None
    audioTrackId: Optional[int] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class VideoInfo(APIObject):
    id: str
    captions: List[Captions] = field(default_factory=list)
    audioTrack: List[AudioTrack] = field(default_factory=list)
    conversion: List[VideoConversion] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Videos(APIObject):
    video: List[Child] = field(default_factory=list)
    value: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


@dataclass(frozen=True)
class Response(APIObject):
    musicFolders: Optional[MusicFolders] = None
    indexes: Optional[Indexes] = None
    directory: Optional[Directory] = None
    genres: Optional[Genres] = None
    artists: Optional[ArtistsID3] = None
    artist: Optional[ArtistWithAlbumsID3] = None
    album: Optional[AlbumWithSongsID3] = None
    song: Optional[Child] = None
    videos: Optional[Videos] = None
    videoInfo: Optional[VideoInfo] = None
    nowPlaying: Optional[NowPlaying] = None
    searchResult: Optional[SearchResult] = None
    searchResult2: Optional[SearchResult2] = None
    searchResult3: Optional[SearchResult3] = None
    playlists: Optional[Playlists] = None
    playlist: Optional[PlaylistWithSongs] = None
    jukeboxStatus: Optional[JukeboxStatus] = None
    jukeboxPlaylist: Optional[JukeboxPlaylist] = None
    license: Optional[License] = None
    users: Optional[Users] = None
    user: Optional[User] = None
    chatMessages: Optional[ChatMessages] = None
    albumList: Optional[AlbumList] = None
    albumList2: Optional[AlbumList2] = None
    randomSongs: Optional[Songs] = None
    songsByGenre: Optional[Songs] = None
    lyrics: Optional[Lyrics] = None
    podcasts: Optional[Podcasts] = None
    newestPodcasts: Optional[NewestPodcasts] = None
    internetRadioStations: Optional[InternetRadioStations] = None
    bookmarks: Optional[Bookmarks] = None
    playQueue: Optional[PlayQueue] = None
    shares: Optional[Shares] = None
    starred: Optional[Starred] = None
    starred2: Optional[Starred2] = None
    albumInfo: Optional[AlbumInfo] = None
    artistInfo: Optional[ArtistInfo] = None
    artistInfo2: Optional[ArtistInfo2] = None
    similarSongs: Optional[SimilarSongs] = None
    similarSongs2: Optional[SimilarSongs2] = None
    topSongs: Optional[TopSongs] = None
    scanStatus: Optional[ScanStatus] = None
    error: Optional[Error] = None
    value: Optional[str] = None
    status: Optional[ResponseStatus] = None
    version: Optional[Version] = None

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)
