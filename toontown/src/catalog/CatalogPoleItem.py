import CatalogItem
from toontown.toonbase import ToontownGlobals
from toontown.fishing import FishGlobals
from direct.actor import Actor
from toontown.toonbase import TTLocalizer
from direct.interval.IntervalGlobal import *

class CatalogPoleItem(CatalogItem.CatalogItem):
    """CatalogPoleItem

    This represents any of the fishing pole models you might be able
    to buy.  We assume that you can buy fishing poles only in
    sequence, and that the rodId number increases with each better
    pole.

    """

    sequenceNumber = 0
    
    def makeNewItem(self, rodId):
        self.rodId = rodId
        
        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        # Returns the maximum number of this particular item an avatar
        # may purchase.  This is either 0, 1, or some larger number; 0
        # stands for infinity.
        return 1

    def reachedPurchaseLimit(self, avatar):
        # Returns true if the item cannot be bought because the avatar
        # has already bought his limit on this item.
        return avatar.getFishingRod() >= self.rodId or \
               self in avatar.onOrder or \
               self in avatar.mailboxContents
    

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def getTypeName(self):
        return TTLocalizer.PoleTypeName

    def getName(self):
        return TTLocalizer.FishingRod % (TTLocalizer.FishingRodNameDict[self.rodId])

    def recordPurchase(self, avatar, optional):
        if self.rodId < 0 or self.rodId > FishGlobals.MaxRodId:
            self.notify.warning("Invalid fishing pole: %s for avatar %s" % (self.rodId, avatar.doId))
            return ToontownGlobals.P_InvalidIndex

        if self.rodId < avatar.getFishingRod():
            self.notify.warning("Avatar already has pole: %s for avatar %s" % (self.rodId, avatar.doId))
            return ToontownGlobals.P_ItemUnneeded
                         
        avatar.b_setFishingRod(self.rodId)
        return ToontownGlobals.P_ItemAvailable
        
    def isGift(self):
        return 0

    def getDeliveryTime(self):
        # Returns the elapsed time in minutes from purchase to
        # delivery for this particular item.
        return 24 * 60  # 24 hours.

    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.

        rodPath = FishGlobals.RodFileDict.get(self.rodId)

        pole = Actor.Actor(rodPath, {'cast' : 'phase_4/models/props/fishing-pole-chan'})
        
        pole.setPosHpr(
            1.47, 0, -1.67,
            90, 55, -90)
        pole.setScale(0.8)
        
        pole.setDepthTest(1)
        pole.setDepthWrite(1)

        frame = self.makeFrame()
        frame.attachNewNode(pole.node())

        name = "pole-item-%s" % (self.sequenceNumber)
        CatalogPoleItem.sequenceNumber += 1

        # Not sure if this looks good or not.  This interval makes the
        # pole slowly wind and unwind.  For now, we'll just put in an
        # interval that leaves the pole posed at its wound frame.  (We
        # have to use an interval instead of just posing the actor and
        # forgetting it, because otherwise the Actor python object
        # will destruct and forget about the pose.)
        
##         track = Sequence(ActorInterval(pole, 'cast', startFrame=84, endFrame=130),
##                          ActorInterval(pole, 'cast', startFrame=130, endFrame=84),
##                          Wait(2),
##                          name = name)
        track = Sequence(Func(pole.pose, 'cast', 130),
                         Wait(100),
                         name = name)
        assert (not self.hasPicture)
        self.hasPicture=True

        return (frame, track)

    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptPole
        elif retcode == ToontownGlobals.P_ItemUnneeded:
            return TTLocalizer.CatalogAcceptPoleUnneeded
            
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def output(self, store = ~0):
        return "CatalogPoleItem(%s%s)" % (
            self.rodId,
            self.formatOptionalData(store))

    def getFilename(self):
        return FishGlobals.RodFileDict.get(self.rodId)

    def compareTo(self, other):
        return self.rodId - other.rodId

    def getHashContents(self):
        return self.rodId

    def getBasePrice(self):
        return FishGlobals.RodPriceDict[self.rodId]

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.rodId = di.getUint8()

        # The following will generate an exception if self.rodId is
        # invalid.
        price = FishGlobals.RodPriceDict[self.rodId]

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.rodId)
        

def nextAvailablePole(avatar, duplicateItems):
    rodId = avatar.getFishingRod() + 1
    if rodId > FishGlobals.MaxRodId:
        # No more fishing rods for this avatar.
        return None

    item = CatalogPoleItem(rodId)

    # But if this rod is already on order, don't offer the same rod
    # again.  Skip to the next one instead.
    while item in avatar.onOrder or \
          item in avatar.mailboxContents:
        rodId += 1
        if rodId > FishGlobals.MaxRodId:
            return None
        item = CatalogPoleItem(rodId)

    return item

def getAllPoles():
    list = []
    for rodId in range(0, FishGlobals.MaxRodId + 1):
        list.append(CatalogPoleItem(rodId))
    return list
