from pandac.PandaModules import WindowProperties
from direct.showbase import ShowBase

class ShowBaseAI(ShowBase.ShowBase):
    def __init__(self, windowTitle=None):
        self.windowTitle = windowTitle
        ShowBase.ShowBase.__init__(self)

    def openMainWindow(self, *args, **kw):
        ShowBase.ShowBase.openMainWindow(self, *args, **kw)
        if self.windowTitle is not None:
            wp = WindowProperties()
            wp.setTitle(self.windowTitle)
            self.win.requestProperties(wp)
        
    def finalizeExit(self):
        # don't shut down the app when user closes the window
        pass
