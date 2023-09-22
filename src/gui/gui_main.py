from efl.elementary import Box, Button, Progressbar, Fileselector, FileselectorButton
from efl.emotion import Emotion
import efl.evas as evas
from gui.main_windows import MainBoxDisplayPlaying, MainWindow
from gui.player_controls import PlayerController
from gui.gui_callbacks import *


class HeaderButton(Button):
    def __init__(self, parent, content, text) -> None:
        super().__init__(parent, content=content, text=text, style="anchor", scale=1.2, autorepeat=False)


class FSButton(Fileselector, FileselectorButton):
    def __init__(self, *args, **kwargs) -> None:
        FileselectorButton.__init__(self, *args, **kwargs)


"""
Initialize everything
"""
def init_gui():
    win = MainWindow()
    vbx = Box(win, size_hint_weight=evas.EXPAND_BOTH)
    main = MainBoxDisplayPlaying(vbx)
    playback = Emotion(win.evas, module_name="vlc")
    player_controls = PlayerController(vbx)

    win.resize_object_add(vbx)
    vbx.show()
    #### Header Box #####
    header = Box(vbx, size_hint_weight=evas.EXPAND_BOTH, horizontal=True, align=(0,1), size_hint_align=evas.FILL_BOTH)
    fs = FSButton(parent=header, style="anchor", text="Select folder", folder_only=True)
    cue_fs = FSButton(parent=header, style="anchor", text="Select cue")
    playlist_fs = FSButton(parent=header, style="anchor", text="Select playlist")
    playlist_fs.callback_file_chosen_add(set_playlist, player_controls, playback, main)
    queue_add = FSButton(parent=header, style="anchor", text="Add file to queue", multi_select=True) # multi_select doesn't seem to work
    queue_viewer = Button(header, text="View queue")
    header.pack_end(fs)
    header.pack_end(cue_fs)
    header.pack_end(playlist_fs)
    header.pack_end(queue_add)
    header.pack_end(queue_viewer)

    fs.show()
    cue_fs.show()
    queue_add.show()
    playlist_fs.show()
    queue_viewer.show()
    header.show()

    #### Main Box #####
    vbx.pack_start(main)

    bottom = Box(vbx, size_hint_weight=evas.EXPAND_HORIZ, size_hint_align=evas.FILL_HORIZ, padding=(0, 30))
    bottom.show()

    #### Progress Bar ####
    time_bar = Progressbar(vbx, horizontal=True, value=0, size_hint_align=evas.FILL_HORIZ, size_hint_weight=evas.EXPAND_BOTH)
    time_bar.show()
    bottom.pack_end(time_bar)

    # add all the callbacks
    player_controls.volume.callback_changed_add(ch_volume, playback)
    player_controls.shuffle.callback_pressed_add(toggle_shuffle, player_controls, playback)
    player_controls.repeat.callback_pressed_add(toggle_repeat, player_controls)
    player_controls.stop.callback_pressed_add(stop_player, main, playback, player_controls, time_bar)
    player_controls.seek_for.callback_pressed_add(seek_forward, playback, player_controls, main)
    player_controls.b_next.callback_pressed_add(play_next, player_controls, playback, main)
    player_controls.prev.callback_pressed_add(play_prev, player_controls, playback, main, time_bar)
    player_controls.seek_back.callback_pressed_add(seek_backward, playback)
    player_controls.play.callback_pressed_add(ch_playpause, main.title, main.album, main.artist, main.cover, player_controls, playback)
    fs.callback_file_chosen_add(set_dir, player_controls, playback, main)
    cue_fs.callback_file_chosen_add(set_cue, main, playback, player_controls)
    queue_add.callback_file_chosen_add(add_to_queue, player_controls, main, playback)
    queue_viewer.callback_pressed_add(sh_queue, player_controls)
    playback.on_position_update_add(ch_progress, playback, time_bar)
    playback.on_position_update_add(ch_track_cue, player_controls, playback, main)
    playback.on_playback_finished_add(play_next, player_controls, playback, main)

    player_controls.show()
    bottom.pack_end(player_controls)
    vbx.pack_end(bottom)
    win.show()
    return {"playback": playback, "player_controls": player_controls, "main": main, "time_bar": time_bar} # return them so they can be used elsewehere
