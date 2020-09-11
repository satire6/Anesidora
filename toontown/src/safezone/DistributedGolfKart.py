from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from TrolleyConstants import *

from toontown.golf import GolfGlobals
from toontown.toonbase import ToontownGlobals
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.distributed import DelayDelete
from direct.task.Task import Task
from direct.showbase import PythonUtil
from toontown.toontowngui import TeaserPanel
from toontown.toon import ToonDNA
from toontown.hood import ZoneUtil

class DistributedGolfKart(DistributedObject.DistributedObject):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGolfKart")
    SeatOffsets = ((0.5, -0.5, 0), (-0.5, -0.5, 0), (0.5, 0.5, 0), (-0.5, 0.5, 0))
    JumpOutOffsets = ((3, 5, 0), (1.5, 4, 0), (-1.5, 4, 0), (-3, 4, 0))
    KART_ENTER_TIME = 400
    
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

        # this is to stop the seeing toons sitting in midair
        # a little scary as it might cause more problems
        self.avIds = [0,0,0,0] # which toons are in the seats

        self.kartModelPath = 'phase_6/models/golf/golf_cart3.bam'
        
    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedObject.DistributedObject.generate(self)

        # Get the state machine stuff for playGame
        self.loader = self.cr.playGame.hood.loader
        if(self.loader):
            self.notify.debug("Loader has been loaded")
            self.notify.debug(str(self.loader))
        else:
            self.notify.debug("Loader has not been loaded")

        self.golfKart = render.attachNewNode('golfKartNode')
        #kart = loader.loadModel('phase_6/models/karting/Kart3_Final')
        self.kart = loader.loadModel(self.kartModelPath)
        self.kart.setPos(0, 0, 0)
        self.kart.setScale(1)
        self.kart.reparentTo(self.golfKart)
        self.golfKart.reparentTo(self.loader.geom)

        # Wheels
        self.wheels = self.kart.findAllMatches('**/wheelNode*')
        self.numWheels = self.wheels.getNumPaths()

        #debugAxis = loader.loadModel('models/misc/xyzAxis')
        #debugAxis.setColorScale(1.0, 1.0, 1.0, 0.25)
        #debugAxis.setTransparency(True)
        #debugAxis.reparentTo(self.golfKart)
        
        trolleyExitBellInterval = SoundInterval(self.trolleyBellSfx, node=self.golfKart)
        trolleyExitAwayInterval = SoundInterval(self.trolleyAwaySfx, node=self.golfKart)

    def announceGenerate(self):
        """Setup other fields dependent on the required fields."""
        DistributedObject.DistributedObject.announceGenerate(self)
        #self.golfKartSphereNode = self.golfKart.attachNewNode(CollisionNode('golfkart_sphere_%d' % self.golfCourse))
        self.golfKartSphereNode = self.golfKart.attachNewNode(CollisionNode('golfkart_sphere_%d' % self.getDoId()))
        self.golfKartSphereNode.node().addSolid(CollisionSphere(0, 0, 0, 2))

        angle = self.startingHpr[0]
        angle -= 90
        radAngle = deg2Rad(angle)
        unitVec = Vec3( math.cos(radAngle), math.sin(radAngle), 0)
        unitVec *= 45.0
        self.endPos =  self.startingPos + unitVec

        dist = Vec3(self.endPos - self.enteringPos).length()
        wheelAngle = (dist / (4.8 * 1.4 * math.pi)) * 360

        self.kartEnterAnimateInterval = Parallel(
            # start a lerp HPR for each wheel
            LerpHprInterval(self.wheels[0], 5.0, Vec3(self.wheels[0].getH(), wheelAngle, self.wheels[0].getR())),
            LerpHprInterval(self.wheels[1], 5.0, Vec3(self.wheels[1].getH(), wheelAngle, self.wheels[1].getR())),
            LerpHprInterval(self.wheels[2], 5.0, Vec3(self.wheels[2].getH(), wheelAngle, self.wheels[2].getR())),
            LerpHprInterval(self.wheels[3], 5.0, Vec3(self.wheels[3].getH(), wheelAngle, self.wheels[3].getR())),
            name = "KartAnimate")

        trolleyExitTrack1 = Parallel(
            LerpPosInterval(self.golfKart, 5.0, self.endPos),
            self.kartEnterAnimateInterval,
            name = "KartExitTrack")
        self.trolleyExitTrack = Sequence(
            trolleyExitTrack1,
            Func(self.hideSittingToons),
            )

        self.trolleyEnterTrack = Sequence(
            LerpPosInterval(self.golfKart, 5.0, self.startingPos, startPos = self.enteringPos))

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        # Go to the off state when the object is put in the cache
        self.fsm.request("off")

        # No more toon animating
        self.clearToonTracks()

        del self.wheels
        del self.numWheels

        del self.golfKartSphereNode
        self.notify.debug("Deleted self loader " + str(self.getDoId()))
        del self.loader
        self.golfKart.removeNode()
        self.kart.removeNode()
        del self.kart
        del self.golfKart


        self.trolleyEnterTrack.pause()
        self.trolleyEnterTrack = None
        del self.kartEnterAnimateInterval
        # del'ing this will cause the application to exit with an error code: del self.trolleyEnterTrack
        # Lets try it again - maybe the ghosts are gone now?
        # If we leave it commented out, we leak trolleys on the clients
        del self.trolleyEnterTrack
        self.trolleyExitTrack.pause()
        self.trolleyExitTrack = None
        del self.trolleyExitTrack

        #import pdb;
        #pdb.set_trace()

    def delete(self):
        self.notify.debug("Golf kart getting deleted: %s" % self.getDoId())
        del self.trolleyAwaySfx
        del self.trolleyBellSfx
        DistributedObject.DistributedObject.delete(self)
        del self.fsm
    
    def setState(self, state, timestamp):
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def handleEnterTrolleySphere(self, collEntry):
        self.notify.debug("Entering Trolley Sphere....")
        # Put localToon into requestBoard mode.
        self.loader.place.detectedTrolleyCollision()

    def allowedToEnter(self):
        """Check if the local toon is allowed to enter."""
        if base.cr.isPaid():
            return True
        return False

    def handleEnterGolfKartSphere(self, collEntry):
        self.notify.debug("Entering Golf Kart Sphere.... %s" % self.getDoId())
        if self.allowedToEnter():
            # Put localToon into requestBoard mode.
            self.loader.place.detectedGolfKartCollision(self)  
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='golf',
                                                  doneFunc=self.handleOkTeaser)

    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')            
            
    
    def handleEnterTrolley(self):
        # Tell the server that this avatar wants to board.
        toon = base.localAvatar
        self.sendUpdate("requestBoard",[])

    def handleEnterGolfKart(self):
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
        assert self.notify.debugStateCall(self)
        #print "fill Slot: %d for %d" % (index, avId)
        self.avIds[index] = avId
        if avId == 0:
            # This means that the slot is now empty, and no action should
            # be taken.
            pass
        else:
            # If localToon is boarding, he needs to change state
            if avId == base.localAvatar.getDoId():
                self.loader.place.trolley.fsm.request("boarding", [self.golfKart])
                self.localToonOnBoard = 1

            # Put that toon on the trolley

            # If it's localToon, tell him he's on the trolley now
            if avId == base.localAvatar.getDoId():
                self.loader.place.trolley.fsm.request("boarded")

            if self.cr.doId2do.has_key(avId):
                # If the toon exists, look it up
                toon = self.cr.doId2do[avId]
                # Parent it to the trolley
                toon.stopSmooth()
                toon.wrtReparentTo(self.golfKart)
                #toon.setAnimState("run", 1.0)
                #toon.headsUp(-5, -4.5 + (index * 3), 1.4)

                sitStartDuration = toon.getDuration("sit-start")
                jumpTrack = self.generateToonJumpTrack(toon, index)
                track = Sequence(
                    #LerpPosInterval(toon, TOON_BOARD_TIME * 0.75,
                    #                Point3(-5, -4.5 + (index * 3), 1.4)),
                    #LerpHprInterval(toon, TOON_BOARD_TIME * 0.25,
                    #                Point3(90, 0, 0)),
                    #Parallel(Sequence(Wait(sitStartDuration*0.25),
                    #                  LerpPosInterval(toon, sitStartDuration*0.25,
                    #                         Point3(-3.9, -4.5 + (index * 3), 3.0)),
                    #                  ),
                    #         ActorInterval(toon, "sit-start"),
                    #         ),
                    jumpTrack,
                    Func(toon.setAnimState, "Sit", 1.0),
                    Func(self.clearToonTrack, avId),
                    name = toon.uniqueName("fillTrolley"),
                    autoPause = 1)
                
                track.delayDelete = DelayDelete.DelayDelete(toon, 'GolfKart.fillSlot')
                self.storeToonTrack(avId, track)
                track.start()
            else:
                self.notify.warning("toon: " + str(avId) +
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
            self.avIds[index] = 0
            if self.cr.doId2do.has_key(avId):
                # If the toon exists, look it up
                toon = self.cr.doId2do[avId]
                # Parent it to render
                #toon.setHpr(self.golfKart, 90,0,0)
                #toon.wrtReparentTo(render)
                toon.stopSmooth()
                # toon.setAnimState("run", 1.0)
                
                # Place it on the appropriate spot relative to the
                # trolley station

                sitStartDuration = toon.getDuration("sit-start")
                jumpOutTrack = self.generateToonReverseJumpTrack(toon, index)
                track = Sequence(
                    # Hop off the seat
                    #Parallel(ActorInterval(toon, "sit-start",
                    #                       startTime=sitStartDuration,
                    #                       endTime=0.0),
                    #         Sequence(Wait(sitStartDuration*0.5),
                    #                  LerpPosInterval(toon, sitStartDuration*0.25,
                    #                                  Point3( -4.5 + (index * 3), 5, 1.4),
                    #                                  other=self.golfKart),
                    #                  ),
                    #         ),
                    # Then run
##                     Func(toon.setAnimState, "run", 1.0),
##                     LerpPosInterval(toon, TOON_EXIT_TIME,
##                                     Point3(21 - (index * 3),
##                                            -5,
##                                            0.02),
##                                     #Point3(165, 0, 0),
##                                     other=self.golfKart
##                                     ),
                    
                    jumpOutTrack,
                    # Tell the toon he is free to roam now
                    Func(self.notifyToonOffTrolley, toon),
                    Func(self.clearToonTrack, avId),
                    name = toon.uniqueName("emptyTrolley"),
                    autoPause = 1)
                track.delayDelete = DelayDelete.DelayDelete(toon, 'GolfKart.emptySlot')
                self.storeToonTrack(avId, track)
                track.start()

                # Tell localToon he is exiting (if localToon is on board)
                if avId == base.localAvatar.getDoId():
                    self.loader.place.trolley.fsm.request("exiting")

            else:
                self.notify.warning("toon: " + str(avId) +
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

    def setGolfZone(self, zoneId, courseId):
        """This is how the server puts the clients into a golf course."""
        self.localToonOnBoard = 0        
        messenger.send("playGolf", [zoneId, courseId])

    def __enableCollisions(self):
        # start listening for toons to enter.
        assert self.notify.debugStateCall(self)
        self.accept('entertrolley_sphere', self.handleEnterTrolleySphere)
        self.accept('enterTrolleyOK', self.handleEnterTrolley)

        self.accept('entergolfkart_sphere_%d' % self.getDoId(), self.handleEnterGolfKartSphere)
        self.accept('enterGolfKartOK_%d' % self.getDoId(), self.handleEnterGolfKart)        
        self.golfKartSphereNode.setCollideMask(ToontownGlobals.WallBitmask)        

    def __disableCollisions(self):
        # stop listening for toons.
        self.ignore('entertrolley_sphere')
        self.ignore('enterTrolleyOK')
        #self.ignore('entergolfkart_sphere_%d' % self.golfCourse)
        #self.ignore('enterTrolleyOK_%d' % self.golfCourse)
        #self.ignore('enterGolfKartOK_%d' % self.golfCourse)

        self.ignore('entergolfkart_sphere_%d' % self.getDoId())
        self.ignore('enterTrolleyOK_%d' % self.getDoId())
        self.ignore('enterGolfKartOK_%d' % self.getDoId())

        self.golfKartSphereNode.setCollideMask(BitMask32(0))        

    
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
        self.clock = self.golfKart.attachNewNode(self.clockNode)
        self.clock.setBillboardAxis()
        self.clock.setPosHprScale(0, -1, 7.0,
                                  -0.00, 0.00, 0.00,
                                  2.0, 2.0, 2.0)
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
        taskMgr.remove(self.uniqueName("golfKartTimerTask"))
        return taskMgr.add(countdownTask, self.uniqueName("golfKartTimerTask"))

    def handleExitButton(self):
        # This gets called when the exit button gets pushed.
        self.sendUpdate("requestExit")
        #import pdb; pdb.set_trace()
        
    def exitWaitCountdown(self):
        # Toons may not attempt to board the trolley if it isn't waiting
        self.__disableCollisions()
        self.ignore("trolleyExitButton")
        # Stop the countdown clock...
        taskMgr.remove(self.uniqueName("golfKartTimerTask"))
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
        pass


    ##### Miscellaneous support functions #####

    def getStareAtNodeAndOffset(self):
        return self.golfKart, Point3(0,0,4)

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
            if self.__toonTracks.get(avId):
                DelayDelete.cleanupDelayDeletes(self.__toonTracks[avId])
                del self.__toonTracks[avId]

    def clearToonTracks(self):
        #We can't use an iter because we are deleting keys
        keyList = []
        for key in self.__toonTracks:
            keyList.append(key)
            
        for key in keyList:
            if self.__toonTracks.has_key(key):
                self.clearToonTrack(key)

    def setGolfCourse(self, golfCourse):
        """Set the golf course as dictated by the AI."""
        assert self.notify.debugStateCall(self)
        self.golfCourse = golfCourse

    def setPosHpr(self, x, y, z, h, p ,r):
        """Set the pos hpr as dictated by the AI."""
        self.startingPos = Vec3(x, y, z)
        self.enteringPos = Vec3(x, y, z - 10)
        self.startingHpr = Vec3(h, 0, 0)
        self.golfKart.setPosHpr( x, y, z, h, 0, 0 )        

    def setColor(self, r, g, b):
        """Set the color of the golf kart."""
        kartBody = self.kart.find('**/main_body')
        kartBody.setColor(r / 255.0, g / 255.0, b / 255.0, 1)
        cartBase = self.kart.find('**/cart_base*')

        # Desaturate coloring of kart for bumper
        red = r / 255.0
        green = g / 255.0
        blue = b / 255.0

        if red >= green and red > blue:
            # Mostly red kart
            s = (red - blue) / float(red)
            v = red
            if(green > blue):
                h = ( green - blue ) / (red - blue)
            else:
                h = ( green - blue ) / (red - green)
        elif green >= blue:
            # Mostly green kart
            s = (green - blue) / float(green)
            v = green
            if( red > blue ):
                h = 2 + ( blue - red ) / ( green - blue )
            else:
                h = 2 + ( blue - red ) / ( green - red )
        else:
            # Currently unused blue kart
            if( red > green ):
                s = ( blue - green ) / blue
                h = 4 + (red - green) / (blue - green)
            else:
                s = (blue - red) / blue
                h = 4 + (red - green) / (blue - red)
            v = blue

        if( h < 0):
            h *= 60
            h += 360
            h /= 60
        s /= 3

        if s == 0:
            # All gray
            red = green = blue = v
        else:
            i = int(h)
            f = h - i
            p = v * ( 1 - s)
            q = v * ( 1 - s * f )
            t = v * ( 1 - s * ( 1 - f ) )

            if i == 0:
                red = v
                green = t
                blue = p
            elif i == 1:
                red = q
                green = v
                blue = p
            elif i == 2:
                red = p
                green = v
                blue = t
            elif i == 3:
                red = p
                green = q
                blue = v
            elif i == 4:
                red = t
                green = p
                blue = v
            elif i == 5:
                red = v
                green = p
                blue = q
            
        cartBase.setColorScale(red, green, blue, 1)
        #seats = self.kart.find('**/seat_cushion')
        #seats.setColor(GolfGlobals.PlayerColors[g])
        #seatBack.setColor(GolfGlobals.PlayerColors[g])

    def generateToonJumpTrack( self, av, seatIndex ):
        """Return an interval of the toon jumping into the golf kart."""
        # Maintain a reference to Parent and Scale of avatar in case they
        # exit from the kart.
        #base.sb = self

        av.pose('sit', 47)
        hipOffset = av.getHipsParts()[2].getPos(av)
        
        def getToonJumpTrack( av, seatIndex ):
            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = self.golfKart):
                dest = Point3(0,0,0)
                if hasattr(self, 'golfKart') and self.golfKart:
                    dest = Vec3(self.golfKart.getPos(av.getParent()))
                    seatNode = self.golfKart.find("**/seat" + str(seatIndex + 1))
                    dest += seatNode.getPos(self.golfKart)
                    dna = av.getStyle()
                    dest -= hipOffset
                    if(seatIndex < 2):
                        dest.setY( dest.getY() + 2 * hipOffset.getY())
                    dest.setZ(dest.getZ() + 0.1)
                else:
                    self.notify.warning('getJumpDestinvalid golfKart, returning (0,0,0)') 
                return dest

            def getJumpHpr(av = av, node = self.golfKart):
                hpr = Point3(0,0,0)
                if hasattr(self, 'golfKart') and self.golfKart:
                    hpr = self.golfKart.getHpr(av.getParent())
                    if(seatIndex < 2):
                        hpr.setX( hpr.getX() + 180)
                    else:
                        hpr.setX( hpr.getX() )
                    angle = PythonUtil.fitDestAngle2Src(av.getH(), hpr.getX())
                    hpr.setX(angle)
                else:
                    self.notify.warning('getJumpHpr invalid golfKart, returning (0,0,0)')                    
                return hpr

            toonJumpTrack = Parallel(
                ActorInterval( av, 'jump' ),
                Sequence(
                   Wait( 0.43 ),
                   Parallel( LerpHprInterval( av,
                                              hpr = getJumpHpr,
                                              duration = .9 ),
                             ProjectileInterval( av,
                                                 endPos = getJumpDest,
                                                 duration = .9 )
                             ),
                   )
                )
            return toonJumpTrack

        def getToonSitTrack( av ):
            toonSitTrack = Sequence(

                ActorInterval( av, 'sit-start' ),
                Func( av.loop, 'sit' )
                )
            return toonSitTrack

        toonJumpTrack = getToonJumpTrack( av, seatIndex )
        toonSitTrack = getToonSitTrack( av )
        
        jumpTrack = Sequence(
            Parallel(
                toonJumpTrack,
                Sequence( Wait(1),
                          toonSitTrack,
                          ),
                ),
            #Func( self.av.setPosHpr, 0, 0, 0, 0, 0, 0 ),
            #Func( self.av.setPosHpr, 0, .45, -.25, 0, 0, 0 ),
            Func( av.wrtReparentTo, self.golfKart ),            
            #Func( av.setPosHpr, self.SeatOffsets[seatIndex][0], self.SeatOffsets[seatIndex][1],
            #      self.SeatOffsets[seatIndex][2], 180, 0, 0),
            #Func( self.av.setScale, self.kart.accGeomScale/self.kart.baseScale ),
            #toonSitTrack,
            #Func( self.av.wrtReparentTo, self.kart.rotateNode )
            )
        
        return jumpTrack

    def generateToonReverseJumpTrack( self, av, seatIndex ):
        """Return an interval of the toon jumping out of the golf kart."""        
        self.notify.debug("av.getH() = %s" % av.getH())
        def getToonJumpTrack( av, destNode ):
            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = destNode):
                dest = node.getPos(av.getParent())
                dest += Vec3(*self.JumpOutOffsets[seatIndex])
                return dest

            def getJumpHpr(av = av, node = destNode):
                hpr = node.getHpr(av.getParent())
                hpr.setX( hpr.getX() + 180)
                angle = PythonUtil.fitDestAngle2Src(av.getH(), hpr.getX())
                hpr.setX(angle)
                return hpr
            
            toonJumpTrack = Parallel(
                ActorInterval( av, 'jump' ),
                Sequence(
                  Wait( 0.1), #43 ),
                  Parallel( #LerpHprInterval( av,
                            #                 hpr = getJumpHpr,
                            #                 duration = .9 ),
                            ProjectileInterval( av,
                                                endPos = getJumpDest,
                                                duration = .9 ) )
                  )
                )  
            return toonJumpTrack

        toonJumpTrack = getToonJumpTrack( av, self.golfKart)
        jumpTrack = Sequence(
            toonJumpTrack,
            Func( av.loop, 'neutral' ),
            Func( av.wrtReparentTo, render ),
            #Func( self.av.setPosHpr, self.exitMovieNode, 0,0,0,0,0,0 ),
            )
        return jumpTrack

    def hideSittingToons(self):
        """Hide the toons sittting on the kart. To avoid seeing them sitting in midair."""
        for avId in self.avIds:
            if avId:
                av = base.cr.doId2do.get(avId)
                if av:
                    av.hide()
