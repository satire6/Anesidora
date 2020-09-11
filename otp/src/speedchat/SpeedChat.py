"""SpeedChat.py: contains the SpeedChat class"""

from direct.showbase.PythonUtil import boolEqual
from SpeedChatTypes import *
from SCSettings import SCSettings
from SCTerminal import SCWhisperModeChangeEvent
from otp.otpbase import OTPLocalizer

# for speedchat tech details, see the bottom of this file.

class SpeedChat(SCMenu):
    """
    SpeedChat object. Create one of these to make a complete SpeedChat menu.

    If you provide a name for the SpeedChat, the name will be prepended onto
    all events that the SpeedChat generates.

    The entire structure of the menu may be specified upon construction,
    through the 'structure' argument to SpeedChat.__init__. Alternatively,
    you may add SpeedChat elements manually using the standard Python list
    interfaces implemented by SCMenu.

    See SCMenu.appendFromStructure for the format of 'structure'.
    """

    def __init__(self, name='', structure=None, backgroundModelName = None,
                 guiModelName = None):
        SCMenu.BackgroundModelName = backgroundModelName
        SCMenu.GuiModelName = guiModelName
        
        SCMenu.__init__(self)
        self.name = name

        self.settings = SCSettings(
            eventPrefix = self.name,
            )
        self.privSetSettingsRef(self.settings)

        if structure is not None:
            self.rebuildFromStructure(structure)

        # this is used to detect if the menu needs to be invalidated
        # because of a change in position or scale etc.
        self._lastTransform = None

    def destroy(self):
        if self.isVisible():
            self.exitVisible()
        self._lastTransform = None
        SCMenu.destroy(self)

    def __str__(self):
        return "%s: '%s'" % (self.__class__.__name__, self.name)

    def enter(self):
        self._detectTransformChange()
        self.enterVisible()

    def exit(self):
        self.exitVisible()

    def _detectTransformChange(self):
        # check if our transform has changed
        newTransform = self.getTransform(aspect2d)
        if self._lastTransform is not None:
            if newTransform != self._lastTransform:
                self.invalidateAll()
        self._lastTransform = newTransform

    def setWhisperMode(self, whisperMode):
        if not boolEqual(self.settings.whisperMode, whisperMode):
            self.settings.whisperMode = whisperMode
            messenger.send(self.getEventName(SCWhisperModeChangeEvent),
                           [whisperMode])

    def setColorScheme(self, colorScheme):
        self.settings.colorScheme = colorScheme
        # this affects pretty much every element, and it's not a common
        # occurence. invalidate the entire tree.
        self.invalidateAll()

    def setSubmenuOverlap(self, submenuOverlap):
        self.settings.submenuOverlap = submenuOverlap
        self.invalidateAll()

    def setTopLevelOverlap(self, topLevelOverlap):
        self.settings.topLevelOverlap = topLevelOverlap
        self.invalidateAll()

    def finalizeAll(self):
        self.notify.debug('finalizing entire SpeedChat tree')
        self._detectTransformChange()
        SCMenu.finalizeAll(self)

"""
SpeedChat tech
==============

The SpeedChat comprises cascading menus of 'elements'. Some elements
act as holders for submenus, others represent phrases or emotions that
the user can select to make their avatar speak and/or animate.

The classes that make up the basic SpeedChat system are:
SCObject: base class for all SpeedChat entities, contains support functions
SCColorScheme: contains a set of colors for the elements of the SpeedChat
SCMenu: a single menu that contains a number of elements
SCElement: base class for all entities that may appear within a menu
SCMenuHolder: element that has a submenu attached to it
SCTerminal: base class for all elements that can be clicked on to perform
            an action; once selected, the SpeedChat session is over
SCStaticTextTerminal: basic terminal, contains a phrase that can be spoken
SpeedChat: the top-level menu that contains the entire SpeedChat and provides
           interface functions to the user of the system

To support the needs of Toontown, the following classes are derived:
SCCustomMenu: menu that holds purchased custom phrases
SCCustomTerminal: element of an SCCustomMenu
SCEmoteMenu: menu that holds the set of emotions that local toon has access to
SCEmoteTerminal: element of an SCEmoteMenu
SCToontaskMenu: menu that contains phrases related to local toon's toontasks
SCToontaskTerminal: element of an SCToontaskMenu

GRAPHICAL REPRESENTATION
Graphically, menus are responsible for displaying a transparent frame around
and behind its elements. The background is a flat area with borders around it,
with rounded corners. The geometry of the background image is a model split
into 9 pieces: a 1x1 square middle section, top/left/right/bottom sections,
each 1 foot long or high, and four corner pieces. The origin of the model is
at the intersection of the top-left corner, top, left, and middle pieces.

To make this background big enough for a menu that must contain elements that
take up a WxH-feet area, the pieces are scaled and moved in an intuitive
manner. The middle piece is scaled by W and H, the top/left/right/bottom
pieces are scaled similarly but along one dimension, and the top-right,
bottom-left, and bottom-right corners are moved by W or H appropriately.
Finally, all border elements are scaled wrt aspect2d in the appropriate
dimensions in order to maintain an appropriate border width regardless of
the scale of the overall SpeedChat. See SCMenu.finalize() for the
implementation.

Each menu element contains a DirectButton that takes care of interaction
with the mouse. The DirectButton is also used as the graphical representation
of the element. (In the future, it would be a good idea to rework the code
so that SCElements *are* DirectButtons.)

Each element creates its button so that it contains some text. For terminals,
this is usually the phrase that the local toon would say if selected. Some
elements also add a graphical element to their button; for instance, menu
holders contain an arrow graphic, and terminals that have emotions that will
be triggered upon selection (linked emotes) contain an 'emote icon' graphic.

The background of the button is made completely transparent most of the time,
since the menu already has created a background frame underneath the elements.
Menu holders use a slight alpha on their background, to darken the menu frame
behind them. Solid, opaque colors are used to indicate rollover.

GRAPHICAL DYNAMICS
Every graphical object in the SpeedChat (everything that derives from
SCObject) inherits an interface that is designed to minimize
graphics-related processing. The methods that SCObject defines are:

invalidate(): mark this object as 'dirty' (needs processing before being shown)
isDirty(): returns true if this object has been marked dirty
validate(): reset the 'dirty' flag (presumably after updating the object's
            graphical representation)
finalize(): performs the necessary operations to ensure that the object's
            graphical representation is up-to-date

invalidate() should be a light operation; it is acceptable for finalize() to
be a heavy operation. Dirty objects only need to be finalized once per frame,
regardless of how many times it is marked as dirty. It should be OK to call
finalize() on a non-dirty object, and that should be a light operation.

In the current implementation, SCElements destroy their button and rebuild it
from scratch every time they are invalidated. For performance reasons,
some subclasses of SCElement avoid this by making dynamic modifications to
their button when they can. If and when the SpeedChat objects are made into
first-class DirectGui elements, dynamic modifications will become a necessity;
presumably, this will result in slightly better performance (and slightly
more complex code).

MENU DYNAMICS
As the user moves the mouse cursor through an open menu, different elements
of the menu gain the input focus. Only one element can have the input focus
at any instant. Correspondingly, only one element should be 'active' at any
instant, where 'active' is interpreted according to the type of element:
menu holders show their submenu when active, terminals simply show their
rollover state, etc.

Naively, we can say that the element that has the input focus should be the
active element. This works OK, until the user moves the mouse cursor away
from the menu -- or into a submenu! What we really want is for some elements,
such as menu holders, to have 'sticky focus' -- that is to say, once activated,
elements with sticky focus will stay active until a sibling becomes
activated, even if they lose the input focus.

The SpeedChat takes advantage of this separation of 'active' and 'focus-having'
elements in order to make the menus easier to use. When an element
gains the input focus, it is only activated if the element maintains the
input focus for a specific period of time. By calibrating the duration of
the wait period, we create a 'tolerance' for 'sloppy' use of the menu: the
user can drag the mouse across large sections of an open menu without causing
any of the elements that are dragged over to become active.

COLOR SCHEMES
To change the color scheme of a SpeedChat, you must create a new SCColorScheme
object and pass it to the SpeedChat with its setColorScheme() method.
SCColorScheme objects are immutable.

There are some crude utility functions to dynamically change the color scheme
of a SpeedChat in SCColorPanel.py.

SpeedChat color schemes are basically described by two colors: a main color
and a contrasting color. The main color ('arrowColor') is used directly on
the menuHolder arrows, and a lightened version of it is used for the menu
backgrounds. The contrasting color is used directly as the element rollover
color, and variations of it are calculated for the pressed and 'active'
element colors, as well as the emote icon color.

The color modifications and calculations are done by converting RGB colors
into the YUV and HSV color spaces, manipulating those values, and
converting back to RGB. The conversion functions and descriptions of the
YUV and HSV color spaces are in ColorSpace.py
"""
