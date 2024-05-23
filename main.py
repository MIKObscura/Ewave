import ewave.gui.gui_main as gui_main
import ewave.cli
import efl.elementary as elm
import efl.emotion as em
import ewave.mpris
from ewave.gui.player_interface import PlayerInterface

if __name__=="__main__":
    elm.init()
    em.init()
    gui_elems = gui_main.init_gui()
    player = PlayerInterface(gui_elems)
    ewave.cli.init_cli(gui_elems)
    #mpris.init_bus(player)
    elm.run()
    em.shutdown()