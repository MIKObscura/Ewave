import sqlite3

def insert_file(filename, artist, album, title, duration, tracknumber):
    index = sqlite3.connect("index")
    index_cur = index.cursor()
    index_cur.execute("insert into audio_files (filename, artist, album, title, duration, tracknumber) values (?, ?, ?, ?, ?, ?)",
        (filename, artist, album, title, duration, tracknumber))
    index.commit()
    index.close()

def insert_cue(cue, file, artist, album, title, duration, timestamp):
    index = sqlite3.connect("index")
    index_cur = index.cursor()
    index_cur.execute("insert into cue_sheets (cue, file, artist, album, title, duration, timestamp) values (?, ?, ?, ?, ?, ?, ?)",
    (cue, file, artist, album, title, duration, timestamp))
    index.commit()
    index.close()

def get_artists():
    index = sqlite3.connect("index")
    index_cur = index.cursor()
    artists = index_cur.execute("select distinct artist \
        from audio_files \
        union select distinct artist from cue_sheets \
        order by lower(artist)").fetchall()
    index.close()
    return [a[0] for a in artists]

def get_albums():
    index = sqlite3.connect("index")
    index_cur = index.cursor()
    albums = index_cur.execute("select artist, album \
        from audio_files \
        group by artist, album \
        order by lower(album)").fetchall()
    albums += index_cur.execute("select artist, album \
        from cue_sheets \
        group by artist, album \
        order by lower(album)").fetchall()
    index.close()
    return sorted(albums, key=lambda a: a[1].lower())

def get_artist_albums(artist):
    index = sqlite3.connect("index")
    index_cur = index.cursor()
    albums = index_cur.execute("select distinct album \
        from audio_files as a \
        where a.artist = ? \
        union select distinct album \
        from cue_sheets as c \
        where c.artist = ?", (artist, artist)).fetchall()
    index.close()
    return albums

def get_album_tracks(artist, album):
    index = sqlite3.connect("index")
    index_cur = index.cursor()
    tracks = index_cur.execute("select filename, title, duration, tracknumber \
        from audio_files \
        where artist=? and album=? \
        order by tracknumber", (artist, album)).fetchall()
    if len(tracks) > 0:
        index.close()
        return tracks
    tracks = index_cur.execute("select cue, file, title, timestamp, duration \
        from cue_sheets \
        where artist=? and album=? \
        order by timestamp", (artist, album)).fetchall()
    index.close()
    return tracks
