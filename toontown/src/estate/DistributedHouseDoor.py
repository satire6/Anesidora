""" DistributedHouseDoor module: contains the DistributedHouseDoor
    class, the client side representation of a 'landmark door'."""

from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObject
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.MessengerGlobal import messenger
from direct.fsm import ClassicFSM
from toontown.building import DistributedDoor
from toontown.hood import ZoneUtil
from toontown.suit import Suit
from toontown.building import FADoorCodes
from toontown.building import DoorTypes

class DistributedHouseDoor(DistributedDoor.DistributedDoor):
    """
    DistributedHouseDoor class: a slightly different version
    of DistributedDoor that gets its 'building' info by waiting
    for a message from the AI that tells it the doId of the
    house that owns it.
    """

    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHouseDoor')

    def __init__(self, cr):
        """constructor for the DistributedHouseDoor"""
        DistributedDoor.DistributedDoor.__init__(self, cr)

    def disable(self):
        """
        This method is called when the DistributedObject
        is removed from active duty and stored in a cache.
        """
        DistributedDoor.DistributedDoor.disable(self)
        self.ignoreAll()

        
    def setZoneIdAndBlock(self, zoneId, block):
        # We override DistributedDoor's function so we can also set the houseId to the block
        self.houseId = block
        DistributedDoor.DistributedDoor.setZoneIdAndBlock(self, zoneId, block)
        

    def getTriggerName(self):
        # HQ doors need to have an index appended, since they are
        # the only type of door that supports multiple doors on a building.
        # Only built ins can have door indices > 0.
        #assert(self.doorIndex == 0)
        return ("door_trigger_" + str(self.houseId))

    def hideDoorParts(self):
        return

    def announceGenerate(self):
        assert(self.notify.debug("announceGenerate"))
        # note we are skipping DistributedDoor.announceGenerate as
        # it assumes the building is already loaded in
        DistributedObject.DistributedObject.announceGenerate(self)
        if self.doorType == DoorTypes.EXT_STANDARD:
            house = base.cr.doId2do.get(self.houseId)
            if house and house.house_loaded:
                self.__gotRelatedHouse()
            else:
                self.acceptOnce("houseLoaded-%d" % self.houseId, self.__gotRelatedHouse)
        elif self.doorType == DoorTypes.INT_STANDARD:
            # wish there was a better way to test if houseInterior has already called setup
            door=render.find("**/leftDoor;+s")
            if door.isEmpty():
                self.acceptOnce("houseInteriorLoaded-%d" % self.zoneId, self.__gotRelatedHouse)
            else:
                self.__gotRelatedHouse()

    def __gotRelatedHouse(self):
        """Handle the callback that we have the related house."""
        # this used to be done in DistributedDoor.announceGenerate
        # and DistributedHouseDoor.announceGenerate
        self.doPostAnnounceGenerate() # in DistributedDoor
        
        # This is called when the door is completely created, so we know
        # that we have all the info we need to get a proper trigger event.

        # Tiki house does not have flat
        self.bHasFlat = not self.findDoorNode("door*flat", True).isEmpty()

        # Hide doors parts if necessary
        self.hideDoorParts()

        # Find the door trigger poly, and give it the proper name if necessary
        self.setTriggerName()

        # Accept a hit on the door trigger
        self.accept(self.getEnterTriggerEvent(), self.doorTrigger)
        self.acceptOnce("clearOutToonInterior", self.doorTrigger)

        self.zoneDoneLoading = 0
        

    def getBuilding(self, allowEmpty=False):
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
            elif self.doorType == DoorTypes.EXT_STANDARD:
                if self.houseId:
                    self.building = self.cr.playGame.hood.loader.houseId2house.get(self.houseId, None)

        if allowEmpty:
            return self.building
                    
        assert(not self.building.isEmpty())
        return self.building

    def isInterior(self):
        if (self.doorType == DoorTypes.INT_STANDARD):
            return 1
        return 0
                
    def getDoorNodePath(self):
        assert(self.debugPrint("getDoorNodePath()"))
        if self.doorType == DoorTypes.INT_STANDARD:
            # ...interior door.
            assert(self.debugPrint("getDoorNodePath() -- isInterior"))
            otherNP=render.find("**/door_origin")
            assert(not otherNP.isEmpty())
        elif self.doorType == DoorTypes.EXT_STANDARD:
            building = self.getBuilding()
            otherNP = building.find("**/door")
            if otherNP.isEmpty():
                otherNP = building.find("**/door_origin")
            assert(not otherNP.isEmpty())
        else:
            self.notify.error("No such door type as " + str(self.doorType))
                
        return otherNP
        
    def enterClosing(self, ts):
        assert(self.debugPrint("enterClosing()"))
        # Start animation:
        #building=self.getBuilding()
        # The right hole (aka doorway):
        #doorFrameHoleRight=building.find("**/doorFrameHoleRight;+s")
        doorFrameHoleRight=self.findDoorNode("doorFrameHoleRight")
        if (doorFrameHoleRight.isEmpty()):
            self.notify.warning("enterClosing(): did not find doorFrameHoleRight")
            return
        
        # Right door:
        #rightDoor=building.find("rightDoor")
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
            assert(self.debugPrint("exiting the estate, to a house"))
            base.cr.playGame.hood.loader.setHouse(self.houseId)
            zoneId=self.otherZoneId
            if self.doorType == DoorTypes.EXT_STANDARD:
                whereTo = "house"
            else:
                whereTo = "estate"
            # We must set allowRedirect to 0 because we expect to meet
            # our other door on the other side.
            request={
                    #"loader": "estateLoader" ,
                    "loader": "safeZoneLoader" ,
                    "where": whereTo,
                    "how": "doorIn",
                    "hoodId": ToontownGlobals.MyEstate,
                    "zoneId": zoneId,
                    "shardId": None,
                    "avId": -1,
                    "allowRedirect" : 0,
                    "doorDoId":self.otherDoId}
            messenger.send("doorDoneEvent", [request])

    if __debug__:
        def debugPrint(self, message):
            """for debugging""" 
            type=self.__dict__.get('doorType', '?')
            if type == DoorTypes.INT_STANDARD:
                type="INT_ST"
            elif type == DoorTypes.EXT_STANDARD:
                type="EXT_ST"
            return self.notify.debug(
                    str(self.__dict__.get('houseId', '?'))+' '+type+' '+message)
