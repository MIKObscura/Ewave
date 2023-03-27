from efl.elementary import Box, StandardWindow, Button, Icon, Table, Photo, Label, Progressbar
from efl.elementary import exit as elm_exit
from efl.emotion import Emotion
import efl.evas as evas

class MainWindow(StandardWindow):
    def __init__(self) -> None:
        super().__init__("main", "Ewave", autodel=True, borderless=False, size=(1080,720))
        self.callback_delete_request_add(lambda o: elm_exit())

def ch_progress(obj):
    duration = playback.play_length_get()
    position = playback.position_get()
    try:
        percent = position / duration
        time_bar.value_set(percent)
    except ZeroDivisionError:
        return

def playing_icon(ic):
    return "media_player/play" if ic == "media_player/pause" else "media_player/pause"

def ch_playpause(obj):
    obj.content_get().standard_set(playing_icon(obj.content_get().standard_get()))
    playback.play_set(not playback.play_get())

def init_gui():
    global win, vbx, header, main, cover, time_bar, playing, playback
    win = MainWindow()
    playback = Emotion(win.evas, module_name="vlc")
    vbx = Box(win, size_hint_weight=evas.EXPAND_BOTH)
    win.resize_object_add(vbx)
    vbx.show()
    #### Header Box #####
    header = Box(vbx, size_hint_weight=evas.EXPAND_BOTH, horizontal=True, align=(0,1), size_hint_align=evas.FILL_BOTH)
    ic_home = Icon(header, standard="user-home")
    home = Button(header, text="Home", content=ic_home, style="anchor", scale=1.2)
    ic_playlist = Icon(header, standard="media-eject")
    playlist = Button(header, text="Playlists", content=ic_playlist, style="anchor", scale=1.2)
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
    cover = Photo(main, size=500, size_hint_weight=evas.EXPAND_BOTH, editable=False, fill_inside=False)
    title = Label(main, text="<b>Title</b>", size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_HORIZ, scale=2)
    album = Label(main, text="<b>Album</b>", size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_HORIZ, scale=2)
    artist = Label(main, text="<b>Artist</b>", size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_HORIZ, scale=2)

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
    player_controls = Box(vbx, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_BOTH, horizontal=True)
    ic_prev = Icon(player_controls, standard="media_player/prev")
    prev = Button(player_controls, content=ic_prev, scale=1.8)
    player_controls.pack_end(prev)

    ic_play = Icon(player_controls, standard="media_player/play")
    play = Button(player_controls, content=ic_play, scale=1.8)
    play.callback_pressed_add(ch_playpause)
    player_controls.pack_end(play)

    ic_next = Icon(player_controls, standard="media_player/next")
    b_next = Button(player_controls, content=ic_next, scale=1.8)
    player_controls.pack_end(b_next)

    ic_stop = Icon(player_controls, standard="media_player/stop")
    stop = Button(player_controls, content=ic_stop, scale=1.8)
    stop.callback_pressed_add(lambda x: playback.play_set(False))
    player_controls.pack_end(stop)
    
    stop.show()
    b_next.show()
    play.show()
    prev.show()
    player_controls.show()
    vbx.pack_end(player_controls)
    playback.on_position_update_add(ch_progress)

    #return [win, header, vbx, main, playing, cover, time_bar] # this is done to access them later when we need to edit some of them