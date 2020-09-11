from toontown.toonbase import ToontownBattleGlobals

# This file contains a collection of functions to manage battle
# experience and generation of reward movies on the client side.
# These functions used to be methods on DistributedBattleBase and
# Movie, but they have been pulled out here to collect them together
# and generalize them for final battles, which might have as many as 8
# Toons.


def genRewardDicts(entries):
    toonRewardDicts = []
    for toonId, origExp, earnedExp, origQuests, items, missedItems, origMerits, merits, parts in entries:
        if (toonId != -1):
            dict = {}
            toon = base.cr.doId2do.get(toonId)
            if (toon == None):
                continue
            dict['toon'] = toon
            dict['origExp'] = origExp
            dict['earnedExp'] = earnedExp
            dict['origQuests'] = origQuests
            dict['items'] = items
            dict['missedItems'] = missedItems
            dict['origMerits'] = origMerits
            dict['merits'] = merits
            dict['parts'] = parts
            toonRewardDicts.append(dict)
    #import pdb; pdb.set_trace()

    return toonRewardDicts
