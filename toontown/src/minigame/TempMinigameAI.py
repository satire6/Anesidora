"""
@author: Schell Games
3-16-2010

Allows the creation of temp minigames for testing new game ideas
under the minigame framework without hard-coding them in.
"""
from toontown.toonbase import ToontownGlobals

# This config allows devs to temporarily register temp games created with the minigame framework
ALLOW_TEMP_MINIGAMES = simbase.config.GetBool('allow-temp-minigames', False)

TEMP_MG_ID_COUNTER = ToontownGlobals.TravelGameId - 1

TempMgCtors = {}

def _printMessage(message):
    print "\n\n!!!", message, "\n\n"

def _registerTempMinigame(name, Class, id, minPlayers=1, maxPlayers=4):
    """
    Temporarily registers a minigame in toontown.
    Can be used for prototyping a new idea under the minigame framework without hardcoding.
    allow-temp-minigames config has to be set to true
    """
    if not ALLOW_TEMP_MINIGAMES:
        _printMessage("registerTempMinigame WARNING: allow-temp-minigames config is set to false, but we are trying to register temp minigame " + name)
        import traceback
        traceback.print_stack()
        return

    assert minPlayers >= 1 and minPlayers <= 4 and maxPlayers >=1 and maxPlayers <= 4 and minPlayers <= maxPlayers
    assert ToontownGlobals.MinigameNames.has_key(name) == False
    assert id is not None and id not in ToontownGlobals.MinigameIDs and id < ToontownGlobals.TravelGameId

    ToontownGlobals.MinigameIDs += (id,)
    ToontownGlobals.MinigameNames[name] = id

    TempMgCtors[id] = Class

    for i in range(minPlayers, maxPlayers):
        ToontownGlobals.MinigamePlayerMatrix[i] += (id,)

    _printMessage("registerTempMinigame: " + name)


#------------------------------------------------------------------------------
# Temp Minigames
# Please remove when done with them!
# What to do:
# 1. Create AI/client class
# 2. Add the empty declaration to the DC file
# 3. Register right here with a custom name, and give it an id >= 50 and < 100
if ALLOW_TEMP_MINIGAMES:
    from toontown.cogdominium.DistCogdoMazeGameAI import DistCogdoMazeGameAI
    _registerTempMinigame("cogdomaze", DistCogdoMazeGameAI, id=50)

    from toontown.cogdominium.DistCogdoFlyingGameAI import DistCogdoFlyingGameAI
    _registerTempMinigame("cogdoflying", DistCogdoFlyingGameAI, id=51)

    pass

