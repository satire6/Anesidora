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
from toontown.toonbase.ToontownTimer import ToontownTimer

from direct.task.Task import Task
from direct.showbase import PythonUtil

from toontown.toon import ToonDNA

from direct.showbase import RandomNumGen
from toontown.battle.BattleSounds import *

class DistributedPicnicBasket(DistributedObject.DistributedObject):

    seatState = Enum("Empty, Full, Eating")
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPicnicBasket")
    
    def __init__(self, cr):
        """__init__(cr)
        """
        DistributedObject.DistributedObject.__init__(self, cr)

        self.localToonOnBoard = 0
        self.seed = 0
        self.random = None
        self.picnicCountdownTime = \
                              base.config.GetFloat("picnic-countdown-time",
                                                   ToontownGlobals.PICNIC_COUNTDOWN_TIME)
        self.picnicBasketTrack = None # only one track contains the picnic basket shrink/grow

        self.fsm = ClassicFSM.ClassicFSM('DistributedTrolley',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['waitEmpty','waitCountdown']),
                            State.State('waitEmpty',
                                        self.enterWaitEmpty,
                                        self.exitWaitEmpty,
                                        ['waitCountdown']),
                            State.State('waitCountdown',
                                        self.enterWaitCountdown,
                                        self.exitWaitCountdown,
                                        ['waitEmpty'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                           )
        self.fsm.enterInitialState()

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
        self.foodLoader = ['phase_6/models/golf/picnic_sandwich.bam',
                           'phase_6/models/golf/picnic_apple.bam',
                           'phase_6/models/golf/picnic_cupcake.bam',
                           'phase_6/models/golf/picnic_chocolate_cake.bam'
                           ]
        self.fullSeat = []
        self.food = []
        for i in range(4):
            self.food.append(None)
            self.fullSeat.append(self.seatState.Empty)
        self.picnicItem = 0
     
    def announceGenerate(self):
        """Setup other fields dependent on the required fields."""

        self.picnicTable = self.loader.geom.find("**/*picnic_table_" + str(self.tableNumber))
        self.picnicTableSphereNodes = []

        self.numSeats = 4
        self.seats = []
        self.jumpOffsets = []
        self.basket = None
        for i in range(self.numSeats):
            self.seats.append(self.picnicTable.find("**/*seat%d" % (i+1)))
            self.jumpOffsets.append(self.picnicTable.find("**/*jumpOut%d" % (i+1)))
            #debugAxis = loader.loadModel('models/misc/xyzAxis')
            #debugAxis.setColorScale(1.0, 1.0, 1.0, 0.25)
            #debugAxis.setTransparency(True)
            #debugAxis.reparentTo(self.seats[i])

        self.tablecloth = self.picnicTable.find("**/basket_locator")
        
        DistributedObject.DistributedObject.announceGenerate(self)
        for i in range(self.numSeats):
            self.picnicTableSphereNodes.append(self.seats[i].attachNewNode(CollisionNode('picnicTable_sphere_%d_%d' % (self.getDoId(), i))))
            self.picnicTableSphereNodes[i].node().addSolid(CollisionSphere(0, 0, 0, 2))

        self.tableclothSphereNode = self.tablecloth.attachNewNode(CollisionNode('tablecloth_sphere'))
        self.tableclothSphereNode.node().addSolid(CollisionSphere(0, 0, -1, 4))

        angle = self.startingHpr[0]
        angle -= 90
        radAngle = deg2Rad(angle)
        unitVec = Vec3( math.cos(radAngle), math.sin(radAngle), 0)
        unitVec *= 30.0
        self.endPos =  self.startingPos + unitVec

        dist = Vec3(self.endPos - self.enteringPos).length()
        wheelAngle = dist/(0.5 * 1.4 * math.pi ) * 360

        self.seatNumber = 0

        self.clockNode = ToontownTimer()
        self.clockNode.setPos(1.16, 0, -0.83)
        self.clockNode.setScale(0.3)
        self.clockNode.hide()

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        # Go to the off state when the object is put in the cache
        self.fsm.request("off")

        # No more toon animating
        self.clearToonTracks()

        for i in range(self.numSeats):
            del self.picnicTableSphereNodes[0]
        del self.picnicTableSphereNodes
        
        self.notify.debug("Deleted self loader " + str(self.getDoId()))
        self.picnicTable.removeNode()
        self.picnicBasketTrack = None        
        #self.kart.removeNode()
        #del self.kart

        #import pdb;
        #pdb.set_trace()

    def delete(self):
        self.notify.debug("Golf kart getting deleted: %s" % self.getDoId())        
        DistributedObject.DistributedObject.delete(self)
        del self.fsm
    
    def setState(self, state, seed, timestamp):
        self.seed = seed
        if not self.random:
            self.random = RandomNumGen.RandomNumGen(seed)
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def handleEnterPicnicTableSphere(self, i, collEntry):
        # collEntry):
        assert self.notify.debugStateCall(self)
        self.seatNumber = i
        self.notify.debug("Entering Picnic Table Sphere.... %s" % self.getDoId())
        # Put localToon into requestBoard mode.
        #import pdb; pdb.set_trace()
        self.loader.place.detectedPicnicTableSphereCollision(self)  
    
    def handleEnterPicnicTable(self, i):
        # Tell the server that this avatar wants to board.
        assert self.notify.debugStateCall(self)
        toon = base.localAvatar
        self.sendUpdate("requestBoard",[i])        

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
        self.notify.debug( "fill Slot: %d for %d" % (index, avId) )
        if avId == 0:
            # This means that the slot is now empty, and no action should
            # be taken.
            pass
        else:
            self.fullSeat[index] = self.seatState.Full
            # If localToon is boarding, he needs to change state
            if avId == base.localAvatar.getDoId():
                # Start the countdown clock...
                self.clockNode.show()
                if index ==  0 or index == 3:
                    side = -1
                else:
                    side = 1
                if hasattr(self.loader.place, "trolley"):
                    self.loader.place.trolley.fsm.request("boarding", [self.tablecloth, side])
                else:
                    self.notify.warning('fillSlot no trolley in place')
                self.localToonOnBoard = 1

            # Put that toon on the table

            # If it's localToon, tell him he's on the trolley now
            if avId == base.localAvatar.getDoId():
                if hasattr(self.loader.place, "trolley"):
                    self.loader.place.trolley.fsm.request("boarded")
                    # hide the exit button until basket interval is over
                    self.loader.place.trolley.exitButton.hide()
            if self.cr.doId2do.has_key(avId):
                # If the toon exists, look it up
                toon = self.cr.doId2do[avId]
                # Parent it to the trolley
                toon.stopSmooth()
                toon.wrtReparentTo(self.tablecloth)
                sitStartDuration = toon.getDuration("sit-start")
                jumpTrack = self.generateToonJumpTrack(toon, index)
                track = Sequence(
                    jumpTrack,
                    Func(toon.setAnimState, "Sit", 1.0))
                # only add basket appear if there is no toons are already sitting
                self.notify.debug( "### fillSlot: fullSeat = %s" % self.fullSeat)
                if self.fullSeat.count(0) == 3:
                    self.notify.debug( "### fillSlot: adding basketAppear")
                    #track.append(self.generateBasketAppearTrack())
                    if self.picnicBasketTrack:
                        self.picnicBasketTrack.finish()
                    waitDuration = track.getDuration()
                    self.picnicBasketTrack = Sequence(
                        Wait(waitDuration),
                        self.generateBasketAppearTrack())
                    self.picnicBasketTrack.start()
                # make a random food appear
                track.append(self.generateFoodAppearTrack(index))
                # finish the rest of the staging
                track.append(
                    Sequence(
                    Func(self.clearToonTrack, avId),
                    name = toon.uniqueName("fillTrolley"),
                    autoPause = 1)
                    )
                if avId == base.localAvatar.getDoId():
                    if hasattr(self.loader.place, "trolley"):
                        track.append(Func(self.loader.place.trolley.exitButton.show))
                track.delayDelete = DelayDelete.DelayDelete(toon, 'PicnicBasket.fillSlot')
                self.storeToonTrack(avId, track)
                track.start()

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
        if hasattr(base,'localAvatar') and toon == base.localAvatar:
            if hasattr(self.loader.place, "trolley"):
                self.loader.place.trolley.handleOffTrolley()
            self.localToonOnBoard = 0
        else:
            toon.startSmooth()
        return
                
    def emptySlot(self, index, avId, timestamp):
        def emptySeat(index):
            # If localToon is exiting, he needs to change state
            self.notify.debug( "### seat %s now empty" % index)
            self.fullSeat[index] = self.seatState.Empty
        if avId == 0:
            # This means that the slot is now empty, and no action should
            # be taken.
            pass
        elif avId == 1:
            # Special cardinal value for unexpected exit.
            # The toon is gone, but we may still need to clean up his food
            self.fullSeat[index] = self.seatState.Empty
            track  = Sequence(self.generateFoodDisappearTrack(index))
            # if no toons left, make the basket go away
            self.notify.debug( "### empty slot - unexpetected: fullSeat = %s" % self.fullSeat)
            if self.fullSeat.count(0) == 4:
                self.notify.debug("### empty slot - unexpected: losing basket")
                if self.picnicBasketTrack:
                    self.picnicBasketTrack.finish()
                #track.append(self.generateBasketDisappearTrack())
                waitDuration = track.getDuration()
                self.picnicBasketTrack = Sequence(
                    Wait(waitDuration),
                    self.generateBasketDisappearTrack())
                self.picnicBasketTrack.start()
            track.start()
        else:
            self.fullSeat[index] = self.seatState.Empty
            if self.cr.doId2do.has_key(avId):
                if avId == base.localAvatar.getDoId():
                    # Stop the countdown clock..
                    if(self.clockNode):
                        self.clockNode.hide()

                # If the toon exists, look it up
                toon = self.cr.doId2do[avId]
                toon.stopSmooth()
                sitStartDuration = toon.getDuration("sit-start")
                jumpOutTrack = self.generateToonReverseJumpTrack(toon, index)
                track = Sequence(jumpOutTrack)
                # make the food go away
                track.append(self.generateFoodDisappearTrack(index))
                # if no toons left, make the basket go away
                self.notify.debug( "### empty slot: fullSeat = %s" % self.fullSeat)
                if self.fullSeat.count(0) == 4:
                    self.notify.debug( "### empty slot: losing basket")
                    if self.picnicBasketTrack:
                        self.picnicBasketTrack.finish()
                    #track.append(self.generateBasketDisappearTrack())
                    waitDuration = track.getDuration()
                    self.picnicBasketTrack = Sequence(
                        Wait(waitDuration),
                        self.generateBasketDisappearTrack())
                    self.picnicBasketTrack.start()
                    
                    # let the toon loose
                track.append(Sequence(
                    # Tell the toon he is free to roam now
                    Func(self.notifyToonOffTrolley, toon),
                    Func(self.clearToonTrack, avId),
                    Func(self.doneExit, avId),
                    Func(emptySeat, index),
                    name = toon.uniqueName("emptyTrolley"),
                    autoPause = 1))
                track.delayDelete = DelayDelete.DelayDelete(toon, 'PicnicBasket.emptySlot')
                self.storeToonTrack(avId, track)
                track.start()

    def rejectBoard(self, avId):
        # This should only be sent to us if our localToon requested
        # permission to board the trolley.
        assert(base.localAvatar.getDoId() == avId)
        self.loader.place.trolley.handleRejectBoard()

    def __enableCollisions(self):
        # start listening for toons to enter.
        assert self.notify.debugStateCall(self)
        for i in range(self.numSeats): 
            self.accept('enterpicnicTable_sphere_%d_%d' % (self.getDoId(), i), self.handleEnterPicnicTableSphere, [i])
            self.accept('enterPicnicTableOK_%d_%d' % (self.getDoId(), i), self.handleEnterPicnicTable, [i])        
            self.picnicTableSphereNodes[i].setCollideMask(ToontownGlobals.WallBitmask)        

    def __disableCollisions(self):
        assert self.notify.debugStateCall(self)
        for i in range(self.numSeats): 
            self.ignore('enterpicnicTable_sphere_%d_%d' % (self.getDoId(), i))
            self.ignore('enterPicnicTableOK_%d_%d' % (self.getDoId(), i))

        for i in range(self.numSeats):
            self.picnicTableSphereNodes[i].setCollideMask(BitMask32(0))        

    
    ##### Off state #####

    def enterOff(self):
        return None

    def exitOff(self):
        return None

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
        #self.clockNode.countdown(self.picnicCountdownTime - ts, self.handleExitButton)
        self.clockNode.countdown(self.picnicCountdownTime, self.handleExitButton)

    def handleExitButton(self):
        # This gets called when the exit button gets pushed.
        self.sendUpdate("requestExit")
        self.clockNode.hide()
        #import pdb; pdb.set_trace()
        
    def exitWaitCountdown(self):
        # Toons may not attempt to board the trolley if it isn't waiting
        self.__disableCollisions()
        self.ignore("trolleyExitButton")
        self.clockNode.reset()

    def getStareAtNodeAndOffset(self):
        return self.tablecloth, Point3(0,0,4)
    
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

    def doneExit(self, avId):
        if(avId == base.localAvatar.getDoId()):
            self.sendUpdate("doneExit")

    def setPosHpr(self, x, y, z, h, p ,r):
        """Set the pos hpr as dictated by the AI."""
        self.startingPos =Vec3(x, y, z)
        self.enteringPos = Vec3(x, y, z-10)
        self.startingHpr =Vec3(h, 0, 0)
        #self.golfKart.setPosHpr( x, y, z, h, 0, 0 )        

    def setTableNumber(self, tn):
        self.tableNumber = tn

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
            def getJumpDest(av = av, node = self.tablecloth):
                dest = Vec3(self.tablecloth.getPos(av.getParent()))
                seatNode = self.picnicTable.find("**/seat" + str(seatIndex + 1))
                dest += seatNode.getPos(self.tablecloth)
                dna = av.getStyle()
                dest -= hipOffset
                if(seatIndex  == 2 or seatIndex == 3):
                    dest.setY( dest.getY() + 2 * hipOffset.getY())
                dest.setZ(dest.getZ() + 0.2)

                return dest

            def getJumpHpr(av = av, node = self.tablecloth):
                hpr = self.seats[seatIndex].getHpr(av.getParent())
                #if(seatIndex < 2):
                #hpr.setX( hpr.getX() + 180)
                #else:
                #    hpr.setX( hpr.getX() )
                angle = PythonUtil.fitDestAngle2Src(av.getH(), hpr.getX())
                hpr.setX(angle)                
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
            Func( av.wrtReparentTo, self.tablecloth ),            
            )
        
        return jumpTrack

    def generateToonReverseJumpTrack( self, av, seatIndex ):
        """Return an interval of the toon jumping out of the golf kart."""        
        self.notify.debug("av.getH() = %s" % av.getH())
        def getToonJumpTrack( av, destNode ):
            # using a local func allows the ProjectileInterval to
            # calculate this pos at run-time
            def getJumpDest(av = av, node = destNode):
                dest = node.getPos(self.tablecloth)
                dest += self.jumpOffsets[seatIndex].getPos(self.tablecloth)
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

        toonJumpTrack = getToonJumpTrack( av, self.tablecloth)
                                          #self.seats[seatIndex])
        jumpTrack = Sequence(
            toonJumpTrack,
            Func( av.loop, 'neutral' ),
            Func( av.wrtReparentTo, render ),
            #Func( self.av.setPosHpr, self.exitMovieNode, 0,0,0,0,0,0 ),
            )
        return jumpTrack

    def generateBasketAppearTrack( self ):
        """
        """
        if(self.basket == None):
            self.basket = loader.loadModel('phase_6/models/golf/picnic_basket.bam')
            
        self.basket.setScale( 0.1 )

        basketTrack = Sequence(
            Func( self.basket.show ),
            SoundInterval(globalBattleSoundCache.getSound('GUI_balloon_popup.mp3'), node=self.basket),
            Func( self.basket.reparentTo, self.tablecloth ),
            Func( self.basket.setPos, 0, 0, .2 ),
            Func( self.basket.setHpr, 45, 0, 0),
            Func( self.basket.wrtReparentTo, render ),
            Func( self.basket.setShear, 0, 0, 0),
            #Func( self.basket.setActiveShadow, True ),
            # Must be a cleaner way to do this.
            Sequence( LerpScaleInterval( self.basket,
                                         scale = Point3( 1.1, 1.1, .1),
                                         duration = 0.2),
                      LerpScaleInterval( self.basket,
                                         scale = Point3(1.6, 1.6, 0.2 ),
                                         duration = 0.1 ),
                      LerpScaleInterval( self.basket,
                                         scale = Point3( 1., 1., 0.4 ),
                                         duration = 0.1 ),
                      LerpScaleInterval( self.basket,
                                         scale = Point3( 1.5, 1.5, 2.5 ),
                                         duration = 0.2 ),
                      LerpScaleInterval( self.basket,
                                         scale = Point3(2.5,2.5, 1.5 ),
                                         duration = 0.1 ),
                      LerpScaleInterval( self.basket,
                                         scale = Point3( 2., 2., 2. ),
                                         duration = 0.1 ),
                      Func( self.basket.wrtReparentTo, self.tablecloth ),
                      Func( self.basket.setPos, 0, 0, 0) ),
            )
        
        return basketTrack


    def generateBasketDisappearTrack(self):
        if not self.basket:
            return Sequence()
        
        pos = self.basket.getPos()
        pos.addZ(-1)

        basketTrack = Sequence(
            LerpScaleInterval( self.basket,
                               scale = Point3( 2., 2., 1.8 ),
                               duration = 0.1 ),
            LerpScaleInterval( self.basket,
                               scale = Point3( 1., 1., 2.5 ),
                               duration = 0.1 ),
            LerpScaleInterval( self.basket,
                               scale = Point3( 2., 2., 0.5 ),
                               duration = 0.2 ),
            LerpScaleInterval( self.basket,
                               scale = Point3( 0.5, 0.5, 1.0 ),
                               duration = 0.1 ),
            LerpScaleInterval( self.basket,
                               scale = Point3( 1.1, 1.1, .1 ),
                               duration = 0.1 ),
            LerpScaleInterval( self.basket,
                               scale = Point3( .1, .1, .1 ),
                               duration = 0.2 ),
            SoundInterval(globalBattleSoundCache.getSound('GUI_balloon_popup.mp3'), node=self.basket),
            Wait( 0.2 ),
            LerpPosInterval( self.basket,
                             pos = pos,
                             duration = 0.2 ),
            Func( self.basket.hide ),
            )
        return basketTrack

    def generateFoodAppearTrack(self, seat):
        """
        """
        if(self.fullSeat[seat] == self.seatState.Full):
            self.notify.debug( "### food appear: self.fullSeat = %s" % self.fullSeat)
            if not self.food[seat]:
                self.food[seat] = loader.loadModel(self.random.choice(self.foodLoader))
                self.notify.debug( "### food appear: self.food = %s" % self.food)
                
            self.food[seat].setScale(0.1)
            self.food[seat].reparentTo(self.tablecloth)
            self.food[seat].setPos(self.seats[seat].getPos(self.tablecloth)[0]/2, self.seats[seat].getPos(self.tablecloth)[1]/2, 0)
            
            # Func( self.food[seat].setActiveShadow, False ),
            foodTrack = Sequence(
                Func( self.food[seat].show ),
                SoundInterval(globalBattleSoundCache.getSound('GUI_balloon_popup.mp3'), node=self.food[seat]),
                Func( self.food[seat].reparentTo, self.tablecloth ),
                Func( self.food[seat].setHpr, 45, 0, 0),
                Func( self.food[seat].wrtReparentTo, render ),
                Func( self.food[seat].setShear, 0, 0, 0),
                #Func( self.food[seat].setActiveShadow, True ),
                # Must be a cleaner way to do this.
                Sequence( LerpScaleInterval( self.food[seat],
                                             scale = Point3( 1.1, 1.1, .1),
                                             duration = 0.2),
                          LerpScaleInterval( self.food[seat],
                                             scale = Point3(1.6, 1.6, 0.2 ),
                                             duration = 0.1 ),
                          LerpScaleInterval( self.food[seat],
                                             scale = Point3( 1., 1., 0.4 ),
                                             duration = 0.1 ),
                          LerpScaleInterval( self.food[seat],
                                             scale = Point3( 1.5, 1.5, 2.5 ),
                                             duration = 0.2 ),
                          LerpScaleInterval( self.food[seat],
                                             scale = Point3(2.5,2.5, 1.5 ),
                                             duration = 0.1 ),
                          LerpScaleInterval( self.food[seat],
                                             scale = Point3( 2., 2., 2. ),
                                             duration = 0.1 ),
                          Func( self.food[seat].wrtReparentTo, self.tablecloth )
                          ),
                )
            return foodTrack
        else:
            return Sequence()

    def generateFoodDisappearTrack(self, seat):
        if not self.food[seat]:
            return Sequence()
        pos = self.food[seat].getPos()
        pos.addZ( -1. )
        foodTrack = Sequence(
            LerpScaleInterval( self.food[seat],
                               scale = Point3( 2., 2., 1.8 ),
                               duration = 0.1 ),
            LerpScaleInterval( self.food[seat],
                               scale = Point3( 1., 1., 2.5 ),
                               duration = 0.1 ),
            LerpScaleInterval( self.food[seat],
                               scale = Point3( 2., 2., 0.5 ),
                               duration = 0.2 ),
            LerpScaleInterval( self.food[seat],
                               scale = Point3( 0.5, 0.5, 1.0 ),
                               duration = 0.1 ),
            LerpScaleInterval( self.food[seat],
                               scale = Point3( 1.1, 1.1, .1 ),
                               duration = 0.1 ),
            LerpScaleInterval( self.food[seat],
                               scale = Point3( .1, .1, .1 ),
                               duration = 0.2 ),
            SoundInterval(globalBattleSoundCache.getSound('GUI_balloon_popup.mp3'), node=self.food[seat]),
            Wait( 0.2 ),
            LerpPosInterval( self.food[seat],
                             pos = pos,
                             duration = 0.2 ),
            Func( self.food[seat].hide ),
            )
        return foodTrack

    def destroy(self, node):
        node.removeNode()
        node = None
        self.basket.removeNode()
        self.basket = None
        for food in self.food:
            food.removeNode()
        self.food = None
        self.clockNode.removeNode()
        del self.clockNode
        self.clockNode = None

    def setPicnicDone(self):
        if self.localToonOnBoard:
            if hasattr(self.loader.place, "trolley"):
                self.loader.place.trolley.fsm.request("final")
                self.loader.place.trolley.fsm.request("start")
            self.localToonOnBoard = 0
            messenger.send("picnicDone")
