from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from direct.distributed.ClockDelta import *
from toontown.hood import Place
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
import random
from direct.showbase import PythonUtil
from toontown.hood import Place
from toontown.hood import SkyUtil
from toontown.pets import PetTutorial
from direct.controls.GravityWalker import GravityWalker
import HouseGlobals

class Estate(Place.Place):
    notify = DirectNotifyGlobal.directNotify.newCategory("Estate")

    def __init__(self, loader, avId, zoneId, parentFSMState, doneEvent):
        Place.Place.__init__(self, None, doneEvent)

        self.id = MyEstate
        self.avId = avId
        self.zoneId = zoneId
        self.loader = loader

        # Underwater stuff
        self.cameraSubmerged = -1
        self.toonSubmerged = -1

        self.fsm = ClassicFSM.ClassicFSM(
            'Estate',
            [State.State('init',
                         self.enterInit,
                         self.exitInit,
                         ['final', 'teleportIn', 'doorIn', 'walk']),
             State.State('petTutorial',
                         self.enterPetTutorial,
                         self.exitPetTutorial,
                         ['walk',]),
             State.State('walk',
                         self.enterWalk,
                         self.exitWalk,
                         ['final', 'sit', 'stickerBook',
                          'options', 'quest', 'fishing',
                          'mailbox', 'stopped', 'DFA', 'trialerFA',
                          'doorOut', 'push', 'pet',
                          ]),
            State.State('stopped',
                        self.enterStopped,
                        self.exitStopped,
                        ['walk', 'teleportOut',
                         ]),
             State.State('sit',
                         self.enterSit,
                         self.exitSit,
                         ['walk',]),
             State.State('push',
                         self.enterPush,
                         self.exitPush,
                         ['walk',]),
             State.State('stickerBook',
                         self.enterStickerBook,
                         self.exitStickerBook,
                         ['walk', 'sit',
                          'quest', 'fishing',
                          'mailbox', 'stopped',
                          'doorOut', 'push', 'pet',
                          'DFA', 'trialerFA',
                          ]),
             State.State('teleportIn',
                         self.enterTeleportIn,
                         self.exitTeleportIn,
                         ['walk', 'petTutorial']),
             State.State('teleportOut',
                         self.enterTeleportOut,
                         self.exitTeleportOut,
                         ['teleportIn', 'walk', 'final']), # 'final'
             State.State('doorIn',
                         self.enterDoorIn,
                         self.exitDoorIn,
                         ['walk']),
             State.State('doorOut',
                         self.enterDoorOut,
                         self.exitDoorOut,
                         ['final', 'walk']),
             State.State('final',
                         self.enterFinal,
                         self.exitFinal,
                         ['teleportIn']),
             State.State('quest',
                         self.enterQuest,
                         self.exitQuest,
                         ['walk']),
             State.State('fishing',
                         self.enterFishing,
                         self.exitFishing,
                         ['walk', 'stopped']),
             State.State('mailbox',
                         self.enterMailbox,
                         self.exitMailbox,
                         ['walk','stopped']),
             State.State('stopped',
                         self.enterStopped,
                         self.exitStopped,
                         ['walk']),
             State.State('pet',
                         self.enterPet,
                         self.exitPet,
                         ['walk', 'trialerFA']),
             # Trialer Force Acknowledge:
             State.State('trialerFA',
                         self.enterTrialerFA,
                         self.exitTrialerFA,
                         ['trialerFAReject', 'DFA']),
             State.State('trialerFAReject',
                         self.enterTrialerFAReject,
                         self.exitTrialerFAReject,
                         ['walk']),
             # Download Force Acknowledge
             State.State('DFA',
                         self.enterDFA,
                         self.exitDFA,
                         ['DFAReject',
                          'teleportOut']),
             State.State('DFAReject',
                         self.enterDFAReject,
                         self.exitDFAReject,
                         ['walk']),
             ],
            # Initial state
            'init',
            # Final state
            'final',
            )

        self.fsm.enterInitialState()
        self.doneEvent = doneEvent
        self.parentFSMState = parentFSMState


    def delete(self):
        assert(self.notify.debug("delete()"))
        self.unload()

    def load(self):
        assert(self.notify.debug("load()"))
        # Call up the chain
        Place.Place.load(self)

        # water stuff (copied from DD code)
        self.fog = Fog("EstateFog")
        taskMgr.add(self.__checkCameraUnderwater,
                    'estate-check-cam-underwater')

        # make the foot path render properly wrt the ground polys
        path = self.loader.geom.find("**/Path")
        path.setBin("ground", 10, 1)

        self.parentFSMState.addChild(self.fsm)

    def unload(self):
        assert(self.notify.debug("unload()"))
        self.ignoreAll()        
        self.notify.info("remove estate-check-toon-underwater to TaskMgr in unload()")
        taskMgr.remove('estate-check-toon-underwater')
        taskMgr.remove('estate-check-cam-underwater')
        self.parentFSMState.removeChild(self.fsm)
        del self.fsm        
        self.fog = None        
        Place.Place.unload(self)        

    def enter(self, requestStatus):
        """
        enter this estate and start the state machine
        """
        assert(self.notify.debug("enter(requestStatus="+str(requestStatus)+")"))
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]

        # start the sky
        newsManager = base.cr.newsManager

        if newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            if (ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds) and self.loader.hood.spookySkyFile:

                lightsOff = Sequence(LerpColorScaleInterval(
                    base.cr.playGame.hood.loader.geom,
                    0.1,
                    Vec4(0.55, 0.55, 0.65, 1)),
                    Func(self.loader.hood.startSpookySky),
                    )

                lightsOff.start()
            else:
                # Turn the sky on
                self.loader.hood.startSky()
                lightsOn = LerpColorScaleInterval(
                    base.cr.playGame.hood.loader.geom,
                    0.1,
                    Vec4(1, 1, 1, 1))
                lightsOn.start()
        else:
            # Turn the sky on
            self.loader.hood.startSky()
            lightsOn = LerpColorScaleInterval(
                base.cr.playGame.hood.loader.geom,
                0.1,
                Vec4(1, 1, 1, 1))
            lightsOn.start()

        self.loader.hood.sky.setFogOff()
        self.__setFaintFog()
        # Turn on the animated props for the estate
        for i in self.loader.nodeList:
            self.loader.enterAnimatedProps(i)
        self.loader.geom.reparentTo(render)

        # April toons
        if hasattr(base.cr, "newsManager") and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds:
                self.startAprilFoolsControls()

        # leaving or entering the estate via door (i.e. a house door)
        self.accept("doorDoneEvent", self.handleDoorDoneEvent)
        self.accept("DistributedDoor_doorTrigger", self.handleDoorTrigger)
        self.fsm.request(requestStatus["how"], [requestStatus])

    def startAprilFoolsControls(self):
        if isinstance(base.localAvatar.controlManager.currentControls, GravityWalker):
            base.localAvatar.controlManager.currentControls.setGravity(32.174*0.75)

    def stopAprilFoolsControls(self):
        if isinstance(base.localAvatar.controlManager.currentControls, GravityWalker):
            base.localAvatar.controlManager.currentControls.setGravity(32.174*2.0)

    def exit(self):
        assert(self.notify.debug("exit"))
        base.localAvatar.stopChat()

        if hasattr(base.cr, "newsManager") and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds:
                self.stopAprilFoolsControls()

        # Make sure our ClassicFSM goes into its final state
        # so the walkStateData cleans up its tasks
        if (hasattr(self, 'fsm')):
            self.fsm.requestFinalState()

        # hide the estate terrain
        self.loader.geom.reparentTo(hidden)

        # Turn off the animated props once since there is only one zone
        for i in self.loader.nodeList:
            self.loader.exitAnimatedProps(i)

        # Turn the sky off
        self.loader.hood.stopSky()

        render.setFogOff()
        base.cr.cache.flush()

    def __setZoneId(self, zoneId):
        #print "setting our local zone ID from %d to %d" % (self.zoneId, zoneId)
        self.zoneId = zoneId

    def detectedMailboxCollision(self):
        assert(self.notify.debug("detectedMailboxCollision"))
        self.fsm.request('mailbox')

    def detectedGardenPlotUse(self):
        assert(self.notify.debug("detectedGardenPlotCollision"))
        # protect against estate owning toon leaving
        if hasattr(self, 'fsm'):
            self.fsm.request('stopped')

    def detectedGardenPlotDone(self):
        assert(self.notify.debug("detectedGardenPlotDone"))
        # protect against estate owning toon leaving
        if hasattr(self, 'fsm'):
            self.fsm.request('walk')

    def detectedFlowerSellUse(self):
        assert(self.notify.debug("detectedFlowerSellUse"))
        # protect against estate owning toon leaving
        if hasattr(self, 'fsm'):
            self.fsm.request('stopped')

    def detectedFlowerSellDone(self):
        assert(self.notify.debug("detectedFlowerSellDone"))
        # protect against estate owning toon leaving
        if hasattr(self, 'fsm'):
            self.fsm.request('walk')

    def doRequestLeave(self, requestStatus):
        # when it's time to leave, check their trialer status first
        self.fsm.request('trialerFA', [requestStatus])

    def enterInit(self):
        pass

    def exitInit(self):
        pass

    def enterPetTutorial(self, bDummy = True):
        self.notify.info("remove estate-check-toon-underwater to TaskMgr in enterPetTutorial()")
        taskMgr.remove('estate-check-toon-underwater')
        self.petTutorialDoneEvent = "PetTutorialDone"
        self.acceptOnce(self.petTutorialDoneEvent, self.petTutorialDone)
        self.petTutorial = PetTutorial.PetTutorial(self.petTutorialDoneEvent)
        pass

    def exitPetTutorial(self):
        self.notify.info("add estate-check-toon-underwater to TaskMgr in exitPetTutorial()")

        if hasattr(self, 'fsm'):
            taskMgr.add(self.__checkToonUnderwater, 'estate-check-toon-underwater')

        if hasattr(self, "petTutorial") and (self.petTutorial is not None):
            self.petTutorial.destroy()

    def petTutorialDone(self):
        self.ignore(self.petTutorialDoneEvent)
        self.petTutorial.destroy()
        self.petTutorial = None
        self.fsm.request('walk', [1])

    def enterMailbox(self):
        # this state just locks the toon down so he can't move
        Place.Place.enterPurchase(self)
        # Spawn the task that checks to see if toon has fallen asleep
        base.localAvatar.startSleepWatch(self.__handleFallingAsleepMailbox)
        self.enablePeriodTimer()

    def __handleFallingAsleepMailbox(self, arg):
        if hasattr(self, "fsm"):
            #the place has been unloaded... ignore this request
            self.fsm.request("walk")
        # this message will make sure the item picking GUI goes away
        messenger.send("mailboxAsleep")
        base.localAvatar.forceGotoSleep()

    def exitMailbox(self):
        Place.Place.exitPurchase(self)
        base.localAvatar.stopSleepWatch()
        self.disablePeriodTimer()

    def enterTeleportIn(self, requestStatus):
        assert(self.notify.debug("enterTeleportIn()"))
        try:
            # if we have a house assigned to us, teleport in front of it
            houseDo = base.cr.doId2do.get(base.localAvatar.houseId)
            house = houseDo.house
            pos = house.getPos(render)
            base.localAvatar.detachNode()
            base.localAvatar.setPosHpr(house, 17, 3, 0, 125, 0, 0)
        except:
            # do this if we don't have a house assigned
            # or if for some reason our house object isn't created
            x,y,z,h,p,r = HouseGlobals.defaultEntryPoint
            base.localAvatar.detachNode()
            base.localAvatar.setPosHpr(render, x,y,z,h,p,r)
        base.localAvatar.setScale(1,1,1)
        self.toonSubmerged = -1
        self.notify.info("remove estate-check-toon-underwater to TaskMgr in enterTeleportIn()")
        taskMgr.remove('estate-check-toon-underwater')
        Place.Place.enterTeleportIn(self, requestStatus)

        if base.wantPets:
            #show the petTutorial
            if base.localAvatar.hasPet() and (not base.localAvatar.bPetTutorialDone):
                self.nextState = 'petTutorial'

    def teleportInDone(self):
        """
        Override Place.py teleportInDone to check if we are cameraSubmerged.
        If we are cameraSubmerged, we should swim instead of walk
        """
        self.notify.debug("teleportInDone")
        self.toonSubmerged = -1
        if self.nextState is not 'petTutorial':
            self.notify.info("add estate-check-toon-underwater to TaskMgr in teleportInDone()")
            if hasattr(self, 'fsm'):
                taskMgr.add(self.__checkToonUnderwater, 'estate-check-toon-underwater')
        Place.Place.teleportInDone(self)

    def enterTeleportOut(self, requestStatus):
        assert(self.notify.debug("enterTeleportOut()"))
        Place.Place.enterTeleportOut(self, requestStatus,
                self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        assert(self.notify.debug("__teleportOutDone()"))
        # If we're teleporting from a safezone, we need to set the
        # fsm to the final state
        if (hasattr(self, 'fsm')):
            self.fsm.requestFinalState()
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        avId = requestStatus["avId"]
        shardId = requestStatus["shardId"]
        if ((hoodId == ToontownGlobals.MyEstate) and
            (zoneId == self.getZoneId()) and
            shardId == None):
            # we are going to someone in the same estate
            self.fsm.request("teleportIn", [requestStatus])
        elif (hoodId == ToontownGlobals.MyEstate and shardId == None):
            # we are going to a different estate
            self.doneStatus = requestStatus
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            # Different hood, zone or shard, exit the safe zone
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent, [self.doneStatus])

    def goHomeFailed(self, task):
        # it took to long to hear back from the server,
        # or we tried going to a non-friends house
        self.notifyUserGoHomeFailed()
        #  ignore the setLocalEstateZone message
        self.ignore("setLocalEstateZone")
        self.doneStatus["avId"] =  -1
        self.doneStatus["zoneId"] =  self.getZoneId()
        self.fsm.request("teleportIn", [self.doneStatus])
        return Task.done

    def exitTeleportOut(self):
        assert(self.notify.debug("exitTeleportOut()"))
        Place.Place.exitTeleportOut(self)

    def exitDoorIn(self):
        self.toonSubmerged = -1
        self.notify.info("add estate-check-toon-underwater to TaskMgr in exitDoorIn()")
        if hasattr(self, 'fsm'):
            taskMgr.add(self.__checkToonUnderwater, 'estate-check-toon-underwater')
        Place.Place.exitDoorIn(self)

    def getZoneId(self):
        """
        Returns the current zone ID.  This is either the same as the
        hoodID for a Playground class, or the current zoneId for a Town
        class.
        """
        #self.zoneId
        if self.zoneId:
            return self.zoneId
        else:
            self.notify.warning("no zone id available")

    def __checkCameraUnderwater(self, task):
        # We need to take into account the height of the local toon
        # if (base.localAvatar.getZ() < -2.3314585):
        # It is more accurate to use the camera because it can
        # move independently of the toon
        if (camera.getZ(render) < -1.2):
            self.__submergeCamera()
        else:
            self.__emergeCamera()
        return Task.cont

    def __checkToonUnderwater(self, task):
        # We need to take into account the height of the local toon
        # if (base.localAvatar.getZ() < -2.3314585):
        if (base.localAvatar.getZ() < -4.0):
            self.__submergeToon()
        else:
            self.__emergeToon()
        return Task.cont

    def __submergeCamera(self):
        if (self.cameraSubmerged == 1):
            return
        self.__setUnderwaterFog()
        base.playSfx(self.loader.underwaterSound, looping = 1, volume = 0.8)
        self.cameraSubmerged = 1
        self.walkStateData.setSwimSoundAudible(1)

    def __emergeCamera(self):
        if (self.cameraSubmerged == 0):
            return
        self.loader.underwaterSound.stop()
        self.loader.hood.sky.setFogOff()
        #render.setFogOff()
        self.__setFaintFog()
        #self.__setWhiteFog()
        self.cameraSubmerged = 0
        self.walkStateData.setSwimSoundAudible(0)

    def forceUnderWater(self):
        self.toonSubmerged = 0
        self.__submergeToon()

    def __submergeToon(self):
        if (self.toonSubmerged == 1):
            #pos = base.localAvatar.getPos(render)
            #base.localAvatar.setPos(pos[0]-.5, pos[1]+.5, pos[2])
            return
        self.notify.debug('continuing in __submergeToon')        
        if hasattr(self, 'loader') and self.loader:
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
        base.localAvatar.d_playSplashEffect(pos[0], pos[1], -2.3)
        #base.localAvatar.stopSmooth()
        self.toonSubmerged = 1

    def __emergeToon(self):
        if (self.toonSubmerged == 0):
            return
        self.notify.debug('continuing in __emergeToon')
        #base.localAvatar.startSmooth()
        if hasattr(self, "walkStateData"):
            self.walkStateData.fsm.request('walking')
        self.toonSubmerged = 0

        if hasattr(base.cr, "newsManager") and base.cr.newsManager:
            holidayIds = base.cr.newsManager.getHolidayIdList()
            if ToontownGlobals.APRIL_FOOLS_COSTUMES in holidayIds:
                self.startAprilFoolsControls()
            else:
                self.stopAprilFoolsControls()

    def __setUnderwaterFog(self):
        if base.wantFog:
            self.fog.setColor(Vec4(0.0, 0.0, 0.6, 1.0))
            self.fog.setLinearRange(0.1, 100.0)
            render.setFog(self.fog)
            self.loader.hood.sky.setFog(self.fog)

    def __setWhiteFog(self):
        if base.wantFog:
            self.fog.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
            self.fog.setLinearRange(0.0, 400.0)
            render.setFog(self.fog)
            # Insist that fog is on the sky.  This will prevent the
            # sky from being contaminated by the trolley tunnel shadow
            # if we jump on the trolley.
            self.loader.hood.sky.setFog(self.fog)

    def __setFaintFog(self):
        if base.wantFog:
            self.fog.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
            self.fog.setLinearRange(0.0, 700.0)
            render.setFog(self.fog)
            # don't set the sky fog, it looks depressing
            #self.loader.hood.sky.setFog(self.fog)

