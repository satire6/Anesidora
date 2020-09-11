from direct.distributed.AsyncRequest import AsyncRequest
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.UberDogGlobal import *
import binascii
from toontown.rpc import RATResponses


class TimeoutException(Exception):
    "Exception raised on request timeout"
    def __init__(self,*args):
        Exception.__init__(self,*args)

class GetToonIdListRequest(AsyncRequest):
    """
    Given an account name, retrieves a list of toon IDs.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GetToonIdListRequest')
        
    def __init__(self,replyTo,accountName):
        """
        replyTo is where we stick the response
        accountName is the account whose avatar list we're fetching
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.replyTo = replyTo
        self.accountName = accountName

        self.askForObjectFieldsByString(4008,"AccountUD",self.accountName,("ACCOUNT_AV_SET",))
 
    def finish(self):
        resDict = self.neededObjects[("ACCOUNT_AV_SET",)]
        res = resDict.get("ACCOUNT_AV_SET",[])
        toonlist = []
        for id in res:
            if id != 0:
                toonlist.append(id)

        GetToonNameRequest(self.replyTo,toonlist)
        
        self.delete()

    def timeout(self,task):
        self.notify.warning("Request timeout in GetToonIdListRequest(%s)." % (self.accountName))
        self.air.writeServerEvent("UberRPC-RequestTimeout",self.replyTo.getSourceAddress(),"GetToonIdListRequest|%s" % self.accountName)
        self.replyTo.respondXML(RATResponses.toonListFailureXML % "DB_TIMEOUT")
        self.delete()


class GetToonNameRequest(AsyncRequest):
    """
    Given a list of toon doIDs, retrieves the toon names.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GetToonNameRequest')

    def __init__(self,replyTo,idList):
        """
        replyTo is where we stick the response
        idList is a list of IDs of the toons whose names we're fetching
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.replyTo = replyTo
        self.idList = idList
        for id in idList:
            self.askForObjectField("DistributedToonUD","setName",id,key=id)

    def finish(self):
        assert self.notify.debugCall()
        assert not self.__deleted

        s = ""

        for id in self.idList:
            name = self.neededObjects.get(id,("unknown",))[0]
            s = s + "  <toon><id>%s</id><name>%s</name></toon>\n" % (id,name)

        self.replyTo.respondXML(RATResponses.getToonListSuccessXML % s)

        self.delete()

    def timeout(self,task):
        self.notify.warning("Request timeout in GetToonNameRequest(%s)." % (self.idList))
        self.air.writeServerEvent("UberRPC-RequestTimeout",self.replyTo.getSourceAddress(),"GetToonNameRequest|%s" % self.idList)
        self.replyTo.respondXML(RATResponses.getToonListFailureXML % "DB_TIMEOUT")
        self.delete()


class GetToonPicIdRequest(AsyncRequest):
    """
    Given the doID of a toon, get the ID for that toon's portrait

    ID format is 'hhggcc' where hh is the two-digit head code, gg is gender code, and cc is the two-digit color code from toon's DNA string
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GetToonPicIdRequest')
    def __init__(self,replyTo,toonID):
        """
        replyTo is where we stick the response
        toonID is the doID of the toon whose picture we want
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.replyTo = replyTo
        self.toonID = toonID
        self.air.writeServerEvent("UberRPC-GetToonPicId",self.replyTo.getSourceAddress(),"%s" % self.toonID)
        self.askForObjectField("DistributedToonUD","setDNAString",self.toonID)

    def finish(self):
        assert self.notify.debugCall()
        assert not self.__deleted
        dna = self.neededObjects["setDNAString"][0]

        picid = "74%02x%02x%02x" % (ord(dna[1]),ord(dna[4]),ord(dna[-1]))

        self.replyTo.respondXML(RATResponses.getToonPicIdSuccessXML % picid)

        self.delete()

    def timeout(self,task):
        self.notify.warning("Request timeout in GetToonPicIdRequest(%s) from %s." % (self.toonID,self.replyTo.getSourceAddress()))
        self.air.writeServerEvent("UberRPC-RequestTimeout",self.replyTo.getSourceAddress(),"GetToonPicIdRequest|%s" % self.toonID)
        self.replyTo.respondXML(RATResponses.getToonPicIdFailureXML % "DB_TIMEOUT")
        self.delete()


class GetToonDNARequest(AsyncRequest):
    """
    Given the doID of a toon, return the toon's DNA string
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GetToonDNARequest')
    def __init__(self,replyTo,toonID):
        """
        replyTo is where we stick the response
        toonID is the doID of the toon whose picture we want
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.replyTo = replyTo
        self.toonID = toonID
        self.air.writeServerEvent("UberRPC-GetToonDNA",self.replyTo.getSourceAddress(),"%u" % self.toonID)
        self.askForObjectField("DistributedToonUD","setDNAString",self.toonID)
        
    def finish(self):
        assert self.notify.debugCall()
        assert not self.__deleted
        dna = self.neededObjects["setDNAString"][0]

        self.replyTo.respondXML(RATResponses.getToonDNASuccessXML % binascii.hexlify(dna))

        self.delete()

    def timeout(self,task):
        self.notify.warning("Request timeout in GetToonDNARequest(%s) from %s." % (self.toonID,self.replyTo.getSourceAddress()))
        self.air.writeServerEvent("UberRPC-RequestTimeout",self.replyTo.getSourceAddress(),"GetToonDNARequest|%s" % self.toonID)
        self.replyTo.respondXML(RATResponses.getToonDNAFailureXML % "DB_TIMEOUT")
        self.delete()
