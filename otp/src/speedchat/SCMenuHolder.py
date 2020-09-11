"""SCMenuHolder.py: contains the SCMenuHolder class"""

from pandac.PandaModules import *
from direct.gui.DirectGui import *
from SCObject import SCObject
from SCElement import SCElement
from SCMenu import SCMenu
import types

class SCMenuHolder(SCElement):
    """
    SCMenuHolder is an SCElement that owns an SCMenu and is
    responsible for displaying it.
    """

    # our default background color should simply darken the underlying
    # pixels
    #
    # The alpha-blending equation:
    #
    # Cout = Asrc*Csrc + (1-Asrc)*Cdst
    #
    # where Cout is the result, Csrc is the color of the transparent
    # pixel being drawn, Asrc is the alpha value of said pixel,
    # and Cdst is the color that is currently in the framebuffer.
    #
    # We will use Csrc = (0,0,0), since we only want to darken the
    # framebuffer, not change its color/hue. This gives us:
    #
    # Cout = (1-Asrc)*Cdst
    #
    # Intuitively, we want to be able to say 'Make the existing color N%
    # of its current brightness.' Assuming N in 0..1:
    #
    # Cout = N*Cdst
    #  thus
    # N = (1-Asrc),
    # Asrc = (1-N)
    N = .9
    DefaultFrameColor = (0,0,0,1.-N)
    del N

    # how much darker a child menu should be than its parent
    MenuColorScaleDown = .95

    def __init__(self, title, menu=None):
        SCElement.__init__(self)
        self.title = title

        scGui = loader.loadModel(SCMenu.GuiModelName)
        self.scArrow = scGui.find('**/chatArrow')

        self.menu = None
        self.setMenu(menu)

    def destroy(self):
        if self.menu is not None:
            self.menu.destroy()
            self.menu = None
        SCElement.destroy(self)

    def setTitle(self, title):
        self.title = title
        self.invalidate()
    def getTitle(self):
        return self.title

    def setMenu(self, menu):
        if self.menu is not None:
            self.menu.destroy()
        self.menu = menu
        if self.menu is not None:
            self.privAdoptSCObject(self.menu)
            self.menu.setHolder(self)
            # make sure the menu shows up over us
            self.menu.reparentTo(self, 1)
            self.menu.hide()
        self.updateViewability()
    def getMenu(self):
        return self.menu

    def showMenu(self):
        """use this if we go back to a sorted bin
        # make sure the menu shows up over us
        drawOrder = self.getNetState().getDrawOrder()
        self.menu.setBin('fixed', drawOrder + 1)
        """
        if self.menu is not None:
            cS = SCMenuHolder.MenuColorScaleDown
            self.menu.setColorScale(cS,cS,cS,1)
            self.menu.enterVisible()
            self.menu.show()

    def hideMenu(self):
        if self.menu is not None:
            self.menu.hide()
            self.menu.exitVisible()

    def getMenuOverlap(self):
        """returns a value in 0..1 representing the percentage
        of our width that submenus should cover"""
        if self.parentMenu.isTopLevel():
            return self.getTopLevelOverlap()
        else:
            return self.getSubmenuOverlap()

    def getMenuOffset(self):
        """should return a Point3 offset at which the menu should be
        positioned relative to this element"""
        xOffset = self.width * (1. - self.getMenuOverlap())
        return Point3(xOffset, 0, 0)

    # from SCElement
    def onMouseClick(self, event):
        SCElement.enterActive(self)
        self.parentMenu.memberSelected(self)

    # 'active-state' state-change handlers; called by parent menu
    def enterActive(self):
        SCElement.enterActive(self)
        self.showMenu()

        # set the frame color to show that this menuHolder is active
        if hasattr(self, 'button'):
            r,g,b = self.getColorScheme().getMenuHolderActiveColor()
            a = self.getColorScheme().getAlpha()
            self.button.frameStyle[DGG.BUTTON_READY_STATE].setColor(r,g,b,a)
            self.button.updateFrameStyle()
        else:
            self.notify.warning("SCMenuHolder has no button (has finalize been called?).")

    def exitActive(self):
        SCElement.exitActive(self)
        self.hideMenu()

        # reset the frame color
        self.button.frameStyle[DGG.BUTTON_READY_STATE].setColor(
            *SCMenuHolder.DefaultFrameColor)
        self.button.updateFrameStyle()

    def getDisplayText(self):
        return self.title

    def updateViewability(self):
        if self.menu is None:
            self.setViewable(0)
            return
        # if our menu is empty or none of our children are
        # viewable, we should not be viewable
        isViewable = False
        for child in self.menu:
            if child.isViewable():
                isViewable = True
                break
        self.setViewable(isViewable)

    def getMinSubmenuWidth(self):
        # return the minimum width for a submenu, so that it covers
        # this menu out past its right edge
        parentMenu = self.getParentMenu()
        # if we are in a menu, use the menu's width, since we are also
        # that wide
        if parentMenu is None:
            myWidth, myWeight = self.getMinDimensions()
        else:
            myWidth = parentMenu.getWidth()
        # this assumes offsetMult in [0,1]
        return .15 + (myWidth * self.getMenuOverlap())

    def getMinDimensions(self):
        width, height = SCElement.getMinDimensions(self)
        # add space for the arrow
        width += 1.
        return width, height

    def invalidate(self):
        SCElement.invalidate(self)
        # invalidate our menu, since our width may have changed and
        # the menu may be stretched to cover our width
        if self.menu is not None:
            self.menu.invalidate()

    def finalize(self, dbArgs={}):
        """catch this call and influence the appearance of our button"""
        if not self.isDirty():
            return

        r,g,b = self.getColorScheme().getArrowColor()
        a = self.getColorScheme().getAlpha()
        self.scArrow.setColorScale(r,g,b,a)

        if self.menu is not None:
            # adjust the position of the menu
            self.menu.setPos(self.getMenuOffset())

        if self.isActive():
            r,g,b = self.getColorScheme().getMenuHolderActiveColor()
            a = self.getColorScheme().getAlpha()
            frameColor = (r,g,b,a)
        else:
            frameColor = SCMenuHolder.DefaultFrameColor

        args = {
            'image':      self.scArrow,
            'image_pos':  (self.width-.5,0,-self.height*.5),
            'frameColor': frameColor,
            }

        args.update(dbArgs)
        SCElement.finalize(self, dbArgs=args)

    def hasStickyFocus(self):
        """menu holders have sticky focus. Once a menu holder gets
        activated, it stays active until a sibling becomes active."""
        return 1

    # from SCObject
    def privSetSettingsRef(self, settingsRef):
        SCObject.privSetSettingsRef(self, settingsRef)
        # propogate the settings reference to our menu
        if self.menu is not None:
            self.menu.privSetSettingsRef(settingsRef)

    def invalidateAll(self):
        SCObject.invalidateAll(self)
        if self.menu is not None:
            self.menu.invalidateAll()

    def finalizeAll(self):
        SCObject.finalizeAll(self)
        if self.menu is not None:
            self.menu.finalizeAll()

