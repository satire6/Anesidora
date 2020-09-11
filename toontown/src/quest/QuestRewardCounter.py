from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
import Quests
from toontown.toonbase import ToontownGlobals
from toontown.fishing import FishGlobals
from toontown.suit import SuitDNA
from toontown.racing import RaceGlobals
from toontown.estate import GardenGlobals
from toontown.golf import GolfGlobals

class QuestRewardCounter:
    """QuestRewardCounter

    This class is used by the AI to verify and repair the rewards a
    given toon should have been assigned, based on the quests he/she
    has already completed.

    """

    notify = directNotify.newCategory("QuestRewardCounter")
    
    # TODO: track progress

    def __init__(self):
        self.reset()

    def reset(self):
        self.maxHp = 15
        self.maxCarry = 20
        self.maxMoney = 40
        self.questCarryLimit = 1
        self.teleportAccess = []
        self.trackAccess = [0, 0, 0, 0, 1, 1, 0]
        self.trackProgressId = -1
        self.trackProgress = 0

    def addTeleportAccess(self, zoneId):
        if zoneId not in self.teleportAccess:
            self.teleportAccess.append(zoneId)

    def addTrackAccess(self, track):
        self.trackAccess[track] = 1

    def addTrackProgress(self, trackId, progressIndex):
        if self.trackProgressId != trackId:
            self.notify.warning("tried to update progress on a track toon is not training")
        self.trackProgress = self.trackProgress | (1 << progressIndex)

    def getTrackProgress(self):
        return self.trackProgressId, self.trackProgress

    def clearTrackProgress(self):
        self.trackProgressId = -1
        self.trackProgress = 0

    def setFromAvatar(self, av):
        # Set the rewards to indicate what the avatar would have after
        # applying all rewards up to but not including the current
        # reward index, and not including any currently active quests.

        # Get the list of current reward ID's.
        rewardIds = []

        for q in av.quests:
            questId, fromNpcId, toNpcId, rewardId, toonProgress = q
            if rewardId == Quests.NA:
                rewardId = Quests.getFinalRewardId(questId, fAll = 1)
            rewardIds.append(rewardId)

        self.notify.debug("Ignoring rewards: %s" % (rewardIds))
        
        self.setRewardIndex(av.rewardTier, rewardIds, av.rewardHistory)

        # add maxHp for fishCollection
        fishHp = int(len(av.fishCollection) / FishGlobals.FISH_PER_BONUS)
        self.notify.debug("Adding %s hp for fish collection" % (fishHp))
        self.maxHp += fishHp

        # add maxHp for flowerCollection
        flowerHp = int(len(av.flowerCollection) / GardenGlobals.FLOWERS_PER_BONUS)
        self.notify.debug("Adding %s hp for fish collection" % (flowerHp))
        self.maxHp += flowerHp        

        # add maxHp for HQ cog suit
        HQdepts = (
            # add depts as the HQs are released
            ToontownGlobals.cogHQZoneId2deptIndex(ToontownGlobals.SellbotHQ),
            #ToontownGlobals.cogHQZoneId2deptIndex(ToontownGlobals.BossbotHQ),
            ToontownGlobals.cogHQZoneId2deptIndex(ToontownGlobals.LawbotHQ),
            ToontownGlobals.cogHQZoneId2deptIndex(ToontownGlobals.CashbotHQ),
            )
        levels = av.getCogLevels()
        cogTypes = av.getCogTypes()
        suitHp = 0
        for dept in HQdepts:
            level = levels[dept]
            type = cogTypes[dept]
            if type >= (SuitDNA.suitsPerDept - 1):
                # add 1 HP for every milestone level they've hit
                for milestoneLevel in ToontownGlobals.CogSuitHPLevels:
                    if level >= milestoneLevel:
                        suitHp += 1
                    else:
                        break
        self.notify.debug("Adding %s hp for cog suits" % (suitHp))
        self.maxHp += suitHp

        # add maxHp for karting trophies
        kartingHp = int(av.kartingTrophies.count(1) / RaceGlobals.TrophiesPerCup)
        self.notify.debug("Adding %s hp for karting trophies" % (kartingHp))
        self.maxHp += kartingHp

        # add maxHp for golf trophies
        golfHp = int (av.golfTrophies.count(True) / GolfGlobals.TrophiesPerCup)
        self.notify.debug("Adding %s hp for golf trophies" % (golfHp))
        self.maxHp += golfHp

    def setRewardIndex(self, tier, rewardIds, rewardHistory):
        self.reset()

        # Fill in all the tiers up to this one unconditionally
        for tierNum in range(tier):
            for rewardId in Quests.getRewardsInTier(tierNum):

                # TODO: what about rewards on the previous tier?
                #if ((rewardIds.count(rewardId) != 0) and
                #    (rewardId is not in [100, 101, 102, 103, 104, 105, 106, 107, 108, 109])):
                #    # This is a reward we're still working on.
                #    rewardIds.remove(rewardId)
                #    self.notify.debug("Ignoring reward %d" % (rewardId))

                reward = Quests.getReward(rewardId)
                reward.countReward(self)
                self.notify.debug("Assigning reward %d" % (rewardId))

        # For the current tier, only give credit for rewards we have completed
        #print 'rewardHistory: ', rewardHistory
        for rewardId in rewardHistory:
            # Only count required rewards
            if rewardId in Quests.getRewardsInTier(tier):
                if rewardIds.count(rewardId) != 0:
                    # This is a reward we're still working on.
                    #print 'before: ', rewardIds
                    rewardIds.remove(rewardId)
                    self.notify.debug("Ignoring reward %d" % (rewardId))
                    #print 'after: ', rewardIds
                else:
                    reward = Quests.getReward(rewardId)
                    reward.countReward(self)
                    self.notify.debug("Assigning reward %d" % (rewardId))

        self.notify.debug("Remaining rewardIds %s" % (rewardIds))

        # Make sure maxHp does not exceed its maximum.
        self.maxHp = min(ToontownGlobals.MaxHpLimit, self.maxHp)

    def assignReward(self, rewardId, rewardIds):
        if rewardIds.count(rewardId) != 0:
            # This is a reward we're still working on.
            rewardIds.remove(rewardId)
            self.notify.debug("Ignoring reward %d" % (rewardId))
        else:
            reward = Quests.getReward(rewardId)
            reward.countReward(self)
            self.notify.debug("Assigning reward %d" % (rewardId))
        
    def fixAvatar(self, av):
        """fixAvatar(self, DistributedAvatarAI av)

        This is called from the AI side to reset an avatar to match
        his computed QuestRewards.  Returns 1 if the avatar was
        changed, or 0 if it already matched.

        """
        self.setFromAvatar(av)

        anyChanged = 0

        if (self.maxHp != av.maxHp):
            self.notify.info("Changed avatar %d to have maxHp %d instead of %d" % (av.doId, self.maxHp, av.maxHp))
            av.b_setMaxHp(self.maxHp)
            anyChanged = 1

        if (self.maxCarry != av.maxCarry):
            self.notify.info("Changed avatar %d to have maxCarry %d instead of %d" % (av.doId, self.maxCarry, av.maxCarry))
            av.b_setMaxCarry(self.maxCarry)
            anyChanged = 1
            
        if (self.maxMoney != av.maxMoney):
            self.notify.info("Changed avatar %d to have maxMoney %d instead of %d" % (av.doId, self.maxMoney, av.maxMoney))
            av.b_setMaxMoney(self.maxMoney)
            anyChanged = 1
            
        if (self.questCarryLimit != av.questCarryLimit):
            self.notify.info("Changed avatar %d to have questCarryLimit %d instead of %d" % (av.doId, self.questCarryLimit, av.questCarryLimit))
            av.b_setQuestCarryLimit(self.questCarryLimit)
            anyChanged = 1
            
        if (self.teleportAccess != av.teleportZoneArray):
            self.notify.info("Changed avatar %d to have teleportAccess %s instead of %s" % (av.doId, self.teleportAccess, av.teleportZoneArray))
            av.b_setTeleportAccess(self.teleportAccess)
            anyChanged = 1
            
        if (self.trackAccess != av.trackArray):
            self.notify.info("Changed avatar %d to have trackAccess %s instead of %s" % (av.doId, self.trackAccess, av.trackArray))
            av.b_setTrackAccess(self.trackAccess)
            anyChanged = 1

        if av.fixTrackAccess():
            anyChanged = 1

        return anyChanged
