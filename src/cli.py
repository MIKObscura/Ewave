from argparse import ArgumentParser
from pathlib import Path
from gui.gui_callbacks import set_metadata, set_dir, set_cue, set_playlist
import utils.player_utils as player_utils

def select_files_cli(args, widgets):
    widgets["player_controls"].player_queue = args
    widgets["playback"].file_set(args[0])
    metadata = player_utils.get_metadata(Path(args[0]))
    set_metadata(widgets["main"].title, widgets["main"].album, widgets["main"].artist, metadata, widgets["main"].cover)


def select_dir_cli(args, widgets):
    set_dir(None, args, widgets["player_controls"], widgets["playback"], widgets["main"])


def select_cue_cli(args, widgets):
    set_cue(None, args, widgets["main"], widgets["playback"], widgets["player_controls"])

def select_playlist_cli(args, widgets):
    set_playlist(None, args, widgets["player_controls"], widgets["playback"], widgets["main"])

args_callbacks = {
    "filenames": select_files_cli,
    "cue": select_cue_cli,
    "playlist": select_playlist_cli,
    "dir": select_dir_cli
}

def init_cli(widgets):
    args_parser = ArgumentParser(prog="Ewave", description="python-efl based music player")
    args_group = args_parser.add_mutually_exclusive_group()
    args_group.add_argument("-f", "--filenames",
                        type=str,
                        nargs="*",
                        required=False,
                        help="Space sperated list of absolute paths to audio files (use the --cue option if you want to input a cue sheet)")
    args_group.add_argument("-c", "--cue",
                        type=str,
                        required=False,
                        help="Absolute path to a cue sheet")
    args_group.add_argument("-p", "--playlist",
                        type=str,
                        required=False,
                        help="Absolute path to a text file defining a playlist")
    args_group.add_argument("-d", "--dir",
                        type=str,
                        required=False,
                        help="Absolute path to a directory containing audio file")
    args = vars(args_parser.parse_args())
    for a in args:
        if args[a] is not None:
            args_callbacks[a](args[a], widgets)
            break