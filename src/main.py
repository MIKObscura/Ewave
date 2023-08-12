import gui.gui_main as gui_main
import cli
import efl.elementary as elm
import efl.emotion as em
import mpris
from gui.player_interface import PlayerInterface

if __name__=="__main__":
    elm.init()
    em.init()
    gui_elems = gui_main.init_gui()
    player = PlayerInterface(gui_elems)
    cli.init_cli(gui_elems)
    #mpris.init_bus(player)
    elm.run()
    em.shutdown()