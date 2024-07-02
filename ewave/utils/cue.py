from re import findall, split
from dataclasses import dataclass, field

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
    try:
        cue = open(file, "r", errors="ignore")
        current_track = 0
        for line in cue.readlines():
            print(line)
            tokens = line.strip().split(" ")
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

def strtime_to_sec(timestamp):
    mins, sec, frames = timestamp.split(":")
    return (60 * int(mins)) + int(sec) + (int(frames) / 75)