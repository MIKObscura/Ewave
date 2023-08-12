from pydbus import SessionBus
from gi.repository import GLib

# The classes below are used to implement the different services required by the MPRIS2 standard
# More information about the specifics of the standard can be found there:
# https://specifications.freedesktop.org/mpris-spec/latest/index.html
class MPRIS2Service():
    """
    <node>
        <interface name="org.freedestop.MediaPlayer2.ewave">
            <method name="Raise" />
            <method name="Quit" />
            <property name="CanQuit" type="b" access="read" />
            <property name="CanRaise" type="b" access="read" />
            <property name="HasTrackList" type="b" access="read" />
            <property name="Identity" type="s" access="read" />
            <property name="SupportedUriSchemes" type="as" />
            <property name="SupportedMimeTypes" type="as" />
        </interface>
    </node>
    """
    def __init__():
        self.CanQuit = False
        self.CanRaise = False
        self.HasTrackList = True
        self.Identity = "Ewave"
        self.SupportedMimeTypes = ["audio"]
        self.SupportedUriSchemes = ["file"]

    def Raise():
        pass

    def Quit():
        pass


class MPRIS2PlayerService():
    """
    <node>
        <interface name="org.freedestop.MediaPlayer2.ewave.Player">
            <tp:enum name="Playback_Status" tp:name-for-bindings="Playback_Status" type="s">
                <tp:enumvalue suffix="Playing" value="Playing" />
                <tp:enumvalue suffix="Paused" value="Paused" />
                <tp:enumvalue suffix="Stopped" value="Stopped" />
            </tp:enum>
            <tp:enum name="Loop_Status" tp:name-for-bindings="Loop_Status" type="s">
                <tp:enumvalue suffix="None" value="None" />
                <tp:enumvalue suffix="Track" value="Track" />
                <tp:enumvalue suffix="Playlist" value="Playlist" />
            </tp:enum>
            <tp:simple-type name="Track_Id" type="o" array-name="Track_Id_List" />
            <tp:simple-type name="Playback_Rate" type="d" />
            <tp:simple-type name="Volume" type="d" />
            <tp:simple-type name="Time_In_Us" type="x" />
            <tp:mapping name="Metadata_Map" array-name="Metadata_Map_List">
                <tp:member type="s" name="Attribute" />
                <tp:member type="v" name="Value" />
                </tp:member>
            </tp:mapping>
            <method name="Next" />
            <method name="Previous" />
            <method name="Pause" />
            <method name="PlayPause" />
            <method name="Stop" />
            <method name="Play" />
            <method name="Seek">
                <arg direction="in" type="x" tp:type="Time_In_Us" name="Offset"/>
            </method>
            <method name="SetPosition">
                <arg direction="in" type="o" tp:type="Track_Id" name="TrackId" />
                <arg direction="in" type="x" tp:type="Time_In_Us" name="Position" />
            </method>
            <method name="OpenUri">
                <arg direction="in" type="s" name="Uri" />
            </method>
            <property name="PlaybackStatus" tp:name-for-bindings="Playback_Status" type="s" tp:type="Playback_Status" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="LoopStatus" type="s" access="readwrite" tp:name-for-bindings="Loop_Status" tp:type="Loop_Status">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
                <annotation name="org.mpris.MediaPlayer2.property.optional" value="true"/>
            </property>
            <property name="Rate" tp:name-for-bindings="Rate" type="d" tp:type="Playback_Rate" access="readwrite">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="Shuffle" tp:name-for-bindings="Shuffle" type="b" access="readwrite">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
                <annotation name="org.mpris.MediaPlayer2.property.optional" value="true"/>
            </property>
            <property name="Metadata" tp:name-for-bindings="Metadata" type="a{sv}" tp:type="Metadata_Map" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="Volume" type="d" tp:type="Volume" tp:name-for-bindings="Volume" access="readwrite">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true" />
            </property>
            <property name="Position" type="x" tp:type="Time_In_Us" tp:name-for-bindings="Position" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
            </property>
            <property name="MinimumRate" tp:name-for-bindings="Minimum_Rate" type="d" tp:type="Playback_Rate" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="MaximumRate" tp:name-for-bindings="Maximum_Rate" type="d" tp:type="Playback_Rate" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanGoNext" tp:name-for-bindings="Can_Go_Next" type="b" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanGoPrevious" tp:name-for-bindings="Can_Go_Previous" type="b" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanPlay" tp:name-for-bindings="Can_Play" type="b" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanPause" tp:name-for-bindings="Can_Pause" type="b" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanSeek" tp:name-for-bindings="Can_Seek" type="b" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
            </property>
            <property name="CanControl" tp:name-for-bindings="Can_Control" type="b" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
            </property>
            <signal name="Seeked" tp:name-for-bindings="Seeked">
                <arg name="Position" type="x" tp:type="Time_In_Us" />
            </signal>
        </interface>
    </node>
    """

    def __init__(self, player):
        self.__playback_status = "Stopped"
        self.loop_status = "Playlist"
        self.rate = 1.0
        self.shuffle = False
        self.__position = 0
        self.volume = 1.0
        self.__minimum_rate = 1.0 # doesn't support alternative playback speed yet
        self.__maximum_rate = 1.0
        self.__can_go_next = True
        self.__can_go_previous = True
        self.__can_control = True
        self.__can_pause = True
        self.__can_play = True
        self.__can_seek = True
        self.__player = player
        self.__metadata = {}

    @property
    def PlaybackStatus(self):
        return self.__playback_status

    @property
    def Position(self):
        return self.__position

    @property
    def MinimumRate(self):
        return self.__minimum_rate

    @property
    def Maximum_Rate(self):
        return self.__maximum_rate

    @property
    def CanGoNext(self):
        return self.__can_go_next

    @property
    def CanGoPrevious(self):
        return self.__can_go_previous

    @property
    def CanControl(self):
        return self.__can_control

    @property
    def CanPause(self):
        return self.__can_pause

    @property
    def CanPlay(self):
        return self.__can_play

    @property
    def CanSeek(self):
        return self.__can_seek

    @property
    def Metadata(self):
        return self.__metadata

    @Metadata.setter
    def Metadata(self, new_data):
        self.__metadata = new_data

    def Next(self):
        self.__player.play_next()

    def Previous():
        self.__player.play_previous()

    def Pause():
        if self.__playback_status == "Playing":
            self.__player.play_pause()
            self.__playback_status = "Paused"

    def PlayPause():
        self.__player.play_pause()
        self.__playback_status = "Playing" if self.__playback_status == "Paused" else "Paused"

    def Play():
        if self.__playback_status == "Paused":
            self.__player.play_pause()
            self.__playback_status = "Playing"

    def Stop():
        self.__playback_status = "Stopped"
        self.player.stop()

    def Seek(Offset):
        self.player.seek(Offset)

    def SetPosition(TrackId, Position):
        pass

    def OpenUri(Uri):
        pass


class MPRIS2TracklistService():
    """
    <node name="/Track_List_Interface">
        <interface name="org.mpris.MediaPlayer2.ewave.TrackList">
            <tp:mapping name="Metadata_Map" array-name="Metadata_Map_List">
            <tp:member type="s" name="Attribute" />
            <tp:member type="v" name="Value" />
            </tp:mapping>
            <tp:simple-type name="Uri" type="s" />
            <method name="GetTracksMetadata" tp:name-for-bindings="Get_Tracks_Metadata">
                <arg direction="in" name="TrackIds" type="ao" tp:type="Track_Id[]" />
                <arg direction="out" type="aa{sv}" tp:type="Metadata_Map[]" name="Metadata" />
            </method>
            <method name="AddTrack" tp:name-for-bindings="Add_Track">
                <arg direction="in" type="s" tp:type="Uri" name="Uri" />
                <arg direction="in" type="o" tp:type="Track_Id" name="AfterTrack" />
                <arg direction="in" type="b" name="SetAsCurrent" />
            </method>
            <method name="RemoveTrack" tp:name-for-bindings="Remove__Track">
                <arg direction="in" type="o" tp:type="Track_Id" name="TrackId" />
            </method>
            <method name="GoTo" tp:name-for-bindings="Go_To">
                <arg direction="in" type="o" tp:type="Track_Id" name="TrackId" />
            </method>
            <property name="Tracks" type="ao" tp:type="Track_Id[]" tp:name-for-bindings="Tracks" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="invalidates" />
            </property>
            <property name="CanEditTracks" type="b" tp:name-for-bindings="Can_Edit_Tracks" access="read">
                <annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true" />
            </property>
            <signal name="TrackListReplaced" tp:name-for-bindings="Track_List_Replaced">
                <arg name="Tracks" type="ao" tp:type="Track_Id[]" />
                <arg name="CurrentTrack" type="o" tp:type="Track_Id" />
            </signal>
            <signal name="TrackAdded" tp:name-for-bindings="Track_Added">
                <arg type="a{sv}" tp:type="Metadata_Map" name="Metadata" />
                <arg type="o" tp:type="Track_Id" name="AfterTrack" />
            </signal>
            <signal name="TrackRemoved" tp:name-for-bindings="Track_Removed">
                <arg type="o" tp:type="Track_Id" name="TrackId" />
            </signal>
            <signal name="TrackMetadataChanged" tp:name-for-bindings="Track_Metadata_Changed">
                <arg type="o" tp:type="Track_Id" name="TrackId" />
                <arg type="a{sv}" tp:type="Metadata_Map" name="Metadata" />
            </signal>
        </interface>
    </node>
    """

    def __init__(self, player):
        self.__player = player
        self.__tracklist = player.get_tracklist()
        self.__track_ids = [self.__tracklist.index(x) for x in self.__tracklist]
        self.__can_edit_tracks = False

    @property
    def Tracks(self):
        return self.__track_ids

    @property
    def CanEditTracks(self):
        return self.__can_edit_tracks

    # These won't be used as dbus clients shouldn't modify this, imo at least, but they need to be implemented anyway
    def TrackListReplaced(self, Tracks, CurrentTrack):
        pass

    def TrackAdded(self, Metadata, AfterTrack):
        pass

    def TrackRemoved(self, TrackId):
        pass

    def TrackMetadataChanged(self, TrackId, Metadata):
        pass


def init_bus(player):
    loop = GLib.MainLoop()
    bus = SessionBus()
    bus.publish("org.freedestop.MediaPlayer2.ewave", MPRIS2Service(), ("Player", MPRIS2PlayerService(player)), ("Tracklist", MPRIS2TracklistService(player)))
    loop.run()