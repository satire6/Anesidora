from toontown.toonbase.ToontownGlobals import *

# TO START A MINIGAME:

# call this on the client to print your local toon's avatar ID
def getLocalAvId():
    print str(base.localAvatar.doId)

# call startMinigameAI() on the AI server (see MinigameDebugAI.py)

# call this on the client
# pass in the same minigameID as passed to startMinigameAI()
# pass in the zoneId that was printed out by startMinigameAI()
def startMinigame(minigameID, zoneId):
    base.cr.playGame.hood.loader.debugStartMinigame(zoneId, minigameID)
