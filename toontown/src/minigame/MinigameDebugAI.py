from toontown.toonbase import ToontownGlobals

import DistributedRaceGameAI
import DistributedCannonGameAI

# TO START A MINIGAME:

# call getLocalAvId() on the client to print your local toon's avatar ID

# call this first on the AI server
# pass in a minigame ID (from ToontownGlobals)
# pass in your avatar's ID as the 2nd parameter
# pass in 1-3 other avatars' IDs (it might work...), or let them be suits
def startMinigameAI(minigameId, avID, avID2=1, avID3=2, avID4=3):
    # Trolley manager code:
    # allocate a zone
    zoneId = simbase.air.allocateZone()
    # Create the minigame
    if minigameId == ToontownGlobals.RaceGameId:
        mg = DistributedRaceGameAI.DistributedRaceGameAI(simbase.air)
    elif minigameId == ToontownGlobals.CannonGameId:
        mg = DistributedCannonGameAI.DistributedCannonGameAI(simbase.air)
    # Generate it in that zone
    mg.generateWithRequired(zoneId)
    # set the expected avatars directly
    # (I do not think this needs to be an update)
    mg.setExpectedAvatars(avID, avID2, avID3, avID4)
    print "zoneId = " + str(zoneId)

# call startMinigame() on the client
