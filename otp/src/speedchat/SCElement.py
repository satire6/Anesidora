"""SCElement.py: contains the SCElement class"""

from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task
from SCConstants import *
from SCObject import SCObject
from direct.showbase.PythonUtil import boolEqual
from otp.otpbase import OTPGlobals

class SCElement(SCObject, NodePath):
    """ SCElement is the base class for all entities that can appear
    as entries in a SpeedChat menu. """

    font = OTPGlobals.getInterfaceFont()

    SerialNum = 0

    def __init__(self, parentMenu=None):
        SCObject.__init__(self)

        self.SerialNum = SCElement.SerialNum
        SCElement.SerialNum += 1
        node = hidden.attachNewNode('SCElement%s' % self.SerialNum)
        NodePath.__init__(self, node)

        self.FinalizeTaskName = 'SCElement%s_Finalize' % self.SerialNum

        self.parentMenu = parentMenu
        self.__active = 0
        self.__viewable = 1

        # these are used to detect changes to the size of this element
        # to avoid unnecessary button rebuilds
        self.lastWidth = 0
        self.lastHeight = 0

        self.setDimensions(0,0)

        # how much space to put in around the edges of the button
        self.padX = .25
        self.padZ = .1

    def destroy(self):
        if self.isActive():
            self.exitActive()
        # this calls exitVisible if necessary
        SCObject.destroy(self)
        if hasattr(self, 'button'):
            self.button.destroy()
            del self.button
        self.parentMenu = None
        self.detachNode()

    def setParentMenu(self, parentMenu):
        self.parentMenu = parentMenu
    def getParentMenu(self):
        return self.parentMenu

    def getDisplayText(self):
        """ derived classes should override and return the text that
        should be visually displayed on this item. Note that elements
        that must do non-trivial processing to produce this text
        should cache the text when they can. """
        self.notify.error(
            'getDisplayText is pure virtual, derived class must override')

    # input event handlers that derived classes can override
    def onMouseEnter(self, event):
        """ the mouse has just entered this entity """
        if self.parentMenu is not None:
            self.parentMenu.memberGainedInputFocus(self)
        
    def onMouseLeave(self, event):
        """ the mouse has just left this entity """
        if self.parentMenu is not None:
            self.parentMenu.memberLostInputFocus(self)

    def onMouseClick(self, event):
        """ the user just clicked on this entity """
        pass

    """ inheritors should override these methods and perform whatever
    actions are appropriate when this element becomes 'active' and
    'inactive' (for example, menu holders should show/hide their menu;
    other element types might play some sort of animation on activation).
    'active' generally corresponds to having the input focus, but not
    always; see 'hasStickyFocus' below. """
    def enterActive(self):
        self.__active = 1
    def exitActive(self):
        self.__active = 0

    def isActive(self):
        return self.__active

    def hasStickyFocus(self):
        """ Inheritors should override and return non-zero if they
        should remain active until a sibling becomes active, even
        if they lose the input focus. For example, menu holders should
        remain open until a sibling becomes active, even if the user
        moves the mouse out of the menu holder, or even completely away
        from the SpeedChat menus. """
        return 0

    """ If this element is marked as 'not viewable', it will disappear from
    its parent menu, and it will not be possible for the user to
    interact with this element. """
    def setViewable(self, viewable):
        if (not boolEqual(self.__viewable, viewable)):
            self.__viewable = viewable

            # inform our parent that our visibility state has changed
            if self.parentMenu is not None:
                self.parentMenu.memberViewabilityChanged(self)

    def isViewable(self):
        return self.__viewable

    def getMinDimensions(self):
        """ Should return the width/height that this element would
        ideally like to be. We may be asked to display ourselves
        larger than this, never smaller.
        returns (width, height)
        """
        text = TextNode('SCTemp')
        text.setFont(SCElement.font)
        dText = self.getDisplayText()
        text.setText(dText)
        bounds = text.getCardActual()
        # there's already padding on the right, apparently
        width  = abs(bounds[1] - bounds[0]) + self.padX
        # the height will always be the same regardless of the string
        height = abs(bounds[3] - bounds[2]) + 2.*self.padZ
        return width, height

    def setDimensions(self, width, height):
        """ Call this to tell this element how big it should be. Must be
        called before calling finalize. """
        self.width  = float(width)
        self.height = float(height)
        if (self.lastWidth, self.lastHeight) != (self.width, self.height):
            self.invalidate()

    def invalidate(self):
        """ call this if something about our appearance has changed and
        we need to re-create our button """
        SCObject.invalidate(self)
        parentMenu = self.getParentMenu()
        if parentMenu is not None:
            # if our parent menu caused us to become invalid during its
            # finalization, don't re-invalidate it
            if not parentMenu.isFinalizing():
                parentMenu.invalidate()

    # from SCObject
    def enterVisible(self):
        SCObject.enterVisible(self)
        self.privScheduleFinalize()

    def exitVisible(self):
        SCObject.exitVisible(self)
        self.privCancelFinalize()

    def privScheduleFinalize(self):
        # spawn a task to finalize ourselves before we render.
        def finalizeElement(task, self=self):
            # if our parent menu is dirty, it will be finalizing us shortly;
            # our size may change in the process, so don't bother
            # finalizing yet.
            if self.parentMenu is not None:
                if self.parentMenu.isDirty():
                    return Task.done
            self.finalize()
            return Task.done
        taskMgr.remove(self.FinalizeTaskName)
        taskMgr.add(finalizeElement, self.FinalizeTaskName,
                    priority=SCElementFinalizePriority)

    def privCancelFinalize(self):
        taskMgr.remove(self.FinalizeTaskName)

    def finalize(self, dbArgs={}):
        """ 'dbArgs' can contain parameters (and parameter overrides) for
        the DirectButton.
        """
        if not self.isDirty():
            return
        
        SCObject.finalize(self)
        
        if hasattr(self, 'button'):
            self.button.destroy()
            del self.button

        halfHeight = self.height/2.

        # if we're given a 'center' value for the text alignment,
        # calculate the appropriate text X position
        textX = 0
        if dbArgs.has_key('text_align'):
            if dbArgs['text_align'] == TextNode.ACenter:
                textX = self.width/2.

        args = {
            'text': self.getDisplayText(),
            'frameColor': (0,0,0,0),
            'rolloverColor': self.getColorScheme().getRolloverColor()+(1,),
            'pressedColor': self.getColorScheme().getPressedColor()+(1,),
            'text_font': OTPGlobals.getInterfaceFont(),
            'text_align': TextNode.ALeft,
            'text_fg': self.getColorScheme().getTextColor()+(1,),
            'text_pos': (textX,-.25-halfHeight,0),
            'relief': DGG.FLAT,
            # disable the 'press effect' (slight scale-down)
            'pressEffect': 0,
            }
        # add external parameters and apply any overrides
        args.update(dbArgs)

        # these can't be passed directly to DirectButton
        rolloverColor = args['rolloverColor']
        pressedColor = args['pressedColor']
        del args['rolloverColor']
        del args['pressedColor']

        """
        from direct.gui.DirectGui import *;import OTPGlobals;
        btn.destroy();w=3;h=2;btn = DirectButton(parent=aspect2d,frameSize=(0,w,-h,0),text='TEST',frameColor=(.8,.8,1,1),text_font=OTPGlobals.getInterfaceFont(),text_align=TextNode.ALeft,text_fg=(0,0,0,1),text_pos=(0,-.25-(h/2.),0),image=('phase_3/models/props/page-arrow', 'poly'),image_pos=(w*.9,0,-h/2.),state=DGG.NORMAL,relief=DGG.RAISED);btn.setPos(-.5,0,0);btn.setScale(.5)"""

        btn = DirectButton(
            parent = self,
            frameSize = (0,self.width,
                         -self.height,0),
            # this doesn't trigger until mouse-up. We want to trigger
            # on mouse-down; see the 'bind' calls below
            #command = self.onMouseClick,
            **args
            )

        # Set frame color for rollover and pressed states
        btn.frameStyle[DGG.BUTTON_ROLLOVER_STATE].setColor(*rolloverColor)
        btn.frameStyle[DGG.BUTTON_DEPRESSED_STATE].setColor(*pressedColor)
        btn.updateFrameStyle()

        # listen for input events
        btn.bind(DGG.ENTER,   self.onMouseEnter)
        btn.bind(DGG.EXIT,    self.onMouseLeave)
        btn.bind(DGG.B1PRESS, self.onMouseClick)
        self.button = btn

        # store the new display params
        self.lastWidth  = self.width
        self.lastHeight = self.height

        self.validate()

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.getDisplayText())
    
