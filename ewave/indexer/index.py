import glob
from pathlib import Path
import ewave.utils.cue as cue
import ewave.indexer.database as db
import sqlite3
import os
import taglib
import ffmpeg

EXTENSIONS = ["flac", "mp3", "wav", "ogg", "m4a", "aac", "alac"]

def find_files():
    files = []
    for e in EXTENSIONS:
        files += glob.glob(str(Path("~").expanduser()) + F"/Music/**/*.{e}", recursive=True)
    return files

def find_cues():
    return glob.glob(str(Path("~").expanduser()) + "/Music/**/*.cue", recursive=True)

def get_tracknumber(string):
    try:
        return int(string)
    except ValueError:
        return int(string.split("/")[0])

def make_index():
    files = find_files()
    cues = find_cues()
    cue_files = [os.path.splitext(cue.get_linked_file(a))[0] for a in cues]
    cue_files = list(set(cue_files))
    files_no_cue = [x for x in files if os.path.splitext(os.path.basename(x))[0] not in cue_files]
    #index_audio(files_no_cue)
    index_cues(cues, cue_files)

def index_files(files):
    for f in files:
        print(f)
        fileTags = taglib.File(f)
        meta = fileTags.tags
        artist = ""
        album = ""
        title = ""
        duration = fileTags.length
        try:
            artist = " & ".join(meta["ARTIST"])
        except KeyError:
            continue
        try:
            title = meta["TITLE"][0]
        except (KeyError, IndexError):
            continue
        try:
            album = meta["ALBUM"][0]
        except (KeyError, IndexError):
            album = meta["TITLE"][0]
        tracknumber = 1
        try:
            tracknumber = get_tracknumber(meta["TRACKNUMBER"][0])
        except (KeyError, IndexError):
            tracknumber = 1
        db.insert_file(f, artist, album, title, duration, tracknumber)

def index_cues(cues, linked_files):
    for c in cues:
        print(c)
        parsed_cue = cue.parse_cue(c)
        if isinstance(parsed_cue, list): # if it's a list, that means it has multiple files (not handled for now)
            break
        timestamp = 0
        for t in parsed_cue['tracklist']:
            try:
                db.insert_cue(c, cue.get_linked_file(c), " & ".join(t.artists), parsed_cue["album"], t.title, t.timestamp - timestamp, t.timestamp)
                timestamp = t.timestamp
            except Exception:
                pass
        print(parsed_cue)