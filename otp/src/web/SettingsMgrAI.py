from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from otp.web.SettingsMgrBase import SettingsMgrBase

class SettingsMgrAI(DistributedObjectGlobalAI, SettingsMgrBase):
    """global object for tweaking settings across all shards and clients in realtime"""
    notify = directNotify.newCategory('SettingsMgrAI')
    
    def announceGenerate(self):
        assert self.notify.debugCall()
        DistributedObjectGlobalAI.announceGenerate(self)
        SettingsMgrBase.announceGenerate(self)
        self.sendUpdate('requestAllChangedSettings', [])

    def delete(self):
        assert self.notify.debugCall()
        SettingsMgrBase.delete(self)
        DistributedObjectGlobalAI.delete(self)

    def settingChange(self, settingName, valueStr):
        if valueStr == self._getCurrentValueRepr(settingName):
            # this is a repeat of the current value, probably from the UD starting back up
            return
        
        self.notify.info("got setting change: %s -> %s" % (settingName, valueStr))
        self._changeSetting(settingName, valueStr)
