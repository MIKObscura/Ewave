import gui
import efl.elementary as elm
import efl.emotion as em

if __name__=="__main__":
    elm.init()
    em.init()
    gui.init_gui()
    elm.run()
    em.shutdown()