from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.task.Task import Task
from otp.otpbase import OTPGlobals
from otp.friends.FriendInfo import FriendInfo
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.uberdog.SpeedchatRelayUD import SpeedchatRelayUD
from otp.uberdog import SpeedchatRelayGlobals
from otp.speedchat import SCDecoders
from toontown.speedchat import TTSCDecoders

class TTSpeedchatRelayUD(SpeedchatRelayUD):

    def __init__(self, air):
        SpeedchatRelayUD.__init__(self, air)

    def setTest(self):
        print ("TTSpeedchatRelayUD TEST!")
        
    def translateMessage(self, messageType, indexArray, senderDISLName):
        message = SpeedchatRelayUD.translateMessage(self, messageType, indexArray, "Bob")
        if message:
            return message
        elif messageType == SpeedchatRelayGlobals.TOONTOWN_QUEST:
            #message = SCDecoders.decodeTTSCToontaskMsg(taskId, toNpcId, toonProgress, msgIndex)
            message = TTSCDecoders.decodeTTSCToontaskMsg(indexArray[0], indexArray[1], indexArray[2], indexArray[3])
            return message
        else:
            return None
                