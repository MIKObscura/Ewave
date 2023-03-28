import player
import gui
import efl.elementary as elm
import efl.emotion as em

FILE = ""

if __name__=="__main__":
    elm.init()
    em.init()
    gui.init_gui()
    meta = player.get_metadata(FILE)
    title_zone = gui.playing.child_get(0, 4)
    album_zone = gui.playing.child_get(0, 5)
    artist_zone = gui.playing.child_get(0, 6)
    gui.set_metadata(title_zone, album_zone, artist_zone, meta)
    gui.playback.file_set(FILE)
    elm.run()
    em.shutdown()