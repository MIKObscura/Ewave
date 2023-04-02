from efl.elementary import Box, StandardWindow, Button, Icon, Table, Photo, Label, Progressbar, Slider, Fileselector, FileselectorButton
from efl.elementary import ELM_WRAP_WORD
from efl.elementary import exit as elm_exit
from efl.emotion import Emotion
import efl.evas as evas
from binascii import b2a_hex
from os import urandom, path
from math import isclose
import player_utils
import cue

PLACEHOLDER_IMG = path.abspath("img/202377.png")
PLAY_MODES = {
    "DIR": 1,
    "CUE": 2,
    "PLAYLIST": 3
}

class MainWindow(StandardWindow):
    def __init__(self) -> None:
        super().__init__("main", "Ewave", autodel=True, borderless=False, size=(1200,800))
        self.callback_delete_request_add(lambda o: elm_exit())

class HeaderButton(Button):
    def __init__(self, parent, content, text) -> None:
        super().__init__(parent, content=content, text=text, style="anchor", scale=1.2, autorepeat=False)

class MetaTextDisplay(Label):
    def __init__(self, parent, text) -> None:
        super().__init__(parent, text=text, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_HORIZ, scale=2, style="marker", wrap_width=400, line_wrap=ELM_WRAP_WORD)

class DirPicker(Fileselector, FileselectorButton):
    def __init__(self, parent) -> None:
        FileselectorButton.__init__(self, parent=parent, style="anchor", text="Select folder", folder_only=True)

class CuePicker(Fileselector, FileselectorButton):
    def __init__(self, parent) -> None:
        FileselectorButton.__init__(self, parent=parent, style="anchor", text="Select cue")

class PlaylistPicker(Fileselector, FileselectorButton):
    def __init__(self, parent) -> None:
        FileselectorButton.__init__(self, parent=parent, style="anchor", text="Select playlist")

class FilesPicker(Fileselector, FileselectorButton):
    def __init__(self, parent) -> None:
        FileselectorButton.__init__(self, parent=parent, style="anchor", text="Add file to queue")

class PlayerController(Box):
    def __init__(self, parent) -> None:
        super().__init__(parent, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_BOTH, horizontal=True)

        # Elements
        # Previous
        ic_prev = Icon(self, standard="media_player/prev")
        self.prev = Button(self, content=ic_prev, scale=1.8)
        self.prev.callback_pressed_add(play_prev)
        self.pack_end(self.prev)

        # Play/Pause
        ic_play = Icon(self, standard="media_player/play")
        self.play = Button(self, content=ic_play, scale=1.8)
        self.pack_end(self.play)

        # Next
        ic_next = Icon(self, standard="media_player/next")
        self.b_next = Button(self, content=ic_next, scale=1.8)
        self.b_next.callback_pressed_add(play_next)
        self.pack_end(self.b_next)

        # Stop
        ic_stop = Icon(self, standard="media_player/stop")
        self.stop = Button(self, content=ic_stop, scale=1.8)
        self.stop.callback_pressed_add(stop_player)
        self.pack_end(self.stop)

        # Volume Slider
        self.volume = Slider(self, horizontal=True, span_size=100, value=1.0)
        self.volume.callback_changed_add(ch_volume)
        self.pack_end(self.volume)

        self.prev.show()
        self.play.show()
        self.b_next.show()
        self.stop.show()
        self.volume.show()

        # Misc
        self.stopped = False
        self.player_queue = []
        self.current_track = 0
        self.play_mode = 1

    def get_current_track(self):
        if self.player_queue is None:
            return None
        return self.player_queue[self.current_track]


class MainBoxDisplayPlaying(Box):
    def __init__(self, parent) -> None:
        super().__init__(parent, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_BOTH, horizontal=True)
        self.playing = Table(self, size_hint_weight=evas.EXPAND_BOTH)
        self.playing.show()
        self.cover = Photo(self, size=500, size_hint_weight=evas.EXPAND_BOTH, editable=False, fill_inside=False, file=PLACEHOLDER_IMG)
        self.title = MetaTextDisplay(self, text="Nothing Playing!")
        self.album = MetaTextDisplay(self, text=" ")
        self.artist = MetaTextDisplay(self, text=" ")

        self.album.show()
        self.title.show()
        self.artist.show()
        self.cover.show()

        self.playing.pack(self.title, 0, 4, 1, 1)
        self.playing.pack(self.album, 0, 5, 1, 1)
        self.playing.pack(self.artist, 0, 6, 1, 1)

        self.show()
        self.pack_end(self.playing)
        self.pack_start(self.cover)

"""
Functions used for callbacks
"""
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

def ch_track_cue(obj):
    """
    Changes track if it's a cue file
    """
    if player_controls.play_mode != PLAY_MODES["CUE"]:
        return
    position = playback.position_get()
    next_track, index = which_is_close(player_controls.player_queue, position)
    if next_track:
        player_controls.current_track = index
        main.title.text_set(player_controls.get_current_track().title)
        main.artist.text_set(format_artists(player_controls.get_current_track().artists))


def which_is_close(arr, el):
    """
    returns an element and its index if it's close and smaller to the given element
    """
    for a in arr:
        if isclose(a.timestamp, el, rel_tol=0.001) and el > a.timestamp:
            return [a, arr.index(a)]
    return [False, 0]

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
        if player_controls.play_mode == PLAY_MODES["CUE"]:
            pass # we don't need to do anything here, the callback handles that
        else:
            playback.file_set(str(player_controls.get_current_track()))
            meta = player_utils.get_metadata(playback.file_get())
            set_metadata(title, album, artist, meta)
        player_controls.stopped = False
    obj.content_get().standard_set(playing_icon(obj.content_get().standard_get()))
    playback.play_set(not playback.play_get())

def stop_player(obj):
    """
    Stops the player and removes the audio metadata display
    """
    main.cover.file_set(PLACEHOLDER_IMG)
    play_button = player_controls.play
    player_controls.stopped = True
    play_button.content_get().standard_set("media_player/play")
    main.title.text_set("Nothing playing!")
    main.album.text_set(" ")
    main.artist.text_set(" ")
    time_bar.value_set(0)
    playback.position_set(0)
    playback.play_set(False)
    playback.file_set(None)
    player_controls.current_track = 0

def set_metadata(title_zone, album_zone, artist_zone, meta):
    """
    Puts the audio metadata in the window
    """
    # this is very ugly and dumb but for some reasons efl's Image with memfile_set wouldn't work so it's the only way I found 
    # to display the image from the audio metadata
    tmp_filename_bin = path.join(path.abspath("/tmp"), F"{b2a_hex(urandom(10)).decode('ascii')}.bin")
    try:
        cover_data = meta["pictures"][0].data
        with open(tmp_filename_bin, "wb") as raw_img:
            raw_img.write(cover_data)
        main.cover.file_set(tmp_filename_bin)
    except IndexError:
        main.cover.file_set(PLACEHOLDER_IMG)
    #cover.memfile_set(meta["pictures"][0].data, len(meta["pictures"][0].data), format="jpeg") why no work ??????
    title_zone.text_set(meta['tags'].title[0])
    try:
        album_zone.text_set(meta['tags'].album[0])
    except AttributeError:
        album_zone.text_set(meta['tags'].title[0])
    artist_zone.text_set(" & ".join(meta['tags'].artist))

def ch_volume(obj):
    """
    Change the volume
    """
    new_vol = obj.value_get()
    playback.audio_volume_set(new_vol)

def set_dir(obj, event_info):
    """
    Sets the current directory and populate the play queue with it
    """
    player_controls.play_mode = PLAY_MODES["DIR"]
    files = player_utils.filter_files(player_utils.get_all_files(event_info))
    if len(files) == 0: # no audio file in directory
        return
    try:
        player_controls.player_queue = sorted(files, key=lambda f: int(player_utils.get_metadata(f)["tags"].tracknumber[0]))
    except AttributeError:
        player_controls.player_queue = files
    except ValueError:
        player_controls.player_queue = files
    queue_start = player_controls.player_queue[player_controls.current_track]
    playback.file_set(str(queue_start))
    playback.play_set(False)
    set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(queue_start))

def set_cue(obj, event_info):
    if not event_info.endswith(".cue"):
        return
    dirname = path.dirname(event_info)
    player_controls.play_mode = PLAY_MODES["CUE"]
    cue_info = cue.parse_cue(event_info)
    playback.file_set(path.join(dirname, cue_info["file"]))
    player_controls.player_queue = cue_info["tracklist"]
    main.title.text_set(player_controls.get_current_track().title)
    main.album.text_set(cue_info["album"])
    main.artist.text_set(cue_info["artist"])

def add_to_queue(obj, event_info):
    if player_controls.play_mode == PLAY_MODES["CUE"]:
        return
    else:
        player_controls.player_queue.append(event_info)
        if playback.file_get() is None:
            playback.file_set(player_controls.get_current_track())
            set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(player_controls.get_current_track()))

def set_playlist(obj, event_info):
    player_controls.play_mode = PLAY_MODES["PLAYLIST"]
    pl = player_utils.parse_playlist(event_info)
    player_controls.player_queue = pl
    set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(player_controls.get_current_track()))

def format_artists(artist_list):
    return " & ".join(artist_list)

def play_next(obj):
    """
    play the next track in the queue, stop the player if none after
    """
    if player_controls.play_mode == PLAY_MODES["CUE"]:
        try:
            player_controls.current_track += 1
            new_track = player_controls.get_current_track().title
            new_time = player_controls.get_current_track().timestamp
            new_artist = player_controls.get_current_track().artists
            playback.position_set(new_time)
            player_controls.play.content_get().standard_set("media_player/pause")
            playback.play_set(True)
            main.title.text_set(new_track)
            main.artist.text_set(format_artists(new_artist))
        except IndexError:
            stop_player(obj)
    else:
        try:
            player_controls.current_track += 1
            new_track = player_controls.get_current_track()
            playback.file_set(str(new_track))
            set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(new_track))
            player_controls.play.content_get().standard_set("media_player/pause")
            playback.play_set(True)
        except IndexError:
            stop_player(obj)

def play_prev(obj):
    """
    play the previous track,
    or go back to the beginning of the current track if 
    no track before or at more than 30% of the track
    """
    if player_controls.play_mode == PLAY_MODES["CUE"]:
        player_controls.current_track -= 1
        prev_track = player_controls.get_current_track().title
        prev_timestamp = player_controls.get_current_track().timestamp
        prev_artist = player_controls.get_current_track().artists
        playback.position_set(prev_timestamp)
        player_controls.play.content_get().standard_set("media_player/pause")
        playback.play_set(True)
        main.title.text_set(prev_track)
        main.artist.text_set(format_artists(prev_artist))
    else:
        if time_bar.value_get() > 0.3:
            time_bar.value_set(0)
            playback.position_set(0)
            return
        player_controls.current_track -= 1
        prev_track = None
        player_controls.play.content_get().standard_set("media_player/pause")
        playback.play_set(True)
        try:
            prev_track = player_controls.get_current_track()
            playback.file_set(str(prev_track))
            set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(prev_track))
        except IndexError:
            time_bar.value_set(0)
            playback.position_set(0)

"""
Initialize everything
"""
def init_gui():
    global win, vbx, header, main, time_bar, playback, player_controls
    win = MainWindow()
    playback = Emotion(win.evas, module_name="vlc")
    #playback.on_open_done_add(load_test)

    vbx = Box(win, size_hint_weight=evas.EXPAND_BOTH)
    win.resize_object_add(vbx)
    vbx.show()
    #### Header Box #####
    header = Box(vbx, size_hint_weight=evas.EXPAND_BOTH, horizontal=True, align=(0,1), size_hint_align=evas.FILL_BOTH)
    #ic_home = Icon(header, standard="user-home") these buttons don't serve any purpose so I'll comment them out until 
    # I find a use for them
    #home = HeaderButton(header, text="Home", content=ic_home)
    #ic_playing = Icon(header, standard="media_player/play")
    #playing = HeaderButton(header, text="Playing", content=ic_playing)
    fs = DirPicker(header)
    fs.callback_file_chosen_add(set_dir)
    cue_fs = CuePicker(header)
    cue_fs.callback_file_chosen_add(set_cue)
    playlist_fs = PlaylistPicker(header)
    playlist_fs.callback_file_chosen_add(set_playlist)
    queue_add = FilesPicker(header)
    queue_add.callback_file_chosen_add(add_to_queue)
    #header.pack_end(home)
    #header.pack_end(playing)
    header.pack_end(fs)
    header.pack_end(cue_fs)
    header.pack_end(playlist_fs)
    header.pack_end(queue_add)

    #playing.show()
    #ic_playing.show()
    #home.show()
    #ic_home.show()
    fs.show()
    cue_fs.show()
    queue_add.show()
    playlist_fs.show()
    #cue_fs.custom_filter_append(custom_filter_cue, filter_name="Cue Sheets") doesn't work for some reasons
    header.show()

    #### Main Box #####
    main = MainBoxDisplayPlaying(vbx)
    vbx.pack_start(main)

    #### Progress Bar ####
    time_bar = Progressbar(vbx, horizontal=True, value=0, size_hint_align=evas.FILL_HORIZ, size_hint_weight=evas.EXPAND_BOTH)
    time_bar.show()
    vbx.pack_end(time_bar)

    #### Player Buttons ####
    player_controls = PlayerController(vbx)
    player_controls.play.callback_pressed_add(ch_playpause, main.title, main.album, main.artist)
    player_controls.show()
    vbx.pack_end(player_controls)
    playback.on_position_update_add(ch_progress)
    playback.on_position_update_add(ch_track_cue)
    playback.on_playback_finished_add(play_next)
    #home.callback_clicked_add(ch_main_home, main_display, main)
    #playing.callback_clicked_add(ch_main_playing, main_display, main)
    win.show()
