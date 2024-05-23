from efl.elementary import Box, Icon, Button, Slider
import efl.evas as evas

PLAY_MODES = {
    "DIR": 1,
    "CUE": 2,
    "PLAYLIST": 3 # changes nothing for now but was added in case
}

class PlayerController(Box):
    def __init__(self, parent) -> None:
        super().__init__(parent, size_hint_weight=evas.EXPAND_BOTH, size_hint_align=evas.FILL_BOTH, horizontal=True)

        # Elements
        # Seek backwards
        ic_seek_back = Icon(self, standard="media-seek-backward")
        self.seek_back = Button(self, content=ic_seek_back, scale=2)
        self.pack_end(self.seek_back)
        # Previous
        ic_prev = Icon(self, standard="media-skip-backward")
        self.prev = Button(self, content=ic_prev, scale=2)
        self.pack_end(self.prev)

        # Play/Pause
        ic_play = Icon(self, standard="media-playback-start")
        self.play = Button(self, content=ic_play, scale=2)
        self.pack_end(self.play)

        # Next
        ic_next = Icon(self, standard="media-skip-forward")
        self.b_next = Button(self, content=ic_next, scale=2)
        self.pack_end(self.b_next)

        # Seek forward
        ic_seek_for = Icon(self, standard="media-seek-forward")
        self.seek_for = Button(self, content=ic_seek_for, scale=2)
        self.pack_end(self.seek_for)

        # Stop
        ic_stop = Icon(self, standard="media-playback-stop")
        self.stop = Button(self, content=ic_stop, scale=2)
        self.pack_end(self.stop)

        # Repeat
        ic_repeat = Icon(self, standard="media-playlist-repeat")
        self.repeat = Button(self, content=ic_repeat, scale=2)
        self.pack_end(self.repeat)

        # Shuffle
        ic_shuffle = Icon(self, standard="media-playlist-shuffle")
        self.shuffle = Button(self, content=ic_shuffle, scale=2)
        self.pack_end(self.shuffle)

        # Volume Slider
        ic_volume = Icon(self, standard="audio-volume-high")
        self.volume = Slider(self, horizontal=True, span_size=150, value=1.0, content=ic_volume, scale=1.5)
        self.pack_end(self.volume)

        self.prev.show()
        self.play.show()
        self.b_next.show()
        self.stop.show()
        self.repeat.show()
        self.shuffle.show()
        self.volume.show()
        self.seek_back.show()
        self.seek_for.show()

        # Misc
        self.stopped = False
        self.player_queue = []
        self.unshuffled_queue = [] # used for going back to the normal queue when toggling shuffle
        self.current_track = 0
        self.pos_save = 0 # memorize the position we were at before going into shuffle mode
        self.play_mode = 1
        self.repeat_mode = False
        self.shuffle_mode = False

    def get_current_track(self):
        if not len(self.player_queue):
            return None
        return self.player_queue[self.current_track]