from direct.showbase.TkGlobal import *

class LauncherTool:
    def __init__(self, launcher):
        self.launcher = launcher
        self.toplevel = Toplevel()
        self.frame = Frame(self.toplevel)

        self.statusLabel = Label(self.frame, justify=LEFT,
                                 anchor=W, text='Status: Ok')

        self.goButton = Button(self.frame, text='Go', command=self.launcher.go)

        self.frame.pack(side=LEFT)
        self.statusLabel.pack(side=TOP, fill=X)
        self.goButton.pack(side=TOP, fill=X)

    def setStatus(self, action):
        self.statusLabel['text'] = 'Status: ' + action

        
