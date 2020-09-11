
from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *

from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
from toontown.building import DistributedDoorAI
from direct.fsm import State
from toontown.toonbase import ToontownGlobals
import CogDisguiseGlobals
from toontown.building import FADoorCodes
from toontown.building import DoorTypes
from toontown.toonbase import ToontownAccessAI

class DistributedCogHQDoorAI(DistributedDoorAI.DistributedDoorAI):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCogHQDoorAI')
    #notify.setDebug(True)
    def __init__(self, air, blockNumber, doorType, destinationZone, doorIndex=0,
                 lockValue=FADoorCodes.SB_DISGUISE_INCOMPLETE, swing=3):
        assert(self.notify.debug("__init__: dest:%s, doorIndex:%d)" %
                                 (destinationZone, doorIndex)))
        DistributedDoorAI.DistributedDoorAI.__init__(self, air, blockNumber, doorType, doorIndex, lockValue, swing)
        self.destinationZone = destinationZone

    def requestEnter(self):
        avatarID = self.air.getAvatarIdFromSender()
        assert(self.notify.debug("requestEnter: avatarID:%s" % avatarID))
        # Ext cog hq doors require all cog disguise parts
        # does the toon have a complete cog disguise?
        dept = ToontownGlobals.cogHQZoneId2deptIndex(self.destinationZone)
        av = self.air.doId2do.get(avatarID)
        if av:
            if self.doorType == DoorTypes.EXT_COGHQ and self.isLockedDoor():
                parts = av.getCogParts()
                if CogDisguiseGlobals.isSuitComplete(parts, dept):
                    allowed = 1
                else:
                    allowed = 0
            # Interior doors allow all
            else:
                allowed = 1
                
        # Check that player has full access
        if not ToontownAccessAI.canAccess(avatarID, self.zoneId):
            allowed = 0
                
        # Now send a message back - either reject or accept
        if not allowed:
            self.sendReject(avatarID, self.isLockedDoor())
        else:
            self.enqueueAvatarIdEnter(avatarID)
            self.sendUpdateToAvatarId(avatarID, "setOtherZoneIdAndDoId",
                                      [self.destinationZone, self.otherDoor.getDoId()])

    def requestExit(self):
        assert(self.debugPrint("requestExit()"))
        avatarID = self.air.getAvatarIdFromSender()
        assert(self.notify.debug("  avatarID:%s" % (str(avatarID),)))
        
        if self.avatarsWhoAreEntering.has_key(avatarID):
            del self.avatarsWhoAreEntering[avatarID]

        if not self.avatarsWhoAreExiting.has_key(avatarID):
            dept = ToontownGlobals.cogHQZoneId2deptIndex(self.destinationZone)
            self.avatarsWhoAreExiting[avatarID]=1
            self.sendUpdate("avatarExit", [avatarID])
            self.openDoor(self.exitDoorFSM) 

            # currently, there are no coghq doors that are unlocked and still
            # put us our cog suit.  Therefore, if we're not locked, we
            # don't need to update the suit.
            # We use .lockedDoor instead of .isDoorLocked() because we don't
            # want to check the 'no-locked-doors' flag
            if self.lockedDoor:
                av = self.air.doId2do[avatarID]
                if self.doorType == DoorTypes.EXT_COGHQ:
                    av.b_setCogIndex(-1)
                else:
                    av.b_setCogIndex(dept)
        else:
            assert(self.notify.debug(str(avatarID)
                    +" requested an exit, and they're already exiting"))
