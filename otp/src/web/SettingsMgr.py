from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.web.SettingsMgrBase import SettingsMgrBase

class SettingsMgr(DistributedObjectGlobal, SettingsMgrBase):
    """global object for tweaking settings across all shards and clients in realtime"""
    notify = directNotify.newCategory('SettingsMgr')

    def announceGenerate(self):
        assert self.notify.debugCall()
        DistributedObjectGlobal.announceGenerate(self)
        SettingsMgrBase.announceGenerate(self)
        if not self.cr.isLive():
            # make sure we have the latest changes to the settings
            self._sracs = None
            if self.cr.isConnected():
                self._scheduleChangedSettingRequest()
            # re-send the request every time we connect to the servers
            self._crConnectEvent = self.cr.getConnectedEvent()
            self.accept(self._crConnectEvent, self._handleConnected)

    def _handleConnected(self):
        self._scheduleChangedSettingRequest()

    def _scheduleChangedSettingRequest(self):
        # for some reason we need to wait a bit before sending the request
        # otherwise the UD doesn't get the msg
        if self._sracs:
            self._sracs.destroy()
        self._sracs = FrameDelayedCall('requestAllChangedSettings',
                                       self.sendRequestAllChangedSettings,)

    def delete(self):
        assert self.notify.debugCall()
        self.ignore(self._crConnectEvent)
        if self._sracs:
            self._sracs.destroy()
        SettingsMgrBase.delete(self)
        DistributedObjectGlobal.delete(self)

    def sendRequestAllChangedSettings(self):
        self.sendUpdate('requestAllChangedSettings', [])

    def settingChange(self, settingName, valueStr):
        if valueStr == self._getCurrentValueRepr(settingName):
            # this is a repeat of the current value, probably from the UD starting back up
            return
        
        self.notify.info("got setting change: %s -> %s" % (settingName, valueStr))
        self._changeSetting(settingName, valueStr)
