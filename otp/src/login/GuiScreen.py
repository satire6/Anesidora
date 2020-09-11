"""GuiScreen"""

from pandac.PandaModules import *
from otp.otpbase import OTPGlobals
from direct.gui.DirectGui import *
from otp.otpgui import OTPDialog
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from direct.task.Task import Task

class GuiScreen:
    notify = DirectNotifyGlobal.directNotify.newCategory("GuiScreen")

    # Enter-press behaviors
    # Note: none of these prevent the entries' DirectGui 'command' handlers
    # from being invoked
    DGG.ENTERPRESS_ADVANCE = 0
    DGG.ENTERPRESS_ADVANCE_IFNOTEMPTY = 1
    DGG.ENTERPRESS_DONT_ADVANCE = 2
    DGG.ENTERPRESS_REMOVE_FOCUS = 3

    # standard entry width for all of the gui screens; a long email address
    # that fits on one screen should fit on every screen
    ENTRY_WIDTH = 20

    def __init__(self):
        self.waitingForDatabase = None
        self.focusIndex = None
        # when we set the focus explicitly, we don't want to play
        # the click sound
        self.suppressClickSound = 0
        
    def startFocusMgmt(self,
                       startFocus=0,
                       enterPressBehavior=DGG.ENTERPRESS_ADVANCE_IFNOTEMPTY,
                       overrides={},
                       globalFocusHandler=None):
        """
        Sets up handlers to handle management of input focus
        For now, you must set self.focusList before calling startFocusMgmt.
        
        GuiScreen hooks into the callbacks of DirectEntrys. Thus, GuiScreen
        is automatically notified when a DirectEntry focus item gains the
        input focus through a mouse click. The same is true for
        DirectScrolledLists.

        NOTE: between calls to startFocusMgmt and stopFocusMgmt, client
        code should not modify the following properties of DirectEntry
        and DirectScrolledList items that are in the focus list:
        -command
        -extraArgs
        -focusInCommand
        -focusInExtraArgs

        enterPressBehavior defines the default behavior for entries
        when Enter is pressed; it can be one of the values defined above,
        or simply a callback

        overrides is a dictionary of (entry, behavior) associations that
        specify exceptions to the default Enter-press behavior

        globalFocusHandler is a handler that will be called with the item
        that has just gained focus; it will be called just before the
        item's focusInCommand handler
        """
        GuiScreen.notify.debug('startFocusMgmt:\n'
                               'startFocus=%s,\n'
                               'enterPressBehavior=%s\n'
                               'overrides=%s' %
                               (startFocus, enterPressBehavior, overrides))

        self.accept('tab', self.__handleTab)
        self.accept('shift-tab', self.__handleShiftTab)

        # listen for enter presses so we can handle them for
        # non-DirectEntry widgets
        self.accept('enter', self.__handleEnter)

        # start a task to enable us to know at any point whether the
        # focus has already changed *this frame*
        self.__startFrameStartTask()

        self.userGlobalFocusHandler = globalFocusHandler

        # When we want to manually give the focus to a DirectEntry, we set
        # its 'focus' property to one, which generates a focus callback.
        # DirectGui calls the focus handlers for DirectEntrys at
        # the end of the frame. We manually call our focus handler
        # immediately when non-DirectEntry items get the focus.
        # This causes problems:
        # E is a DirectEntry, L is a DirectScrolledList
        # setFocus(E); setFocus(L)
        # __handleFocus(L) will be called immediately
        # __handleFocus(E) will be called at the end of the frame
        # To counter this, we manually call the focus handler for
        # _all_ focus items when they receive the focus, and maintain
        # a list of how many times each DirectEntry item got the focus
        # this frame. When DirectGui calls the callback at the end of
        # the frame, we 'absorb' the callbacks according to the number
        # of times each item got the focus during that frame.
        #
        # Note that we still need to listen for DirectEntry focus events,
        # in case the user clicks on a DirectEntry.
        self.focusHandlerAbsorbCounts = {}
        for i in xrange(len(self.focusList)):
            item = self.focusList[i]
            if isinstance(item, DirectEntry):
                self.focusHandlerAbsorbCounts[item] = 0

        # store the user's 'focus' and 'command' handlers
        self.userFocusHandlers = {}
        self.userCommandHandlers = {}

        for i in xrange(len(self.focusList)):
            item = self.focusList[i]
            if isinstance(item, DirectEntry):
                # store the old focus handler so that we can chain to it
                # and restore it
                self.userFocusHandlers[item] = (item['focusInCommand'],
                                                item['focusInExtraArgs'])
                # see discussion of focusHandlerAbsorbCounts above
                item['focusInCommand'] = self.__handleFocusChangeAbsorb
                item['focusInExtraArgs'] = [i]

                # store the old command handler so that we can chain to it
                # and restore it
                self.userCommandHandlers[item] = (item['command'],
                                                  item['extraArgs'])
                # we have our own Enter-press handlers; disable the Entry's
                item['command'] = None
                # this has to be a list (not a tuple)
                item['extraArgs'] = []
                
            elif isinstance(item, DirectScrolledList):
                # for DirectScrolledLists, 'command' is invoked whenever
                # the up/down controls are pressed; hook into that to
                # determine when the DSLists should gain focus

                # store the old handler so that we can chain to it
                # and restore it
                self.userCommandHandlers[item] = (item['command'],
                                                  item['extraArgs'])
                # hook the command handler so we can set the focus
                item['command'] = self.__handleDirectScrolledListCommand
                item['extraArgs'] = [i]

        # set up the Enter-press handlers
        self.enterPressHandlers = {}
        for i in xrange(len(self.focusList)):
            item = self.focusList[i]

            # pick an enter-press behavior
            behavior = enterPressBehavior
            if overrides.has_key(item):
                behavior = overrides[item]

            if callable(behavior):
                # the behavior is a callback
                self.enterPressHandlers[item] = behavior
            else:
                # DGG.ENTERPRESS_ADVANCE_IFNOTEMPTY is only meaningful for
                # DirectEntrys
                if ((not isinstance(item, DirectEntry)) and
                    (behavior == GuiScreen_ENTERPRESS_ADVANCE_IFNOTEMPTY)):
                    """ too much
                    GuiScreen.notify.debug(
                        "DGG.ENTERPRESS_ADVANCE_IFNOTEMPTY is not a valid "
                        "behavior for %s; defaulting to "
                        "DGG.ENTERPRESS_ADVANCE" % str(item))
                        """
                    behavior = GuiScreen_ENTERPRESS_ADVANCE

                commandHandlers = (
                    self.__alwaysAdvanceFocus,
                    self.__advanceFocusIfNotEmpty,
                    self.__neverAdvanceFocus,
                    self.__ignoreEnterPress,
                    )
                self.enterPressHandlers[item] = commandHandlers[behavior]

        self.setFocus(startFocus)

    def focusMgmtActive(self):
        return self.focusIndex != None

    def stopFocusMgmt(self):
        """
        Removes input focus management handlers
        OK to call even if startFocusMgmt has not been called
        OK to call multiple times in a row
        """
        GuiScreen.notify.debug('stopFocusMgmt')
        if not self.focusMgmtActive():
            return

        self.ignore('tab')
        self.ignore('shift-tab')

        self.ignore('enter')

        self.__stopFrameStartTask()

        self.userGlobalFocusHandler = None

        self.focusIndex = None

        self.focusHandlerAbsorbCounts = {}

        # restore the old focus and command handlers
        for item in self.focusList:
            if isinstance(item, DirectEntry):
                userHandler, userHandlerArgs = self.userFocusHandlers[item]
                item['focusInCommand'] = userHandler
                item['focusInExtraArgs'] = userHandlerArgs

                userHandler, userHandlerArgs = self.userCommandHandlers[item]
                item['command'] = userHandler
                item['extraArgs'] = userHandlerArgs
            elif isinstance(item, DirectScrolledList):
                userHandler, userHandlerArgs = self.userCommandHandlers[item]
                item['command'] = userHandler
                item['extraArgs'] = userHandlerArgs
        self.userFocusHandlers = {}
        self.userCommandHandlers = {}

        self.enterPressHandlers = {}

    def setFocus(self, arg, suppressSound=1):
        """setFocus(self, int|item)
        Sets the keyboard focus to the indicated field, which should
        be either an index into self.focusList or an actual item in the
        focusList.  If an index exceeds the length of the list, or is
        less than zero, it will be wrapped.
        """
        #GuiScreen.notify.spam('setFocus: %s' % arg)
        
        if type(arg) == type(0):
            index = arg
        else:
            assert arg in self.focusList
            index = self.focusList.index(arg)
        if suppressSound:
            self.suppressClickSound += 1
        self.__setFocusIndex(index)

    def advanceFocus(self, condition=1):
        """
        advances the keyboard focus to the next entry (if condition is true)
        curItem is the item that currently has the input focus
        """
        index = self.getFocusIndex()
        if condition:
            # on overflow, this will get wrapped in __setFocusIndex
            index += 1
        self.setFocus(index, suppressSound=0)

    def getFocusIndex(self):
        """
        Returns the index within focusList of the item that currently
        has focus.
        """
        if not self.focusMgmtActive():
            return None
        return self.focusIndex

    def getFocusItem(self):
        """
        Returns the item that has the input focus
        """
        if not self.focusMgmtActive():
            return None
        return self.focusList[self.focusIndex]

    def removeFocus(self):
        """
        removes focus from focus item so that nothing has input focus
        """
        #GuiScreen.notify.spam('removeFocus')
        focusItem = self.getFocusItem()
        if isinstance(focusItem, DirectEntry):
            focusItem['focus'] = 0

        if self.userGlobalFocusHandler:
            self.userGlobalFocusHandler(None)

    def restoreFocus(self):
        """
        call to restore the input focus after a call to removeFocus()
        """
        #GuiScreen.notify.spam('restoreFocus')
        self.setFocus(self.getFocusItem())

    def __setFocusIndex(self, index):
        """
        internal; wraps index; does not suppress the click sound
        """
        # self.focusIndex will be set in __handleFocusChange;
        # this function should simulate an external event that causes
        # a focus change (i.e., don't muck with the internal state
        # here, let __handleFocusChange do that)
        focusIndex = index % len(self.focusList)
        focusItem = self.focusList[focusIndex]
        if isinstance(focusItem, DirectEntry):
            focusItem['focus'] = 1
            # bump up the focus event absorb count, and
            # manually call the handler immediately
            self.focusHandlerAbsorbCounts[focusItem] += 1

        # force a call to focus change handler
        self.__handleFocusChange(focusIndex)

    def __chainToUserCommandHandler(self, item):
        # call the user 'command' handler, if any
        # DirectEntry command handlers accept a text string; pass
        # that text as 'enteredText'
        # for DirectEntrys, 'command' is invoked by pressing Enter
        # for DirectScrolledLists, 'command' is invoked by pressing
        # on the up or down button
        userHandler, userHandlerArgs = self.userCommandHandlers[item]
        if userHandler:
            if isinstance(item, DirectEntry):
                enteredText = item.get()
                apply(userHandler, [enteredText] + userHandlerArgs)
            elif isinstance(item, DirectScrolledList):
                apply(userHandler, userHandlerArgs)

    def __chainToUserFocusHandler(self, item):
        # call the user focus handler, if any
        if isinstance(item, DirectEntry):
            userHandler, userHandlerArgs = self.userFocusHandlers[item]
            if userHandler:
                apply(userHandler, userHandlerArgs)

    ### TAB key handlers ##########

    # 'focusDirection' allows focus handlers to manipulate
    # the focus; self.focusDirection is guaranteed to
    # be 1 or -1
    def __handleTab(self):
        self.tabPressed = 1
        self.focusDirection = 1
        self.__setFocusIndex(self.getFocusIndex() + self.focusDirection)

    def __handleShiftTab(self):
        self.tabPressed = 1
        self.focusDirection = -1
        self.__setFocusIndex(self.getFocusIndex() + self.focusDirection)

    ### Focus change handler ###########

    def __handleFocusChangeAbsorb(self, index):
        # this handler is called by DirectGui (at the end of the
        # frame; see startFocusMgmt() for details)
        item = self.focusList[index]
        if self.focusHandlerAbsorbCounts[item] > 0:
            self.focusHandlerAbsorbCounts[item] -= 1
        else:
            self.__handleFocusChange(index)

    def playFocusChangeSound(self):
        base.playSfx(DGG.getDefaultClickSound())

    def __handleFocusChange(self, index):
        #print ("__handleFocusChange: %s" % index)

        # if the focus is moving, make sure to remove the focus from
        # the current focus item
        if index != self.focusIndex:
            self.removeFocus()

        self.__focusChangedThisFrame = 1

        if hasattr(self, 'tabPressed'):
            # tab was just pressed, focusDirection is already set
            del self.tabPressed
        else:
            self.focusDirection = 1

        # update our record of who has the focus
        self.focusIndex = index

        # should we play a sound?
        if self.suppressClickSound > 0:
            self.suppressClickSound -= 1
        else:
            self.playFocusChangeSound()

        # keep a copy of the current focus index, in case
        # one of the callbacks changes it
        focusItem = self.getFocusItem()

        # chain to the global focus handler
        if self.userGlobalFocusHandler:
            self.userGlobalFocusHandler(focusItem)

        # TODO: what should we do if they've changed the focus?
        # should we still call the item's focus handler?
        # at this point, have the new item's handler calls already been made?
        if self.getFocusItem() != focusItem:
            GuiScreen.notify.debug("focus changed by global focus handler")

        # global focus handler may have shut us down
        if self.focusMgmtActive():
            # call the user focus handler, if any
            self.__chainToUserFocusHandler(focusItem)

    ### FrameStart task ##############
    def __startFrameStartTask(self):
        self.__focusChangedThisFrame = 0
        self.frameStartTaskName = 'GuiScreenFrameStart'
        taskMgr.add(self.__handleFrameStart, self.frameStartTaskName, -100)
        
    def __stopFrameStartTask(self):
        taskMgr.remove(self.frameStartTaskName)
        del self.frameStartTaskName
        del self.__focusChangedThisFrame

    def __handleFrameStart(self, task):
        # reset the 'changed' flag; this occurs at the
        # beginning of the frame
        self.__focusChangedThisFrame = 0
        return Task.cont

    ### DirectScrolledList command handler ##############
    def __handleDirectScrolledListCommand(self, index):
        self.__chainToUserCommandHandler(self.focusList[index])
        # set the focus to this item
        # don't play a sound if this DirectScrolledList already has the focus
        self.setFocus(index, suppressSound=(self.getFocusIndex()==index))

    ### DGG.ENTER key handler ##########

    def __handleEnter(self):
        # if the focus already changed this frame, and Enter was pressed,
        # there's a good chance that this same Enter press event just
        # caused the focus change (DirectEntrys independently listen for
        # Enter on their own and trigger their 'command' handler)
        # Assuming that's true, we should ignore this event.
        if self.__focusChangedThisFrame:
            return

        # this event pertains to the current focus item
        focusItem = self.getFocusItem()

        # DirectEntrys' command handlers are called when Enter is pressed
        if isinstance(focusItem, DirectEntry):
            self.__chainToUserCommandHandler(focusItem)

        # user handler may have shut us down or changed the focus
        if (self.focusMgmtActive() and
            focusItem == self.getFocusItem()):
            # call the enter-press handler for the focus item
            self.enterPressHandlers[focusItem]()


    ### DGG.ENTER key behavior handlers ############

    def __alwaysAdvanceFocus(self):
        """
        when enter is pressed, the focus will move to the next field
        """
        # move the focus forward
        self.advanceFocus()

    def __advanceFocusIfNotEmpty(self):
        """
        when enter is pressed, the focus will move to the next field
        if there is text entered in the current field. otherwise, it
        will stay in the current field
        """
        # this event pertains to the current focus item
        focusItem = self.getFocusItem()
        assert isinstance(focusItem, DirectEntry)
        enteredText = focusItem.get()

        if enteredText != "":
            # if there is text entered, move the focus forward
            self.advanceFocus()
        else:
            # restore the focus to the current item
            self.setFocus(self.getFocusIndex())

    def __neverAdvanceFocus(self):
        """
        when enter is pressed, focus is always restored to current item
        """
        # restore the focus to the current item
        self.setFocus(self.getFocusIndex())

    def __ignoreEnterPress(self):
        """
        when enter is pressed, nothing happens (input focus is lost)
        """
        pass


    # Deal with timeouts and such:

    # Maybe GuiScreen.py isn't the best place for this.  Please move this
    # as you see fit.  Right now, it is common that a GuiScreen will talk
    # to the game server and thus will make use of these timeout handlers.

    def waitForDatabaseTimeout(self, requestName='unknown'):
        # If nothing happens within a few seconds, pop up a dialog to
        # show we're still hanging on, and to give the user a chance
        # to bail.
        GuiScreen.notify.debug(
            'waiting for database timeout %s at %s' %
            (requestName, globalClock.getFrameTime()))
        globalClock.tick()
        taskMgr.doMethodLater(OTPGlobals.DatabaseDialogTimeout,
                              self.__showWaitingForDatabase,
                              "waitingForDatabase", extraArgs=[requestName])

    def __showWaitingForDatabase(self, requestName):
        GuiScreen.notify.info("timed out waiting for %s at %s" % (
            requestName, globalClock.getFrameTime()))
        dialogClass = OTPGlobals.getDialogClass()
        self.waitingForDatabase = dialogClass(
            text = OTPLocalizer.GuiScreenToontownUnavailable,
            dialogName = "WaitingForDatabase",
            buttonTextList = [OTPLocalizer.GuiScreenCancel],
            style = OTPDialog.Acknowledge,
            command = self.__handleCancelWaiting)
        self.waitingForDatabase.show()
        taskMgr.doMethodLater(OTPGlobals.DatabaseGiveupTimeout,
                              self.__giveUpWaitingForDatabase,
                              "waitingForDatabase", extraArgs=[requestName])
        return Task.done

    def __giveUpWaitingForDatabase(self, requestName):
        GuiScreen.notify.info("giving up waiting for %s at %s" % (
            requestName, globalClock.getFrameTime()))
        self.cleanupWaitingForDatabase()
        messenger.send(self.doneEvent, [{'mode': 'failure'}])
        return Task.done

    def cleanupWaitingForDatabase(self):
        if self.waitingForDatabase != None:
            self.waitingForDatabase.cleanup()
            self.waitingForDatabase = None
        taskMgr.remove("waitingForDatabase")

    def __handleCancelWaiting(self, value):
        self.cleanupWaitingForDatabase()
        messenger.send(self.doneEvent, [{'mode': 'quit'}])
