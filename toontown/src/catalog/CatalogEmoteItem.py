import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *

# A list of emotesthat are loyalty items, needed by award manager
LoyaltyEmoteItems = (20, 21, 22, 23, 24)

class CatalogEmoteItem(CatalogItem.CatalogItem):
    """
    This represents a particular emote animation.
    """

    sequenceNumber = 0
    pictureToon = None
    def makeNewItem(self, emoteIndex, loyaltyDays = 0):
        self.emoteIndex = emoteIndex
        self.loyaltyDays = loyaltyDays
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
        if self.emoteIndex >= len(avatar.emoteAccess):
            return 0
        return avatar.emoteAccess[self.emoteIndex] != 0
        
    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptEmote
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def getTypeName(self):
        return TTLocalizer.EmoteTypeName

    def getName(self):
        return OTPLocalizer.EmoteList[self.emoteIndex]

    def recordPurchase(self, avatar, optional):
        if self.emoteIndex < 0 or self.emoteIndex > len(avatar.emoteAccess):
            self.notify.warning("Invalid emote access: %s for avatar %s" % (self.emoteIndex, avatar.doId))
            return ToontownGlobals.P_InvalidIndex
                         
        avatar.emoteAccess[self.emoteIndex] = 1
        avatar.d_setEmoteAccess(avatar.emoteAccess)
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.

        # Don't import this at the top of the file, since this code
        # must run on the AI.
        from toontown.toon import Toon
        from toontown.toon import ToonHead
        from toontown.toon import TTEmote
        from otp.avatar import Emote

        assert (not self.hasPicture)
        self.hasPicture=True

        if self.emoteIndex in Emote.globalEmote.getHeadEmotes():
            toon = ToonHead.ToonHead()
            toon.setupHead(avatar.style, forGui = 1)
        else:
            toon = Toon.Toon()
            toon.setDNA(avatar.style)
            toon.loop('neutral')

        toon.setH(180)
        model, ival = self.makeFrameModel(toon, 0)
        

        # Discard the ival from makeFrameModel, since we don't want to
        # spin.

        track, duration = Emote.globalEmote.doEmote(toon, self.emoteIndex, volume = self.volume)
        
        if duration == None:
            duration = 0
        name = "emote-item-%s" % (self.sequenceNumber)
        CatalogEmoteItem.sequenceNumber += 1
        if track != None:
            track = Sequence(Sequence(track, duration = 0),
                             Wait(duration + 2),
                             name = name)
        else:
            track = Sequence(Func(Emote.globalEmote.doEmote, toon, self.emoteIndex),
                             Wait(duration + 4),
                             name = name)
        self.pictureToon = toon
        return (model, track)

    def changeIval(self, volume):
        """Return an interval of the toon doing the emote, with a possible change in volume."""
        # Don't import this at the top of the file, since this code
        # must run on the AI.
        from toontown.toon import Toon
        from toontown.toon import ToonHead
        from toontown.toon import TTEmote
        from otp.avatar import Emote

        self.volume = volume
        
        # assumes getPicture has been called previously
        if not hasattr(self, 'pictureToon'):
            return Sequence()
        track, duration = Emote.globalEmote.doEmote(self.pictureToon, self.emoteIndex, volume = self.volume)
        if duration == None:
            duration = 0
        name = "emote-item-%s" % (self.sequenceNumber)
        CatalogEmoteItem.sequenceNumber += 1
        if track != None:
            track = Sequence(Sequence(track, duration = 0),
                             Wait(duration + 2),
                             name = name)
        else:
            track = Sequence(Func(Emote.globalEmote.doEmote, toon, self.emoteIndex),
                             Wait(duration + 4),
                             name = name)
        return track
    
    def cleanupPicture(self):
        CatalogItem.CatalogItem.cleanupPicture(self)
        assert self.pictureToon
        self.pictureToon.emote.finish()
        self.pictureToon.emote = None
        self.pictureToon.delete()
        self.pictureToon = None
         
    def output(self, store = ~0):
        return "CatalogEmoteItem(%s%s)" % (
            self.emoteIndex,
            self.formatOptionalData(store))

    def compareTo(self, other):
        return self.emoteIndex - other.emoteIndex

    def getHashContents(self):
        return self.emoteIndex

    def getBasePrice(self):
        # All emotes are the same price for now.
        return 550

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.emoteIndex = di.getUint8()
        if versionNumber >= 6:
            self.loyaltyDays = di.getUint16()
        else:
            #RAU this seeems safe, as an old user would never have the new loyalty items
            self.loyaltyDays = 0
        if self.emoteIndex > len(OTPLocalizer.EmoteList):
            raise ValueError
        
    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.emoteIndex)
        dg.addUint16(self.loyaltyDays)
        
    def isGift(self):
        if (self.loyaltyRequirement() > 0):
            return 0
        else:
            if self.emoteIndex in LoyaltyEmoteItems:
                return 0
            else:
                return 1
        
