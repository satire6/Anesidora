"""Place module: contains the Place class"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *

from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from toontown.safezone import PublicWalk
from toontown.launcher import DownloadForceAcknowledge
import TrialerForceAcknowledge
import ZoneUtil
from toontown.friends import FriendsListManager
from toontown.toonbase import ToontownGlobals
from toontown.estate import HouseGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from otp.avatar import Emote
from direct.task import Task
import QuietZoneState
from toontown.distributed import ToontownDistrictStats

class Place(StateData.StateData,
            FriendsListManager.FriendsListManager):
    """
    This class is the parent of Playground, Street, Estate, etc., and defines
    functionality common to all. It defines implementations of various
    localToon states, but does not itself define an ClassicFSM.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("Place")
    
    def __init__(self, loader, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        FriendsListManager.FriendsListManager.__init__(self)
        self.loader = loader
        self.dfaDoneEvent = "dfaDoneEvent"
        self.trialerFADoneEvent = 'trialerFADoneEvent'
        self.zoneId = None
        self.trialerFA = None
        # We don't keep a pointer to the FriendInvitee panel, since we
        # expect that to remain onscreen until the user deals with it,
        # even when switching hoods etc.

    def load(self):
        assert(self.notify.info("loading Place"))
        StateData.StateData.load(self)
        FriendsListManager.FriendsListManager.load(self)
        self.walkDoneEvent = "walkDone"
        self.walkStateData = PublicWalk.PublicWalk(self.fsm,
                                                   self.walkDoneEvent)
        self.walkStateData.load()

        self._tempFSM = self.fsm

    def unload(self):
        StateData.StateData.unload(self)
        FriendsListManager.FriendsListManager.unload(self)
        self.notify.info("Unloading Place (%s). Fsm in %s" % (self.zoneId, self._tempFSM.getCurrentState().getName()))
        del self._tempFSM
        taskMgr.remove("goHomeFailed")
        del self.walkDoneEvent
        self.walkStateData.unload()
        del self.walkStateData
        del self.loader
        if self.trialerFA:
            self.trialerFA.exit()
            del self.trialerFA

    def setState(self, state):
        assert(self.notify.debug("setState(state="+str(state)+")"))
        if hasattr(self, 'fsm'):
            curState = self.fsm.getName()
            if state == "pet" or curState == "pet":
                self.preserveFriendsList()
            self.fsm.request(state)

    def getState(self):
        assert(self.notify.debug("getState"))
        if hasattr(self, 'fsm'):
            curState = self.fsm.getCurrentState().getName()
            return curState

    def getZoneId(self):
        """
        Returns the current zone ID.  This is either the same as the
        hoodID for a SafeZone class, or the current zoneId for a Street
        class.
        """
        return self.zoneId

    def getTaskZoneId(self):
        """
        subclasses can override this to fool the task system into thinking
        that we're in a different zone (i.e. you can return a hood id when
        we're actually in a dynamically-allocated zone)
        """
        return self.getZoneId()

    def isPeriodTimerEffective(self):
        """
        Returns true if the period timer will be honored if it expires
        in this kind of Place (and we're also in a suitable mode).
        Generally, SuitInterior returns false, and other kinds of
        Place return true.
        """
        return 1

    def handleTeleportQuery(self, fromAvatar, toAvatar):
        """
        Called when another avatar somewhere in the world wants to
        teleport to us, and we're available to be teleported to.
        """
        fromAvatar.d_teleportResponse(toAvatar.doId, 1, toAvatar.defaultShard,
                                      base.cr.playGame.getPlaceId(), self.getZoneId())

    def enablePeriodTimer(self):
        """
        Called on entering a particular state that will respect the
        period timer, this sets up the hooks to detect when the period
        timer has expired.  If the timer then expires, the toon will
        automatically pull out his hole and exit the game gracefully.
        """
        if self.isPeriodTimerEffective():
            if base.cr.periodTimerExpired:
                # If the timer has already expired, it must have happened
                # when we were in some other state and we weren't
                # listening.  We could respond immediately, but I think
                # that looks a little funny (your toon runs through a
                # tunnel and immediately pulls out his hole and jumps in
                # when he gets to the other side).  Instead, we'll trigger
                # the event in a few seconds, say about 5.
                taskMgr.doMethodLater(5, self.redoPeriodTimer, "redoPeriodTimer")
            self.accept("periodTimerExpired", self.periodTimerExpired)

    def disablePeriodTimer(self):
        """
        Undoes the effect of enablePeriodTimer().
        """
        taskMgr.remove("redoPeriodTimer")
        self.ignore("periodTimerExpired")

    def redoPeriodTimer(self, task):
        messenger.send("periodTimerExpired")
        return Task.done

    def periodTimerExpired(self):
        """
        The period timer has just expired.  Go away.
        """
        self.fsm.request('final')
        if base.localAvatar.book.isEntered:
            # if the book is open, close it first.
            base.localAvatar.book.exit()
            base.localAvatar.b_setAnimState('CloseBook', 1,
                                              callback = self.__handlePeriodTimerBookClose)
        else:
            # if the book is not open, just leave.
            base.localAvatar.b_setAnimState('TeleportOut', 1,
                                              self.__handlePeriodTimerExitTeleport)

    def exitPeriodTimerExpired(self):
        pass

    def __handlePeriodTimerBookClose(self):
        base.localAvatar.b_setAnimState('TeleportOut', 1,
                                          self.__handlePeriodTimerExitTeleport)

    def __handlePeriodTimerExitTeleport(self):
        base.cr.loginFSM.request("periodTimeout")

    def detectedPhoneCollision(self):
        assert(self.notify.debug("detectedPhoneCollision"))
        self.fsm.request('phone')

    def detectedFishingCollision(self):
        assert(self.notify.debug("detectedFishingCollision()"))
        self.fsm.request("fishing")

    # start state

    def enterStart(self):
        assert(self.notify.debug("enterStart()"))

    def exitStart(self):
        assert(self.notify.debug("exitStart()"))

    # final state

    def enterFinal(self):
        assert(self.notify.debug("enterFinal()"))
    
    def exitFinal(self):
        assert(self.notify.debug("exitFinal()"))

    # walk state

    def enterWalk(self, teleportIn=0):
        #import pdb; pdb.set_trace()
        assert self.notify.debugStateCall(self)
        """
        Allow the user to navigate and chat
        """
        # The friends list is available here.
        self.enterFLM()

        self.walkStateData.enter()
        if (teleportIn == 0):
            self.walkStateData.fsm.request("walking")
        self.acceptOnce(self.walkDoneEvent, self.handleWalkDone)
        # if we are US, unpaid, and not in tutorial, show the chat buttons
        if ((base.cr.productName in ["DisneyOnline-US", "ES"]) and
            (not base.cr.isPaid()) and
            (base.localAvatar.tutorialAck)):
            base.localAvatar.chatMgr.obscure(0,0)
            base.localAvatar.chatMgr.normalButton.show()
        # People can teleport to us in walk mode.
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.questPage.acceptOnscreenHooks()
        base.localAvatar.invPage.acceptOnscreenHooks()
        #*#base.localAvatar.setActiveShadow(1)
        self.walkStateData.fsm.request('walking')
        self.enablePeriodTimer()

    def exitWalk(self):
        # The friends list is no longer available.
        self.exitFLM()

        # if we are US, unpaid, not in tutorial, hide the chat button
        if ((base.cr.productName in ["DisneyOnline-US", "ES"]) and
            (not base.cr.isPaid()) and
            (base.localAvatar.tutorialAck) and (not base.cr.whiteListChatEnabled)):
            base.localAvatar.chatMgr.obscure(1,0)
        # If we aren't in walk, we can't be sleeping
        self.disablePeriodTimer()
        messenger.send("wakeup")
        self.walkStateData.exit()
        self.ignore(self.walkDoneEvent)
        # Clean up teleport handling.
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        #*#base.localAvatar.setActiveShadow(0)
        # Put away the "welcome" sign
        #self.loader.hood.hideTitleText()
        if base.cr.playGame.hood != None:
            base.cr.playGame.hood.hideTitleText()
        base.localAvatar.questPage.hideQuestsOnscreen()
        base.localAvatar.questPage.ignoreOnscreenHooks()
        base.localAvatar.invPage.ignoreOnscreenHooks()
        base.localAvatar.invPage.hideInventoryOnscreen()

    # this is no longer private as we need to call it from
    # other functions
    def handleWalkDone(self, doneStatus):
        mode = doneStatus["mode"]
        if mode == "StickerBook":
            self.last = self.fsm.getCurrentState().getName()
            self.fsm.request("stickerBook")
        elif mode == "Options":
            self.last = self.fsm.getCurrentState().getName()
            self.fsm.request("stickerBook", [base.localAvatar.optionsPage])
        elif mode == "Sit":
            self.last = self.fsm.getCurrentState().getName()
            self.fsm.request("sit")
        else:
            Place.notify.error("Invalid mode: %s" % mode)

    # sit state
    
    def enterSit(self):
        # The friends list is available here.
        self.enterFLM()
        # The laffmeter is visible.
        base.localAvatar.laffMeter.start()
        # People can teleport to us in sit  mode.
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        # Play the sit animations
        base.localAvatar.b_setAnimState('SitStart', 1)
        # Just push up to get up again
        self.accept("arrow_up", self.fsm.request, extraArgs=['walk'])

    def exitSit(self):
        # The friends list is no longer available.
        self.exitFLM()
        base.localAvatar.laffMeter.stop()
        # Clean up teleport handling.
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        self.ignore("arrow_up")

    # drive state
    
    def enterDrive(self):
        # The friends list is available here.
        self.enterFLM()
        # The laffmeter is visible.
        base.localAvatar.laffMeter.start()
        # People can teleport to us in drive  mode.
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        # Play the drive animations
        base.localAvatar.b_setAnimState('SitStart', 1)

    def exitDrive(self):
        # The friends list is no longer available.
        self.exitFLM()
        base.localAvatar.laffMeter.stop()
        # Clean up teleport handling.
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")

    # push state
    
    def enterPush(self):
        # The friends list is available here.
        self.enterFLM()
        # The laffmeter is visible.
        base.localAvatar.laffMeter.start()
        # People can teleport to us in push mode.
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)

        # Start the smart camera, to put it in the right place, but be
        # prepared to stop it again in exitPush
        base.localAvatar.attachCamera()
        base.localAvatar.startUpdateSmartCamera()

        # Specifically start posHpr broadcast since we aren't
        # exiting walk state disables it
        base.localAvatar.startPosHprBroadcast()
        # Play the 'push' animation
        base.localAvatar.b_setAnimState('Push', 1)

    def exitPush(self):
        # The friends list is no longer available.
        self.exitFLM()
        base.localAvatar.laffMeter.stop()
        # Clean up teleport handling.
        base.localAvatar.setTeleportAvailable(0)
        # Stop the tasks which we started above.
        base.localAvatar.stopUpdateSmartCamera()
        base.localAvatar.detachCamera()
        base.localAvatar.stopPosHprBroadcast()
        self.ignore("teleportQuery")


    # sticker book state

    def enterStickerBook(self, page = None):
        # The friends list is available here.
        self.enterFLM()

        # The laffmeter is visible.
        base.localAvatar.laffMeter.start()

        # Hide the cannon game GUI if present
        target = base.cr.doFind("DistributedTarget")
        if target:
            target.hideGui()
            
        # People can teleport to us in book mode.
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        if page:
            base.localAvatar.book.setPage(page)
        # Play the open book animation
        base.localAvatar.b_setAnimState('OpenBook', 1, 
                                          self.enterStickerBookGUI)
        base.localAvatar.obscureMoveFurnitureButton(1)

    def enterStickerBookGUI(self):
        base.localAvatar.collisionsOn()
        base.localAvatar.book.showButton()
        base.localAvatar.book.enter()
        base.localAvatar.setGuiConflict(1)
        # Spawn the task that checks to see if toon has fallen asleep
        base.localAvatar.startSleepWatch(self.__handleFallingAsleep)
        # Hang hooks for when selection is made
        self.accept("bookDone", self.__handleBook)
        self.accept(ToontownGlobals.OptionsPageHotkey, self.__escCloseBook)

        # Play read book animation
        base.localAvatar.b_setAnimState('ReadBook', 1)
        self.enablePeriodTimer()

    def __handleFallingAsleep(self, task):
        # Close the book first
        base.localAvatar.book.exit()
        base.localAvatar.b_setAnimState('CloseBook', 1,
                           callback = self.__handleFallingAsleepBookClose)
        return Task.done

    def __handleFallingAsleepBookClose(self):
        if hasattr(self, "fsm"):
            #the place has been unloaded... ignore this request
            self.fsm.request("walk")
        base.localAvatar.forceGotoSleep()

    def __escCloseBook(self):
        """
        User hit esc to get out of book
        """
        if hasattr(localAvatar, "newsPage") and localAvatar.book.isOnPage(localAvatar.newsPage):
            localAvatar.newsButtonMgr.simulateEscapeKeyPress()
        else:
            base.localAvatar.stopSleepWatch()
            base.localAvatar.book.exit()
            base.localAvatar.b_setAnimState(
                'CloseBook', 1, callback = self.handleBookClose)

    def exitStickerBook(self):
        base.localAvatar.stopSleepWatch()
        self.disablePeriodTimer()
        # The friends list is no longer available.
        self.exitFLM()

        base.localAvatar.laffMeter.stop()

        base.localAvatar.setGuiConflict(0)
        base.localAvatar.book.exit()
        base.localAvatar.book.hideButton()
        base.localAvatar.collisionsOff()
        self.ignore("bookDone")
        self.ignore(ToontownGlobals.OptionsPageHotkey)

        # Clean up teleport handling.
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        base.localAvatar.obscureMoveFurnitureButton(-1)

        # Show the cannon game GUI if present
        target = base.cr.doFind("DistributedTarget")
        if target:
            target.showGui()

    def __handleBook(self):
        base.localAvatar.stopSleepWatch()
        base.localAvatar.book.exit()
        bookStatus = base.localAvatar.book.getDoneStatus()
        if (bookStatus["mode"] == "close"):
            # Play the close book animation
            base.localAvatar.b_setAnimState(
                    'CloseBook', 1,
                    callback = self.handleBookClose)
        elif (bookStatus["mode"] == "teleport"):
            # Play the close book animation
            zoneId = bookStatus["hood"]
            # We don't want to start a battle after toon chooses to teleport!
            base.localAvatar.collisionsOff()
            base.localAvatar.b_setAnimState(
                    'CloseBook', 1,
                    callback = self.handleBookCloseTeleport,
                    extraArgs = [zoneId, zoneId])
        elif (bookStatus["mode"] == "exit"):
            self.exitTo = bookStatus.get('exitTo') 
            # Play the close book animation
            base.localAvatar.collisionsOff()
            base.localAvatar.b_setAnimState(
                    'CloseBook', 1,
                    callback = self.__handleBookCloseExit)
        elif (bookStatus["mode"] == "gohome"):
            zoneId = bookStatus["hood"]
            # Play the close book animation
            base.localAvatar.collisionsOff()
            base.localAvatar.b_setAnimState(
                'CloseBook', 1,
                callback = self.goHomeNow,
                extraArgs = [zoneId])
        elif (bookStatus["mode"] == "startparty"):
            firstStart = bookStatus["firstStart"]
            hostId = bookStatus["hostId"]
            # Play the close book animation
            base.localAvatar.collisionsOff()
            base.localAvatar.b_setAnimState(
                'CloseBook', 1,
                callback = self.startPartyNow,
                extraArgs=[firstStart, hostId],
            )

    def handleBookCloseTeleport(self, hoodId, zoneId):
        # The local avatar cannot leave the zone if he is part of a boarding group.
        if localAvatar.hasActiveBoardingGroup():
            rejectText = TTLocalizer.BoardingCannotLeaveZone
            localAvatar.elevatorNotifier.showMe(rejectText)
            return
        # Pass avId of -1 if you are teleporting to a safe zone
        self.requestLeave({
            "loader": ZoneUtil.getBranchLoaderName(zoneId),
            "where": ZoneUtil.getToonWhereName(zoneId),
            "how" : "teleportIn",
            "hoodId" : hoodId,
            "zoneId" : zoneId,
            "shardId" : None,
            "avId" : -1
            })
            
    def __handleBookCloseExit(self):
        base.localAvatar.b_setAnimState('TeleportOut', 1,
                self.__handleBookExitTeleport, [0])

    def __handleBookExitTeleport(self, requestStatus):
        if base.cr.timeManager:
            base.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectBookExit)

        # usually the quiet zone state fades the screen out, but we're not going
        # through the quiet zone
        base.transitions.fadeScreen(1.0)
            
        base.cr.gameFSM.request(self.exitTo)

    def goHomeNow(self, curZoneId):
        # The local avatar cannot leave the zone if he is part of a boarding group.
        if localAvatar.hasActiveBoardingGroup():
            rejectText = TTLocalizer.BoardingCannotLeaveZone
            localAvatar.elevatorNotifier.showMe(rejectText)
            return
        # We will get this process started before we have heard back
        # from the AI which zone we'll be using for the estate.
        # We do this so there is some immediate animation in response to the
        # goHome button press.  If we wait for the server response before
        # starting the animation, and there is a lot of lag in the system,
        # the user might be tempted to press the button repeatedly until
        # he sees something happen.
        hoodId = ToontownGlobals.MyEstate
        # check if we still have an fsm.  if we don't, it means
        # we have already left the Estate, probably because the
        # owner booted us out.
        self.requestLeave({
            #"loader": "estateLoader",
            "loader": "safeZoneLoader",
            "where": "estate",
            "how" : "teleportIn",
            "hoodId" : hoodId,
            "zoneId" : -1,
            "shardId" : None,
            "avId" : -1,
            })

    def startPartyNow(self, firstStart, hostId):
        # The local avatar cannot leave the zone if he is part of a boarding group.
        if localAvatar.hasActiveBoardingGroup():
            rejectText = TTLocalizer.BoardingCannotLeaveZone
            localAvatar.elevatorNotifier.showMe(rejectText)         
            return
        base.localAvatar.creatingNewPartyWithMagicWord = False
        base.localAvatar.aboutToPlanParty = False
        hoodId = ToontownGlobals.PartyHood
        # If we're starting the party for the 1st time, find the least populated shard
        if firstStart:
            # we crash when zoneId is -1, localAvatar.zoneId gets set to it
            # then we try to send it over the wire we get a range error
            zoneId = 0
            ToontownDistrictStats.refresh('shardInfoUpdated')
            # We need to find the lowest populated shard and have the party there
            curShardTuples = base.cr.listActiveShards()
            # Tuple is of form : (shardId, name, pop, WelcomeValleyPopulation)
            lowestPop = 100000000000000000
            shardId = None
            for shardInfo in curShardTuples:
                pop = shardInfo[2]
                if pop < lowestPop:
                    lowestPop = pop
                    shardId = shardInfo[0]
            if shardId == base.localAvatar.defaultShard:
                shardId = None
            base.cr.playGame.getPlace().requestLeave({
                "loader": "safeZoneLoader",
                "where": "party",
                "how" : "teleportIn",
                "hoodId" : hoodId,
                "zoneId" : zoneId,
                "shardId" : shardId,
                "avId" : -1,
            })
        # If we're going back to a party we've started or are a guest of a party
        else:
            if hostId is None:
                hostId = base.localAvatar.doId
            base.cr.partyManager.sendAvatarToParty(hostId)
            return

    def handleBookClose(self):
        # SafeZones that have the walkStateData in modes other than walking
        # should override this function.
        if hasattr(self, 'fsm'):
            self.fsm.request("walk")
        # GRW - this was breaking the sad-walk stuff
        # base.localAvatar.b_setAnimState('neutral', 1)
        
        # If we are underwater, we should swim.
        if hasattr(self, 'toonSubmerged') and self.toonSubmerged == 1:
            if hasattr(self, 'walkStateData'):
                self.walkStateData.fsm.request("swimming", [self.loader.swimSound])
    
    def requestLeave(self, requestStatus):
        # Request to leave the current location and go somewhere else.
        if hasattr(self, 'fsm'):
            self.doRequestLeave(requestStatus)

    def doRequestLeave(self, requestStatus):
        # ** If you want to go to a different state before entering DFA,
        # override this.
        # This was added to accomodate the trialerFA; we want to do the
        # trialer check before the download check, so that we don't get
        # their hopes up
        self.fsm.request('DFA', [requestStatus])

    def enterDFA(self, requestStatus):
        """
        NOTE: TTPlayground redefines this because the TT streets are in phase 5,
        not the same phase as the safe zone like the rest of the hoods
        """
        self.acceptOnce(self.dfaDoneEvent, self.enterDFACallback, [requestStatus])
        self.dfa = DownloadForceAcknowledge.DownloadForceAcknowledge(self.dfaDoneEvent)
        self.dfa.enter(base.cr.hoodMgr.getPhaseFromHood(requestStatus["hoodId"]))
        
    def exitDFA(self):
        self.ignore(self.dfaDoneEvent)
            
    def handleEnterTunnel(self, requestStatus, collEntry):
        """
        Note: TutorialSafeZone overrides this function.
        """
        # The local avatar cannot leave the zone if he is part of a boarding group.
        if localAvatar.hasActiveBoardingGroup():
            rejectText = TTLocalizer.BoardingCannotLeaveZone
            localAvatar.elevatorNotifier.showMe(rejectText)
            
            dummyNP = NodePath('dummyNP')
            dummyNP.reparentTo(render)
            tunnelOrigin = requestStatus["tunnelOrigin"]
            dummyNP.setPos(localAvatar.getPos())
            dummyNP.setH(tunnelOrigin.getH())
            dummyNP.setPos(dummyNP, 0, 4, 0)
            localAvatar.setPos(dummyNP.getPos())
            dummyNP.removeNode()
            del dummyNP
            return
        
        self.requestLeave(requestStatus)

    def enterDFACallback(self, requestStatus, doneStatus):
        """
        Note: the SafeZone.py overrides this becuase the safe zone needs to
        check your health meter before letting you into the tunnel too.
        """
        self.dfa.exit()
        del self.dfa
        # Check the status from the fda
        # If the download force acknowledge tells us the download is complete, then
        # we can enter the tunnel, otherwise for now we just stand there
        # Allowed, do the tunnel transition
        if (doneStatus["mode"] == "complete"):
            # We may be tunneling or teleporting, either way, we simply
            # request the mode and send the status
            if requestStatus.get("tutorial", 0):
                # This is to handle the peculiar case of leaving the
                # tutorial tunnel. We walk out via the tunnel, but
                # teleport into the toontown central playground.
                out = {"teleportIn":"tunnelOut"}
                # make the tutorial put toon in Welcome Valley
                requestStatus['zoneId'] = 22000
                requestStatus['hoodId'] = 22000
            else:
                out = {"teleportIn":"teleportOut",
                       "tunnelIn":"tunnelOut",
                       "doorIn":"doorOut"}
 
            assert(self.notify.info("HOW: " + out[requestStatus["how"]]))
            self.fsm.request(out[requestStatus["how"]], [requestStatus])
        # Rejected
        elif (doneStatus["mode"] == 'incomplete'):
            self.fsm.request("DFAReject")
        else:
            # Some return code that is not handled
            Place.notify.error("Unknown done status for DownloadForceAcknowledge: "
                              + `doneStatus`)

    def enterDFAReject(self):
        # TODO: reject movie, turn toon around
        self.fsm.request("walk")
    
    def exitDFAReject(self):
        pass

    # prevent trialers from leaving TTC
    def enterTrialerFA(self, requestStatus):
        self.acceptOnce(self.trialerFADoneEvent, self.trialerFACallback,
                        [requestStatus])
        self.trialerFA = TrialerForceAcknowledge.TrialerForceAcknowledge(
            self.trialerFADoneEvent)
        self.trialerFA.enter(requestStatus["hoodId"])

    def exitTrialerFA(self):
        pass

    def trialerFACallback(self, requestStatus, doneStatus):
        if (doneStatus["mode"] == 'pass'):
            self.fsm.request('DFA', [requestStatus])
        elif (doneStatus["mode"] == 'fail'):
            self.fsm.request('trialerFAReject')
        else:
            # Some return code that is not handled
            Place.notify.error(
                "Unknown done status for TrialerForceAcknowledge: %s" %
                doneStatus)

    def enterTrialerFAReject(self):
        self.fsm.request('walk')

    def exitTrialerFAReject(self):
        pass

    # door in state

    def enterDoorIn(self, requestStatus):
        assert(self.notify.debug("enterDoorIn(requestStatus="
                +str(requestStatus)+")"))
        # Turn off the little red arrows while we pass through the
        # door.
        NametagGlobals.setMasterArrowsOn(0)

        door=base.cr.doId2do.get(requestStatus['doorDoId'])
        assert(door)
        door.readyToExit()
        #door_origin=door.getDoorNodePath()
        #assert(not door_origin.isEmpty())
        #camera.setPosHprScale(
        #    VBase3(-1.5, 5, 5),
        #    VBase3(180, 0, 0),
        #    VBase3(1, 1, 1),
        #    other=door_origin)
        base.localAvatar.obscureMoveFurnitureButton(1)

    def exitDoorIn(self):
        assert(self.notify.debug("exitDoorIn()"))

        # Turn on the little red arrows now that we're done passing
        # through the door.
        NametagGlobals.setMasterArrowsOn(1)
        base.localAvatar.obscureMoveFurnitureButton(-1)

    # door out state

    def enterDoorOut(self):
        assert(self.notify.debug("enterDoorOut()"))
        base.localAvatar.obscureMoveFurnitureButton(1)

    def exitDoorOut(self):
        assert(self.notify.debug("exitDoorOut()"))
        base.localAvatar.obscureMoveFurnitureButton(-1)

    def handleDoorDoneEvent(self, requestStatus):
        assert(self.notify.debug("handleDoorDoneEvent(requestStatus="
                +str(requestStatus)+")"))
        self.doneStatus=requestStatus
        messenger.send(self.doneEvent)

    def handleDoorTrigger(self):
        assert(self.notify.debug("handleDoorTrigger()"))
        self.fsm.request("doorOut")

    # tunnel in state

    def enterTunnelIn(self, requestStatus):
        self.notify.debug("enterTunnelIn(requestStatus="+str(requestStatus)+")")
        # By now, you are already in the hood and zone
        # Find the node we are supposed to position the toon relative to
        tunnelOrigin = base.render.find(requestStatus["tunnelName"])
        assert not tunnelOrigin.isEmpty(), \
                "did not find tunnelOrigin: "+requestStatus["tunnelName"]
        self.accept("tunnelInMovieDone", self.__tunnelInMovieDone)
        base.localAvatar.reconsiderCheesyEffect()
        base.localAvatar.tunnelIn(tunnelOrigin)
        
    def __tunnelInMovieDone(self):
        self.ignore("tunnelInMovieDone")
        self.fsm.request('walk')
        # the remote clients may still be showing the tunnel in movie;
        # sending these messages might mess them up, and they're unnecessary
        #base.localAvatar.d_broadcastPositionNow()
        #base.localAvatar.d_setParent(ToontownGlobals.SPRender)

    def exitTunnelIn(self):
        assert(self.notify.debug("exitTunnelIn()"))

    # tunnel out state

    def enterTunnelOut(self, requestStatus):
        assert(self.notify.debug("enterTunnelOut(requestStatus="+str(requestStatus)+")"))
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        how = requestStatus["how"]
        tunnelOrigin = requestStatus["tunnelOrigin"]
        fromZoneId = ZoneUtil.getCanonicalZoneId(self.getZoneId())
        tunnelName = requestStatus.get("tunnelName")
        if tunnelName == None:
            tunnelName = base.cr.hoodMgr.makeLinkTunnelName(
                self.loader.hood.id, fromZoneId)
        self.doneStatus = {"loader": ZoneUtil.getLoaderName(zoneId),
                           "where": ZoneUtil.getToonWhereName(zoneId),
                           "how" : how,
                           "hoodId" : hoodId,
                           "zoneId" : zoneId,
                           "shardId" : None,
                           "tunnelName" : tunnelName,
                           }
        self.accept("tunnelOutMovieDone", self.__tunnelOutMovieDone)
        base.localAvatar.tunnelOut(tunnelOrigin)

    def __tunnelOutMovieDone(self):
        self.ignore("tunnelOutMovieDone")
        messenger.send(self.doneEvent)

    def exitTunnelOut(self):
        assert(self.notify.debug("exitTunnelOut()"))

    # teleport states

    def enterTeleportOut(self, requestStatus, callback):
        assert(self.notify.debug("enterTeleportOut()"))
        base.localAvatar.laffMeter.start()
        base.localAvatar.b_setAnimState('TeleportOut', 1,
                callback, [requestStatus])
        base.localAvatar.obscureMoveFurnitureButton(1)

    def exitTeleportOut(self):
        assert(self.notify.debug("exitTeleportOut()"))
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)
        # It is a bad idea to broadcast these messages; first, it
        # shouldn't be necessary (since the server will send a disable
        # message to anyone around anyway); and second, it is possible
        # to get interrupted from the teleportOut state and not
        # complete the teleport operation, so that we still remain in
        # the same zone.
        #base.localAvatar.b_setParent(ToontownGlobals.SPHidden)
        #base.localAvatar.b_setAnimState('neutral', 1)

    def enterDied(self, requestStatus, callback = None):
        assert(self.notify.debug("enterDied()"))
        if callback == None:
            callback = self.__diedDone
        base.localAvatar.laffMeter.start()
        # Make sure the camera isn't attached to the toon when we
        # start to play the scale animation.
        camera.wrtReparentTo(render)
        base.localAvatar.b_setAnimState('Died', 1,
                                        callback, [requestStatus])
        base.localAvatar.obscureMoveFurnitureButton(1)

    def __diedDone(self, requestStatus):
        self.doneStatus = requestStatus
        messenger.send(self.doneEvent)

    def exitDied(self):
        assert(self.notify.debug("exitDied()"))
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)

    # for going home
    def getEstateZoneAndGoHome(self, requestStatus):
        self.doneStatus = requestStatus

        # owner of the estate we are teleporting to
        avId = requestStatus["avId"]

        self.acceptOnce("setLocalEstateZone", self.goHome)
        if avId > 0:
            # we are teleporting to another toons estate
            base.cr.estateMgr.getLocalEstateZone(avId)
        else:
            # we are teleporting to our own estate
            base.cr.estateMgr.getLocalEstateZone(base.localAvatar.getDoId())

        # set a timeout just in case we never hear back
        # SDN:  this doesn't work correctly yet.  getEstateZone
        # in EstateManagerAI will try and allocate us a new zone,
        # and if it is successful, it will delete the objects in
        # our current zone.  it does not wait to hear back from the
        # client if it got it's setEstateZone message before deleting
        # the objects.  It is not
        # clear that waiting for a response from the client is any
        # better than just assuming that the client got the message..

        # ..thus, for now, just config this off
        if HouseGlobals.WANT_TELEPORT_TIMEOUT:
            taskMgr.doMethodLater(HouseGlobals.TELEPORT_TIMEOUT,
                                  self.goHomeFailed,
                                  "goHomeFailed")
            
    def goHome(self, ownerId, zoneId):
        self.notify.debug("goHome ownerId = %s" % ownerId)
        taskMgr.remove("goHomeFailed")

        # Disallow transitive visits, i.e. teleporting to a friend who is
        # currently at a non-friends estate

        if (ownerId > 0 and ownerId != base.localAvatar.doId and
            not base.cr.isFriend(ownerId)):
            self.doneStatus["failed"] = 1
            self.goHomeFailed(None)
            return

        if (ownerId == 0 and zoneId == 0):
            if ((self.doneStatus['shardId'] is None) or
                (self.doneStatus['shardId'] is base.localAvatar.defaultShard)):
                # we are staying on the same shard... but the toon we are teleporting
                # to is no longer there!
                self.doneStatus["failed"] = 1
                self.goHomeFailed(None)
                return
            else:
                # If we are switching shards the AI will not be able to give us
                # the ownerId and zoneId of the estate owner.  We'll just go ahead and
                # switch shards and let the user click "go to" again
                # SDN:  actually this is no longer true.  We switch shards before the goHome
                # function is called, so the new AI will be able to tell us the ownerId and zoneId
                # This chunk of code is just a failsafe then..and may not be needed.

                # This was changed from 'hood'/'zone' to 'hoodId'/'zoneId' by
                # Pappy, and it caused a crash when teleporting to an estate
                # on a different shard.
                self.doneStatus["hood"] =  ToontownGlobals.MyEstate
                self.doneStatus["zone"] =  base.localAvatar.lastHood
                self.doneStatus["loaderId"] = "safeZoneLoader"
                #self.doneStatus["loaderId"] = "estateLoader"
                self.doneStatus["whereId"] = "estate"
                self.doneStatus["how"] = "teleportIn"

                messenger.send(self.doneEvent)
                return
        
        # If doneStatus["zoneId"]==-1 it means we got here from the
        # Go Home button in the shticker book.  We'll go to the zoneId
        # returned to us by the AI.  If doneStatus["zoneId"] != -1, it means
        # we are teleporting to someone at an estate.  Check if doneStatus["zoneId"]
        # is the same as the zoneId returned by the AI.  If it is, teleport to the estate;
        # if not, teleport to a house on the estate.
        if self.doneStatus["zoneId"] == -1:
            self.doneStatus["zoneId"] = zoneId
        elif self.doneStatus["zoneId"] != zoneId:
            # we are teleporting to a house
            self.doneStatus["where"] = "house"

        # for certain functions, we need to know who is the owner of the estate
        self.doneStatus["ownerId"] = ownerId
        messenger.send(self.doneEvent)

        # if we are leaving a suit building, the AI will need to know
        messenger.send("localToonLeft")
        
    def goHomeFailed(self, task):
        self.notify.debug("goHomeFailed")
        # it took too long to hear back from the server,
        # or we tried going to a non-friends house
        self.notifyUserGoHomeFailed()
        #  ignore the setLocalEstateZone message
        self.ignore("setLocalEstateZone")
        # This was changed from 'hood'/'zone' to 'hoodId'/'zoneId' by
        # Pappy, and it caused a crash when teleporting to an estate
        # on a different shard.
        self.doneStatus["hood"] =  base.localAvatar.lastHood
        self.doneStatus["zone"] =  base.localAvatar.lastHood

        self.fsm.request('teleportIn', [self.doneStatus])
        return Task.done

    def notifyUserGoHomeFailed(self):
        self.notify.debug("notifyUserGoHomeFailed")
        failedToVisitAvId = self.doneStatus.get("avId", -1)
        avName = None
        if failedToVisitAvId != -1:
            avatar = base.cr.identifyAvatar(failedToVisitAvId)
            if avatar:
                avName = avatar.getName()

        if avName:
            message = TTLocalizer.EstateTeleportFailedNotFriends % avName
        else:
            message = TTLocalizer.EstateTeleportFailed
        base.localAvatar.setSystemMessage(0, message)
        

    def enterTeleportIn(self, requestStatus):
        assert(self.notify.debug("enterTeleportIn()"))

        # Turn off the little red arrows while we teleport in.
        NametagGlobals.setMasterArrowsOn(0)
        base.localAvatar.laffMeter.start()
        base.localAvatar.reconsiderCheesyEffect()
        base.localAvatar.obscureMoveFurnitureButton(1)

        avId = requestStatus.get("avId", -1)
        if avId != -1:
            if base.cr.doId2do.has_key(avId):
                # Teleport to avatar
                avatar = base.cr.doId2do[avId]
                avatar.forceToTruePosition()
                base.localAvatar.gotoNode(avatar)
                base.localAvatar.b_teleportGreeting(avId)
            else:
                # The avatar isn't here!
                friend = base.cr.identifyAvatar(avId)
                if friend != None:
                    base.localAvatar.setSystemMessage(
                        avId,
                        OTPLocalizer.WhisperTargetLeftVisit % (friend.getName(),))
                    friend.d_teleportGiveup(base.localAvatar.doId)
            
        base.transitions.irisIn()
        # We might be going to "popup" state if it's a newbie
        self.nextState = requestStatus.get('nextState', 'walk')

        # Start the smart camera, to put it in the right place, but be
        # prepared to stop it again in exitTeleportIn.
        base.localAvatar.attachCamera()
        base.localAvatar.startUpdateSmartCamera()

        # Similarly with the posHprBroacast task.
        base.localAvatar.startPosHprBroadcast()

        # We'll cheat here, and tick the clock by hand.  This pretends
        # this is the beginning of the frame, and will sync up the
        # frame time with the real time to compensate for any long
        # frame we may have suffered while loading up this scene.
        # This way, the teleport-in animation will be played in its
        # entirety.
        globalClock.tick()
        base.localAvatar.b_setAnimState('TeleportIn', 1, 
                                          callback=self.teleportInDone)
        base.localAvatar.d_broadcastPositionNow()
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)
        #import pdb; pdb.set_trace()

    def teleportInDone(self):
        """
        Note: DDPlayground overrides this to go to swimming if it needs to.
        """
        assert(self.notify.debug("teleportInDone()"))
        # This will either go to "walk" or "popup"
        if hasattr(self, 'fsm'):
            self.fsm.request(self.nextState, [1])
        
    def exitTeleportIn(self):
        assert(self.notify.debug("exitTeleportIn()"))
        # Turn on the little red arrows now that we're done teleporting.
        NametagGlobals.setMasterArrowsOn(1)
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)

        # Stop the tasks which we started above.
        base.localAvatar.stopUpdateSmartCamera()
        base.localAvatar.detachCamera()
        base.localAvatar.stopPosHprBroadcast()


    def requestTeleport(self, hoodId, zoneId, shardId, avId):
        # The local avatar cannot leave the zone if he is part of a boarding group.
        if localAvatar.hasActiveBoardingGroup():
            rejectText = TTLocalizer.BoardingCannotLeaveZone
            localAvatar.elevatorNotifier.showMe(rejectText)
            return
        loaderId = ZoneUtil.getBranchLoaderName(zoneId)
        whereId = ZoneUtil.getToonWhereName(zoneId)
        if hoodId == ToontownGlobals.MyEstate:
            #loaderId = "estateLoader"
            loaderId = "safeZoneLoader"
            whereId = "estate"
        # If we're teleporting directly to a friend at a party, we need to
        # specify that here.
        if hoodId == ToontownGlobals.PartyHood:
            loaderId = "safeZoneLoader"
            whereId = "party"

        self.requestLeave({
            "loader": loaderId,
            "where": whereId,
            "how" : "teleportIn",
            "hoodId" : hoodId, 
            "zoneId" : zoneId, 
            "shardId" : shardId,
            "avId" : avId})

    def enterQuest(self, npcToon):
        base.localAvatar.b_setAnimState('neutral', 1)
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.laffMeter.start()
        base.localAvatar.obscureMoveFurnitureButton(1)
        
    def exitQuest(self):
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)

    def enterPurchase(self):
        base.localAvatar.b_setAnimState('neutral', 1)
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.laffMeter.start()
        base.localAvatar.obscureMoveFurnitureButton(1)
        
    def exitPurchase(self):
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)

    def enterFishing(self):
        base.localAvatar.b_setAnimState('neutral', 1)
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.laffMeter.start()

    def exitFishing(self):
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()

    def enterBanking(self):
        base.localAvatar.b_setAnimState('neutral', 1)
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.laffMeter.start()
        base.localAvatar.obscureMoveFurnitureButton(1)
        # Spawn the task that checks to see if toon has fallen asleep
        base.localAvatar.startSleepWatch(self.__handleFallingAsleepBanking)
        self.enablePeriodTimer()        

    def __handleFallingAsleepBanking(self, arg):
        if hasattr(self, "fsm"):
            # the place has been unloaded... ignore this request
            messenger.send('bankAsleep')
            self.fsm.request("walk")
        base.localAvatar.forceGotoSleep()
        
    def exitBanking(self):
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)
        base.localAvatar.stopSleepWatch()
        self.disablePeriodTimer()

    def enterPhone(self):
        base.localAvatar.b_setAnimState('neutral', 1)
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        base.localAvatar.laffMeter.start()
        base.localAvatar.obscureMoveFurnitureButton(1)
        # Spawn the task that checks to see if toon has fallen asleep
        base.localAvatar.startSleepWatch(self.__handleFallingAsleepPhone)
        self.enablePeriodTimer()        

    def __handleFallingAsleepPhone(self, arg):
        if hasattr(self, "fsm"):
            #the place has been unloaded... ignore this request
            self.fsm.request("walk")
        messenger.send('phoneAsleep')
        base.localAvatar.forceGotoSleep()
        
    def exitPhone(self):
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)
        base.localAvatar.stopSleepWatch()
        self.disablePeriodTimer()

    def enterStopped(self):
        base.localAvatar.b_setAnimState('neutral', 1)
        # disable emotes
        Emote.globalEmote.disableBody(base.localAvatar, "enterStopped")
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        
        if base.localAvatar.isDisguised:
            base.localAvatar.setTeleportAvailable(0)
        else:
            base.localAvatar.setTeleportAvailable(1)
        
        base.localAvatar.laffMeter.start()
        base.localAvatar.obscureMoveFurnitureButton(1)
        # Spawn the task that checks to see if toon has fallen asleep
        base.localAvatar.startSleepWatch(self.__handleFallingAsleepStopped)
        self.enablePeriodTimer()        

    def __handleFallingAsleepStopped(self, arg):
        if hasattr(self, "fsm"):
            #the place has been unloaded... ignore this request
            self.fsm.request("walk")
        base.localAvatar.forceGotoSleep()
        # throw an event to alert any GUIs that may be up that the toon is asleep
        messenger.send("stoppedAsleep")
 
    def exitStopped(self):
        # enable emotes
        Emote.globalEmote.releaseBody(base.localAvatar, "exitStopped")
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()
        base.localAvatar.obscureMoveFurnitureButton(-1)
        base.localAvatar.stopSleepWatch()
        self.disablePeriodTimer()
        messenger.send("exitingStoppedState")

    def enterPet(self):
        base.localAvatar.b_setAnimState('neutral', 1)
        # disable emotes
        Emote.globalEmote.disableBody(base.localAvatar, "enterPet")
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        # but we cannot teleport to other people
        base.localAvatar.setTeleportAllowed(0)
        base.localAvatar.laffMeter.start()
        # The friends list is available here.
        self.enterFLM()
        
    def exitPet(self):
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(0)
        base.localAvatar.setTeleportAllowed(1)
        # enable emotes
        Emote.globalEmote.releaseBody(base.localAvatar, "exitPet")
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()
        # The friends list is no longer available.
        self.exitFLM()

    # quietZone state

    def enterQuietZone(self, requestStatus):
        assert(self.notify.debug("enterQuietZone()"))
        self.quietZoneDoneEvent = "quietZoneDone"
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(
                self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)

    def exitQuietZone(self):
        assert(self.notify.debug("exitQuietZone()"))
        self.ignore(self.quietZoneDoneEvent)
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData=None

    def handleQuietZoneDone(self):
        assert(self.notify.debug("handleQuietZoneDone()"))
        # Change to the destination state:
        how = base.cr.handlerArgs["how"]
        assert(how=="teleportIn")# Please tell skyler if this assert fails.
        self.fsm.request(how, [base.cr.handlerArgs])
