from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task

from toontown.toonbase import TTLocalizer

import PlayingCardGlobals

class PlayingCardBase:
    """
    The AI could use this class, or the client in situations where we will
    not need to actually display the card onscreen.  If you need to display
    the card graphically, use PlayingCardNodePath or PlayingCardButton.
    RAU modified from Pirates
    """
    def __init__(self, value):
        self.faceUp = 1
        self.setValue(value)

    def getCardName(self):
        PlayingCardGlobals.getCardName(self.value)

    def getRank(self):
        return self.rank

    def getSuit(self):
        return self.suit

    def getValue(self):
        return self.value

    def setImage(self):
        # The base class has no display image
        pass

    def setValue(self, value):
        self.value = value
        if self.value == PlayingCardGlobals.Unknown:
            self.suit = None
            self.rank = None
            # An unknown card must be turned down
            self.turnDown()
        else:
            self.suit = value / PlayingCardGlobals.MaxRank
            self.rank = value % PlayingCardGlobals.MaxRank
        self.setImage()

    def isFaceUp(self):
        return self.faceUp

    def isFaceDown(self):
        return not self.faceUp

    def turnUp(self):
        assert self.value != PlayingCardGlobals.Unknown
        self.faceUp = 1
        self.setImage()

    def turnDown(self):
        self.faceUp = 0
        self.setImage()


class PlayingCardNodePath(NodePath, PlayingCardBase):
    """
    PlayingCardNodePath creates a new nodepath that has two children - the
    front image and the back image.  This class can be used when no input
    from the player is needed on the card - that is, the card has no mouse
    or button events. If you need those, use PlayingCardButton.
    """
    def __init__(self, style, value):
        self.image = None
        self.style = style
        NodePath.__init__(self, "PlayingCard")
        PlayingCardBase.__init__(self, value)

    def setImage(self):
        if self.faceUp:
            image = PlayingCardGlobals.getImage(self.style, self.suit, self.rank)
        else:
            image = PlayingCardGlobals.getBack(self.style)
        if self.image:
            self.image.removeNode()
        self.image = image.copyTo(self)
        

class PlayingCardButton(PlayingCardBase, DirectButton):
    """
    PlayingCardButton is a DirectButton that can have code bindings on
    mouse events (like a button). Drag and drop is also supported.  If you
    want to show a playing card graphically but do not have the need for
    mouse input, use PlayingCardNodePath -- it is cheaper.
    """    
    def __init__(self, style, value):
        PlayingCardBase.__init__(self, value)
        self.style = style
        DirectButton.__init__(self,
                              relief = None,
                              )
        self.initialiseoptions(PlayingCardButton)

        # Drag and drop
        self.bind(DGG.B1PRESS, self.dragStart)
        self.bind(DGG.B1RELEASE, self.dragStop)
        
    def setImage(self):
        if self.faceUp:
            image = PlayingCardGlobals.getImage(self.style, self.suit, self.rank)
        else:
            image = PlayingCardGlobals.getBack(self.style)
        self['image'] = image

    def dragStart(self, event):
        taskMgr.remove(self.taskName('dragTask'))
        vWidget2render2d = self.getPos(render2d)
        vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
        editVec = Vec3(vWidget2render2d - vMouse2render2d)
        task = taskMgr.add(self.dragTask, self.taskName('dragTask'))
        task.editVec = editVec

    def dragTask(self, task):
        mwn = base.mouseWatcherNode
        if mwn.hasMouse():
            vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
            newPos = vMouse2render2d + task.editVec
            self.setPos(render2d, newPos)
        return Task.cont

    def dragStop(self, event):
        taskMgr.remove(self.taskName('dragTask'))
        messenger.send("PlayingCardDrop", sentArgs=[self])

    def destroy(self):
        taskMgr.remove(self.taskName('dragTask'))
        DirectButton.destroy(self)
