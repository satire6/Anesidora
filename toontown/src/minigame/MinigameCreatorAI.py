import copy
import random
import time

from toontown.toonbase import ToontownGlobals

# Import all the minigames because we create them
import DistributedMinigameTemplateAI
import DistributedRaceGameAI
import DistributedCannonGameAI
import DistributedTagGameAI
import DistributedPatternGameAI
import DistributedRingGameAI
import DistributedMazeGameAI
import DistributedTugOfWarGameAI
import DistributedCatchGameAI
import DistributedDivingGameAI
import DistributedTargetGameAI
import DistributedPairingGameAI
import DistributedPhotoGameAI
import DistributedVineGameAI
import DistributedIceGameAI
import DistributedCogThiefGameAI
import DistributedTwoDGameAI
import DistributedTravelGameAI
import TravelGameGlobals

#------------------------------------------------------------------------------
# This config allows devs to temporarily register temp games created with the minigame framework
ALLOW_TEMP_MINIGAMES = simbase.config.GetBool('allow-temp-minigames', False)

if ALLOW_TEMP_MINIGAMES:
    # Import temp minigames
    from toontown.minigame.TempMinigameAI import *
#------------------------------------------------------------------------------

# put this on simbase so that it's easy to change on-the-fly
simbase.forcedMinigameId = simbase.config.GetInt('minigame-id', 0)

# This map is only used for support of the magic word ~minigame
RequestMinigame = {}

# this map is used to track minigame zone reference counts
MinigameZoneRefs = {}

def createMinigame(air, playerArray, trolleyZone,
                   minigameZone = None,
                   previousGameId = ToontownGlobals.NoPreviousGameId,
                   newbieIds = [],
                   startingVotes = None,
                   metagameRound = -1,
                   desiredNextGame = None):
    if minigameZone == None:
        minigameZone = air.allocateZone()

    acquireMinigameZone(minigameZone)

    mgId = None
    mgDiff = None
    mgSzId = None
    # Check for a specifically requested minigame from one of the players.
    for avId in playerArray:
        request = RequestMinigame.get(avId)
        if request != None:
            mgId, mgKeep, mgDiff, mgSzId = request
            if not mgKeep:
                del RequestMinigame[avId]
            break

    if mgId != None:
        # One of the players requested a particular minigame via
        # ~minigame; no need to pick another one.
        pass
    elif simbase.forcedMinigameId:
        # A particular minigame was forced using the Configrc option
        # minigame-id.
        mgId = simbase.forcedMinigameId
    else:
        # The normal path: choose a random minigame.
        randomList = list(copy.copy(ToontownGlobals.MinigamePlayerMatrix[len(playerArray)]))

        # when debugging minigames, it's useful to be able to play all
        # of the multi-player games with only two toons, even if some of
        # them normally require three or four toons
        if simbase.air.useAllMinigames and (len(playerArray) > 1):
            randomList = list(copy.copy(ToontownGlobals.MinigameIDs))
            # don't include these games until they're ready
            for gameId in [ToontownGlobals.TravelGameId]:
                if gameId in randomList:
                    randomList.remove(gameId)

        # we never want to get travel game as a regular minigame
        for gameId in [ToontownGlobals.TravelGameId]:
            if gameId in randomList:
                randomList.remove(gameId)

        # Never play the same game twice in a row
        if previousGameId != ToontownGlobals.NoPreviousGameId:
            # We might have just switched from multiplayer to
            # single-player minigames, which changes the pool of
            # minigames we have to draw from.  Thus, it's possible our
            # previousGameId is not in randomList.
            if randomList.count(previousGameId) != 0:
                randomList.remove(previousGameId)

        # remove our unreleased minigames
        randomList = removeUnreleasedMinigames(randomList, True)

        mgId = random.choice(randomList)

        if (metagameRound > -1):
            if (metagameRound % 2 == 0):
                #we must start a trolley metagame
                mgId = ToontownGlobals.TravelGameId
            elif desiredNextGame:
                mgId = desiredNextGame

    # Create the minigame
    mgCtors = {
        ToontownGlobals.RaceGameId: DistributedRaceGameAI.DistributedRaceGameAI,
        ToontownGlobals.CannonGameId: DistributedCannonGameAI.DistributedCannonGameAI,
        ToontownGlobals.TagGameId: DistributedTagGameAI.DistributedTagGameAI,
        ToontownGlobals.PatternGameId: DistributedPatternGameAI.DistributedPatternGameAI,
        ToontownGlobals.RingGameId: DistributedRingGameAI.DistributedRingGameAI,
        ToontownGlobals.MazeGameId: DistributedMazeGameAI.DistributedMazeGameAI,
        ToontownGlobals.TugOfWarGameId: DistributedTugOfWarGameAI.DistributedTugOfWarGameAI,
        ToontownGlobals.CatchGameId: DistributedCatchGameAI.DistributedCatchGameAI,
        ToontownGlobals.DivingGameId: DistributedDivingGameAI.DistributedDivingGameAI,
        ToontownGlobals.TargetGameId: DistributedTargetGameAI.DistributedTargetGameAI,
        ToontownGlobals.MinigameTemplateId: DistributedMinigameTemplateAI.DistributedMinigameTemplateAI,
        ToontownGlobals.PairingGameId : DistributedPairingGameAI.DistributedPairingGameAI,
        ToontownGlobals.VineGameId: DistributedVineGameAI.DistributedVineGameAI,
        ToontownGlobals.IceGameId : DistributedIceGameAI.DistributedIceGameAI,
        ToontownGlobals.CogThiefGameId : DistributedCogThiefGameAI.DistributedCogThiefGameAI,
        ToontownGlobals.TwoDGameId : DistributedTwoDGameAI.DistributedTwoDGameAI,
        ToontownGlobals.TravelGameId : DistributedTravelGameAI.DistributedTravelGameAI,
        ToontownGlobals.PhotoGameId: DistributedPhotoGameAI.DistributedPhotoGameAI,
        }


    if ALLOW_TEMP_MINIGAMES:
        # Adds the temp minigames to the list of minigame creators...
        from TempMinigameAI import TempMgCtors

        for key, value in TempMgCtors.items():
            mgCtors[key] = value


    """
    print "\n\n\n\n\n\n\n\n\n\n"

    print mgCtors
    print air
    print mgId
    print mgCtors[mgId]
    print mgCtors[mgId](air,mgId)

    print "\n\n\n\n\n\n\n\n\n\n"
    """
    try:
        #import pdb; pdb.set_trace()
        mg = mgCtors[mgId](air, mgId)
    except KeyError:
        raise Exception, "unknown minigame ID: %s" % mgId

    # Tell the minigame who we are expecting
    # do this before generating the minigame;
    # the av list is a required field
    mg.setExpectedAvatars(playerArray)
    # tell the minigame which players are playing their first minigame
    mg.setNewbieIds(newbieIds)
    # set trolley zone; another required field
    mg.setTrolleyZone(trolleyZone)
    # set the difficulty overrides
    mg.setDifficultyOverrides(mgDiff, mgSzId)

    # set the needed info for the trolley metagame
    if startingVotes == None:
        for avId in playerArray:
            mg.setStartingVote(avId, TravelGameGlobals.DefaultStartingVotes )
            #print('setting starting vote of %d to %d default' % (avId,TravelGameGlobals.DefaultStartingVotes))
    else:
        for index in range(len(startingVotes)):
            avId = playerArray[index]
            votes = startingVotes[index]
            if votes < 0:
                print('createMinigame negative votes, avId=%s votes=%s' %(avId, votes))
                votes = 0
            mg.setStartingVote(avId, votes )
            #print('setting starting vote of %d to %d' % (avId,votes))

    mg.setMetagameRound(metagameRound)


    # Generate it in that zone
    # this will kick off the minigame's ClassicFSM
    mg.generateWithRequired(minigameZone)

    # Notify the quest manager in case any toon had a minigame quest
    # TODO: should this be done AFTER the minigame, so that people can't get
    # out of newbie quests by hopping on the trolley and alt+F4-ing? Don't
    # if people are doing that. Maybe better to give credit to people that
    # crash during the game.
    toons = []
    for id in playerArray:
        toon = simbase.air.doId2do.get(id)
        if (toon != None):
            toons.append(toon)
    for toon in toons:
        simbase.air.questManager.toonPlayedMinigame(toon, toons)

    retVal = {}
    retVal["minigameZone"] = minigameZone
    retVal["minigameId"] = mgId

    return retVal

def acquireMinigameZone(zoneId):
    if not zoneId in MinigameZoneRefs:
        MinigameZoneRefs[zoneId] = 0
    MinigameZoneRefs[zoneId] += 1

def releaseMinigameZone(zoneId):
    MinigameZoneRefs[zoneId] -= 1
    if MinigameZoneRefs[zoneId] <= 0:
        del MinigameZoneRefs[zoneId]
        simbase.air.deallocateZone(zoneId)

def removeUnreleasedMinigames(startList, increaseChanceOfNewGames = 0):
    """Return a new list of minigames by removing the unreleased minigames."""
    randomList = startList[:]
    for gameId in ToontownGlobals.MinigameReleaseDates:
        dateTuple = ToontownGlobals.MinigameReleaseDates[gameId]
        currentTime = time.time()
        releaseTime = time.mktime((dateTuple[0], # year
                                   dateTuple[1], # month
                                   dateTuple[2], # day
                                   0, # hour
                                   0, # min
                                   0, # sec
                                   0, # wday
                                   0, # yday
                                   -1, # dst flag
                                   ))

        releaseTimePlus1Week = releaseTime + (7 * 24 *60 *60)

        if currentTime < releaseTime:
            if gameId in randomList:
                doRemove = True
                if gameId == ToontownGlobals.CogThiefGameId and \
                   simbase.air.config.GetBool('force-allow-thief-game',0):
                    doRemove = False
                    if increaseChanceOfNewGames:
                        randomList += [gameId]*4
                elif gameId == ToontownGlobals.IceGameId and \
                     simbase.air.config.GetBool('force-allow-ice-game',0):
                    doRemove = False
                    if increaseChanceOfNewGames:
                        randomList += [gameId]*4
                elif gameId == ToontownGlobals.TwoDGameId and \
                     simbase.air.config.GetBool('force-allow-2d-game', 0):
                    doRemove = False
                    if increaseChanceOfNewGames:
                        randomList += [gameId]*4
                elif gameId == ToontownGlobals.PhotoGameId and \
                     simbase.air.config.GetBool('force-allow-photo-game',0):
                    doRemove = False
                    if increaseChanceOfNewGames:
                        randomList += [gameId]*4
                if doRemove:
                    randomList.remove(gameId)

        # on live, one week after a new minigame is released, increase its chances
        if releaseTime < currentTime and \
           currentTime < releaseTimePlus1Week and \
           gameId in randomList and \
           increaseChanceOfNewGames:
            randomList += [gameId]*4

    return randomList
