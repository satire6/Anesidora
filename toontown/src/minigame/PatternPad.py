"""PatternPad module: contains the PatternPad class"""

from pandac.PandaModules import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *

class PatternPad(DirectFrame):
    """PatternPad class: pad used by the pattern matching game
    with four buttons, basically like a Simon
    """

    ButtonNames = ('upButton', 'rightButton',
                   'downButton', 'leftButton',)

    buttonNormalScale = 1.
    buttonPressScale = 1.1

    buttonNormalColor = Point4(1,1,1,1)
    buttonDisabledColor = Point4(.7,.7,.7,1)

    def __init__(self, parent = aspect2d, **kw):
        """__init__(self, list of functions)
        create the pad and its four buttons
        'callbacks' should contain four callback functions
        buttons are ordered clockwise from top
        """

        # PatternPad's button event handlers
        # these will chain the client's button event handlers
        self.__pressHandlers = (
            lambda db, self=self: self.__pressButton(0),
            lambda db, self=self: self.__pressButton(1),
            lambda db, self=self: self.__pressButton(2),
            lambda db, self=self: self.__pressButton(3),
            )
        self.__releaseHandlers = (
            lambda db, self=self: self.__releaseButton(0),
            lambda db, self=self: self.__releaseButton(1),
            lambda db, self=self: self.__releaseButton(2),
            lambda db, self=self: self.__releaseButton(3),
            )
        self.__enterHandlers = (
            lambda db, self=self: self.__enterButton(0),
            lambda db, self=self: self.__enterButton(1),
            lambda db, self=self: self.__enterButton(2),
            lambda db, self=self: self.__enterButton(3),
            )
        self.__exitHandlers = (
            lambda db, self=self: self.__exitButton(0),
            lambda db, self=self: self.__exitButton(1),
            lambda db, self=self: self.__exitButton(2),
            lambda db, self=self: self.__exitButton(3),
            )

        optiondefs = (
            ('callbacks',           None,                self.setCallbacks),
            # these handler parameters should NOT be set by a client;
            # see setPressCallback, setReleaseCallback, etc., below
            ('pressHandlers',  self.__pressHandlers,    self.setPressHandlers),
            ('releaseHandlers',self.__releaseHandlers,self.setReleaseHandlers),
            ('enterHandlers',  self.__enterHandlers,    self.setEnterHandlers),
            ('exitHandlers',   self.__exitHandlers,     self.setExitHandlers),
            ('frameColor',            (0,0,0,0),        None),
            ('buttons_clickSound',    None,             None),
            ('buttons_rolloverSound', None,             None),
            )
        self.defineoptions(kw, optiondefs, dynamicGroups = ('buttons',))

        DirectFrame.__init__(self, parent)

        gui = loader.loadModel("phase_3.5/models/gui/matching_game_gui")
        self['geom'] = gui.find("**/pink_circle")

        # create the buttons
        bnames = ('trumpet', 'guitar', 'drums', 'piano')
        bpos = ((-0.005, 0,  0.305),
                ( 0.448, 0,  0.090),
                ( 0.029, 0, -0.348),
                (-0.419, 0,  0.043))
        for i in range(0,len(bnames)):
            buttonGeom = gui.find("**/" + bnames[i])
            buttonGeomRollover = gui.find("**/" + bnames[i] + "_rollover")
            buttonGeomPressed = buttonGeomRollover
            buttonGeomDisabled = buttonGeom
            self.createcomponent(self.ButtonNames[i], (), 'buttons',
                                 DirectButton, (),
                                 parent = self,
                                 pos = bpos[i],
                                 frameColor = (0,0,0,0),
                                 pressEffect = 0, # we'll do our own effect
                                 image = (buttonGeom,
                                          buttonGeomPressed,
                                          buttonGeomRollover,
                                          buttonGeomDisabled,),
                                 image3_color = self.buttonDisabledColor,
                                 )

        buttonGeomDisabled.removeNode()
        gui.removeNode()

        # obligatory init call
        self.initialiseoptions(PatternPad)

        # clear out the user handlers
        self.setPressCallback(None)
        self.setReleaseCallback(None)
        self.setEnterCallback(None)
        self.setExitCallback(None)


    def destroy(self):
        del self.__pressHandlers
        del self.__releaseHandlers
        del self.__enterHandlers
        del self.__exitHandlers
        self.setPressCallback(None)
        self.setReleaseCallback(None)
        self.setEnterCallback(None)
        self.setExitCallback(None)
        for name in self.ButtonNames:
            self.destroycomponent(name)
        DirectFrame.destroy(self)

    def __getButtons(self):
        buttons = []
        for name in self.ButtonNames:
            buttons.append(self.component(name))
        return buttons

    def disable(self):
        buttons = self.__getButtons()
        for button in buttons:
            button['state'] = DGG.DISABLED

    def enable(self):
        buttons = self.__getButtons()
        for button in buttons:
            button['state'] = DGG.NORMAL

    # these can be set by a client -- callback
    # will be called with index of button
    def setPressCallback(self, callback):
        self.__clientPressCallback = callback
    def setReleaseCallback(self, callback):
        self.__clientReleaseCallback = callback
    def setEnterCallback(self, callback):
        self.__clientEnterCallback = callback
    def setExitCallback(self, callback):
        self.__clientExitCallback = callback

    # handler called when self['callbacks'] is set
    def setCallbacks(self):
        buttons = self.__getButtons()
        if self['callbacks'] == None:
            for button in buttons:
                button['command'] = None
        else:
            for i in range(0,len(buttons)):
                buttons[i]['command'] = self['callbacks'][i]

    def __bindButtonHandlers(self, event, handlerTypeName):
        buttons = self.__getButtons()
        if self[handlerTypeName] == None:
            for button in buttons:
                button.unbind(event)
        else:
            for i in range(0,len(buttons)):
                buttons[i].bind(event, self[handlerTypeName][i])

    # handler called when self['pressHandlers'] is set
    def setPressHandlers(self):
        self.__bindButtonHandlers(DGG.B1PRESS, 'pressHandlers')
    # handler called when self['releaseHandlers'] is set
    def setReleaseHandlers(self):
        self.__bindButtonHandlers(DGG.B1RELEASE, 'releaseHandlers')
    # handler called when self['enterHandlers'] is set
    def setEnterHandlers(self):
        self.__bindButtonHandlers(DGG.ENTER, 'enterHandlers')
    # handler called when self['exitHandlers'] is set
    def setExitHandlers(self):
        self.__bindButtonHandlers(DGG.EXIT, 'exitHandlers')

    # button handlers
    def __pressButton(self, index):
        # scale the button up
        button = self.__getButtons()[index]
        button.setScale(self.buttonPressScale)
        if self.__clientPressCallback != None:
            self.__clientPressCallback(index)
    def __releaseButton(self, index):
        # scale the button back down
        button = self.__getButtons()[index]
        button.setScale(self.buttonNormalScale)
        if self.__clientReleaseCallback != None:
            self.__clientReleaseCallback(index)
    def __enterButton(self, index):
        if self.__clientEnterCallback != None:
            self.__clientEnterCallback(index)
    def __exitButton(self, index):
        if self.__clientExitCallback != None:
            self.__clientExitCallback(index)

    def simButtonPress(self, index):
        button = self.__getButtons()[index]
        button.setScale(self.buttonPressScale)
        button.component('image3').setColor(self.buttonNormalColor)

    def simButtonRelease(self, index):
        button = self.__getButtons()[index]
        button.setScale(self.buttonNormalScale)
        button.component('image3').setColor(self.buttonDisabledColor)
