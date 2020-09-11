"""SCMenu.py: contains the SCMenu class"""

from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task
from SCConstants import *
from direct.interval.IntervalGlobal import *
from SCObject import SCObject
from direct.showbase.PythonUtil import makeTuple
import types

class SCMenu(SCObject, NodePath):
    """ SCMenu is a menu of SCElements """

    # The speedchat will wait this long before switching to a new
    # active menu member when the mouse rolls over the new member.
    # Set to zero to disable this behavior.
    config = getConfigShowbase()
    SpeedChatRolloverTolerance = config.GetFloat(
        'speedchat-rollover-tolerance', .08)

    # should we fade in the menus?
    WantFade = config.GetBool('want-speedchat-fade', 0)

    # How long it should take for a menu to fade in.
    FadeDuration = config.GetFloat('speedchat-fade-duration', .2)

    SerialNum = 0

    # This should be filled in by SpeedChat.py to indicate the
    # appropriate model file to load for the background and the gui
    # objects, respectively. Also the names of the gui icon nodes.
    BackgroundModelName = None
    GuiModelName = None

    def __init__(self, holder=None):
        SCObject.__init__(self)

        self.SerialNum = SCMenu.SerialNum
        SCMenu.SerialNum += 1

        node = hidden.attachNewNode('SCMenu%s' % self.SerialNum)
        NodePath.__init__(self, node)

        # if 'None', this menu is a top-level menu (it's not under anything)
        self.setHolder(holder)

        self.FinalizeTaskName = 'SCMenu%s_Finalize' % self.SerialNum
        self.ActiveMemberSwitchTaskName = (
            'SCMenu%s_SwitchActiveMember' % self.SerialNum)

        self.bg = loader.loadModel(self.BackgroundModelName)
        def findNodes(names, model=self.bg):
            results = []
            for name in names:
                # if name is a tuple we need to look for the first match
                for nm in makeTuple(name):
                    node = model.find('**/%s' % nm)
                    if not node.isEmpty():
                        results.append(node)
                        break
            return results

        # Maya doesn't allow nodes to be named 'top' so it's named
        # 'top1' in the Pirates model
        (self.bgTop, self.bgBottom, self.bgLeft, self.bgRight,
         self.bgMiddle, self.bgTopLeft, self.bgBottomLeft,
         self.bgTopRight, self.bgBottomRight) = findNodes(
            [('top', 'top1'), 'bottom', 'left', 'right',
             'middle', 'topLeft', 'bottomLeft',
             'topRight', 'bottomRight'])

        # give the bg frame a render order that puts it behind the rest
        # of our children
        self.bg.reparentTo(self, -1)

        # the member elements in this menu
        # note that our member list should be manipulated by applying
        # list operations to 'self'
        self.__members = []

        # Each menu can have a maximum of one 'active' member ('active'
        # being interpreted based on the member's element type; menu holders
        # show their menu when active, etc.)
        self.activeMember = None
        self.activeCandidate = None

        self.fadeIval = None

        # initialized; only used for horizonal centering
        self.width = 1

        # to prevent recursive invalidates from members
        self.inFinalize = 0

    def destroy(self):
        self.stopFade()
        SCObject.destroy(self)
        del self.bgTop
        del self.bgBottom
        del self.bgLeft
        del self.bgRight
        del self.bgMiddle
        del self.bgBottomLeft
        del self.bgTopRight
        del self.bgBottomRight
        self.bg.removeNode()
        del self.bg
        
        self.holder = None
        for member in self.__members:
            member.destroy()
        del self.__members
        self.removeNode()

        taskMgr.remove(self.FinalizeTaskName)
        taskMgr.remove(self.ActiveMemberSwitchTaskName)

    def clearMenu(self):
        """ This will empty our menu, and destroy all of the current
        member elements. """
        while len(self):
            # It is important to del the item from the list *before*
            # destroying it, because the __delitem__ method may
            # perform some additional cleanup.
            item = self[0]
            del self[0]
            item.destroy()

    def rebuildFromStructure(self, structure, title=None):
        """ This will destroy the current content of this menu and replace
        it with the tree described by 'structure'."""
        self.clearMenu()
        
        if title:
            holder = self.getHolder()
            if holder:
                holder.setTitle(title)

        self.appendFromStructure(structure)

    def appendFromStructure(self, structure):
        """ This will add the tree elements described by 'structure' to the
        existing menu elements.

        structure should be a list of Python objects that represent SpeedChat
        elements. Here is the mapping of Python objects to SpeedChat elements:

        Integers represent static-text terminal elements. They should be valid
        indices into OTPLocalizer.SpeedChatStaticText.

        TODO: how to represent different terminals

        Lists represent menus: the format is
         [menuType, title, elem1, elem2, ..]
        'menuType' is the desired menu class (if omitted, defaults to SCMenu).
        'title' is the text that should appear on the menu's holder element.
        elem1, etc. are the elements that should appear in the menu.

        Emotes are attached to terminal elements using dictionaries:
         {terminal:emoteId}
        """
        from SpeedChatTypes import SCMenuHolder, SCStaticTextTerminal, SCGMTextTerminal
        from otp.otpbase import OTPLocalizer
        
        def addChildren(menu, childList):
            """ this recursive function adds children to an SCMenu
            according to the specification in 'childList'. See above
            for the format of childList (it matches the format of
            'structure'). """
            for child in childList:
                # if it's a dictionary, there's an emote attached
                emote = None
                if type(child) == type({}):
                    assert len(child.keys()) == 1
                    item = child.keys()[0]
                    emote = child[item]
                    child = item

                # use this func to add terminal nodes;
                # takes care of linking emotes
                # def addTerminal(terminal, menu=menu, emote=emote):
                #    if emote is not None:
                #        terminal.setLinkedEmote(emote)
                #    menu.append(terminal)

                if type(child) == type(0):
                    # it's a static text ID
                    assert child in OTPLocalizer.SpeedChatStaticText
                    terminal = SCStaticTextTerminal(child)
                    if emote is not None:
                        terminal.setLinkedEmote(emote)
                    menu.append(terminal)
                    # addTerminal(SCStaticTextTerminal(child))
                elif type(child) == type([]):
                    # we've got a menu holder and a menu to be held
                    # if first element of list is string, it's a plain SCMenu
                    if type(child[0]) == type(''):
                        holderTitle = child[0]
                        subMenu = SCMenu()
                        subMenuChildren = child[1:]
                    else:
                        # otherwise, first element of list is class
                        menuType, holderTitle = child[0], child[1]
                        subMenu = menuType()
                        subMenuChildren = child[2:]
                    if emote:
                        print ('warning: tried to link emote %s '
                               'to a menu holder' % emote)
                    holder = SCMenuHolder(holderTitle, menu=subMenu)
                    menu.append(holder)
                    addChildren(subMenu, subMenuChildren)
                elif type(child) == type('') and child[:2] == 'gm':
                    terminal = SCGMTextTerminal(child)
                    menu.append(terminal)
                else:
                    raise ('error parsing speedchat structure. '
                           'invalid child: %s' % child)

        addChildren(self, structure)
        # clean up memory leak
        addChildren = None

    def fadeFunc(self, t):
        cs = self.getColorScale()
        self.setColorScale(cs[0],cs[1],cs[2],t)

    def stopFade(self):
        if self.fadeIval is not None:
            self.fadeIval.pause()
            self.fadeIval = None

    def enterVisible(self):
        SCObject.enterVisible(self)
        self.privScheduleFinalize()

        # tell our members that they're visible now
        for member in self:
            if member.isViewable():
                if not member.isVisible():
                    member.enterVisible()

        # we are just becoming visible, so reset our child fade flag
        self.childHasFaded = 0

        # if a sibling menu has already faded in, don't fade in again
        alreadyFaded = 0
        parentMenu = None
        if self.holder is not None:
            if self.holder.parentMenu is not None:
                parentMenu = self.holder.parentMenu
                alreadyFaded = parentMenu.childHasFaded

        if SCMenu.WantFade:
            if alreadyFaded:
                self.fadeFunc(1.)
            else:
                self.stopFade()
                self.fadeIval = LerpFunctionInterval(
                    self.fadeFunc, fromData=0., toData=1.,
                    duration = SCMenu.FadeDuration)
                self.fadeIval.play()
                if parentMenu is not None:
                    parentMenu.childHasFaded = 1

    def exitVisible(self):
        SCObject.exitVisible(self)
        self.stopFade()
        self.privCancelFinalize()
        self.__cancelActiveMemberSwitch()
        # if there is a member that is active, deactive it
        self.__setActiveMember(None)
        # tell all of our visible members that they're about to
        # not be visible anymore
        for member in self:
            if member.isVisible():
                member.exitVisible()

    """ The 'holder' is an element that 'owns' this menu; if 'None', this
    is a free-standing menu. """
    def setHolder(self, holder):
        self.holder = holder
    def getHolder(self):
        return self.holder

    def isTopLevel(self):
        return (self.holder == None)

    def memberSelected(self, member):
        """ non-terminal member elements should call this when they are
        clicked on; immediately makes them the active member. """
        assert member in self

        # cancel any pending active candidate
        self.__cancelActiveMemberSwitch()

        self.__setActiveMember(member)

    def __setActiveMember(self, member):
        """ this function actually does the work of switching the active
        member. """
        # if this member is already the active member, ignore
        if self.activeMember is member:
            return
        # if there is a member element that was active, deactive it
        if self.activeMember is not None:
            self.activeMember.exitActive()
        # set up with the new member as the active member
        self.activeMember = member
        if self.activeMember is not None:
            # reparent the active member to us, so that it (and its children,
            # if any) will be rendered on top of all of its siblings
            self.activeMember.reparentTo(self)
            self.activeMember.enterActive()

    """ Member elements will call these functions to inform us that they
    have gained/lost the input focus. Based on calls to these functions,
    we will instruct our elements to go active or inactive. """
    def memberGainedInputFocus(self, member):
        """ member elements will call this function to let us know that
        they have gained the input focus """
        assert member in self

        # kill any candidate-active-member wait task
        self.__cancelActiveMemberSwitch()

        # this could be the currently-active member, if it has sticky
        # focus (elements with sticky focus don't necessarily become
        # inactive when the mouse leaves)
        if member is self.activeMember:
            return

        # we can improve the feel and ease-of-use of the menus by
        # delaying the switching of the active member state, to make
        # sure that the user actually intends to give the element the
        # focus, and is not just grazing past it on the way to something
        # else.

        # if there is no active member, just make the candidate member
        # active right away. Also, switch immediately if this member
        # is above the candidate in the menu.
        if ((self.activeMember is None) or
            (SCMenu.SpeedChatRolloverTolerance == 0) or
            (member.posInParentMenu < self.activeMember.posInParentMenu)):
            self.__setActiveMember(member)
        else:
            # otherwise, don't switch the active member right away.
            # if this element maintains the input focus for N seconds,
            # make it active
            
            def doActiveMemberSwitch(task, self=self, member=member):
                self.activeCandidate = None
                self.__setActiveMember(member)
                return Task.done

            # If we just spawn a simple doLater task, the task is guaranteed
            # to run no sooner than after the next display update, and thus
            # the visual results are guaranteed to show up no sooner than two
            # display updates from now. This is a minimum time delay of two
            # full frame cycles, from the time that the mouse enters the member
            # to the time that the user sees that member as active.
            #
            # At a certain threshold of slow framerate, we want to cut our
            # losses, assume that the mouse has been over the candidate member
            # long enough, and switch to that member during this frame.

            # +-- dt ---+
            # |---------|---------|---------|---------|
            #  +--------+   |        |      |
            #    mouse     reg    doLater  results
            #    enter   doLater    run    visible

            minFrameRate = 1./SCMenu.SpeedChatRolloverTolerance
            if globalClock.getAverageFrameRate() > minFrameRate:
                taskMgr.doMethodLater(SCMenu.SpeedChatRolloverTolerance,
                                      doActiveMemberSwitch,
                                      self.ActiveMemberSwitchTaskName)
                # keep a record of the candidate member that wants to be active
                self.activeCandidate = member
            else:
                # do the switch this frame
                self.__setActiveMember(member)

    def __cancelActiveMemberSwitch(self):
        """ Call this to clean up a delayed active-member switch without
        switching to the candidate. Okay to call even if there currently
        is no candidate.
        """
        taskMgr.remove(self.ActiveMemberSwitchTaskName)
        self.activeCandidate = None

    def memberLostInputFocus(self, member):
        """ member elements will call this function to let us know that
        they have lost the input focus """
        assert member in self

        if member is self.activeCandidate:
            # this member was waiting to become active; kill the wait task
            self.__cancelActiveMemberSwitch()

        # if this member is not *the* active member in this menu,
        # we don't really care
        if member is not self.activeMember:
            """ this can occur now that we delay switching of the active
            member to ensure that the user actually wants the switch
            to occur. """
            assert not member.isActive()
        else:
            # this is currently the active member. if it doesn't have
            # sticky focus, de-activate it now
            if not member.hasStickyFocus():
                self.__setActiveMember(None)

    def memberViewabilityChanged(self, member):
        """ member elements will call this if their viewability state
        changes. """
        # Keep in mind that the viewability of this member may change back
        # before the frame ends. If the active member calls this saying
        # that it's not viewable, don't deactivate it... yet.

        # our menu is no longer valid
        self.invalidate()

    def invalidate(self):
        """ Call this if something has changed and we should reconstruct
        ourselves:
        - member added
        - member removed
        - member visibility state change
        etc.
        """
        SCObject.invalidate(self)

        # If we're visible, we need to spawn a task to rebuild our menu
        # before we render. We could rebuild the menu immediately, but
        # that would get expensive if there are many consecutive member
        # adds and/or removes.
        if self.isVisible():
            self.privScheduleFinalize()

    def privScheduleFinalize(self):
        # spawn a task to finalize our menu before we render.
        def finalizeMenu(task, self=self):
            self.finalize()
            return Task.done
        taskMgr.remove(self.FinalizeTaskName)
        taskMgr.add(finalizeMenu, self.FinalizeTaskName,
                    priority=SCMenuFinalizePriority)

    def privCancelFinalize(self):
        taskMgr.remove(self.FinalizeTaskName)

    def isFinalizing(self):
        return self.inFinalize

    def finalize(self):
        if not self.isDirty():
            return

        self.inFinalize = 1

        SCObject.finalize(self)

        if __debug__:
            # make sure all of our members know that we are their parent menu
            # (who's yo daddy?)
            for member in self:
                assert member.getParentMenu() is self

        # we aren't interested in members that aren't viewable.
        # build a list of viewable members. Also parent viewable
        # members to us, parent non-viewable members to hidden.
        visibleMembers = []
        for member in self:
            if member.isViewable():
                visibleMembers.append(member)
                member.reparentTo(self)
            else:
                member.reparentTo(hidden)
                # if this is the active member, deactivate it
                if self.activeMember is member:
                    self.__setActiveMember(None)

        # survey the members to find out their ideal dimensions, and
        # determine the maximum dimensions
        maxWidth = 0.
        maxHeight = 0.
        for member in visibleMembers:
            width,height = member.getMinDimensions()
            maxWidth = max(maxWidth, width)
            maxHeight = max(maxHeight, height)

        # make sure that we cover our parent menu all the way out past its
        # right edge
        holder = self.getHolder()
        if holder is not None:
            # how wide do we need to be to cover our parent menu?
            widthToCover = holder.getMinSubmenuWidth()
            maxWidth = max(maxWidth, widthToCover)

        # all of the menu members will be at least as big as the biggest
        # member, in each dimension
        memberWidth, memberHeight = maxWidth, maxHeight
        # Store this so that we can do horizonal centering
        self.width = maxWidth

        # put the members in the right place, and tell them what size
        # they should be
        for i in xrange(len(visibleMembers)):
            member = visibleMembers[i]
            member.setPos(0,0,-i * maxHeight)
            member.setDimensions(memberWidth, memberHeight)
            member.finalize()

        if len(visibleMembers) > 0:
            z1 = visibleMembers[0].getZ(aspect2d)
            visibleMembers[0].setZ(-maxHeight)
            z2 = visibleMembers[0].getZ(aspect2d)
            visibleMembers[0].setZ(0)

            actualHeight = (z2-z1) * len(visibleMembers)

            # keep the menu from going off the bottom of the screen
            bottomZ = self.getZ(aspect2d) + actualHeight
            if bottomZ < -1.:
                overlap = bottomZ - (-1.)
                self.setZ(aspect2d, self.getZ(aspect2d) - overlap)
            # keep the menu from going off the top of the screen
            if self.getZ(aspect2d) > 1.:
                self.setZ(aspect2d, 1.)
        
        # set up the background frame
        sX = memberWidth
        sZ = memberHeight * len(visibleMembers)
        self.bgMiddle.setScale(sX,1,sZ)
        self.bgTop.setScale(sX,1,1)
        self.bgBottom.setScale(sX,1,1)
        self.bgLeft.setScale(1,1,sZ)
        self.bgRight.setScale(1,1,sZ)
        self.bgBottomLeft.setZ(-sZ)
        self.bgBottom.setZ(-sZ)
        self.bgTopRight.setX(sX)
        self.bgRight.setX(sX)
        self.bgBottomRight.setX(sX)
        self.bgBottomRight.setZ(-sZ)
        # scale the border wrt aspect2d
        # note: changing the Y-scale from literal '1' wrt parent
        # is not necessary and was causing visibility problems
        sB = .15
        self.bgTopLeft.setSx(aspect2d, sB)
        self.bgTopLeft.setSz(aspect2d, sB)
        self.bgBottomRight.setSx(aspect2d, sB)
        self.bgBottomRight.setSz(aspect2d, sB)
        self.bgBottomLeft.setSx(aspect2d, sB)
        self.bgBottomLeft.setSz(aspect2d, sB)
        self.bgTopRight.setSx(aspect2d, sB)
        self.bgTopRight.setSz(aspect2d, sB)
        self.bgTop.setSz(aspect2d, sB)
        self.bgBottom.setSz(aspect2d, sB)
        self.bgLeft.setSx(aspect2d, sB)
        self.bgRight.setSx(aspect2d, sB)

        r,g,b = self.getColorScheme().getFrameColor()
        a = self.getColorScheme().getAlpha()
        self.bg.setColorScale(r,g,b,a)

        # if we have an active member, reparent it to us, so that
        # it and its children show up over the rest of the menu elements
        if self.activeMember is not None:
            self.activeMember.reparentTo(self)

        self.validate()

        self.inFinalize = 0

    # Functions to make the SCMenu object act just like a Python
    # list of SCElements
    #
    # Note that removing an element does not remove the element from
    # the menu visually; the owner of the element is responsible for
    # parenting it away somewhere else and/or destroying the element.
    # If you just want to clear out the entire menu, see clearMenu()
    # above.
    def append(self, element):
        # Appends a single element to the list so far.
        if isinstance(self.__members, types.TupleType):
            self.__members = list(self.__members)
        self.__members.append(element)
        self.privMemberListChanged(added=[element])

    def extend(self, elements):
        # Appends a list of elements to the list so far.
        # note that this operation invokes __iadd__
        self += elements

    def index(self, element):
        return self.__members.index(element)

    def __len__(self):
        return len(self.__members)

    def __getitem__(self, index):
        return self.__members[index]

    def __setitem__(self, index, value):
        if isinstance(self.__members, types.TupleType):
            self.__members = list(self.__members)
        removedMember = self.__members[index]
        self.__members[index] = value
        self.privMemberListChanged(added=[value], removed=[removedMember])

    def __delitem__(self, index):
        if isinstance(self.__members, types.TupleType):
            self.__members = list(self.__members)
        removedMember = self.__members[index]
        del self.__members[index]
        self.privMemberListChanged(removed=[removedMember])

    def __getslice__(self, i, j):
        if isinstance(self.__members, types.TupleType):
            self.__members = list(self.__members)
        return self.__members[i:j]

    def __setslice__(self, i, j, s):
        if isinstance(self.__members, types.TupleType):
            self.__members = list(self.__members)
        removedMembers = self.__members[i:j]
        self.__members[i:j] = list(s)
        self.privMemberListChanged(added=list(s), removed=removedMembers)

    def __delslice__(self, i, j):
        if isinstance(self.__members, types.TupleType):
            self.__members = list(self.__members)
        removedMembers = self.__members[i:j]
        del self.__members[i:j]
        self.privMemberListChanged(removed=removedMembers)

    def __iadd__(self, other):
        if isinstance(self.__members, types.TupleType):
            self.__members = list(self.__members)
        if isinstance(other, SCMenu):
            otherMenu = other
            other = otherMenu.__members
            del otherMenu[:]
        self.__members += list(other)
        self.privMemberListChanged(added=list(other))
        return self

    def privMemberListChanged(self, added=None, removed=None):
        assert added or removed
        
        if removed is not None:
            for element in removed:
                # if this element is our active member, we no longer have an
                # active member
                if element is self.activeMember:
                    self.__setActiveMember(None)
                # if this element has not been reassigned to a different
                # menu, make sure it knows it's not visible, and set its
                # parent to None
                if element.getParentMenu() is self:
                    if element.isVisible():
                        element.exitVisible()
                    element.setParentMenu(None)
                    element.reparentTo(hidden)

        if added is not None:
            for element in added:
                self.privAdoptSCObject(element)
                element.setParentMenu(self)

        # it's possible that we are now empty, or have become not-empty
        # tell our holder item to update its 'viewability' property
        if self.holder is not None:
            self.holder.updateViewability()

        # set a 'posInParentMenu' index value on each member
        for i in range(len(self.__members)):
            self.__members[i].posInParentMenu = i

        self.invalidate()

    def privSetSettingsRef(self, settingsRef):
        SCObject.privSetSettingsRef(self, settingsRef)
        # propogate the settings reference to our children
        for member in self:
            member.privSetSettingsRef(settingsRef)

    def invalidateAll(self):
        SCObject.invalidateAll(self)
        for member in self:
            member.invalidateAll()

    def finalizeAll(self):
        SCObject.finalizeAll(self)
        for member in self:
            member.finalizeAll()

    def getWidth(self):
        return self.width

    def __str__(self):
        return '%s: menu%s' % (self.__class__.__name__, self.SerialNum)
