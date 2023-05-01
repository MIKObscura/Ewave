import gui.gui_main as gui_main
import cli
import efl.elementary as elm
import efl.emotion as em

if __name__=="__main__":
    elm.init()
    em.init()
    gui_elems = gui_main.init_gui()
    cli.init_cli(gui_elems)
    elm.run()
    em.shutdown()