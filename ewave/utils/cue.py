from re import findall, split
from dataclasses import dataclass, field
import os

@dataclass
class Track:
    title: str
    timestamp: float
    artists: list[str] = field(default_factory=list)

def parse_cue(file):
    """
    parses the cue file and returns its infos
    """
    audio_file = None
    album = None
    artist = None
    tracks = []
    result = {}
    multi_file = False # cue sheets with multiple FILE are not handled currently, so it will just return a list of the files instead
    files_in_cue = open(file, "r", errors="ignore").read().count("FILE")
    try:
        if files_in_cue == 0:
            return None
        if files_in_cue > 1:
            multi_file = True
        cue = open(file, "r", errors="ignore")
        current_track = 0
        for line in cue.readlines():
            tokens = line.strip().split(" ")
            if multi_file:
                if tokens[0] == "FILE":
                    tracks.append(os.path.dirname(file) + "/" + " ".join(tokens[1:-1]).replace('"', '').strip())
                if len(tracks) == files_in_cue:
                    return tracks
                continue
            if tokens[0] == "REM": # comment
                continue
            elif tokens[0] == "FILE":
                result["file"] = " ".join(tokens[1:-1]).replace('"', '').strip()
                continue
            elif tokens[0] == "PERFORMER":
                if "albumartist" not in result:
                    result["albumartist"] = " ".join(tokens[1:]).replace('"', '').strip()
                else:
                    tracks[current_track].artists.append(" ".join(tokens[1:]).replace('"', '').strip())
                continue
            elif tokens[0] == "TITLE":
                if "album" not in result:
                    result["album"] = " ".join(tokens[1:]).replace('"', '').strip()
                else:
                    tracks[current_track].title = " ".join(tokens[1:]).replace('"', '').strip()
                continue
            elif tokens[0] == "INDEX" and tokens[1] == "01":
                tracks[current_track].timestamp = strtime_to_sec(tokens[2])
                continue
            elif tokens[0] == "TRACK":
                current_track = int(tokens[1]) - 1
                tracks.append(Track(None, None))
                continue
        result["tracklist"] = tracks
    except FileNotFoundError:
        pass
    return result

def get_linked_file(file):
    cue = open(file, "r", errors="ignore")
    for line in cue.readlines():
        tokens = line.strip().split(" ")
        if tokens[0] == "FILE":
            return " ".join(tokens[1:-1]).replace('"', '')
    return None

def strtime_to_sec(timestamp):
    mins, sec, frames = timestamp.split(":")
    return (60 * int(mins)) + int(sec) + (int(frames) / 75)