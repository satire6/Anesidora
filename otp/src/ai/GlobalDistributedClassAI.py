from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.showbase import DirectObject
#from direct.directnotify import DirectNotifyGlobal
import time

class GlobalDistributedClassAI(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("GlobalDistributedClassAI")

    def __init__(self, air, doid, className):
        self.doId = doid
        self.air = air
        # Setting teh Zone to None means No zone logic for this object
        self.zoneId = None
        self.dclass = air.dclassesByName[className]
        # upside registration
        self.air.addDOToTables(self)
        self.air.registerForChannel(self.doId)
        
    def remove():              
        self.air.unregisterForChannel(do.doId)
        # This is a race, you may have messages pending delivery that are already
        # on there way to or in the local queue:
        self.air.removeDOFromTables(self)
        del self.air
        del sel.doId
       
    #############################
    ## Support Functions
    #############################
    
    def sendUpdateToAvatarIdFromDOID(self, avId, fieldName, args):
        channelId = self.GetPuppetConnectionChannel(avId)
        self.sendUpdateToChannelFromDOID(channelId, fieldName, args)
        
    ########    
    # Special Function to set return address to the DOID
    ########
    def sendUpdateToChannelFromDOID(self, channelId, fieldName, args):
        self.air.sendUpdateToChannelFrom(self, channelId, fieldName,self.doId, args)


