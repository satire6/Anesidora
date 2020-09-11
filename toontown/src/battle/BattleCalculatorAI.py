from BattleBase import *
from DistributedBattleAI import *
from toontown.toonbase.ToontownBattleGlobals import *

import random
from toontown.suit import DistributedSuitBaseAI
import SuitBattleGlobals
import BattleExperienceAI
from toontown.toon import NPCToons
from toontown.pets import PetTricks, DistributedPetProxyAI
from direct.showbase.PythonUtil import lerp


class BattleCalculatorAI:
    """
    An object that each battle
    creates in order to perform all of the combat calculations, such
    as hits/misses, damage amounts, bonuses, etc
    
    Attributes:
        Derived plus...
        battle: reference to the battle that owns this object
        SuitAttackers: a map of suit id's and each toon that did damage
                       to that suit and how much damage was done, this is
                       used to let the suit 'intelligently' pick which
                       toon it is going to attack next, generally favoring
                       the toon that did the most damage to it
        currentlyLuredSuits: list of currently lured suits, used for
                             calculating knockback bonuses and drop
                             hits/misses during a single round (once a suit
                             takes damage, it is no longer lured)
        kbBonuses:  a list of accumulated damage done to a lured suit by
                    knockback bonus qualified attacks and the track of each
                    attack the damage was done by, when that track of
                    attacks is done a single, total knockback bonus is
                    applied to the suit
        hpBonuses:  same as kbBonuses but used to record knock-back bonuses
        toonAtkOrder: list of toon id's that indicate the order that the
                      toon attacks for a single round will play out
        toonHPAdjusts: a list of toon HP adjustments used for accurate
                       calculations of each toon's health, useful for
                       deciding if a toon has just died and cannot
                       perform its chosen attack as well as letting the
                       suits know if a toon dies so they dont beat on a dead
                       toon
        toonSkillPtsGained: a dictionary of lists of experience gained
                            in each track, indexed by toonId
    """

    # a map of the number of previous hits to
    # an accuracy bonus for the next attack
    AccuracyBonuses = [0, 20, 40, 60]

    # a map of the number of previous hits to
    # a damage bonus for the next attack
    DamageBonuses = [0, 20, 20, 20]

    # how much of an accuracy bonus a toon gets for each level of
    # an attack track
    AttackExpPerTrack = [0, 10, 20, 30, 40, 50, 60] #HARDCODE UBER

    # number of max rounds for targets to be lured for each different
    # level of lure
    NumRoundsLured = [2, 2, 3, 3, 4, 4, 15]

    # a trap level value placed in self.traps if more than one trap is
    # placed on a single suit within the same round, this value should not
    # be -1 (the value of NO_TRAP) or a valid level of 0 or greater
    TRAP_CONFLICT = -2

    # whether or not to apply healt adjustments to suits and toons when
    # damages are calculated from attacks
    APPLY_HEALTH_ADJUSTMENTS = 1

    # make attacks on toons always miss
    TOONS_TAKE_NO_DAMAGE     = 0

    # whether or not to reduce the reported attack damages to the
    # target's min and max hp
    CAP_HEALS                = 1

    # whether or not to clear the SuitAttackers map each round, this
    # way suits don't remember which toon attacked him/her for more than
    # a single round
    CLEAR_SUIT_ATTACKERS     = 1

    # a temporary flag until a more correct version of the movie is in place
    # which will unlure suits as soon as they are knocked back, rather than
    # waiting until the suits does his/her attack
    SUITS_UNLURED_IMMEDIATELY = 1

    # whether or not the battle calculator should clear out trap toon attacks
    # if there is already a trap on the target
    CLEAR_MULTIPLE_TRAPS     = 0

    # a flag placed in the KBBONUS_COL for a toon attack (right now only
    # for sounds and drops) that hits when the target is lured, this is used
    # so the movie can know to do something special for the target, such as
    # not play a sidestep animation for a drop and play a special animation
    # for the target when hit by a sound
    KBBONUS_LURED_FLAG       = 0

    # another flag for the movies that is placed into the KBBONUS_COL for
    # lure attacks to indicate each suit that is successfully lured
    KBBONUS_TGT_LURED        = 1

    notify = DirectNotifyGlobal.directNotify.newCategory('BattleCalculatorAI')

    toonsAlwaysHit = simbase.config.GetBool('toons-always-hit', 0)
    toonsAlwaysMiss = simbase.config.GetBool('toons-always-miss', 0)
    toonsAlways5050 = simbase.config.GetBool('toons-always-5050', 0)    
    suitsAlwaysHit = simbase.config.GetBool('suits-always-hit', 0)
    suitsAlwaysMiss = simbase.config.GetBool('suits-always-miss', 0)
    immortalSuits = simbase.config.GetBool('immortal-suits', 0)

    propAndOrganicBonusStack = simbase.config.GetBool('prop-and-organic-bonus-stack', 0)

    def __init__(self, battle, tutorialFlag=0):
        self.battle = battle

        # a map of maps, containing suit id's and each toon that did
        # damage to that suit and how much damage was done, this is
        # used to let the suit 'intelligently' pick which
        # toon it is going to attack next, generally favoring
        # the toon that did the most damage to it
        self.SuitAttackers = {}

        # list of currently lured suits, used for calculating knockback bonuses
        # and drop hits/misses during a single round (lured suits are no longer
        # lured after the round is over)
        self.currentlyLuredSuits = {}
#        self.suitsUnluredThisRound = []

        # a list created each round and used to keep track of which lure
        # applies to which target when there are multiple lures in a single
        # round
        self.successfulLures = {}

        # list indicating toon attack order
        self.toonAtkOrder = []

        # a list of toon HP adjustments used for sub-round calculations
        # of which suit might actually kill a specific toon, useful for
        # deciding if a toon has just died and cannot perform its chosen
        # attack
        self.toonHPAdjusts = {}

        # a dict of lists of the number of skill points gained in each
        # attack skill for each toon in this battle, at the beginning of
        # a battle these are zeroed, as the battle progresses, each toon
        # will gain skill points, when a toon leaves the battle the skill
        # points will have to be applied and the list in this structure
        # zeroed out
        self.toonSkillPtsGained = {}

        # map of suitId's to trap lvl that is associated with that suit,
        # used to let the battle calculator remember between and during
        # rounds which suits have traps, this list contains the same values
        # as the DistributedSuitAI.battleTrap flag but is independent of it
        # since we cannot rely on that value being set when we expect it to
        self.traps = {}
        self.npcTraps = {}

        self.suitAtkStats = {}

        # list used for calculating toon hpBonuses each round
        self.__clearBonuses(hp=1)
        self.__clearBonuses(hp=0)
        self.delayedUnlures = []

        # This is a factor that's applied to all experience points
        # awarded in this battle.  It's always 1 for a street battle,
        # but a building battle will set this higher based on the
        # current floor number within the building.
        self.__skillCreditMultiplier = 1

        self.tutorialFlag = tutorialFlag

        self.trainTrapTriggered = False

    def setSkillCreditMultiplier(self, mult):
        self.__skillCreditMultiplier = mult

    def getSkillCreditMultiplier(self):
        return self.__skillCreditMultiplier

    def cleanup(self):
        self.battle = None

    def __calcToonAtkHit(self, attackIndex, atkTargets):
        """
        attackIndex, toonAttacks entry indicating the attack
            to use
        Returns:     1 if attack hit, 0 if not, the second number is the
                     resulting accuracy of the attack not taking into
                     account any accuracy bonus

        calculate whether or not a specific toon attack hits
        or misses all of its targets (assumes that either
        all targets are hit or all are missed)
        """
        if len(atkTargets) == 0:
            return 0, 0

        # If this is a tutorial, the toon always hits. I'm returning
        # a 95% accuracy just as a dummy number, because I don't think
        # it gets used. Just in case it does, 95% is a safe value. Greater
        # than that may cause something to crash somewhere.
        if self.tutorialFlag:
            return 1, 95

        if self.toonsAlways5050:
            roll = random.randint(0, 99)
            if roll < 50:
                return 1, 95
            else:
                return 0, 0

        if self.toonsAlwaysHit:
            return 1, 95
        elif self.toonsAlwaysMiss:
            return 0, 0

        debug = self.notify.getDebug()
        attack = self.battle.toonAttacks[attackIndex]

        atkTrack, atkLevel = self.__getActualTrackLevel(attack)

        # According to Justin's comment it might be risky to return 100%
        # accuracy for any attack other than trap
        # If the track comes back as NPCSOS, it's not a normal toon attack,
        # so it really doesn't matter what we return anyway
        if (atkTrack == NPCSOS):
            return (1, 95)
            
        if (atkTrack == FIRE):
            return (1, 95)

        # certain attack tracks (trap) always hit
        if (atkTrack == TRAP):
            if debug:
                self.notify.debug("Attack is a trap, so it hits regardless")
            attack[TOON_ACCBONUS_COL] = 0
            return (1, 100)
        elif (atkTrack == DROP and attack[TOON_TRACK_COL] == NPCSOS):
            # NPC drop can hit multiple targets
            unluredSuits = 0
            for tgt in atkTargets:
                if (not self.__suitIsLured(tgt.getDoId())):
                   unluredSuits = 1
            if (unluredSuits == 0):
                attack[TOON_ACCBONUS_COL] = 1
                return (0, 0)
        elif (atkTrack == DROP):
            # there can be only one target for a drop, and if the target is
            # lured, the drop misses
            # uber drop has multiple targets
            # RAU TODO, make uber drop be able hit only some of the suits and miss lured suits
            allLured = True
            for i in range(len(atkTargets)):
                if (self.__suitIsLured(atkTargets[i].getDoId())):
                    assert(self.notify.debug("Drop on lured suit " +
                                             str(atkTargets[i].getDoId()) + " missed"))
                else:
                    allLured = False
                    
            if allLured:
                attack[TOON_ACCBONUS_COL] = 1
                return (0, 0)
        elif (atkTrack == PETSOS):
            return self.__calculatePetTrickSuccess(attack)

        # in the case of suit targets, go through each target and pick out
        # defense of the highest level suit
        tgtDef = 0
        numLured = 0
        if (atkTrack != HEAL):
            for currTarget in atkTargets:
                thisSuitDef = self.__targetDefense(currTarget, atkTrack)
                if debug:
                    self.notify.debug("Examining suit def for toon attack: " +
                                       str(thisSuitDef))
                tgtDef = min(thisSuitDef, tgtDef)
                if (self.__suitIsLured(currTarget.getDoId())):
                    numLured += 1

        # for combos (multiple toon attacks of the same track with the same
        # target), use the track exp acc bonus of the highest level toon
        # attacking in this combo
        trackExp = self.__toonTrackExp(attack[TOON_ID_COL], atkTrack)
        for currOtherAtk in self.toonAtkOrder:
            if currOtherAtk != attack[TOON_ID_COL]:
                nextAttack = self.battle.toonAttacks[currOtherAtk]
                nextAtkTrack = self.__getActualTrack(nextAttack)
                if atkTrack == nextAtkTrack and \
                   attack[TOON_TGT_COL] == nextAttack[TOON_TGT_COL]:
                    currTrackExp = self.__toonTrackExp(
                        nextAttack[TOON_ID_COL], atkTrack)
                    if debug:
                        self.notify.debug("Examining toon track exp bonus: " +
                                           str(currTrackExp))
                    trackExp = max(currTrackExp, trackExp)

        if debug:
            if atkTrack == HEAL:
                self.notify.debug("Toon attack is a heal, no target def used")
            else:
                self.notify.debug("Suit defense used for toon attack: " +
                                   str(tgtDef))
            self.notify.debug("Toon track exp bonus used for toon attack: " +
                               str(trackExp))

        # now determine the accuracy of the attack the toon is using
        #
        # NPCs always hit
        if (attack[TOON_TRACK_COL] == NPCSOS): 
            randChoice = 0
        else:
            randChoice = random.randint(0, 99)
        propAcc = AvPropAccuracy[atkTrack][atkLevel]

        # use an adjusted LURE  accuracy level if they have a fruiting gag-tree
        if atkTrack == LURE:
            treebonus = self.__toonCheckGagBonus(attack[TOON_ID_COL], atkTrack, atkLevel)
            propBonus = self.__checkPropBonus(atkTrack)
            if self.propAndOrganicBonusStack:
                propAcc = 0
                if treebonus :
                    self.notify.debug( "using organic bonus lure accuracy")
                    propAcc+= AvLureBonusAccuracy[atkLevel]
                if propBonus:
                    self.notify.debug( "using prop bonus lure accuracy")
                    propAcc+= AvLureBonusAccuracy[atkLevel]
            else:
                if treebonus or propBonus:
                    self.notify.debug( "using oragnic OR prop bonus lure accuracy")
                    propAcc = AvLureBonusAccuracy[atkLevel]
            
        attackAcc = propAcc + trackExp + tgtDef

        # see if the previous attack was the same track as the current
        # track, if so the hit or miss status of this attack is the same
        # as the that of the prevous attack
        currAtk = self.toonAtkOrder.index(attackIndex)
        # Heals shouldn't be affected by the previous attack
        if (currAtk > 0 and atkTrack != HEAL):
            prevAtkId = self.toonAtkOrder[currAtk - 1]
            prevAttack = self.battle.toonAttacks[prevAtkId]
            prevAtkTrack = self.__getActualTrack(prevAttack)

            # if the track of this attack is the same as the previous attack
            # and the target(s) of this and the previous attacks are the same
            # and the previous attack was side-stepped, then this attack
            # is also side-stepped since attacks of the same track occurr at
            # once NOTE: the target column for the attack is the id of the
            # target, if the attack is a group attack, this id is 0 since
            # there is no single target, in either case the real id or id of
            # 0 must be the same for this and the previous attack
            # we need to special handle a lure attack, since lures can be
            # either group or single targets and when one hits in a single
            # round all others during that same round also hit
            lure = atkTrack == LURE and \
                 ((not attackAffectsGroup(atkTrack, atkLevel, 
                                          attack[TOON_TRACK_COL]) and \
                   self.successfulLures.has_key(attack[TOON_TGT_COL])) or \
                  attackAffectsGroup(atkTrack, atkLevel, attack[TOON_TRACK_COL]))
            if atkTrack == prevAtkTrack and \
               (attack[TOON_TGT_COL] == prevAttack[TOON_TGT_COL] or \
                lure):

                if prevAttack[TOON_ACCBONUS_COL] == 1:
                    if debug:
                        self.notify.debug("DODGE: Toon attack track dodged")
                elif prevAttack[TOON_ACCBONUS_COL] == 0:
                    if debug:
                        self.notify.debug("HIT: Toon attack track hit")
                else:
                    assert 0, "Unknown value for sidestep flag"
                attack[TOON_ACCBONUS_COL] = prevAttack[TOON_ACCBONUS_COL]
                return (not attack[TOON_ACCBONUS_COL],
#                         (not attack[TOON_ACCBONUS_COL]) * 100)
                         attackAcc)

        atkAccResult = attackAcc
        if debug:
            self.notify.debug("setting atkAccResult to %d" % atkAccResult)
        acc = attackAcc + self.__calcToonAccBonus(attackIndex)

        if (atkTrack != LURE and atkTrack != HEAL):
            # non-lure attacks are affected by how many targets are lured,
            # the more targets that are lured, the better chance the attack
            # has to hit, if all targets are lured, the attack will hit
            if atkTrack != DROP:
                if numLured == len(atkTargets):
                    # all suits are lured so the attack hits regardless
                    if debug:
                        self.notify.debug("all targets are lured, attack hits")
                    attack[TOON_ACCBONUS_COL] = 0
                    return (1, 100)
                else:
                    # at least one target is not lured, but lets reduce the
                    # defense of all the targets based on how many suits are lured
                    luredRatio = float(numLured) / float(len(atkTargets))
                    accAdjust = 100 * luredRatio
                    if accAdjust > 0 and debug:
                        self.notify.debug(str(numLured) + " out of " +
                                       str(len(atkTargets)) +
                                       " targets are lured, so adding " +
                                       str(accAdjust) +
                                       " to attack accuracy")
                    acc += accAdjust
            else:
                #lets reverse the logic if it's a drop
                if numLured == len(atkTargets):
                    # all suits are lured so the attack misses
                    if debug:
                        self.notify.debug("all targets are lured, attack misses")
                    attack[TOON_ACCBONUS_COL] = 0
                    return (0, 0)
                else:
                    #RAU this feels too overpowered
                    pass
                    # at least one target is not lured, but lets reduce the
                    # defense of all the targets based on how many suits are lured
                    #luredRatio = float(numLured) / float(len(atkTargets))
                    #luredRatio = 1.0 - luredRatio
                    #accAdjust = 100 * luredRatio
                    #if accAdjust > 0 and debug:
                    #    self.notify.debug(str(numLured) + " out of " +
                    #                   str(len(atkTargets)) +
                    #                   " targets are lured, so adding " +
                    #                   str(accAdjust) +
                    #                   " to attack accuracy")
                    #acc += accAdjust
                    
                
                


        # NOTE: We are imposing an upper limit on accuracy, so there is
        # always some chance of missing (for toons anyway)
        if acc > MaxToonAcc:
            acc = MaxToonAcc

        if randChoice < acc:
            if debug:
                self.notify.debug("HIT: Toon attack rolled" +
                                   str(randChoice) +
                                   "to hit with an accuracy of" + str(acc))
            attack[TOON_ACCBONUS_COL] = 0
        else:
            if debug:
                self.notify.debug("MISS: Toon attack rolled" +
                                  str(randChoice) +
                                  "to hit with an accuracy of" + str(acc))
            attack[TOON_ACCBONUS_COL] = 1
        return (not attack[TOON_ACCBONUS_COL], atkAccResult)


    def __toonTrackExp(self, toonId, track):
        """
        toonId, toon to get the track exp value for
        
        calculate a track exp value used for the specified
        toon's attack accuracy calculations
        """
        # CCC look at next attacks that are the same track, take the max
        # toon track exp and use that for this attack
        toon = self.battle.getToon(toonId)
        if (toon != None):
            toonExpLvl = toon.experience.getExpLevel(track)
            exp = self.AttackExpPerTrack[toonExpLvl]
            if track == HEAL:
                exp = exp * 0.5
            self.notify.debug("Toon track exp: " + str(toonExpLvl) +
                               " and resulting acc bonus: " + str(exp))
            return exp
        else:
            return 0

    def __toonCheckGagBonus(self, toonId, track, level):
        toon = self.battle.getToon(toonId)
        if (toon != None):
            return toon.checkGagBonus(track, level)
        else:
            return False

    def __checkPropBonus(self, track):
        """Return true if this battle has a prop buffing it."""
        result = False
        if self.battle.getInteractivePropTrackBonus() == track:
            result = True
        return result

    def __targetDefense(self, suit, atkTrack):
        """
        Parameters: suit, the suit to get the defense of
                    atkTrack, attack track type being used on the suit
        
        calculate a suit's defense value given its level
        """
        if atkTrack == HEAL:
            return 0
        suitDef = SuitBattleGlobals.SuitAttributes[suit.dna.name]\
                    ['def'][suit.getLevel()]
        return -suitDef

    def __createToonTargetList(self, attackIndex):
        """
        attackIndex, index into the toonAttacks list which
          indicates which attack we are using
        
        create a list of targets for the specified toon
        attack, the target type of the attack determines
        which participants in the battle are targets
        """

        attack = self.battle.toonAttacks[attackIndex]
        atkTrack, atkLevel = self.__getActualTrackLevel(attack)
        targetList = []
        if (atkTrack == NPCSOS):
            # Must be a non-toon NPC attack of some kind
            return targetList
        if (not attackAffectsGroup(atkTrack, atkLevel, attack[TOON_TRACK_COL])):
            # add only the specified target to the target list
            if (atkTrack == HEAL):
                # If the "attack" is a heal, then the target is a
                # toon, and for toons we only keep track of the doId,
                # so just add that to the target list.
                target = attack[TOON_TGT_COL]
            else:
                # Otherwise, the target must be a suit.
                target = self.battle.findSuit(attack[TOON_TGT_COL])

            if target != None:
                targetList.append(target)
        else:
            # all targets currently in battle
            #
            if (atkTrack == HEAL or atkTrack == PETSOS):
                if (attack[TOON_TRACK_COL] == NPCSOS or atkTrack == PETSOS):
                    targetList = self.battle.activeToons
                else:
                    # copy over the toon ids for all toons except for the
                    # one doing the heal
                    for currToon in self.battle.activeToons:
                        if attack[TOON_ID_COL] != currToon:
                            targetList.append(currToon)
            else:
                targetList = self.battle.activeSuits
        return targetList

    def __prevAtkTrack(self, attackerId, toon=1):
        """
        toon, 1 if the attacker is a toon, 0 otherwise
        
        get the track type of the previous attack, wrt to
        the attackerId given, and in the order that the movie
        will play out the attacks
        """
        if toon:
            prevAtkIdx = self.toonAtkOrder.index(attackerId) - 1
            if prevAtkIdx >= 0:
                prevAttackerId = self.toonAtkOrder[prevAtkIdx]
                attack = self.battle.toonAttacks[prevAttackerId]
                return self.__getActualTrack(attack)
            else:
                return NO_ATTACK
        else:
            assert 0, "__prevAtkTrack: not defined for suits!"

    def getSuitTrapType(self, suitId):
        """
        Parameters: suitId, the suit to get the trap type from
        Returns:    the type of trap currently on the suit, NO_TRAP if
                    no trap exists on this suit
        
        the type of trap the specified suit has on it
        """
        if (self.traps.has_key(suitId)):
            if (self.traps[suitId][0] == self.TRAP_CONFLICT):
                return NO_TRAP
            else:
                return self.traps[suitId][0]
        else:
            return NO_TRAP

    def __suitTrapDamage(self, suitId):
        """
        Returns the damage that will be done to the suit when its trap
        is sprung.
        """
        if (self.traps.has_key(suitId)):
            return self.traps[suitId][2]
        else:
            return 0

    def addTrainTrapForJoiningSuit(self, suitId):
        """
        a joining suit needs to be marked with the train trap
        """
        self.notify.debug('addTrainTrapForJoiningSuit suit=%d self.traps=%s' % (suitId,self.traps))
        trapInfoToUse = None
        for trapInfo in self.traps.values():
            if trapInfo[0] == UBER_GAG_LEVEL_INDEX:
                trapInfoToUse = trapInfo
                break

        if trapInfoToUse:
            self.traps[suitId] = trapInfoToUse
        else:
            self.notify.warning('huh we did not find a train trap?')
                
            

    def __addSuitGroupTrap(self, suitId, trapLvl, attackerId, allSuits, npcDamage = 0):
        """
        suitId, the suit to place the trap on
        trapLvl, the type of trap to place
        
        place a trap in front of a specific suit
        if we're place a group trap, and we detect a conflict, we need to
        mark all the other suits as trap conflicts
        """
        #import pdb; pdb.set_trace()
        if (npcDamage == 0):
            if (self.traps.has_key(suitId)):
                # a trap level of TRAP_CONFLICT indicates that this suit has
                # had more than one trap placed on it this round so any new
                # traps placed on this suit should not stay
                if (self.traps[suitId][0] == self.TRAP_CONFLICT):
                    pass
                else:
                    # this is the second trap placed on this suit this round
                    # so both the previous trap and this trap are gone, indicate
                    # this case by setting trap level to 'TRAP_CONFLICT'
                    self.traps[suitId][0] = self.TRAP_CONFLICT

                #mark all the suits as trap conflict
                for suit in allSuits:
                    id = suit.doId
                    if (self.traps.has_key(id)):
                        self.traps[id][0] = self.TRAP_CONFLICT
                    else:
                        self.traps[id] = [self.TRAP_CONFLICT, 0, 0]
                    
            else:
                toon = self.battle.getToon(attackerId)
                organicBonus = toon.checkGagBonus(TRAP, trapLvl)
                propBonus = self.__checkPropBonus(TRAP)
                damage = getAvPropDamage(TRAP, trapLvl, 
                                        toon.experience.getExp(TRAP), organicBonus,
                                         propBonus, self.propAndOrganicBonusStack)
                if self.itemIsCredit(TRAP, trapLvl):
                    self.traps[suitId] = [trapLvl, attackerId, damage]
                else:
                    # If we don't deserve credit for the high-level trap
                    # attack, don't bother to record the creator.
                    self.traps[suitId] = [trapLvl, 0, damage]

                #what do we do in a multi suit battle, if we lure
                #one suit the do the train trap? Currently we just unlure
                self.notify.debug('calling __addLuredSuitsDelayed')
                self.__addLuredSuitsDelayed(attackerId, targetId=-1, ignoreDamageCheck = True)
        else:
            # NPC traps defer to any pre-set traps, but they can take
            # the spot of two traps that collided
            if (self.traps.has_key(suitId)): 
                if (self.traps[suitId][0] == self.TRAP_CONFLICT):
                    self.traps[suitId] = [trapLvl, 0, npcDamage]
            elif (not self.__suitIsLured(suitId)):
                self.traps[suitId] = [trapLvl, 0, npcDamage]


    def __addSuitTrap(self, suitId, trapLvl, attackerId, npcDamage = 0):
        """
        suitId, the suit to place the trap on
        trapLvl, the type of trap to place
        
        place a trap in front of a specific suit
        """
        if (npcDamage == 0):
            if (self.traps.has_key(suitId)):
                # a trap level of TRAP_CONFLICT indicates that this suit has
                # had more than one trap placed on it this round so any new
                # traps placed on this suit should not stay
                if (self.traps[suitId][0] == self.TRAP_CONFLICT):
                    pass
                else:
                    # this is the second trap placed on this suit this round
                    # so both the previous trap and this trap are gone, indicate
                    # this case by setting trap level to 'TRAP_CONFLICT'
                    self.traps[suitId][0] = self.TRAP_CONFLICT
            else:
                toon = self.battle.getToon(attackerId)
                organicBonus = toon.checkGagBonus(TRAP, trapLvl)
                propBonus = self.__checkPropBonus(TRAP)
                damage = getAvPropDamage(TRAP, trapLvl, 
                                        toon.experience.getExp(TRAP), organicBonus,
                                         propBonus, self.propAndOrganicBonusStack)
                if self.itemIsCredit(TRAP, trapLvl):
                    self.traps[suitId] = [trapLvl, attackerId, damage]
                else:
                    # If we don't deserve credit for the high-level trap
                    # attack, don't bother to record the creator.
                    self.traps[suitId] = [trapLvl, 0, damage]
        else:
            # NPC traps defer to any pre-set traps, but they can take
            # the spot of two traps that collided
            if (self.traps.has_key(suitId)): 
                if (self.traps[suitId][0] == self.TRAP_CONFLICT):
                    self.traps[suitId] = [trapLvl, 0, npcDamage]
            elif (not self.__suitIsLured(suitId)):
                self.traps[suitId] = [trapLvl, 0, npcDamage]

    def __removeSuitTrap(self, suitId):
        """
        suitId, the doId of the suit to remove the trap from
        
        remove any trap from the specified suit
        """
        if self.traps.has_key(suitId):
            del self.traps[suitId]

    def __clearTrapCreator(self, creatorId, suitId = None):
        """
        creatorId, the doId of the toon who placed the trap
        suitId, the particular suit's trap to remove (or None)
        
        remove the specified creator id from any trap on
        the specified target (or any target if suitId is
        None). this should be done when the creator should
        no longer get exp credit for the trap
        """
        if suitId == None:
            for currTrap in self.traps.keys():
                if creatorId == self.traps[currTrap][1]:
                    self.traps[currTrap][1] = 0
        else:
            if self.traps.has_key(suitId):
                assert(self.traps[suitId][1] == 0 or self.traps[suitId][1] == creatorId)
                self.traps[suitId][1] = 0

    def __trapCreator(self, suitId):
        """
        suitId, the doId of the suit to remove the trap from
        
        If a suit has a trap associated with it, get the
        id of who created the trap, for the purposes of
        awarding experience points after the trap is
        sprung.  If the creator is no longer in the
        battle, or if the creator is still in the
        battle but used an overly-powerful trap item, 0
        is returned.
        """
        if self.traps.has_key(suitId):
            return self.traps[suitId][1]
        else:
            return 0

    def __initTraps(self):
        """
        Make sure every round to go through the traps list
        and any that exist and have values of 'TRAP_CONFLICT'
        should be deleted since this is a new round and
        'trap conflicts' dont persist between rounds
        """
        self.trainTrapTriggered = False
        keysList = self.traps.keys()
        for currTrap in keysList:
            if (self.traps[currTrap][0] == self.TRAP_CONFLICT):
                del self.traps[currTrap]

    def __calcToonAtkHp(self, toonId):
        """
        attackIndex, index into the list of toonAttacks
            that indicates which attack we are to be calculating
            the damage for
        
        Calculate the amount of damage the specified attack
        will do
        """
        # generate a list of possible targets based on the attack and
        # determine the damage done to each
        assert(self.battle.toonAttacks.has_key(toonId))
        attack = self.battle.toonAttacks[toonId]
        targetList = self.__createToonTargetList(toonId)

        #import pdb; pdb.set_trace()

        # make sure the attack has hit all targets before even
        # trying to continue
        atkHit, atkAcc = self.__calcToonAtkHit(toonId, targetList)

        atkTrack, atkLevel, atkHp = self.__getActualTrackLevelHp(attack)

        if (not atkHit and atkTrack != HEAL):
            return

        # for each target calculate the damage done, it is possible
        # to be different amounts for the different targets
        # validTargetAvail tabulates if there is at least one valid
        # target for this attack (valid depends on the attack, but it
        # involves the target's lure status as well as if the target
        # is dead or not)
        validTargetAvail = 0
        lureDidDamage = 0
        currLureId = -1
        for currTarget in range(len(targetList)):
            # first get the attack's base damage
            # check to see if this is a 'lure' attack, if it is, the
            # lure itself doesn't damage the target, but rather any
            # trap that might exist in front of the target
            attackLevel = -1
            attackTrack = None
            attackDamage = 0
            toonTarget = 0
            targetLured = 0
            if (atkTrack == HEAL or atkTrack == PETSOS):
                # the targets are toons, so we need to handle getting info
                # about the target differently than we do a suit
                targetId = targetList[currTarget]
                toonTarget = 1
            else:
                targetId = targetList[currTarget].getDoId()
            if (atkTrack == LURE):
                # check to see if the target of this lure has a trap set
                # on him/her, if no then go ahead and lure the suit normally,
                # if yes, then the trap will damage the target and the target
                # will effectively not end up lured (because the trap itself
                # unlures the target)
                if (self.getSuitTrapType(targetId) == NO_TRAP):
                    if self.notify.getDebug():
                        self.notify.debug("Suit lured, but no trap exists")

                    if self.SUITS_UNLURED_IMMEDIATELY:
                        # make sure to add the suit to the lured list,
                        # if suits are unlured immediately then we only need
                        # to add suits which are not lured onto a trap to
                        # the currently lured list (if the suit was lured this
                        # round by some other attack, then still add the suit
                        # to the lured list because we want to update the lured
                        # suit info with this new lure, but if the suit was
                        # lured on a previous round and is still lured, then
                        # this lure does not affect the suit)
                        if not self.__suitIsLured(targetId, prevRound=1):
                            if not self.__combatantDead(targetId,
                                                         toon=toonTarget):
                                validTargetAvail = 1
                            rounds = self.NumRoundsLured[atkLevel]
                            wakeupChance = 100 - (atkAcc * 2)
                            npcLurer = (attack[TOON_TRACK_COL] == NPCSOS)
                            currLureId = self.__addLuredSuitInfo(
                                targetId, -1, rounds, wakeupChance, toonId,
                                atkLevel, lureId=currLureId, npc = npcLurer)
                            if self.notify.getDebug():
                                self.notify.debug(
                                    "Suit lured for " +
                                    str(rounds)+
                                    " rounds max with " +
                                    str(wakeupChance)+
                                    "% chance to wake up each round")
                            targetLured = 1
                else:
                    # get the damage for the trap that was triggered
                    # which is obtained from asking the target itself
                    # since we only get here if there is a trap in front
                    # of the target, we know that the target is not lured
                    attackTrack = TRAP
                    #attackLevel = targetList[currTarget].battleTrap
                    if (self.traps.has_key(targetId)):
                        trapInfo = self.traps[targetId]
                        attackLevel = trapInfo[0]
                    else:
                        attackLevel = NO_TRAP
                    attackDamage = self.__suitTrapDamage(targetId)

                    # determine who placed the trap and give them exp
                    trapCreatorId = self.__trapCreator(targetId)
                    if trapCreatorId > 0:
                        self.notify.debug("Giving trap EXP to toon " +
                                           str(trapCreatorId))
                        self.__addAttackExp(attack, track=TRAP,
                                             level=attackLevel,
                                             attackerId=trapCreatorId)

                    # Remove the owner record now, so we don't
                    # accidentally give the trap placer multiple
                    # experience points if multiple players sprung the
                    # trap.
                    self.__clearTrapCreator(trapCreatorId, targetId)

                    lureDidDamage = 1
                    if self.notify.getDebug():
                        self.notify.debug(
                            "Suit lured right onto a trap! (" +
                            str(AvProps[attackTrack][attackLevel]) +
                            "," + str(attackLevel) + ")")
                    if not self.__combatantDead(targetId, toon=toonTarget):
                        validTargetAvail = 1
                    targetLured = 1
                if not self.SUITS_UNLURED_IMMEDIATELY:
                    # make sure to add the suit to the lured list,
                    # if suits are not unlured immediately, then even a suit
                    # which is lured onto a trap will still be lured until
                    # all toon attacks are finished
                    if not self.__suitIsLured(targetId, prevRound=1):
                        if not self.__combatantDead(targetId,
                                                     toon=toonTarget):
                            validTargetAvail = 1
                        rounds = self.NumRoundsLured[atkLevel]
                        wakeupChance = 100 - (atkAcc * 2)
                        npcLurer = (attack[TOON_TRACK_COL] == NPCSOS)
                        currLureId = self.__addLuredSuitInfo(
                            targetId, -1, rounds, wakeupChance, toonId,
                            atkLevel, lureId=currLureId, npc = npcLurer)
                        if self.notify.getDebug():
                            self.notify.debug(
                                "Suit lured for " +
                                str(rounds)+
                                " rounds max with " +
                                str(wakeupChance)+
                                "% chance to wake up each round")
                        targetLured = 1

                    # be sure to unlure this guy after calculating toon attacks
                    # if he/she was lured onto a trap, attackLevel should be
                    # the level of the trap that the suit was lured onto
                    if attackLevel != -1:
                        self.__addLuredSuitsDelayed(toonId, targetId)

                # now check to see if this target is lured by this lure
                # based on any previous lures that happened this round,
                # higher level lures over-ride lower level ones because
                # they cause the suit to be lured for a longer period of
                # time
                if targetLured and \
                   (not self.successfulLures.has_key(targetId) or \
                     (self.successfulLures.has_key(targetId) and \
                       self.successfulLures[targetId][1] < \
                       atkLevel)):
                    self.notify.debug("Adding target " + str(targetId) +
                                       " to successfulLures list")
                    self.successfulLures[targetId] = [
                        toonId,
                        atkLevel,
                        atkAcc,
                        -1]
            else:
                if (atkTrack == TRAP):
                    #import pdb; pdb.set_trace()
                    npcDamage = 0
                    if (attack[TOON_TRACK_COL] == NPCSOS):
                        npcDamage = atkHp
                    if self.CLEAR_MULTIPLE_TRAPS:
                        # if this attack is a trap and the target already has
                        # a trap on it, clear the attack and move to the next
                        # attack.  NOTE: this assumes that a trap will only
                        # affect a single target
                        if self.getSuitTrapType(targetId) != NO_TRAP:
                            self.__clearAttack(toonId)
                            return

                    # be sure to set our own internal trap indicator for
                    # this suit so no more traps can be placed on this target
                    if atkLevel == UBER_GAG_LEVEL_INDEX:
                        #the SOS trap will also affect a group, but we want the train trap to behave differently
                        self.__addSuitGroupTrap(targetId, atkLevel, toonId, targetList, npcDamage)

                        if self.__suitIsLured(targetId):
                            # if this is a train trap  on a lured suit,
                            # be sure to place a indicator in the
                            # KBBONUS_COL so the battle movie knows
                            # that this is a train trap on a lured suit
                            # and it should do something different than other
                            # attack types on lured suits
                            self.notify.debug("Train Trap on lured suit %d, \n indicating with KBBONUS_COL flag" % targetId)
                            tgtPos = self.battle.activeSuits.index(
                                targetList[currTarget])
                            attack[TOON_KBBONUS_COL][tgtPos] = \
                                                             self.KBBONUS_LURED_FLAG                        
                    else:
                        self.__addSuitTrap(targetId, atkLevel, toonId, npcDamage)
                elif self.__suitIsLured(targetId) and \
                     atkTrack == SOUND:
                    # if this is a sound on a lured suit,
                    # be sure to place a indicator in the
                    # KBBONUS_COL so the battle movie knows
                    # that this is a drop or sound on a lured suit
                    # and it should do something different than other
                    # attack types on lured suits
                    self.notify.debug("Sound on lured suit, " +
                                       "indicating with KBBONUS_COL flag")
                    tgtPos = self.battle.activeSuits.index(
                        targetList[currTarget])
                    attack[TOON_KBBONUS_COL][tgtPos] = \
                            self.KBBONUS_LURED_FLAG

                attackLevel = atkLevel 
                attackTrack = atkTrack 
                toon = self.battle.getToon(toonId)
                assert toon
                if ((attack[TOON_TRACK_COL] == NPCSOS and lureDidDamage != 1) or
                    attack[TOON_TRACK_COL] == PETSOS):
                    # If lureDidDamage == 1, attackDamage has already been
                    # filled in
                    attackDamage = atkHp
                else:
                    if (atkTrack == FIRE):
                        suit = self.battle.findSuit(targetId)
                        if suit:
                            costToFire = 1#suit.getActualLevel()
                            abilityToFire = toon.getPinkSlips()
                            numLeft = abilityToFire - costToFire
                            if numLeft < 0:
                                numLeft = 0
                            toon.b_setPinkSlips(numLeft)
                            if costToFire > abilityToFire:
                                commentStr = "Toon attempting to fire a %s cost cog with %s pinkslips" % (costToFire, abilityToFire)
                                simbase.air.writeServerEvent('suspicious', toonId, commentStr)
                                dislId = toon.DISLid
                                simbase.air.banManager.ban(toonId, dislId, commentStr)
                                print("Not enough PinkSlips to fire cog - print a warning here")
                            else:
                                suit.skeleRevives = 0
                                attackDamage = suit.getHP()

                        else:
                            attackDamage = 0
                        bonus = 0
                    else:
                        organicBonus = toon.checkGagBonus(attackTrack, attackLevel)
                        propBonus = self.__checkPropBonus(attackTrack)
                        attackDamage = getAvPropDamage(attackTrack, attackLevel,
                                       toon.experience.getExp(attackTrack), organicBonus,
                                                       propBonus, self.propAndOrganicBonusStack)
                                       

                if not self.__combatantDead(targetId, toon=toonTarget):
                    #RAU a drop on a lured suit is not a valid target
                    if self.__suitIsLured(targetId) and \
                     atkTrack == DROP:
                        self.notify.debug('not setting validTargetAvail, since drop on a lured suit')
                    else:
                        validTargetAvail = 1

            # check to see if any damage is done at all by this attack,
            # just because it hit does not mean it necessarily did damage
            if (attackLevel == -1) and not (atkTrack == FIRE):
                # if suit is lured, and no trap exists, no damage
                # is taken but the lure works, so set damage to -1
                # to indicate the that the lure was successful and
                # we get proper visual indication
                result = LURE_SUCCEEDED
            else:
                # only specify a damage for a non-trap attack, the
                # damage field for traps is used elsewhere and we should
                # not change it
                if (atkTrack != TRAP):
                    result = attackDamage
                    if (atkTrack == HEAL):
                        if not self.__attackHasHit(attack, suit=0):
                            # heals that indicate a 'miss' only do 1/5 the
                            # normal heal amount
                            result = result * 0.2
                        if self.notify.getDebug():
                            self.notify.debug("toon does " +
                                               str(result) +
                                               " healing to toon(s)")
                    else:
                        if self.__suitIsLured(targetId) and \
                           atkTrack == DROP:
                            result = 0
                            self.notify.debug('setting damage to 0, since drop on a lured suit')
                            
                        if self.notify.getDebug():
                            self.notify.debug("toon does " +
                                               str(result) +
                                               " damage to suit")
                else:
                    result = 0

            #if (self.dbg_ToonSuperDamage):
            #    result = 200

            if (result != 0 or atkTrack == PETSOS):
                # be sure to set the amount of damage done by this attack
                # in the appropriate slot in the toonAttacks list
                # corresponding to this target
                targets = self.__getToonTargets(attack)
                if not targetList[currTarget] in targets:
                    if self.notify.getDebug():
                        self.notify.debug("Target of toon is not accessible!")
                    continue
                targetIndex = targets.index(targetList[currTarget])
                if (atkTrack == HEAL):
                    # we need to divide up the heal amounts among all
                    # targets, and heals alway hit the target
                    result = result / len(targetList)
                    if self.notify.getDebug():
                        self.notify.debug("Splitting heal among " +
                                           str(len(targetList)) +
                                           " targets")
                assert(targetIndex < len(attack[TOON_HP_COL]))

                # if this target is already in the successfulLures list,
                # then be sure to put in the damage done to this target
                # by this lure since this might not be the actual lure
                # that ends up causing damage to the suit
                if (self.successfulLures.has_key(targetId) and
                    atkTrack == LURE):
                    self.notify.debug("Updating lure damage to " +
                                       str(result))
                    self.successfulLures[targetId][3] = result
                else:
                    attack[TOON_HP_COL][targetIndex] = result

                # make sure to give exp for any lures associated with
                # this target if it was lured when it took damage
                if (result > 0 and atkTrack != HEAL and atkTrack != DROP
                               and atkTrack != PETSOS):
                    attackTrack = LURE
                    lureInfos = self.__getLuredExpInfo(targetId)

                    # determine who lured the target and give them exp
                    # then make sure to remove the lured info for this
                    # target
                    for currInfo in lureInfos:
                        if currInfo[3]:
                            self.notify.debug("Giving lure EXP to toon " +
                                               str(currInfo[0]))
                            self.__addAttackExp(attack, track=attackTrack,
                                                 level=currInfo[1],
                                                 attackerId=currInfo[0])

                        # now that this lurer has gotten exp for luring this
                        # target that took damage while lured, remove any
                        # references that this target might have to this
                        # lurer to make sure the lurer only gets exp once per
                        # lure, comprende?
                        self.__clearLurer(currInfo[0],
                                           lureId=currInfo[2])

        if lureDidDamage:
            # since the lure resulted in damage, give exp to the toon
            if self.itemIsCredit(atkTrack, atkLevel):
                self.notify.debug("Giving lure EXP to toon " + str(toonId))
                self.__addAttackExp(attack)

               

        # if it has been discovered that all targets are dead or lured and
        # this is a lure attack or this attack track is different from the
        # previous attack and all targets are dead, then we want to clear
        # out this attack
        if (not validTargetAvail and
            self.__prevAtkTrack(toonId) != atkTrack):
            self.__clearAttack(toonId)

    def __getToonTargets(self, attack):
        """
        attack, the attack to get the targets for
        
        Get a list of available targets for a specific
        attack
        """
        track = self.__getActualTrack(attack)
        if (track == HEAL or track == PETSOS):
            # heals from a toon only apply to other toons
            return self.battle.activeToons
        else:
            # all other attack types apply to suits
            return self.battle.activeSuits

    def __attackHasHit(self, attack, suit=0):
        """
        attack, the attack to check
        Returns:     1 if the attack successfully hit
                     0 if the attack has not hit anything
        
        Check the given attack to see if it has hit anything
        """
        # return whether or not the target(s) dodged the attack
        if (suit == 1):
            for dmg in attack[SUIT_HP_COL]:
                if (dmg > 0):
                    return 1
            return 0
        else:
            track = self.__getActualTrack(attack)
            return not attack[TOON_ACCBONUS_COL] and \
                       track != NO_ATTACK

    def __attackDamage(self, attack, suit=0):
        """
        attack, the attack to find the damage for
        suit, 1 if the attack is a suit attack, 0 otherwise
        Returns:    damage done to one of the targets, 0 if no damage
                    was done
        
        Ask how much damage an attack did to any given target
        """
        if suit:
            for dmg in attack[SUIT_HP_COL]:
                if (dmg > 0):
                    return dmg
            return 0
        else:
            for dmg in attack[TOON_HP_COL]:
                if (dmg > 0):
                    return dmg
            return 0

    def __attackDamageForTgt(self, attack, tgtPos, suit=0):
        """
        attack, the attack to find the damage for
        suit, 1 if the attack is a suit attack, 0 otherwise
        Returns:    damage done to one of the targets, 0 if no damage
                    was done
        
        Ask how much damage an attack did to a specific
        target
        """
        if suit:
            return attack[SUIT_HP_COL][tgtPos]
        else:
            return attack[TOON_HP_COL][tgtPos]

    def __calcToonAccBonus(self, attackKey):
        """
        attackIndex, the attack to calculate the accuracy
            bonus for
        
        Calculate the accuracy bonus for a specific attack
        """
        # look at previous attacks performed this round to determine
        # accuracy bonus
        numPrevHits = 0
        attackIdx = self.toonAtkOrder.index(attackKey)
        for currPrevAtk in range(attackIdx - 1, -1, -1):
            attack = self.battle.toonAttacks[attackKey]
            atkTrack, atkLevel = self.__getActualTrackLevel(attack)
            prevAttackKey = self.toonAtkOrder[currPrevAtk]
            prevAttack = self.battle.toonAttacks[prevAttackKey]
            prvAtkTrack, prvAtkLevel = self.__getActualTrackLevel(prevAttack)

            # only if the previous attack hit, the current
            # attack is not the same track as the prevous attack, and
            # the target of the attacks are the same (or the previous
            # or current attack are a group attack), then there is a
            # possibility of getting an accuracy bonus for this attack
            if self.__attackHasHit(prevAttack) and \
               (attackAffectsGroup(prvAtkTrack, prvAtkLevel, prevAttack[TOON_TRACK_COL]) or \
                 attackAffectsGroup(atkTrack, atkLevel, attack[TOON_TRACK_COL]) or \
                 attack[TOON_TGT_COL] == prevAttack[TOON_TGT_COL]) and \
               atkTrack != prvAtkTrack:
                numPrevHits += 1

        if numPrevHits > 0 and self.notify.getDebug():
            self.notify.debug("ACC BONUS: toon attack received accuracy " +
                               "bonus of " +
                               str(self.AccuracyBonuses[numPrevHits]) +
                               " from previous attack by (" +
                               str(attack[TOON_ID_COL]) +
                               ") which hit")
        return self.AccuracyBonuses[numPrevHits]


    def __applyToonAttackDamages(self, toonId, hpbonus=0, kbbonus=0):
        """
        attackIndex, the attack to apply damages from
        Returns:     total damage done to everything
        
        Apply any damages for the specified toon attack by
        modifying any suit hit-points, also be sure to flag
        if any suit died as a result of this damage
        """
        # now be sure to adjust the damage to the suit, but only
        # if the track of the attack is not 0, meaning it is not
        # a heal, if it's a heal, then the damage is applied as
        # a plus to the target's health and we don't handle adjusting
        # toon health here (additionally attack 1 is a trap attacks,
        # doesn't cause damage directly but only in conjunction with a
        # lure attack)
        totalDamages = 0
        if not self.APPLY_HEALTH_ADJUSTMENTS:
            return totalDamages
        assert(self.battle.toonAttacks.has_key(toonId))
        attack = self.battle.toonAttacks[toonId]
        track = self.__getActualTrack(attack)
        if (track != NO_ATTACK and track != SOS and
            track != TRAP and track != NPCSOS):
            # first create a list of targets based on group or
            # single target designation for this particular attack
            targets = self.__getToonTargets(attack)
            for position in range(len(targets)):
                if hpbonus:
                    # handle applying the hp-bonus if this target
                    # was actually hit by this attack
                    if targets[position] in \
                       self.__createToonTargetList(toonId):
                        damageDone = attack[TOON_HPBONUS_COL]
                    else:
                        damageDone = 0
                elif kbbonus:
                    # handle applying the hp-bonus if this target
                    # was actually hit by this attack
                    if targets[position] in \
                       self.__createToonTargetList(toonId):
                        damageDone = attack[TOON_KBBONUS_COL][position]
                    else:
                        damageDone = 0
                else:
                    assert(position < len(attack[TOON_HP_COL]))
                    damageDone = attack[TOON_HP_COL][position]
                if damageDone <= 0 or self.immortalSuits:
                    # suit at this position was not hit
                    continue
                if (track == HEAL or track == PETSOS):
                    # target of toon attack was another toon, we
                    # don't want to apply any damage yet
                    currTarget = targets[position]
                    assert(self.toonHPAdjusts.has_key(currTarget))
                    if self.CAP_HEALS:
                        # make sure to bound the toon's health to its
                        # max health
                        toonHp = self.__getToonHp(currTarget)
                        toonMaxHp = self.__getToonMaxHp(currTarget)
                        if toonHp + damageDone > toonMaxHp:
                            damageDone = toonMaxHp - toonHp
                            attack[TOON_HP_COL][position] = damageDone
                    self.toonHPAdjusts[currTarget] += damageDone
                    totalDamages = totalDamages + damageDone
                    continue

                # we should only get here if the target is a suit and
                # at least 1hp of damage was done
                currTarget = targets[position]
                assert isinstance(currTarget,
                                   DistributedSuitBaseAI.DistributedSuitBaseAI), \
                                   targets
                currTarget.setHP(currTarget.getHP() - damageDone)
                targetId = currTarget.getDoId()
                if self.notify.getDebug():
                    if hpbonus:
                        self.notify.debug(str(targetId) +
                                           ": suit takes " +
                                           str(damageDone) +
                                           " damage from HP-Bonus")
                    elif kbbonus:
                        self.notify.debug(str(targetId) +
                                           ": suit takes " +
                                           str(damageDone) +
                                           " damage from KB-Bonus")
                    else:
                        self.notify.debug(str(targetId) + ": suit takes " +
                                           str(damageDone) + " damage")
                totalDamages = totalDamages + damageDone

                # if the suit died from this or a previous
                # attack, make sure to set the 'died' field for
                # the target to 1, indicating to the higher-ups
                # that this suit has died
                if currTarget.getHP() <= 0:
                    if currTarget.getSkeleRevives() >= 1:
                       currTarget.useSkeleRevive()
                       attack[SUIT_REVIVE_COL] = \
                                attack[SUIT_REVIVE_COL] | (1 << position)
                    else:
                        self.suitLeftBattle(targetId)
                        attack[SUIT_DIED_COL] = \
                                attack[SUIT_DIED_COL] | (1 << position)
                        if self.notify.getDebug():
                            self.notify.debug("Suit" + str(targetId) +
                                               "bravely expired in combat")

        return totalDamages

    def __combatantDead(self, avId, toon):
        """
        attackIdx, index into the appropriate attacks list
            indicating which attack we are examining
        toon, whether this attacker is a toon or a suit
        Returns:     1 if the attacker is dead, 0 otherwise
        
        Check to see if the attacker for the specified
        attack is still alive, useful to check to see if
        the attack should be calculated
        """
        if toon:
            if self.__getToonHp(avId) <= 0:
                return 1
        else:
            # the suit's hp is adjusted after each attack, so the current
            # value should be correctly adjusted for attack ordering
            suit = self.battle.findSuit(avId)
            assert(suit != None)
            if (suit.getHP() <= 0):
                return 1
        return 0
        
    def __combatantJustRevived(self, avId):
        suit = self.battle.findSuit(avId)
        assert(suit != None)
        if suit.reviveCheckAndClear():
            return 1
        else:
            return 0

    def __addAttackExp(self, attack, track=-1, level=-1, attackerId=-1):
        """
        attack, the toon attack to record exp for
        track, optional track to add exp to
        lvl, optional lvl to add exp to
        toonId, optional toon to add exp to
        
        Record any exp gained for a toon for the specified
        attack, the optional parameters, if all are provided
        will override the attack parameter and add exp to
        the specified toon for the specified attack track
        and level
        """
        trk = -1
        lvl = -1
        id = -1
        if track != -1 and level != -1 and attackerId != -1:
            trk = track
            lvl = level
            id = attackerId
        elif self.__attackHasHit(attack):
            if self.notify.getDebug():
                self.notify.debug("Attack " + repr(attack) + " has hit")
            # now be sure to update the skill points gained for the
            # attacking toon, but only if the attack actually 'hit'
            # something, meaning it was a 'successful' attack
            trk = attack[TOON_TRACK_COL]
            lvl = attack[TOON_LVL_COL]
            id = attack[TOON_ID_COL]

        if trk != -1 and trk != NPCSOS and trk != PETSOS and \
           lvl != -1 and id != -1:
            expList = self.toonSkillPtsGained.get(id, None)
            if expList == None:
                expList = [0, 0, 0, 0, 0, 0, 0]
                self.toonSkillPtsGained[id] = expList
                
            expList[trk] = min(ExperienceCap,
                               expList[trk] + (lvl + 1) * self.__skillCreditMultiplier)

    def __clearTgtDied(self, tgt, lastAtk, currAtk):
        """
        tgt, the target (in this case a suit)
        lastAtk, an attack that might have killed the 'tgt'
        currAtk, an attack that should flag 'tgt' killed if
            necessary
        
        Check to see if the suit died flag for 'lastAtk'
        should be cleared.  This can happen if 'lastAtk'
        killed the suit, but 'currAtk', which happened right
        after 'lastAtk', is of the same track and thus we
        want to play both 'lastAtk' and 'currAtk' for visual
        and gameplay appeal, even though 'currAtk' is not
        actually necessary to kill the suit.  In this case
        we only want to flag that the suit died on 'currAtk'
        so the movie can play the attack sequence properly.
        """
        position = self.battle.activeSuits.index(tgt)
        currAtkTrack = self.__getActualTrack(currAtk)
        lastAtkTrack = self.__getActualTrack(lastAtk)
        if currAtkTrack == lastAtkTrack and \
           lastAtk[SUIT_DIED_COL] & (1 << position) and \
           self.__attackHasHit(currAtk, suit=0):
            if self.notify.getDebug():
                self.notify.debug("Clearing suit died for " +
                                   str(tgt.getDoId()) +
                                   " at position " + str(position) +
                                   " from toon attack " +
                                   str(lastAtk[TOON_ID_COL]) +
                                   " and setting it for " +
                                   str(currAtk[TOON_ID_COL]))

            # clear the flag from the previous attack
            lastAtk[SUIT_DIED_COL] = \
                         lastAtk[SUIT_DIED_COL] ^ (1 << position)

            # make sure since the last attack
            # indicated that it killed the
            # suit and we are now clearing out
            # that indication, that this
            # attack, which is of the same
            # track, does flag the suit as
            # dead
            assert tgt.getHP() <= 0
            self.suitLeftBattle(tgt.getDoId())
            currAtk[SUIT_DIED_COL] = \
                    currAtk[SUIT_DIED_COL] | (1 << position)

    def __addDmgToBonuses(self, dmg, attackIndex, hp=1):
        """
        dmg, how much damage to add to the bonuses list
        attackIndex, the attack that did specified damage
        hp, 1 if this is for the hpBonuses list, 0 for the
            kbBonuses list
        
        Add a given damage value done by a specified attack
        to a specified bonus list, this should be called
        as soon as a suit is damaged by any attack
        """
        toonId = self.toonAtkOrder[attackIndex]
        attack = self.battle.toonAttacks[toonId]
        atkTrack = self.__getActualTrack(attack)
        if (atkTrack == HEAL or atkTrack == PETSOS):
            return

        # for each target of this attack, keep track of any bonus from this
        # attack
        tgts = self.__createToonTargetList(toonId)
        for currTgt in tgts:
            tgtPos = self.battle.suits.index(currTgt)
            attackerId = self.toonAtkOrder[attackIndex]
            attack = self.battle.toonAttacks[attackerId]
            track = self.__getActualTrack(attack)
            if hp:
                if self.hpBonuses[tgtPos].has_key(track):
                    self.hpBonuses[tgtPos][track].append([attackIndex, dmg])
                else:
                    self.hpBonuses[tgtPos][track] = [[attackIndex, dmg]]
            else:
                # only add a kbBonus value if the suit is currently lured
                if self.__suitIsLured(currTgt.getDoId()):
                    if self.kbBonuses[tgtPos].has_key(track):
                        self.kbBonuses[tgtPos][track].append([attackIndex, dmg])
                    else:
                        self.kbBonuses[tgtPos][track] = [[attackIndex, dmg]]

    def __clearBonuses(self, hp=1):
        """
        hp, 1 if the hpBonuses list should be cleared, 0 if
            the kbBonuses list should be cleared
        
        Clear a specific bonuses list, usually done before
        calculating a new round
        """
        if hp:
            self.hpBonuses = [{}, {}, {}, {}]
        else:
            self.kbBonuses = [{}, {}, {}, {}]

    def __bonusExists(self, tgtSuit, hp=1):
        """
        tgtSuit, the suit to check to see if some sort of
            damage bonus will be applied to him/her
        hp, 1 to check for a hp-bonus, 0 to check for a
            knock-back bonus
        Returns:    1 if a bonus does exist, 0 otherwise
        
        Check to see if a certain bonus type exists for a
        given target suit
        """
        tgtPos = self.activeSuits.index(tgtSuit)
        if hp:
            bonusLen = len(self.hpBonuses[tgtPos])
        else:
            bonusLen = len(self.kbBonuses[tgtPos])
        if bonusLen > 0:
            return 1
        return 0

    def __processBonuses(self, hp=1):
        """
        Process all current hpBonus information, also
        clearing out the hpBonus information so a new track
        can be processed
        """
        # Process all hpBonus information, making sure to update the
        # appropriate attacks with the calculated hpBonus for grouped
        # attacks of the same track that did damage.  NOTE:  this code
        # is fairly basic because it assumes that all attacks in a single
        # track type of attacks are either group or single targets.  If in
        # the future attacks in a track that does damage (not including the
        # heal track) varies in group or single targets, this function will
        # not work the way it should.  This is because the hpBonuses list is
        # ordered by target and so an attack that receives an hp-bonus on
        # say the first target will apply that hp-bonus to all of its
        # targets depending on if it is a group or single type attack.  And
        # since any other attack that might also receive an hp-bonus in
        # combination with this attack must be the same track, it must
        # therefore also be of the same target type.  This prevents say
        # target 1 from receiving a damage bonus of 10 from attack 1 and
        # target 2 from receiving a damage bonus of 5 from attack 1 (all
        # targets receiving a damage bonus from attack 1 would all be 10)
        # Additionally there is only one spot for a hp-bonus for each toon
        # attack (so if in the future group/single target attacks are mixed
        # within a single track that does damage then this code will have to
        # be improved to handle this case and the self.battle.toonAttacks
        # list will have to have 4 entries for hp-bonuses for each toon
        # attack)
        if hp:
            bonusList = self.hpBonuses
            self.notify.debug("Processing hpBonuses: " +
                               repr(self.hpBonuses))
        else:
            bonusList = self.kbBonuses
            self.notify.debug("Processing kbBonuses: " +
                               repr(self.kbBonuses))
        tgtPos = 0
        for currTgt in bonusList:
            for currAtkType in currTgt.keys():
                # for an hpBonus we need at least 2 damages from a single
                # attack type, for kbBonuses we only need at least 1 damage
                # value
                if len(currTgt[currAtkType]) > 1 or \
                   ((not hp) and len(currTgt[currAtkType]) > 0):
                    totalDmgs = 0
                    for currDmg in currTgt[currAtkType]:
                        totalDmgs += currDmg[1]
                    numDmgs = len(currTgt[currAtkType])
                    attackIdx = currTgt[currAtkType][numDmgs-1][0]
                    attackerId = self.toonAtkOrder[attackIdx]
                    attack = self.battle.toonAttacks[attackerId]
                    if hp:
                        attack[TOON_HPBONUS_COL] = math.ceil(
                            totalDmgs * \
                            (self.DamageBonuses[numDmgs - 1] * 0.01))
                        if self.notify.getDebug():
                            self.notify.debug(
                                "Applying hp bonus to track " +
                                str(attack[TOON_TRACK_COL]) +
                                " of " +
                                str(attack[TOON_HPBONUS_COL]))
                    else:
                        if (len(attack[TOON_KBBONUS_COL]) > tgtPos):
                            attack[TOON_KBBONUS_COL][tgtPos] = \
                                        totalDmgs * 0.5
                            if self.notify.getDebug():
                                self.notify.debug(
                                    "Applying kb bonus to track " +
                                    str(attack[TOON_TRACK_COL]) +
                                    " of " +
                                    str(attack[TOON_KBBONUS_COL][tgtPos]) +
                                    " to target " +
                                    str(tgtPos))
                        else:
                            self.notify.warning("invalid tgtPos for knock back bonus: %d" % tgtPos)
            # move on to the next suit in line
            tgtPos += 1

        if hp:
            self.__clearBonuses()
        else:
            self.__clearBonuses(hp=0)


    def __handleBonus(self, attackIdx, hp=1):
        """
        attackIdx, index into self.toonAtkOrder indicating
            which toon attack to calculate the HPBonus for
        
        Handle any Bonus that might apply for a specific
        toon attack (possible bonuses are hp and knockback)
        """
        attackerId = self.toonAtkOrder[attackIdx]
        attack = self.battle.toonAttacks[attackerId]
        atkDmg = self.__attackDamage(attack, suit=0)
        atkTrack = self.__getActualTrack(attack)
        if atkDmg > 0:
            if hp:
                # add the attack damage to the hpBonuses list
                # lures don't get hpBonuses
                if (atkTrack != LURE):
                    self.notify.debug("Adding dmg of " + str(atkDmg) +
                                       " to hpBonuses list")
                    self.__addDmgToBonuses(atkDmg, attackIdx)
            else:
                # make sure this attack can get a knockback bonus, if
                # so add the damage done by the attack to the kbBonuses
                # list
                if self.__knockBackAtk(attackerId, toon=1):
                    self.notify.debug("Adding dmg of " + str(atkDmg) +
                                       " to kbBonuses list")
                    self.__addDmgToBonuses(atkDmg, attackIdx, hp=0)


    def __clearAttack(self, attackIdx, toon=1):
        """
        // Parameters: attackIdx, the attack to clear out
        //             toon, 1 if this is a toon attack, 0 for a suit attack
        // Function:   clear out a specific attack, usually because it has
        //             been determined that all of its targets are dead
        """
        if toon:
            if self.notify.getDebug():
                self.notify.debug(
                    "clearing out toon attack for toon " +
                    str(attackIdx) +
                    "...")
            attack = self.battle.toonAttacks[attackIdx]
            self.battle.toonAttacks[attackIdx] = \
                                     getToonAttack(attackIdx)

            # make sure to create all the necessary hp columns
            # for this toon attack
            longest = max(len(self.battle.activeToons),
                          len(self.battle.activeSuits))
            taList = self.battle.toonAttacks
            for j in range(longest):
                taList[attackIdx][TOON_HP_COL].append(-1)
                taList[attackIdx][TOON_KBBONUS_COL].append(-1)

            if self.notify.getDebug():
                self.notify.debug("toon attack is now " + \
                                  repr(self.battle.toonAttacks[attackIdx]))
        else:
            self.notify.warning("__clearAttack not implemented for suits!")

    def __rememberToonAttack(self, suitId, toonId, damage):
        """
        suitId, the suit that the toon attacked
        toonId, the toon that attacked
        damage, how much damage the toon did to the suit
        
        Allow the suit to remember the toon that attacked
        it and it will attack back if it thinks the toon is
        worthy of his/her time
        """
        if not self.SuitAttackers.has_key(suitId):
            self.SuitAttackers[suitId] = { toonId: damage }
        elif not self.SuitAttackers[suitId].has_key(toonId):
            self.SuitAttackers[suitId][toonId] = damage
        elif self.SuitAttackers[suitId][toonId] <= damage:
            # this toon has done more damage than was done on a previous
            # round, so replace any lesser recorded damage for this toon
            self.SuitAttackers[suitId] = [toonId, damage]

    def __postProcessToonAttacks(self):
        """
        After all battle calculations have been performed
        for all toon attacks, make another pass through the
        attacks to clear out attacks that target dead suits
        and add up experience points gained by toons this
        round, also apply damages/heals done by toon attacks
        """
        # Now go through each toon attack in order and clear out any
        # that has all dead targets.  For any attack that is still left,
        # apply its damages to all of its targets
        self.notify.debug("__postProcessToonAttacks()")
        lastTrack = -1
        lastAttacks = []
        self.__clearBonuses()
        for currToonAttack in self.toonAtkOrder:
            if currToonAttack != -1:
                # if this attack targets suits, get all of its targets
                # and make sure at least one of them is still alive,
                # otherwise clear out the attack, also be sure to handle
                # any hp bonuses (excluding hp bonuses for heals)
                attack = self.battle.toonAttacks[currToonAttack]
                atkTrack, atkLevel = self.__getActualTrackLevel(attack)
                if (atkTrack != HEAL and atkTrack != SOS and 
                    atkTrack != NO_ATTACK and atkTrack != NPCSOS and
                    atkTrack != PETSOS):

                    targets = self.__createToonTargetList(currToonAttack)

                    allTargetsDead = 1
                    for currTgt in targets:
                        # be sure to let the suit remember which toon
                        # attacked it so the suit can attack back
                        # if the track of this attack is the same as that of
                        # the previous attack
                        damageDone = self.__attackDamage(attack, suit=0)
                        if damageDone > 0:
                            self.__rememberToonAttack(
                                currTgt.getDoId(),
                                attack[TOON_ID_COL],
                                damageDone)

                        # Make sure traps are placed on the suits
                        if (atkTrack == TRAP):
                            if (self.traps.has_key(currTgt.doId)):
                                trapInfo = self.traps[currTgt.doId]
                                currTgt.battleTrap = trapInfo[0]

                        targetDead = 0
                        if currTgt.getHP() > 0:
                            allTargetsDead = 0
                        else:
                            targetDead = 1
                            if (atkTrack != LURE):
                                # check every previous attack that is of
                                # the same track as the current attack.
                                # If they both kill the same suit, then
                                # clear out the suit died flag for the
                                # prevous attack.  This does not apply to
                                # LURE attacks since lure's are not combined
                                # during movie playback and thus the first lure
                                # did kill the suit and the second lure plays
                                # after the suit has already died.
                                for currLastAtk in lastAttacks:
                                    self.__clearTgtDied(currTgt, currLastAtk,
                                                         attack)

                        # process the successful lures list to see if this
                        # guy was lured and if so which attack successfully
                        # lured him/her/it
                        tgtId = currTgt.getDoId()
                        if (self.successfulLures.has_key(tgtId) and
                            atkTrack == LURE):
                            lureInfo = self.successfulLures[tgtId]
                            self.notify.debug("applying lure data: " +
                                               repr(lureInfo))
                            toonId = lureInfo[0]
                            lureAtk = self.battle.toonAttacks[toonId]
                            tgtPos = self.battle.activeSuits.index(currTgt)

                            #check if a train trap will triger, if so remember it
                            if (self.traps.has_key(currTgt.doId)):
                                trapInfo = self.traps[currTgt.doId]
                                if trapInfo[0] == UBER_GAG_LEVEL_INDEX:
                                    self.notify.debug('train trap triggered for %d' % currTgt.doId)
                                    self.trainTrapTriggered = True

                            # make sure to remove any trap that might be
                            # associated with this target since he/she/it
                            # is now lured and therefore should have
                            # triggered the trap
                            self.__removeSuitTrap(tgtId)

                            # be sure to flag that this target has been
                            # lured by this attack, and also indicate any
                            # damage that the lure might have resulted in
                            lureAtk[TOON_KBBONUS_COL][tgtPos] = \
                                     self.KBBONUS_TGT_LURED
                            lureAtk[TOON_HP_COL][tgtPos] = lureInfo[3]

                        elif (self.__suitIsLured(tgtId) and
                              atkTrack == DROP):
                            # if this is a drop on a lured suit,
                            # be sure to place a indicator in the
                            # KBBONUS_COL so the battle movie knows
                            # that this is a drop or sound on a lured suit
                            # and it should do something different than other
                            # attack types on lured suits
                            self.notify.debug("Drop on lured suit, " +
                                               "indicating with KBBONUS_COL " +
                                               "flag")
                            tgtPos = self.battle.activeSuits.index(currTgt)
                            attack[TOON_KBBONUS_COL][tgtPos] = \
                                    self.KBBONUS_LURED_FLAG

                        # if this individual target is dead, then make sure to
                        # clear out any damage and kbBonus info for it
                        if (targetDead and atkTrack != lastTrack):
                            tgtPos = self.battle.activeSuits.index(currTgt)
                            attack[TOON_HP_COL][tgtPos] = 0
                            attack[TOON_KBBONUS_COL][tgtPos] = -1

                    # Clear out this toon attack if all of its targets are
                    # dead and it is not part of a combo attack (one of a
                    # group of attacks from the same track).
                    if (allTargetsDead and atkTrack != lastTrack):
                        if self.notify.getDebug():
                            self.notify.debug("all targets of toon attack " +
                                               str(currToonAttack) +
                                               " are dead")
                        self.__clearAttack(currToonAttack, toon=1)
                        attack = self.battle.toonAttacks[currToonAttack]
                        atkTrack, atkLevel = self.__getActualTrackLevel(attack)

                # now apply any relevant damages to the target suit(s)
                # (or health to toons)
                damagesDone = self.__applyToonAttackDamages(currToonAttack)
                self.__applyToonAttackDamages(currToonAttack, hpbonus=1)

                # apply knockback bonuses for this attack only if it is not
                # a lure, since lures dont get knockback bonuses anyways and
                # we use the knockback bonuses values for something other
                # than knockback bonuses when the attack is a lure (same goes
                # for drops and sounds)
                if (atkTrack != LURE and atkTrack != DROP and 
                    atkTrack != SOUND):
                    self.__applyToonAttackDamages(currToonAttack, kbbonus=1)

                # remember the attack so the future attacks this round
                # that are of the same track type can look at them and
                # set the target died flag appropriately
                if (lastTrack != atkTrack):
                    lastAttacks = []
                    lastTrack = atkTrack 
                lastAttacks.append(attack)

                # record any exp received for this attack
                if (self.itemIsCredit(atkTrack, atkLevel)):
                    if (atkTrack == TRAP or atkTrack == LURE):
                        # Don't add trap exp here; that is handled as
                        # soon as the trap is triggered, and don't add
                        # lure exp here; that is only given if the
                        # lured targets are damaged while lured.
                        pass

                    elif (atkTrack == HEAL):
                        # For heal attacks, we only give credit if any
                        # heal points were actually awarded.  You don't
                        # get credit for healing someone who didn't need
                        # healing!
                        if damagesDone != 0:
                            self.__addAttackExp(attack)

                    else:
                        self.__addAttackExp(attack)

        if self.trainTrapTriggered:
            #since a train trap can be triggered from a single lure, make sure the
            #trap is removed for the other suits
            for suit in self.battle.activeSuits:
                suitId = suit.doId
                self.__removeSuitTrap(suitId)
                suit.battleTrap = NO_TRAP
                self.notify.debug('train trap triggered, removing trap from %d'  % suitId)

        # if debugging, print out all of the final toon attacks after all
        # adjustments have been performed on them
        if self.notify.getDebug():
            for currToonAttack in self.toonAtkOrder:
                attack = self.battle.toonAttacks[currToonAttack]
                self.notify.debug("Final Toon attack: " + str(attack))


    def __allTargetsDead(self, attackIdx, toon=1):
        """
        attackIdx, the attack to examine
        toon, 1 if this is a toon attack, 0 if it is suit
        Returns:    1 if all targets are dead, 0 otherwise
        
        Check to see if all targets of a specific attack
        are currently dead
        """
        allTargetsDead = 1
        if toon:
            # now that we have added some more damage done to any
            # targets, make sure to clear out
            targets = self.__createToonTargetList(attackIdx)
            for currTgt in targets:
                if currTgt.getHp() > 0:
                    allTargetsDead = 0
                    break
        else:
            self.notify.warning("__allTargetsDead: suit ver. not implemented!")
        return allTargetsDead


    def __clearLuredSuitsByAttack(self, toonId, kbBonusReq=0, targetId=-1):
        """
        toonId, the attack to wake suits up from
        kbBonusReq, 1 if a knockback bonus on the suit is
            required for the suit to become unlured, 0 if no
            knockback bonus is needed
        
        Wake up all suits which have been hit by the
        specified toon attack
        """
        if self.notify.getDebug():
            self.notify.debug("__clearLuredSuitsByAttack")
        if targetId != -1 and \
           self.__suitIsLured(t.getDoId()):
            self.__removeLured(t.getDoId())
        else:
            tgtList = self.__createToonTargetList(toonId)
            for t in tgtList:
                # for all targets of this attack, if any have received a
                # knockback bonus and are currently lured, wake them up
                if self.__suitIsLured(t.getDoId()) and \
                   (not kbBonusReq or self.__bonusExists(t, hp=0)):
                    self.__removeLured(t.getDoId())
                    if self.notify.getDebug():
                        self.notify.debug("Suit %d stepping from lured spot" %
                                          t.getDoId())
                else:
                    self.notify.debug("Suit " + str(t.getDoId()) +
                                       " not found in currently lured suits")

    def __clearLuredSuitsDelayed(self):
        """
        toonId, the attack to wake suits up from
        kbBonusReq, 1 if a knockback bonus on the suit is
            required for the suit to become unlured, 0 if no
            knockback bonus is needed
        
        Wke up all suits which have been hit by the
        specified toon attack
        """
        if self.notify.getDebug():
            self.notify.debug("__clearLuredSuitsDelayed")
        for t in self.delayedUnlures:
            # for all targets of this attack, if any have received a
            # knockback bonus and are currently lured, wake them up
            if self.__suitIsLured(t):
#                self.suitsUnluredThisRound.append(t)
                self.__removeLured(t)
                if self.notify.getDebug():
                    self.notify.debug("Suit %d stepping back from lured spot" %
                                      t)
            else:
                self.notify.debug("Suit " + str(t) +
                                   " not found in currently lured suits")
        self.delayedUnlures = []


    def __addLuredSuitsDelayed(self, toonId, targetId=-1, ignoreDamageCheck = False):
        """
        toonId, the attack to wake suits up from
        kbBonusReq, 1 if a knockback bonus on the suit is
            required for the suit to become unlured, 0 if no
            knockback bonus is needed
        
        Add any suits damaged by the specified toon attack
        to the delayed-unlure list to make sure that they
        will be unlured as soon as possible (usually when
        the last toon attack is processed or when a new track
        of toon attacks is processed, whichever comes first)
        """
        if self.notify.getDebug():
            self.notify.debug("__addLuredSuitsDelayed")
        if targetId != -1:
            # add only the specified target to the unlure list
            self.delayedUnlures.append(targetId)
        else:
            tgtList = self.__createToonTargetList(toonId)
            for t in tgtList:
                # for all targets of this attack, if any are lured then
                # plan to unlure them at a later time
                if self.__suitIsLured(t.getDoId()) and \
                   not t.getDoId() in self.delayedUnlures and \
                   (self.__attackDamageForTgt(self.battle.toonAttacks[toonId],
                                             self.battle.activeSuits.index(t),
                                             suit=0) > 0 or \
                    ignoreDamageCheck):
                    self.delayedUnlures.append(t.getDoId())


    def __calculateToonAttacks(self):
        """
        For each toon attack in the toonAttacks list,
        calculate and fill in appropriate damage,
        accuracyBonus, and HPBonus values
        """
        # a list of suits, and any knockback bonuses that are applied
        # to them, each sublist corresponds to each entry in battle.suits
        # the first value in the each sublist is the total knockback
        # bonus damage done to that suit, while the second value in each
        # sublist is the toon attack track that has gotten the corresponging
        # knockback bonus damage
        self.notify.debug("__calculateToonAttacks()")
        self.__clearBonuses(hp=0)
        currTrack = None

        self.notify.debug("Traps: " + str(self.traps))

        # Determine the maximum level attack item we'll get credit
        # for, based on the suits in the battle.  This is the same as
        # the highest level suit we're currently facing.
        maxSuitLevel = 0
        for cog in self.battle.activeSuits:
            maxSuitLevel = max(maxSuitLevel, cog.getActualLevel())
        self.creditLevel = maxSuitLevel
        

        for toonId in self.toonAtkOrder:
            # do some checks to make sure this toon actually has an attack
            # and that this toon is not already dead
            assert(toonId != -1)
            if self.__combatantDead(toonId, toon=1):
                if self.notify.getDebug():
                    self.notify.debug("Toon %d is dead and can't attack" %
                                       toonId)
                continue

            assert(self.battle.toonAttacks.has_key(toonId))
            attack = self.battle.toonAttacks[toonId]
            atkTrack = self.__getActualTrack(attack)
            

            
            if (atkTrack != NO_ATTACK and atkTrack != SOS and
                atkTrack != NPCSOS):

                if self.notify.getDebug():
                    self.notify.debug("Calculating attack for toon: %d" %
                                       toonId)

                # if this a new track of attacks, then any suit that is in
                # the 'unlure' list (list of suits that should be unlured
                # as soon as it is reasonable) should now be unlured
                # for now, only do this if suits are unlured immediately,
                # otherwise wait to unlure the suit until all toon attacks
                # have been calculated
                if self.SUITS_UNLURED_IMMEDIATELY:
                    if currTrack and atkTrack != currTrack:
                        self.__clearLuredSuitsDelayed()
                currTrack = atkTrack 

                # now calculate how much damage the attack has done, not yet
                # accounting for bonuses
                self.__calcToonAtkHp(toonId)

                # now handle the knockback and hp bonuses
                attackIdx = self.toonAtkOrder.index(toonId)
                self.__handleBonus(attackIdx, hp=0)
                self.__handleBonus(attackIdx, hp=1)

                # if this is the last toon attack this round, is an attack that
                # can knock a target back, and it has hit its target, be sure
                # to wakeup any suits knocked back by this attack, but if this
                # is not the last attack but still knocks back its target,
                # place the suit in the 'delayedUnlures' list to make sure it
                # is unlured when we get to a new track of attacks
                lastAttack = self.toonAtkOrder.index(toonId) >= \
                             len(self.toonAtkOrder) - 1
                unlureAttack = self.__attackHasHit(attack, suit=0) and \
                               self.__unlureAtk(toonId, toon=1)
                if unlureAttack:
                    if lastAttack:
                        self.__clearLuredSuitsByAttack(toonId)
                    else:
                        self.__addLuredSuitsDelayed(toonId)

                # if this is the last toon attack this round, be sure to clean
                # up any delayed unlured suits that might still be around,
                # possible unlured from this last attack or some other previous
                # attack that is of the same track as this one
                if lastAttack:
                    self.__clearLuredSuitsDelayed()

        # process all hpBonuses and kbBonuses and apply the appropriate
        # bonus values to the appropriate locations in the toonAttacks
        # then make a second pass on all toon attacks to clear out attacks
        # that no longer have valid targets
        self.__processBonuses(hp=0)
        self.__processBonuses(hp=1)
        self.__postProcessToonAttacks()

    def __knockBackAtk(self, attackIndex, toon=1):
        """
        attackIndex, the attack to check
        toon, whether or not the attack is a toon attack
        Returns:    1 if the attack is a knockback attack, 0 otherwise
        
        Determine if a specific attack is one that is
        eligible for a knockback bonus
        """
        if toon and \
           (self.battle.toonAttacks[attackIndex][TOON_TRACK_COL] == THROW or \
             self.battle.toonAttacks[attackIndex][TOON_TRACK_COL] == SQUIRT):
            if self.notify.getDebug():
                self.notify.debug("attack is a knockback")
            return 1
        return 0

    def __unlureAtk(self, attackIndex, toon=1):
        """
        attackIndex, the attack to check
        toon, whether or not the attack is a toon attack
        Returns:    1 if the attack is an unlure attack, 0 otherwise
        
        Determine if a specific attack is one that is
        eligible for unluring a target
        """
        attack = self.battle.toonAttacks[attackIndex]
        track = self.__getActualTrack(attack)
        if (toon and (track == THROW or track == SQUIRT or track == SOUND)):
            if self.notify.getDebug():
                self.notify.debug("attack is an unlure")
            return 1
        return 0

    def __calcSuitAtkType(self, attackIndex):
        """
        attackIndex, row in suitAttacks that contains the
            attack type and the target of the attack
        
        Determine the best attack type for a suit
        """
        theSuit = self.battle.activeSuits[attackIndex]
        attacks = SuitBattleGlobals.SuitAttributes[theSuit.dna.name]['attacks']
        atk = SuitBattleGlobals.pickSuitAttack(attacks, theSuit.getLevel())
        return atk

    def __calcSuitTarget(self, attackIndex):
        """
        attackIndex, row in suitAttacks that contains the
            attack type and the target of the attack
        Returns:     an index into the battle.toons list indicating the
                     target for the specified suit attack
        
        Determine the best target for a suit attack
        """
        attack = self.battle.suitAttacks[attackIndex]
        suitId = attack[SUIT_ID_COL]
        if self.SuitAttackers.has_key(suitId) and \
           random.randint(0, 99) < 75:
            # first calculate the total damage done to this suit by all
            # recorded attackers, this is so we can create a frequency
            # list of damage percentages that we can randomly pick from
            totalDamage = 0
            for currToon in self.SuitAttackers[suitId].keys():
                totalDamage += self.SuitAttackers[suitId][currToon]

            # create a list of damage percentages and pick one of the
            # weighted values, this tells us which toon attacker that
            # the suit should attack
            dmgs = []
            for currToon in self.SuitAttackers[suitId].keys():
                dmgs.append((self.SuitAttackers[suitId][currToon] /
                               totalDamage) * 100)
            dmgIdx = SuitBattleGlobals.pickFromFreqList(dmgs)
            if (dmgIdx == None):
                toonId = self.__pickRandomToon(suitId) 
            else:
                toonId = self.SuitAttackers[suitId].keys()[dmgIdx]
            if (toonId == -1 or toonId not in self.battle.activeToons):
                return -1
            self.notify.debug("Suit attacking back at toon " + str(toonId))
            return self.battle.activeToons.index(toonId)
        else:
            #return random.randint(0, len(self.battle.activeToons) - 1)
            # make sure we only randomly choose from the active toons
            # that are still alive at this point in the round
            return self.__pickRandomToon(suitId)

    def __pickRandomToon(self, suitId):
        liveToons = []
        for currToon in self.battle.activeToons:
            if not self.__combatantDead(currToon, toon=1):
                liveToons.append(self.battle.activeToons.index(currToon))
        if len(liveToons) == 0:
            # no toons left alive to attack
            self.notify.debug("No tgts avail. for suit " + str(suitId))
            return -1
        chosen = random.choice(liveToons)
        self.notify.debug("Suit randomly attacking toon " +
                           str(self.battle.activeToons[chosen]))
        return chosen

    def __suitAtkHit(self, attackIndex):
        """
        Calculate whether or not a specific suit attack hit
        """
        if self.suitsAlwaysHit:
            return 1
        elif self.suitsAlwaysMiss:
            return 0
        theSuit = self.battle.activeSuits[attackIndex]
        atkType = self.battle.suitAttacks[attackIndex][SUIT_ATK_COL]

        atkInfo = SuitBattleGlobals.getSuitAttack(theSuit.dna.name,
                                                   theSuit.getLevel(),
                                                   atkType)
        atkAcc = atkInfo['acc']
        suitAcc = SuitBattleGlobals.SuitAttributes[theSuit.dna.name]\
                  ['acc'][theSuit.getLevel()]

        # Jesse changed this because he doesn't think we need suit
        # accuracies.
        #acc = (atkAcc + suitAcc) / 2
        acc = atkAcc
        randChoice = random.randint(0, 99)
        if self.notify.getDebug():
            self.notify.debug("Suit attack rolled " + str(randChoice) +
                               " to hit with an accuracy of " + str(acc) +
                               " (attackAcc: " + str(atkAcc) +
                               " suitAcc: " + str(suitAcc) + ")")
        if randChoice < acc:
            return 1
        return 0

    def __suitAtkAffectsGroup(self, attack):
        atkType = attack[SUIT_ATK_COL]

        # determine if the attack targets a group or an individual
        theSuit = self.battle.findSuit(attack[SUIT_ID_COL])
        assert theSuit != None
        atkInfo = SuitBattleGlobals.getSuitAttack(theSuit.dna.name,
                                                   theSuit.getLevel(),
                                                   atkType)
        return atkInfo['group'] != SuitBattleGlobals.ATK_TGT_SINGLE

    def __createSuitTargetList(self, attackIndex):
        """
        attackIndex, index into the suitAttacks list which
            indicates which attack we are using
        
        Create a list of targets for the specified suit
        attack, the target type of the attack determines
        which participants in the battle are targets
        """
        attack = self.battle.suitAttacks[attackIndex]
        targetList = []
        if attack[SUIT_ATK_COL] == NO_ATTACK:
            self.notify.debug("No attack, no targets")
            return targetList
        debug = self.notify.getDebug()

        if not self.__suitAtkAffectsGroup(attack):
            # add only the specified target to the target list
            targetList.append(self.battle.activeToons[attack[SUIT_TGT_COL]])
            if debug:
                self.notify.debug("Suit attack is single target")
        else:
            # all toons currently in battle
            if debug:
                self.notify.debug("Suit attack is group target")
            for currToon in self.battle.activeToons:
                if debug:
                    self.notify.debug("Suit attack will target toon" +
                                       str(currToon))
                targetList.append(currToon)
        return targetList

    def __calcSuitAtkHp(self, attackIndex):
        """
        attackIndex, row in suitAttacks that contains the
            attack type and the target of the attack
        
        Calculate how much damage a specific suit attack
        does to a toon
        """
        targetList = self.__createSuitTargetList(attackIndex)
        attack = self.battle.suitAttacks[attackIndex]
        
        for currTarget in range(len(targetList)):
            toonId = targetList[currTarget]
            toon = self.battle.getToon(toonId)

            result = 0
            if toon and toon.immortalMode:
                # At least 1 hp, otherwise the battle counts it as a miss.
                result = 1
            elif self.TOONS_TAKE_NO_DAMAGE:
                result = 0
            elif self.__suitAtkHit(attackIndex):
                # suits don't get any accuracy or damage bonuses
                atkType = attack[SUIT_ATK_COL]

                theSuit = self.battle.findSuit(attack[SUIT_ID_COL])
                atkInfo = SuitBattleGlobals.getSuitAttack(
                    theSuit.dna.name,
                    theSuit.getLevel(),
                    atkType)
                result = atkInfo['hp']

            # be sure to set the amount of damage done by this attack
            # in the appropriate slot in the toonAttacks list
            # corresponding to this target
            targetIndex = self.battle.activeToons.index(toonId)
            attack[SUIT_HP_COL][targetIndex] = result

    def __getToonHp(self, toonDoId):
        """
        toonDoId, the unique id of the toon
        Returns:     the health of the specified toon, as it is
                     currently known on the server
        
        Get the health of a toon given its doId
        """
        handle = self.battle.getToon(toonDoId)
        if handle != None and self.toonHPAdjusts.has_key(toonDoId):
            return handle.hp + self.toonHPAdjusts[toonDoId]
        else:
            return 0

    def __getToonMaxHp(self, toonDoId):
        """
        toonDoId, the unique id of the toon
        Returns:     the health of the specified toon, as it is
                     currently known on the server
        
        Get the health of a toon given its doId
        """
        handle = self.battle.getToon(toonDoId)
        if (handle != None):
            assert(self.toonHPAdjusts.has_key(toonDoId))
            return handle.maxHp
        else:
            return 0

    def __applySuitAttackDamages(self, attackIndex):
        """
        attackIndex, the suit attack to apply damages for
        
        Apply damages created by the specified suit attack
        """
        # we dont actually adjust the toon health here, we just need to
        # indicate if the toon has died and print something out for each
        # toon hit
        attack = self.battle.suitAttacks[attackIndex]
        if self.APPLY_HEALTH_ADJUSTMENTS:
            for t in self.battle.activeToons:
                # first see if the toon was damaged by this attack
                position = self.battle.activeToons.index(t)
                assert(position < len(attack[SUIT_HP_COL]))
                if attack[SUIT_HP_COL][position] <= 0:
                    # toon at this position was not hit by this attack
                    continue

                # now see if the toon had died, if so, remove the toon from
                # the battle and mark the toon as being killed by this attack
                # also, whether or not the toon is dead, adjust the hp adjust
                # value for the toon in our toonHPAdjusts list which is used
                # to keep toon health values as up to date as possible so we
                # know exactly when the toon died within the sequence of
                # attacks
                assert(position < len(attack[SUIT_HP_COL]))
                toonHp = self.__getToonHp(t)
                assert(self.toonHPAdjusts.has_key(t))
                if toonHp - attack[SUIT_HP_COL][position] <= 0:
                    if self.notify.getDebug():
                        self.notify.debug("Toon %d has died, removing" % t)
                    self.toonLeftBattle(t)
                    attack[TOON_DIED_COL] = \
                        attack[TOON_DIED_COL] | (1 << position)
                if self.notify.getDebug():
                    self.notify.debug("Toon " + str(t) + " takes " +
                                       str(attack[SUIT_HP_COL][position]) +
                                       " damage")
                self.toonHPAdjusts[t] -= attack[SUIT_HP_COL][position]
                self.notify.debug("Toon " + str(t) + " now has " +
                                   str(self.__getToonHp(t)) + " health")

    def __suitCanAttack(self, suitId):
        """
        suitId, the suit to check
        Returns:    1 if the suit can attack, 0 otherwise
        
        Check to see if a specific suit is able to attack.
        various factors determine this, such as if the suit
        is lured and if the suit is dead
        """
        if self.__combatantDead(suitId, toon=0) or \
           self.__suitIsLured(suitId) or self.__combatantJustRevived(suitId):
            return 0
        return 1

    def __updateSuitAtkStat(self, toonId):
        if self.suitAtkStats.has_key(toonId):
            self.suitAtkStats[toonId] += 1
        else:
            self.suitAtkStats[toonId] = 1

    def __printSuitAtkStats(self):
        self.notify.debug("Suit Atk Stats:")
        for currTgt in self.suitAtkStats.keys():
            if not currTgt in self.battle.activeToons:
                continue
            tgtPos = self.battle.activeToons.index(currTgt)
            self.notify.debug(" toon " + str(currTgt) +
                               " at position " + str(tgtPos) +
                               " was attacked " +
                               str(self.suitAtkStats[currTgt]) +
                               " times")
        self.notify.debug("\n")

    def __calculateSuitAttacks(self):
        """
        For each suit attack on the suitAttacks list,
        calculate and fill in appropriate attack type,
        target, and damage information
        """
        for i in range(len(self.battle.suitAttacks)):
            if i < len(self.battle.activeSuits):

                # check to make sure that the suit is not dead before
                # worrying about its attack, but before doing that make
                # sure the current suit attack refers to an existing suit
                # by setting the doId of the attack to the suit that is
                # performing the attack
                suitId = self.battle.activeSuits[i].doId
                self.battle.suitAttacks[i][SUIT_ID_COL] = suitId
                if not self.__suitCanAttack(suitId):
                    if self.notify.getDebug():
                        self.notify.debug("Suit %d can't attack" % suitId)
                    continue

                # make sure this suit is not in either the pending
                # or to pending lists
                if self.battle.pendingSuits.count(
                                self.battle.activeSuits[i])>0 or \
                   self.battle.joiningSuits.count(
                                self.battle.activeSuits[i])>0:
                    continue

                attack = self.battle.suitAttacks[i]
                # only perform attack calculations if this suit exists in
                # the list of suits currently existing in the battle
                # order of calculation matters, since some calculations depend
                # on previously calculated values, such as an attack's damage
                # depending on attack type, we also need to handle damage
                # to multiple targets for group attacks
                attack[SUIT_ID_COL] = self.battle.activeSuits[i].doId
                attack[SUIT_ATK_COL] = self.__calcSuitAtkType(i)
                attack[SUIT_TGT_COL] = self.__calcSuitTarget(i)
                if attack[SUIT_TGT_COL] == -1:
                    # no available target, clear out the suit attack
                    self.battle.suitAttacks[i] = getDefaultSuitAttack()
                    attack = self.battle.suitAttacks[i]
                    self.notify.debug("clearing suit attack, no avail targets")
                self.__calcSuitAtkHp(i)

                # for debugging, keep track of how many times each toon
                # was attacked
                if attack[SUIT_ATK_COL] != NO_ATTACK:
                    if self.__suitAtkAffectsGroup(attack):
                        for currTgt in self.battle.activeToons:
                            self.__updateSuitAtkStat(currTgt)
                    else:
                        tgtId = self.battle.activeToons[attack[SUIT_TGT_COL]]
                        self.__updateSuitAtkStat(tgtId)

                # if this attack targets suits, get all of its targets
                # and make sure at least one of them is still alive,
                # otherwise clear out the attack
                targets = self.__createSuitTargetList(i)
                allTargetsDead = 1
                for currTgt in targets:
                    if self.__getToonHp(currTgt) > 0:
                        allTargetsDead = 0
                        break
                if allTargetsDead:
                    # clear out attack, all targets for it are already dead
                    self.battle.suitAttacks[i] = \
                        getDefaultSuitAttack()
                    if self.notify.getDebug():
                        self.notify.debug("clearing suit attack, targets dead")
                        self.notify.debug("suit attack is now " + \
                                          repr(self.battle.suitAttacks[i]))
                        self.notify.debug("all attacks: " +
                                          repr(self.battle.suitAttacks))
                    attack = self.battle.suitAttacks[i]

                # now apply any relevant damages to the target toon(s)
                if self.__attackHasHit(attack, suit=1):
                    self.__applySuitAttackDamages(i)

                if self.notify.getDebug():
                    self.notify.debug("Suit attack: " +
                                       str(self.battle.suitAttacks[i]))

                # determine if this suit will attack after the toon attacks
                # or after.  For now, all toons attack before any suits
                attack[SUIT_BEFORE_TOONS_COL] = 0

    def __updateLureTimeouts(self):
        """
        Check all lured suits and see if the lure has expired
        also randomly un-lure suits
        """
        # check for lured suits and determine which should no longer be
        # lured
        if self.notify.getDebug():
            self.notify.debug("__updateLureTimeouts()")
            self.notify.debug("Lured suits: " + str(self.currentlyLuredSuits))
        noLongerLured = []

        # check each lured suit, add to the lured suit's count of how many
        # rounds it has been lured, then check to see if the suit has now been
        # lured for the maximum rounds allowed for the particular lure used
        # on the suit, if not, randomly decide if the suit should 'magically
        # wake up' from the lure based on the fail chance of the particular
        # lure originally used on the suit
        for currLuredSuit in self.currentlyLuredSuits.keys():
            self.__incLuredCurrRound(currLuredSuit)
            if self.__luredMaxRoundsReached(currLuredSuit) or \
               self.__luredWakeupTime(currLuredSuit):
                noLongerLured.append(currLuredSuit)

        # now we can safely clear out the no-longer-lured suits
        for currLuredSuit in noLongerLured:
#            self.suitsUnluredThisRound.append(currLuredSuit)
            self.__removeLured(currLuredSuit)
        if self.notify.getDebug():
            self.notify.debug("Lured suits: " + str(self.currentlyLuredSuits))


    def __initRound(self):
        """
        Called when a new round starts, sets up initial
        values used to calculate various bonuses
        """
        # only allow suits to remember who attacked them for a single round
        if self.CLEAR_SUIT_ATTACKERS:
            self.SuitAttackers = {}

        # fill in self.toonAtkOrder at the beginning of each round, this
        # list contains the order of toon attacks, each element
        # is an index into the self.battle.toonAttacks list
        self.toonAtkOrder = []
        # Fill in PETSOS attacks first
        attacks = findToonAttack(self.battle.activeToons,
                                 self.battle.toonAttacks,
                                 PETSOS)
        for atk in attacks:
            self.toonAtkOrder.append(atk[TOON_ID_COL])
            
        
        #Do the cog firing
        attacks = findToonAttack(self.battle.activeToons,
                                 self.battle.toonAttacks,
                                 FIRE)
        for atk in attacks:
            self.toonAtkOrder.append(atk[TOON_ID_COL])
            

        for track in range(HEAL, DROP + 1):
            # find all attacks for each possible type of attack
            attacks = findToonAttack(self.battle.activeToons,
                                     self.battle.toonAttacks,
                                     track)
            # Make sure that any non-NPC traps occur before the first
            # NPC trap (if any)
            if (track == TRAP):
                sortedTraps = []
                for atk in attacks:
                    if (atk[TOON_TRACK_COL] == TRAP):
                        sortedTraps.append(atk)
                for atk in attacks:
                    if (atk[TOON_TRACK_COL] == NPCSOS):
                        sortedTraps.append(atk)
                assert(len(attacks) == len(sortedTraps))
                attacks = sortedTraps
                
            for atk in attacks:
                # indicate where this toon fits in in the order of things, and
                # be sure to move to the next attack
                self.toonAtkOrder.append(atk[TOON_ID_COL])

        # Handle special NPC attacks
        specials = findToonAttack(self.battle.activeToons,
                                  self.battle.toonAttacks, NPCSOS)

        toonsHit = 0
        cogsMiss = 0
        for special in specials:
            npc_track = NPCToons.getNPCTrack(special[TOON_TGT_COL])
            if (npc_track == NPC_TOONS_HIT):
                BattleCalculatorAI.toonsAlwaysHit = 1
                toonsHit = 1
            elif (npc_track == NPC_COGS_MISS):
                BattleCalculatorAI.suitsAlwaysMiss = 1 
                cogsMiss = 1

        if self.notify.getDebug():
            self.notify.debug("Toon attack order: " +
                               str(self.toonAtkOrder))
            self.notify.debug("Active toons: " +
                               str(self.battle.activeToons))
            self.notify.debug("Toon attacks: " +
                               str(self.battle.toonAttacks))
            self.notify.debug("Active suits: " +
                               str(self.battle.activeSuits))
            self.notify.debug("Suit attacks: " +
                               str(self.battle.suitAttacks))

        # all toons should now have their HP set properly locally, so
        # clear out any HP adjustments we may have, this list contains
        # a list of indexes into battle.toons
        self.toonHPAdjusts = {}
        for t in self.battle.activeToons:
            self.toonHPAdjusts[t] = 0

        # list used for calculating HPBonuses that toons may receive by
        # coordinating attacks
        self.__clearBonuses()

        # remove any toons that are no longer in the battle, this can happen
        # if a toon has recently left unexpectedly
        self.__updateActiveToons()
        self.delayedUnlures = []

        # initialize the traps list each round, which consists of removing
        # trap conflicts that might have occurred last round
        self.__initTraps()

        # clear out the successful lures map which is used to figure out
        # for each target which lures apply and which don't
        self.successfulLures = {}

        # clear the list that we use to keep track of suits unlured during
        # a single round of attacks
#        self.suitsUnluredThisRound = []

        return toonsHit, cogsMiss 

    def calculateRound(self):
        """
        Calculate a single round of toon and suit attacks
        for a single battle
        """
        # Make sure toonAttacks have the right number of TOON_HP_COL
        # initial values and TOON_KBBONUS_COL initial values
        # Also make sure suitAttacks have the right number of SUIT_HP_COL
        # initial values
        longest = max(len(self.battle.activeToons),
                      len(self.battle.activeSuits))
        for t in self.battle.activeToons:
            assert(self.battle.toonAttacks.has_key(t))
            for j in range(longest):
                self.battle.toonAttacks[t][TOON_HP_COL].append(-1)
                self.battle.toonAttacks[t][TOON_KBBONUS_COL].append(-1)
        for i in range(4):
            for j in range(len(self.battle.activeToons)):
                self.battle.suitAttacks[i][SUIT_HP_COL].append(-1)

        # set-up some initial values that help calculate various bonuses
        # that can occurr in a round
        toonsHit, cogsMiss = self.__initRound()

        # broadcast the active suit HP's to everyone in the battle
        for suit in self.battle.activeSuits:
            if suit.isGenerated():
                suit.b_setHP(suit.getHP())
            
        # test to see if the suits have been deleted and do nothing if that is the case    
        for suit in self.battle.activeSuits:
            if not hasattr(suit, "dna"):
                self.notify.warning("a removed suit is in this battle!")
                return None
                
       
        
        #self.__calculateFiredCogs(self)
        
        # perform number calculations, also apply damages/heals
        self.__calculateToonAttacks()

        # update lure timeout values after toon attacks and before suit
        # attacks, so suits can wake up from being lured before their chance
        # to attack but the toons still have a chance to hit a lured suit
        # this round
        self.__updateLureTimeouts()

        self.__calculateSuitAttacks()

        # Restore globals
        if (toonsHit == 1):
            BattleCalculatorAI.toonsAlwaysHit = 0
        if (cogsMiss == 1):
            BattleCalculatorAI.suitsAlwaysMiss = 0

        if self.notify.getDebug():
            self.notify.debug("Toon skills gained after this round: " + \
                               repr(self.toonSkillPtsGained))
            self.__printSuitAtkStats()

        return None
        
    def __calculateFiredCogs():
        import pdb; pdb.set_trace()

    def toonLeftBattle(self, toonId):
        """
        toonId, the id of the toon that has left the battle
        
        Notify the battle calculator when a toon leaves
        this battle
        """
        if self.notify.getDebug():
            self.notify.debug('toonLeftBattle()' + str(toonId))
        if self.toonSkillPtsGained.has_key(toonId):
            del self.toonSkillPtsGained[toonId]
        if self.suitAtkStats.has_key(toonId):
            del self.suitAtkStats[toonId]

        if not self.CLEAR_SUIT_ATTACKERS:
            # clear out the SuitAttackers map (which allows suits to remember
            # which toons attacked him/her last round) of the specified toonId
            oldSuitIds = []
            for s in self.SuitAttackers.keys():
                if self.SuitAttackers[s].has_key(toonId):
                    del self.SuitAttackers[s][toonId]
                    if len(self.SuitAttackers[s]) == 0:
                        oldSuitIds.append(s)

            # remove any suit ids that refer to an empty toonId/damage map
            for oldSuitId in oldSuitIds:
                del self.SuitAttackers[oldSuitId]

        # clear out any reference that a trap might have for this toon,
        # this means that any trap this toon created that still exists
        # and gets triggered will no longer give trap exp to this toon
        self.__clearTrapCreator(toonId)

        # remove any references of this toon from the currentlyLuredSuits
        # list, which remembers which toons lured which suits (used for
        # giving the toon exp when the lured suit takes damage), when a
        # toon leaves the battle, any lure credit for the toon is removed
        self.__clearLurer(toonId)

    def suitLeftBattle(self, suitId):
        """
        suitId, the id of the suit that has left the battle
        
        Notify the battle calculator when a suit leaves
        this battle (most likely by death)
        """
        if self.notify.getDebug():
            self.notify.debug('suitLeftBattle(): ' + str(suitId))

        # remove the suit from the currently lured suits list
        self.__removeLured(suitId)

        # also make sure to remove the suit from the 'which toon attacked
        # me last round' list
        if self.SuitAttackers.has_key(suitId):
            del self.SuitAttackers[suitId]

        # remove the suit from the traps list which helps us keep track of
        # which suits have traps on them
        self.__removeSuitTrap(suitId)

    def __updateActiveToons(self):
        """
        Every round, update lists that remember toon id's
        from previous rounds, because a toon might have
        unexpectedly left the battle
        """
        if self.notify.getDebug():
            self.notify.debug('updateActiveToons()')
        # don't remove exp for toons that are not in this battle; some
        # parts of the game (factories, VP battles) use a single dict
        # to accumulate toon exp over multiple battles; toons that are in
        # the dict may be currently in a different battle or not in a
        # battle at all, but that's no reason to remove them from the dict.
        # exp entries are removed when a toon leaves this battle before it
        # finishes (when they get sad, run away, or disconnect) --
        # see DistributedBattleBaseAI.__removeToon
        #for toonId in self.toonSkillPtsGained.keys():
        #    if not toonId in self.battle.activeToons:
        #        self.notify.debug("Exp for toon " + str(toonId) +
        #                           " has been cleared")
        #        del self.toonSkillPtsGained[toonId]

        if not self.CLEAR_SUIT_ATTACKERS:
            # clear out the SuitAttackers map (which allows suits to remember
            # which toons attacked him/her last round) of all toons that are
            # not found in the battle.activeToons list
            oldSuitIds = []
            for s in self.SuitAttackers.keys():
                for t in self.SuitAttackers[s].keys():
                    if not t in self.battle.activeToons:
                        del self.SuitAttackers[s][t]
                        if len(self.SuitAttackers[s]) == 0:
                            oldSuitIds.append(s)

            # remove any suit ids that refer to an empty toonId/damage map
            for oldSuitId in oldSuitIds:
                del self.SuitAttackers[oldSuitId]

        # clear out any traps creator id's that refer to a toon not found
        # in the active toons list
        for trap in self.traps.keys():
            if not self.traps[trap][1] in self.battle.activeToons:
                self.notify.debug("Trap for toon " +
                                   str(self.traps[trap][1]) +
                                   " will no longer give exp")
                self.traps[trap][1] = 0

    def getSkillGained(self, toonId, track):
        return BattleExperienceAI.getSkillGained(self.toonSkillPtsGained, toonId, track)

    def getLuredSuits(self):
        """
        Get the doId's of all suits that are currently lured
        """
        luredSuits = self.currentlyLuredSuits.keys()
        # make sure that any suits that were still lured at the begining
        # of this round are still in the lured suits list that we return
        # to the battle
#        for currLured in self.suitsUnluredThisRound:
#            if not currLured in luredSuits:
#                luredSuits.append(currLured)
        self.notify.debug("Lured suits reported to battle: " +
                           repr(luredSuits))
        return luredSuits

    def __suitIsLured(self, suitId, prevRound=0):
        """
        suitId, doId of the suit to checkout
        prevRound, only return true if the suit has been
            lured in a previous round
        Returns:     1 if the suit is lured, 0 otherwise
        
        Check to see if a suit is currently lured
        """
        inList = self.currentlyLuredSuits.has_key(suitId)
        if prevRound:
            # only return true if the suit has been lured for at least
            # one entire round
            return inList and self.currentlyLuredSuits[suitId][0] != -1
        return inList

    def __findAvailLureId(self, lurerId):
        """
        lurerId, the doId of the lurer
        Returns:    the lowest available unique lure id wrt to the
                    specified lurer
        Find the lowest available lure id associated with
        a specific lurer, this way suits lured by different
        lure attacks from the same lurer can be distinguished
        from each other and exp can be given properly
        """
        luredSuits = self.currentlyLuredSuits.keys()
        lureIds = []
        for currLured in luredSuits:
            lurerInfo = self.currentlyLuredSuits[currLured][3]
            lurers = lurerInfo.keys()
            for currLurer in lurers:
                # if we have found a match for the specified lurer, add the
                # lureId to a list of lureId's for this toon
                currId = lurerInfo[currLurer][1]
                if currLurer == lurerId and not currId in lureIds:
                    lureIds.append(currId)
        lureIds.sort()
        currId = 1
        for currLureId in lureIds:
            if currLureId != currId:
                return currId
            currId += 1
        return currId

    def __addLuredSuitInfo(self, suitId, currRounds, maxRounds, wakeChance,
                            lurer, lureLvl, lureId=-1, npc=0):
        """
        suitId, doId of the suit to be added
        currRounds, current number of rounds that the suit
            has been lured for (usually this should
            be -1 when a suit is first lured)
        maxRounds, maximum number of battle rounds that this
            suit will be lured
        wakeChance, percent chance of the suit becoming
            unlured each battle round
        lurer, doId of the toon that lured this suit
        lureLvl, the level of the lure used
        lureId, if provided, use this value to identify
            this specific lure, if not provided find
            the lowest available lure id unique to the
            lurer
        Returns:    the id used for the lure info, this can be used to
                    pass back to this function when we are adding
                    multiple lured suit infos for the same lure
        
        Add a suit to the lured suits list (updates any
        currently existing data if the suit is already lured,
        and adds a reference to the lurer so exp can be given
        if the suit takes damage while lured)
        """
        if lureId == -1:
            availLureId = self.__findAvailLureId(lurer)
        else:
            availLureId = lureId
        # Nobody gets experience for NPC lures
        if (npc == 1):
            credit = 0
        else:
            credit = self.itemIsCredit(LURE, lureLvl)

        if self.currentlyLuredSuits.has_key(suitId):
            # This suit was already lured; we're just luring it more.

            lureInfo = self.currentlyLuredSuits[suitId]
            if not lureInfo[3].has_key(lurer):
                # This toon hasn't lured this suit yet this time around.
                lureInfo[1] += maxRounds
                if wakeChance < lureInfo[2]:
                    lureInfo[2] = wakeChance
                lureInfo[3][lurer] = [lureLvl, availLureId, credit]

        else:
            # This suit hadn't been lured yet.
            lurerInfo = { lurer: [lureLvl, availLureId, credit] }
            self.currentlyLuredSuits[suitId] = \
                                      [currRounds, maxRounds, wakeChance,
                                        lurerInfo]
        self.notify.debug("__addLuredSuitInfo: currLuredSuits -> %s" %
                           repr(self.currentlyLuredSuits))
        return availLureId

    def __getLurers(self, suitId):
        """
        suitId, the id of the lured suit
        Returns:    a list of doId's of the lurers, empyt list if there
                    are none
        
        Get the doId of the toon that lured the specified
        suit
        """
        if self.__suitIsLured(suitId):
            return self.currentlyLuredSuits[suitId][3].keys()
        return []

    def __getLuredExpInfo(self, suitId):
        """
        suitId, the doId of the target to get lured info for
        Returns:    a list of lists, each containing the lurer's doId,
                    the level of the lure used, and the unique id
                    distinguishing this particular lure from other
                    possible lures from the same lurer, followed by
                    a boolean flag indicating whether the lurer deserves
                    experience credit:
                    [[<lurerId>, <lureLvl>, <lureId>, <credit>], [...], ...]
        
        Get lurer info for a specific target, this way when
        this lured target takes damage we can get the
        appropriate amount of exp to anyone that helped lure
        this target
        """
        returnInfo = []
        lurers = self.__getLurers(suitId)
        if len(lurers) == 0:
            return returnInfo
        lurerInfo = self.currentlyLuredSuits[suitId][3]
        for currLurer in lurers:
            returnInfo.append([currLurer,
                                 lurerInfo[currLurer][0],
                                 lurerInfo[currLurer][1],
                                 lurerInfo[currLurer][2],
                                ])
        return returnInfo

    def __clearLurer(self, lurerId, lureId=-1):
        """
        lurerId, the doId of the toon to clear from the list
        lureId, the unique id of the lure that lured this
            target, this is useful to only clear
            references of a specific lurer AND a specifc
            lure (since a single lurer may have done
            more than a single lure on any of the
            currently lured targets)
        
        Remove any references to the specified toon from the
        lured suits list
        """
        luredSuits = self.currentlyLuredSuits.keys()
        for currLured in luredSuits:
            lurerInfo = self.currentlyLuredSuits[currLured][3]
            lurers = lurerInfo.keys()
            for currLurer in lurers:
                if currLurer == lurerId and \
                   (lureId == -1 or lureId == lurerInfo[currLurer][1]):
                    del lurerInfo[currLurer]

    def __setLuredMaxRounds(self, suitId, rounds):
        """
        suitId, the suit to modify the lure info for
        rounds, the new maximum number of battle rounds
        
        Change the maximum number of battle rounds that a
        specific suit will stay lured
        """
        if self.__suitIsLured(suitId):
            self.currentlyLuredSuits[suitId][1] = rounds

    def __setLuredWakeChance(self, suitId, chance):
        """
        suitId, the suit to modify the lure info for
        chance, the new wakeup chance
        
        Change the percentage chance that a specific suit
        will wakeup from being lured each battle round
        """
        if self.__suitIsLured(suitId):
            self.currentlyLuredSuits[suitId][2] = chance

    def __incLuredCurrRound(self, suitId):
        """
        suitId, the suit to modify the lure info for
        
        Increment the number of battle rounds that a specific
        suit has been lured for
        """
        if self.__suitIsLured(suitId):
            self.currentlyLuredSuits[suitId][0] += 1

    def __removeLured(self, suitId):
        """
        suitId, the suit to be unlured
        
        Unlure a specific suit
        """
        if self.__suitIsLured(suitId):
            del self.currentlyLuredSuits[suitId]

    def __luredMaxRoundsReached(self, suitId):
        """
        suitId, the suit to check lure info for
        Returns:    1 if the suit has reached max rounds, 0 otherwise
        
        Check to see if a specific suit has reached the max
        number of rounds that it can be lured for
        """
        return self.__suitIsLured(suitId) and \
               self.currentlyLuredSuits[suitId][0] >= \
               self.currentlyLuredSuits[suitId][1]

    def __luredWakeupTime(self, suitId):
        """
        suitId, the suit to check on
        Returns:    1 if the suit has awakened, 0 otherwise
        
        Check to see if a specific suit randomly wakes up
        from being lured (should only be called once each
        battle round since a random check is made each call)
        """
        return self.__suitIsLured(suitId) and \
               self.currentlyLuredSuits[suitId][0] > 0 and \
               random.randint(0, 99) < \
               self.currentlyLuredSuits[suitId][2]

    def itemIsCredit(self, track, level):
        """
        This returns true if a toon will gain credit for using this
        item in this particular battle, false otherwise.  This is
        based on the credit level computed at the beginning of
        __calculateToonAttacks.
        """
        if (track == PETSOS):
            return 0
        return level < self.creditLevel

    def __getActualTrack(self, toonAttack):
        # NPC friends share the same attack columns, so we often need to
        # convert from an NPCSOS track to whatever track the NPC uses
        if (toonAttack[TOON_TRACK_COL] == NPCSOS):
            track = NPCToons.getNPCTrack(toonAttack[TOON_TGT_COL])
            if (track != None):
                return track
            else:
                self.notify.warning("No NPC with id: %d" % toonAttack[TOON_TGT_COL])
        return toonAttack[TOON_TRACK_COL]

    def __getActualTrackLevel(self, toonAttack):
        # NPC friends share the same attack columns, so we often need to
        # convert from an NPCSOS track to whatever track the NPC uses
        if (toonAttack[TOON_TRACK_COL] == NPCSOS):
            track, level, hp = NPCToons.getNPCTrackLevelHp(toonAttack[TOON_TGT_COL])
            if (track != None):
                return track, level
            else:
                self.notify.warning("No NPC with id: %d" % toonAttack[TOON_TGT_COL])
        return toonAttack[TOON_TRACK_COL], toonAttack[TOON_LVL_COL]

    def __getActualTrackLevelHp(self, toonAttack):
        # NPC friends share the same attack columns, so we often need to
        # convert from an NPCSOS track to whatever track the NPC uses
        if (toonAttack[TOON_TRACK_COL] == NPCSOS):
            track, level, hp = NPCToons.getNPCTrackLevelHp(toonAttack[TOON_TGT_COL])
            if (track != None):
                return track, level, hp
            else:
                self.notify.warning("No NPC with id: %d" % toonAttack[TOON_TGT_COL])
        elif (toonAttack[TOON_TRACK_COL] == PETSOS):
            trick = toonAttack[TOON_LVL_COL]
            petProxyId = toonAttack[TOON_TGT_COL]
            trickId = toonAttack[TOON_LVL_COL]
            assert(trickId < len(PetTricks.TrickHeals))
            healRange = PetTricks.TrickHeals[trickId]
            hp = 0
            if simbase.air.doId2do.has_key(petProxyId):
                petProxy = simbase.air.doId2do[petProxyId]
                if trickId < len(petProxy.trickAptitudes):
                    aptitude = petProxy.trickAptitudes[trickId]
                    hp = int(lerp(healRange[0], healRange[1], aptitude)) 
            else: 
                self.notify.warning("pet proxy: %d not in doId2do!" % petProxyId)
            return toonAttack[TOON_TRACK_COL], toonAttack[TOON_LVL_COL], hp 
        return toonAttack[TOON_TRACK_COL], toonAttack[TOON_LVL_COL], 0

    def __calculatePetTrickSuccess(self, toonAttack):
        petProxyId = toonAttack[TOON_TGT_COL]
        if not simbase.air.doId2do.has_key(petProxyId):
            self.notify.warning("pet proxy %d not in doId2do!" % petProxyId)
            toonAttack[TOON_ACCBONUS_COL] = 1
            return (0, 0)
        petProxy = simbase.air.doId2do[petProxyId]
        trickId = toonAttack[TOON_LVL_COL]
        toonAttack[TOON_ACCBONUS_COL] = petProxy.attemptBattleTrick(trickId)
        if toonAttack[TOON_ACCBONUS_COL] == 1:
            return (0, 0)
        else:
            return (1, 100)

# history
#
# 21Mar01   jlbutler   created
# 26Mar01   jlbutler   added bonus calculations to suit and toon attacks
# 15Jun01   jlbutler   added 'getAvPropDamage' to calculate the proper damage
#                      for a given prop for a specific toon
# 25Jul01   jnschell   moved 'getAvPropDamage' to ToontownBattleGlobals.py
# 27Jul01   jlbutler   fixed a few bugs with trap and lure and combinations
#                      with other toon attacks
# 27Aug01   jlbutler   Added code to remember statistics about suit attacks
#                      during the course of the entire battle.  Also fixed
#                      a problem where suits would attack dead toons because
#                      they would look randomly for a target in
#                      self.battle.activeToons but this list is not updated
#                      immediately as far as toon deaths go, so instead suits
#                      create a temporary list of active toons that are still
#                      alive when the suit gets around to attacking.
