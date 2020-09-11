from direct.distributed.AsyncRequest import AsyncRequest
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.UberDogGlobal import *
import binascii


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
        
    def __init__(self,resultQueue,clientIP,accountName):
        """
        resultQueue is where we stick the response
        clientIP is the client's address for logging purposes
        accountName is the account whose avatar list we're fetching
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.resultQueue = resultQueue
        self.clientIP = clientIP
        self.accountName = accountName
 
    def submit(self):
        self.air.writeServerEvent("UberRPC-GetToonIdList",self.clientIP,"%s" % self.accountName)
        self.askForObjectFieldsByString(4008,"AccountUD",self.accountName,("ACCOUNT_AV_SET",))

    def finish(self):
        resDict = self.neededObjects[("ACCOUNT_AV_SET",)]
        assert resDict.has_key("ACCOUNT_AV_SET")
        self.resultQueue.put(resDict["ACCOUNT_AV_SET"])
        self.delete()

    def timeout(self,task):
        self.notify.warning("Request timeout in GetToonIdListRequest(%s) from %s." % (self.accountName,self.clientIP))
        self.air.writeServerEvent("UberRPC-RequestTimeout",self.clientIP,"GetToonIdListRequest|%s" % self.accountName)
        self.resultQueue.put(TimeoutException())
        self.delete()
    
class GetToonNameRequest(AsyncRequest):
    """
    Given a doID for a toon, retrieves the toon's name.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GetToonNameRequest')

    def __init__(self,resultQueue,clientIP,toonID):
        """
        resultQueue is where we stick the response
        clientIP is for logging purposes
        toonID is the ID of the toon whose name we're fetching
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.resultQueue = resultQueue
        self.clientIP = clientIP
        self.toonID = toonID

    def submit(self):
        self.askForObjectField("DistributedToonUD","setName",self.toonID)

    def finish(self):
        assert self.notify.debugCall()
        assert not self.__deleted
        resultList = self.neededObjects["setName"]
        self.resultQueue.put(resultList[0])
        self.delete()

    def timeout(self,task):
        self.notify.warning("Request timeout in GetToonNameRequest(%s) from %s." % (self.toonID,self.clientIP))
        self.air.writeServerEvent("UberRPC-RequestTimeout",self.clientIP,"GetToonNameRequest|%s" % self.toonID)
        self.resultQueue.put(TimeoutException())
        self.delete()


class GiveToonBeansCSRequest(AsyncRequest):
    """
    Only for Customer Service requests.
    Given a toon ID and a jellybean amount, give a toon jellybeans.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GiveToonBeansCSRequest')
    def __init__(self,resultQueue,clientIP,toonID,beanAmount):
        """
        resultQueue is where we stick the response
        clientIP is for logging purposes
        toonID is the toon receiving beans
        beanAmount is the number of beans to give
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.resultQueue = resultQueue
        self.clientIP = clientIP
        self.toonID = toonID
        self.beanAmount = beanAmount
        self.done=False

    def submit(self):
        self.air.writeServerEvent("UberRPC-GiveToonBeansCS",self.clientIP,"%u|%u" % (self.toonID,self.beanAmount))
        self.air.deliveryManager.giveBeanBonus(self.toonID,self.beanAmount)
        self.finish()

    def finish(self):
        assert self.notify.debugCall()
        assert not self.__deleted
        if not self.done:
            self.done = True
            self.resultQueue.put("Success")
            self.delete()


class GiveToonBeansRATRequest(AsyncRequest):
    """
    Only for Recruit-a-Toon program.
    Given a toon ID and a jellybean amount, give a toon jellybeans.
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GiveToonBeansRATRequest')
    def __init__(self,resultQueue,clientIP,toonID,beanAmount):
        """
        resultQueue is where we stick the response
        clientIP is for logging purposes
        toonID is the toon receiving beans
        beanAmount is the number of beans to give
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.resultQueue = resultQueue
        self.clientIP = clientIP
        self.toonID = toonID
        self.beanAmount = beanAmount
        self.done=False

    def submit(self):
        self.air.writeServerEvent("UberRPC-GiveToonBeansRAT",self.clientIP,"%u|%u" % (self.toonID,self.beanAmount))
        self.air.deliveryManager.giveRecruitAToonPayment(self.toonID,self.beanAmount)
        self.finish()

    def finish(self):
        assert self.notify.debugCall()
        assert not self.__deleted
        if not self.done:
            self.done = True
            self.resultQueue.put("Success")
            self.delete()
            


class GetToonPicIdRequest(AsyncRequest):
    """
    Given the doID of a toon, get the ID for that toon's portrait

    ID format is 'hhggcc' where hh is the two-digit head code, gg is gender code, and cc is the two-digit color code from toon's DNA string
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GetToonPicIdRequest')
    def __init__(self,resultQueue,clientIP,toonID):
        """
        resultQueue is where we stick the response
        clientIP is for logging purposes
        toonID is the doID of the toon whose picture we want
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.resultQueue = resultQueue
        self.clientIP = clientIP
        self.toonID = toonID

    def submit(self):
        self.air.writeServerEvent("UberRPC-GetToonPicId",self.clientIP,"%u" % self.toonID)
        self.askForObjectField("DistributedToonUD","setDNAString",self.toonID)

    def finish(self):
        assert self.notify.debugCall()
        assert not self.__deleted
        dna = self.neededObjects["setDNAString"][0]

        picid = "74%02x%02x%02x" % (ord(dna[1]),ord(dna[4]),ord(dna[-1]))

        self.resultQueue.put(picid)
        self.delete()

    def timeout(self,task):
        self.notify.warning("Request timeout in GetToonPicIdRequest(%s) from %s." % (self.toonID,self.clientIP))
        self.air.writeServerEvent("UberRPC-RequestTimeout",self.clientIP,"GetToonPicIdRequest|%s" % self.toonID)
        self.resultQueue.put(TimeoutException())
        self.delete()


class GetToonDNARequest(AsyncRequest):
    """
    Given the doID of a toon, return the toon's DNA string
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory('GetToonDNARequest')
    def __init__(self,resultQueue,clientIP,toonID):
        """
        resultQueue is where we stick the response
        clientIP is for logging purposes
        toonID is the doID of the toon whose picture we want
        """
        assert self.notify.debugCall()
        self.__deleted=False
        AsyncRequest.__init__(self,uber.air)
        self.air = uber.air
        self.resultQueue = resultQueue
        self.clientIP = clientIP
        self.toonID = toonID

    def submit(self):
        self.air.writeServerEvent("UberRPC-GetToonDNA",self.clientIP,"%u" % self.toonID)
        self.askForObjectField("DistributedToonUD","setDNAString",self.toonID)

    def finish(self):
        assert self.notify.debugCall()
        assert not self.__deleted
        dna = self.neededObjects["setDNAString"][0]

        self.resultQueue.put(binascii.hexlify(dna))
        self.delete()

    def timeout(self,task):
        self.notify.warning("Request timeout in GetToonDNARequest(%s) from %s." % (self.toonID,self.clientIP))
        self.air.writeServerEvent("UberRPC-RequestTimeout",self.clientIP,"GetToonDNARequest|%s" % self.toonID)
        self.resultQueue.put(TimeoutException())
        self.delete()
