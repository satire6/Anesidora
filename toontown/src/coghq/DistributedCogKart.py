import math
from pandac.PandaModules import CollisionSphere, CollisionNode, Vec3, Point3, deg2Rad
from direct.interval.IntervalGlobal import Sequence, Func, Parallel, ActorInterval, Wait, Parallel, LerpHprInterval, ProjectileInterval, LerpPosInterval
from direct.directnotify import DirectNotifyGlobal
from toontown.building import ElevatorConstants
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.safezone import DistributedGolfKart
from toontown.building import DistributedElevatorExt
from toontown.building import ElevatorConstants
from toontown.distributed import DelayDelete
from direct.showbase import PythonUtil
from toontown.building import BoardingGroupShow

class DistributedCogKart(DistributedElevatorExt.DistributedElevatorExt):

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCogKart")
    JumpOutOffsets = ((6.5, -2, -0.025), 
                      (-6.5, -2, -0.025), 
                      (3.75, 5, -0.025), 
                      (-3.75, 5, -0.025))
                      
    def __init__(self, cr):
        """__init__(cr)
        """
        DistributedElevatorExt.DistributedElevatorExt.__init__(self, cr)
        self.type = ElevatorConstants.ELEVATOR_COUNTRY_CLUB
        # note since we did elevator init last, self.fsm is DistributedElevator.fsm
        self.kartModelPath = 'phase_12/models/bossbotHQ/Coggolf_cart3.bam'
        self.leftDoor = None
        self.rightDoor = None
        self.fillSlotTrack = None
        
    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedElevatorExt.DistributedElevatorExt.generate(self)

        # Get the state machine stuff for playGame
        self.loader = self.cr.playGame.hood.loader
        if(self.loader):
            self.notify.debug("Loader has been loaded")
            self.notify.debug(str(self.loader))
        else:
            self.notify.debug("Loader has not been loaded")
        
        self.golfKart = render.attachNewNode('golfKartNode')
        self.kart = loader.loadModel(self.kartModelPath)
        self.kart.setPos(0, 0, 0)
        self.kart.setScale(1)
        self.kart.reparentTo(self.golfKart)
        self.golfKart.reparentTo(self.loader.geom)

        # Wheels
        self.wheels = self.kart.findAllMatches('**/wheelNode*')
        self.numWheels = self.wheels.getNumPaths()      
               

    def announceGenerate(self):
        """Setup other fields dependent on the required fields."""        
        DistributedElevatorExt.DistributedElevatorExt.announceGenerate(self)

        angle = self.startingHpr[0]
        angle -= 90
        radAngle = deg2Rad(angle)
        unitVec = Vec3( math.cos(radAngle), math.sin(radAngle), 0)
        unitVec *= 45.0
        self.endPos =  self.startingPos + unitVec
        self.endPos.setZ(0.5)

        dist = Vec3(self.endPos - self.enteringPos).length()
        wheelAngle = (dist / (4.8 * 1.4 * math.pi)) * 360

        self.kartEnterAnimateInterval = Parallel(
            # start a lerp HPR for each wheel
            LerpHprInterval(self.wheels[0], 5.0, Vec3(self.wheels[0].getH(), wheelAngle, self.wheels[0].getR())),
            LerpHprInterval(self.wheels[1], 5.0, Vec3(self.wheels[1].getH(), wheelAngle, self.wheels[1].getR())),
            LerpHprInterval(self.wheels[2], 5.0, Vec3(self.wheels[2].getH(), wheelAngle, self.wheels[2].getR())),
            LerpHprInterval(self.wheels[3], 5.0, Vec3(self.wheels[3].getH(), wheelAngle, self.wheels[3].getR())),
            name = "CogKartAnimate")

        trolleyExitTrack1 = Parallel(
            LerpPosInterval(self.golfKart, 5.0, self.endPos),
            self.kartEnterAnimateInterval,
            name = "CogKartExitTrack")
        self.trolleyExitTrack = Sequence(
            trolleyExitTrack1,
            # Func(self.hideSittingToons), # we may not need this
            )

        self.trolleyEnterTrack = Sequence(
            LerpPosInterval(self.golfKart, 5.0, self.startingPos, startPos = self.enteringPos))

        self.closeDoors = Sequence(
            self.trolleyExitTrack,
            Func(self.onDoorCloseFinish))
        self.openDoors = Sequence(
            self.trolleyEnterTrack
            )

    def delete(self):
        """
        This method is called when the DistributedObject is permanently
        removed from the world and deleted from the cache.
        """
        DistributedElevatorExt.DistributedElevatorExt.delete(self)
        if hasattr(self, 'elevatorFSM') :
            del self.elevatorFSM

    def setBldgDoId(self, bldgDoId):
        """Handle the AI telling us the associated bldg doid."""
        # The doId is junk, there is no building object for the factory
        # exterior elevators. Do the appropriate things that
        # DistributedElevator.gotBldg does.
        self.bldg = None
        self.setupElevatorKart()

    def setupElevatorKart(self):
        """Setup elevator related fields."""
        # Establish a collision sphere. There must be an easier way!
        collisionRadius = ElevatorConstants.ElevatorData[self.type]['collRadius']
        self.elevatorSphere = CollisionSphere(0, 0, 0, collisionRadius)
        self.elevatorSphere.setTangible(1)
        self.elevatorSphereNode = CollisionNode(self.uniqueName("elevatorSphere"))
        self.elevatorSphereNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
        self.elevatorSphereNode.addSolid(self.elevatorSphere)
        self.elevatorSphereNodePath = self.getElevatorModel().attachNewNode(
            self.elevatorSphereNode)
        self.elevatorSphereNodePath.hide()
        self.elevatorSphereNodePath.reparentTo(self.getElevatorModel())
        self.elevatorSphereNodePath.stash()

        self.boardedAvIds = {}
        self.finishSetup()

    def setColor(self, r, g, b):
        """Ignore this AI message to make it look cog grayish."""
        pass

    def getElevatorModel(self):
        return self.golfKart

    def enterWaitEmpty(self, ts):
        """Handle entering the wait empty state."""
        DistributedElevatorExt.DistributedElevatorExt.enterWaitEmpty(self, ts)

    def exitWaitEmpty(self):
        """Handle exiting the wait empty state."""
        DistributedElevatorExt.DistributedElevatorExt.exitWaitEmpty(self)

    def forceDoorsOpen(self):
        """Deliberately do nothing."""
        pass

    def forceDoorsClosed(self):
        """Deliberately do nothing."""
        pass    
    
    def setPosHpr(self, x, y, z, h, p ,r):
        """Set the pos hpr as dictated by the AI."""
        self.startingPos = Vec3(x, y, z)
        self.enteringPos = Vec3(x, y, z - 10)
        self.startingHpr = Vec3(h, 0, 0)
        self.golfKart.setPosHpr( x, y, z, h, 0, 0 )       

    def enterClosing(self, ts):
        # Close the elevator doors
        if self.localToonOnBoard:
            elevator = self.getPlaceElevator()
            if elevator:
                elevator.fsm.request("elevatorClosing")
        self.closeDoors.start(ts)

    def enterClosed(self, ts):
        self.forceDoorsClosed()
        self.kartDoorsClosed(self.getZoneId())        
        return

    def kartDoorsClosed(self, zoneId):
        assert(self.notify.debug('doorsClosed()'))
        if (self.localToonOnBoard):
            hoodId = ZoneUtil.getHoodId(zoneId)
            doneStatus = {
                'loader' : 'suitInterior',
                'where' : 'suitInterior',
                'hoodId' : hoodId,
                'zoneId' : zoneId,
                'shardId' : None,
                }

            elevator = self.elevatorFSM #self.getPlaceElevator()
            del self.elevatorFSM
            elevator.signalDone(doneStatus)


    def setCountryClubInteriorZone(self, zoneId):
        if (self.localToonOnBoard):
            hoodId = self.cr.playGame.hood.hoodId
            countryClubId = self.countryClubId
            if bboard.has('countryClubIdOverride'):
                countryClubId = bboard.get('countryClubIdOverride')
            doneStatus = {
                'loader' : "cogHQLoader",
                'where'  : "countryClubInterior",
                'how'    : "teleportIn",
                'zoneId' : zoneId,
                'countryClubId' : self.countryClubId,
                'hoodId' : hoodId,
                }
            self.cr.playGame.getPlace().elevator.signalDone(doneStatus)
            
    def setCountryClubInteriorZoneForce(self, zoneId):
        place = self.cr.playGame.getPlace()
        if place:
            place.fsm.request("elevator", [self, 1])            
            hoodId = self.cr.playGame.hood.hoodId
            countryClubId = self.countryClubId
            if bboard.has('countryClubIdOverride'):
                countryClubId = bboard.get('countryClubIdOverride')
            doneStatus = {
                'loader' : "cogHQLoader",
                'where'  : "countryClubInterior",
                'how'    : "teleportIn",
                'zoneId' : zoneId,
                'countryClubId' : self.countryClubId,
                'hoodId' : hoodId,
                }
            if hasattr(place, 'elevator') and place.elevator:
                place.elevator.signalDone(doneStatus)
            else:
                self.notify.warning("setMintInteriorZoneForce: Couldn't find playGame.getPlace().elevator, zoneId: %s" %zoneId)
        else:
            self.notify.warning("setCountryClubInteriorZoneForce: Couldn't find playGame.getPlace(), zoneId: %s" %zoneId)

    def setCountryClubId(self, countryClubId):
        self.countryClubId = countryClubId

    def getZoneId(self):
        return 0
    
    def fillSlot(self, index, avId, wantBoardingShow = 0):
        """Put someone in the kart, as dictated by the AI."""
        self.notify.debug("%s.fillSlot(%s, %s, ... %s)" % (self.doId, index, avId, globalClock.getRealTime()))
        request = self.toonRequests.get(index)
        if request:
            self.cr.relatedObjectMgr.abortRequest(request)
            del self.toonRequests[index]
            
        if avId == 0:
            # This means that the slot is now empty, and no action should
            # be taken.
            pass

        elif not self.cr.doId2do.has_key(avId):
            # It's someone who hasn't been generated yet.
            func = PythonUtil.Functor(
                self.gotToon, index, avId)
                                      
            assert not self.toonRequests.has_key(index)
            self.toonRequests[index] = self.cr.relatedObjectMgr.requestObjects(
                [avId], allCallback = func)

        elif not self.isSetup:
            # We haven't set up the elevator yet.
            self.deferredSlots.append((index, avId, wantBoardingShow))
        
        else:
            # If localToon is boarding, he needs to change state
            if avId == base.localAvatar.getDoId():
                place = base.cr.playGame.getPlace()
                if not place:
                    return
                elevator = self.getPlaceElevator()
                if elevator == None:
                    place.fsm.request('elevator')
                    elevator = self.getPlaceElevator()
                if not elevator:
                    return
                
                self.localToonOnBoard = 1
                
                if hasattr(localAvatar, "boardingParty") and localAvatar.boardingParty:
                    localAvatar.boardingParty.forceCleanupInviteePanel()
                    localAvatar.boardingParty.forceCleanupInviterPanels()
                                
                # Cleanup any leftover elevator messages before boarding the elevator.
                if hasattr(base.localAvatar, "elevatorNotifier"):
                    base.localAvatar.elevatorNotifier.cleanup()
                
                cameraTrack = Sequence()
                # Move the camera towards and face the elevator.
                cameraTrack.append(Func(elevator.fsm.request, "boarding", [self.getElevatorModel()]))
                # Enable the Hop off button.
                cameraTrack.append(Func(elevator.fsm.request, "boarded"))
            
            toon = self.cr.doId2do[avId]
            # Parent it to the elevator
            toon.stopSmooth()
            toon.wrtReparentTo(self.golfKart)

            sitStartDuration = toon.getDuration("sit-start")
            jumpTrack = self.generateToonJumpTrack(toon, index)
            
            track = Sequence(
				jumpTrack,
                Func(toon.setAnimState, "Sit", 1.0),
                Func(self.clearToonTrack, avId),
                name = toon.uniqueName("fillElevator"),
                autoPause = 1)
            
            if wantBoardingShow:
                boardingTrack, boardingTrackType = self.getBoardingTrack(toon, index, True)
                track = Sequence(boardingTrack, track)
                
                if avId == base.localAvatar.getDoId():
                    cameraWaitTime = 2.5
                    if (boardingTrackType == BoardingGroupShow.TRACK_TYPE_RUN):
                        cameraWaitTime = 0.5
                    cameraTrack = Sequence(Wait(cameraWaitTime), cameraTrack)
            
            if self.canHideBoardingQuitBtn(avId):
                track = Sequence(Func(localAvatar.boardingParty.groupPanel.disableQuitButton), 
                                 track)
                                 
            # Start the camera track in parallel here
            if avId == base.localAvatar.getDoId():
                track = Parallel(cameraTrack, track)
            
            track.delayDelete = DelayDelete.DelayDelete(toon, 'CogKart.fillSlot')
            self.storeToonTrack(avId, track)
            track.start()
            
            self.fillSlotTrack = track

            assert avId not in self.boardedAvIds
            self.boardedAvIds[avId] = None
        
    def generateToonJumpTrack(self, av, seatIndex):
        """Return an interval of the toon jumping into the golf kart."""
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
            
            toonJumpTrack = Parallel(ActorInterval( av, 'jump' ),
                                     Sequence(Wait( 0.43 ),
                                              Parallel(LerpHprInterval(av, 
                                                                       hpr = getJumpHpr, 
                                                                       duration = .9 ),
                                                       ProjectileInterval(av,
                                                                          endPos = getJumpDest,
                                                                          duration = .9 ),
                                                      ),          
                                             ),
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
##            Func( av.wrtReparentTo, self.golfKart ),
            )
        
        return jumpTrack


    def emptySlot(self, index, avId, bailFlag, timestamp, timeSent=0):
        """Remove someone as dictated by the AI."""
        if self.fillSlotTrack:
            self.fillSlotTrack.finish()
            self.fillSlotTrack = None
        
        # If localToon is exiting, he needs to change state
        if avId == 0:
            # This means that no one is currently exiting, and no action
            # should be taken
            pass

        elif not self.isSetup:
            # We haven't set up the elevator yet.  Remove the toon
            # from the deferredSlots list, if it is there.
            newSlots = []
            for slot in self.deferredSlots:
                if slot[0] != index:
                    newSlots.append(slot)
                    
            self.deferredSlots = newSlots

        else:
            if self.cr.doId2do.has_key(avId):
                # See if we need to reset the clock
                # (countdown assumes we've created a clockNode already)
                if (bailFlag == 1 and hasattr(self, 'clockNode')):
                    if (timestamp < self.countdownTime and 
                        timestamp >= 0):
                        self.countdown(self.countdownTime - timestamp)
                    else:
                        self.countdown(self.countdownTime)
                # If the toon exists, look it up
                toon = self.cr.doId2do[avId]
                # avoid wrtReparent so that we don't muck with the toon's scale
                # Parent it to render
                #toon.wrtReparentTo(render)
                toon.stopSmooth()

                sitStartDuration = toon.getDuration("sit-start")
                jumpOutTrack = self.generateToonReverseJumpTrack(toon, index)

                # Place it on the appropriate spot relative to the
                # elevator

                track = Sequence(
                    # TODO: Find the right coords for the elevator
                    jumpOutTrack,
                    # Tell the toon he is free to roam now
                    Func(self.notifyToonOffElevator, toon),
                    Func(self.clearToonTrack, avId),
                    name = toon.uniqueName("emptyElevator"),
                    autoPause = 1)
                
                if self.canHideBoardingQuitBtn(avId):
                    # Enable the Boarding Group Panel Quit Button here if it is relevant.
                    track.append(Func(localAvatar.boardingParty.groupPanel.enableQuitButton))
                    # Enable the Boarding Group GO Button here if it is relevant.
                    track.append(Func(localAvatar.boardingParty.enableGoButton))
                
                track.delayDelete = DelayDelete.DelayDelete(toon, 'CogKart.emptySlot')
                self.storeToonTrack(toon.doId, track)
                track.start()

                # Tell localToon he is exiting (if localToon is on board)
                if avId == base.localAvatar.getDoId():
                    messenger.send("exitElevator")

                # if the elevator is generated as a toon is leaving it,
                # we will not have gotten a corresponding 'fillSlot' message
                # for that toon, hence the toon will not be found in
                # boardedAvIds
                if avId in self.boardedAvIds:
                    del self.boardedAvIds[avId]

            else:
                self.notify.warning("toon: " + str(avId) +
                                                  " doesn't exist, and" +
                                                  " cannot exit the elevator!")

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

    def startCountdownClock(self, countdownTime, ts):
        """Start the countdown clock."""
        # just reverse the text counter
        DistributedElevatorExt.DistributedElevatorExt.startCountdownClock(self, countdownTime, ts)
        self.clock.setH(self.clock.getH() + 180)

    def rejectBoard(self, avId, reason = 0):
        """Show the reason why he was rejected."""
        # Only difference from base clase is the use of KartMinLaff
        # This should only be sent to us if our localToon requested
        # permission to board the elevator.
        # reason 0: unknown, 1: shuffle, 2: too low laff, 3: no seat, 4: need promotion        
        print("rejectBoard %s" % (reason))
        if hasattr(base.localAvatar, "elevatorNotifier"):
            if reason == ElevatorConstants.REJECT_SHUFFLE:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.ElevatorHoppedOff)
            elif reason == ElevatorConstants.REJECT_MINLAFF:
                base.localAvatar.elevatorNotifier.showMe((TTLocalizer.KartMinLaff % (self.minLaff)))
            elif reason == ElevatorConstants.REJECT_PROMOTION:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.BossElevatorRejectMessage)
            elif reason == ElevatorConstants.REJECT_NOT_YET_AVAILABLE:
                base.localAvatar.elevatorNotifier.showMe(TTLocalizer.NotYetAvailable)
        assert(base.localAvatar.getDoId() == avId)
        
        doneStatus = {
                'where' : 'reject',
                }
        elevator = self.getPlaceElevator()
        if elevator:
            elevator.signalDone(doneStatus)

    def getDestName(self):
        if self.countryClubId == ToontownGlobals.BossbotCountryClubIntA:
            return TTLocalizer.ElevatorBossBotCourse0
        elif self.countryClubId == ToontownGlobals.BossbotCountryClubIntB:
            return TTLocalizer.ElevatorBossBotCourse1
        elif self.countryClubId == ToontownGlobals.BossbotCountryClubIntC:
            return TTLocalizer.ElevatorBossBotCourse2