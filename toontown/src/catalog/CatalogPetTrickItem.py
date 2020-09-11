import CatalogItem
from toontown.pets import PetTricks
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *

class CatalogPetTrickItem(CatalogItem.CatalogItem):
    """
    This represents a phrase you can say to teach your pet to do a
    particular trick.
    """

    sequenceNumber = 0
    petPicture = None
    def makeNewItem(self, trickId):
        self.trickId = trickId
        
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
        return self.trickId in avatar.petTrickPhrases
        
    def getAcceptItemErrorText(self, retcode):
        # Returns a string describing the error that occurred on
        # attempting to accept the item from the mailbox.  The input
        # parameter is the retcode returned by recordPurchase() or by
        # mailbox.acceptItem().
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptPet
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def saveHistory(self):
        # Returns true if items of this type should be saved in the
        # back catalog, false otherwise.
        return 1

    def getTypeName(self):
        return TTLocalizer.PetTrickTypeName

    def getName(self):
        phraseId = PetTricks.TrickId2scIds[self.trickId][0]
        return OTPLocalizer.SpeedChatStaticText[phraseId]

    def recordPurchase(self, avatar, optional):
        avatar.petTrickPhrases.append(self.trickId)
        avatar.d_setPetTrickPhrases(avatar.petTrickPhrases)
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        # Returns a (DirectWidget, Interval) pair to draw and animate a
        # little representation of the item, or (None, None) if the
        # item has no representation.  This method is only called on
        # the client.

        # Don't import this at the top of the file, since this code
        # must run on the AI.
        from toontown.pets import PetDNA, Pet

        pet = Pet.Pet(forGui = 1)

        # We use the avatar's own pet if he/she has a pet (and we know
        # its DNA), otherwise use a random pet.
        dna = avatar.petDNA
        if dna == None:
            dna = PetDNA.getRandomPetDNA()
        pet.setDNA(dna)
        
        pet.setH(180)
        model, ival = self.makeFrameModel(pet, 0)
        pet.setScale(2.0)
        pet.setP(-40)

        # Discard the ival from makeFrameModel, since we don't want to
        # spin.

        track = PetTricks.getTrickIval(pet, self.trickId)
        name = "petTrick-item-%s" % (self.sequenceNumber)
        CatalogPetTrickItem.sequenceNumber += 1
        if track != None:
            track = Sequence(Sequence(track),
                             ActorInterval(pet, 'neutral', duration = 2),
                             name = name)
        else:
            pet.animFSM.request('neutral')
            track = Sequence(Wait(4),
                             name = name)
        self.petPicture = pet

        assert (not self.hasPicture)
        self.hasPicture=True
        
        return (model, track)

    def cleanupPicture(self):
        CatalogItem.CatalogItem.cleanupPicture(self)
        assert self.petPicture
        self.petPicture.delete()
        self.petPicture = None
        
    def output(self, store = ~0):
        return "CatalogPetTrickItem(%s%s)" % (
            self.trickId,
            self.formatOptionalData(store))

    def compareTo(self, other):
        return self.trickId - other.trickId

    def getHashContents(self):
        return self.trickId

    def getBasePrice(self):
        # All petTricks are the same price for now.
        return 500

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.trickId = di.getUint8()
        self.dna = None
        if self.trickId not in PetTricks.TrickId2scIds:
            raise ValueError
        
    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.trickId)
        

def getAllPetTricks():
    # Returns a list of all valid CatalogPetTrickItems.
    list = []
    for trickId in PetTricks.TrickId2scIds.keys():
        list.append(CatalogPetTrickItem(trickId))

    return list

