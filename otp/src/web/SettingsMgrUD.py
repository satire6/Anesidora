from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.http.WebRequest import WebRequestDispatcher
from direct.task import Task
from otp.ai import AIMsgTypes
from otp.web.SettingsMgrBase import SettingsMgrBase
from otp.web.Setting import Setting, StateVarSetting
import random
import string
import socket

class SettingsMgrUD(DistributedObjectGlobalUD, SettingsMgrBase):
    """global object for tweaking settings across all shards and clients in realtime"""
    notify = directNotify.newCategory('SettingsMgrUD')

    SessionIdAlphabet = string.letters + string.digits

    ModifiedColor = "CCFFCC"
    
    def __init__(self, air):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)

        self.HTTPListenPort = uber.settingsMgrHTTPListenPort
        
        self.webDispatcher = WebRequestDispatcher()
        self.webDispatcher.landingPage.setTitle("SettingsMgr")
        self.webDispatcher.landingPage.setDescription("SettingsMgr enables developers to tweak game settings without restarting the site.")
        self.webDispatcher.registerGETHandler("settings",self.handleHTTPSettings,returnsResponse=True,autoSkin=True)
        self.webDispatcher.landingPage.addTab("Settings","/settings")
        self.webDispatcher.listenOnPort(self.HTTPListenPort)

        self.air.setConnectionName("SettingsMgr")
        self.air.setConnectionURL("http://%s:%s/" % (socket.gethostbyname(socket.gethostname()),self.HTTPListenPort))

    def announceGenerate(self):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        SettingsMgrBase.announceGenerate(self)
        self._newSessionId()
        # clear any changed state from a previous session across all AIs and clients
        self._broadcastCurrentSettings()
        self.startCheckingIncomingHTTP()

    def delete(self):
        assert self.notify.debugCall()
        self.stopCheckingIncomingHTTP()
        SettingsMgrBase.delete(self)
        del self._sessionId
        DistributedObjectGlobalUD.delete(self)

    def getPageTitle(self):
        return "Settings Page"

    def _newSessionId(self):
        # unique URL-safe string
        self._sessionId = ''
        for i in xrange(32):
            self._sessionId += random.choice(SettingsMgrUD.SessionIdAlphabet)

    def handleHTTPSettings(self, **kw):
        assert self.notify.debugCall()
        if ('restart%s' % self._sessionId in kw) and ('sessionId' not in kw):
            self.notify.error('restart requested, please ignore')
        # make sure we're not getting stale data
        sessionId = kw.pop('sessionId', None)
        staleSession = (sessionId is not None) and (sessionId != self._sessionId)
        if not staleSession:
            self._newSessionId()
            for settingName, valueStr in kw.iteritems():
                try:
                    setting = self._getSetting(settingName)
                except:
                    self.notify.warning('unknown setting "%s"' % settingName)
                    continue
                # convert escaped characters
                while 1:
                    try:
                        i = valueStr.index('%')
                    except:
                        break
                    lastCharIndex = len(valueStr)-1
                    if i <= lastCharIndex-2:
                        try:
                            num = eval('0x' + valueStr[i+1:i+3])
                        except:
                            self.notify.warning('error un-escaping string: %s' % valueStr)
                            break
                        else:
                            valueStr = valueStr[:i] + chr(num) + valueStr[i+3:]
                # spaces get replaced with + in the URL
                # this means we can't accept + in our webpage fields
                valueStr = valueStr.replace('+', ' ')
                if valueStr != self._getCurrentValueRepr(settingName):
                    try:
                        val = eval(valueStr)
                    except:
                        self.notify.warning('error setting %s to "%s"' % (settingName, valueStr))
                        continue
                    # detect attempt to set value back to original
                    if repr(val) == self._getOriginalValueRepr(settingName):
                        valueStr = repr(val)
                    self.notify.info("from webpage: %s -> %s" % (settingName, valueStr))
                    # send to AIs
                    self.sendUpdate('settingChange', [settingName, valueStr])
                    # send to clients
                    self.sendUpdateToChannel(AIMsgTypes.CHANNEL_CLIENT_BROADCAST,
                                             'settingChange', [settingName, valueStr])
                    setting.setValue(val)
                    self._currentValueReprs[settingName] = valueStr

        page = ''
        if staleSession:
            page += \
                 """
                 <b><font color="FF0000">STALE SESSION ID -- SETTING CHANGES LOST -- PLEASE RETRY</font></b>
                 """
        page += \
             """
             <form action="settings" method="GET"><p>
             <input type="hidden" id="restart%s" name="restart%s" value="1">
             <input type="submit" value="Restart Process">
             </p></form>
             <form action="settings" method="GET"><p>""" % (self._sessionId, self._sessionId, )
        settingNames = self._settings.keys()
        settingNames.sort()
        page += "<table><caption>%s</caption><thead><tr><th scope=col>Setting</th><th scope=col>Value</th></tr></thead>\n" % self.getPageTitle()
        rowNum=-1
        for name in settingNames:
            rowNum += 1
            valueRepr = self._getCurrentValueRepr(name)
            origValueRepr = self._getOriginalValueRepr(name)
            # color the background of modified input fields
            inputColorCode = ''
            if valueRepr != origValueRepr:
                inputColorCode = ' STYLE="background-color: #%s"' % SettingsMgrUD.ModifiedColor
            if rowNum % 2 == 1:
                page += "<tr class=\"odd\">"
            else:
                page += "<tr>"
            page += (
                """<td><label for="%(name)s">%(name)s: </label></td>
                <td><input type="text" id="%(name)s" name="%(name)s" value="%(value)s"%(color)s>""" % {
                'name': name, 'value': valueRepr, 'color': inputColorCode})
            if valueRepr != origValueRepr:
                page += (""" <b>modified, original value</b>=%s""" %
                         (origValueRepr,))
            page += """</td></tr>\n"""
        # hidden sessionId protects us from the back button and stale data
        page += """<input type="hidden" id="sessionId" name="sessionId" value="%s">""" % (
            self._sessionId)
        page += \
             """</table><input type="submit" value="Submit">
             </p></form>"""
        return page

    def _broadcastCurrentSettings(self):
        # send all current settings to all AIs and clients
        for settingName in self._iterSettingNames():
            curRepr = self._getCurrentValueRepr(settingName)
            # all AIs
            self.sendUpdate('settingChange', [settingName, curRepr])
            # all clients
            self.sendUpdateToChannel(AIMsgTypes.CHANNEL_CLIENT_BROADCAST,
                                     'settingChange', [settingName, curRepr])

    def requestAllChangedSettings(self):
        # client or AI just came online, send them everything that's changed
        returnChannel = self.air.getSenderReturnChannel()
        self.notify.debug('got requestAllChangedSettings from %s' % returnChannel)
        for settingName in self._iterSettingNames():
            if self._isSettingModified(settingName):
                curRepr = self._getCurrentValueRepr(settingName)
                self.sendUpdateToChannel(returnChannel,
                                         'settingChange', [settingName, curRepr])

    def startCheckingIncomingHTTP(self):
        assert self.notify.debugCall()
        taskMgr.remove(self.uniqueName('pollHTTPTask'))
        taskMgr.doMethodLater(0.3,self.pollHTTPTask,self.uniqueName('pollHTTPTask'))

    def stopCheckingIncomingHTTP(self):
        assert self.notify.debugCall()
        taskMgr.remove(self.uniqueName('pollHTTPTask'))

    def pollHTTPTask(self,task):
        """
        Task that polls the HTTP server for new requests.
        """
        assert self.notify.debugCall()
        self.webDispatcher.poll()
        return Task.again
