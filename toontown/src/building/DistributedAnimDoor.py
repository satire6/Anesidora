""" DistributedAnimDoor module: contains the DistributedAnimDoor
    class, the client side representation of a 'animated landmark door'."""

from pandac.PandaModules import NodePath, VBase3
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import  Parallel, Sequence, Wait, \
     HprInterval, LerpHprInterval, SoundInterval
from toontown.building import DistributedDoor
from toontown.building import DoorTypes

if( __debug__ ):
    import pdb

class DistributedAnimDoor(DistributedDoor.DistributedDoor):   
    """
    DistributedAnimDoor class:  The client side representation of a
    animated 'landmark door'.
    Too much stuff has changed to put them in DistributedDoor.py
    """

    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAnimDoor')
        #notify.setDebug(True)

    def __init__(self, cr):
        """constructor for the DistributedDoor"""
        DistributedDoor.DistributedDoor.__init__(self, cr)
        # WARNING debug only
        base.animDoor = self

    def getBuilding(self):
        """Return only a nodepath to our parent building.
        See also getAnimBuilding.
        """
        if (not self.__dict__.has_key('building')):
            if self.doorType == DoorTypes.EXT_ANIM_STANDARD:
                searchStr = "**/??"+str(self.block)+":animated_building_*_DNARoot;+s"
                self.notify.debug("searchStr=%s" % searchStr)
                self.building = self.cr.playGame.hood.loader.geom.find(searchStr)
            else:
                self.notify.error("DistributedAnimDoor.getBuiding with doorType=%s"% self.doorType)

        assert(not self.building.isEmpty())
        return self.building       
   
    def getDoorNodePath(self):
        """Return the nodepath to door origin."""
        if self.doorType == DoorTypes.EXT_ANIM_STANDARD:
            if hasattr(self, "tempDoorNodePath"):
                return self.tempDoorNodePath
            else:
                # tempDoorNodePath gets removed in disable
                # ...exterior door.                
                assert(self.debugPrint("getDoorNodePath() -- exterior"))
                building = self.getBuilding()
                doorNP = building.find("**/door_origin")
                self.notify.debug("creating doorOrigin at %s %s" % (str(doorNP.getPos()),
                                                                   str(doorNP.getHpr())))
                otherNP=NodePath("doorOrigin")
                otherNP.setPos(doorNP.getPos())
                otherNP.setHpr(doorNP.getHpr()) #
                otherNP.reparentTo(doorNP.getParent())
                assert(not otherNP.isEmpty())                
                # Store this for clean up later
                self.tempDoorNodePath=otherNP                
        else:
            self.notify.error("DistributedAnimDoor.getDoorNodePath with doorType=%s"% self.doorType)
        return otherNP

    def setTriggerName(self):
        """Find and rename the collision trigger."""
        if self.doorType == DoorTypes.EXT_ANIM_STANDARD:
            building = self.getBuilding()
            if not building.isEmpty():
                doorTrigger = building.find("**/door_0_door_trigger")
                if not doorTrigger.isEmpty():
                    doorTrigger.node().setName(self.getTriggerName())
                else:
                    # we could have already set it
                    pass
            else:
                self.notify.warning("setTriggerName failed no building")
        else:
            self.notify.error("setTriggerName doorTYpe=%s" % self.doorType)

    def getAnimBuilding(self):
        """Return a handle on the animated building prop."""
        # Once we find it, we store it, so we don't have to find it again.
        if (not self.__dict__.has_key('animBuilding')):            
            if self.doorType == DoorTypes.EXT_ANIM_STANDARD:
                #self.building = self.cr.playGame.hood.loader.geom.find(
                #        "**/??"+str(self.block)+":animated_building_*_DNARoot;+s")
                bldg= self.getBuilding()
                key = bldg.getParent().getParent()
                animPropList = self.cr.playGame.hood.loader.animPropDict.get(key)
                
                if animPropList:
                    for prop in animPropList:
                        # TODO string matching is such a hack, maybe test paths?
                        if bldg ==  prop.getActor().getParent():
                            self.animBuilding = prop
                            break
                else:
                    self.notify.error("could not find" + str(key))
            else:
                self.notify.error("No such door type as " + str(self.doorType))

        assert(not self.animBuilding.getActor().isEmpty())
        return self.animBuilding

    def getBuildingActor(self):
        """Return the animated building actor."""
        result = self.getAnimBuilding().getActor()
        return result

    ##### opening state #####
    def enterOpening(self, ts):
        #if( __debug__ ):
        #    import pdb
        #    pdb.set_trace()
        assert(self.debugPrint("enterOpening()"))

        # Right door:
        bldgActor = self.getBuildingActor()
        rightDoor = bldgActor.controlJoint(None, "modelRoot", "def_right_door")
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
                    #other=otherNP,
                    ),
                Wait(0.4),
                #Func(rightDoor.show),
                #Func(doorFrameHoleRight.show),
                LerpHprInterval(
                    nodePath=rightDoor,
                    duration=0.6,
                    hpr=VBase3(h, 0, 0),
                    startHpr=VBase3(0, 0, 0),
                    #other=otherNP,
                    blendType="easeInOut")),
            name = trackName)
        # Start the tracks:
        self.doorTrack.start(ts)

    ##### closing state #####

    def enterClosing(self, ts):
        assert(self.debugPrint("enterClosing()"))
        # Right door:
        bldgActor = self.getBuildingActor()
        rightDoor = bldgActor.controlJoint(None, "modelRoot", "def_right_door")
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
                    #other=otherNP,
                    blendType="easeInOut"),
                #Func(doorFrameHoleRight.hide),
                #Func(self.hideIfHasFlat, rightDoor),
                SoundInterval(self.closeSfx, node=rightDoor),
                name = trackName)
        self.doorTrack.start(ts)
        if hasattr(self, "done"):
            request = self.getRequestStatus()
            messenger.send("doorDoneEvent", [request])

    ##### Exit Door opening state #####

    def exitDoorEnterOpening(self, ts):
        assert(self.debugPrint("exitDoorEnterOpening()"))
        bldgActor = self.getBuildingActor()
        leftDoor = bldgActor.controlJoint(None, "modelRoot", "def_left_door")
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
                    #Func(leftDoor.show),
                    #Func(doorFrameHoleLeft.show),
                    LerpHprInterval(nodePath=leftDoor,
                                    duration=0.6,
                                    hpr=VBase3(h, 0, 0),
                                    startHpr=VBase3(0, 0, 0),
                                    #other=otherNP,
                                    blendType="easeInOut")),
                name = trackName)
            # Start the tracks:
            self.doorExitTrack.start(ts)
        else:
            self.notify.warning("exitDoorEnterOpening(): did not find leftDoor")

    ##### Exit Door closing state #####
    
    def exitDoorEnterClosing(self, ts):
        assert(self.debugPrint("exitDoorEnterClosing()"))
        # Start animation:

        bldgActor = self.getBuildingActor()
        leftDoor = bldgActor.controlJoint(None, "modelRoot", "def_left_door")

        #if ZoneUtil.isInterior(self.zoneId):
        #    doorFrameHoleLeft.setColor(1., 1., 1., 1.)
        # Left door:
        if self.leftSwing:
            h = -100
        else:
            h = 100

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
                        #other=otherNP,
                        blendType="easeInOut"),
                    #Func(doorFrameHoleLeft.hide),
                    #Func(self.hideIfHasFlat, leftDoor),
                    SoundInterval(self.closeSfx, node=leftDoor),
                    name = trackName)
            self.doorExitTrack.start(ts)
        #else:
        #    self.notify.error("enterOpening(): did not find leftDoor")
    
