from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.task.Task import Task
from otp.otpbase import OTPGlobals
from otp.friends.FriendInfo import FriendInfo
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed import OtpDoGlobals
from otp.uberdog import SpeedchatRelayGlobals
from otp.speedchat import SCDecoders

class SpeedchatRelayUD(DistributedObjectGlobalUD):
    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        
    def forwardSpeedchat(self, receiverDISLid,  messageType, indexArray, senderDISLId, senderDISLName, flags):
        senderAvId = self.air.getAvatarIdFromSender()
        
        message = self.translateMessage(messageType, indexArray, senderDISLName)
        if not message:
            return
            
        fieldName = "setTalkAccount"
        parameters = [receiverDISLid, senderDISLId, senderDISLName, message, [], flags]
        pfmID = OtpDoGlobals.OTP_DO_ID_PLAYER_FRIENDS_MANAGER
        dg = self.dclass.aiFormatUpdate(fieldName, pfmID, pfmID, pfmID, parameters)
        self.air.sendDatagram(dg)

        
    def translateMessage(self, messageType, indexArray, senderDISLName):
        if messageType == SpeedchatRelayGlobals.NORMAL:
            return SCDecoders.decodeSCStaticTextMsg(indexArray[0])
        elif messageType == SpeedchatRelayGlobals.CUSTOM:
            return SCDecoders.decodeSCCustomMsg(indexArray[0])
        elif messageType == SpeedchatRelayGlobals.EMOTE:
            return SCDecoders.decodeSCEmoteWhisperMsg(indexArray[0], senderDISLName)
        else:
            return None
        
        
    def sendUpdateToAvatarIdFromDOID(self, avId, fieldName, args):
        channelId = self.GetPuppetConnectionChannel(avId)
        self.sendUpdateToChannelFromDOID(channelId, fieldName, args)
        
    def sendUpdateToChannelFromDOID(self, channelId, fieldName, args):
        self.air.sendUpdateToChannelFrom(self, channelId, fieldName,self.doId, args)
        