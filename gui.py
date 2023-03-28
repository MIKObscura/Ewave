from efl.elementary import Box, StandardWindow, Button, Icon, Table, Photo, Label, Progressbar
from efl.elementary import exit as elm_exit
from efl.emotion import Emotion
import efl.evas as evas
from binascii import b2a_hex
from os import urandom, path
import player

PLACEHOLDER_IMG = path.abspath("img/202377.png")

class MainWindow(StandardWindow):
    def __init__(self) -> None:
        super().__init__("main", "Ewave", autodel=True, borderless=False, size=(1200,800))
        self.callback_delete_request_add(lambda o: elm_exit())

class HeaderButton(Button):
    def __init__(self, parent, content, text) -> None:
        super().__init__(parent, content=content, text=text, style="anchor", scale=1.2)

class MetaTextDisplay(Label):
    def __init__(self, parent, text) -> None:
        super().__init__(parent, text=F"<b>{text}</b>", size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_HORIZ, scale=2)

class PlayerController(Box):
    def __init__(self, parent) -> None:
        super().__init__(parent, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_BOTH, horizontal=True)

        # Elements
        # Previous
        ic_prev = Icon(self, standard="media_player/prev")
        self.prev = Button(self, content=ic_prev, scale=1.8)
        self.pack_end(self.prev)

        # Play/Pause
        ic_play = Icon(self, standard="media_player/play")
        self.play = Button(self, content=ic_play, scale=1.8)
        self.pack_end(self.play)

        # Next
        ic_next = Icon(self, standard="media_player/next")
        self.b_next = Button(self, content=ic_next, scale=1.8)
        self.pack_end(self.b_next)

        # Stop
        ic_stop = Icon(self, standard="media_player/stop")
        self.stop = Button(self, content=ic_stop, scale=1.8)
        self.stop.callback_pressed_add(stop_player)
        self.pack_end(self.stop)

        self.prev.show()
        self.play.show()
        self.b_next.show()
        self.stop.show()

        # Misc
        self.stopped = False


def ch_progress(obj):
    """
    Updates the progressbar based on the position in the file
    """
    duration = playback.play_length_get()
    position = playback.position_get()
    try:
        percent = position / duration
        time_bar.value_set(percent)
    except ZeroDivisionError:
        return

def playing_icon(ic):
    """
    Switches between play and pause icons
    """
    return "media_player/play" if ic == "media_player/pause" else "media_player/pause"

def ch_playpause(obj, title, album, artist):
    """
    Sets the play state and icon of the play/pause icon
    If the player was stopped, set the audio metadata
    """
    if player_controls.stopped:
        meta = player.get_metadata(playback.file_get())
        set_metadata(title, album, artist, meta)
        player_controls.stopped = False
    obj.content_get().standard_set(playing_icon(obj.content_get().standard_get()))
    playback.play_set(not playback.play_get())

def stop_player(obj):
    """
    Stops the player and removes the audio metadata display
    """
    playback.play_set(False)
    cover.file_set(PLACEHOLDER_IMG)
    play_button = player_controls.play
    player_controls.stopped = True
    play_button.content_get().standard_set("media_player/play")
    playing.child_get(0, 4).text_set("<b>Nothing playing!</b>")
    playing.child_get(0, 5).text_set(" ")
    playing.child_get(0, 6).text_set(" ")
    time_bar.value_set(0)
    playback.position_set(0)

def set_metadata(title_zone, album_zone, artist_zone, meta):
    """
    Puts the audio metadata in the window
    """
    # this is very ugly and dumb but for some reasons efl's Image with memfile_set wouldn't work so it's the only way I found 
    # to display the image from the audio metadata
    tmp_filename_bin = path.join(path.abspath("/tmp"), F"{b2a_hex(urandom(10)).decode('ascii')}.bin")
    with open(tmp_filename_bin, "wb") as raw_img:
        raw_img.write(meta["pictures"][0].data)
    #cover.memfile_set(meta["pictures"][0].data, len(meta["pictures"][0].data), format="jpeg") why no work ??????
    cover.file_set(tmp_filename_bin)
    title_zone.text_set(F"<b>{meta['tags'].title[0]}</b>")
    try:
        album_zone.text_set(F"<b>{meta['tags'].album[0]}</b>")
    except AttributeError:
        album_zone.text_set(F"<b>{meta['tags'].title[0]}</b>")
    artist_zone.text_set(F"<b>{meta['tags'].artist[0]}</b>")

def init_gui():
    global win, vbx, header, main, cover, time_bar, playing, playback, player_controls
    win = MainWindow()
    playback = Emotion(win.evas, module_name="vlc")
    #playback.on_open_done_add(load_test)

    vbx = Box(win, size_hint_weight=evas.EXPAND_BOTH)
    win.resize_object_add(vbx)
    vbx.show()
    #### Header Box #####
    header = Box(vbx, size_hint_weight=evas.EXPAND_BOTH, horizontal=True, align=(0,1), size_hint_align=evas.FILL_BOTH)
    ic_home = Icon(header, standard="user-home")
    home = HeaderButton(header, text="Home", content=ic_home)
    ic_playlist = Icon(header, standard="media-eject")
    playlist = HeaderButton(header, text="Playlists", content=ic_playlist)
    header.pack_end(home)
    header.pack_end(playlist)

    playlist.show()
    ic_playlist.show()
    home.show()
    ic_home.show()
    header.show()

    #### Main Box #####
    main = Box(vbx, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_BOTH, horizontal=True)
    playing = Table(main, size_hint_weight=evas.EXPAND_BOTH)
    playing.show()
    cover = Photo(main, size=500, size_hint_weight=evas.EXPAND_BOTH, editable=False, fill_inside=False, file=PLACEHOLDER_IMG)
    title = MetaTextDisplay(main, text="Nothing Playing!")
    album = MetaTextDisplay(main, text=" ")
    artist = MetaTextDisplay(main, text=" ")

    album.show()
    title.show()
    artist.show()
    playing.pack(artist, 0, 4, 1, 1)
    playing.pack(album, 0, 5, 1, 1)
    playing.pack(title, 0, 6, 1, 1)
    main.show()
    vbx.pack_start(main)
    main.pack_end(playing)
    main.pack_start(cover)
    cover.show()

    #### Progress Bar ####
    time_bar = Progressbar(vbx, horizontal=True, value=0, size_hint_align=evas.FILL_HORIZ, size_hint_weight=evas.EXPAND_BOTH)
    time_bar.show()
    vbx.pack_end(time_bar)
    win.show()

    #### Player Buttons ####
    player_controls = PlayerController(vbx)
    player_controls.play.callback_pressed_add(ch_playpause, title, album, artist)
    player_controls.show()
    vbx.pack_end(player_controls)
    playback.on_position_update_add(ch_progress)
