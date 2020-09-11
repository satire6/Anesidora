import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

class CatalogNametagItem(CatalogItem.CatalogItem):
    """
    This represents nametags sent 
    """

    sequenceNumber = 0
    
    def makeNewItem(self, nametagStyle):
        self.nametagStyle = nametagStyle
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        return 1

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder \
           or self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1        
        if avatar.nametagStyle == self.nametagStyle:
            return 1
        return 0
        
    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptNametag
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def getTypeName(self):
        return TTLocalizer.NametagTypeName

    def getName(self):
        if self.nametagStyle == 100:
            name = TTLocalizer.UnpaidNameTag
        else:
            name = TTLocalizer.NametagFontNames[self.nametagStyle]
        name = name + TTLocalizer.NametagLabel
        return name
        if self.nametagStyle == 0:
            name = TTLocalizer.NametagPaid
        elif self.nametagStyle == 1:
            name = TTLocalizer.NametagAction
        elif self.nametagStyle == 2:
            name = TTLocalizer.NametagFrilly
        

    def recordPurchase(self, avatar, optional):
        if avatar:
            avatar.b_setNametagStyle(self.nametagStyle)

        #avatar.emoteAccess[self.emoteIndex] = 1
        #avatar.d_setEmoteAccess(avatar.emoteAccess)
        #TODO: increase the toon's money here
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        #chatBalloon = loader.loadModel("phase_3/models/props/chatbox.bam")
        frame = self.makeFrame()
        if self.nametagStyle == 100:
            inFont = ToontownGlobals.getToonFont()
        else:
            inFont = ToontownGlobals.getNametagFont(self.nametagStyle)
            
        #nametagJar = loader.loadModel("phase_3.5/models/gui/jar_gui")
        nameTagDemo = DirectLabel(
            parent = frame,
            relief = None,
            pos = (0,0,0.24),
            scale = 0.5,
            text = localAvatar.getName(),
            text_fg = (1.0, 1.0, 1.0, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = inFont,
            text_wordwrap = 9,
            )
        #chatBalloon.find("**/top").setPos(1,0,5)
        #chatBalloon.find("**/middle").setScale(1,1,3)
        
        #nametagJar.reparentTo(frame)

        #nametagJar.setPos(0,0,0)
        #nametagJar.setScale(2.5)

        assert (not self.hasPicture)
        self.hasPicture=True

        return (frame, None)

    def output(self, store = ~0):
        return "CatalogNametagItem(%s%s)" % (
            self.nametagStyle,
            self.formatOptionalData(store))

    def compareTo(self, other):
        return self.nametagStyle - other.nametagStyle

    def getHashContents(self):
        return self.nametagStyle

    def getBasePrice(self):
        return 500
        cost = 500
        if self.nametagStyle == 0:
            cost = 600
        elif self.nametagStyle == 1:
            cost = 600
        elif self.nametagStyle == 2:
            cost = 600
        elif self.nametagStyle == 100:
            cost = 50
        return cost

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.nametagStyle = di.getUint16()
        
    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint16(self.nametagStyle)
        
    def isGift(self):
        return 0
        
    def getBackSticky(self):
        #some items should hang around in the back catalog
        itemType = 1 #the types that should stick around
        numSticky = 4 #how many should stick around
        return itemType, numSticky
        
