## """
## The Guild AI handles all the guilds accross all districts.
## """

## from otp.ai.AIBaseGlobal import *
## from direct.distributed.ClockDelta import *

## from direct.directnotify import DirectNotifyGlobal
## from direct.distributed import DistributedObjectAI
## from otp.guild import DistributedGuildBase
## from otp.guild import DistributedGuildAI

## class DistributedGuildManagerAI(DistributedObjectAI.DistributedObjectAI):
    ## """
    ## The Guild AI is a global object.
    ## See Also:
        ## "otp/src/guild/DistributedGuildBase.py"
        ## "otp/src/guild/DistributedGuildManager.py"
        ## "otp/src/configfiles/otp.dc"
    ## """
    ## if __debug__:
        ## notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGuildManagerAI')

    ## def __init__(self, air):
        ## assert self.notify.debugCall()
        ## DistributedObjectAI.DistributedObjectAI.__init__(self, air)

        ## # doId to guild object:
        ## self.guilds={}

    ## def delete(self):
        ## assert self.notify.debugCall()
        ## self.ignoreAll()
        ## DistributedObjectAI.DistributedObjectAI.delete(self)

    ## def sendReject(self, avatarId, reasonId):
        ## assert self.notify.debugCall()
        ## self.sendUpdateToAvatarId(avatarId, "rejectCreate", [reasonId])

    ## def requestCreate(self, newGuildName):
        ## avatarId = self.air.getAvatarIdFromSender()
        ## assert self.notify.debugCall("avatarId:%s" % (str(avatarId),))
        ## #assert avatarId in self.air.doId2do
        ## # we don't have avtar info! avatar = self.air.doId2do[avatarId]
        ## if 0 and     not avatar.may("createGuild"):
            ## # ...this avatar does not have permission to create a guild:
            ## self.sendReject(avatarId, DistributedGuildBase.MAY_NOT_CREATE_GUILD)
        ## elif 0 and     not avatar.has("guild"):
            ## # ...this avatar already has a guild:
            ## self.sendReject(avatarId, DistributedGuildBase.ALREADY_HAS_GUILD)
        ## elif 0 and      guildNameUsed(newGuildName):
            ## # ...this guild name is taken:
            ## self.sendReject(avatarId, DistributedGuildBase.GUILD_NAME_TAKEN)
        ## else:
            ## # ...ready to create:
            ## guild = DistributedGuildAI.DistributedGuildAI(
                    ## self.air, newGuildName, avatarId)
            ## guild.generateOtpObject(self.getDoId(), avatarId)
            ## self.guilds[guild.getDoId()]=guild
