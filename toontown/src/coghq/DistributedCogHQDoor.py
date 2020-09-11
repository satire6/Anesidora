
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *

from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from toontown.building import DistributedDoor
from toontown.hood import ZoneUtil
from toontown.building import FADoorCodes
from toontown.building import DoorTypes
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TeaserPanel

class DistributedCogHQDoor(DistributedDoor.DistributedDoor):

    def __init__(self, cr):
        """constructor for the DistributedDoor"""
        DistributedDoor.DistributedDoor.__init__(self, cr)
        # We have our own sfx
        self.openSfx = base.loadSfx("phase_9/audio/sfx/CHQ_door_open.mp3")
        self.closeSfx = base.loadSfx("phase_9/audio/sfx/CHQ_door_close.mp3")

    def wantsNametag(self):
        """ return true if this door needs an arrow pointing to it. """
        return 0

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
        
    # HACK: the only reason we are overwriting this entire function is to
    # change the timing on the closeSfx. Perhaps there is a more elegant
    # way to handle this
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
        self.finishDoorTrack()            
        self.doorTrack=Parallel(Sequence(LerpHprInterval(nodePath=rightDoor,
                                                         duration=1.0,
                                                         hpr=VBase3(0, 0, 0),
                                                         startHpr=VBase3(h, 0, 0),
                                                         other=otherNP,
                                                         blendType="easeInOut"),
                                         Func(doorFrameHoleRight.hide),
                                         Func(self.hideIfHasFlat, rightDoor),
                                         ),
                                Sequence(Wait(0.5),
                                         SoundInterval(self.closeSfx, node=rightDoor),
                                         ),
                                name = trackName)
        self.doorTrack.start(ts)
        if hasattr(self, "done"):
            request = self.getRequestStatus()
            messenger.send("doorDoneEvent", [request])
    
    # HACK: the only reason we are overwriting this entire function is to
    # change the timing on the closeSfx. Perhaps there is a more elegant
    # way to handle this
    def exitDoorEnterClosing(self, ts):
        assert(self.debugPrint("exitDoorEnterClosing()"))
        # Start animation:
        # The left hole doorway:
        doorFrameHoleLeft=self.findDoorNode("doorFrameHoleLeft")
        if (doorFrameHoleLeft.isEmpty()):
            self.notify.warning("enterOpening(): did not find flatDoors")
            return

        if ZoneUtil.isInterior(self.zoneId):
            doorFrameHoleLeft.setColor(1., 1., 1., 1.)
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
            self.doorExitTrack = Parallel(Sequence(LerpHprInterval(nodePath=leftDoor,
                                                                   duration=1.0,
                                                                   hpr=VBase3(0, 0, 0),
                                                                   startHpr=VBase3(h, 0, 0),
                                                                   other=otherNP,
                                                                   blendType="easeInOut"),
                                                   Func(doorFrameHoleLeft.hide),
                                                   Func(self.hideIfHasFlat, leftDoor),
                                                   ),
                                          Sequence(Wait(0.5),
                                                   SoundInterval(self.closeSfx, node=leftDoor),
                                                   ),
                                          name = trackName)
            self.doorExitTrack.start(ts)
        #else:
        #    self.notify.error("enterOpening(): did not find leftDoor")


    def setZoneIdAndBlock(self, zoneId, block):
        assert(self.notify.debug("setZoneIdAndBlock(zoneId="+str(zoneId)
                                 +", block="+str(block)+") for doId=" + str(self.doId)))
        self.zoneId=zoneId
        self.block=block

        # special checking for narrower bossbot cog hq doors
        canonicalZoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        if canonicalZoneId in (ToontownGlobals.BossbotHQ,
                               ToontownGlobals.BossbotLobby):
            self.doorX = 1.0
        

    def enterDoor(self):
        assert(self.debugPrint("enterDoor()"))
        if self.allowedToEnter():
            messenger.send("DistributedDoor_doorTrigger")
            self.sendUpdate("requestEnter") # calls back with a avatarEnter.
        else:
            place = base.cr.playGame.getPlace()
            if place:
                place.fsm.request('stopped')
            self.dialog = TeaserPanel.TeaserPanel(pageName='cogHQ',
                                                  doneFunc=self.handleOkTeaser)
                                                  
    def doorTrigger(self, args=None):
        # The local avatar cannot leave the zone if he is part of a boarding group.
        if localAvatar.hasActiveBoardingGroup():
            rejectText = TTLocalizer.BoardingCannotLeaveZone
            localAvatar.boardingParty.showMe(rejectText)
            return
        DistributedDoor.DistributedDoor.doorTrigger(self, args)