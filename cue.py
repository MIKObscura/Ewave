from re import findall

def parse_cue(file):
    """
    parses the cue file and returns its infos
    """
    audio_file = None
    album = None
    artist = None
    track_titles = []
    track_times = []
    try:
        with open(file, "r") as cue:
            for line in cue:
                if line.startswith("FILE"):
                    audio_file = findall(r'"([^"]*)"', line)[0]
                    continue
                if audio_file is None: # this is done so that the first TITLE directive (the album's title) isn't added to the tracks list
                    if line.startswith("TITLE"):
                        album = findall(r'"([^"]*)"', line)[0]
                    if line.startswith("PERFORMER"):
                        artist = findall(r'"([^"]*)"', line)[0]
                    continue
                if line.strip().startswith("TITLE"):
                    track_titles.append(findall(r'"([^"]*)"', line)[0])
                    continue
                if line.strip().startswith("INDEX 01"): # other indexes exist but they only indicate pregap and postgap
                    track_times.append(strtime_to_sec(line.strip()))
                    continue
    except FileNotFoundError:
        pass
    return {"file": audio_file, "tracklist": track_titles, "timestamps": track_times, "album": album, "artist": artist}

def strtime_to_sec(time):
    timestamp = time.split(" ")[2]
    mins, sec, frames = timestamp.split(":")
    return (60 * int(mins)) + int(sec) + (int(frames) / 75)