import string
import direct
import socket
from direct.http.WebRequest import WebRequestDispatcher
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from direct.distributed.AsyncRequest import AsyncRequest
from otp.ai import AIMsgTypes
from otp.distributed import OtpDoGlobals

from toontown.rpc import RATRequests
from toontown.rpc import RATResponses

class RATManagerUD(DistributedObjectGlobalUD):
    """
    Uberdog object for making RAT awards to Toons
    """
    notify = directNotify.newCategory('RATManagerUD')

    def __init__(self, air):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)

        self.air = air

        self.HTTPListenPort = uber.RATManagerHTTPListenPort

        self.numServed = 0

        self.webDispatcher = WebRequestDispatcher()
        self.webDispatcher.landingPage.setTitle("RATManager")
        self.webDispatcher.landingPage.setDescription("RATManager is a REST-like interface allowing in-game awards from other services.")
        self.webDispatcher.registerGETHandler("getToonList",self.handleHTTPGetToonList)
        self.webDispatcher.registerGETHandler("giveToonBeansRAT",self.handleHTTPGiveToonBeansRAT)
        self.webDispatcher.registerGETHandler("giveToonBeansCS",self.handleHTTPGiveToonBeansCS)
        self.webDispatcher.registerGETHandler("getToonPicId",self.handleHTTPGetToonPicId)
        self.webDispatcher.registerGETHandler("getToonDNA",self.handleHTTPGetToonDNA)
            
        self.webDispatcher.listenOnPort(self.HTTPListenPort)

        self.air.setConnectionName("RATManagerUD")
        self.air.setConnectionURL("http://%s:%s/" % (socket.gethostbyname(socket.gethostname()),self.HTTPListenPort))


    def announceGenerate(self):
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        self.webDispatcher.startCheckingIncomingHTTP()


    # -- HTTP Handlers --

    def handleHTTPGetToonList(self,replyTo,**kw):
        """
        Given an account name, returns the list of toons owned by the account.
        Should never fail unless we have a DB issue or connectivity problem somewhere.
        """
        accountName = kw.get("accountName",None)
        try:
            assert isinstance(accountName,str)
        except:
            self.notify.warning("Invalid getToonList request from %s: %s" % (replyTo.getSourceAddress(),str(kw)))
            replyTo.respondXML(RATResponses.getToonListFailureXML % "INVALID_REQUEST")
            return

        RATRequests.GetToonIdListRequest(replyTo,accountName)


    def handleHTTPGiveToonBeansRAT(self,replyTo,**kw):
        """
        Request to award quantity of beans to toon.
        Used by RAT service.
        """
        toonId = kw.get("toonId",'0')
        beanAmount = kw.get("beanAmount",'0')
        try:
            toonId = int(toonId)
            beanAmount = int(beanAmount)
            assert toonId > 0
            assert toonId < (1<<32)
            assert beanAmount > 0
            assert beanAmount < (1<<16)
        except Exception,e:
            self.notify.warning("Invalid giveToonBeansRAT request from %s: %s" % (replyTo.getSourceAddress(),str(kw)))
            replyTo.respondXML(RATResponses.giveToonBeansRATFailureXML % "INVALID_REQUEST")
            return
        
        self.air.writeServerEvent("UberRPC-GiveToonBeansRAT",replyTo.getSourceAddress(),"%u|%u" % (toonId,beanAmount))

        if hasattr(self.air,"deliveryManager"):
            try:
                self.air.deliveryManager.giveBeanBonus(toonId,beanAmount)
            except:
                replyTo.respondXML(RATResponses.giveToonBeansRATFailureXML % "DELIVERY_FAILURE")
                return
        else:
            self.air.sendUpdateToGlobalDoId(
                "DistributedDeliveryManagerUD",
                "giveBeanBonus",
                OtpDoGlobals.OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER,
                [toonId,beanAmount])

        replyTo.respondXML(RATResponses.giveToonBeansRATSuccessXML)


    def handleHTTPGiveToonBeansCS(self,replyTo,**kw):
        """
        Request to award quantity of beans to toon.
        Used by CS only.
        """
        toonId = kw.get("toonId",'0')
        beanAmount = kw.get("beanAmount",'0')
        try:
            toonId = int(toonId)
            beanAmount = int(beanAmount)
            assert toonId > 0
            assert toonId < (1<<32)
            assert beanAmount > 0
            assert beanAmount < (1<<16)
        except:
            self.notify.warning("Invalid giveToonBeansCS request from %s: %s" % (replyTo.getSourceAddress(),str(kw)))
            replyTo.respondXML(RATResponses.giveToonBeansCSFailureXML % "INVALID_REQUEST")
            return
        
        self.air.writeServerEvent("UberRPC-GiveToonBeansCS",replyTo.getSourceAddress(),"%u|%u" % (toonId,beanAmount))

        if hasattr(self.air,"deliveryManager"):
            try:
                self.air.deliveryManager.giveBeanBonus(toonId,beanAmount)
            except:
                replyTo.respondXML(RATResponses.giveToonBeansCSFailureXML % "DELIVERY_FAILURE")
                return
        else:
            self.air.sendUpdateToGlobalDoId(
                "DistributedDeliveryManagerUD",
                "giveBeanBonus",
                OtpDoGlobals.OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER,
                [toonId,beanAmount])

        replyTo.respondXML(RATResponses.giveToonBeansCSSuccessXML)
        

    def handleHTTPGetToonPicId(self,replyTo,**kw):
        """
        Given a toon ID, returns the pic ID of that toon's image.
        """
        toonId = kw.get("toonId",'0')
        try:
            toonId = int(toonId)
            assert toonId > 0
            assert toonId < (1<<32)
        except:
            self.notify.warning("Invalid getToonPicId request from %s: %s" % (replyTo.getSourceAddress(),str(kw)))
            replyTo.respondXML(RATResponses.getToonPicIdFailureXML % "INVALID_REQUEST")
            return

        RATRequests.GetToonPicIdRequest(replyTo,toonId)


    def handleHTTPGetToonDNA(self,replyTo,**kw):
        """
        Given a toon ID, returns a DNA string for that toon.
        """
        toonId = kw.get("toonId",'0')
        try:
            toonId = int(toonId)
            assert toonId > 0
            assert toonId < (1<<32)
        except:
            self.notify.warning("Invalid getToonDNA request from %s: %s" % (replyTo.getSourceAddress(),str(kw)))
            replyTo.respondXML(RATResponses.getToonDNAFailureXML % "INVALID_REQUEST")
            return

        RATRequests.GetToonDNARequest(replyTo,toonId)
