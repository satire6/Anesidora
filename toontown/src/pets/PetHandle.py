from toontown.toonbase import ToontownGlobals
from toontown.pets import PetMood, PetTraits, PetDetail

class PetHandle:
    """PetHandle

    This is a class object that serves as a structure to hold all the
    details we are entitled to find out about a pet. 

    """

    def __init__(self, avatar):
        self.doId = avatar.doId
        self.name = avatar.name
        self.style = avatar.style
        self.ownerId = avatar.ownerId
        self.bFake = False

        self.cr = avatar.cr
        self.traits = PetTraits.PetTraits(avatar.traitSeed, avatar.safeZone,
                                          traitValueList=avatar.traitList)
        self._grabMood(avatar)

    def _grabMood(self, avatar):
        # make a copy of the avatar's mood manager. we need to have a
        # self.traits first.
        self.mood = avatar.lastKnownMood.makeCopy()
        self.mood.setPet(self)
        self.lastKnownMood = self.mood.makeCopy()
        self.setLastSeenTimestamp(avatar.lastSeenTimestamp)
        # and calculate the current mood
        self.updateOfflineMood()

    def getDoId(self):
        """getDoId(self)
        Return the distributed object id
        """
        return self.doId

    def getOwnerId(self):
        return self.ownerId

    def isPet(self):
        return True

    def getName(self):
        return self.name

    def getDNA(self):
        return self.style

    def getFont(self):
        # All friends are toons.
        return ToontownGlobals.getToonFont()

    def setLastSeenTimestamp(self, timestamp):
        self.lastSeenTimestamp = timestamp

    def getTimeSinceLastSeen(self):
        # returns time since pet was last seen on the AI
        t = self.cr.getServerTimeOfDay() - self.lastSeenTimestamp
        return max(0., t)

    def updateOfflineMood(self):
        # Used by the client to figure out what the pet's mood is when
        # the pet is not currently instantiated on the AI. Once the pet's
        # last-known-mood fields and last-seen timestamp are filled in,
        # and the object is 'fake-generated', you can call this at any
        # time to recalculate the pet's mood.
        self.mood.driftMood(dt=self.getTimeSinceLastSeen(),
                            curMood=self.lastKnownMood)

    def getDominantMood(self):
        # there are situations where this is being called by PetAvatarPanel
        # before we're fully generated. Not a big deal if the panel erroneously
        # shows the pet as neutral
        if not hasattr(self, 'mood'):
            return PetMood.PetMood.Neutral
        return self.mood.getDominantMood()

    def uniqueName(self, idString):
        return (idString + "-" + str(self.getDoId()))

    def updateMoodFromServer(self, callWhenDone=None):
        # call this to query the server for an up-to-date mood
        def handleGotDetails(avatar, callWhenDone=callWhenDone):
            self._grabMood(avatar)
            if callWhenDone:
                callWhenDone()
        PetDetail.PetDetail(self.doId, handleGotDetails)
        
