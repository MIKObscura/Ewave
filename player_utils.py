import audio_metadata
from dataclasses import dataclass, field
from pathlib import Path
from time import time_ns

EXTENSIONS = ["mp3", "flac", "ogg"] # will be expanded in the future

"""
# basically C/C++ structs but in Python, currently unused but may be useful in the future
@dataclass
class Album:
    name: str
    tracklist: list[Track] = field(default_factory=list)

@dataclass
class Artist:
    name: str
    albums: list[Album] = field(default_factory=list)
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
