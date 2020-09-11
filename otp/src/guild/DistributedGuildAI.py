## """
## The Guild AI handles all the guilds accross all shards.
## """

## from otp.ai.AIBaseGlobal import *
## from direct.distributed.ClockDelta import *

## from direct.directnotify import DirectNotifyGlobal
## from direct.distributed import DistributedObjectAI

## class DistributedGuildAI(DistributedObjectAI.DistributedObjectAI):
    ## """
    ## The Guild AI is a global object.

    ## See Also:
        ## "otp/src/configfiles/otp.dc"
        ## "otp/src/guild/DistributedGuild.py"
    ## """
    ## if __debug__:
        ## notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGuildAI')

    ## def __init__(self, air, name, ownerAvatarId):
        ## assert self.notify.debugCall()
        ## DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        ## self.name=name
        ## self.dateCreated=0
        ## self.ownerAvatarId=ownerAvatarId
        ## self.guildStatus=0
        ## self.reputations={}
        ## self.memberListId=0
        ## self.memberApplicationListId=0

    ## def delete(self):
        ## assert self.notify.debugCall()
        ## self.ignoreAll()
        ## DistributedObjectAI.DistributedObjectAI.delete(self)
  
    ## def getName(self):
        ## return self.name
  
    ## def getDateCreated(self):
        ## return self.dateCreated

    ## def getOwnerAvatarId(self):
        ## """
        ## return the avatar doId for the avatar that
        ## created/owns this guild.
        ## """
        ## return self.ownerAvatarId
        
    ## def getGuldStatus(self):
        ## return self.guildStatus
        
    ## def getReputations(self):
        ## return self.reputations
    
    ## def getMemberListId(self):
        ## return self.memberListId
        
    ## def getMemberApplicationListId(self):
        ## return self.memberApplicationListId
