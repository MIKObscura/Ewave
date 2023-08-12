import audio_metadata
from dataclasses import dataclass, field
from pathlib import Path

EXTENSIONS = ["mp3", "flac", "ogg", "wav"] # will be expanded in the future

"""
General utilities for the program
"""

def get_metadata(path):
    try:
        return audio_metadata.load(path)
    except ValueError:
        return False

def get_all_files(base_dir):
    """
    searches recursively in all the dirs for files
    """
    files = []
    for file in Path(base_dir).glob("*"):
        files.append(file) if not file.is_dir() else True
    return files

def filter_files(filelist):
    """
    filter the files to keep audio files only
    """
    return list(filter(lambda f: f.name.split(".")[len(f.name.split(".")) - 1] in EXTENSIONS, filelist))

def parse_playlist(file):
    pl = []
    try:
        with open(file, "r") as playlist:
            for track in playlist:
                pl.append(track.strip())
        return pl
    except FileNotFoundError:
        return []
    except IOError:
        return []

def time_string_to_us(string):
    """
    Converts a time string formatted like this: hour:minutes:seconds to microseconds
    """
    parts = string.split(':')
    if len(parts) == 2:
        return (int(parts[0]) * 60000000) + (int(parts[1] * 1000000))
    elif len(parts) == 3:
        return (int(parts[0] * 3600000000)) + (int(parts[1]) * 60000000) + (int(parts[2] * 1000000))
    else:
        return int(parts[0]) * 1000000
