from efl.elementary import Table, Photo, StandardWindow, Box, Label, ELM_WRAP_WORD
import efl.evas as evas
from os import path
from efl.elementary import exit as elm_exit

PLACEHOLDER_IMG = path.abspath("src/gui/img/202377.png")
class MetaTextDisplay(Label):
    def __init__(self, parent, text) -> None:
        super().__init__(parent, text=text, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_HORIZ, scale=2, style="marker", wrap_width=400, line_wrap=ELM_WRAP_WORD)

class MainWindow(StandardWindow):
    def __init__(self) -> None:
        super().__init__("main", "Ewave", autodel=True, borderless=False, size=(1200,800))
        self.callback_delete_request_add(lambda o: elm_exit())

class MainBoxDisplayPlaying(Box):
    def __init__(self, parent) -> None:
        super().__init__(parent, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_BOTH, horizontal=True)
        self.playing = Table(self, size_hint_weight=evas.EXPAND_BOTH)
        self.playing.show()
        self.cover = Photo(self, size=500, size_hint_weight=evas.EXPAND_BOTH, editable=False, fill_inside=False, file=PLACEHOLDER_IMG)
        self.title = MetaTextDisplay(self, text="Nothing Playing!")
        self.album = MetaTextDisplay(self, text=" ")
        self.artist = MetaTextDisplay(self, text=" ")

        self.album.show()
        self.title.show()
        self.artist.show()
        self.cover.show()

        self.playing.pack(self.title, 0, 4, 1, 1)
        self.playing.pack(self.album, 0, 5, 1, 1)
        self.playing.pack(self.artist, 0, 6, 1, 1)

        self.show()
        self.pack_end(self.playing)
        self.pack_start(self.cover)