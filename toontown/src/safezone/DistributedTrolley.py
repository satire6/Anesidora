from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from TrolleyConstants import *

from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.distributed import DelayDelete
from direct.task.Task import Task
from toontown.hood import ZoneUtil
from toontown.toontowngui import TeaserPanel


class DistributedTrolley(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedTrolley")
    
    def __init__(self, cr):
        """__init__(cr)
        """
        DistributedObject.DistributedObject.__init__(self, cr)

        self.localToonOnBoard = 0

        self.trolleyCountdownTime = \
                              base.config.GetFloat("trolley-countdown-time",
                                                   TROLLEY_COUNTDOWN_TIME)

        self.fsm = ClassicFSM.ClassicFSM('DistributedTrolley',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['entering',
                                         'waitEmpty',
                                         'waitCountdown',
                                         'leaving']),
                            State.State('entering',
                                        self.enterEntering,
                                        self.exitEntering,
                                        ['waitEmpty']),
                            State.State('waitEmpty',
                                        self.enterWaitEmpty,
                                        self.exitWaitEmpty,
                                        ['waitCountdown']),
                            State.State('waitCountdown',
                                        self.enterWaitCountdown,
                                        self.exitWaitCountdown,
                                        ['waitEmpty', 'leaving']),
                            State.State('leaving',
                                        self.enterLeaving,
                                        self.exitLeaving,
                                        ['entering'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )
        self.fsm.enterInitialState()

        self.trolleyAwaySfx = base.loadSfx("phase_4/audio/sfx/SZ_trolley_away.mp3")
        self.trolleyBellSfx = base.loadSfx("phase_4/audio/sfx/SZ_trolley_bell.mp3")

        # Tracks on toons, for starting and stopping
        # stored by avId : track. There is only a need for one at a time,
        # in fact the point of the dict is to ensure only one is playing at a time
        self.__toonTracks = {}

    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedObject.DistributedObject.generate(self)

        # Get the state machine stuff for playGame
        self.loader = self.cr.playGame.hood.loader
        self.trolleyStation = self.loader.geom.find('**/*trolley_station*')
        self.trolleyCar = self.trolleyStation.find('**/trolley_car')
        self.trolleySphereNode = self.trolleyStation.find('**/trolley_sphere').node()

        # We'll need a pair of fog objects to enshadow the trolley
        # while it's rolling through the entrance or exit tunnels.

        exitFog = Fog("TrolleyExitFog")
        exitFog.setColor(0.0, 0.0, 0.0)
        exitFog.setLinearOnsetPoint(30.0, 14.0, 0.0)
        exitFog.setLinearOpaquePoint(37.0, 14.0, 0.0)
        exitFog.setLinearFallback(70.0, 999.0, 1000.0)
        self.trolleyExitFog = self.trolleyStation.attachNewNode(exitFog)
        self.trolleyExitFogNode = exitFog
        
        enterFog = Fog("TrolleyEnterFog")
        enterFog.setColor(0.0, 0.0, 0.0)
        enterFog.setLinearOnsetPoint(0.0, 14.0, 0.0)
        enterFog.setLinearOpaquePoint(-7.0, 14.0, 0.0)
        enterFog.setLinearFallback(70.0, 999.0, 1000.0)
        self.trolleyEnterFog = self.trolleyStation.attachNewNode(enterFog)
        self.trolleyEnterFogNode = enterFog

        # We'll have fog explicitly disabled for the trolley car, by
        # default.  This makes it look maybe a little weird in
        # Donald's Dock--why does the trolley punch through the fog so
        # well?  But it keeps the trolley from flashing in and out as
        # we turn on and off the shadow fog.
        self.trolleyCar.setFogOff()

        # Variables used to animate trolley parts
        # Key
        self.keys = self.trolleyCar.findAllMatches('**/key')
        self.numKeys = self.keys.getNumPaths()
        self.keyInit = []
        self.keyRef = []
        for i in range(self.numKeys):
            key = self.keys[i]
            key.setTwoSided(1)
            ref = self.trolleyCar.attachNewNode('key' + `i` + 'ref')
            ref.iPosHpr(key)
            self.keyRef.append(ref)
            self.keyInit.append(key.getTransform())
        # Front wheels
        self.frontWheels = self.trolleyCar.findAllMatches('**/front_wheels')
        self.numFrontWheels = self.frontWheels.getNumPaths()
        self.frontWheelInit = []
        self.frontWheelRef = []
        for i in range(self.numFrontWheels):
            wheel = self.frontWheels[i]
            ref = self.trolleyCar.attachNewNode('frontWheel' + `i` + 'ref')
            ref.iPosHpr(wheel)
            self.frontWheelRef.append(ref)
            self.frontWheelInit.append(wheel.getTransform())
        # Back wheels
        self.backWheels = self.trolleyCar.findAllMatches('**/back_wheels')
        self.numBackWheels = self.backWheels.getNumPaths()
        self.backWheelInit = []
        self.backWheelRef = []
        for i in range(self.numBackWheels):
            wheel = self.backWheels[i]
            ref = self.trolleyCar.attachNewNode('backWheel' + `i` + 'ref')
            ref.iPosHpr(wheel)
            self.backWheelRef.append(ref)
            self.backWheelInit.append(wheel.getTransform())

        # Create the trolley enter track
        trolleyAnimationReset = Func(self.resetAnimation)
        trolleyEnterStartPos = Point3(-20, 14, -1)
        trolleyEnterEndPos = Point3(15, 14, -1)

        trolleyEnterPos = Sequence(name="TrolleyEnterPos")
        if base.wantFog:
            trolleyEnterPos.append(Func(self.trolleyCar.setFog, self.trolleyEnterFogNode))
        trolleyEnterPos.append(self.trolleyCar.posInterval(
            TROLLEY_ENTER_TIME,
            trolleyEnterEndPos,
            startPos=trolleyEnterStartPos,
            blendType="easeOut"))
        if base.wantFog:
            trolleyEnterPos.append(Func(self.trolleyCar.setFogOff))
            
        trolleyEnterTrack = Sequence(trolleyAnimationReset, 
                                     trolleyEnterPos,
                                     name = 'trolleyEnter')
        # 
        # How many revolutions of the wheel?
        keyAngle = round(TROLLEY_ENTER_TIME) * 360
        dist = Vec3(trolleyEnterEndPos - trolleyEnterStartPos).length()
        wheelAngle = dist/(2.0 * math.pi * 0.95) * 360
        trolleyEnterAnimateInterval = LerpFunctionInterval(
            self.animateTrolley,
            duration = TROLLEY_ENTER_TIME,
            blendType = "easeOut",
            extraArgs = [keyAngle, wheelAngle],
            name = "TrolleyAnimate")
        trolleyEnterSoundTrack = SoundInterval(self.trolleyAwaySfx, node=self.trolleyCar)
        self.trolleyEnterTrack = Parallel(trolleyEnterTrack,
                                          trolleyEnterAnimateInterval,
                                          trolleyEnterSoundTrack,
                                          )

        # Create the trolley exit track
        trolleyExitStartPos = Point3(15, 14, -1)
        trolleyExitEndPos = Point3(50, 14, -1)

        trolleyExitPos = Sequence(name="TrolleyExitPos")
        if base.wantFog:
            trolleyExitPos.append(Func(self.trolleyCar.setFog, self.trolleyExitFogNode))
        trolleyExitPos.append(self.trolleyCar.posInterval(
            TROLLEY_EXIT_TIME,
            trolleyExitEndPos,
            startPos=trolleyExitStartPos,
            blendType="easeIn"))
        if base.wantFog:
            trolleyExitPos.append(Func(self.trolleyCar.setFogOff))
        
        
        trolleyExitBellInterval = SoundInterval(self.trolleyBellSfx, node=self.trolleyCar)
        trolleyExitAwayInterval = SoundInterval(self.trolleyAwaySfx, node=self.trolleyCar)

        keyAngle = round(TROLLEY_EXIT_TIME) * 360
        dist = Vec3(trolleyExitEndPos - trolleyExitStartPos).length()
        wheelAngle = dist/(2.0 * math.pi * 0.95) * 360
        trolleyExitAnimateInterval = LerpFunctionInterval(
            self.animateTrolley,
            duration = TROLLEY_EXIT_TIME,
            blendType = "easeIn",
            extraArgs = [keyAngle, wheelAngle],
            name = "TrolleyAnimate")

        self.trolleyExitTrack = Parallel(trolleyExitPos,
                                         trolleyExitBellInterval,
                                         trolleyExitAwayInterval,
                                         trolleyExitAnimateInterval,
                                         name = self.uniqueName("trolleyExit")
                                         )

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        # Go to the off state when the object is put in the cache
        self.fsm.request("off")

        # No more toon animating
        self.clearToonTracks()

        self.trolleyExitFog.removeNode()
        del self.trolleyExitFog
        del self.trolleyExitFogNode
        self.trolleyEnterFog.removeNode()
        del self.trolleyEnterFog
        del self.trolleyEnterFogNode

        del self.loader
        self.trolleyEnterTrack.pause()
        self.trolleyEnterTrack = None
        # del'ing this will cause the application to exit with an error code: del self.trolleyEnterTrack
        # Lets try it again - maybe the ghosts are gone now?
        # If we leave it commented out, we leak trolleys on the clients
        del self.trolleyEnterTrack
        self.trolleyExitTrack.pause()
        self.trolleyExitTrack = None
        del self.trolleyExitTrack
        del self.trolleyStation
        del self.trolleyCar
        del self.keys
        del self.numKeys
        del self.keyInit
        del self.keyRef
        del self.frontWheels
        del self.numFrontWheels
        del self.frontWheelInit
        del self.frontWheelRef
        del self.backWheels
        del self.numBackWheels
        del self.backWheelInit
        del self.backWheelRef
    
    def delete(self):
        del self.trolleyAwaySfx
        del self.trolleyBellSfx
        DistributedObject.DistributedObject.delete(self)
        del self.fsm
    
    def setState(self, state, timestamp):
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def allowedToEnter(self):
        """Check if the local toon is allowed to enter."""
        if base.cr.isPaid():
            return True
        place = base.cr.playGame.getPlace()
        myHoodId = ZoneUtil.getCanonicalHoodId(place.zoneId)
        if  myHoodId in \
           (ToontownGlobals.ToontownCentral,
            ToontownGlobals.MyEstate,
            ToontownGlobals.GoofySpeedway,
            ):
            # trialer going to TTC/Estate/Goofy Speedway, let them through
            return True
        return False

    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')         

    def handleEnterTrolleySphere(self, collEntry):
        self.notify.debug("Entering Trolley Sphere....")
        
        # To counter the toon trap bug
        if(base.localAvatar.getPos(render).getZ() < (self.trolleyCar.getPos(render).getZ())):
            return
        if self.allowedToEnter():
            # Put localToon into requestBoard mode.
            self.loader.place.detectedTrolleyCollision()
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='minigames',
                                                  doneFunc=self.handleOkTeaser)            
    
    def handleEnterTrolley(self):
        # Tell the server that this avatar wants to board.
        toon = base.localAvatar
        self.sendUpdate("requestBoard",[])

    def fillSlot0(self, avId):
        self.fillSlot(0, avId)
    
    def fillSlot1(self, avId):
        self.fillSlot(1, avId)
    
    def fillSlot2(self, avId):
        self.fillSlot(2, avId)
    
    def fillSlot3(self, avId):
        self.fillSlot(3, avId)

    def fillSlot(self, index, avId):
        #print "fill Slot: %d for %d" % (index, avId)
        if avId == 0:
            # This means that the slot is now empty, and no action should
            # be taken.
            pass
        else:
            # If localToon is boarding, he needs to change state and board the trolley.
            if avId == base.localAvatar.getDoId():
                # Ignore this message if it comes late (e.g., trolley is in the leaving state).
                if not (self.fsm.getCurrentState().getName() == 'waitEmpty' or
                        self.fsm.getCurrentState().getName() == 'waitCountdown'):
                    self.notify.warning("Can't board the trolley while in the '%s' state." % 
                        (self.fsm.getCurrentState().getName()))
                    self.loader.place.fsm.request('walk')
                    return
                    
                self.loader.place.trolley.fsm.request("boarding", [self.trolleyCar])
                self.localToonOnBoard = 1
                
				# Tell him he's on the trolley now.
                self.loader.place.trolley.fsm.request("boarded")

            if self.cr.doId2do.has_key(avId):
                # If the toon exists, look it up
                toon = self.cr.doId2do[avId]
                # Parent it to the trolley
                toon.stopSmooth()
                toon.wrtReparentTo(self.trolleyCar)
                toon.setAnimState("run", 1.0)
                toon.headsUp(-5, -4.5 + (index * 3), 1.4)

                sitStartDuration = toon.getDuration("sit-start")

                track = Sequence(
                    LerpPosInterval(toon, TOON_BOARD_TIME * 0.75,
                                    Point3(-5, -4.5 + (index * 3), 1.4)),
                    LerpHprInterval(toon, TOON_BOARD_TIME * 0.25,
                                    Point3(90, 0, 0)),
                    Parallel(Sequence(Wait(sitStartDuration*0.25),
                                      LerpPosInterval(toon, sitStartDuration*0.25,
                                             Point3(-3.9, -4.5 + (index * 3), 3.0)),
                                      ),
                             ActorInterval(toon, "sit-start"),
                             ),
                    Func(toon.setAnimState, "Sit", 1.0),
                    Func(self.clearToonTrack, avId),
                    name = toon.uniqueName("fillTrolley"),
                    autoPause = 1)
                
                track.delayDelete = DelayDelete.DelayDelete(toon, 'Trolley.fillSlot')
                self.storeToonTrack(avId, track)
                track.start()
            else:
                DistributedTrolley.notify.warning("toon: " + str(avId) +
                                                  " doesn't exist, and" +
                                                  " cannot board the trolley!")

    def emptySlot0(self, avId, timestamp):
        self.emptySlot(0, avId, timestamp)

    def emptySlot1(self, avId, timestamp):
        self.emptySlot(1, avId, timestamp)

    def emptySlot2(self, avId, timestamp):
        self.emptySlot(2, avId, timestamp)

    def emptySlot3(self, avId, timestamp):
        self.emptySlot(3, avId, timestamp)

    def notifyToonOffTrolley(self, toon):
        toon.setAnimState("neutral", 1.0)
        if toon == base.localAvatar:
            self.loader.place.trolley.handleOffTrolley()
            self.localToonOnBoard = 0
        else:
            toon.startSmooth()
        return
                
    def emptySlot(self, index, avId, timestamp):
        #print "Emptying slot: %d for %d" % (index, avId)
        # If localToon is exiting, he needs to change state
        if avId == 0:
            # This means that no one is currently exiting, and no action
            # should be taken
            pass
        else:
            if self.cr.doId2do.has_key(avId):
                # If the toon exists, look it up
                toon = self.cr.doId2do[avId]
                # Parent it to render
                toon.setHpr(self.trolleyCar, 90,0,0)
                toon.wrtReparentTo(render)
                toon.stopSmooth()
                # toon.setAnimState("run", 1.0)
                
                # Place it on the appropriate spot relative to the
                # trolley station

                sitStartDuration = toon.getDuration("sit-start")

                track = Sequence(
                    # Hop off the seat
                    Parallel(ActorInterval(toon, "sit-start",
                                           startTime=sitStartDuration,
                                           endTime=0.0),
                             Sequence(Wait(sitStartDuration*0.5),
                                      LerpPosInterval(toon, sitStartDuration*0.25,
                                                      Point3(-5, -4.5 + (index * 3), 1.4),
                                                      other=self.trolleyCar),
                                      ),
                             ),
                    # Then run
                    Func(toon.setAnimState, "run", 1.0),
                    LerpPosInterval(toon, TOON_EXIT_TIME,
                                    Point3(21 - (index * 3),
                                           -5,
                                           0.02),
                                    #Point3(165, 0, 0),
                                    other=self.trolleyStation
                                    ),
                    # Tell the toon he is free to roam now
                    Func(self.notifyToonOffTrolley, toon),
                    Func(self.clearToonTrack, avId),
                    name = toon.uniqueName("emptyTrolley"),
                    autoPause = 1)
                track.delayDelete = DelayDelete.DelayDelete(toon, 'Trolley.emptySlot')
                self.storeToonTrack(avId, track)
                track.start()

                # Tell localToon he is exiting (if localToon is on board)
                if avId == base.localAvatar.getDoId():
                    self.loader.place.trolley.fsm.request("exiting")

            else:
                DistributedTrolley.notify.warning("toon: " + str(avId) +
                                                  " doesn't exist, and" +
                                                  " cannot exit the trolley!")

    def rejectBoard(self, avId):
        # This should only be sent to us if our localToon requested
        # permission to board the trolley.
        assert(base.localAvatar.getDoId() == avId)
        self.loader.place.trolley.handleRejectBoard()

    def setMinigameZone(self, zoneId, minigameId):
        # This is how the server puts the clients into a minigame
        self.localToonOnBoard = 0        
        messenger.send("playMinigame", [zoneId, minigameId])

    def __enableCollisions(self):
        # start listening for toons to enter.
        self.accept('entertrolley_sphere', self.handleEnterTrolleySphere)
        self.accept('enterTrolleyOK', self.handleEnterTrolley)
        self.trolleySphereNode.setCollideMask(ToontownGlobals.WallBitmask)

    def __disableCollisions(self):
        # stop listening for toons.
        self.ignore('entertrolley_sphere')
        self.ignore('enterTrolleyOK')
        self.trolleySphereNode.setCollideMask(BitMask32(0))
    
    ##### Off state #####

    def enterOff(self):
        return None

    def exitOff(self):
        return None
    
    ##### Entering state #####

    def enterEntering(self, ts):
        # Lerp the trolley into place via a track
        self.trolleyEnterTrack.start(ts)

    def exitEntering(self):
        self.trolleyEnterTrack.finish()

    ##### WaitEmpty state #####

    def enterWaitEmpty(self, ts):
        # Toons may now try to board the trolley
        self.__enableCollisions()

    def exitWaitEmpty(self):
        # Toons may not attempt to board the trolley if it isn't waiting
        self.__disableCollisions()

    ##### WaitCountdown state #####

    def enterWaitCountdown(self, ts):
        # Toons may now try to board the trolley
        self.__enableCollisions()
        self.accept("trolleyExitButton", self.handleExitButton)
        # Start the countdown clock...
        self.clockNode = TextNode("trolleyClock")
        self.clockNode.setFont(ToontownGlobals.getSignFont())
        self.clockNode.setAlign(TextNode.ACenter)
        self.clockNode.setTextColor(0.9, 0.1, 0.1, 1)
        self.clockNode.setText("10")
        self.clock = self.trolleyStation.attachNewNode(self.clockNode)
        self.clock.setBillboardAxis()
        self.clock.setPosHprScale(15.86, 13.82, 11.68,
                                  -0.00, 0.00, 0.00,
                                  3.02, 3.02, 3.02)
        if ts < self.trolleyCountdownTime:
            self.countdown(self.trolleyCountdownTime - ts)
        return

    def timerTask(self, task):
        countdownTime = int(task.duration - task.time)
        timeStr = str(countdownTime)

        if self.clockNode.getText() != timeStr:
            self.clockNode.setText(timeStr)

        if task.time >= task.duration:
            return Task.done
        else:
            return Task.cont

    def countdown(self, duration):
        countdownTask = Task(self.timerTask)
        countdownTask.duration = duration
        taskMgr.remove("trolleyTimerTask")
        return taskMgr.add(countdownTask, "trolleyTimerTask")

    def handleExitButton(self):
        # This gets called when the exit button gets pushed.
        self.sendUpdate("requestExit")
        
    def exitWaitCountdown(self):
        # Toons may not attempt to board the trolley if it isn't waiting
        self.__disableCollisions()
        self.ignore("trolleyExitButton")
        # Stop the countdown clock...
        taskMgr.remove("trolleyTimerTask")
        self.clock.removeNode()
        del self.clock
        del self.clockNode
        
    ##### Leaving state #####

    def enterLeaving(self, ts):
        # Move the trolley into the tunnel via a track
        self.trolleyExitTrack.start(ts)
        if self.localToonOnBoard:
            if hasattr(self.loader.place, 'trolley') and self.loader.place.trolley:
                self.loader.place.trolley.fsm.request("trolleyLeaving")
        
    def exitLeaving(self):
        self.trolleyExitTrack.finish()


    ##### Miscellaneous support functions #####

    def animateTrolley(self, t, keyAngle, wheelAngle):
        # Make key rotate at 1 rotation per second
        for i in range(self.numKeys):
            key = self.keys[i]
            ref = self.keyRef[i]
            key.setH(ref, t * keyAngle)
        for i in range(self.numFrontWheels):
            frontWheel = self.frontWheels[i]
            ref = self.frontWheelRef[i]
            frontWheel.setH(ref, t * wheelAngle)
        for i in range(self.numBackWheels):
            backWheel = self.backWheels[i]
            ref = self.backWheelRef[i]
            backWheel.setH(ref, t * wheelAngle)

    def resetAnimation(self):
        for i in range(self.numKeys):
            self.keys[i].setTransform(self.keyInit[i])
        for i in range(self.numFrontWheels):
            self.frontWheels[i].setTransform(self.frontWheelInit[i])
        for i in range(self.numBackWheels):
            self.backWheels[i].setTransform(self.backWheelInit[i])

    def getStareAtNodeAndOffset(self):
        return self.trolleyCar, Point3(0,0,4)

    def storeToonTrack(self, avId, track):
        # Clear out any currently playing tracks on this toon
        self.clearToonTrack(avId)
        # Store this new one
        self.__toonTracks[avId] = track

    def clearToonTrack(self, avId):
        # Clear out any currently playing tracks on this toon
        oldTrack = self.__toonTracks.get(avId)
        if oldTrack:
            oldTrack.pause()
            DelayDelete.cleanupDelayDeletes(oldTrack)
            del self.__toonTracks[avId]

    def clearToonTracks(self):
        #We can't use an iter because we are deleting keys
        keyList = []
        for key in self.__toonTracks:
            keyList.append(key)
            
        for key in keyList:
            if self.__toonTracks.has_key(key):
                self.clearToonTrack(key)
            
        

        
