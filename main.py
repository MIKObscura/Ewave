import player
import gui
import efl.elementary as elm
import efl.emotion as em

FILE = "/home/mikobscura/Bureau/Music/Other/C/covet - effloresce/covet - effloresce - 01 shibuya (ft San Holo).flac"

if __name__=="__main__":
    elm.init()
    em.init()
    gui.init_gui()
    meta = player.get_metadata(FILE)
    title = gui.playing.child_get(0, 4)
    album_zone = gui.playing.child_get(0, 5)
    artist = gui.playing.child_get(0, 6)
    gui.set_metadata(title, album_zone, artist, meta)
    gui.playback.file_set(FILE)
    elm.run()
    em.shutdown()