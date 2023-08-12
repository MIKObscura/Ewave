import gui_callbacks
from utils.player_utils import get_metadata, time_string_to_us
import datetime

class PlayerInterface():
    """
    Class used by other part of the program to interact with the player
    """
    def __init__(self, widgets):
        self.__player_controls = widgets["player_controls"]
        self.__playback = widgets["playback"]
        self.__main = widgets["main"]
        self.__time_bar = widgets["time_bar"]

    def play_pause(self):
        gui_callbacks.ch_playpause(self.__player_controls.play, self.__main.title, self.__main.album, self.__main.artist, self.__main.cover, self.__player_controls, self.__playback)

    def volume(self, volume):
        gui_callbacks.ch_volume(self.__player_controls.volume, self.__playback, volume)

    def shuffle(self):
        gui_callbacks.toggle_shuffle(self.__player_controls.shuffle, self.__player_controls, self.__playback)

    def repeat(self):
        gui_callbacks.toggle_repeat(self.__player_controls.repeat, self.__player_controls)

    def stop(self):
        gui_callbacks.stop_player(self.__player_controls.stop, self.__main, self.__playback, self.__player_controls, self.__main, self.__time_bar)

    def seek(self, offset):
        if offset < 0:
            gui_callbacks.seek_backward(self.__player_controls.seek_back, self.__playback, -offset)
        else:
            gui_callbacks.seek_forward(self.__player_controls.seek_for, self.__playback, self.__player_controls, self.__main, offset)

    def play_next(self):
        gui_callbacks.play_next(self.__player_controls.next, self.__player_controls, self.__playback, self.__main)

    def play_previous(self):
        gui_callbacks.play_prev(self.__player_controls.prev, self.__player_controls, self.__playback, self.__main, self.__time_bar)

    def get_tracklist(self):
        return self.__player_controls.player_queue

    def get_metadata(self):
        meta = get_metadata(self.__playback.file_get())
        return {
            "mpris:trackid": meta["tags"].tracknumber[0],
            "mpris:length": time_string_to_us(meta["streaminfo"].duration),
            "mpris:artUrl": "file:///tmp/album_art.bin",
            "xesam:album": meta["tags"].album[0],
            "xesam:albumArtist": meta["tags"].albumartist,
            "xesam:artist": meta["tags"].artist,
            "xesam:comment": meta["tags"].comment,
            "xesam:title": meta["tags"].title[0],
            "xesam:url": F"file://{self.__playback.file_get()}",
            "xesam:trackNumber": meta["tags"].tracknumber[0],
            "xesam:contentCreated": datetime.date(int(meta["tags"].date[0]), 1, 1).isoformat() # it requires a full ISO8601 date even though the xesam doc says only the year is relevant, very cool
        }
