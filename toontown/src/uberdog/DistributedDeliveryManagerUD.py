"""
The Toontown Delivery Manager UD handles all the delivery accross all
districts.
"""

from cPickle import loads, dumps

from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from otp.otpbase import OTPGlobals

from otp.uberdog.UberDogUtil import ManagedAsyncRequest
from otp.distributed import OtpDoGlobals
from toontown.toonbase import ToontownGlobals
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from otp.uberdog.RejectCode import RejectCode
from direct.distributed.AsyncRequest import AsyncRequest
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem
from toontown.catalog import CatalogPoleItem
from toontown.catalog import CatalogBeanItem
from LRUlist import LRUlist


if __debug__:
    from direct.directnotify.DirectNotifyGlobal import directNotify
    notify = directNotify.newCategory('DeliveryManagerUD')

#-----------------------------------------------------------------------------

        
class AddGiftRequestFR(AsyncRequest):
    def __init__(self, distObj, replyToChannelId,avatarId, newGift, senderId, context, retcode, timeout = 4.0):
        #print "AddGiftRequestFR INIT"
        AsyncRequest.__init__(self, distObj.air, replyToChannelId, timeout)
        self.distObj=distObj
        self.avatarId=avatarId
        self.newGift = newGift
        self.senderId = senderId
        self.context = context
        self.retcode = retcode
        self.askForObjectField(
                    "DistributedToonUD", "setGiftSchedule", avatarId)
    def finish(self):
        #print "AddGiftRequestFR FINISH"
        """
        gift = self.distObj.avatarIdToGifts.get(self.avatarId)
        if gift == None:        
            gift=self.neededObjects.get("setGiftSchedule")[0]
        gift.append(self.newGift)
        self.distObj.writeGift(self.avatarId, gift, self.replyToChannelId)
        AsyncRequest.finish(self)
        """
        giftBlob = self.distObj.avatarIdToGifts.getData(self.avatarId)
        if giftBlob == None:        
            giftBlob=self.neededObjects.get("setGiftSchedule")[0]
        giftItem = CatalogItemList.CatalogItemList(self.newGift, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        giftList = CatalogItemList.CatalogItemList(giftBlob, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        giftList.append(giftItem[0])
        giftBlob = giftList.getBlob(CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.distObj.writeGiftFR(self.avatarId, giftBlob, self.replyToChannelId, self.senderId, self.context, self.retcode)
        AsyncRequest.finish(self)
        
        
class AddGift(AsyncRequest):
    def __init__(self, distObj, replyToChannelId,avatarId, newGift, timeout = 4.0):
        #print "AddGiftRequestFR INIT"
        AsyncRequest.__init__(self, distObj.air, replyToChannelId, timeout)
        self.distObj=distObj
        self.avatarId=avatarId
        self.newGift = newGift
        self.askForObjectField(
                    "DistributedToonUD", "setGiftSchedule", avatarId)
    def finish(self):
        #print "AddGiftRequestFR FINISH"
        """
        gift = self.distObj.avatarIdToGifts.get(self.avatarId)
        if gift == None:        
            gift=self.neededObjects.get("setGiftSchedule")[0]
        gift.append(self.newGift)
        self.distObj.writeGift(self.avatarId, gift, self.replyToChannelId)
        AsyncRequest.finish(self)
        """
        giftBlob = self.distObj.avatarIdToGifts.getData(self.avatarId)
        if giftBlob == None:        
            giftBlob=self.neededObjects.get("setGiftSchedule")[0]
        giftItem = CatalogItemList.CatalogItemList(self.newGift, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        giftList = CatalogItemList.CatalogItemList(giftBlob, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        if giftItem[0].giftCode != ToontownGlobals.GIFT_RAT:
            #print("Gift Item not RAT")
            giftList.append(giftItem[0])
            giftBlob = giftList.getBlob(CatalogItem.Customization | CatalogItem.DeliveryDate)
        else:
            #print("Gift Item is RAT")
            giftBlob = AccumRATBeans(giftItem[0], giftBlob)
        self.distObj.writeGift(self.avatarId, giftBlob, self.replyToChannelId)
        giftList.append(giftItem[0])
        giftBlob = giftList.getBlob(CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.distObj.writeGift(self.avatarId, giftBlob, self.replyToChannelId)

        AsyncRequest.finish(self)
        
def AccumRATBeans(newGift, GiftListBlob):
        giftList = CatalogItemList.CatalogItemList(GiftListBlob, store = CatalogItem.Customization | CatalogItem.DeliveryDate)

        if newGift.giftCode == ToontownGlobals.GIFT_RAT:
            numBeans = newGift.beanAmount
            found = 0
            for index in range(len(giftList)):
                if(giftList[index].giftCode == ToontownGlobals.GIFT_RAT and found == 0):
                    found = 1
                    giftList[index].beanAmount = numBeans + giftList[index].beanAmount
                    #print giftList[index].beanAmount 
        if found:
            #print("RAT already on list") 
            giftList.markDirty()
        else:
            #print("RAT is not on the list")
            giftList.append(newGift)
       
        newBlobList = giftList.getBlob(CatalogItem.Customization | CatalogItem.DeliveryDate)

        return newBlobList
        
        
        
class DeliverGiftRequest(AsyncRequest):
    def __init__(self, distObj, replyToChannelId, avatarId, time, timeout = 4.0):
        AsyncRequest.__init__(self, distObj.air, replyToChannelId, timeout)
        self.distObj=distObj
        self.avatarId=avatarId
        self.time = time
        self.askForObjectField(
                    "DistributedToonUD", "setGiftSchedule", avatarId)

    def finish(self):

        giftListBlob=self.neededObjects.get("setGiftSchedule")[0]
        giftList = CatalogItemList.CatalogItemList(giftListBlob, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        delivered, remaining = giftList.extractDeliveryItems(self.time)
        giftBlob = remaining.getBlob(CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.distObj.writeGiftField(self.avatarId, giftBlob, self.replyToChannelId)
        AsyncRequest.finish(self)
        
class GetAvatarRequest(AsyncRequest):
    def __init__(self, distObj, replyToChannelId, avatarId, timeout = 4.0):
        AsyncRequest.__init__(self, distObj.air, replyToChannelId, timeout)
        self.distObj=distObj
        self.avatarId=avatarId
        self.askForObject(avatarId)
        
    def finish(self):
        avatar = self.neededObjects[self.avatarId]
        #put neat stuff here
        AsyncRequest.finish(self)
        
class PurchaseGiftRequest(AsyncRequest):
    def __init__(self, distObj, replyToChannelId, senderId, receiverId, itemBlob, context, timeout = 4.0):
        #print "PurchaseGiftRequest INIT"
        AsyncRequest.__init__(self, distObj.air, replyToChannelId, timeout)
        self.distObj=distObj
        self.senderId=senderId
        self.receiverId=receiverId
        self.itemBlob=itemBlob
        self.context = context
        self.retcode = None
        self.item = None
        self.catalogType = None
        self.neededObjects[senderId] = None
        self.neededObjects[receiverId] = None
        self.askForObject(senderId)
        self.askForObject(receiverId)
        self.cost = 0
        #print "PurchaseGiftRequest INIT10"
        
    def checkCatalog(self, retcode):
        sAv = self.neededObjects[self.senderId]
        rAv = self.neededObjects[self.receiverId]
        if self.item in sAv.monthlyCatalog:
            self.catalogType = CatalogItem.CatalogTypeMonthly
        elif self.item in sAv.weeklyCatalog:
            self.catalogType = CatalogItem.CatalogTypeWeekly
        elif self.item in sAv.backCatalog:
            self.catalogType = CatalogItem.CatalogTypeBackorder
        else:
            self.air.writeServerEvent('suspicious', sAv.doId, 'purchaseItem %s not in catalog' % (self.item))
            self.notify.warning("Avatar %s attempted to purchase %s, not on catalog." % (sAv.doId, self.item))
            self.notify.warning("Avatar %s weekly: %s" % (sAv.doId, sAv.weeklyCatalog))
            return ToontownGlobals.P_NotInCatalog
        return retcode
        
    def checkMoney(self, retcode):
        sAv = self.neededObjects[self.senderId]
        rAv = self.neededObjects[self.receiverId]
        price = self.item.getPrice(self.catalogType)
        self.cost = price
        if price > sAv.getTotalMoney():
            self.air.writeServerEvent('suspicious', sAv.doId, 'purchaseItem %s not enough money' % (self.item))
            self.notify.warning("Avatar %s attempted to purchase %s, not enough money." % (sAv.doId, self.item))
            return ToontownGlobals.P_NotEnoughMoney
        return retcode
        
    def checkGift(self, retcode):
        if (self.item.isGift() <= 0):
            return ToontownGlobals.P_NotAGift
        return retcode
        
    def checkGender(self, retcode):
        sAv = self.neededObjects[self.senderId]
        rAv = self.neededObjects[self.receiverId]
        if ((self.item.forBoysOnly() and rAv.dna.getGender() == 'f') or (self.item.forGirlsOnly() and rAv.dna.getGender() == 'm')):
            return ToontownGlobals.P_WillNotFit
        return retcode
        
    def checkPurchaseLimit(self, retcode):
        sAv = self.neededObjects[self.senderId]
        rAv = self.neededObjects[self.receiverId]
        if self.item.reachedPurchaseLimit(rAv):
            return ToontownGlobals.P_ReachedPurchaseLimit
        return retcode
        
    def checkMailbox(self, retcode):
        sAv = self.neededObjects[self.senderId]
        rAv = self.neededObjects[self.receiverId]
        if len(rAv.mailboxContents) + len(rAv.onGiftOrder) >= ToontownGlobals.MaxMailboxContents:
            if len(rAv.mailboxContents) == 0:
                retcode = ToontownGlobals.P_OnOrderListFull
            else:
                retcode = ToontownGlobals.P_MailboxFull
        return retcode
                
        
        
    def finish(self):
        #print "PurchaseGiftRequest FINISH"
        sAv = self.neededObjects[self.senderId]
        rAv = self.neededObjects[self.receiverId]
        self.item = CatalogItem.getItem(self.itemBlob, store = CatalogItem.Customization)
        retcode = None
        #put neat stuff here
        #-----------------------------------------------------------------------------
        retcode = self.checkGift(retcode)
        retcode = self.checkCatalog(retcode)
        #retcode = self.checkMoney(retcode)
        retcode = self.checkGender(retcode)
        retcode = self.checkPurchaseLimit(retcode)
        retcode = self.checkMailbox(retcode)
        if (retcode != None):
                self.distObj.sendUpdateToChannel(self.replyToChannelId, "receiveRejectPurchaseGift",
                [self.senderId, self.context, retcode, self.cost])
        else:
            now = (int)(time.time() / 60 + 0.5)
            deliveryTime = self.item.getDeliveryTime() / self.distObj.timeScale
            if deliveryTime < 2:
                deliveryTime = 2
            self.item.deliveryDate = int(now + deliveryTime)
            #self.item.giftTag = self.senderId
            itemList = CatalogItemList.CatalogItemList([self.item])
            itemBlob = itemList.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            retcode = ToontownGlobals.P_ItemOnOrder
            self.distObj.addGiftFR(self.receiverId, itemBlob, self.senderId, self.context, retcode, self.replyToChannelId)
        #-----------------------------------------------------------------------------
  
        AsyncRequest.finish(self)
        
        
class GiveItem(AsyncRequest):
    def __init__(self, distObj, replyToChannelId, receiverId, itemBlob, timeout = 4.0):
        #print "AddItem INIT"
        AsyncRequest.__init__(self, distObj.air, replyToChannelId, timeout)
        self.distObj=distObj
        #self.senderId=senderId
        self.receiverId=receiverId
        self.itemBlob=itemBlob
        self.item = None
        self.catalogType = None
        self.neededObjects[receiverId] = None
        #self.askForObject(senderId)
        self.askForObject(receiverId)
        self.cost = 0
        #print "AddItem INIT10"
        
        
        
    def finish(self):
        #print "AddItem FINISH"
        rAv = self.neededObjects[self.receiverId]
        self.item = CatalogItem.getItem(self.itemBlob, store = CatalogItem.Customization)

        now = (int)(time.time() / 60 + 0.5)
        deliveryTime = self.item.getDeliveryTime() / self.distObj.timeScale
        #if deliveryTime < 2:
        #    deliveryTime = 2
        deliveryTime = 2
        self.item.deliveryDate = int(now + deliveryTime)
        itemList = CatalogItemList.CatalogItemList([self.item])
        itemBlob = itemList.getBlob(store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        retcode = ToontownGlobals.P_ItemOnOrder
        self.distObj.addGift(self.receiverId, itemBlob, self.replyToChannelId)
        #-----------------------------------------------------------------------------
  
        AsyncRequest.finish(self)
        
class DistributedDeliveryManagerUD(DistributedObjectGlobalUD):
    timeScale = simbase.config.GetFloat('catalog-time-scale', 1.0)
    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.avatarIdToName = LRUlist(8192)#{} #cache for names from the database
        self.avatarIdToGifts = LRUlist(8192)#{} #cache for gifts from the database
        self.giftPendingCounter = 0;
        
    def giveGiftItemToAvatar(self, itemBlob, receiverId):
        print("Adding Unchecked Gift Item")
        replyToChannel = self.air.getSenderReturnChannel()
        myGiveItem = GiveItem(self, replyToChannel, receiverId, itemBlob)
        
    def giveTestItemToAvatar(self, receiverId):
        print("Adding Test Item")
        replyToChannel = self.air.getSenderReturnChannel()
        testItem = CatalogBeanItem.CatalogBeanItem(500)
        testItem.tes = 0
        testItem.giftCode = 1
        itemBlob = testItem.getBlob(store = CatalogItem.Customization)
        myGiveItem = GiveItem(self, replyToChannel, receiverId, itemBlob)
        
    def giveBeanBonus(self, receiverId, amount = 1):
        replyToChannel = self.air.getSenderReturnChannel()
        testItem = CatalogBeanItem.CatalogBeanItem(amount)
        testItem.giftTag = 0
        testItem.giftCode = 1
        itemBlob = testItem.getBlob(store = CatalogItem.Customization)
        myGiveItem = GiveItem(self, replyToChannel, receiverId, itemBlob)
        
        
    def giveRecruitAToonPayment(self, receiverId, amount = 1):
        # print("Adding Bean Item")
        replyToChannel = self.air.getSenderReturnChannel()
        testItem = CatalogBeanItem.CatalogBeanItem(amount)
        testItem.giftTag = 0
        testItem.giftCode = ToontownGlobals.GIFT_RAT
        itemBlob = testItem.getBlob(store = CatalogItem.Customization)
        testBlob = CatalogItemList.CatalogItemList(itemBlob, store = CatalogItem.Customization)
        #import pdb; pdb.set_trace()
        myGiveItem = GiveItem(self, replyToChannel, receiverId, itemBlob)
        
        
    def receiveRequestPurchaseGift(self, giftBlob, receiverId, senderId, context):
        #print "receiveRequestPurchaseGift"
        # this is where the message gets sent back to, in this case it is the calling Client
        replyToChannelAI = self.air.getSenderReturnChannel()
        # senderId = self.air.getAvatarIdFromSender()
        myPGR=PurchaseGiftRequest(self, replyToChannelAI, senderId, receiverId, giftBlob, context)
        
    def addGiftFR(self, doId, newGift, senderId, context, retcode, replyToChannelId):
        #print "addGiftFR"
        """
        Appends an existing gift list with the parameter newGift
        doId is the DO that you want to append newGift onto
        newGift the gift blob you want to add
        """
        # this is where the message gets sent back to, in this case it is the calling AI
        # replyToChannel = self.air.getSenderReturnChannel()
        # check to see if the gift is in our cache dictionary
        giftBlob = self.avatarIdToGifts.getData(doId)
        giftItem = CatalogItemList.CatalogItemList(newGift, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.air.writeServerEvent("Adding Gift", doId, "sender %s receiver %s gift %s" % (senderId, doId, giftItem[0].getName()))
        if giftBlob == None:
            # if not in our cache
            myAddGiftRequestFR=AddGiftRequestFR(self, replyToChannelId, doId, newGift, senderId, context, retcode)
        else:
            # else it's in our cache 
            giftList = CatalogItemList.CatalogItemList(giftBlob, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            giftItem = CatalogItemList.CatalogItemList(newGift, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            giftList.append(giftItem[0])
            
            giftBlob = giftList.getBlob(CatalogItem.Customization | CatalogItem.DeliveryDate)
            self.writeGiftFR(doId, giftBlob, replyToChannelId, senderId, context, retcode)
            
        
    def writeGiftFR(self, avatarId, newGift, replyToChannelId, senderId, context, retcode):
        #print "writeGiftFR"
        #print retcode
        """
        Writes the newly appended gift to the database
        doId is the DO that you want to append newGift onto
        newGift final appended blob to write to the database
        replyToChannel is where the message gets sent back to, in this case it is the calling AI
        """
        if 1 == 1: #case where it works
            #print "sending acceptFR"
            self.avatarIdToGifts.putData(avatarId, newGift)#update the cache
            self.air.sendUpdateToDoId(
                "DistributedToon",
                "setGiftSchedule", avatarId, [newGift])
                #update the database
            self.sendUpdateToChannel(replyToChannelId, "receiveAcceptPurchaseGift", 
                [senderId, context, retcode])
                #return an Accept message to the AI caller
        else:
            #print "sending rejectFR"
            self.sendUpdateToChannel(replyToChannelId, "receiveRejectPurchaseGift",
                [senderid, context, retcode])
                #return a Reject message to the AI caller
                
                
    def addGift(self, doId, newGift, replyToChannelId):
        # print "addGift"
        """
        Appends an existing gift list with the parameter newGift
        doId is the DO that you want to append newGift onto
        newGift the gift blob you want to add
        """
        # this is where the message gets sent back to, in this case it is the calling AI
        # replyToChannel = self.air.getSenderReturnChannel()
        # check to see if the gift is in our cache dictionary
        giftBlob = self.avatarIdToGifts.getData(doId)
        giftItem = CatalogItemList.CatalogItemList(newGift, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
        self.air.writeServerEvent("Adding Server Gift", doId, "receiver %s gift %s" % (doId, giftItem[0].getName()))
        if giftBlob == None:
            # if not in our cache
            myAddGift=AddGift(self, replyToChannelId, doId, newGift)
        else:
            # else it's in our cache
            giftList = CatalogItemList.CatalogItemList(giftBlob, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            giftItem = CatalogItemList.CatalogItemList(newGift, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            if giftItem[0].giftCode != ToontownGlobals.GIFT_RAT:

                giftList.append(giftItem[0])
                giftBlob = giftList.getBlob(CatalogItem.Customization | CatalogItem.DeliveryDate)
            else:
                giftBlob = AccumRATBeans(giftItem[0], giftBlob)
            self.writeGift(doId, giftBlob, replyToChannelId)
            
    def writeGift(self, avatarId, newGift, replyToChannelId):
        #print "writeGift"
        #print retcode
        """
        Writes the newly appended gift to the database
        doId is the DO that you want to append newGift onto
        newGift final appended blob to write to the database
        """
        if 1 == 1: #case where it works
            #print "sending acceptFR"
            self.avatarIdToGifts.putData(avatarId, newGift)#update the cache
            self.air.sendUpdateToDoId(
                "DistributedToon",
                "setGiftSchedule", avatarId, [newGift])
                #update the database
                
    def deliverGifts(self, avId, time):
        """
        a request to have a toon's gifts delivered to their mailbox
        this simply removes old gifts based on the time parameter
        """
        #retreive the onGiftDelivery field
        #remove the old gifts from the onGiftDelivery field
        replyToChannelId = self.air.getSenderReturnChannel()
        
        giftListBlob = self.avatarIdToGifts.getData(avId)
        if giftListBlob == None:
            # if not in our cache
            myAddGiftRequest=DeliverGiftRequest(self, replyToChannelId, avId, time)
        else:
            giftList = CatalogItemList.CatalogItemList(giftListBlob, store = CatalogItem.Customization | CatalogItem.DeliveryDate)
            delivered, remaining = giftList.extractDeliveryItems(time)
            giftBlob = remaining.getBlob(CatalogItem.Customization | CatalogItem.DeliveryDate)
            self.writeGiftField(avId, giftBlob, replyToChannelId)
            
        self.sendUpdateToChannel(replyToChannelId, "receiveAcceptDeliverGifts", 
           [avId, "deliverGifts activated"])
        #print "Delivering Gifts"

                
    def writeGiftField(self, avatarId, giftBlob, replyToChannelId):
        """
        Rewrites the gift feild
        doId is the DO that you want to append newGift onto
        giftBlob final blob to write to the database
        replyToChannel is where the message gets sent back to, in this case it is the calling AI
        """
        if 1 == 1: #case where it works
            self.avatarIdToGifts.putData(avatarId, giftBlob)#update the cache
            self.air.sendUpdateToDoId(
                "DistributedToon",
                "setGiftSchedule", avatarId, [giftBlob])
                #update the database
            self.sendUpdateToChannel(replyToChannelId, "receiveAcceptDeliverGifts", 
                [avatarId, "rADG"])
                #return an Accept message to the AI caller
        else:
            self.sendUpdateToChannel(replyToChannelId, "receiveRejectDeliverGifts",
                [avatarId, "rRDG"])
                #return a Reject message to the AI caller
    
    def hello(self, message):
        print message
        replyToChannel = self.air.getSenderReturnChannel()
        if message == "boo boo stinks":
            print "no he doesn't you fool"
            self.sendUpdateToChannel(
                   replyToChannel, "rejectHello", ["no he doesn't you fool"])
        else:
               self.sendUpdateToChannel(
                   replyToChannel, "helloResponse", [message + "response"])
                   
    def requestAck(self):
        replyToChannel = self.air.getSenderReturnChannel()
        self.sendUpdateToChannel(replyToChannel, "returnAck", [])
        
        

