## """
## """

## from direct.distributed.ClockDelta import *

## from direct.directnotify import DirectNotifyGlobal
## from direct.distributed import DistributedObject

## class DistributedGuildMembership(DistributedObject.DistributedObject):
    ## """
    ## See Also:
        ## "otp/src/configfiles/otp.dc"
        ## "otp/src/guild/DistributedGuildMembershipAI.py"
    ## """
    ## if __debug__:
        ## notify = DirectNotifyGlobal.directNotify.newCategory(
                ## 'DistributedGuildMembership')

    ## def __init__(self, air):
        ## assert self.notify.debugCall()
        ## DistributedObject.DistributedObject.__init__(self, air)

    ## def delete(self):
        ## assert self.notify.debugCall()
        ## self.ignoreAll()
        ## DistributedObject.DistributedObject.delete(self)
