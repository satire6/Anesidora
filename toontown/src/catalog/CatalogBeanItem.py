import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *

class CatalogBeanItem(CatalogItem.CatalogItem):
    """
    This represents jellybeans sent in the gift system
    """

    sequenceNumber = 0
    
    def makeNewItem(self, beanAmount, tagCode = 1):
        self.beanAmount = beanAmount
        self.giftCode = tagCode
        
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        return 0

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder \
           or self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        return 0
        
    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_ItemAvailable:
            if self.giftCode == ToontownGlobals.GIFT_RAT:
                return TTLocalizer.CatalogAcceptRATBeans
            else:
                return TTLocalizer.CatalogAcceptBeans
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 0

    def getTypeName(self):
        return TTLocalizer.BeanTypeName

    def getName(self):
        name = ("%s %s" % (self.beanAmount , TTLocalizer.BeanTypeName))
        return name

    def recordPurchase(self, avatar, optional):
        if avatar:
            avatar.addMoney(self.beanAmount)

        #avatar.emoteAccess[self.emoteIndex] = 1
        #avatar.d_setEmoteAccess(avatar.emoteAccess)
        #TODO: increase the toon's money here
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        #chatBalloon = loader.loadModel("phase_3/models/props/chatbox.bam")
        beanJar = loader.loadModel("phase_3.5/models/gui/jar_gui")
        #chatBalloon.find("**/top").setPos(1,0,5)
        #chatBalloon.find("**/middle").setScale(1,1,3)
        frame = self.makeFrame()
        beanJar.reparentTo(frame)

        beanJar.setPos(0,0,0)
        beanJar.setScale(2.5)

        assert (not self.hasPicture)
        self.hasPicture=True

        return (frame, None)

    def output(self, store = ~0):
        return "CatalogBeanItem(%s%s)" % (
            self.beanAmount,
            self.formatOptionalData(store))

    def compareTo(self, other):
        return self.beanAmount - other.beanAmount

    def getHashContents(self):
        return self.beanAmount

    def getBasePrice(self):
        # equal to it's worth
        return self.beanAmount

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.beanAmount = di.getUint16()
        
    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.beanAmount)
        
