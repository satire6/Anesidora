from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownBattleGlobals
from toontown.suit import SuitDNA

# This file contains a collection of functions to manage battle
# experience and generation of reward movies on the AI side.  These
# functions used to be methods on DistributedBattleBaseAI,
# BattleCalculatorAI, and Movie, but they have been pulled out here to
# collect them together and generalize them for final battles, which
# might have as many as 8 Toons.

BattleExperienceAINotify = DirectNotifyGlobal.directNotify.newCategory('BattleExprienceAI')

def getSkillGained(toonSkillPtsGained, toonId, track):
    """
    ////////////////////////////////////////////////////////////////////
    // Function:    get the skill points obtained so far in this battle
    //              for a toon position and a specific attack track
    // Parameters:  toonSlot, which toon to get the skill points for
    //              track, the attack track to get the skill pts for
    // Changes:
    // Returns:     skill points received so far in this battle
    ////////////////////////////////////////////////////////////////////
    """
    exp = 0
    expList = toonSkillPtsGained.get(toonId, None)
    if expList != None:
        exp = expList[track]
    return int(exp + 0.5)

def getBattleExperience(numToons, activeToons, toonExp,
                        toonSkillPtsGained, toonOrigQuests, toonItems,
                        toonOrigMerits, toonMerits,
                        toonParts, suitsKilled, helpfulToonsList = None):
    # First, build a list of active toons for the quest manager
    if helpfulToonsList == None:
        BattleExperienceAINotify.warning("=============\nERROR ERROR helpfulToons=None in assignRewards , tell Red")
        if __debug__:
            import pdb; pdb.set_trace()
    
    p = []
    for k in range(numToons):
        toon = None
        if (k < len(activeToons)):
            toonId = activeToons[k]
            toon = simbase.air.doId2do.get(toonId)

        if (toon == None):
            p.append(-1)
            p.append([0, 0, 0, 0, 0, 0, 0])
            p.append([0, 0, 0, 0, 0, 0, 0])
            p.append([]) # orig quests
            p.append([]) # items
            p.append([]) # missed items
            p.append([0, 0, 0, 0]) # orig merits                
            p.append([0, 0, 0, 0]) # merits
            p.append([0, 0, 0, 0]) # parts
        else:
            assert(toon.doId == toonId)
            p.append(toonId)
            origExp = toonExp[toonId]
            earnedExp = []
            for i in range(len(ToontownBattleGlobals.Tracks)):
                earnedExp.append(getSkillGained(toonSkillPtsGained, toonId, i))
            p.append(origExp)
            p.append(earnedExp)
            origQuests = toonOrigQuests.get(toonId, [])
            p.append(origQuests)
            items = toonItems.get(toonId, ([], []))
            p.append(items[0])
            p.append(items[1])
            origMerits = toonOrigMerits.get(toonId, [])
            p.append(origMerits)
            merits = toonMerits.get(toonId, [0, 0, 0, 0])                
            p.append(merits)
            parts = toonParts.get(toonId, [0, 0, 0, 0])                
            p.append(parts)


    # Now make a list of the suits that were killed so we can update
    # quest progress during the movie
    deathList = []
    # create a lookup table of the indices of the active toons
    toonIndices = {}
    for i in range(len(activeToons)):
        # map toonId -> toon's battle index
        toonIndices[activeToons[i]] = i
    for deathRecord in suitsKilled:
        # Record the suit index and the suit level
        level = deathRecord['level']
        type = deathRecord['type']
        if deathRecord['isVP'] or deathRecord['isCFO']:
            # VPs/CFOs are not 'cogs' per se
            # they have no level or type; they only have a track
            # pass dept index as type. This, combined with isVP/isCFO flag,
            # uniquely identifies VPs/CFOs.
            level = 0
            typeNum = SuitDNA.suitDepts.index(deathRecord['track'])
        else:
            # Convert the type (name string) into an int to pass on the network
            typeNum = SuitDNA.suitHeadTypes.index(type)

        # create a bitmask that represents which toons were involved
        involvedToonIds = deathRecord['activeToons']
        toonBits = 0
        for toonId in involvedToonIds:
            if toonId in toonIndices:
                toonBits |= (1 << toonIndices[toonId])

        # create a flags byte w/ extra info
        flags = 0
        if deathRecord['isSkelecog']:
            flags |= ToontownBattleGlobals.DLF_SKELECOG
        if deathRecord['isForeman']:
            flags |= ToontownBattleGlobals.DLF_FOREMAN
        if deathRecord['isVP']:
            flags |= ToontownBattleGlobals.DLF_VP
        if deathRecord['isCFO']:
            flags |= ToontownBattleGlobals.DLF_CFO
        if deathRecord['isSupervisor']:
            flags |= ToontownBattleGlobals.DLF_SUPERVISOR
        if deathRecord['isVirtual']:
            flags |= ToontownBattleGlobals.DLF_VIRTUAL
        if ("hasRevies" in deathRecord) and (deathRecord['hasRevives']):
            flags |= ToontownBattleGlobals.DLF_REVIVES
        deathList.extend([typeNum, level, toonBits, flags])
    # Put the deathList in the master array
    p.append(deathList)
    
    
    #add the bitfields of the toons ubergags
    #print("activeToons %s" % (activeToons))
    uberStats = getToonUberStatus(activeToons, numToons)
    #uberStats = [77,42]
    #print(uberStats)
    p.append(uberStats)
    #import pdb; pdb.set_trace()
    #p.append([77,42])

    if helpfulToonsList == None:
        helpfulToonsList = []
    p.append(helpfulToonsList)

    return p
    
def getToonUberStatus(toons, numToons):
    #UBERCHANGE
    #print("getToonUberStatus")

    fieldList = []
    uberIndex = ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1
    for toonId in toons:
        toonList = []
        toon = simbase.air.doId2do.get(toonId)
        if toon == None:
            #toonList = [0,0,0,0,0,0,0]
            fieldList.append(-1)
        else:
            for trackIndex in range(ToontownBattleGlobals.MAX_TRACK_INDEX + 1):
                toonList.append(toon.inventory.numItem(trackIndex, uberIndex))
            fieldList.append(ToontownBattleGlobals.encodeUber(toonList))
    lenDif = numToons - len(toons)
    if lenDif > 0:
        for index in range(lenDif):
            fieldList.append(-1)
    #print(fieldList) 
    return fieldList


def assignRewards(activeToons, toonSkillPtsGained, suitsKilled, zoneId, helpfulToons=None):
    # First, build a list of active toons for the quest manager
    if helpfulToons == None:
        BattleExperienceAINotify.warning("=============\nERROR ERROR helpfulToons=None in assignRewards , tell Red")
        if __debug__:
            import pdb; pdb.set_trace()
        
    activeToonList = []
    for t in activeToons:
        toon = simbase.air.doId2do.get(t)
        if (toon != None):
            activeToonList.append(toon)

    # Now walk through the list and add the gained experience to each
    # toon.
    for toon in activeToonList:
        for i in range(len(ToontownBattleGlobals.Tracks)):
            
            uberIndex = ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1
            exp = getSkillGained(toonSkillPtsGained, toon.doId, i)
            needed = ToontownBattleGlobals.Levels[i][ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1] + ToontownBattleGlobals.UberSkill
            #print("Track %s Needed %s Current %s" % (ToontownBattleGlobals.Tracks[i], needed, exp + toon.experience.getExp(i)))
            assert(exp >= 0)
            hasUber = 0
            totalExp = exp + toon.experience.getExp(i)
            if (toon.inventory.numItem(i, uberIndex) > 0):
                hasUber = 1
            if (totalExp >= (needed)) or (totalExp >= ToontownBattleGlobals.MaxSkill):
            #the toon has exceeded the uberGag tredmill threshold 
            #and needs to be awarded the USE of an ubergag
            #then the toon should have their exp level reduced to the amount needed to have the uber gag
                #print("uber threshold met")
                if toon.inventory.totalProps < toon.getMaxCarry() and not hasUber:
                #make sure the toon has room for the uber gag
                    #print("adding uber gag")
                    uberLevel = ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1
                    #need to hang this and assign it after the toons play their movies
                    #taskMgr.doMethodLater(3.0, toon.inventory.addItem, 'ToT-phrase-reset', extraArgs=[i, uberLevel])
                    toon.inventory.addItem(i, uberLevel)
                    toon.experience.setExp(i, ToontownBattleGlobals.Levels[i][ToontownBattleGlobals.LAST_REGULAR_GAG_LEVEL + 1])
                else:
                    toon.experience.setExp(i, ToontownBattleGlobals.MaxSkill)
                    pass
                    #print("full not adding ubergag")
            elif (exp > 0):
                #print("regular exp")
                newGagList = toon.experience.getNewGagIndexList(i, exp)
                toon.experience.addExp(i, amount=exp)
                toon.inventory.addItemWithList(i, newGagList)


        toon.b_setExperience(toon.experience.makeNetString())
        toon.d_setInventory(toon.inventory.makeNetString())

        # The AI starts each toon dancing.  Each client will
        # eventually be responsible for stopping the dance,
        # after the client has viewed the entire reward movie.
        # This means that all toons will start dancing at the
        # same time, but they may not all end at the same time.
        toon.b_setAnimState('victory', 1)

        # Tell the quest manager about the cogs this toon killed
        # so it can update the quest progress
        if simbase.air.config.GetBool('battle-passing-no-credit', True):
            # toons who just pass all the time will not get the quest credit
            if helpfulToons and (toon.doId in helpfulToons):
                simbase.air.questManager.toonKilledCogs(toon, suitsKilled, zoneId, activeToonList)
                # Tell the cog page manager about the cogs this toon killed
                simbase.air.cogPageManager.toonKilledCogs(toon, suitsKilled, zoneId)
            else:
                BattleExperienceAINotify.debug('toon=%d unhelpful not getting killed cog quest credit' % toon.doId)
        else:
            simbase.air.questManager.toonKilledCogs(toon, suitsKilled, zoneId, activeToonList)
            # Tell the cog page manager about the cogs this toon killed
            simbase.air.cogPageManager.toonKilledCogs(toon, suitsKilled, zoneId)
            
        
