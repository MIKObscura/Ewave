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