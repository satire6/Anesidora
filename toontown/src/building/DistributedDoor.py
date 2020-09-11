""" DistributedDoor module: contains the DistributedDoor
    class, the client side representation of a 'landmark door'."""

from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *

from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.distributed import DistributedObject
from toontown.hood import ZoneUtil
from toontown.suit import Suit
from toontown.distributed import DelayDelete
import FADoorCodes
from direct.task.Task import Task
import DoorTypes
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TeaserPanel
from toontown.distributed.DelayDeletable import DelayDeletable

if( __debug__ ):
    import pdb

class DistributedDoor(DistributedObject.DistributedObject, DelayDeletable):
    """
    DistributedDoor class:  The client side representation of a
    'landmark door'.  Each of these doors can also be 'entered' by bad
    guys and toons.  This object has to worry about updating
    the display of the door and all of its components on the client's
    machine.   This object also has a server side representation
    of it, DistributedDoorAI.
    """

    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDoor')
        #notify.setDebug(True)

    def __init__(self, cr):
        """constructor for the DistributedDoor"""
        DistributedObject.DistributedObject.__init__(self, cr)

        self.openSfx = base.loadSfx("phase_3.5/audio/sfx/Door_Open_1.mp3")
        self.closeSfx = base.loadSfx("phase_3.5/audio/sfx/Door_Close_1.mp3")

        # When we get enough information about the door, we can set up
        # its nametag.  The nametag points out nearby buildings to the
        # player.
        self.nametag = None

        assert(self.notify.debug("__init__()"))
        self.fsm = ClassicFSM.ClassicFSM('DistributedDoor_right',
                           [State.State('off',
                                        self.enterOff,
                                        self.exitOff,
                                        ['closing',
                                        'closed',
                                        'opening',
                                        'open']),
                            State.State('closing',
                                        self.enterClosing,
                                        self.exitClosing,
                                        ['closed', 'opening']),
                            State.State('closed',
                                        self.enterClosed,
                                        self.exitClosed,
                                        ['opening']),
                            State.State('opening',
                                        self.enterOpening,
                                        self.exitOpening,
                                        ['open']),
                            State.State('open',
                                        self.enterOpen,
                                        self.exitOpen,
                                        ['closing', 'open'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                          )
        self.fsm.enterInitialState()
        self.exitDoorFSM = ClassicFSM.ClassicFSM('DistributedDoor_left',
                           [State.State('off',
                                        self.exitDoorEnterOff,
                                        self.exitDoorExitOff,
                                        ['closing',
                                        'closed',
                                        'opening',
                                        'open']),
                            State.State('closing',
                                        self.exitDoorEnterClosing,
                                        self.exitDoorExitClosing,
                                        ['closed', 'opening']),
                            State.State('closed',
                                        self.exitDoorEnterClosed,
                                        self.exitDoorExitClosed,
                                        ['opening']),
                            State.State('opening',
                                        self.exitDoorEnterOpening,
                                        self.exitDoorExitOpening,
                                        ['open']),
                            State.State('open',
                                        self.exitDoorEnterOpen,
                                        self.exitDoorExitOpen,
                                        ['closing', 'open'])],
                           # Initial State
                           'off',
                           # Final State
                           'off',
                          )
        self.exitDoorFSM.enterInitialState()
        # self.generate will be called automatically.

        self.specialDoorTypes = { DoorTypes.EXT_HQ:0, DoorTypes.EXT_COGHQ:0, DoorTypes.INT_COGHQ:0, DoorTypes.EXT_KS:0, DoorTypes.INT_KS:0  }

        # bossbot door is narrower and will override this
        self.doorX = 1.5

    def generate(self):
        """
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert(self.debugPrint("generate()"))
        DistributedObject.DistributedObject.generate(self)
        self.avatarTracks=[]
        self.avatarExitTracks=[]
        self.avatarIDList=[]
        self.avatarExitIDList=[]
        self.doorTrack=None
        self.doorExitTrack=None

    def disable(self):
        assert(self.debugPrint("disable()"))

        self.clearNametag()
        
        # Go to the off state when the object is put in the cache
        taskMgr.remove(self.checkIsDoorHitTaskName())
        self.ignore(self.getEnterTriggerEvent())
        self.ignore(self.getExitTriggerEvent())
        self.ignore("clearOutToonInterior")
        self.fsm.request("off")
        self.exitDoorFSM.request("off")
        if self.__dict__.has_key('building'):
            del self.building

        # Clean up a little more gracefully; we might get a disable
        # message at any time.
        self.finishAllTracks()
        self.avatarIDList = []
        self.avatarExitIDList = []

        if hasattr(self, "tempDoorNodePath"):
            self.tempDoorNodePath.removeNode()
            del self.tempDoorNodePath
        DistributedObject.DistributedObject.disable(self)
        # self.delete() will automatically be called.
    
    def delete(self):
        assert(self.debugPrint("delete()"))
        del self.fsm
        del self.exitDoorFSM
        del self.openSfx
        del self.closeSfx
        DistributedObject.DistributedObject.delete(self)

    def wantsNametag(self):
        """ return true if this door needs an arrow pointing to it. """
        # We don't create nametags for interior doors.
        return not ZoneUtil.isInterior(self.zoneId)

    def setupNametag(self):
        assert(self.debugPrint("setupNametag()"))
        if not self.wantsNametag():
            return
        if self.nametag == None:
            self.nametag = NametagGroup()
            self.nametag.setFont(ToontownGlobals.getBuildingNametagFont())
            if TTLocalizer.BuildingNametagShadow:
                self.nametag.setShadow(*TTLocalizer.BuildingNametagShadow)
            self.nametag.setContents(Nametag.CName)
            self.nametag.setColorCode(NametagGroup.CCToonBuilding)
            self.nametag.setActive(0)
            self.nametag.setAvatar(self.getDoorNodePath())
            # Since some buildings have multiple doors for the same
            # building, we'll apply a uniquifying code so the
            # building doesn't appear to have multiple nametags.
            # Only the nearest door will be tagged.
            self.nametag.setObjectCode(self.block)
            name = self.cr.playGame.dnaStore.getTitleFromBlockNumber(self.block)
            self.nametag.setName(name)
            self.nametag.manage(base.marginManager)

    def clearNametag(self):
        assert(self.debugPrint("clearNametag()"))
        if self.nametag != None:
            self.nametag.unmanage(base.marginManager)
            self.nametag.setAvatar(NodePath())
            self.nametag = None

    def getTriggerName(self):
        # HQ doors (toon, cog, and kartshop) need to have an index appended, since they are
        # the only type of door that supports multiple doors on a building.
        if (self.doorType == DoorTypes.INT_HQ or
            self.specialDoorTypes.has_key(self.doorType) ):
            return ("door_trigger_" + str(self.block) + "_" +
                    str(self.doorIndex))
        else:
            # Only built ins can have door indices > 0.
            assert(self.doorIndex == 0)
            return ("door_trigger_" + str(self.block))

    def getTriggerName_wip(self):
        ####if ZoneUtil.tutorialDict:
        ####    return "door_trigger_%d" % (self.block, )
        #name="door_trigger_%d_%d" % (self.block, self.doorIndex)
        name="door_trigger_%d" % (self.doId, )
        assert(self.debugPrint("getTriggerName()  returning \"%s\""%(name, )))
        return name

    def getEnterTriggerEvent(self):
        return "enter" + self.getTriggerName()

    def getExitTriggerEvent(self):
        return "exit" + self.getTriggerName()

    def hideDoorParts(self):
        if (self.specialDoorTypes.has_key(self.doorType)):
            # This work gets done by the DNA in non HQ buildings.
            self.hideIfHasFlat(self.findDoorNode("rightDoor"))
            self.hideIfHasFlat(self.findDoorNode("leftDoor"))
            self.findDoorNode("doorFrameHoleRight").hide()
            self.findDoorNode("doorFrameHoleLeft").hide()
        else:
            return

    def setTriggerName(self):
        # This may seem strange, but it is an optimization. Buildings with
        # just one door will already have the right name applied to the
        # trigger poly (door_trigger_<blockNumber>). This was done by
        # dnaDoor.cxx.  So if the doorIndex
        # is None, we do nothing. Buildings with more than one door will
        # have the wrong name applied to the trigger poly
        # (door_trigger_<doorIndex>), so we have to find it, and change it
        # to (door_trigger_<blockNumber>_<doorIndex>).
        if (self.specialDoorTypes.has_key(self.doorType)):
            building = self.getBuilding()            
            doorTrigger = building.find("**/door_" + str(self.doorIndex) +
                                        "/**/door_trigger*")
            doorTrigger.node().setName(self.getTriggerName())
        else:
            return

    def setTriggerName_wip(self):
        building = self.getBuilding()
        doorTrigger = building.find("**/door_%d/**/door_trigger_%d"%(self.doorIndex, self.block))
        if doorTrigger.isEmpty():
            doorTrigger = building.find("**/door_trigger_%d"%(self.block, ))
        if doorTrigger.isEmpty():
            doorTrigger = building.find("**/door_%d/**/door_trigger_*"%(self.doorIndex,))
        if doorTrigger.isEmpty():
            doorTrigger = building.find("**/door_trigger_*")
        assert(not doorTrigger.isEmpty())
        doorTrigger.node().setName(self.getTriggerName())
            
    def setZoneIdAndBlock(self, zoneId, block):
        assert(self.notify.debug("setZoneIdAndBlock(zoneId="+str(zoneId)
                                 +", block="+str(block)+") for doId=" + str(self.doId)))
        self.zoneId=zoneId
        self.block=block

    def setDoorType(self, doorType):
        self.notify.debug("Door type = " + str(doorType) +
                          " on door #" + str(self.doId))
        self.doorType = doorType

    def setDoorIndex(self, doorIndex):
        assert(self.notify.debug("Door index = " + str(doorIndex) +
                                 " on door #" + str(self.doId)))
        self.doorIndex = doorIndex
    
    def setSwing(self, flags):
        """
        false: swings inward, true: the door swings outward.
        bit 1 is the left door, bit 2 is the right door:
        """
        self.leftSwing=(flags&1)!=0
        self.rightSwing=(flags&2)!=0
    
    def setOtherZoneIdAndDoId(self, zoneId, distributedObjectID):
        assert(self.debugPrint("setOtherZoneIdAndDoId(zoneId=" 
               +str(zoneId)+", distributedObjectID="+str(distributedObjectID)+")"))
        self.otherZoneId=zoneId
        self.otherDoId=distributedObjectID
    
    def setState(self, state, timestamp):
        assert(self.debugPrint("setState(%s, %d)" % (state, timestamp)))
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])
    
    def setExitDoorState(self, state, timestamp):
        assert(self.debugPrint("setExitDoorState(%s, %d)" % (state, timestamp)))
        self.exitDoorFSM.request(state,
                             [globalClockDelta.localElapsedTime(timestamp)])

    def announceGenerate(self):
        # This is called when the door is completely created, so we know
        # that we have all the info we need to get a proper trigger event.
        DistributedObject.DistributedObject.announceGenerate(self)
        self.doPostAnnounceGenerate()

    def doPostAnnounceGenerate(self):
        """Setup needed stuff after we have an announceGenerate."""

        # determine if this door has a flat or not
        if self.doorType == DoorTypes.INT_STANDARD:
            self.bHasFlat = True
        else:
            self.bHasFlat = not self.findDoorNode("door*flat", True).isEmpty()

        # Hide doors parts if necessary
        self.hideDoorParts()

        # Find the door trigger poly, and give it the proper name if necessary
        self.setTriggerName()

        # Accept a hit on the door trigger
        self.accept(self.getEnterTriggerEvent(), self.doorTrigger)
        self.acceptOnce("clearOutToonInterior", self.doorTrigger)

        # Set up the door nametag
        self.setupNametag()

    def getBuilding(self):
        # Once we find it, we store it, so we don't have to find it again.        
        if (not self.__dict__.has_key('building')):
            if self.doorType == DoorTypes.INT_STANDARD:
                #if ZoneUtil.isInterior(self.zoneId):
                # building interior.
                # Hack: assume that the node above the door is the building:
                door=render.find("**/leftDoor;+s")
                assert(not door.isEmpty())
                # Cut the door off of the nodePath to get the building:
                self.building = door.getParent()
            elif (self.doorType == DoorTypes.INT_HQ):
                # I know this is a hackful way to find the building node,
                # but it works.
                door=render.find("**/door_0")
                self.building = door.getParent()
            elif (self.doorType == DoorTypes.INT_KS):
                # I know this is a hackful way to find the building node,
                # but it works.
                # NOTE - separate to keep exterior kartshop index to match
                #        with interior index. (jjtaylor - 06/24/05)
                self.building=render.find("**/KartShop_Interior*")
            elif ((self.doorType == DoorTypes.EXT_STANDARD) or
                  (self.doorType == DoorTypes.EXT_HQ) or
                  (self.doorType == DoorTypes.EXT_KS)):
                # street or playground.
                self.building=self.cr.playGame.hood.loader.geom.find(
                        "**/??"+str(self.block)+":*_landmark_*_DNARoot;+s")
                if self.building.isEmpty(): # [gjeon] for animated buildlngs
                    self.building = self.cr.playGame.hood.loader.geom.find(
                        "**/??"+str(self.block)+":animated_building_*_DNARoot;+s")
            elif ((self.doorType == DoorTypes.EXT_COGHQ) or
                  (self.doorType == DoorTypes.INT_COGHQ)):
                self.building=self.cr.playGame.hood.loader.geom
            else:
                self.notify.error("No such door type as " + str(self.doorType))

        assert(not self.building.isEmpty())
        return self.building
        
    def getBuilding_wip(self):
        # Once we find it, we store it, so we don't have to find it again.
        if (not self.__dict__.has_key('building')):
            if self.__dict__.has_key('block'):
                self.building=self.cr.playGame.hood.loader.geom.find(
                    "**/??"+str(self.block)+":*_landmark_*_DNARoot;+s")
            else:
                self.building=self.cr.playGame.hood.loader.geom
                print "---------------- door is interior -------"

            #if ZoneUtil.isInterior(self.zoneId):
            #    self.building=self.cr.playGame.hood.loader.geom
            #    #self.building=render
            #    print "---------------- door is interior -------"
            #else:
            #    self.building=self.cr.playGame.hood.loader.geom.find(
            #        "**/??"+str(self.block)+":*_landmark_*_DNARoot;+s")

            # building interior.
            # Hack: assume that the node above the door is the building:
            #door=render.find("**/leftDoor;+s")
            #assert(not door.isEmpty())
            # Cut the door off of the nodePath to get the building:
            #self.building = door.getParent()
            #if (self.doorType == DoorTypes.INT_STANDARD or
            #    self.doorType == DoorTypes.INT_HQ):
            #    # I know this is a hackful way to find the building node,
            #    # but it works.
            #    door=render.find("**/door_0")
            #    self.building = door.getParent()
            #elif ((self.doorType == DoorTypes.EXT_STANDARD) or
            #      (self.doorType == DoorTypes.EXT_HQ)):
            #    # street or playground.
            #    self.building=self.cr.playGame.hood.loader.geom.find(
            #            "**/??"+str(self.block)+":*_landmark_*_DNARoot;+s")
            #else:
            #    self.notify.error("No such door type as " + str(self.doorType))
        assert(not self.building.isEmpty())
        return self.building

    def readyToExit(self):
        assert(self.debugPrint("readyToExit()"))
        base.transitions.fadeScreen(1.0)
        # Ask permission to exit:
        self.sendUpdate("requestExit")

    def avatarEnterDoorTrack(self, avatar, duration):
        trackName = "avatarEnterDoor-%d-%d" % (self.doId, avatar.doId)
        track = Parallel(name = trackName)
        otherNP=self.getDoorNodePath()

        if hasattr(avatar, "stopSmooth"):
            avatar.stopSmooth()

        # Move the camera:
        if avatar.doId == base.localAvatar.doId:
            # Move the camera behind the toon:
            track.append(
                LerpPosHprInterval(nodePath=camera,
                                   other=avatar,
                                   duration=duration,
                                   pos=Point3(0, -8, avatar.getHeight()),
                                   hpr=VBase3(0, 0, 0),
                                   blendType="easeInOut")
                )

        finalPos = avatar.getParent().getRelativePoint(
            otherNP, Point3(self.doorX,2,ToontownGlobals.FloorOffset))

        # Move the avatar:
        moveHere = Sequence(
            self.getAnimStateInterval(avatar, 'walk'),
            LerpPosInterval(nodePath=avatar,
                            duration=duration,
                            pos=finalPos,
                            blendType="easeIn")
            )
        track.append(moveHere)
        
        # iris:
        if (avatar.doId == base.localAvatar.doId):
            track.append(Sequence(
                Wait(duration*0.5),
                Func(base.transitions.irisOut, duration*0.5),
                Wait(duration*0.5),
                Func(avatar.b_setParent, ToontownGlobals.SPHidden),
                ))

        # Prevent the avatar from being deleted:
        track.delayDelete = DelayDelete.DelayDelete(avatar, 'avatarEnterDoorTrack')
        return track

    def avatarEnqueueTrack(self, avatar, duration):
        if hasattr(avatar, "stopSmooth"):
            avatar.stopSmooth()
        # Move the avatar:
        back=-5.-(2.*len(self.avatarIDList))
        if back<-9.:
            back=-9.
        offset=Point3(self.doorX, back, ToontownGlobals.FloorOffset)
        otherNP=self.getDoorNodePath()
        walkLike= ActorInterval(
            avatar, 'walk', 
            startTime=1, duration=duration, 
            endTime=0.0001
            )
        standHere = Sequence(
            LerpPosHprInterval(
                nodePath=avatar,
                other=otherNP,
                duration=duration,
                pos=offset,
                hpr=VBase3(0,0,0), # hpr will come from otherNP.
                blendType="easeInOut"),
            self.getAnimStateInterval(avatar, 'neutral'),
            )
        # Create the track:
        trackName = "avatarEnqueueDoor-%d-%d" % (self.doId, avatar.doId)
        track = Parallel(walkLike, standHere, name = trackName)
        track.delayDelete = DelayDelete.DelayDelete(avatar, 'avatarEnqueueTrack')
        return track

    def getAnimStateInterval(self, avatar, animName):
        """
        returns a FunctionInterval that sets the indicated animation
        playing on the avatar, however that should be accomplished.
        Unfortunately, this is slightly different for Suits and Toons.
        """
        isSuit = isinstance(avatar, Suit.Suit)
        if isSuit:
            return Func(avatar.loop, animName, 0)
        else:
            return Func(avatar.setAnimState, animName)
    
    def isDoorHit(self):
        """
        We're checking the angle of attack from the avatar to the
        door.  This is to reduce that, "I got sucked into a door" 
        effect.
        """
        #assert(self.spamPrint("isDoorHit()"))
        vec=base.localAvatar.getRelativeVector(
                self.currentDoorNp,
                self.currentDoorVec)
        netScale = self.currentDoorNp.getNetTransform().getScale()
        # the door in bossbot has been scaled down, account for that
        yToTest = vec.getY() / netScale[1]
        assert(self.debugPrint("  door dot: % .04f" % (vec.getY())))
        # return true if the avatar is +-60 degrees of looking at the door:
        return yToTest < -0.5

    def enterDoor(self):
        assert(self.debugPrint("enterDoor()"))
        if self.allowedToEnter():
            messenger.send("DistributedDoor_doorTrigger")
            self.sendUpdate("requestEnter") # calls back with a avatarEnter.
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='otherHoods',
                                                  doneFunc=self.handleOkTeaser)
        
    def handleOkTeaser(self):
        """Handle the user clicking ok on the teaser panel."""
        self.accept(self.getEnterTriggerEvent(), self.doorTrigger)
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')
        

    def allowedToEnter(self):
        """Check if the local toon is allowed to enter."""
        if base.cr.isPaid():
            return True
        place = base.cr.playGame.getPlace()
        myHoodId = ZoneUtil.getCanonicalHoodId(place.zoneId)
        # if we're in the estate we should use place.id
        if hasattr(place, 'id'):
            myHoodId = place.id
        if  myHoodId in \
           (ToontownGlobals.ToontownCentral,
            ToontownGlobals.MyEstate,
            ToontownGlobals.GoofySpeedway,
            ToontownGlobals.Tutorial,
            ):
            # trialer going to TTC/Estate/Goofy Speedway, let them through
            return True
        return False
        

    def checkIsDoorHitTaskName(self):
        return 'checkIsDoorHit'+self.getTriggerName()
    
    def checkIsDoorHitTask(self, task):
        """
        Check to see if the avatar has turned to face the door that
        they are already colliding with.
        """
        #assert(self.spamPrint("checkIsDoorHitTask()"))
        if (self.isDoorHit()):
            self.ignore(self.checkIsDoorHitTaskName())
            self.ignore(self.getExitTriggerEvent())
            self.enterDoor()
            return Task.done
        return Task.cont
    
    def cancelCheckIsDoorHitTask(self, args):
        """
        Stop waiting to see if the avatar is going to turn to face the
        door.  Instead go back to the default mode of waiting for the
        avatar to hit the door at all.
        """
        taskMgr.remove(self.checkIsDoorHitTaskName())
        del self.currentDoorNp
        del self.currentDoorVec
        self.ignore(self.getExitTriggerEvent())
        self.accept(self.getEnterTriggerEvent(), self.doorTrigger)

    def doorTrigger(self, args=None):
        """Call doorTrigger when the avatar first collides with the door."""
        assert(self.debugPrint("doorTrigger(args="+str(args)+")"))
        self.ignore(self.getEnterTriggerEvent())
        if (args==None):
            # ...we want the trigger to work when the
            # clearOutToonInterior is sent.
            self.enterDoor()
        else:
            self.currentDoorNp=NodePath(args.getIntoNodePath())
            self.currentDoorVec=Vec3(args.getSurfaceNormal(self.currentDoorNp))
            if (self.isDoorHit()):
                self.enterDoor()
            else:
                # ...the door was hit by the side or back of the toon.
                # Start a task to see if the avatar turns to face the door:
                self.accept(self.getExitTriggerEvent(), self.cancelCheckIsDoorHitTask)
                taskMgr.add(self.checkIsDoorHitTask, self.checkIsDoorHitTaskName())
    
    def avatarEnter(self, avatarID):
        """Server approves Toon or cog to enter door queue"""
        assert(self.debugPrint("avatarEnter(avatarID="+str(avatarID)+")"))
        avatar = self.cr.doId2do.get(avatarID, None)
        if avatar:
            avatar.setAnimState('neutral')
            track=self.avatarEnqueueTrack(avatar, 0.5)
            track.start()
            self.avatarTracks.append(track)
            self.avatarIDList.append(avatarID)

    def rejectEnter(self, reason):
        assert(self.debugPrint("rejectEnter()"))
        message = FADoorCodes.reasonDict[reason]
        if message:
            self.__faRejectEnter(message)
        else:
            self.__basicRejectEnter()
    
    def __basicRejectEnter(self):
        """Server doesn't let the avatar in the door queue, but
        there's no reason we can tell the user."""
        assert(self.debugPrint("basicRejectEnter()"))
        # Hang the hook again
        self.accept(self.getEnterTriggerEvent(), self.doorTrigger)
        # Go back into walk mode.
        if self.cr.playGame.getPlace():
            self.cr.playGame.getPlace().setState('walk')

    def __faRejectEnter(self, message):
        assert(self.debugPrint("faRejectEnter()"))
        self.rejectDialog = TTDialog.TTGlobalDialog(
            message = message,
            doneEvent = "doorRejectAck",
            style = TTDialog.Acknowledge)
        self.rejectDialog.show()
        self.rejectDialog.delayDelete = DelayDelete.DelayDelete(self, '__faRejectEnter')

        event = 'clientCleanup'
        self.acceptOnce(event, self.__handleClientCleanup)
        
        # Make the toon stand still.
        base.cr.playGame.getPlace().setState('stopped')
        # Hang a hook for hitting OK
        self.acceptOnce("doorRejectAck", self.__handleRejectAck)
        self.acceptOnce("stoppedAsleep", self.__handleFallAsleepDoor)

    def __handleClientCleanup(self):
        """Handle the user closing the toontown window when the reject dialog is up."""
        if hasattr(self,'rejectDialog') and self.rejectDialog:
            self.rejectDialog.doneStatus = 'ok'
        self.__handleRejectAck()        

    def __handleFallAsleepDoor(self):
        # it's 'ok' to fall asleep  =]
        self.rejectDialog.doneStatus = 'ok'
        self.__handleRejectAck()
        
    def __handleRejectAck(self):
        self.ignore("doorRejectAck")
        self.ignore("stoppedAsleep")
        self.ignore('clientCleanup')
        doneStatus = self.rejectDialog.doneStatus
        if doneStatus != "ok":
            self.notify.error("Unrecognized doneStatus: " +
                              str(doneStatus))
        self.__basicRejectEnter()
        self.rejectDialog.delayDelete.destroy()
        self.rejectDialog.cleanup()
        del self.rejectDialog

    def getDoorNodePath(self):
        assert(self.debugPrint("getDoorNodePath()"))
        if self.doorType == DoorTypes.INT_STANDARD:
            # ...interior door.
            assert(self.debugPrint("getDoorNodePath() -- isInterior"))
            otherNP=render.find("**/door_origin")
            assert(not otherNP.isEmpty())
        elif self.doorType == DoorTypes.EXT_STANDARD:
            if hasattr(self, "tempDoorNodePath"):
                return self.tempDoorNodePath
            else:
                # ...exterior door.
                assert(self.debugPrint("getDoorNodePath() -- exterior"))
                posHpr=self.cr.playGame.dnaStore.getDoorPosHprFromBlockNumber(self.block)
                # This will be used as a relative node, even though
                # it is not attached to render.
                otherNP=NodePath("doorOrigin")
                otherNP.setPos(posHpr.getPos())
                otherNP.setHpr(posHpr.getHpr())
                # Store this for clean up later
                self.tempDoorNodePath=otherNP
        elif (self.specialDoorTypes.has_key(self.doorType)):
            building = self.getBuilding()
            otherNP = building.find("**/door_origin_" + str(self.doorIndex))
            assert(not otherNP.isEmpty())
        elif (self.doorType == DoorTypes.INT_HQ):
            otherNP=render.find("**/door_origin_" + str(self.doorIndex))
            assert(not otherNP.isEmpty())
        else:
            self.notify.error("No such door type as " + str(self.doorType))
                
        return otherNP
    
    def avatarExitTrack(self, avatar, duration):
        assert(self.debugPrint("avatarExitTrack(avatar="+str(avatar)
                +", duration="+str(duration)+")"))
        if hasattr(avatar, "stopSmooth"):
            avatar.stopSmooth()
        # Get the pos and hpr of the door origin:
        otherNP=self.getDoorNodePath()

        trackName = "avatarExitDoor-%d-%d" % (self.doId, avatar.doId)
        track = Sequence(name = trackName)

        # Put the avatar in the doorway:
        track.append(self.getAnimStateInterval(avatar, 'walk'))
        track.append(PosHprInterval(
            avatar,
            Point3(-self.doorX, 0, ToontownGlobals.FloorOffset),
            VBase3(179, 0, 0),
            other=otherNP))
        track.append(Func(avatar.setParent, ToontownGlobals.SPRender))
                     
        if avatar.doId==base.localAvatar.doId:
            # Position the camera:
            track.append(PosHprInterval(
                camera,
                VBase3(-self.doorX, 5, avatar.getHeight()),
                VBase3(180, 0, 0),
                other=otherNP
                ))

        # Move the avatar through:
        if (avatar.doId == base.localAvatar.doId):
            finalPos = render.getRelativePoint(
                otherNP, Point3(-self.doorX, -6, ToontownGlobals.FloorOffset))
        else:
            finalPos = render.getRelativePoint(
                otherNP, Point3(-self.doorX, -3, ToontownGlobals.FloorOffset))
            
        track.append(LerpPosInterval(
            nodePath=avatar,
            duration=duration,
            pos=finalPos,
            blendType="easeInOut"))

        if (avatar.doId == base.localAvatar.doId):
            # Cleanup localToon:
            track.append(Func(self.exitCompleted))
            # iris in:
            track.append(Func(base.transitions.irisIn))

        if hasattr(avatar, "startSmooth"):
            track.append(Func(avatar.startSmooth))
        
        track.delayDelete = DelayDelete.DelayDelete(avatar, 'DistributedDoor.avatarExitTrack')
        return track
    
    def exitCompleted(self):
        assert(self.notify.debug('exitCompleted()'))
        base.localAvatar.setAnimState('neutral')
        place = self.cr.playGame.getPlace()
        if place:
            place.setState('walk')

        # This is just to ensure the distributed parent gets set properly.
        base.localAvatar.d_setParent(ToontownGlobals.SPRender)

    def avatarExit(self, avatarID):
        assert(self.debugPrint("avatarExit(avatarID="+str(avatarID)+")"))
        # Animate the avatar
        if (avatarID in self.avatarIDList):
            # ...this avatar was waiting to go in, and bailed out.
            assert(self.notify.debug("  bailed out"))
            self.avatarIDList.remove(avatarID)
            if (avatarID == base.localAvatar.doId):
                self.exitCompleted()
        else:
            # ...this avatar just went through the out door.
            assert(self.notify.debug("  regular exit"))
            self.avatarExitIDList.append(avatarID)
        
    def finishDoorTrack(self):
        if self.doorTrack:
            self.doorTrack.finish()
        self.doorTrack=None
        
    def finishDoorExitTrack(self):
        if self.doorExitTrack:
            self.doorExitTrack.finish()
        self.doorExitTrack=None

    def finishAllTracks(self):
        self.finishDoorTrack()
        self.finishDoorExitTrack()

        for t in self.avatarTracks:
            t.finish()
            DelayDelete.cleanupDelayDeletes(t)
        self.avatarTracks = []

        for t in self.avatarExitTracks:
            t.finish()
            DelayDelete.cleanupDelayDeletes(t)
        self.avatarExitTracks = []

    ##### off state #####
    
    def enterOff(self):
        assert(self.debugPrint("enterOff()"))
    
    def exitOff(self):
        assert(self.debugPrint("exitOff()"))
    
    ##### closing state #####

    def getRequestStatus(self):
        zoneId=self.otherZoneId
        # We must set allowRedirect to 0 because we expect to meet
        # our other door on the other side.
        request={
                "loader": ZoneUtil.getBranchLoaderName(zoneId),
                "where": ZoneUtil.getToonWhereName(zoneId),
                "how": "doorIn",
                "hoodId": ZoneUtil.getHoodId(zoneId),
                "zoneId": zoneId,
                "shardId": None,
                "avId": -1,
                "allowRedirect" : 0,
                "doorDoId":self.otherDoId
                }
        return request        
    
    def enterClosing(self, ts):
        assert(self.debugPrint("enterClosing()"))
        # Start animation:
        # The right hole doorway:
        doorFrameHoleRight=self.findDoorNode("doorFrameHoleRight")
        if (doorFrameHoleRight.isEmpty()):
            self.notify.warning("enterClosing(): did not find doorFrameHoleRight")
            return

        # Hmmm, you can try setting the door color to something else
        # other than black.  I tried white, but that doesn't look to
        # good either.
        #if ZoneUtil.isInterior(self.zoneId):
        #    doorFrameHoleRight.setColor(1., 1., 1., 1.)
        
        # Right door:
        rightDoor=self.findDoorNode("rightDoor")
        if (rightDoor.isEmpty()):
            self.notify.warning("enterClosing(): did not find rightDoor")
            return
        
        # Close the door:
        otherNP=self.getDoorNodePath()
        trackName = "doorClose-%d" % (self.doId)
        if self.rightSwing:
            h = 100
        else:
            h = -100
        # Stop animation:
        self.finishDoorTrack()
        self.doorTrack=Sequence(
                LerpHprInterval(
                    nodePath=rightDoor,
                    duration=1.0,
                    hpr=VBase3(0, 0, 0),
                    startHpr=VBase3(h, 0, 0),
                    other=otherNP,
                    blendType="easeInOut"),
                Func(doorFrameHoleRight.hide),
                Func(self.hideIfHasFlat, rightDoor),
                SoundInterval(self.closeSfx, node=rightDoor),
                name = trackName)
        self.doorTrack.start(ts)
        if hasattr(self, "done"):
            request = self.getRequestStatus()
            messenger.send("doorDoneEvent", [request])
    
    def exitClosing(self):
        assert(self.debugPrint("exitClosing()"))
    
    ##### closed state #####
    
    def enterClosed(self, ts):
        assert(self.debugPrint("enterClosed()"))
    
    def exitClosed(self):
        assert(self.debugPrint("exitClosed()"))
    
    ##### opening state #####
    
    def enterOpening(self, ts):
        #if( __debug__ ):
        #    import pdb
        #    pdb.set_trace()
        assert(self.debugPrint("enterOpening()"))
        # Start animation:
        # The right doorway:
        doorFrameHoleRight=self.findDoorNode("doorFrameHoleRight")
        if (doorFrameHoleRight.isEmpty()):
            self.notify.warning("enterOpening(): did not find doorFrameHoleRight")
            return

        # Hmmm, you can try setting the door color to something else
        # other than black.  I tried white, but that doesn't look to
        # good either.
        #if ZoneUtil.isInterior(self.zoneId):
        #    doorFrameHoleRight.setColor(1., 1., 1., 1.)

        # Right door:
        rightDoor=self.findDoorNode("rightDoor")
        if (rightDoor.isEmpty()):
            self.notify.warning("enterOpening(): did not find rightDoor")
            return
        # Open the door:
        otherNP=self.getDoorNodePath()
        trackName = "doorOpen-%d" % (self.doId)
        if self.rightSwing:
            h = 100
        else:
            h = -100
        # Stop animation:
        self.finishDoorTrack()
        self.doorTrack=Parallel(
            SoundInterval(self.openSfx, node=rightDoor),
            Sequence(
                HprInterval(
                    rightDoor,
                    VBase3(0, 0, 0),
                    other=otherNP,
                    ),
                Wait(0.4),
                Func(rightDoor.show),
                Func(doorFrameHoleRight.show),
                LerpHprInterval(
                    nodePath=rightDoor,
                    duration=0.6,
                    hpr=VBase3(h, 0, 0),
                    startHpr=VBase3(0, 0, 0),
                    other=otherNP,
                    blendType="easeInOut")),
            name = trackName)
        # Start the tracks:
        self.doorTrack.start(ts)
    
    def exitOpening(self):
        assert(self.debugPrint("exitOpening()"))
    
    ##### open state #####
    
    def enterOpen(self, ts):
        assert(self.debugPrint("enterOpen()"))
        # Run everybody in:
        for avatarID in self.avatarIDList:
            assert(self.notify.debug("  avatarID: "+str(avatarID)))
            avatar = self.cr.doId2do.get(avatarID)
            if avatar:
                track=self.avatarEnterDoorTrack(avatar, 1.0)
                track.start(ts)
                self.avatarTracks.append(track)
            if (avatarID == base.localAvatar.doId):
                self.done=1
        self.avatarIDList=[]
    
    def exitOpen(self):
        assert(self.debugPrint("exitOpen()"))
        for track in self.avatarTracks:
            track.finish()
            DelayDelete.cleanupDelayDeletes(track)
        self.avatarTracks=[]
    
    ##### Exit Door off state #####
    
    def exitDoorEnterOff(self):
        assert(self.debugPrint("exitDoorEnterOff()"))
    
    def exitDoorExitOff(self):
        assert(self.debugPrint("exitDoorExitOff()"))
    
    ##### Exit Door closing state #####
    
    def exitDoorEnterClosing(self, ts):
        assert(self.debugPrint("exitDoorEnterClosing()"))
        # Start animation:
        # The left hole doorway:
        doorFrameHoleLeft=self.findDoorNode("doorFrameHoleLeft")
        if (doorFrameHoleLeft.isEmpty()):
            self.notify.warning("enterOpening(): did not find flatDoors")
            return

        #if ZoneUtil.isInterior(self.zoneId):
        #    doorFrameHoleLeft.setColor(1., 1., 1., 1.)
        # Left door:
        if self.leftSwing:
            h = -100
        else:
            h = 100
        leftDoor=self.findDoorNode("leftDoor")
        if (not leftDoor.isEmpty()):
            # Close the door:
            otherNP=self.getDoorNodePath()
            trackName = "doorExitTrack-%d" % (self.doId)
            self.finishDoorExitTrack()
            self.doorExitTrack = Sequence(
                    LerpHprInterval(
                        nodePath=leftDoor,
                        duration=1.0,
                        hpr=VBase3(0, 0, 0),
                        startHpr=VBase3(h, 0, 0),
                        other=otherNP,
                        blendType="easeInOut"),
                    Func(doorFrameHoleLeft.hide),
                    Func(self.hideIfHasFlat, leftDoor),
                    SoundInterval(self.closeSfx, node=leftDoor),
                    name = trackName)
            self.doorExitTrack.start(ts)
        #else:
        #    self.notify.error("enterOpening(): did not find leftDoor")
    
    def exitDoorExitClosing(self):
        assert(self.debugPrint("exitDoorExitClosing()"))
    
    ##### Exit Door closed state #####
    
    def exitDoorEnterClosed(self, ts):
        assert(self.debugPrint("exitDoorEnterClosed()"))
    
    def exitDoorExitClosed(self):
        assert(self.debugPrint("exitDoorExitClosed()"))
    
    ##### Exit Door opening state #####
    
    def exitDoorEnterOpening(self, ts):
        assert(self.debugPrint("exitDoorEnterOpening()"))
        # Start animation:
        # The left hole doorway:
        doorFrameHoleLeft=self.findDoorNode("doorFrameHoleLeft")
        if (doorFrameHoleLeft.isEmpty()):
            self.notify.warning("enterOpening(): did not find flatDoors")
            return

        #if ZoneUtil.isInterior(self.zoneId):
        #    doorFrameHoleLeft.setColor(1., 1., 1., 1.)
        # Left door:
        leftDoor=self.findDoorNode("leftDoor")
        if self.leftSwing:
            h = -100
        else:
            h = 100        
        if (not leftDoor.isEmpty()):
            # Open the door:
            otherNP=self.getDoorNodePath()
            trackName = "doorDoorExitTrack-%d" % (self.doId)
            self.finishDoorExitTrack()
            self.doorExitTrack = Parallel(
                SoundInterval(self.openSfx, node=leftDoor),
                Sequence(
                    Func(leftDoor.show),
                    Func(doorFrameHoleLeft.show),
                    LerpHprInterval(nodePath=leftDoor,
                                    duration=0.6,
                                    hpr=VBase3(h, 0, 0),
                                    startHpr=VBase3(0, 0, 0),
                                    other=otherNP,
                                    blendType="easeInOut")),
                name = trackName)
            # Start the tracks:
            self.doorExitTrack.start(ts)
        else:
            self.notify.warning("exitDoorEnterOpening(): did not find leftDoor")
    
    def exitDoorExitOpening(self):
        assert(self.debugPrint("exitDoorExitOpening()"))
    
    ##### Exit Door open state #####
    
    def exitDoorEnterOpen(self, ts):
        assert(self.debugPrint("exitDoorEnterOpen()"))
        # Run everybody out:
        for avatarID in self.avatarExitIDList:
            assert(self.notify.debug("  avatarID: "+str(avatarID)))
            avatar=self.cr.doId2do.get(avatarID)
            if avatar:
                track=self.avatarExitTrack(avatar, 0.2)
                track.start()
                self.avatarExitTracks.append(track)
        self.avatarExitIDList=[]
    
    def exitDoorExitOpen(self):
        assert(self.debugPrint("exitDoorExitOpen()"))
        for track in self.avatarExitTracks:
            track.finish()
            DelayDelete.cleanupDelayDeletes(track)
        self.avatarExitTracks=[]
    
    def findDoorNode(self, string, allowEmpty = False):
        building = self.getBuilding()
        if not building:
            self.notify.warning("getBuilding() returned None, avoiding crash, remark 896029")
            foundNode = None
        else:
            foundNode = building.find("**/door_" + str(self.doorIndex) +
                                      "/**/" + string + "*;+s+i")
            if foundNode.isEmpty():
                # hack, We should make the trigger finding more general.
                foundNode = building.find("**/" + string + "*;+s+i")
                assert(self.debugPrint("    fyi: find door hack"))
        assert(self.debugPrint("findDoorNode(%s) found %s, %d"%(string, foundNode, self.doorIndex)))
        if allowEmpty:
            return foundNode
        assert(not foundNode.isEmpty())
        return foundNode

    def hideIfHasFlat(self, node):
        if self.bHasFlat:
            node.hide()
            
    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            block=self.__dict__.get('block', '?')
            type=self.__dict__.get('doorType', '?')
            index=self.__dict__.get('doorIndex', '?')
            if type == DoorTypes.INT_HQ:
                type="INT_HQ"
            elif type == DoorTypes.EXT_HQ:
                type="EXT_HQ"
            elif type == DoorTypes.INT_STANDARD:
                type="INT_ST"
            elif type == DoorTypes.EXT_STANDARD:
                type="EXT_ST"
            elif type == DoorTypes.EXT_COGHQ:
                type="EXT_COGHQ"
            elif type == DoorTypes.INT_COGHQ:
                type="INT_COGHQ"
            elif( type == DoorTypes.EXT_KS ):
                type="EXT_KS"
            elif( type == DoorTypes.INT_KS ):
                type="INT_KS"
            return self.notify.debug("%s %s %s %s" %
                    (block, type, index, message))
