from dasbus.connection import SessionMessageBus
from dasbus.identifier import DBusServiceIdentifier, DBusInterfaceIdentifier
from dasbus.loop import EventLoop
from dasbus.server.interface import dbus_interface, dbus_signal
from dasbus.server.publishable import Publishable
from dasbus.server.template import InterfaceTemplate
from dasbus.signal import Signal
from dasbus.typing import Str, ObjPath
from dasbus.xml import XMLGenerator

PLAYBACK_STATUS = ["Playing", "Paused", "Stopped"]
LOOP_STATUS = ["None", "Track", "Playlist"]

SESSION_BUS = SessionMessageBus()
MPRIS_NAMESPACE = ("org", "freedesktop", "MediaPlayer2")
MPRIS2_SERVICE = DBusServiceIdentifier(
    namespace=MPRIS_NAMESPACE,
    basename="ewave",
    message_bus=SESSION_BUS
)
PLAYER_SERVICE = DBusInterfaceIdentifier(
    namespace=MPRIS_NAMESPACE,
    basename="Player"
)
TRACKLIST_SERVICE = DBusInterfaceIdentifier(
    namespace=MPRIS_NAMESPACE,
    basename="TrackList"
)
PLAYLIST_SERVICE = DBusInterfaceIdentifier(
    namespace=MPRIS_NAMESPACE,
    basename="Playlists"
)

@dbus_interface(MPRIS2_SERVICE.interface_name)
class MPRIS2Interface(InterfaceTemplate):
    pass

@dbus_interface(PLAYER_SERVICE.interface_name)
class MPRIS2PlayerInterface(InterfaceTemplate):
    pass

@dbus_interface(TRACKLIST_SERVICE.interface_name)
class MPRIS2TrackListInterface(InterfaceTemplate):
    pass

@dbus_interface(PLAYLIST_SERVICE.interface_name)
class MPRIS2PlaylistsInterface(InterfaceTemplate):
    pass