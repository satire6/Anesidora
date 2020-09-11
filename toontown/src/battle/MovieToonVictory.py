from direct.interval.IntervalGlobal import *
from RewardPanel import *
from BattleSounds import *

import MovieCamera
from direct.directnotify import DirectNotifyGlobal
import types

notify = DirectNotifyGlobal.directNotify.newCategory('MovieToonVictory')

def __findToonReward(rewards, toon):
    for r in rewards:
        if (r['toon'] == toon):
            return r
    return None

def doToonVictory(localToonActive, toons, rewardToonIds, rewardDicts,
                  deathList, rpanel, allowGroupShot = 1, uberList = [], helpfulToonsList= []):
    track = Sequence()
    if (localToonActive == 1):
        track.append(Func(rpanel.show))
        track.append(Func(NametagGlobals.setOnscreenChatForced, 1))
        
    camTrack = Sequence()
    endTrack = Sequence()
    danceSound = globalBattleSoundCache.getSound('ENC_Win.mp3')

    # The toons list might be a list of toons, or it might be a list
    # of toonId's.  In either case, build a list of toons out of it.
    toonList = []
    countToons = 0
    uberListNew = []
    for t in toons:
        if isinstance(t, types.IntType):
            t = base.cr.doId2do.get(t)
        if t:
            toonList.append(t)
            uberListNew.append(uberList[countToons])
        countToons += 1
        

    # make a list of toons/None from the rewardToonIds list. This list
    # corresponds with the bitmasks embedded in the deathList. We need this
    # in case a toon leaves in between the creation of the bitmasks and
    # the client-side interpretation of them. (the bitmasks tell us who
    # of the remaining toons was around when each cog was defeated)
    toonId2toon = {}
    for toon in toonList:
        toonId2toon[toon.doId] = toon
    rewardToonList = []
    for id in rewardToonIds:
        rewardToonList.append(toonId2toon.get(id))

    for tIndex in range(len(toonList)):
        t = toonList[tIndex]
        rdict = __findToonReward(rewardDicts, t)
        # To prevent client from crashing in this case.
        if rdict != None:
            expTrack = rpanel.getExpTrack(t, rdict['origExp'], rdict['earnedExp'],
                                          deathList, rdict['origQuests'], rdict['items'], rdict['missedItems'],
                                          rdict['origMerits'], rdict['merits'],
                                          rdict['parts'], rewardToonList, uberListNew[tIndex],
                                          helpfulToonsList)
            if expTrack:
                track.append(expTrack)
                camDuration = expTrack.getDuration()
                camExpTrack = MovieCamera.chooseRewardShot(t, camDuration)
                assert camDuration == camExpTrack.getDuration()
                camTrack.append(MovieCamera.chooseRewardShot(
                    t, camDuration, allowGroupShot = allowGroupShot))
    if (localToonActive == 1):
        track.append(Func(rpanel.hide))
        track.append(Func(NametagGlobals.setOnscreenChatForced, 0))
    track.append(endTrack)
    trackdur = track.getDuration()
    soundTrack = SoundInterval(danceSound, duration=trackdur, loop=1)
    mtrack = Parallel(track, soundTrack)

    return (mtrack, camTrack)

