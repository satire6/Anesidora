#################################################################
# File: BanManagerAI.py
# Purpose: Module to ban avatars while inside the game and kick
#          them out of the game
#################################################################
import urllib
import os
from pandac.PandaModules import HTTPClient, Ramfile
from direct.directnotify import DirectNotifyGlobal

class BanManagerAI:
    notify = DirectNotifyGlobal.directNotify.newCategory("BanManagerAI")

    # These URLS came from Alper Akture
    # dev instance (but as of 7/1/2010 hooked to live disl)
    # http://dnhdosapp01.wdig.com:8005/dis-hold/action/event
    # qa instance
    # http://qnhspapp02.wdig.com:8005/dis-hold/action/event
    # live
    # https://vapps.disl.starwave.com:8005/dis-hold/action/event
    BanUrl = simbase.config.GetString("ban-base-url", "https://vapps.disl.starwave.com:8005/dis-hold/action/event")
    App = simbase.config.GetString("ban-app-name", "TTWorldAI")
    Product = simbase.config.GetString("ban-product", "Toontown")
    EventName = simbase.config.GetString("ban-event-name", "tthackattempt")
    
    def __init__(self):
        """Construct and initialize members."""
        self.curBanRequestNum = 0
        self.channels = {}
        self.ramFiles = {}

    def ban(self, avatarId, dislid, comment):
        """Ban the player"""
        
        parameters = ""
        parameters += "app=%s" % self.App
        parameters += "&product=%s" % self.Product
        parameters += "&user_id=%s" % dislid
        parameters += "&event_name=%s" % self.EventName
        commentWithAvatarId = "avId-%s " % avatarId
        commentWithAvatarId += comment
        parameters += "&comments=%s" % urllib.quote(str(commentWithAvatarId))

        # get the base ban url from the environment variable first
        baseUrlToUse = self.BanUrl
        osBaseUrl = os.getenv("BAN_URL")
        if osBaseUrl:
            baseUrlToUse  = osBaseUrl
        fullUrl = baseUrlToUse + "?" + parameters
        
        self.notify.info ("ban request %s dislid=%s comment=%s fullUrl=%s" % (self.curBanRequestNum, dislid, comment, fullUrl))
        simbase.air.writeServerEvent('ban_request', avatarId, "%s|%s|%s" % (dislid, comment, fullUrl))

        if simbase.config.GetBool('do-actual-ban',False):            
            newTaskName = "ban-task-%d" % self.curBanRequestNum
            newTask = taskMgr.add(self.doBanUrlTask, newTaskName)
            newTask.banRequestNum = self.curBanRequestNum
            http = HTTPClient.getGlobalPtr()
            channel = http.makeChannel(False) # hmm should we make true for a persistent connection?
            self.channels [ self.curBanRequestNum] = channel
            rf = Ramfile()
            self.ramFiles [ self.curBanRequestNum] = rf

            channel.beginGetDocument(fullUrl)
            channel.downloadToRam(rf)
        
        self.curBanRequestNum += 1

    def cleanupBanReq(self, banReq):
        """Cleanup stuff that's associated with this ban request."""
        channel = self.channels.get(banReq)
        if channel:
            del self.channels[banReq]
        ramfile = self.ramFiles.get(banReq)
        if ramfile:
            del self.ramFiles[banReq]


    def doBanUrlTask(self, task):
        """Continue downloading the ban url if needed."""
        banReq = task.banRequestNum
        channel = self.channels.get(banReq)
        if channel:
            if channel.run():
                return task.cont
        else:
            self.notify.warning("no channel for ban req %s" % banReq)
            self.cleanupBanReq(banReq)
            return task.done

        result = ""
        ramfile = self.ramFiles.get(banReq)
        if ramfile:
            result = ramfile.getData()
        self.notify.info("done processing ban request %s, ramFile=%s" % (banReq, result))
        self.cleanupBanReq(banReq)
        return task.done
