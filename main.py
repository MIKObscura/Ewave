import player
import gui
import efl.elementary as elm
import efl.emotion as em
from binascii import b2a_hex
from os import urandom, path, system

FILE = ""

if __name__=="__main__":
    elm.init()
    em.init()
    gui.init_gui()
    meta = player.get_metadata(FILE)
    title = gui.playing.child_get(0, 4)
    album = gui.playing.child_get(0, 5)
    artist = gui.playing.child_get(0, 6)
    # this is very ugly and dumb but for some reasons efl's Image with memfile_set wouldn't work so it's the only way I found 
    # to display the image from the audio metadata
    tmp_filename_bin = path.join(path.abspath("/tmp"), F"{b2a_hex(urandom(10)).decode('ascii')}.bin")
    with open(tmp_filename_bin, "wb") as raw_img:
        raw_img.write(meta["pictures"][0].data)
    #cover.memfile_set(meta["pictures"][0].data, len(meta["pictures"][0].data), format="jpeg") why no work ??????
    gui.cover.file_set(tmp_filename_bin)
    title.text_set(F"<b>{meta['tags'].title[0]}</b>")
    try:
        album.text_set(F"<b>{meta['tags'].album[0]}</b>")
    except AttributeError:
        album.text_set(F"<b>{meta['tags'].title[0]}</b>")
    artist.text_set(F"<b>{meta['tags'].artist[0]}</b>")
    gui.playback.file_set(FILE)
    elm.run()
    em.shutdown()