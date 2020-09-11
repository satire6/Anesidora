## """
## """

## from direct.distributed.ClockDelta import *

## from direct.directnotify import DirectNotifyGlobal
## from direct.distributed import DistributedObjectAI

## class DistributedGuildMembershipAI(DistributedObjectAI.DistributedObjectAI):
    ## """
    ## See Also:
        ## "otp/src/configfiles/otp.dc"
        ## "otp/src/guild/DistributedGuildMembership.py"
    ## """
    ## if __debug__:
        ## notify = DirectNotifyGlobal.directNotify.newCategory(
                ## 'DistributedGuildMembershipAI')

    ## def __init__(self, air):
        ## assert self.notify.debugCall()
        ## DistributedObjectAI.DistributedObjectAI.__init__(self, air)

    ## def delete(self):
        ## assert self.notify.debugCall()
        ## self.ignoreAll()
        ## DistributedObjectAI.DistributedObjectAI.delete(self)
