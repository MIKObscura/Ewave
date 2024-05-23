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
    try:
        with open(file, "r") as cue:
            parts = split(r"FILE \"([^\"]*)\" [a-zA-Z]*", cue.read())
            header = parts[0]
            audio_file = parts[1]
            tracks_info = split(r"\s{2}TRACK [0-9]{2} AUDIO\n" , parts[2])
            for i in header.split('\n'):
                if i.startswith("PERFORMER"):
                    artist = findall(r'"([^"]*)"', i)[0]
                if i.startswith("TITLE"):
                    album = findall(r'"([^"]*)"', i)[0]
            for t in tracks_info:
                new_track = Track(None, None)
                for i in t.split("\n"):
                    if i.strip().startswith("TITLE"):
                        new_track.title = findall(r'"([^"]*)"', i)[0]
                        continue
                    if i.strip().startswith("PERFORMER"):
                        new_track.artists.append(findall(r'"([^"]*)"', i)[0])
                        continue
                    if i.strip().startswith("INDEX 01"): # other indexes exist but they only indicate pregap and postgap
                        new_track.timestamp = strtime_to_sec(i.strip())
                if len(new_track.artists) == 0: # it means no track has a specific artist so we just use the one in the header
                    new_track.artists.append(artist)
                if new_track.title is not None: # sometimes empty whitespaces slide in so we don't want them in the list
                    tracks.append(new_track)
    except FileNotFoundError:
        pass
    return {"file": audio_file, "tracklist": tracks, "album": album, "artist": artist}

def strtime_to_sec(time):
    timestamp = time.split(" ")[2]
    mins, sec, frames = timestamp.split(":")
    return (60 * int(mins)) + int(sec) + (int(frames) / 75)