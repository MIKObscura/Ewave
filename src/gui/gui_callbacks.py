from efl.elementary import StandardWindow, Icon, Genlist, GenlistItemClass
from efl.elementary import ELM_GENLIST_ITEM_NONE
from efl.emotion import Emotion
from binascii import b2a_hex
from os import urandom, path
from math import isclose
from random import sample
from pathlib import Path
import utils.player_utils as player_utils
import utils.cue as cue
from gui.main_windows import PLACEHOLDER_IMG
from gui.player_controls import PLAY_MODES

def ch_progress(obj, playback, time_bar):
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


def ch_track_cue(obj, player_controls, playback, main):
    """
    Changes track if it's a cue file
    """
    if player_controls.play_mode != PLAY_MODES["CUE"]:
        return
    position = playback.position_get()
    next_track, index = which_is_close(player_controls.player_queue, position)
    if next_track:
        if player_controls.repeat_mode:
            playback.position_set(player_controls.get_current_track().timestamp)
            return
        player_controls.current_track = index
        main.title.text_set(player_controls.get_current_track().title)
        main.artist.text_set(format_artists(player_controls.get_current_track().artists))


def which_is_close(arr, el):
    """
    returns an element and its index if it's close to the given element and bigger, returns False and 0 if not
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


def ch_playpause(obj, title, album, artist, cover, player_controls, playback):
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
            set_metadata(title, album, artist, meta, cover)
        player_controls.stopped = False
    obj.content_get().standard_set(playing_icon(obj.content_get().standard_get()))
    playback.play_set(not playback.play_get())


def stop_player(obj, main, playback, player_controls, time_bar):
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


def set_metadata(title_zone, album_zone, artist_zone, meta, cover):
    """
    Puts the audio metadata in the window
    """
    # this is very ugly and dumb but for some reasons efl's Image widget with memfile_set wouldn't work so it's the only way I found
    # to display the image from the audio metadata
    tmp_filename_bin = path.join(path.abspath("/tmp"), F"{b2a_hex(urandom(10)).decode('ascii')}.bin")
    try:
        cover_data = meta["pictures"][0].data
        with open(tmp_filename_bin, "wb") as raw_img:
            raw_img.write(cover_data)
        cover.file_set(tmp_filename_bin)
    except IndexError:
        cover.file_set(PLACEHOLDER_IMG)
    #cover.memfile_set(meta["pictures"][0].data, len(meta["pictures"][0].data), format="jpeg") why no work ??????
    title_zone.text_set(meta['tags'].title[0])
    try:
        album_zone.text_set(meta['tags'].album[0])
    except AttributeError:
        album_zone.text_set(meta['tags'].title[0])
    artist_zone.text_set(format_artists(meta['tags'].artist))


def ch_volume(obj, playback):
    """
    Change the volume
    """
    new_vol = obj.value_get()
    playback.audio_volume_set(new_vol)
    if new_vol == 0:
        obj.content_get().standard_set("audio-volume-muted")
    elif new_vol != 0 and obj.content_get().standard_get() == "audio-volume-muted":
        obj.content_get().standard_set("audio-volume")


def set_dir(obj, event_info, player_controls, playback, main):
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
    player_controls.current_track = 0
    playback.file_set(str(player_controls.get_current_track()))
    playback.play_set(False)
    set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(player_controls.get_current_track()), main.cover)


def set_cue(obj, event_info, main, playback, player_controls):
    if not event_info.endswith(".cue"):
        print("Error: not a cue sheet")
        return
    dirname = path.dirname(event_info)
    player_controls.play_mode = PLAY_MODES["CUE"]
    cue_info = cue.parse_cue(event_info)
    playback.file_set(path.join(dirname, cue_info["file"]))
    player_controls.player_queue = cue_info["tracklist"]
    player_controls.current_track = 0
    main.title.text_set(player_controls.get_current_track().title)
    main.album.text_set(cue_info["album"])
    main.artist.text_set(cue_info["artist"])


def add_to_queue(obj, event_info, player_controls, main, playback):
    if player_controls.play_mode == PLAY_MODES["CUE"]:
        return
    else:
        if Path(event_info).suffix.replace('.', '') not in player_utils.EXTENSIONS:
            return
        player_controls.player_queue.append(event_info)
        if playback.file_get() is None:
            playback.file_set(str(player_controls.get_current_track()))
            set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(player_controls.get_current_track()), main.cover)


def set_playlist(obj, event_info, player_controls, playback, main):
    player_controls.play_mode = PLAY_MODES["PLAYLIST"]
    pl = player_utils.parse_playlist(event_info)
    player_controls.player_queue = pl
    player_controls.current_track = 0
    playback.file_set(str(player_controls.get_current_track()))
    set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(player_controls.get_current_track()), main.cover)


def format_artists(artist_list):
    return " & ".join(artist_list)


def play_next(obj, player_controls, playback, main):
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
        if player_controls.repeat_mode and isinstance(obj, Emotion):
            playback.position_set(0)
            return
        try:
            player_controls.current_track += 1
            new_track = player_controls.get_current_track()
            playback.file_set(str(new_track))
            set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(new_track), main.cover)
            player_controls.play.content_get().standard_set("media_player/pause")
            playback.play_set(True)
        except IndexError:
            stop_player(obj)


def play_prev(obj, player_controls, playback, main, time_bar):
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
            set_metadata(main.title, main.album, main.artist, player_utils.get_metadata(prev_track), main.cover)
        except IndexError:
            time_bar.value_set(0)
            playback.position_set(0)


def toggle_repeat(obj, player_controls):
    """
    Toggles the repeat state
    In repeat state, the currently playing track will restart when finished
    """
    player_controls.repeat.style_set("anchor" if player_controls.repeat.style_get() == "default" else "default")
    player_controls.repeat_mode = not player_controls.repeat_mode
    if player_controls.repeat_mode:
        player_controls.repeat.content_get().show()
    else:
        player_controls.repeat.content_get().hide()


def toggle_shuffle(obj, player_controls, playback):
    """
    Toggles the shuffle state
    When in shuffle state, the play queue is shuffled,
    when disabling shuffle, the play queue is put back at
    its original state
    """
    player_controls.shuffle.style_set("anchor" if player_controls.shuffle.style_get() == "default" else "default")
    if player_controls.play_mode == PLAY_MODES["CUE"]: # no idea how to implement that yet
        return
    player_controls.shuffle_mode = not player_controls.shuffle_mode
    if player_controls.shuffle_mode:
        current_track = player_controls.get_current_track()
        player_controls.unshuffled_queue = player_controls.player_queue
        player_controls.player_queue = sample(player_controls.player_queue, len(player_controls.player_queue))
        try:
            if player_controls.player_queue[0] != current_track: # make sure the current track is the first in the shuffled list
                index = player_controls.player_queue.index(current_track)
                old_first = player_controls.player_queue[0]
                player_controls.player_queue[0] = current_track
                player_controls.player_queue[index] = old_first
        except IndexError:
            return
        player_controls.current_track = 0
    else:
        player_controls.player_queue = player_controls.unshuffled_queue
        try:
            player_controls.current_track = player_controls.player_queue.index(Path(playback.file_get()))
        except ValueError:
            player_controls.current_track = player_controls.player_queue.index(playback.file_get())
        except TypeError: # happens when the list is empty
            return

def seek_backward(obj, playback):
    curr_pos = playback.position_get()
    curr_pos -= 10
    if curr_pos < 0:
        playback.position_set(0)
    else:
        playback.position_set(curr_pos)

def seek_forward(obj, playback, player_controls, main):
    curr_pos = playback.position_get()
    curr_pos += 10
    if curr_pos > playback.play_length_get():
        play_next(obj, player_controls, playback, main)
    else:
        playback.position_set(curr_pos)


def glic_text_get(obj, part, item_data):
    """
    Used by GenlistItemClass to set the text of the items
    """
    track_data = player_utils.get_metadata(item_data)
    return F"{format_artists(track_data['tags'].artist)} - {track_data['tags'].title[0]}"

def glic_text_get_cue(obj, part, item_data):
    return F"{format_artists(item_data.artists)} - {item_data.title}"

def glic_content_get(obj, part, item_data):
    return Icon(obj, standard="media-record")

def glic_content_get_playing(obj, part, item_data):
    return Icon(obj, standard="media_player/play")

def reorder_queue(obj, a, player_controls):
    """
    Updates the order of the play queue after a
    track in the list has been moved
    """
    curr_track = player_controls.get_current_track()
    new_list = []
    for i in range(len(player_controls.player_queue)):
        new_list.append(obj.nth_item_get(i).data_get())
    player_controls.player_queue = new_list
    curr_track_index = player_controls.player_queue.index(curr_track)
    player_controls.current_track = curr_track_index # in case the currently playing track moved

def sh_queue(obj, player_controls):
    """
    Displays a window containing the play queue
    """
    list_item = None
    list_item_playing = None
    queue_view = StandardWindow("queue", "Player Queue", autodel=True, borderless=False, size=(500,500))
    queue_list = Genlist(queue_view, reorder_mode=True)
    if player_controls.play_mode == PLAY_MODES["CUE"]:
        list_item = GenlistItemClass(item_style="one_icon", text_get_func=glic_text_get_cue, content_get_func=glic_content_get)
        list_item_playing = GenlistItemClass(item_style="one_icon", text_get_func=glic_text_get_cue, content_get_func=glic_content_get_playing)
    else:
        list_item = GenlistItemClass(item_style="one_icon", text_get_func=glic_text_get, content_get_func=glic_content_get)
        list_item_playing = GenlistItemClass(item_style="one_icon", text_get_func=glic_text_get, content_get_func=glic_content_get_playing)
    for t in player_controls.player_queue:
        if t == player_controls.get_current_track():
            queue_list.item_append(list_item_playing, t, flags=ELM_GENLIST_ITEM_NONE)
        else:
            queue_list.item_append(list_item, t, flags=ELM_GENLIST_ITEM_NONE)

    queue_list.callback_moved_add(reorder_queue, player_controls)
    queue_view.resize_object_add(queue_list)
    queue_list.show()
    queue_view.show()


def custom_filter_cue(is_dir, path, data):
    return not is_dir and path.endswith(".cue")