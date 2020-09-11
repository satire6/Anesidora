## """
## The Guild AI handles all the guilds accross all shards.
## """

## from otp.ai.AIBaseGlobal import *
## from direct.distributed.ClockDelta import *

## from direct.directnotify import DirectNotifyGlobal
## from direct.distributed import DistributedObjectAI

## class DistributedGuildMemberAI(DistributedObjectAI.DistributedObjectAI):
    ## """
    ## The Guild AI is a global object.
    
    ## See Also:
        ## "otp/src/guild/DistributedGuildMember.py"
        ## "otp/src/configfiles/otp.dc"
    ## """
    ## if __debug__:
        ## notify = DirectNotifyGlobal.directNotify.newCategory('guild')

    ## def __init__(self, air, dateJoined, name):
        ## assert self.notify.debugCall()
        ## DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        ## self.dateJoined=dateJoined
        ## self.name=name

    ## def delete(self):
        ## assert self.notify.debugCall()
        ## self.ignoreAll()
        ## DistributedObjectAI.DistributedObjectAI.delete(self)
  
    ## def getSince(self):
        ## """
        ## returns the date the avatar joined the guild.
        ## """
        ## return self.dateJoined
  
    ## def getName(self):
        ## return self.name
        
    ## def getReputations(self):
        ## return self.reputations
