from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.uberdog.SpeedchatRelay import SpeedchatRelay
from otp.uberdog import SpeedchatRelayGlobals


class TTSpeedchatRelay(SpeedchatRelay):

    def __init__(self, cr):
        SpeedchatRelay.__init__(self, cr)
        
    def sendSpeedchatToonTask(self, receiverId, taskId, toNpcId, toonProgress, msgIndex):
        #self.sendUpdate("forwardSpeedchat", [receiverId, SpeedchatRelayGlobals.PIRATES_QUEST, [questInt, msgType, taskNum], base.cr.accountDetailRecord.playerAccountId, base.cr.accountDetailRecord.playerName + " PHD"])
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.TOONTOWN_QUEST, [taskId, toNpcId, toonProgress, msgIndex])
        #import pdb; pdb.set_trace()
        


                