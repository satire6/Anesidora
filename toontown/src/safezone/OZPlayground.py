from pandac.PandaModules import *

from toontown.toonbase import ToontownGlobals
import Playground
from toontown.launcher import DownloadForceAcknowledge
from toontown.building import Elevator
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from toontown.racing import RaceGlobals
from direct.fsm import State
#from toontown.trolley import Trolley
from toontown.safezone import PicnicBasket
from toontown.safezone import GolfKart
from direct.task.Task import Task

class OZPlayground(Playground.Playground):

    waterLevel = -0.53
    
    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM=parentFSM
        self.picnicBasketBlockDoneEvent = "picnicBasketBlockDone"
        self.cameraSubmerged = -1
        self.toonSubmerged = -1
        self.fsm.addState( State.State('picnicBasketBlock',
                                       self.enterPicnicBasketBlock,
                                       self.exitPicnicBasketBlock,
                                       ['walk']))
        state = self.fsm.getStateNamed('walk')
        state.addTransition('picnicBasketBlock')

        self.picnicBasketDoneEvent = "picnicBasketDone"        

    def load(self):
        Playground.Playground.load(self)
    
    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)
        
    def exit(self):
        Playground.Playground.exit(self)
        taskMgr.remove('oz-check-toon-underwater')
        taskMgr.remove('oz-check-cam-underwater')        
        #self.rotateBlimp.finish()
        # Clean up underwater state
        self.loader.hood.setNoFog()

    def doRequestLeave(self, requestStatus):
        # when it's time to leave, check their trialer status first
        self.fsm.request('trialerFA', [requestStatus])

    def enterDFA(self, requestStatus):
        """
        Override the base class because here we specifically ask for
        phase 5, the toontown central streets.
        - NEW: we can now go home.  Check the hood before assuming we
        are going to the streets
        """
        doneEvent = "dfaDoneEvent"
        self.accept(doneEvent, self.enterDFACallback, [requestStatus])
        self.dfa = DownloadForceAcknowledge.DownloadForceAcknowledge(doneEvent)
        if requestStatus["hoodId"] == ToontownGlobals.MyEstate:
            # Ask if we can enter phase 5.5
            self.dfa.enter(base.cr.hoodMgr.getPhaseFromHood(ToontownGlobals.MyEstate))
        else:
            # Ask if we can enter phase 5
            self.dfa.enter(5)

    def enterStart(self):
        assert self.notify.debugStateCall(self)
        self.cameraSubmerged = 0
        self.toonSubmerged = 0
        taskMgr.add(self.__checkToonUnderwater,
                    'oz-check-toon-underwater')
        taskMgr.add(self.__checkCameraUnderwater,
                    'oz-check-cam-underwater')        

    def __checkCameraUnderwater(self, task):
        # spammy: assert self.notify.debugStateCall(self)
        # We need to take into account the height of the local toon
        # if (base.localAvatar.getZ() < -2.3314585):
        # It is more accurate to use the camera because it can
        # move independently of the toon
        if (camera.getZ(render) < self.waterLevel):
            self.__submergeCamera()
        else:
            self.__emergeCamera()
        return Task.cont

    def __checkToonUnderwater(self, task):
        # spammy: assert self.notify.debugStateCall(self)
        # We need to take into account the height of the local toon
        if (base.localAvatar.getZ() < -4.0):
            self.__submergeToon()
        else:
            self.__emergeToon()
        return Task.cont

    def __submergeCamera(self):
        if (self.cameraSubmerged == 1):
            return
        assert self.notify.debugStateCall(self)
        self.loader.hood.setUnderwaterFog()
        base.playSfx(self.loader.underwaterSound, looping = 1, volume = 0.8)
        #self.loader.seagullSound.stop()
        #taskMgr.remove('dd-seagulls')
        self.cameraSubmerged = 1
        self.walkStateData.setSwimSoundAudible(1)

    def __emergeCamera(self):
        if (self.cameraSubmerged == 0):
            return
        assert self.notify.debugStateCall(self)
        #self.loader.hood.setWhiteFog()
        self.loader.hood.setNoFog()
        self.loader.underwaterSound.stop()
        #self.nextSeagullTime = random.random() * 8.0
        #taskMgr.add(self.__seagulls, 'dd-seagulls')
        self.cameraSubmerged = 0
        self.walkStateData.setSwimSoundAudible(0)

    def __submergeToon(self):
        if (self.toonSubmerged == 1):
            return
        assert self.notify.debugStateCall(self)
        base.playSfx(self.loader.submergeSound)  # plays a splash sound
        # Make sure you are in walk mode This fixes a bug where you could
        # open your stickerbook over the water and get stuck in swim mode
        # becuase the Place was still in StickerBook state.
        if base.config.GetBool('disable-flying-glitch') == 0:
            self.fsm.request('walk')
        # You have to pass in the swim sound effect to swim mode.
        self.walkStateData.fsm.request('swimming', [self.loader.swimSound])
        # Let everyone else see your splash
        pos = base.localAvatar.getPos(render)
        # our water level is different from donald's dock
        base.localAvatar.d_playSplashEffect(pos[0], pos[1], self.waterLevel)
        self.toonSubmerged = 1

    def __emergeToon(self):
        if (self.toonSubmerged == 0):
            return
        assert self.notify.debugStateCall(self)
        self.walkStateData.fsm.request('walking')
        self.toonSubmerged = 0

    
    # teleportIn
    def enterTeleportIn(self, requestStatus):
        reason = requestStatus.get("reason")
        if reason == RaceGlobals.Exit_Barrier:
            # we timed out of a race
            requestStatus['nextState'] = 'popup'
            self.dialog = TTDialog.TTDialog(
                text = TTLocalizer.KartRace_RaceTimeout,
                command = self.__cleanupDialog,
                style = TTDialog.Acknowledge)
        elif reason == RaceGlobals.Exit_Slow:
            # we timed out of a race
            requestStatus['nextState'] = 'popup'
            self.dialog = TTDialog.TTDialog(
                text = TTLocalizer.KartRace_RacerTooSlow,
                command = self.__cleanupDialog,
                style = TTDialog.Acknowledge)
        elif reason == RaceGlobals.Exit_BarrierNoRefund:
            # we timed out of a race
            requestStatus['nextState'] = 'popup'
            self.dialog = TTDialog.TTDialog(
                text = TTLocalizer.KartRace_RaceTimeoutNoRefund,
                command = self.__cleanupDialog,
                style = TTDialog.Acknowledge)
        self.toonSubmerged = -1
        taskMgr.remove('oz-check-toon-underwater')
        Playground.Playground.enterTeleportIn(self, requestStatus)

    def teleportInDone(self):
        """
        Override Place.py teleportInDone to check if we are cameraSubmerged.
        If we are cameraSubmerged, we should swim instead of walk
        """
        assert self.notify.debugStateCall(self)
        self.toonSubmerged = -1
        taskMgr.add(self.__checkToonUnderwater,
                    'oz-check-toon-underwater')
        Playground.Playground.teleportInDone(self)

    def __cleanupDialog(self, value):
        if (self.dialog):
            self.dialog.cleanup()
            self.dialog = None
        if hasattr(self, "fsm"):
            self.fsm.request('walk', [1])

    def enterPicnicBasketBlock(self, picnicBasket):
        assert(self.notify.debug("enterPicnicBasketBlock()"))
        # Turn on the laff meter
        base.localAvatar.laffMeter.start()

        # clear the anim state
        base.localAvatar.b_setAnimState("off", 1)

        # Disable leave to pay / set parent password (for consistency)
        base.localAvatar.cantLeaveGame = 1
        
        self.accept(self.picnicBasketDoneEvent, self.handlePicnicBasketDone)
        self.trolley = PicnicBasket.PicnicBasket(self, self.fsm, self.picnicBasketDoneEvent, picnicBasket.getDoId(), picnicBasket.seatNumber)
        self.trolley.load()
        self.trolley.enter()

    def exitPicnicBasketBlock(self):
        assert(self.notify.debug("exitPicnicBasketBlock()"))

        # Turn off the laff meter
        base.localAvatar.laffMeter.stop()        
        base.localAvatar.cantLeaveGame = 0
        
        self.ignore(self.trolleyDoneEvent)
        self.trolley.unload()
        self.trolley.exit()
        del self.trolley

    def detectedPicnicTableSphereCollision(self, picnicBasket):
        assert(self.notify.debug("detectedPicnicTableSphereCollision()"))
        self.fsm.request("picnicBasketBlock", [picnicBasket])

    def handleStartingBlockDone(self, doneStatus):
        assert(self.notify.debug("handleStartingBlockDone()"))
        self.notify.debug("handling StartingBlock done event")
        where = doneStatus['where']
        if (where == 'reject'):
            self.fsm.request("walk")
        elif (where == 'exit'):
            self.fsm.request("walk")
        elif (where == 'racetrack'):
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error("Unknown mode: " + where +
                              " in handleStartingBlockDone")


    def handlePicnicBasketDone(self, doneStatus):
        assert(self.notify.debug("handlePicnicBasketDone()"))
        self.notify.debug("handling picnic basket done event")
        mode = doneStatus["mode"]
        if mode == "reject":
            self.fsm.request("walk")
        elif mode == "exit":
            self.fsm.request("walk")
        #elif mode == "golfcourse":
        #    self.doneStatus = {"loader" : "golfcourse",
        #                       "where" : "golfcourse",
        #                       "hoodId" : self.loader.hood.id,
        #                       "zoneId" : doneStatus["zoneId"],
        #                       "shardId" : None,
        #                       "courseId" : doneStatus["courseId"]
        #                       }
        #    #self.doneStatus = doneStatus
        #    messenger.send(self.doneEvent)
        else:
            self.notify.error("Unknown mode: " + mode + " in handlePicnicBasketDone")

    def showPaths(self):
        # Overridden from Playground to fill in the correct parameters
        # for showPathPoints().
        from toontown.classicchars import CCharPaths
        from toontown.toonbase import TTLocalizer
        self.showPathPoints(CCharPaths.getPaths(TTLocalizer.Chip))
