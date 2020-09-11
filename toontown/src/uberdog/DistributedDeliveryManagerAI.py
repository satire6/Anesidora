
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.AsyncRequest import AsyncRequest
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem

class DistributedDeliveryManagerAI(DistributedObjectAI):

    notify = directNotify.newCategory("DistributedDeliveryManagerAI")
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.nameObject = None;
        self.senderIdContexttoPhone = {}
       
    def hello(self, message):
        print message
        replyToChannel = self.air.getSenderReturnChannel()
        print "This is the AI getting the hello message" , message

    def sendHello(self, message):
        self.sendUpdate("hello", [message])
    
    def rejectHello(self, message):
        print "rejected", message
        
    def helloResponse(self, message):
        print "accepted", message
        
    #NON Test functions begin here
        
    def sendDeliverGifts(self, avId, time):
        self.notify.debugStateCall(self)
        self.sendUpdate("deliverGifts", [avId, time])
        
    def receiveAcceptDeliverGifts(self, avId, message):
        self.notify.debugStateCall(self)        
        receiver = self.air.doId2do.get(avId)
        #if receiver:
        #if the gift receiver happens to be logged in tell them about the gift update
        #print "Deliver Gifts Accepted:", message
        
    def receiveRejectDeliverGifts(self, avId, message):
        self.notify.debugStateCall(self)        
        #print "Deliver Gifts Rejected:", message
        pass        
        
    def sendRequestPurchaseGift(self, item, rAvId, sAvId, context, phone):
        self.notify.debugStateCall(self)        
        #print "sent request for gift"
        uniquekey = (sAvId, context)
        self.senderIdContexttoPhone[uniquekey] = phone
        item.giftTag = sAvId
        
        giftBlob = item.getBlob(store = CatalogItem.Customization)
        self.sendUpdate("receiveRequestPurchaseGift", [giftBlob, rAvId, sAvId, context])
        
        
    def receiveRejectPurchaseGift(self, sAvId, context, retcode, cost):
        self.notify.debugStateCall(self)        
        #print "rejected Purcahse Gift"
        uniquekey = (sAvId, context)
        phone = self.senderIdContexttoPhone[uniquekey]
        phone.sendUpdateToAvatarId(sAvId, "requestGiftPurchaseResponse", [context, retcode])
        simbase.air.catalogManager.refundMoney(sAvId, cost)
        del self.senderIdContexttoPhone[uniquekey]
            
    def receiveAcceptPurchaseGift(self, sAvId, context, retcode):
        self.notify.debugStateCall(self)        
        #print "accepeted Purcahse Gift"
        uniquekey = (sAvId, context)
        phone = self.senderIdContexttoPhone.get(uniquekey)
        if phone:
            phone.sendUpdateToAvatarId(sAvId, "requestGiftPurchaseResponse", [context, retcode])
        if uniquekey in self.senderIdContexttoPhone:
            del self.senderIdContexttoPhone[uniquekey]
    

        
        

        
