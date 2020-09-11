from toontown.toonbase.ToontownGlobals import *
from SuitBattleGlobals import *
from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from toontown.suit.SuitDNA import *
from BattleBase import *
from BattleSounds import *
import MovieCamera
from direct.directnotify import DirectNotifyGlobal
import MovieUtil
from direct.particles import ParticleEffect
import BattleParticles
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

notify = DirectNotifyGlobal.directNotify.newCategory('MovieSuitAttacks')

def __doDamage(toon, dmg, died):
    assert(notify.debug('__doDamage(toon: %s  damage: %d died: %d' % (toon.getName(), dmg, died)))

    if (dmg > 0 and toon.hp != None):
        toon.takeDamage(dmg)

def __showProp(prop, parent, pos, hpr=None, scale=None):
    prop.reparentTo(parent)
    prop.setPos(pos)
    if hpr:
        prop.setHpr(hpr)
    if scale:
        prop.setScale(scale)

def __animProp(prop, propName, propType='actor'):
    if 'actor' == propType:
        prop.play(propName)
    elif 'model' == propType:
        pass
    else:
        self.notify.error("No such propType as: %s" % propType)

def __suitFacePoint(suit, zOffset = 0):
    pnt = suit.getPos()
    pnt.setZ(pnt[2] + suit.shoulderHeight + 0.3 + zOffset)
    return Point3(pnt)

def __toonFacePoint(toon, zOffset = 0, parent=render):
    pnt = toon.getPos(parent)
    pnt.setZ(pnt[2] + toon.shoulderHeight + 0.3 + zOffset)
    return Point3(pnt)

def __toonTorsoPoint(toon, zOffset = 0):
    pnt = toon.getPos()
    pnt.setZ(pnt[2] + toon.shoulderHeight - 0.2)
    return Point3(pnt)

def __toonGroundPoint(attack, toon, zOffset = 0, parent=render):
    pnt = toon.getPos(parent)
    battle = attack['battle']
    pnt.setZ(battle.getZ(parent) + zOffset)
    return Point3(pnt)

def __toonGroundMissPoint(attack, prop, toon, zOffset = 0):
    # The ground miss point is 5 feet beyond the toon, on the ground
    point = __toonMissPoint(prop, toon)
    battle = attack['battle']
    point.setZ(battle.getZ() + zOffset)
    return Point3(point)

def __toonMissPoint(prop, toon, yOffset = 0, parent=None):
    # The miss point is 5 feet beyond the toon.
    if parent:
        p = __toonFacePoint(toon) - prop.getPos(parent)
    else:
        p = __toonFacePoint(toon) - prop.getPos()

    v = Vec3(p)
    baseDistance = v.length()
    v.normalize()

    if parent:
        endPos = prop.getPos(parent) + (v * (baseDistance + 5 + yOffset))
    else:
        endPos = prop.getPos() + (v * (baseDistance + 5 + yOffset))
    return Point3(endPos)

def __toonMissBehindPoint(toon, parent=render, offset=0):
    point = toon.getPos(parent)
    point.setY(point.getY() - 5 + offset)
    return point

def __throwBounceHitPoint(prop, toon):
    startPoint = prop.getPos()
    endPoint = __toonFacePoint(toon)
    return __throwBouncePoint(startPoint, endPoint)

def __throwBounceMissPoint(prop, toon):
    startPoint = prop.getPos()
    endPoint = __toonFacePoint(toon)
    return __throwBouncePoint(startPoint, endPoint)

def __throwBouncePoint(startPoint, endPoint):
    midPoint = startPoint + ((endPoint - startPoint) / 2.0)
    # The bounce point is on the ground
    midPoint.setZ(0)
    return Point3(midPoint)


def doSuitAttack(attack):
    """ doSuitAttack(attack)
    """
    notify.debug('building suit attack in doSuitAttack: %s' % attack['name'])
    name = attack['id']
    if (name == AUDIT):
        suitTrack = doAudit(attack)
    elif (name == BITE):
        suitTrack = doBite(attack)
    elif (name == BOUNCE_CHECK):
        suitTrack = doBounceCheck(attack)
    elif (name == BRAIN_STORM):
        suitTrack = doBrainStorm(attack)
    elif (name == BUZZ_WORD):
        suitTrack = doBuzzWord(attack)
    elif (name == CALCULATE):
        suitTrack = doCalculate(attack)
    elif (name == CANNED):
        suitTrack = doCanned(attack)
    elif (name == CHOMP):
        suitTrack = doChomp(attack)
    elif (name == CIGAR_SMOKE):
        suitTrack = doDefault(attack)
#        suitTrack = doCigarSmoke(attack)
    elif (name == CLIPON_TIE):
        suitTrack = doClipOnTie(attack)
    elif (name == CRUNCH):
        suitTrack = doCrunch(attack)
    elif (name == DEMOTION):
        suitTrack = doDemotion(attack)
    elif (name == DOUBLE_TALK):
        suitTrack = doDoubleTalk(attack)
    elif (name == DOWNSIZE):
        suitTrack = doDownsize(attack)
    elif (name == EVICTION_NOTICE):
        suitTrack = doEvictionNotice(attack)
    elif (name == EVIL_EYE):
        suitTrack = doEvilEye(attack)
    elif (name == FILIBUSTER):
        suitTrack = doFilibuster(attack)
    elif (name == FILL_WITH_LEAD):
        suitTrack = doFillWithLead(attack)
    elif (name == FINGER_WAG):
        suitTrack = doFingerWag(attack)
    elif (name == FIRED):
        suitTrack = doFired(attack)
    elif (name == FIVE_O_CLOCK_SHADOW):
        suitTrack = doDefault(attack)
#        suitTrack = doFiveOClockShadow(attack)
    elif (name == FLOOD_THE_MARKET):
        suitTrack = doDefault(attack)
#        suitTrack = doFloodTheMarket(attack)
    elif (name == FOUNTAIN_PEN):
        suitTrack = doFountainPen(attack)
    elif (name == FREEZE_ASSETS):
        suitTrack = doFreezeAssets(attack)
    elif (name == GAVEL):
        suitTrack = doDefault(attack)
#        suitTrack = doGavel(attack)
    elif (name == GLOWER_POWER):
        suitTrack = doGlowerPower(attack)
    elif (name == GUILT_TRIP):
        suitTrack = doGuiltTrip(attack)
    elif (name == HALF_WINDSOR):
        suitTrack = doHalfWindsor(attack)
    elif (name == HANG_UP):
        suitTrack = doHangUp(attack)
    elif (name == HEAD_SHRINK):
        suitTrack = doHeadShrink(attack)
    elif (name == HOT_AIR):
        suitTrack = doHotAir(attack)
    elif (name == JARGON):
        suitTrack = doJargon(attack)
    elif (name == LEGALESE):
        suitTrack = doLegalese(attack)
    elif (name == LIQUIDATE):
         suitTrack = doLiquidate(attack)
    elif (name == MARKET_CRASH):
         suitTrack = doMarketCrash(attack)
    elif (name == MUMBO_JUMBO):
        suitTrack = doMumboJumbo(attack)
    elif (name == PARADIGM_SHIFT):
        suitTrack = doParadigmShift(attack)
    elif (name == PECKING_ORDER):
        suitTrack = doPeckingOrder(attack)
    elif (name == PICK_POCKET):
        suitTrack = doPickPocket(attack)
    elif (name == PINK_SLIP):
        suitTrack = doPinkSlip(attack)
    elif (name == PLAY_HARDBALL):
        suitTrack = doPlayHardball(attack)
    elif (name == POUND_KEY):
        suitTrack = doPoundKey(attack)
    elif (name == POWER_TIE):
        suitTrack = doPowerTie(attack)
    elif (name == POWER_TRIP):
        suitTrack = doPowerTrip(attack)
    elif (name == QUAKE):
        suitTrack = doQuake(attack)
    elif (name == RAZZLE_DAZZLE):
        suitTrack = doRazzleDazzle(attack)
    elif (name == RED_TAPE):
        suitTrack = doRedTape(attack)
    elif (name == RE_ORG):
        suitTrack = doReOrg(attack)
    elif (name == RESTRAINING_ORDER):
        suitTrack = doRestrainingOrder(attack)
    elif (name == ROLODEX):
        suitTrack = doRolodex(attack)
    elif (name == RUBBER_STAMP):
        suitTrack = doRubberStamp(attack)
    elif (name == RUB_OUT):
        suitTrack = doRubOut(attack)
    elif (name == SACKED):
        suitTrack = doSacked(attack)
    elif (name == SANDTRAP):
        suitTrack = doDefault(attack)
#        suitTrack = doSandtrap(attack)
    elif (name == SCHMOOZE):
        suitTrack = doSchmooze(attack)
    elif (name == SHAKE):
        suitTrack = doShake(attack)
    elif (name == SHRED):
        suitTrack = doShred(attack)
    elif (name == SONG_AND_DANCE):
        suitTrack = doDefault(attack)
#        suitTrack = doSongAndDance(attack)
    elif (name == SPIN):
        suitTrack = doSpin(attack)
    elif (name == SYNERGY):
        suitTrack = doSynergy(attack)
    elif (name == TABULATE):
        suitTrack = doTabulate(attack)
    elif (name == TEE_OFF):
        suitTrack = doTeeOff(attack)
    elif (name == THROW_BOOK):
        suitTrack = doDefault(attack)
#        suitTrack = doThrowBook(attack)
    elif (name == TREMOR):
        suitTrack = doTremor(attack)
    elif (name == WATERCOOLER):
        suitTrack = doWatercooler(attack)
    elif (name == WITHDRAWAL):
        suitTrack = doWithdrawal(attack)
    elif (name == WRITE_OFF):
        suitTrack = doWriteOff(attack)
    else:
        notify.warning('unknown attack: %d substituting Finger Wag' % name)
        suitTrack = doDefault(attack)

    assert(suitTrack != None)
    camTrack = MovieCamera.chooseSuitShot(attack, suitTrack.getDuration())

    # The toons should face the center of the battle after each attack
    battle = attack['battle']
    target = attack['target']
    groupStatus = attack['group']
    if groupStatus == ATK_TGT_SINGLE:
        toon = target['toon']
        toonHprTrack = Sequence(
            Func(toon.headsUp, battle, MovieUtil.PNT3_ZERO),
            Func(toon.loop, 'neutral'),
            )
    else:
        toonHprTrack = Parallel()
        for t in target:
            toon = t['toon']
            toonHprTrack.append(Sequence(
                Func(toon.headsUp, battle, MovieUtil.PNT3_ZERO),
                Func(toon.loop, 'neutral'),
                ))

    suit = attack['suit']
    neutralIval = Func(suit.loop, 'neutral')
    suitTrack = Sequence(suitTrack, neutralIval, toonHprTrack)

    # !!! If the suit is currently in a lured position (slightly forward), then we must
    # first reset the position before performing the attack
    suitPos = suit.getPos(battle)
    resetPos, resetHpr = battle.getActorPosHpr(suit)

    if (battle.isSuitLured(suit)): # If suit is lured, reset its pos
        resetTrack = getResetTrack(suit, battle)
        resetSuitTrack = Sequence(resetTrack, suitTrack)
        # Must incorporate a wait in the camTrack to account for the resetting time
        # and also explicitly unlure the suit
        waitTrack = Sequence(
            Wait(resetTrack.getDuration()),
            Func(battle.unlureSuit, suit),
            )
        resetCamTrack = Sequence(waitTrack, camTrack)
        return (resetSuitTrack, resetCamTrack)
    else:
        return (suitTrack, camTrack)

def getResetTrack(suit, battle):
    resetPos, resetHpr = battle.getActorPosHpr(suit)
    moveDist = Vec3(suit.getPos(battle) - resetPos).length()
    moveDuration = 0.5
#    moveDuration = (moveDist / BattleBase.suitSpeed) # Too short a time interval to see
    walkTrack = Sequence(
        # First face the right direction, then walk backwards
        Func(suit.setHpr, battle, resetHpr),
        ActorInterval(suit, 'walk', startTime=1, duration=moveDuration,
                      endTime=0.00001),
        Func(suit.loop, 'neutral')
        )
    # Actually move the suit
    moveTrack = LerpPosInterval(suit, moveDuration, resetPos, other=battle)
    return Parallel(walkTrack, moveTrack)

def __makeCancelledNodePath():
    # Make the text node
    tn = TextNode("CANCELLED")
    tn.setFont(getSuitFont())
    tn.setText(TTLocalizer.MovieSuitCancelled)
    tn.setAlign(TextNode.ACenter)

    # Make the top node path
    tntop = hidden.attachNewNode("CancelledTop")
    # Make a node path for the text node
    tnpath = tntop.attachNewNode(tn)
    tnpath.setPosHpr(0, 0, 0, 0, 0, 0)
    tnpath.setScale(1)
    tnpath.setColor(0.7, 0, 0, 1)
    # Make a backside node path for the text node
    tnpathback = tnpath.instanceUnderNode(tntop, "backside")
    tnpathback.setPosHpr(0, 0, 0, 180, 0, 0)
    tnpath.setScale(1)
    return tntop

def doDefault(attack):
    """ doDefault(attack)
    """
    notify.debug('building suit attack in doDefault')

    suitName = attack['suitName']
    if (suitName == 'f'):
        attack['id'] = POUND_KEY
        attack['name'] = 'PoundKey'
        attack['animName'] = 'phone'
        return doPoundKey(attack)
    elif (suitName == 'p'):
        attack['id'] = FOUNTAIN_PEN
        attack['name'] = 'FountainPen'
        attack['animName'] = 'pen-squirt'
        return doFountainPen(attack)
    elif (suitName == 'ym'):
        attack['id'] = RUBBER_STAMP
        attack['name'] = 'RubberStamp'
        attack['animName'] = 'rubber-stamp'
        return doRubberStamp(attack)
    elif (suitName == 'mm'):
        attack['id'] = FINGER_WAG
        attack['name'] = 'FingerWag'
        attack['animName'] = 'finger-wag'
        return doFingerWag(attack)
    elif (suitName == 'ds'):
        attack['id'] = DEMOTION
        attack['name'] = 'Demotion'
        attack['animName'] = 'magic1'
        return doDemotion(attack)
    elif (suitName == 'hh'):
        attack['id'] = GLOWER_POWER
        attack['name'] = 'GlowerPower'
        attack['animName'] = 'glower'
        return doGlowerPower(attack)
    elif (suitName == 'cr'):
        attack['id'] = PICK_POCKET
        attack['name'] = 'PickPocket'
        attack['animName'] = 'pickpocket'
        return doPickPocket(attack)
    elif (suitName == 'tbc'):
        attack['id'] = GLOWER_POWER
        attack['name'] = 'GlowerPower'
        attack['animName'] = 'glower'
        return doGlowerPower(attack)
    elif (suitName == 'cc'):
        attack['id'] = POUND_KEY
        attack['name'] = 'PoundKey'
        attack['animName'] = 'phone'
        return doPoundKey(attack)
    elif (suitName == 'tm'):
        attack['id'] = CLIPON_TIE
        attack['name'] = 'ClipOnTie'
        attack['animName'] = 'throw-paper'
        return doClipOnTie(attack)
    elif (suitName == 'nd'):
        attack['id'] = PICK_POCKET
        attack['name'] = 'PickPocket'
        attack['animName'] = 'pickpocket'
        return doPickPocket(attack)
    elif (suitName == 'gh'):
        attack['id'] = FOUNTAIN_PEN
        attack['name'] = 'FountainPen'
        attack['animName'] = 'pen-squirt'
        return doFountainPen(attack)
    elif (suitName == 'ms'):
        attack['id'] = BRAIN_STORM
        attack['name'] = 'BrainStorm'
        attack['animName'] = 'effort'
        return doBrainStorm(attack)
    elif (suitName == 'tf'):
        attack['id'] = RED_TAPE
        attack['name'] = 'RedTape'
        attack['animName'] = 'throw-object'
        return doRedTape(attack)
    elif (suitName == 'm'):
        attack['id'] = BUZZ_WORD
        attack['name'] = 'BuzzWord'
        attack['animName'] = 'speak'
        return doBuzzWord(attack)
    elif (suitName == 'mh'):
        attack['id'] = RAZZLE_DAZZLE
        attack['name'] = 'RazzleDazzle'
        attack['animName'] = 'smile'
        return doRazzleDazzle(attack)
    elif (suitName == 'sc'):
        attack['id'] = WATERCOOLER
        attack['name'] = 'Watercooler'
        attack['animName'] = 'water-cooler'
        return doWatercooler(attack)
    elif (suitName == 'pp'):
        attack['id'] = BOUNCE_CHECK
        attack['name'] = 'BounceCheck'
        attack['animName'] = 'throw-paper'
        return doBounceCheck(attack)
    elif (suitName == 'tw'):
        attack['id'] = GLOWER_POWER
        attack['name'] = 'GlowerPower'
        attack['animName'] = 'glower'
        return doGlowerPower(attack)
    elif (suitName == 'bc'):
        attack['id'] = AUDIT
        attack['name'] = 'Audit'
        attack['animName'] = 'phone'
        return doAudit(attack)
    elif (suitName == 'nc'):
        attack['id'] = RED_TAPE
        attack['name'] = 'RedTape'
        attack['animName'] = 'throw-object'
        return doRedTape(attack)
    elif (suitName == 'mb'):
        attack['id'] = LIQUIDATE
        attack['name'] = 'Liquidate'
        attack['animName'] = 'magic1'
        return doLiquidate(attack)
    elif (suitName == 'ls'):
        attack['id'] = WRITE_OFF
        attack['name'] = 'WriteOff'
        attack['animName'] = 'hold-pencil'
        return doWriteOff(attack)
    elif (suitName == 'rb'):
        attack['id'] = TEE_OFF
        attack['name'] = 'TeeOff'
        attack['animName'] = 'golf-club-swing'
        return doTeeOff(attack)
    elif (suitName == 'bf'):
        attack['id'] = RUBBER_STAMP
        attack['name'] = 'RubberStamp'
        attack['animName'] = 'rubber-stamp'
        return doRubberStamp(attack)
    elif (suitName == 'b'):
        attack['id'] = EVICTION_NOTICE
        attack['name'] = 'EvictionNotice'
        attack['animName'] = 'throw-paper'
        return doEvictionNotice(attack)
    elif (suitName == 'dt'):
        attack['id'] = RUBBER_STAMP
        attack['name'] = 'RubberStamp'
        attack['animName'] = 'rubber-stamp'
        return doRubberStamp(attack)
    elif (suitName == 'ac'):
        attack['id'] = RED_TAPE
        attack['name'] = 'RedTape'
        attack['animName'] = 'throw-object'
        return doRedTape(attack)
    elif (suitName == 'bs'):
        attack['id'] = FINGER_WAG
        attack['name'] = 'FingerWag'
        attack['animName'] = 'finger-wag'
        return doFingerWag(attack)
    elif (suitName == 'sd'):
        attack['id'] = WRITE_OFF
        attack['name'] = 'WriteOff'
        attack['animName'] = 'hold-pencil'
        return doWriteOff(attack)
    elif (suitName == 'le'):
        attack['id'] = JARGON
        attack['name'] = 'Jargon'
        attack['animName'] = 'speak'
        return doJargon(attack)
    elif (suitName == 'bw'):
        attack['id'] = FINGER_WAG
        attack['name'] = 'FingerWag'
        attack['animName'] = 'finger-wag'
        return doFingerWag(attack)
    else:
        self.notify.error('doDefault() - unsupported suit type: %s' % \
                suitName)
    return None

#######
# Begin encapsulating sub functions for suit attack functions
#######

def getSuitTrack(attack, delay=0.000001, splicedAnims=None):
    """ This function returns the standard suit Track of face up, animate, face up."""
    suit = attack['suit']
    battle = attack['battle']
    tauntIndex = attack['taunt']
    target = attack['target']
    toon = target['toon']
    targetPos = toon.getPos(battle)
    taunt = getAttackTaunt(attack['name'], tauntIndex)
    trapStorage = {}
    trapStorage['trap'] = None

    track = Sequence(# Start building the intervals for the suit track
        Wait(delay), # Optionally wait to start animation
        Func(suit.setChatAbsolute, taunt, CFSpeech | CFTimeout), # Use taunt text
        )

    # If suit has a trap prop, be sure to reparent it to the battle and not the
    # suit so it doesn't turn with him when he attacks
    def reparentTrap(suit=suit, battle=battle, trapStorage=trapStorage):
        trapProp = suit.battleTrapProp
        if (trapProp != None):
            trapProp.wrtReparentTo(battle)
            trapStorage['trap'] = trapProp

    track.append(Func(reparentTrap))
    track.append(Func(suit.headsUp, battle, targetPos))

    # Some attacks used spliced animations instead of just the default animation
    if splicedAnims:
        track.append(getSplicedAnimsTrack(splicedAnims, actor=suit))
    else:
        track.append(ActorInterval(suit, attack['animName'])) # Attack animation

    origPos, origHpr = battle.getActorPosHpr(suit) # To restore original hpr
    track.append(Func(suit.setHpr, battle, origHpr))

    # Now return the trapProp to the suit
    def returnTrapToSuit(suit=suit, trapStorage=trapStorage):
        trapProp = trapStorage['trap']
        if (trapProp != None):
            if trapProp.getName() == 'traintrack':
                notify.debug('deliberately not parenting traintrack to suit')
            else:
                trapProp.wrtReparentTo(suit)
            suit.battleTrapProp = trapProp
    track.append(Func(returnTrapToSuit))

    track.append(Func(suit.clearChat))
    return track


def getSuitAnimTrack(attack, delay=0):
    """ This function returns just the attack animation track for a suit """
    suit = attack['suit']
    tauntIndex = attack['taunt']
    taunt = getAttackTaunt(attack['name'], tauntIndex)

    return Sequence(
        Wait(delay),
        # Note: we needn't try to reparent a suit's trap to the battle with this
        # function (as seen in getSuitTrack) since here we never face the target
        # toon (used for group attacks where the suit addresses everyone
        Func(suit.setChatAbsolute, taunt, CFSpeech | CFTimeout),
        ActorInterval(attack['suit'], attack['animName']),
        Func(suit.clearChat),
        )


def getPartTrack(particleEffect, startDelay, durationDelay, partExtraArgs):
    """ This function returns the default particle track for a suit attack
    animation. Arguments:
        startDelay = time delay before particle effect begins
        durationDelay = time delay before particles are cleaned up
        partExtraArgs = extraArgs for startParticleEffect function, the first
        element of which is always the particle effect (function relies on this)
    """
    particleEffect = partExtraArgs[0]
    parent = partExtraArgs[1]
    if (len(partExtraArgs) > 2):
        worldRelative = partExtraArgs[2]
    else:
        worldRelative=1
    return Sequence (
        Wait(startDelay),
        ParticleInterval(particleEffect, parent, worldRelative,
                         duration=durationDelay, cleanup = True),
        )


def getToonTrack(attack, damageDelay=0.000001, damageAnimNames=None, dodgeDelay=0.0001,
                 dodgeAnimNames=None, splicedDamageAnims=None, splicedDodgeAnims=None,
                 target=None, showDamageExtraTime=0.01, showMissedExtraTime=0.5):
    """ This function returns the default Track for a toon portraying whether it is
    hit or missed. Arguments:
        attack = suit attack against the toon(s)
        damageDelay = time delay before damage animation occurs
        damageAnimNames = names of damage animations to perform in order
        dodgeDelay = time delay before dodge animation occurs
        dodgeAnimNames = names of dodge animations to perform in order
        splicedDamageAnims = can use spliced actor intervals from getSplicedAnimsTrack
        splicedDodgeAnims = can use spliced actor intervals from getSplieedAnims
        target = can specify a target for the toon track
        showMissedExtraTime = can add extra time onto the dodge delay to wait before
            showing a missed indicator if applicable
        Note: This function uses damageAnimNames and dodgeAnimNames if they exist.  So do
        not provide these arguments if you want to use splicedDamageAnims and
        splicedDodgeAnims.  Must have one or the other of these two lists.
    """
    if not target: # if a target is not provided, use default target in attack
        target = attack['target']
    toon = target['toon']
    battle = attack['battle']
    suit = attack['suit']
    suitPos = suit.getPos(battle)
    dmg = target['hp']

    animTrack = Sequence()
    animTrack.append(Func(toon.headsUp, battle, suitPos))

    if (dmg > 0): # aka (dmg > 0), or if hitToon
        animTrack.append(getToonTakeDamageTrack(toon, target['died'], dmg, damageDelay,
                                                 damageAnimNames, splicedDamageAnims, showDamageExtraTime))
        return animTrack
    else:
        animTrack.append(getToonDodgeTrack(target, dodgeDelay, dodgeAnimNames,
                                            splicedDodgeAnims, showMissedExtraTime))
        indicatorTrack = Sequence(
            Wait(dodgeDelay + showMissedExtraTime),
            Func(MovieUtil.indicateMissed, toon),
            )
        return Parallel(animTrack, indicatorTrack)

def getToonTracks(attack, damageDelay=0.000001, damageAnimNames=None, dodgeDelay=0.000001,
                  dodgeAnimNames=None, splicedDamageAnims=None, splicedDodgeAnims=None,
                  showDamageExtraTime=0.01, showMissedExtraTime=0.5):
    """ This function returns the default Tracks for a group of toons portraying if
    hit or missed. Arguments identical to getToonTrack(), except that this function
    intentionally uses the optional 'target' keyword argument to cycle through multiple
    targets for a group attack.  Note: The target variable in the attack dictionary
    will (and should) be a list if using a group attack.  Therefore this function
    should never be used for single attacks (use getToonTrack)."""
    toonTracks = Parallel()
    targets = attack['target']
    for i in range(len(targets)):
        tgt = targets[i]
        # slevel = a['suit'].getActualLevel()
        # print "ZZZZ processing attack ", i,"  damage=", tgt['hp'],"   toondied=", tgt['died']," suitlevel=", slevel
        toonTracks.append(getToonTrack(attack, damageDelay, damageAnimNames,
                   dodgeDelay, dodgeAnimNames, splicedDamageAnims, splicedDodgeAnims,
                   target=tgt, showDamageExtraTime=showDamageExtraTime,
                   showMissedExtraTime=showMissedExtraTime))
    return toonTracks

def getToonDodgeTrack(target, dodgeDelay, dodgeAnimNames,
                      splicedDodgeAnims, showMissedExtraTime):
    """ This function returns a track for a toon dodging an attack """

    toon = target['toon']
    toonTrack = Sequence()
    toonTrack.append(Wait(dodgeDelay))
    if dodgeAnimNames: # If exists, use these animations
        for d in dodgeAnimNames: # Use each dodge animation in order
            # If the dodge is a sidestep, other toons may need to get out of the way
            if (d == 'sidestep'):
                toonTrack.append(getAllyToonsDodgeParallel(target))
            else:
                toonTrack.append(ActorInterval(toon, d))
    else:
        toonTrack.append(getSplicedAnimsTrack(splicedDodgeAnims, actor=toon))

    toonTrack.append(Func(toon.loop, 'neutral'))
    return toonTrack


def getAllyToonsDodgeParallel(target):
    """ This function creates a multitrack to portray both a target toon dodging and the
        ally toons of a target toon dodging out of the way if neccessary """
    toon = target['toon']
    leftToons = target['leftToons']
    rightToons = target['rightToons']

    # If there are toons on the left, we then decide which side to dodge towards based on
    # least resistance, the same formula used by the suits
    if len(leftToons) > len(rightToons):
        # Path of Least/Most Resistance
        PoLR = rightToons
        PoMR = leftToons
    else:
        PoLR = leftToons
        PoMR = rightToons

    # most of the time, choose the side with the least avatars
    # base the random choice on the difference between the
    # number of avatars on the left versus the right
    upper = 1 + (4 * abs(len(leftToons) - len(rightToons)))
    if (random.randint(0, upper) > 0):
        toonDodgeList = PoLR
    else:
        toonDodgeList = PoMR
    if toonDodgeList is leftToons:
        sidestepAnim = 'sidestep-left'
        soundEffect = globalBattleSoundCache.getSound('AV_side_step.mp3')
    else:
        sidestepAnim = 'sidestep-right'
        soundEffect = globalBattleSoundCache.getSound('AV_jump_to_side.mp3')

    # Make the other toons dodge
    toonTracks = Parallel()
    for t in toonDodgeList:
            toonTracks.append(Sequence(ActorInterval(t, sidestepAnim),
                                       Func(t.loop, 'neutral'),
                                       ))
    # finally, make the target toon dodge
    toonTracks.append(Sequence(ActorInterval(toon, sidestepAnim),
                               Func(toon.loop, 'neutral'),
                               ))

    # Include a sound track in with the toon tracks
    toonTracks.append(Sequence(Wait(0.5),
                               SoundInterval(soundEffect, node=toon),
                               ))

    return toonTracks


def getPropTrack(prop, parent, posPoints, appearDelay, remainDelay,
                 scaleUpPoint=Point3(1), scaleUpTime=0.5, scaleDownTime=0.5,
                 startScale=Point3(0.01), anim=0, propName='none',
                 animDuration=0.0, animStartTime=0.0):
    """ This function returns a Track portraying the appearance of a prop,
    a delay time for the suit to act with the prop and the disappearancen
    of the prop.  Arguments:
         propName = the prop object itself
         parent = the parent for the prop to be a child of
         posPoints = pos, hpr, scale arguments to __showProp, only requires pos
         appearDelay = the time to delay before causing the prop to appear
         remainDelay = the time to leave the object visible before scaling away
         scaleUpPoint = the point to scale up to
         scaleUpTime = the duration of time to scale up the prop
         scaleDownTime = the duration of time to scale down the prop
         startScale = beginning scale of prop (set to non zero to avoid
            wiping out the HPR)
         anim = whether the prop has an animation to play
         propName = name of the prop (required if calling an animation
         animDuration = the duration for the animation
         animStartTime = the start time for the animation
    """

    if (anim == 1):
        track = Sequence(
            Wait(appearDelay), # Wait the duration of appearDelay
            Func(__showProp, prop, parent, *posPoints),
            LerpScaleInterval(prop, scaleUpTime, scaleUpPoint,
                              startScale=startScale),
            ActorInterval(prop, propName, duration=animDuration,
                          startTime=animStartTime),
            Wait(remainDelay),
            Func(MovieUtil.removeProp, prop)
            )
    else:
        track = Sequence(
            Wait(appearDelay), # Wait the duration of appearDelay
            Func(__showProp, prop, parent, *posPoints),
            LerpScaleInterval(prop, scaleUpTime, scaleUpPoint, startScale=startScale),
            Wait(remainDelay), # Wait while suit animation continues
            LerpScaleInterval(prop, scaleDownTime, MovieUtil.PNT3_NEARZERO), # Scale down the prop
            Func(MovieUtil.removeProp, prop)
            )

    return track

def getPropAppearTrack(prop, parent, posPoints, appearDelay,
                       scaleUpPoint=Point3(1), scaleUpTime=0.5,
                       startScale=Point3(0.01), poseExtraArgs=None):
    """ This function returns the track portraying a prop appearing. Arguments:
         propName = name of the prop object
         parent = the parent for the prop to be a child of
         posPoints = pos, hpr, scale arguments to __showProp, only pos required
         appearDelay = the time to delay before causing the prop to appear
         scaleUpPoint = the point to scale up to
         scaleUpTime = the duration of time to scale up the prop (normally 0.5)
         startScale = beginning scale of prop (set to non zero to avoid
            wiping out the HPR)
    """

    propTrack = Sequence(
        Wait(appearDelay), # Wait the duration of appearDelay
        Func(__showProp, prop, parent, *posPoints) # Use showProp
        )
    if poseExtraArgs: # Add pose for prop if provided
        propTrack.append(Func(prop.pose, *poseExtraArgs))
    propTrack.append(LerpScaleInterval(prop, scaleUpTime, scaleUpPoint,
                                        startScale=startScale))
    return propTrack


def getPropThrowTrack(attack, prop, hitPoints=[], missPoints=[], hitDuration=0.5,
                      missDuration=0.5, hitPointNames='none', missPointNames='none',
                      lookAt='none', groundPointOffSet=0, missScaleDown=None, parent=render):
    """ This function returns the track portraying a prop flying at the target
    toon.  Arguments:
         attack = attack from the suits to the toons
         prop = prop to be flown at target toon
         hitPoints = points to traverse if toon is hit
         missPoints = points to traverse if toon is missed
         hitDuration = how long it takes for prop to fly and hit toon
         missDuration = how long it takes for prop to fly and miss toon
         hitPointNames = names of throw points to traverse if toon is hit
         missPointNames = names of miss points to traverse if toon is missed
         lookAt = cause the prop to lookAt a point if provided
    """
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    battle = attack['battle']

    def getLambdas(list, prop, toon):
        for i in range(len(list)): # Create lambda functions for throw points
            if (list[i] == 'face'):
                list[i] = lambda toon=toon: __toonFacePoint(toon)
            elif (list[i] == 'miss'):
                list[i] = lambda prop=prop, toon=toon: __toonMissPoint(prop, toon)
            elif (list[i] == 'bounceHit'):
                list[i] = lambda prop=prop, toon=toon:__throwBounceHitPoint(prop, toon)
            elif (list[i] == 'bounceMiss'):
                list[i] = lambda prop=prop, toon=toon:__throwBounceMissPoint(prop, toon)
        return list

    if (hitPointNames != 'none'):
        hitPoints = getLambdas(hitPointNames, prop, toon)
    if (missPointNames != 'none'):
        missPoints = getLambdas(missPointNames, prop, toon)

    propTrack = Sequence()
    propTrack.append(Func(battle.movie.needRestoreRenderProp, prop))
    propTrack.append(Func(prop.wrtReparentTo, parent))
    if (lookAt != 'none'):
        propTrack.append(Func(prop.lookAt, lookAt))

    if (dmg > 0): # Fly prop through the hitPoints
        for i in range(len(hitPoints)):
            pos = hitPoints[i]
            propTrack.append(LerpPosInterval(prop, hitDuration, pos=pos))
    else: # Fly prop through the missPoints
        for i in range(len(missPoints)):
            pos = missPoints[i]
            propTrack.append(LerpPosInterval(prop, missDuration, pos=pos))

        # if provide a scale down time for when the prop misses, scale it down
        if missScaleDown:
            propTrack.append(LerpScaleInterval(prop, missScaleDown, MovieUtil.PNT3_NEARZERO))

    propTrack.append(Func(MovieUtil.removeProp, prop))
    propTrack.append(Func(battle.movie.clearRenderProp, prop))

    return propTrack

def getThrowTrack(object, target, duration=1.0, parent=render, gravity=-32.144):


    values = {}
    def calcOriginAndVelocity(object=object, target=target, values=values,
                     duration=duration, parent=parent, gravity=gravity):

        if callable(target):
            target = target()

        object.wrtReparentTo(parent)
        values['origin'] = object.getPos(parent)
        origin = object.getPos(parent)
        # Calculate the initial velocity required for the object to land at the target
        values['velocity'] = ((target[2]-origin[2]) - (0.5*gravity*duration*duration)) \
                             / duration

    return Sequence(
        Func(calcOriginAndVelocity),
        LerpFunctionInterval(throwPos, fromData=0., toData=1., duration=duration,
                             extraArgs=[object, duration, target, values, gravity])
        )

def throwPos(t, object, duration, target, values, gravity=-32.144):
    origin = values['origin']
    velocity = values['velocity']

    if callable(target):
        target = target()

    x = origin[0]*(1-t) + target[0]*t
    y = origin[1]*(1-t) + target[1]*t
    time = t*duration
    z = origin[2] + velocity*time + (0.5*gravity*time*time)
    object.setPos(x, y, z)

def getToonTakeDamageTrack(toon, died, dmg, delay, damageAnimNames=None,
                               splicedDamageAnims=None, showDamageExtraTime=0.01):
    """ This function returns the intervals portraying a target toon taking damage.
    Arguments:
        toon = the toon taking damage
        died = whether the toon died or not
        dmg = how much damage the toon is taking
        delay = time delay before damage animation occurs
        damageAnimNames = damage animations to be performed in order
        splicedDamageAnims = spliced animations from getSplicedAnimsTrack
        Note: This function uses damageAnimNames if it is not null. Provide only
        splicedDamageAnims to have them played.  Must have atleast one or the other.
    """
    toonTrack = Sequence()
    toonTrack.append(Wait(delay))

    assert(notify.debug('getToonTakeDamageTrack(toon: %s damage: %d died: %d' % (toon.getName(), dmg, died)))

    if damageAnimNames: # If exists, use these animations
        for d in damageAnimNames: # Use each damage animation in order
            toonTrack.append(ActorInterval(toon, d)) # Add animation
        indicatorTrack = Sequence(
            Wait(delay + showDamageExtraTime),
            Func(__doDamage, toon, dmg, died),
            )
    else:
        splicedAnims = getSplicedAnimsTrack(splicedDamageAnims, actor=toon)
        toonTrack.append(splicedAnims)

        indicatorTrack = Sequence(
            Wait(delay + showDamageExtraTime),
            Func(__doDamage, toon, dmg, died),
            )

    toonTrack.append(Func(toon.loop, 'neutral'))
    if died:
        # If the battle calculator thinks the toon should have died,
        # then wait a few seconds here to give the toon's client a
        # chance to discover that he's died, and start to broadcast
        # the death animation.

        # The death animation used to be built into the track, but
        # nowadays we just wait quietly, since there's a chance the
        # toon might not have died after all (someone may have used a
        # toon-up ResistanceChat message during the round).
        toonTrack.append(Wait(5.0))

    return Parallel(toonTrack, indicatorTrack)


def getSplicedAnimsTrack(anims, actor=None):
    """ This function returns a Sequence spliced together from the animations
    provided as arguments.  Arguments:
        actor = can optional provide an actor to applay all animations to
        anims = a list of lists.  Each list contains an animation with optional arguments.
        Each argument holds a position in the list and only the first (the animation name)
        is required.  The arguments are:
        [0] = animation name
        [1] = delay time before the animation is played (default=0 if not given)
        [2] = start time within the animation (default=0 if not given)
        [3] = duration of the animation to play (default=animation's duration if not given)
        [4] = an actor for the animation (which would overrule the actor keyword argument)
        The animations will be executed in the order of the anims list.
        Note: Keyword argument actor must be provided unless each animation list includes it.
        You can also provide a standard actor and occassionally override it with a specified
        actor as that fifth argument in the animation list.
    """
    track = Sequence()
    for nextAnim in anims:
        delay = 0.000001 # Ensure that Wait is not called with a value of zero
        if (len(nextAnim) >= 2): # If using a delay before the animation
            if (nextAnim[1] > 0): # Make sure that the given delay is not zero
                delay = nextAnim[1] # And if not, go ahead and use provided value

        if (len(nextAnim) <= 0): # Shouldn't happen, but make negligible wait
            track.append(Wait(delay)) # Delay is 0.000001 here
        elif (len(nextAnim) == 1): # Call animation with default arguments
            track.append(ActorInterval(actor, nextAnim[0]))
        elif (len(nextAnim) == 2): # Calls animation with a delay
            track.append(Wait(delay))
            track.append(ActorInterval(actor, nextAnim[0]))
        elif (len(nextAnim) == 3): # Calls animation with a delay and a start time
            track.append(Wait(delay))
            track.append(ActorInterval(actor, nextAnim[0], startTime=nextAnim[2]))
        elif (len(nextAnim) == 4): # Calls animation with a delay, startTime, and duration
            track.append(Wait(delay))
            # Allow for reversed animations through negative durations
            duration = nextAnim[3]
            if (duration < 0):
                startTime = nextAnim[2]
                endTime = startTime+duration
                if (endTime <= 0): # Ensure endTime is not negative (no animation there)
                    endTime = 0.01
                track.append(ActorInterval(actor, nextAnim[0], startTime=startTime,
                                            endTime=endTime))
            else:
                track.append(ActorInterval(actor, nextAnim[0], startTime=nextAnim[2],
                                        duration=duration))
        elif (len(nextAnim) == 5): # Calls animation with all arguements
            track.append(Wait(delay))
            track.append(ActorInterval(nextAnim[4], nextAnim[0], startTime=nextAnim[2],
                                        duration=nextAnim[3]))
    return track


def getSplicedLerpAnims(animName, origDuration, newDuration, startTime=0, fps=30, reverse=0):
    """ This function returns a series of intervals splicing together an animation
    over a modified frame of time.  This allows an animation to be shortened or
    lengthened (if you can tolerate any resulting rushed or choppy animation. This
    function increases an animation time by inserting a uniform time interval before
    successive ActorInterval calls. It decreases time by progressing the animation
    time forward faster than real-time (basically uniformly skipping frames). This
    function only works in conjunction with getSplicedAnimsTrack, see that function (above)
    for how animation lists are constructed and manipulated.
    Arguments:
        animName = name of the animation to lengthen/shorten
        origDuration = original time duration the animation should normally play in
        newDuration = lengthened or shortened time for the new animation
        startTime = startTime for the animation
        fps = usually held constant, helps determine number of actor intervals to use
    """
    anims = []
    addition = 0 # Addition will be added to the startTime to move animation forward
    numAnims = origDuration * fps # Number of actor intervals to use
    # The timeInterval is what to add before each actor interval to delay time
    timeInterval = newDuration / numAnims
    # The animInterval is how much the animation progresses forward each interval
    animInterval = origDuration / numAnims
    # If we are reversing the animation, make the animInterval negative
    if (reverse == 1):
        animInterval = -animInterval
    for i in range(0, numAnims):
        # Constructing the animation list for later use with getSplicedAnimsTrack
        anims.append([animName, timeInterval, startTime+addition, animInterval])
        addition += animInterval # Add addition to push the animation forward
    return anims


def getSoundTrack(fileName, delay=0.01, duration=None, node=None):
    """ This functions returns the standard sound track, which involves one sound
    effect with a possible delay beforehand and an optional duration specification.
    """

    soundEffect = globalBattleSoundCache.getSound(fileName)

    if duration:
        return Sequence(Wait(delay),
                        SoundInterval(soundEffect, duration=duration, node=node))
    else:
        return Sequence(Wait(delay),
                        SoundInterval(soundEffect, node=node))


#######
# End encapsulating sub functions for suit attack functions
#######


############
# Begin Revamped attacks using sub functions defined above.
############

"""
def doCarbonCopy(attack): # top f: special = copy suit and double attack; depends; depends
    pass #later
"""

def doClipOnTie(attack): # top tm: fixed
    """ This function returns Tracks portraying the Clip-on-tie attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    tie = globalPropPool.getProp('clip-on-tie') # Get tie from pool

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): # type A not yet used
        throwDelay = 2.17
        damageDelay = 3.3
        dodgeDelay = 3.1
    elif (suitType == 'b'):
        throwDelay = 2.17
        damageDelay = 3.3
        dodgeDelay = 3.1
    elif (suitType == 'c'):
        throwDelay = 1.45
        damageDelay = 2.61
        dodgeDelay = 2.34

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(0.66, 0.51, 0.28), VBase3(-69.652, -17.199, 67.960)]
    # First make the tie appear
    tiePropTrack = Sequence(
        getPropAppearTrack(tie, suit.getRightHand(), posPoints, 0.5,
                           MovieUtil.PNT3_ONE, scaleUpTime=0.5, poseExtraArgs=['clip-on-tie', 0]))

    # If tie will hit toon, pose it in its extended position
    if (dmg > 0): # If damage is greater than zero
        # Now throw the tie, which travels much faster if thrown "well" (hits toon)
        tiePropTrack.append(ActorInterval(tie, 'clip-on-tie',
                             duration=throwDelay, startTime=1.1))
    else:
        tiePropTrack.append(Wait(throwDelay)) # Wait while suit animates

    tiePropTrack.append(Func(tie.setHpr, Point3(0, -90, 0)))
    tiePropTrack.append(getPropThrowTrack(attack, tie, [__toonFacePoint(toon)],
                                          [__toonGroundPoint(attack, toon, 0.1)], hitDuration=0.4,
                                          missDuration=0.8, missScaleDown=1.2))

    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])

    throwSound = getSoundTrack('SA_powertie_throw.mp3', delay=throwDelay+1, node=suit)
    
    return Parallel(suitTrack, toonTrack, tiePropTrack, throwSound)


def doPoundKey(attack): # top f: fixed
    """ This function returns Tracks portraying the PoundKey attack """
    suit = attack['suit']
    battle = attack['battle']
    phone = globalPropPool.getProp('phone')
    receiver = globalPropPool.getProp('receiver')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('PoundKey')
    BattleParticles.setEffectTexture(particleEffect, 'poundsign',
                                      color=Vec4(0, 0, 0, 1))

    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.1, 1.55, [particleEffect, suit, 0])
    phonePosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
    receiverPosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]

    propTrack = Sequence(# Single propTrack combines both phone and receiver
        Wait(0.3), # Wait to show the phone and receiver
        Func(__showProp, phone, suit.getLeftHand(),
                         phonePosPoints[0], phonePosPoints[1]), # Show phone
        Func(__showProp, receiver, suit.getLeftHand(),
                         receiverPosPoints[0], receiverPosPoints[1]), # Show receiver

        LerpScaleInterval(phone, 0.5, MovieUtil.PNT3_ONE, MovieUtil.PNT3_NEARZERO), # Scale up phone
        Wait(0.74), # Wait until suit picks up phone
        # Now reparent receiver to suit's right hand (he picks it up)
        Func(receiver.wrtReparentTo, suit.getRightHand()),
        # Jam receiver into position in case reparenting to right hand takes place early or late.
        #Note: These coordinates are specific to Type C suits
        LerpPosHprInterval(receiver, 0.0001, Point3(-0.45, 0.48, -0.62), VBase3(-87.47, -18.21, 7.82)),
        Wait(3.14), # Wait while suit uses the phone
        # Now put the receiver back down on the phone
        Func(receiver.wrtReparentTo, phone),
        Wait(0.62), # Leave the phone around a bit longer
        LerpScaleInterval(phone, 0.5, MovieUtil.PNT3_NEARZERO), # Scale down phone & child receiver
        # Now destroy the receiver and then the phone
        Func(MovieUtil.removeProps, [receiver, phone]),
        )

    toonTrack = getToonTrack(attack, 2.7, ['cringe'], 1.9, ['sidestep'])

    soundTrack = getSoundTrack('SA_hangup.mp3', delay=1.3, node=suit)

    return Parallel(suitTrack, toonTrack, propTrack, partTrack, soundTrack)


def doShred(attack): # top f: fixed
    """ This function returns Tracks portraying the Shred attack """
    suit = attack['suit']
    battle = attack['battle']
    paper = globalPropPool.getProp('shredder-paper')
    shredder = globalPropPool.getProp('shredder')
    particleEffect = BattleParticles.createParticleEffect('Shred')

    suitTrack = getSuitTrack(attack) # Get suit animation track
    partTrack = getPartTrack(particleEffect, 3.5, 1.9, [particleEffect, suit, 0])
    paperPosPoints = [Point3(0.59, -0.31, 0.81), VBase3(79.224, 32.576, -179.449)]
    paperPropTrack = getPropTrack(paper, suit.getRightHand(), paperPosPoints, 2.4, 0.00001,
                                  scaleUpTime=0.2, anim=1, propName='shredder-paper',
                                  animDuration=1.5, animStartTime=2.8)
    shredderPosPoints = [Point3(0, -0.12, -0.34), VBase3(-90.000, -53.770, -0.000)]
    shredderPropTrack = getPropTrack(shredder, suit.getLeftHand(), shredderPosPoints,
                        1, 3, scaleUpPoint=Point3(4.81, 4.81, 4.81))
    toonTrack = getToonTrack(attack, suitTrack.getDuration()-1.1, ['conked'],
                               suitTrack.getDuration()-3.1, ['sidestep'])
    soundTrack = getSoundTrack('SA_shred.mp3', delay=3.4, node=suit)

    return Parallel(suitTrack, paperPropTrack, shredderPropTrack, partTrack,
                    toonTrack, soundTrack)


def doFillWithLead(attack): # top p: particle w/ 2 props; cringe; sidestep
    """ This function returns Tracks portraying the FillWithLead attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    pencil = globalPropPool.getProp('pencil')
    sharpener = globalPropPool.getProp('sharpener')
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect(file='fillWithLeadSpray')
    headSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    torsoSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    legsSmotherEffect = BattleParticles.createParticleEffect(file='fillWithLeadSmother')
    BattleParticles.setEffectTexture(sprayEffect, 'roll-o-dex',
                                      color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(headSmotherEffect, 'roll-o-dex',
                                      color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(torsoSmotherEffect, 'roll-o-dex',
                                      color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(legsSmotherEffect, 'roll-o-dex',
                                      color=Vec4(0, 0, 0, 1))

    suitTrack = getSuitTrack(attack) # Get suit animation track
    sprayTrack = getPartTrack(sprayEffect, 2.5, 1.9, [sprayEffect, suit, 0])
    pencilPosPoints = [Point3(-0.29, -0.33, -0.13), VBase3(160.565, -11.653, -169.244)]
    pencilPropTrack = getPropTrack(pencil, suit.getRightHand(), pencilPosPoints,
                                   0.7, 3.2, scaleUpTime=0.2)
    sharpenerPosPoints = [Point3(0.0, 0.0, -0.03), MovieUtil.PNT3_ZERO]
    sharpenerPropTrack = getPropTrack(sharpener, suit.getLeftHand(), sharpenerPosPoints,
                        1.3, 2.3, scaleUpPoint=MovieUtil.PNT3_ONE)

    # This damage animation makes the toon remain stunned for much longer (while being
    # filled with lead) by repeating that portion of the conked animation
    damageAnims = []
    damageAnims.append(['conked', suitTrack.getDuration()-1.5, 0.00001, 1.4])
    damageAnims.append(['conked', 0.00001, 0.7, 0.7])
    damageAnims.append(['conked', 0.00001, 0.7, 0.7])
    damageAnims.append(['conked', 0.00001, 1.4])
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims,
                dodgeDelay=suitTrack.getDuration()-3.1, dodgeAnimNames=['sidestep'],
                showDamageExtraTime=4.5, showMissedExtraTime=1.6)

    # Now we'll use a particle effect on each color changing body part, so we must first
    # calculate the height of the body part to correctly place the particle effects
    animal = toon.style.getAnimal()
    bodyScale = ToontownGlobals.toonBodyScales[animal]
    headEffectHeight = __toonFacePoint(toon).getZ()
    legsHeight = ToontownGlobals.legHeightDict[toon.style.legs] * bodyScale
    torsoEffectHeight = ((ToontownGlobals.torsoHeightDict[toon.style.torso]*bodyScale)/2)+legsHeight
    legsEffectHeight = legsHeight / 2
    effectX = headSmotherEffect.getX() # This remains the same for each effect
    effectY = headSmotherEffect.getY() # Same for each effect, adjusted slightly for each
    headSmotherEffect.setPos(effectX, effectY - 1.5, headEffectHeight)
    torsoSmotherEffect.setPos(effectX, effectY - 1, torsoEffectHeight)
    legsSmotherEffect.setPos(effectX, effectY - 0.6, legsEffectHeight)
    partDelay = 3.5 # Delay for all particle effects
    partIvalDelay = 0.7 # Delay between each particle effect
    partDuration = 1.0 # Duration for particle effects
    headTrack = getPartTrack(headSmotherEffect, partDelay, partDuration,
                              [headSmotherEffect, toon, 0])
    torsoTrack = getPartTrack(torsoSmotherEffect, partDelay+partIvalDelay, partDuration,
                               [torsoSmotherEffect, toon, 0])
    legsTrack = getPartTrack(legsSmotherEffect, partDelay+partIvalDelay*2, partDuration,
                              [legsSmotherEffect, toon, 0])

    def colorParts(parts): # Function to color each lod part in list parts
        track = Parallel()
        for partNum in range(0, parts.getNumPaths()):
             nextPart = parts.getPath(partNum)
             track.append(Func(nextPart.setColorScale,
                                            Vec4(0, 0, 0, 1)))
        return track

    def resetParts(parts): # Fucntion to reset color on each lod part in list parts
        track = Parallel()
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
            track.append(Func(nextPart.clearColorScale))
        return track

    if (dmg > 0):
        colorTrack = Sequence() # Build intervals to change the toon's color to black
        headParts = toon.getHeadParts()
        torsoParts = toon.getTorsoParts()
        legsParts = toon.getLegsParts()

        # Now color each body part in succession, then show each
        colorTrack.append(Wait(partDelay+0.2))
        colorTrack.append(Func(battle.movie.needRestoreColor))
        colorTrack.append(colorParts(headParts))
        colorTrack.append(Wait(partIvalDelay)) # Wait before next part color change
        colorTrack.append(colorParts(torsoParts))
        colorTrack.append(Wait(partIvalDelay)) # Wait before next part color change
        colorTrack.append(colorParts(legsParts))
        colorTrack.append(Wait(2.5)) # Wait while color has been changed
        colorTrack.append(resetParts(headParts))
        colorTrack.append(resetParts(torsoParts))
        colorTrack.append(resetParts(legsParts))
        colorTrack.append(Func(battle.movie.clearRestoreColor))
        return Parallel(suitTrack, pencilPropTrack, sharpenerPropTrack,
                        sprayTrack, headTrack, torsoTrack, legsTrack,
                        colorTrack, toonTrack)
    else:
        return Parallel(suitTrack, pencilPropTrack, sharpenerPropTrack,
                        sprayTrack, toonTrack)


def doFountainPen(attack): # top p: fixed
    """ This function returns Tracks portraying the FountainPen attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    pen = globalPropPool.getProp('pen')

    def getPenTip(pen=pen):
        tip = pen.find("**/joint_toSpray")
        return tip.getPos(render)
    hitPoint = lambda toon=toon: __toonFacePoint(toon)
    missPoint = lambda prop=pen, toon=toon: __toonMissPoint(prop, toon, 0, parent=render)
    hitSprayTrack = MovieUtil.getSprayTrack(battle,
                              VBase4(0, 0, 0, 1), getPenTip, hitPoint,
                              0.2, 0.2, 0.2, horizScale = 0.1, vertScale = 0.1)
    missSprayTrack = MovieUtil.getSprayTrack(battle,
                                VBase4(0, 0, 0, 1), getPenTip, missPoint,
                                0.2, 0.2, 0.2, horizScale = 0.1, vertScale = 0.1)

    suitTrack = getSuitTrack(attack)
    propTrack = Sequence(# Build intervals for foutain pen, including its spray
        Wait(0.01), # Wait the duration of appearDelay
        Func(__showProp, pen, suit.getRightHand(), MovieUtil.PNT3_ZERO),
        LerpScaleInterval(pen, 0.5, Point3(1.5, 1.5, 1.5)),
        Wait(1.05), # Wait until time to spray
        # was 1.6
        )

    if (dmg > 0): # If squirt hits the toon, use the hit spray
        propTrack.append(hitSprayTrack) # Add in the spray intervals
    else: # Only use the hitSpray until learn how to extend spray distance
        propTrack.append(missSprayTrack) # Add in the spray intervals


    propTrack += [# Add the rest of the prop intervals
        LerpScaleInterval(pen, 0.5, MovieUtil.PNT3_NEARZERO), # Scale down the prop
        Func(MovieUtil.removeProp, pen)
        ]

    # Now build the splash track for if the toon takes damage
    splashTrack = Sequence()
    if (dmg > 0) : # If the target toon takes damage
        def prepSplash(splash, targetPoint):
            splash.reparentTo(render)
            splash.setPos(targetPoint)
            scale = splash.getScale()
            splash.setBillboardPointWorld()
            splash.setScale(scale)
        splash = globalPropPool.getProp('splash-from-splat')
        splash.setColor(0, 0, 0, 1)
        splash.setScale(0.15)
        splashTrack = Sequence(
            Func(battle.movie.needRestoreRenderProp,
                             splash),
            Wait(1.65),
            Func(prepSplash, splash,
                             __toonFacePoint(toon)),
            ActorInterval(splash, 'splash-from-splat'),
            Func(MovieUtil.removeProp,
                                splash),
            Func(battle.movie.clearRenderProp, splash)
            )

        # Grab the head parts to turn it to black when hit
        headParts = toon.getHeadParts()
        # Now change the toon's head color to black from the pen spray
        splashTrack.append(Func(battle.movie.needRestoreColor))
        for partNum in range(0, headParts.getNumPaths()):
             nextPart = headParts.getPath(partNum)
             splashTrack.append(Func(nextPart.setColorScale,
                                                  Vec4(0, 0, 0, 1)))
        splashTrack.append(Func(MovieUtil.removeProp, splash))
        splashTrack.append(Wait(2.6)) # Wait while toon has turned black
        # Now reset the color scale of the head parts
        for partNum in range(0, headParts.getNumPaths()):
            nextPart = headParts.getPath(partNum)
            splashTrack.append(Func(nextPart.clearColorScale))
        splashTrack.append(Func(battle.movie.clearRestoreColor))

    penSpill = BattleParticles.createParticleEffect(file='penSpill')
    penSpill.setPos(getPenTip())
    penSpillTrack = getPartTrack(penSpill, 1.4, 0.7, [penSpill, pen, 0])

    toonTrack = getToonTrack(attack, 1.81, ['conked'], dodgeDelay=0.11,
                             splicedDodgeAnims=[['duck', 0.01, 0.6]],
                             showMissedExtraTime=1.66)
    soundTrack = getSoundTrack('SA_fountain_pen.mp3', delay=1.6, node=suit)

    return Parallel(suitTrack, toonTrack, propTrack,
                    soundTrack, penSpillTrack, splashTrack)


def doRubOut(attack): # top p: fixed
    """ This function returns Tracks portraying the RubOut attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    pad = globalPropPool.getProp('pad')
    pencil = globalPropPool.getProp('pencil')
    headEffect = BattleParticles.createParticleEffect('RubOut',
                                                      color=toon.style.getHeadColor())
    torsoEffect = BattleParticles.createParticleEffect('RubOut',
                                                       color=toon.style.getArmColor())
    legsEffect = BattleParticles.createParticleEffect('RubOut',
                                                      color=toon.style.getLegColor())

    suitTrack = getSuitTrack(attack)
    padPosPoints = [Point3(-0.66, 0.81, -0.06), VBase3(14.930, -2.290, 180.000)]
    padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 0.5, 2.57)
    pencilPosPoints = [Point3(0.04, -0.38, -0.10), VBase3(-170.223, -3.762, -62.929)]
    pencilPropTrack = getPropTrack(pencil, suit.getRightHand(), pencilPosPoints, 0.5, 2.57)
    toonTrack = getToonTrack(attack, 2.2, ['conked'], 2.0, ['jump'])

    hideTrack = Sequence() # Build intervals to hide the target toon's body parts
    headParts = toon.getHeadParts()
    torsoParts = toon.getTorsoParts()
    legsParts = toon.getLegsParts()

    # Now we'll use a particle effect on each disappearing body part, so we must first
    # calculate the height of the body part to correctly place the particle effect
    animal = toon.style.getAnimal()
    bodyScale = ToontownGlobals.toonBodyScales[animal]
    headEffectHeight = __toonFacePoint(toon).getZ()
    legsHeight = ToontownGlobals.legHeightDict[toon.style.legs] * bodyScale
    torsoEffectHeight = ((ToontownGlobals.torsoHeightDict[toon.style.torso]*bodyScale)/2) + legsHeight
    legsEffectHeight = legsHeight / 2
    effectX = headEffect.getX() # This remains the same for each effect
    effectY = headEffect.getY() # Same for each effect, will be adjusted slightly for each
    headEffect.setPos(effectX, effectY - 1.5, headEffectHeight)
    torsoEffect.setPos(effectX, effectY - 1, torsoEffectHeight)
    legsEffect.setPos(effectX, effectY - 0.6, legsEffectHeight)
    partDelay = 2.5 # Delay for particle effects
    headTrack = getPartTrack(headEffect, partDelay+0, 0.5, [headEffect, toon, 0])
    torsoTrack = getPartTrack(torsoEffect, partDelay+1.1, 0.5, [torsoEffect, toon, 0])
    legsTrack = getPartTrack(legsEffect, partDelay+2.2, 0.5, [legsEffect, toon, 0])

    def hideParts(parts): # Function to hide each lod part in list parts
        track = Parallel()
        for partNum in range(0, parts.getNumPaths()):
             nextPart = parts.getPath(partNum)
#             hideTrack.append(Func(nextPart.hide))
             track.append(Func(nextPart.setTransparency, 1))
             track.append(LerpFunctionInterval(nextPart.setAlphaScale, fromData=1,
                                                   toData=0, duration=0.2))
        return track

    def showParts(parts): # Fucntion to show each lod part in list parts
        track = Parallel()
        for partNum in range(0, parts.getNumPaths()):
            nextPart = parts.getPath(partNum)
#            hideTrack.append(Func(nextPart.show))
            track.append(Func(nextPart.clearColorScale))
            track.append(Func(nextPart.clearTransparency))
        return track

    soundTrack = getSoundTrack('SA_rubout.mp3', delay=1.7, node=suit)
    if (dmg > 0):
        # Now hide each body part in succession, then show each
        hideTrack.append(Wait(2.2))
        hideTrack.append(Func(battle.movie.needRestoreColor))
        hideTrack.append(hideParts(headParts))
#       hideTrack.append(Wait(0.9))
        hideTrack.append(Wait(0.4))
        hideTrack.append(hideParts(torsoParts))
#       hideTrack.append(Wait(0.9))
        hideTrack.append(Wait(0.4))
        hideTrack.append(hideParts(legsParts))
        hideTrack.append(Wait(1))
        hideTrack.append(showParts(headParts))
        hideTrack.append(showParts(torsoParts))
        hideTrack.append(showParts(legsParts))
        hideTrack.append(Func(battle.movie.clearRestoreColor))
        return Parallel(suitTrack, toonTrack, padPropTrack, pencilPropTrack, soundTrack,
                        hideTrack, headTrack, torsoTrack, legsTrack)
    else:
        return Parallel(suitTrack, toonTrack, padPropTrack, pencilPropTrack, soundTrack)


def doFingerWag(attack): # top p: fixed
    suit = attack['suit']
    battle = attack['battle']

    #Particle Effect: stream of 'Blahs'
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('FingerWag')
    BattleParticles.setEffectTexture(particleEffect, 'blah',
                                      color=Vec4(0.55, 0, 0.55, 1))

    #Adjust variables based on suit types - p(b), mm(c), tw(c), pp(a)
    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'):
        partDelay = 1.3
        damageDelay = 2.7
        dodgeDelay = 1.7
    elif (suitType == 'b'):
        partDelay = 1.3
        damageDelay = 2.7
        dodgeDelay = 1.8
    elif (suitType == 'c'):
        partDelay = 1.3
        damageDelay = 2.7
        dodgeDelay = 2.0

    #Build suit and particle effect tracks
    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, partDelay, 2, [particleEffect, suit, 0])

    #Adjust particle effect taking suit height into account
    suitName = attack['suitName']
    if (suitName == 'mm'):
        particleEffect.setPos(0.167, 1.5, 2.731)
    elif (suitName == 'tw'):
        particleEffect.setPos(0.167, 1.8, 5)
        particleEffect.setHpr(-90.0, -60.0, 180.0)
    elif (suitName == 'pp'):
        particleEffect.setPos(0.167, 1, 4.1)
    elif (suitName == 'bs'):
        particleEffect.setPos(0.167, 1, 5.1)
    elif (suitName == 'bw'):
        particleEffect.setPos(0.167, 1.9, suit.getHeight()-1.8)
        particleEffect.setP(-110)

    toonTrack = getToonTrack(attack, damageDelay, ['slip-backward'],
                             dodgeDelay, ['sidestep'])
    soundTrack = getSoundTrack('SA_finger_wag.mp3', delay=1.3, node=suit)

    return Parallel(suitTrack, toonTrack, partTrack, soundTrack)


def doWriteOff(attack): # top bc: fixed
    """ This function returns Tracks portraying the WriteOff attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    pad = globalPropPool.getProp('pad')
    pencil = globalPropPool.getProp('pencil')
    BattleParticles.loadParticles()
    checkmark = MovieUtil.copyProp(BattleParticles.getParticle('checkmark'))
    checkmark.setBillboardPointEye()

    suitTrack = getSuitTrack(attack)
    padPosPoints = [Point3(-0.25, 1.38, -0.08), VBase3(-19.078, -6.603, -171.594)]
    padPropTrack = getPropTrack(pad, suit.getLeftHand(),
                                  padPosPoints, 0.5, 2.57, Point3(1.89, 1.89, 1.89))

    # Calculate missPoint of the check mark with lambda function for combined checkmark, pencil Track
    missPoint = lambda checkmark = checkmark, toon=toon: __toonMissPoint(checkmark, toon)

    pencilPosPoints = [Point3(-0.47, 1.08, 0.28), VBase3(21.045, 12.702, -176.374)]
    #pencilPropTrack = getPropTrack(pencil, suit.getRightHand(), pencilPosPoints, #DELETE LATER
    #                               0.5, 2.57, Point3(1.5, 1.5, 1.5)) #DELETE LATER

    extraArgsForShowProp = [pencil, suit.getRightHand()] # Begin extraArgs for __showProp function
    extraArgsForShowProp.extend(pencilPosPoints) # Add in pos points for extraArgs

    pencilPropTrack = Sequence(
        Wait(0.5), # Wait the duration of appearDelay
        Func(__showProp, *extraArgsForShowProp), # Use showProp
        LerpScaleInterval(pencil, 0.5, Point3(1.5, 1.5, 1.5), startScale=Point3(0.01)),
        Wait(2), # Wait while suit animation continues #2.57
        #Checkmark Intervals
        Func(battle.movie.needRestoreRenderProp,
                                checkmark),
        Func(checkmark.reparentTo, render), # Give to render
        Func(checkmark.setScale, 1.6), # Scale the checkmark
        Func(checkmark.setPosHpr, pencil, 0, 0, 0, 0, 0, 0),
        Func(checkmark.setP, 0),
        Func(checkmark.setR, 0),
        )

    # Adding the intervals to throw the checkmark at the toon
    pencilPropTrack.append(getPropThrowTrack(attack, checkmark, [__toonFacePoint(toon)],
                                             [missPoint]))
    pencilPropTrack.append(Func(MovieUtil.removeProp, checkmark))
    pencilPropTrack.append(Func(battle.movie.clearRenderProp,
                                            checkmark))
    pencilPropTrack.append(Wait(0.3)) # Wait before scaling down the pencil
    pencilPropTrack.append(LerpScaleInterval(pencil, 0.5, MovieUtil.PNT3_NEARZERO)) # Scale down the pencil
    pencilPropTrack.append(Func(MovieUtil.removeProp, pencil))
    # All done, now make the PropTrack

    toonTrack = getToonTrack(attack, 3.4, ['slip-forward'], 2.4, ['sidestep'])
    soundTrack = Sequence(
        Wait(2.3),
        SoundInterval(globalBattleSoundCache.getSound('SA_writeoff_pen_only.mp3'), duration=0.9, node=suit),
        SoundInterval(globalBattleSoundCache.getSound('SA_writeoff_ding_only.mp3'), node=suit),
        )

    return Parallel(suitTrack, toonTrack, padPropTrack, pencilPropTrack, soundTrack)


"""
def doDitto(attack): # top ym: special, simultaneously copy attack; depends; depends
    pass #later
"""

def doRubberStamp(attack): # top ym: fixed
    """ This function returns Tracks portraying the RubberStamp attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']

    suitTrack = getSuitTrack(attack)

    stamp = globalPropPool.getProp("rubber-stamp")
    pad = globalPropPool.getProp("pad")
    cancelled = __makeCancelledNodePath()

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): #YesMan
        padPosPoints = [Point3(-0.65, 0.83, -0.04), VBase3(5.625, 4.456, -165.125)]
        stampPosPoints = [Point3(-0.64, -0.17, -0.03), MovieUtil.PNT3_ZERO]
    elif (suitType == 'c'):#Bottom Feeder
        padPosPoints = [Point3(0.19, -0.55, -0.21), VBase3(-166.760, -4.001, -1.658)]
        stampPosPoints = [Point3(-0.64, -0.08, 0.11), MovieUtil.PNT3_ZERO]
    else:
        padPosPoints = [Point3(-0.65, 0.83, -0.04), VBase3(5.625, 4.456, -165.125)]
        stampPosPoints = [Point3(-0.64, -0.17, -0.03), MovieUtil.PNT3_ZERO]

    padPropTrack = getPropTrack(pad, suit.getLeftHand(), padPosPoints, 0.000001, 3.2)

    # Calculate missPoint of the cancelled stamp with lambda function
    missPoint = lambda cancelled=cancelled, toon=toon: __toonMissPoint(cancelled, toon)

    propTrack = Sequence(# Build intervals for the stamp and cancelled props as one track
        Func(__showProp, stamp, suit.getRightHand(),
                         stampPosPoints[0], stampPosPoints[1]),
        LerpScaleInterval(stamp, 0.5, MovieUtil.PNT3_ONE), # Scale up the stamp
        Wait(2.6), # Wait while the suit animation continues
        Func(battle.movie.needRestoreRenderProp, cancelled),
        Func(cancelled.reparentTo, render), # Give to render
        Func(cancelled.setScale, 0.6), # Scale the cancelled
        Func(cancelled.setPosHpr, stamp, 0.81, -1.11, -0.16,
                         0, 0, 90),
        Func(cancelled.setP, 0),
        Func(cancelled.setR, 0),
        )
    # Now add in the intervals to throw the cancelled stamp at the toon
    propTrack.append(getPropThrowTrack(attack, cancelled, [__toonFacePoint(toon)],
                                       [missPoint]))
    propTrack.append(Func(MovieUtil.removeProp, cancelled))
    propTrack.append(Func(battle.movie.clearRenderProp,
                                      cancelled))
    propTrack.append(Wait(0.3)) # Wait before scaling down the stamp
    propTrack.append(LerpScaleInterval(stamp, 0.5, MovieUtil.PNT3_NEARZERO)) # Scale down the stamp
    propTrack.append(Func(MovieUtil.removeProp, stamp))

    toonTrack = getToonTrack(attack, 3.4, ['conked'], 1.9, ['sidestep'])
    soundTrack = getSoundTrack('SA_rubber_stamp.mp3', delay=1.3, duration=1.1, node=suit)

    return Parallel(suitTrack, toonTrack, propTrack, padPropTrack, soundTrack)


def doRazzleDazzle(attack): # top ym:fixed
    """This function returns Tracks portraying the RazzleDazzle attack"""
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    hitSuit = (dmg > 0)
    sign = globalPropPool.getProp('smile')

    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Smile')

    #Suit Track
    suitTrack = getSuitTrack(attack) # Get suit animation track

    #Combined Prop/Particle Track
    """Note: Tracks combined because part effect parented to prop"""
    signPosPoints = [Point3(0.00, -0.42, -0.04), VBase3(105.715, 73.977, 65.932)]

    if hitSuit:
        hitPoint = lambda toon=toon: __toonFacePoint(toon)
    else:
        hitPoint = lambda particleEffect=particleEffect, toon=toon, suit=suit: \
                   __toonMissPoint(particleEffect, toon, parent=suit.getRightHand())

    signPropTrack = Sequence(
        Wait(0.5), # Wait the duration of appearDelay
        Func(__showProp, sign, suit.getRightHand(),
                         signPosPoints[0], signPosPoints[1]),
        LerpScaleInterval(sign, 0.5, Point3(1.39, 1.39, 1.39)),
        Wait(0.5),
        Func(battle.movie.needRestoreParticleEffect,
                                particleEffect),
        Func(particleEffect.start, sign),
        Func(particleEffect.wrtReparentTo, render),
        LerpPosInterval(particleEffect, 2.0, pos=hitPoint),
        Func(particleEffect.cleanup),
        Func(battle.movie.clearRestoreParticleEffect,
                                particleEffect)
        )

    """This track necessary to sync smile sign animation with start of particle effect"""
    signPropAnimTrack = ActorInterval(sign, 'smile', duration=4, startTime=0)

    toonTrack = getToonTrack(attack, 2.6, ['cringe'], 1.9, ['sidestep'])
    soundTrack = getSoundTrack('SA_razzle_dazzle.mp3', delay=1.6, node=suit)

    return Sequence(
        Parallel(suitTrack, signPropTrack, signPropAnimTrack, toonTrack, soundTrack),
        Func(MovieUtil.removeProp, sign),
        )


def doSynergy(attack): # top ym: fixed
    """ This function returns Tracks portraying the Synergy attack """
    suit = attack['suit']
    battle = attack['battle']
    targets = attack['target']
    damageDelay = 1.7
    hitAtleastOneToon = 0
    for t in targets:
        if (t['hp'] > 0):
            hitAtleastOneToon = 1

    particleEffect = BattleParticles.createParticleEffect('Synergy')
    waterfallEffect = BattleParticles.createParticleEffect(file='synergyWaterfall')

    suitTrack = getSuitAnimTrack(attack) # Get suit animation track
    partTrack = getPartTrack(particleEffect, 1.0, 1.9, [particleEffect, suit, 0])
    waterfallTrack = getPartTrack(waterfallEffect, 0.8, 1.9,
                                   [waterfallEffect, suit, 0])

    damageAnims = [['slip-forward']] # Standard slip-forward damage animation
    dodgeAnims = [] # Dodge will be slowed down
    dodgeAnims.append(['jump', 0.01, 0, 0.6]) # Begin to jump
    # Now get animation interval with time inserted to slow down the jump at its peak
    dodgeAnims.extend(getSplicedLerpAnims('jump', 0.31, 1.3, startTime=0.6))
    dodgeAnims.append(['jump', 0, 0.91]) # Complete the jump
    toonTracks = getToonTracks(
        attack, damageDelay=damageDelay,
        damageAnimNames=['slip-forward'], dodgeDelay=0.91,
        splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.0)

    synergySoundTrack = Sequence(Wait(0.9),
                                 SoundInterval(globalBattleSoundCache.getSound('SA_synergy.mp3'), node=suit))

    if (hitAtleastOneToon > 0):
        fallingSoundTrack = Sequence(Wait(damageDelay+0.5),
                                     SoundInterval(globalBattleSoundCache.getSound('Toon_bodyfall_synergy.mp3'), node=suit))
        return Parallel(suitTrack, partTrack, waterfallTrack,
                        synergySoundTrack, fallingSoundTrack, toonTracks)
    else:
        return Parallel(suitTrack, partTrack, waterfallTrack,
                        synergySoundTrack, toonTracks)


def doTeeOff(attack): # top ym: fixed
    """ This function returns Tracks portraying the TeeOff attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    club = globalPropPool.getProp('golf-club')
    ball = globalPropPool.getProp('golf-ball')

    suitTrack = getSuitTrack(attack)
    clubPosPoints = [MovieUtil.PNT3_ZERO, VBase3(63.097, 43.988, -18.435)]
    clubPropTrack = getPropTrack(club, suit.getLeftHand(), clubPosPoints, 0.5, 5.2,
                                 Point3(1.1, 1.1, 1.1))

    # The ball is positioned differently for each suit
    suitName = attack['suitName']
    if (suitName == 'ym'):
        ballPosPoints = [Point3(2.1, 0, 0.1)]
    elif (suitName == 'tbc'):
        ballPosPoints = [Point3(4.1, 0, 0.1)]
    elif (suitName == 'm'):
        ballPosPoints = [Point3(3.2, 0, 0.1)]
    elif (suitName == 'rb'):
        ballPosPoints = [Point3(4.2, 0, 0.1)]
    else:
        ballPosPoints = [Point3(2.1, 0, 0.1)]

    ballPropTrack = Sequence(
        getPropAppearTrack(ball, suit, ballPosPoints, 1.7, Point3(1.5, 1.5, 1.5)),
        # Now leave the ball in place, not on club while it swings
        Func(battle.movie.needRestoreRenderProp, ball),
        Func(ball.wrtReparentTo, render),
        Wait(2.15), # Wait for club to swing
        )

    # Calculate missPoint with lambda function
    missPoint = lambda ball=ball, toon=toon: __toonMissPoint(ball, toon)
    ballPropTrack.append(getPropThrowTrack(attack, ball, [__toonFacePoint(toon)],
                                           [missPoint]))
    ballPropTrack.append(Func(battle.movie.clearRenderProp, ball))

    dodgeDelay = suitTrack.getDuration()-4.35
    toonTrack = getToonTrack(attack, suitTrack.getDuration()-2.25, ['conked'],
                             dodgeDelay, ['duck'], showMissedExtraTime=1.7)
    soundTrack = getSoundTrack('SA_tee_off.mp3', delay=4.1, node=suit)

    return Parallel(suitTrack, toonTrack, clubPropTrack, ballPropTrack, soundTrack)


def doBrainStorm(attack): # top mm(c), m/s(b): fixed
    """ This function returns Tracks portraying the BrainStorm attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    BattleParticles.loadParticles()
    snowEffect = BattleParticles.createParticleEffect('BrainStorm')
    snowEffect2 = BattleParticles.createParticleEffect('BrainStorm')
    snowEffect3 = BattleParticles.createParticleEffect('BrainStorm')
    effectColor = Vec4(0.65, 0.79, 0.93, 0.85)
    BattleParticles.setEffectTexture(snowEffect, 'brainstorm-box', color=effectColor)
    BattleParticles.setEffectTexture(snowEffect2, 'brainstorm-env', color=effectColor)
    BattleParticles.setEffectTexture(snowEffect3, 'brainstorm-track', color=effectColor)
    # cloud = MovieUtil.copyProp(toon.cloudActors[0])
    cloud = globalPropPool.getProp('stormcloud')
    
    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): # not used with type a
        partDelay = 1.2
        damageDelay = 4.5
        dodgeDelay = 3.3
    elif (suitType == 'b'):
        partDelay = 1.2
        damageDelay = 4.5
        dodgeDelay = 3.3
    elif (suitType == 'c'):
        partDelay = 1.2
        damageDelay = 4.5
        dodgeDelay = 3.3

    suitTrack = getSuitTrack(attack, delay=0.9)
    initialCloudHeight = suit.height + 3 #Initial height of cloud set to 3 meters above suit
    cloudPosPoints = [Point3(0, 3, initialCloudHeight), VBase3(180, 0, 0)]
    # Make the storm cloud appear over and slightly in front of the suit
    cloudPropTrack = Sequence()
    cloudPropTrack.append(Func(cloud.pose, 'stormcloud', 0))
    cloudPropTrack.append(getPropAppearTrack(cloud, suit, cloudPosPoints, 0.000001,
                                         Point3(3, 3, 3), scaleUpTime=0.7))
    cloudPropTrack.append(Func(battle.movie.needRestoreRenderProp,
                        cloud))
    cloudPropTrack.append(Func(cloud.wrtReparentTo, render))
    # Now calculate the targetPoint for the cloud to move to (over the target toon)
    targetPoint = __toonFacePoint(toon)
    targetPoint.setZ(targetPoint[2]+ 3)# Set end height of cloud to 3 meters above toon head
    # Push the cloud over to the target point (whether it hits or misses)
    cloudPropTrack.append(Wait(1.1)) # Wait to be pushed by suit
    cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
    # Must include particle track within cloud intervals to be safe...if the cloud is on
    # a separate track and get removed before the effect is parented, it will crash
    cloudPropTrack.append(Wait(partDelay)) # Wait before snow falls from cloud
    cloudPropTrack.append(Parallel(
        ParticleInterval(snowEffect, cloud, worldRelative=0,
                         duration=2.2, cleanup = True),
        Sequence(Wait(0.5),
                 ParticleInterval(snowEffect2, cloud,
                                  worldRelative=0, duration=1.7, cleanup = True)),
        Sequence(Wait(1.0),
                 ParticleInterval(snowEffect3, cloud,
                                  worldRelative=0, duration=1.2, cleanup = True)),
        Sequence(ActorInterval(cloud, 'stormcloud', startTime=3,
                               duration=0.5),
                 ActorInterval(cloud, 'stormcloud', startTime=2.5,
                               duration=0.5),
                 ActorInterval(cloud, 'stormcloud', startTime=1,
                               duration=1.5)),
        ))
        
    cloudPropTrack.append(Wait(0.4)) # Wait a moment before cloud goes away
    cloudPropTrack.append(LerpScaleInterval(cloud, 0.5,
                                         MovieUtil.PNT3_NEARZERO))
    # The particle effect has already been cleaned up, it's safe to remove the cloud
    cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
    cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))

    damageAnims = [['cringe', 0.01, 0.4, 0.8], ['duck', 0.000001, 1.6]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'],
                             showMissedExtraTime=1.1)
    soundTrack = getSoundTrack('SA_brainstorm.mp3', delay=2.6, node=suit)

    return Parallel(suitTrack, toonTrack, cloudPropTrack, soundTrack)


def doBuzzWord(attack): # top mm(c), dt(a): fixed
    """ This function returns Tracks portraying the BuzzWord attack """
    suit = attack['suit']
    target = attack['target']
    toon = target['toon']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffects = []
    texturesList = ['buzzwords-crash', 'buzzwords-inc', 'buzzwords-main',
                     'buzzwords-over', 'buzzwords-syn']
    for i in range(0, 5):
        effect = BattleParticles.createParticleEffect('BuzzWord')
        if (random.random() > 0.5): # 50% chance the words will be yellow or black
            BattleParticles.setEffectTexture(effect, texturesList[i],
                                              color=Vec4(1, 0.94, 0.02, 1))
        else:
            BattleParticles.setEffectTexture(effect, texturesList[i],
                                              color=Vec4(0, 0, 0, 1))
        particleEffects.append(effect)

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): # dt
        partDelay = 4.0
        partDuration = 2.2
        damageDelay = 4.5
        dodgeDelay = 3.8
    elif (suitType == 'b'): # not used with type B
        partDelay = 1.3
        partDuration = 2
        damageDelay = 2.5
        dodgeDelay = 1.8
    elif (suitType == 'c'): # mm
        partDelay = 4.0
        partDuration = 2.2
        damageDelay = 4.5
        dodgeDelay = 3.8

    # Some suits need to move the position and orientation of the particle effects
    suitName = suit.getStyleName()
    if (suitName == 'm'):
        for effect in particleEffects:
            effect.setPos(0, 2.8, suit.getHeight()-2.5)
            effect.setHpr(0, -20, 0)
    elif (suitName == 'mm'):
        for effect in particleEffects:
            effect.setPos(0, 2.1, suit.getHeight()-0.8)

    suitTrack = getSuitTrack(attack)
    particleTracks = []
    for effect in particleEffects:
        particleTracks.append(getPartTrack(effect, partDelay, partDuration,
                                             [effect, suit, 0]))

    toonTrack = getToonTrack(attack, damageDelay=damageDelay, damageAnimNames=['cringe'],
                             splicedDodgeAnims=[['duck', dodgeDelay, 1.4]],
                             showMissedExtraTime=dodgeDelay+0.5)
    soundTrack = getSoundTrack('SA_buzz_word.mp3', delay=3.9, node=suit)

    return Parallel(suitTrack, toonTrack, soundTrack, *particleTracks)


def doDemotion(attack): # top mm: fixed
    """ This function returns Tracks portraying the Demotion attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect('DemotionSpray')
    freezeEffect = BattleParticles.createParticleEffect('DemotionFreeze')
    unFreezeEffect = BattleParticles.createParticleEffect(file='demotionUnFreeze')
    BattleParticles.setEffectTexture(sprayEffect, 'snow-particle')
    BattleParticles.setEffectTexture(freezeEffect, 'snow-particle')
    BattleParticles.setEffectTexture(unFreezeEffect, 'snow-particle')

    # Now set the freezeEffect and unFreezeEffect height to the head of the toon
    facePoint = __toonFacePoint(toon)
    freezeEffect.setPos(0, 0, facePoint.getZ())
    unFreezeEffect.setPos(0, 0, facePoint.getZ())

    suitTrack = getSuitTrack(attack) # Get suit animation track
    partTrack = getPartTrack(sprayEffect, 0.7, 1.1, [sprayEffect, suit, 0])
    partTrack2 = getPartTrack(freezeEffect, 1.4, 2.9, [freezeEffect, toon, 0])
    partTrack3 = getPartTrack(unFreezeEffect, 6.65, 0.5, [unFreezeEffect, toon, 0])

    dodgeAnims = [['duck', 0.000001, 0.8]] # Standard duck animation
    damageAnims = [] # Damage animation will gradually slow down and freeze
    damageAnims.append(['cringe', 0.01, 0, 0.5]) # Start to cringe
    # Now gradually continue to cringe but become slower until freezing completely
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.4, 0.5, startTime=0.5))
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.3, 0.5, startTime=0.9))
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.3, 0.6, startTime=1.2))
    # Finish the cringe animation after holding frozen for a moment
    damageAnims.append(['cringe', 2.6, 1.5])
    toonTrack = getToonTrack(attack, damageDelay=1.0, splicedDamageAnims=damageAnims,
                             splicedDodgeAnims=dodgeAnims, showMissedExtraTime=1.6,
                             showDamageExtraTime=1.3)
    soundTrack = getSoundTrack('SA_demotion.mp3', delay=1.2, node=suit)

    if (dmg > 0): # If toon takes damage then use the freezing particle effects
        return Parallel(suitTrack, toonTrack, soundTrack,
                        partTrack, partTrack2, partTrack3)
    else: # If toon doesn't take damage, then don't include the freeze particle effect
        return Parallel(suitTrack, toonTrack, soundTrack, partTrack)


def doCanned(attack): # ds(b), cr(c) throw/particles?; struggle, slip-backward; sidestep
    """ This function returns Tracks portraying the Canned attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target['hp']
    toon = target['toon']
    hips = toon.getHipsParts()
    propDelay = 0.8

    # Timing slightly different for suits of different types
    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'c'): # cr
        suitDelay = 1.13
        dodgeDelay = 3.1
    else:
        suitDelay = 1.83
        dodgeDelay = 3.6
    throwDuration = 1.5
    can = globalPropPool.getProp('can') # Get prop from pool

    # The can will have an initial scale, but it grows larger after thrown
    # The can's scale is affected by the target toon
    scale = 26
    torso = toon.style.torso
    torso = torso[0] # just want to examine the first letter of the torso
    if (torso == 's'):
        scaleUpPoint = Point3(scale*2.63, scale*2.63, scale*1.9975)
    elif (torso == 'm'):
        scaleUpPoint = Point3(scale*2.63, scale*2.63, scale*1.7975)
    elif (torso == 'l'):
        scaleUpPoint = Point3(scale*2.63, scale*2.63, scale*2.31)
    canHpr = VBase3(-173.47, -0.42, 162.09)

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(-0.14, 0.15, 0.08), VBase3(-10.584, 11.945, -161.684)]
    throwTrack = Sequence(
        getPropAppearTrack(can, suit.getRightHand(), posPoints, propDelay,
                           Point3(6, 6, 6), scaleUpTime=0.5)
        )
    propDelay = propDelay + 0.5 # Add in the time to scale the prop
    throwTrack.append(Wait(suitDelay)) # Wait while suit animates
    hitPoint = toon.getPos(battle)
    hitPoint.setX(hitPoint.getX() + 1.1)
    hitPoint.setY(hitPoint.getY() - 0.5)
    hitPoint.setZ(hitPoint.getZ() + toon.height + 1.1)
    throwTrack.append(Func(battle.movie.needRestoreRenderProp, can))
    throwTrack.append(getThrowTrack(can, hitPoint, duration=throwDuration, parent=battle))

    # At this point, the can either cans the toon or bounces because the toon dodged
    if (dmg > 0): # The can cans the toon
        # Need a second can for the next lod of the toon
        can2 = MovieUtil.copyProp(can)
        hips1 = hips.getPath(2)
        hips2 = hips.getPath(1)
        can2Point = Point3(hitPoint.getX(), hitPoint.getY()+6.4, hitPoint.getZ())
        can2.setPos(can2Point)
        can2.setScale(scaleUpPoint)
        can2.setHpr(canHpr)
        throwTrack.append(Func(battle.movie.needRestoreHips))
        throwTrack.append(Func(can.wrtReparentTo, hips1))
        throwTrack.append(Func(can2.reparentTo, hips2))
        throwTrack.append(Wait(2.4))
        throwTrack.append(Func(MovieUtil.removeProp, can2))
        throwTrack.append(Func(battle.movie.clearRestoreHips))

        scaleTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpScaleInterval(can, throwDuration, scaleUpPoint),
            )
        hprTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpHprInterval(can, throwDuration, canHpr),
            )
        soundTrack = Sequence(
            Wait(2.6),
            SoundInterval(globalBattleSoundCache.getSound('SA_canned_tossup_only.mp3'), node=suit),
            SoundInterval(globalBattleSoundCache.getSound('SA_canned_impact_only.mp3'), node=suit),
            )
    else:
        land = toon.getPos(battle)
        land.setZ(land.getZ() + 0.7)
        bouncePoint1 = Point3(land.getX(), land.getY()-1.5, land.getZ()+2.5)
        bouncePoint2 = Point3(land.getX(), land.getY()-2.1, land.getZ()-0.2)
        bouncePoint3 = Point3(land.getX(), land.getY()-3.1, land.getZ()+1.5)
        bouncePoint4 = Point3(land.getX(), land.getY()-4.1, land.getZ()+0.3)
        throwTrack.append(LerpPosInterval(can, 0.4, land))
        throwTrack.append(LerpPosInterval(can, 0.4, bouncePoint1))
        throwTrack.append(LerpPosInterval(can, 0.3, bouncePoint2))
        throwTrack.append(LerpPosInterval(can, 0.3, bouncePoint3))
        throwTrack.append(LerpPosInterval(can, 0.3, bouncePoint4))
        throwTrack.append(Wait(1.1))
        throwTrack.append(LerpScaleInterval(can, 0.3, MovieUtil.PNT3_NEARZERO))

        scaleTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpScaleInterval(can, throwDuration, Point3(11, 11, 11)),
            )
        hprTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpHprInterval(can, throwDuration, canHpr),
            Wait(0.4),
            LerpHprInterval(can, 0.4, Point3(83.27, 19.52, -177.92)),
            LerpHprInterval(can, 0.3, Point3(95.24, -72.09, 88.65)),
            LerpHprInterval(can, 0.2, Point3(-96.34, -2.63, 179.89)),
            )
        soundTrack = getSoundTrack('SA_canned_tossup_only.mp3', delay=2.6, node=suit)

    canTrack = Sequence(
        Parallel(throwTrack, scaleTrack, hprTrack),
        Func(MovieUtil.removeProp, can),
        Func(battle.movie.clearRenderProp, can),
        )

    damageAnims = [['struggle', propDelay+suitDelay+throwDuration, 0.01, 0.7],
                    ['slip-backward', 0.01, 0.45],]
    toonTrack = getToonTrack(attack, splicedDamageAnims = damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'],
                             showDamageExtraTime=propDelay+suitDelay+2.4)

    return Parallel(suitTrack, toonTrack, canTrack, soundTrack)


def doDownsize(attack): # ds(b) special, toon shrinks; cringe; jump
    """ This function returns Tracks portraying the Downsize attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    damageDelay = 2.3

    sprayEffect = BattleParticles.createParticleEffect(file='downsizeSpray')
    cloudEffect = BattleParticles.createParticleEffect(file='downsizeCloud')
    toonPos = toon.getPos(toon)
    cloudPos = Point3(toonPos.getX(), toonPos.getY(), toonPos.getZ()+toon.getHeight()*0.55)
    cloudEffect.setPos(cloudPos)

    suitTrack = getSuitTrack(attack) # Get suit animation track
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.28, [sprayEffect, suit, 0])
    cloudTrack = getPartTrack(cloudEffect, 2.1, 1.9, [cloudEffect, toon, 0])

    # Need a track to shrink the toon down
    if (dmg > 0): # Only shrinks if takes damage
        initialScale = toon.getScale()
        downScale = Vec3(0.4, 0.4, 0.4)
        shrinkTrack = Sequence(
            Wait(damageDelay+0.5),
            Func(battle.movie.needRestoreToonScale),
            LerpScaleInterval(toon, 1.0, downScale*1.1),
            LerpScaleInterval(toon, 0.1, downScale*0.9),
            LerpScaleInterval(toon, 0.1, downScale*1.05),
            LerpScaleInterval(toon, 0.1, downScale*0.95),
            LerpScaleInterval(toon, 0.1, downScale),
            Wait(2.1),
            LerpScaleInterval(toon, 0.5, initialScale*1.5),
            LerpScaleInterval(toon, 0.15, initialScale*0.5),
            LerpScaleInterval(toon, 0.15, initialScale*1.2),
            LerpScaleInterval(toon, 0.15, initialScale*0.8),
            LerpScaleInterval(toon, 0.15, initialScale),
            Func(battle.movie.clearRestoreToonScale),
            )

    damageAnims = []
    damageAnims.append(['juggle', 0.01, 0.87, 0.5])
    damageAnims.append(['lose', 0.01, 2.17, 0.93])
    damageAnims.append(['lose', 0.01, 3.10, -0.93])
    damageAnims.append(['struggle', 0.01, 0.8, 1.8])
    damageAnims.append(['sidestep-right', 0.01, 2.97, 1.49])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=0.6, dodgeAnimNames=['sidestep'])

    if (dmg > 0): # Then include the shrinking cloud and shrinkTrack
        return Parallel(suitTrack, sprayTrack, cloudTrack, shrinkTrack, toonTrack)
    else:
        return Parallel(suitTrack, sprayTrack, toonTrack)


def doPinkSlip(attack): # ds(b) throw; slip-forward; sidestep
    """ This function returns Tracks portraying the Pinkslip attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    paper = globalPropPool.getProp('pink-slip') # Get prop from pool
    throwDelay = 3.03
    throwDuration = 0.5

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(0.07, -0.06, -0.18), VBase3(-172.075, -26.715, -89.131)]
    paperAppearTrack = Sequence(
        getPropAppearTrack(paper, suit.getRightHand(), posPoints, 0.8,
                           Point3(8, 8, 8), scaleUpTime=0.5)
        )
    paperAppearTrack.append(Wait(1.73)) # Wait while suit animates
    hitPoint = __toonGroundPoint(attack, toon, 0.2, parent=battle)
    paperAppearTrack.append(Func(battle.movie.needRestoreRenderProp,
                                         paper))
    paperAppearTrack.append(Func(paper.wrtReparentTo, battle))
    paperAppearTrack.append(LerpPosInterval(paper, throwDuration, hitPoint))

    if (dmg > 0):
        paperPause = 0.01
        slidePoint = Point3(hitPoint.getX(), hitPoint.getY()-5, hitPoint.getZ()+4)
        landPoint = Point3(hitPoint.getX(), hitPoint.getY()-5, hitPoint.getZ())
        paperAppearTrack.append(Wait(paperPause))
        paperAppearTrack.append(LerpPosInterval(paper, 0.2, slidePoint))
        paperAppearTrack.append(LerpPosInterval(paper, 1.1, landPoint))

        paperSpinTrack = Sequence(
            Wait(throwDelay),
            LerpHprInterval(paper, throwDuration, VBase3(300, 0, 0)),
            Wait(paperPause),
            LerpHprInterval(paper, 1.3, VBase3(-200, 100, 100)),
            )
    else:
        slidePoint = Point3(hitPoint.getX(), hitPoint.getY()-5, hitPoint.getZ())
        paperAppearTrack.append(LerpPosInterval(paper, 0.5, slidePoint))

        paperSpinTrack = Sequence(
            Wait(throwDelay),
            LerpHprInterval(paper, throwDuration, VBase3(300, 0, 0)),
            LerpHprInterval(paper, 0.5, VBase3(10, 0, 0)),
            )

    propTrack = Sequence()
    propTrack.append(Parallel(paperAppearTrack, paperSpinTrack))
    propTrack.append(LerpScaleInterval(paper, 0.4, MovieUtil.PNT3_NEARZERO))
    propTrack.append(Func(MovieUtil.removeProp, paper))
    propTrack.append(Func(battle.movie.clearRenderProp, paper))

    damageAnims = [['jump', 0.01, 0.3, 0.7], ['slip-forward', 0.01]]
    toonTrack = getToonTrack(attack, damageDelay=2.81, splicedDamageAnims=damageAnims,
                             dodgeDelay=2.8, dodgeAnimNames=['jump'],
                             showDamageExtraTime=0.9)
    soundTrack = getSoundTrack('SA_pink_slip.mp3', delay=2.9, duration=1.1, node=suit)

    return Parallel(suitTrack, toonTrack, propTrack, soundTrack)


def doReOrg(attack): # special, reassign toon parts; cringe, jump; jump
    """ This function returns Tracks portraying the ReOrg attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    damageDelay = 1.7
    attackDelay = 1.7
    sprayEffect = BattleParticles.createParticleEffect(file='reorgSpray')

    suitTrack = getSuitTrack(attack) # Get suit animation track
    partTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])

    if (dmg > 0): # Then manipulate the head and chest
        # The head track pops off the head, plays with it a bit, puts it back on upside down,
        # fixes it, rotates it backwards, and then restores it
        headParts = toon.getHeadParts()
        print '***********headParts pos=', headParts[0].getPos()
        print '***********headParts hpr=', headParts[0].getHpr()
        headTracks = Parallel()
        for partNum in range(0, headParts.getNumPaths()):
            part = headParts.getPath(partNum)
            x = part.getX()
            y = part.getY()
            z = part.getZ()
            h = part.getH()
            p = part.getP()
            r = part.getR()
            headTracks.append(Sequence(
                Wait(attackDelay),
                LerpPosInterval(part, 0.1, Point3(x-0.2, y, z-0.03)), # prepare to pop off head
                LerpPosInterval(part, 0.1, Point3(x+0.4, y, z-0.03)), # prepare to pop off head
                LerpPosInterval(part, 0.1, Point3(x-0.4, y, z-0.03)), # prepare to pop off head
                LerpPosInterval(part, 0.1, Point3(x+0.4, y, z-0.03)), # prepare to pop off head
                LerpPosInterval(part, 0.1, Point3(x-0.2, y, z-0.04)), # prepare to pop off head
                LerpPosInterval(part, 0.25, Point3(x, y, z+2.2)), # pop off head
                LerpHprInterval(part, 0.4, VBase3(360, 0, 180)), # spin and flip it
                LerpPosInterval(part, 0.3, Point3(x, y, z+3.1)), # raise it a bit
                LerpPosInterval(part, 0.15, Point3(x, y, z+0.3)), # put it back on
                Wait(0.15),
                LerpHprInterval(part, 0.6, VBase3(-745, 0, 180),
                                startHpr=VBase3(0, 0, 180)), # spin
                LerpHprInterval(part, 0.8, VBase3(25, 0, 180),
                                startHpr=VBase3(0, 0, 180)), # back
                LerpPosInterval(part, 0.15, Point3(x, y, z+1)), # pull it up again
                LerpHprInterval(part, 0.3, VBase3(h, p, r)), # flip it back over
                Wait(0.2),
                LerpPosInterval(part, 0.1, Point3(x, y, z)), # put it back down finally
                Wait(0.9),
                ))

        # The chest tracks involvement movement for the arms, sleeves, and hands,
        # each of which involve three LOD's.  The getChestTrack function returns the
        # interval for movement involving the chest performed upon the body part parameter.
        def getChestTrack(part, attackDelay=attackDelay):
            origScale = part.getScale()
            return Sequence(
                Wait(attackDelay),
                LerpHprInterval(part, 1.1, VBase3(180, 0, 0)),
                Wait(1.1),
                LerpHprInterval(part, 1.1, part.getHpr()),
                )

        chestTracks = Parallel()
        arms = toon.findAllMatches('**/arms')
        sleeves = toon.findAllMatches('**/sleeves')
        hands = toon.findAllMatches('**/hands')
        print '*************arms hpr=', arms[0].getHpr()

        for partNum in range(0, arms.getNumPaths()):
            chestTracks.append(getChestTrack(arms.getPath(partNum)))
            chestTracks.append(getChestTrack(sleeves.getPath(partNum)))
            chestTracks.append(getChestTrack(hands.getPath(partNum)))

    damageAnims = [['neutral', 0.01, 0.01, 0.5],
                    ['juggle', 0.01, 0.01, 1.48],
                    ['think', 0.01, 2.28]]
    dodgeAnims = [] # Dodge will be slowed down
    dodgeAnims.append(['think', 0.01, 0, 0.6]) # Begin to jump
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=0.01, dodgeAnimNames=['duck'],
                             showDamageExtraTime=2.1, showMissedExtraTime=2.0)

    if (dmg > 0): # Use the head and chest tracks
        return Parallel(suitTrack, partTrack, toonTrack, headTracks, chestTracks)
    else:
        return Parallel(suitTrack, partTrack, toonTrack)

def doSacked(attack): # ds(b) throw; struggle, jump; sidestep
    """ This function returns Tracks portraying the Sacked attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target['hp']
    toon = target['toon']
    hips = toon.getHipsParts()
    propDelay = 0.85
    suitDelay = 1.93
    throwDuration = 0.9

    sack = globalPropPool.getProp('sandbag')

    initialScale = Point3(0.65, 1.47, 1.28)
    scaleUpPoint = Point3(1.05, 1.67, 0.98) * 4.1
    sackHpr = VBase3(-154.33, -6.33, 163.80)

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(0.51, -2.03, -0.73), VBase3(90.000, -24.980, 77.730)]
    sackAppearTrack = Sequence(
        getPropAppearTrack(sack, suit.getRightHand(), posPoints, propDelay,
                           initialScale, scaleUpTime=0.2)
        )
    propDelay = propDelay + 0.2 # Add in the time to scale the prop
    sackAppearTrack.append(Wait(suitDelay)) # Wait while suit animates
    hitPoint = toon.getPos(battle)
    if (dmg > 0): # Different points to throw at for hit or miss
        hitPoint.setX(hitPoint.getX() + 2.1)
        hitPoint.setY(hitPoint.getY() + 0.9)
        hitPoint.setZ(hitPoint.getZ() + toon.height + 1.2)
    else:
        hitPoint.setZ(hitPoint.getZ() - 0.2)
    sackAppearTrack.append(Func(battle.movie.needRestoreRenderProp, sack))
    sackAppearTrack.append(getThrowTrack(sack, hitPoint, duration=throwDuration, parent=battle))

    # At this point, the sack either sack the toon or bounces because the toon dodged
    if (dmg > 0): # The sack sacks the toon
        # Need a second sack for the next lod of the toon
        sack2 = MovieUtil.copyProp(sack)
        hips1 = hips.getPath(2)
        hips2 = hips.getPath(1)
        sack2.hide()
        sack2.reparentTo(battle)
        sack2.setPos(Point3(hitPoint.getX(), hitPoint.getY(), hitPoint.getZ()))
        sack2.setScale(scaleUpPoint)
        sack2.setHpr(sackHpr)
        sackAppearTrack.append(Func(battle.movie.needRestoreHips))
        sackAppearTrack.append(Func(sack.wrtReparentTo, hips1))
        sackAppearTrack.append(Func(sack2.show))
        sackAppearTrack.append(Func(sack2.wrtReparentTo, hips2))
        sackAppearTrack.append(Wait(2.4))
        sackAppearTrack.append(Func(MovieUtil.removeProp, sack2))
        sackAppearTrack.append(Func(battle.movie.clearRestoreHips))

        scaleTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpScaleInterval(sack, throwDuration, scaleUpPoint),
            Wait(1.8),
            LerpScaleInterval(sack, 0.3, MovieUtil.PNT3_NEARZERO),
            )
        hprTrack = Sequence(
            Wait(propDelay + suitDelay),
            LerpHprInterval(sack, throwDuration, sackHpr),
            )
        sackTrack = Sequence(
            Parallel(sackAppearTrack, scaleTrack, hprTrack),
            Func(MovieUtil.removeProp, sack),
            Func(battle.movie.clearRenderProp, sack),
            )
    else:
        sackAppearTrack.append(Wait(1.1))
        sackAppearTrack.append(LerpScaleInterval(sack, 0.3, MovieUtil.PNT3_NEARZERO))
        sackTrack = Sequence(
            sackAppearTrack,
            Func(MovieUtil.removeProp, sack),
            Func(battle.movie.clearRenderProp, sack),
            )

    damageAnims = [['struggle', 0.01, 0.01, 0.7],
                    ['slip-backward', 0.01, 0.45],]
    toonTrack = getToonTrack(attack, damageDelay=propDelay+suitDelay+throwDuration,
                             splicedDamageAnims=damageAnims, dodgeDelay=3.0,
                             dodgeAnimNames=['sidestep'], showDamageExtraTime=1.8,
                             showMissedExtraTime=0.8)

    return Parallel(suitTrack, toonTrack, sackTrack)


def doGlowerPower(attack): # tw: fixed
    """ This function returns Tracks portraying the GlowerPower attack """
    suit = attack['suit']
    battle = attack['battle']
    leftKnives = []
    rightKnives = []
    for i in range(0, 3):
        leftKnives.append(globalPropPool.getProp('dagger'))
        rightKnives.append(globalPropPool.getProp('dagger'))

    suitTrack = getSuitTrack(attack)
    # Different suits have different places for their faces when they glower
    suitName = suit.getStyleName()
    if (suitName == 'hh'):
        leftPosPoints = [Point3(0.3, 4.3, 5.3), MovieUtil.PNT3_ZERO]
        rightPosPoints = [Point3(-0.3, 4.3, 5.3), MovieUtil.PNT3_ZERO]
    elif (suitName == 'tbc'):
        leftPosPoints = [Point3(0.6, 4.5, 6), MovieUtil.PNT3_ZERO]
        rightPosPoints = [Point3(-0.6, 4.5, 6), MovieUtil.PNT3_ZERO]
    else:
        leftPosPoints = [Point3(0.4, 3.8, 3.7), MovieUtil.PNT3_ZERO]
        rightPosPoints = [Point3(-0.4, 3.8, 3.7), MovieUtil.PNT3_ZERO]
    leftKnifeTracks = Parallel() # Build a track for the left knives being thrown
    rightKnifeTracks = Parallel() # Build a track for the right knives being thrown

    for i in range(0, 3):
        knifeDelay = 0.11
        leftTrack = Sequence() # Start new interval for next left knife
        leftTrack.append(Wait(1.1)) # All knives wait atleast this much
        leftTrack.append(Wait(i*knifeDelay)) # Put delay between each knife throw
        # Now make the knife scale up quickly
        leftTrack.append(getPropAppearTrack(leftKnives[i], suit, leftPosPoints,
                                            0.000001, Point3(.4, .4, .4), scaleUpTime=0.1))
        # Throw the knife toward the toon's face or the miss point
        leftTrack.append(getPropThrowTrack(attack, leftKnives[i],
                                           hitPointNames=['face'], missPointNames=['miss'],
                                           hitDuration=0.3, missDuration=0.3))
        leftKnifeTracks.append(leftTrack)

        rightTrack = Sequence() # Start new interval for next right knife
        rightTrack.append(Wait(1.1)) # All knives wait atleast this much
        rightTrack.append(Wait(i*knifeDelay)) # Put delay between each knife throw
        # Now make the knife scale up quickly
        rightTrack.append(getPropAppearTrack(rightKnives[i], suit, rightPosPoints,
                                             0.000001, Point3(.4, .4, .4), scaleUpTime=0.1))
        # Throw the knife toward the toon's face or the miss point
        rightTrack.append(getPropThrowTrack(attack, rightKnives[i],
                                            hitPointNames=['face'], missPointNames=['miss'],
                                            hitDuration=0.3, missDuration=0.3))
        rightKnifeTracks.append(rightTrack)

    damageAnims = [['slip-backward', 0.01, 0.35]]
    toonTrack = getToonTrack(attack, damageDelay=1.6, splicedDamageAnims=damageAnims,
                             dodgeDelay=0.7, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_glower_power.mp3', delay=1.1, node=suit)

    return Parallel(suitTrack, toonTrack, soundTrack, leftKnifeTracks, rightKnifeTracks)


def doHalfWindsor(attack): # hh(a) throw; conked; sidestep
    """ This function returns Tracks portraying the Half Windsor attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    tie = globalPropPool.getProp('half-windsor') # Get tie from pool
    throwDelay = 2.17
    damageDelay = 3.4
    dodgeDelay = 2.4

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(0.02, 0.88, 0.48), VBase3(99, -3, -108.2)]
    tiePropTrack = getPropAppearTrack(tie, suit.getRightHand(), posPoints, 0.5,
                     Point3(7, 7, 7), scaleUpTime=0.5)
    tiePropTrack.append(Wait(throwDelay)) # Wait while suit animates
    missPoint = __toonMissBehindPoint(toon, parent=battle)
    missPoint.setX(missPoint.getX() - 1.1)
    missPoint.setZ(missPoint.getZ() + 4)
    hitPoint = __toonFacePoint(toon, parent=battle)
    hitPoint.setX(hitPoint.getX() - 1.1)
    hitPoint.setY(hitPoint.getY() - 0.7)
    hitPoint.setZ(hitPoint.getZ() + 0.9)
    tiePropTrack.append(getPropThrowTrack(attack, tie, [hitPoint], [missPoint],
                                          hitDuration=0.4, missDuration=0.8, missScaleDown=0.3, parent=battle))

    damageAnims = [['conked', 0.01, 0.01, 0.4], ['cringe', 0.01, 0.7]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])

    return Parallel(suitTrack, toonTrack, tiePropTrack)


def doHeadShrink(attack): # hh(a) special, shrink head; cringe; jump
    """ This function returns Tracks portraying the Guilt Trip attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    damageDelay = 2.1
    dodgeDelay = 1.4

    shrinkSpray = BattleParticles.createParticleEffect(file='headShrinkSpray')
    shrinkCloud = BattleParticles.createParticleEffect(file='headShrinkCloud')
    shrinkDrop = BattleParticles.createParticleEffect(file='headShrinkDrop')

    suitTrack = getSuitTrack(attack) # Get suit animation track
    sprayTrack = getPartTrack(shrinkSpray, 0.3, 1.4, [shrinkSpray, suit, 0])

    shrinkCloud.reparentTo(battle)
    adjust = 0.4 # We push the cloud back slightly to be over the head during the animation
    x = toon.getX(battle)
    y = toon.getY(battle) - adjust
    z = 8
    shrinkCloud.setPos(Point3(x, y, z))
    shrinkDrop.setPos(Point3(0, 0-adjust, 7.5))
    off = 0.7
    cloudPoints = [Point3(x+off, y, z), Point3(x+off/2, y+off/2, z), Point3(x, y+off, z),
         Point3(x-off/2, y+off/2, z), Point3(x-off, y, z), Point3(x-off/2, y-off/2, z),
         Point3(x, y-off, z), Point3(x+off/2, y-off/2, z), Point3(x+off, y, z), Point3(x, y, z)]

    # The cloud will "circle" around the toon a bit as it sprinkles down shrinking dust
    circleTrack = Sequence()
    for point in cloudPoints:
        circleTrack.append(LerpPosInterval(shrinkCloud, 0.14, point, other=battle))

    cloudTrack = Sequence()
    cloudTrack.append(Wait(1.42))
    cloudTrack.append(Func(battle.movie.needRestoreParticleEffect,
                                        shrinkCloud))
    cloudTrack.append(Func(shrinkCloud.start, battle))
    cloudTrack.append(circleTrack)
    cloudTrack.append(circleTrack)
    cloudTrack.append(LerpFunctionInterval(shrinkCloud.setAlphaScale, fromData=1,
                                            toData=0, duration=0.7))
    cloudTrack.append(Func(shrinkCloud.cleanup))
    cloudTrack.append(Func(battle.movie.clearRestoreParticleEffect,
                                        shrinkCloud))

    shrinkDelay = 0.8
    shrinkDuration = 1.1
    shrinkTrack = Sequence()
    # Now create intervals to shrink the toons head
    if (dmg > 0):
        headParts = toon.getHeadParts()
        initialScale = headParts.getPath(0).getScale()[0]
        shrinkTrack.append(Wait(damageDelay+shrinkDelay))

        def scaleHeadParallel(scale, duration, headParts=headParts):
            headTracks = Parallel()
            for partNum in range(0, headParts.getNumPaths()):
                nextPart = headParts.getPath(partNum)
                headTracks.append(LerpScaleInterval(nextPart, duration,
                                                    Point3(scale, scale, scale)))
            return headTracks

        shrinkTrack.append(Func(battle.movie.needRestoreHeadScale))
        shrinkTrack.append(scaleHeadParallel(0.6, shrinkDuration))
        shrinkTrack.append(Wait(1.6))
        shrinkTrack.append(scaleHeadParallel(initialScale*3.2, 0.4))
        shrinkTrack.append(scaleHeadParallel(initialScale*0.7, 0.4))
        shrinkTrack.append(scaleHeadParallel(initialScale*2.5, 0.3))
        shrinkTrack.append(scaleHeadParallel(initialScale*0.8, 0.3))
        shrinkTrack.append(scaleHeadParallel(initialScale*1.9, 0.2))
        shrinkTrack.append(scaleHeadParallel(initialScale*0.85, 0.2))
        shrinkTrack.append(scaleHeadParallel(initialScale*1.7, 0.15))
        shrinkTrack.append(scaleHeadParallel(initialScale*0.9, 0.15))
        shrinkTrack.append(scaleHeadParallel(initialScale*1.3, 0.1))
        shrinkTrack.append(scaleHeadParallel(initialScale, 0.1))
        shrinkTrack.append(Func(battle.movie.clearRestoreHeadScale))
        shrinkTrack.append(Wait(0.7))

    dropTrack = getPartTrack(shrinkDrop, 1.5, 2.5, [shrinkDrop, toon, 0])
    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.65, 0.2])
    damageAnims.extend(getSplicedLerpAnims('cringe', 0.64, 1.0, startTime=0.85))
    damageAnims.append(['cringe', 0.4, 1.49])
    damageAnims.append(['conked', 0.01, 3.6, -1.6])
    damageAnims.append(['conked', 0.01, 3.1, 0.4])
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])

    if (dmg > 0): # then use the shrinkTrack
        shrinkSound = globalBattleSoundCache.getSound('SA_head_shrink_only.mp3')
        growSound = globalBattleSoundCache.getSound('SA_head_grow_back_only.mp3')
        soundTrack = Sequence(
            Wait(2.1),
            SoundInterval(shrinkSound, duration=2.1, node=suit),
            Wait(1.6),
            SoundInterval(growSound, node=suit),
            )

        return Parallel(suitTrack, sprayTrack, cloudTrack, dropTrack,
                        toonTrack, shrinkTrack, soundTrack)
    else:
        return Parallel(suitTrack, sprayTrack, cloudTrack,
                        dropTrack, toonTrack)


def doRolodex(attack): # top ac/tm(b), nd(a): fixed
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    rollodex = globalPropPool.getProp('rollodex')

#    particleEffect = BattleParticles.createParticleEffect(file='rollodexVortex')
    particleEffect2 = BattleParticles.createParticleEffect(file='rollodexWaterfall')
    particleEffect3 = BattleParticles.createParticleEffect(file='rollodexStream')

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'):
        propPosPoints = [Point3(-0.51, -0.03, -0.10), VBase3(89.673, 2.166, 177.786)]
        propScale = Point3(1.20, 1.20, 1.20)
        partDelay = 2.6
        part2Delay = 2.8
        part3Delay = 3.2
        partDuration = 1.6
        part2Duration = 1.9
        part3Duration = 1
        damageDelay = 3.8
        dodgeDelay = 2.5
    elif (suitType == 'b'):
        propPosPoints = [Point3(0.12, 0.24, 0.01), VBase3(99.032, 5.973, -179.839)]
        propScale = Point3(0.91, 0.91, 0.91)
        partDelay = 2.9
        part2Delay = 3.1
        part3Delay = 3.5
        partDuration = 1.6
        part2Duration = 1.9
        part3Duration = 1
        damageDelay = 4
        dodgeDelay = 2.5
    elif (suitType == 'c'): # not used with type C
        propPosPoints = [Point3(-0.51, -0.03, -0.10), VBase3(89.673, 2.166, 177.786)]
        propScale = Point3(1.20, 1.20, 1.20)
        partDelay = 2.3
        part2Delay = 2.8
        part3Delay = 3.2
        partDuration = 1.9
        part2Duration = 1.9
        part3Duration = 1
        damageDelay = 3.5
        dodgeDelay = 2.5

    hitPoint = lambda toon=toon: __toonFacePoint(toon)

    #Particle Effect: Vortex
    # Building w/out getPartTrack because of Lerp to move votex effect
#    partTrack = Sequence(
#        (partDelay, Func(battle.movie.needRestoreParticleEffect,
#                        particleEffect)),
#        Func(particleEffect.start, suit),
#        Func(particleEffect.wrtReparentTo, render),
#        LerpPosInterval(particleEffect, partDuration, pos=hitPoint),
#        Func(particleEffect.cleanup),
#        Func(battle.movie.clearRestoreParticleEffect,
#                        particleEffect),
#        )

    #Particle Effect 2: Waterfall
    partTrack2 = getPartTrack(particleEffect2, part2Delay, part2Duration,
    [particleEffect2, suit, 0])

    #Particle Effect 3: Stream
    partTrack3 = getPartTrack(particleEffect3, part3Delay, part3Duration,
    [particleEffect3, suit, 0])

    suitTrack = getSuitTrack(attack)
    propTrack = getPropTrack(rollodex, suit.getLeftHand(), propPosPoints, 0.000001,
                                 4.7, scaleUpPoint=propScale,
                                 anim=0, propName='rollodex', animDuration=0,
                                 animStartTime=0)

    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])
    soundTrack = getSoundTrack('SA_rolodex.mp3', delay=2.8, node=suit)

    return Parallel(suitTrack, toonTrack, propTrack, soundTrack, partTrack2, partTrack3)

def doEvilEye(attack): # cr(c) throw; cringe, slip-backward; duck
    """ This function returns Tracks portraying the Evil Eye attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    eye = globalPropPool.getProp('evil-eye')
    damageDelay = 2.44
    dodgeDelay = 1.64

    suitName = suit.getStyleName()
    if (suitName == 'cr'):
        posPoints = [Point3(-0.46, 4.85, 5.28), VBase3(-155.000, -20.000, 0.000)]
    elif (suitName == 'tf'):
        posPoints = [Point3(-0.4, 3.65, 5.01), VBase3(-155.000, -20.000, 0.000)]
    elif (suitName == 'le'):
        posPoints = [Point3(-0.64, 4.45, 5.91), VBase3(-155.000, -20.000, 0.000)]
    else:
        posPoints = [Point3(-0.4, 3.65, 5.01), VBase3(-155.000, -20.000, 0.000)]

    appearDelay = 0.8
    suitHoldStart = 1.06
    suitHoldStop = 1.69
    suitHoldDuration = suitHoldStop - suitHoldStart
    eyeHoldDuration = 1.1
    moveDuration = 1.1

    suitSplicedAnims = []
    suitSplicedAnims.append(['glower', 0.01, 0.01, suitHoldStart])
    suitSplicedAnims.extend(getSplicedLerpAnims('glower', suitHoldDuration, 1.1,
                                                 startTime=suitHoldStart))
    suitSplicedAnims.append(['glower', 0.01, suitHoldStop])
    suitTrack = getSuitTrack(attack, splicedAnims=suitSplicedAnims)

    eyeAppearTrack = Sequence(
        Wait(suitHoldStart),
        Func(__showProp, eye, suit, posPoints[0], posPoints[1]),
        LerpScaleInterval(eye, suitHoldDuration, Point3(11, 11, 11)),
        Wait(eyeHoldDuration*.3),
        LerpHprInterval(eye, 0.02, Point3(205, 40, 0)),
        Wait(eyeHoldDuration*.7),
        Func(battle.movie.needRestoreRenderProp, eye),
        Func(eye.wrtReparentTo, battle),
        )

    toonFace = __toonFacePoint(toon, parent=battle)
    if (dmg > 0):
        lerpInterval = LerpPosInterval(eye, moveDuration, toonFace)
    else:
        lerpInterval = LerpPosInterval(eye, moveDuration, Point3(toonFace.getX(),
                       toonFace.getY()-5, toonFace.getZ()-2))

    eyeMoveTrack = lerpInterval
    eyeRollTrack = LerpHprInterval(eye, moveDuration, Point3(0, 0, -180))

    eyePropTrack = Sequence(
        eyeAppearTrack,
        Parallel(eyeMoveTrack, eyeRollTrack),
        Func(battle.movie.clearRenderProp, eye),
        Func(MovieUtil.removeProp, eye),
        )

    damageAnims = [['duck', 0.01, 0.01, 1.4], ['cringe', 0.01, 0.3]]
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims, damageDelay=damageDelay,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['duck'],
                             showDamageExtraTime=1.7, showMissedExtraTime=1.7)
    soundTrack = getSoundTrack('SA_evil_eye.mp3', delay=1.3, node=suit)

    return Parallel(suitTrack, toonTrack, eyePropTrack, soundTrack)


def doPlayHardball(attack): # ls(b) throw; slip-backward; sidestep
    """ This function returns Tracks portraying the Play Hardball attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    ball = globalPropPool.getProp('baseball') # Get prop from pool

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'):
        suitDelay = 1.09
        damageDelay = 2.76
        dodgeDelay = 1.86
    elif (suitType == 'b'): # ls
        suitDelay = 1.79
        damageDelay = 3.46
        dodgeDelay = 2.56
    elif (suitType == 'c'): # cr
        suitDelay = 1.09
        damageDelay = 2.76
        dodgeDelay = 1.86

    suitTrack = getSuitTrack(attack) # Get standard suit track
    ballPosPoints = [Point3(0.04, 0.03, -0.31), VBase3(-1.152, 86.581, -76.784)]
    propTrack = Sequence(
        getPropAppearTrack(ball, suit.getRightHand(), ballPosPoints,
                           0.8, Point3(5, 5, 5), scaleUpTime=0.5))
    propTrack.append(Wait(suitDelay)) # Wait while suit animates
    propTrack.append(Func(battle.movie.needRestoreRenderProp,
                                       ball))
    propTrack.append(Func(ball.wrtReparentTo, battle))

    toonPos = toon.getPos(battle)
    x = toonPos.getX()
    y = toonPos.getY()
    z = toonPos.getZ()
    z = z + 0.2 # Should be slightly higher off the ground

    if (dmg > 0): # If hit toons, bounce the ball back toward the suit
        propTrack.append(LerpPosInterval(ball, 0.5, __toonFacePoint(toon, parent=battle)))
        propTrack.append(LerpPosInterval(ball, 0.5, Point3(x, y+3, z)))
        propTrack.append(LerpPosInterval(ball, 0.4, Point3(x, y+5, z+2)))
        propTrack.append(LerpPosInterval(ball, 0.3, Point3(x, y+6, z)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y+7, z+1)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y+8, z)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y+8.5, z+0.6)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y+9, z+0.2)))
        propTrack.append(Wait(0.4))
        soundTrack = getSoundTrack('SA_hardball_impact_only.mp3', delay=2.8, node=suit)
    else: # If misses, keep bouncing beyond the toon
        propTrack.append(LerpPosInterval(ball, 0.5, Point3(x, y+2, z)))
        propTrack.append(LerpPosInterval(ball, 0.4, Point3(x, y-1, z+2)))
        propTrack.append(LerpPosInterval(ball, 0.3, Point3(x, y-3, z)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y-4, z+1)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y-5, z)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y-5.5, z+0.6)))
        propTrack.append(LerpPosInterval(ball, 0.1, Point3(x, y-6, z+0.2)))
        propTrack.append(Wait(0.4))
        soundTrack = getSoundTrack('SA_hardball.mp3', delay=3.1, node=suit)
    propTrack.append(LerpScaleInterval(ball, 0.3, MovieUtil.PNT3_NEARZERO))
    propTrack.append(Func(MovieUtil.removeProp, ball))
    propTrack.append(Func(battle.movie.clearRenderProp,
                                       ball))

    damageAnims = [['conked', damageDelay, 0.01, 0.5], ['slip-backward', 0.01, 0.7]]
    toonTrack = getToonTrack(attack, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'],
                             showDamageExtraTime=3.9)

    return Parallel(suitTrack, toonTrack, propTrack, soundTrack)


def doPowerTie(attack): # cr(c) throw; conked; sidestep
    """ This function returns Tracks portraying the Power Tie attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    tie = globalPropPool.getProp('power-tie') # Get tie from pool

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): # type A not yet used
        throwDelay = 2.17
        damageDelay = 3.3
        dodgeDelay = 3.1
    elif (suitType == 'b'):
        throwDelay = 2.17
        damageDelay = 3.3
        dodgeDelay = 3.1
    elif (suitType == 'c'):
        throwDelay = 1.45
        damageDelay = 2.61
        dodgeDelay = 2.34

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(1.16, 0.24, 0.63), VBase3(171.561, 1.745, -163.443)]
    # First make the tie appear
    tiePropTrack = Sequence(
        getPropAppearTrack(tie, suit.getRightHand(), posPoints, 0.5,
                           Point3(3.5, 3.5, 3.5), scaleUpTime=0.5))
    tiePropTrack.append(Wait(throwDelay)) # Wait while suit animates
    tiePropTrack.append(Func(tie.setBillboardPointEye))
    tiePropTrack.append(getPropThrowTrack(attack, tie, [__toonFacePoint(toon)],
                                          [__toonGroundPoint(attack, toon, 0.1)],
                                          hitDuration=0.4, missDuration=0.8))

    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])

    throwSound = getSoundTrack('SA_powertie_throw.mp3', delay=2.3, node=suit)
    if (dmg > 0): # If take damage include sound effect
        hitSound = getSoundTrack('SA_powertie_impact.mp3', delay=2.9, node=suit)
        return Parallel(suitTrack, toonTrack, tiePropTrack, throwSound, hitSound)
    else:
        return Parallel(suitTrack, toonTrack, tiePropTrack, throwSound)


"""
def doCigarSmoke(attack): # project w/ 1 prop; cringe; sidestep
    pass #later

def doFloodTheMarket(attack): # project w/ 1 prop; slip-backward, jump; sidestep
    pass #later

def doSongAndDance(attack): # group2 particle w/ 0 props; bounce, slip-backward; sidestep
    pass #later
"""

def doDoubleTalk(attack): # top cc(c), tm(b), dt(a) : fixed
    """ This function returns Tracks portraying the DoubleTalk attack """
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('DoubleTalkLeft')
    particleEffect2 = BattleParticles.createParticleEffect('DoubleTalkRight')
    BattleParticles.setEffectTexture(particleEffect, 'doubletalk-double',
                                      color=Vec4(0, 1.0, 0.0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'doubletalk-good',
                                      color=Vec4(0, 1.0, 0.0, 1))

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): # dt
        partDelay = 3.3 # was 1.3 w/ finger-wag
        damageDelay = 3.5 # was 1.5 w/ finger-wag
        dodgeDelay = 3.3 # was 1.3 w/ finger-wag
    elif (suitType == 'b'): # tm
        partDelay = 3.3 # was 1.3 w/ finger-wag
        damageDelay = 3.5 # was 1.5 w/ finger-wag
        dodgeDelay = 3.3 # was 1.3 w/ finger-wag
    elif (suitType == 'c'): # cc
        partDelay = 3.3 # was 1.3 w/ finger-wag
        damageDelay = 3.5 # was 1.5 w/ finger-wag
        dodgeDelay = 3.3 # was 1.3 w/ finger-wag

    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, partDelay, 1.8, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, partDelay, 1.8, [particleEffect2, suit, 0])
    damageAnims = [['duck', 0.01, 0.4, 1.05], ['cringe', 0.000001, 0.8]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, splicedDodgeAnims=[['duck', 0.01, 1.4]],
                             showMissedExtraTime=0.9, showDamageExtraTime=0.8)
    soundTrack = getSoundTrack('SA_filibuster.mp3', delay=2.5, node=suit)
    
    return Parallel(suitTrack, toonTrack, partTrack, partTrack2, soundTrack)


def doFreezeAssets(attack): # top cc(c), pp(a): fixed
    """ This function returns Tracks portraying the FreezeAssets attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']

    BattleParticles.loadParticles()
    snowEffect = BattleParticles.createParticleEffect('FreezeAssets')
    BattleParticles.setEffectTexture(snowEffect, 'snow-particle')
    # cloud = MovieUtil.copyProp(toon.cloudActors[0])
    cloud = globalPropPool.getProp('stormcloud')
    
    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'):
        partDelay = 0.2
        damageDelay = 3.5
        dodgeDelay = 2.3
    elif (suitType == 'b'): # not used with type B
        partDelay = 0.2
        damageDelay = 3.5
        dodgeDelay = 2.3
    elif (suitType == 'c'):
        partDelay = 0.2
        damageDelay = 3.5
        dodgeDelay = 2.3

    suitTrack = getSuitTrack(attack, delay=0.9)
    initialCloudHeight = suit.height + 3 #Initial cloud height set to 3 meters above suit
    cloudPosPoints = [Point3(0, 3, initialCloudHeight), MovieUtil.PNT3_ZERO]
    # Make the storm cloud appear over and slightly in front of the suit
    cloudPropTrack = Sequence()
    cloudPropTrack.append(Func(cloud.pose, 'stormcloud', 0))
    cloudPropTrack.append(getPropAppearTrack(cloud, suit, cloudPosPoints, 0.000001,
                                         Point3(3, 3, 3), scaleUpTime=0.7))
    cloudPropTrack.append(Func(battle.movie.needRestoreRenderProp, cloud))
    cloudPropTrack.append(Func(cloud.wrtReparentTo, render))
    # Now calculate the targetPoint for the cloud to move to (right over the target toon)
    targetPoint = __toonFacePoint(toon)
    targetPoint.setZ(targetPoint[2] + 3)
    # Push the cloud over to the target point (whether it hits or misses)
    cloudPropTrack.append(Wait(1.1)) # Wait to be pushed by suit
    cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
    # Must include particle track within cloud intervals to be safe...if the cloud is on
    # a separate track and get removed before the effect is parented, it will crash
    cloudPropTrack.append(Wait(partDelay)) # Wait before snow falls from cloud
    cloudPropTrack.append(ParticleInterval(snowEffect, cloud, worldRelative=0,
                                duration=2.1, cleanup = True))
    cloudPropTrack.append(Wait(0.4)) # Wait a moment before cloud goes away
    cloudPropTrack.append(LerpScaleInterval(cloud, 0.5,
                                         MovieUtil.PNT3_NEARZERO))
    # The particle effect has already been cleaned up, it's safe to remove the cloud
    cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
    cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))

    damageAnims = [['cringe', 0.01, 0.4, 0.8], ['duck', 0.01, 1.6]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'],
                             showMissedExtraTime=1.2)

    return Parallel(suitTrack, toonTrack, cloudPropTrack)


def doHotAir(attack): # top cc(c): fixed
    """ This function returns Tracks portraying the HotAir attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    # Create spray of flames
    sprayEffect = BattleParticles.createParticleEffect('HotAir')
    # That spray starts a burning flame under the toon
    baseFlameEffect = BattleParticles.createParticleEffect(file='firedBaseFlame')
    # Add additional lense dense flames on top of the base flame
    flameEffect = BattleParticles.createParticleEffect('FiredFlame')
    # Include the flecks off the flame
    flecksEffect = BattleParticles.createParticleEffect('SpriteFiredFlecks')
    BattleParticles.setEffectTexture(sprayEffect, 'fire')
    BattleParticles.setEffectTexture(baseFlameEffect, 'fire')
    BattleParticles.setEffectTexture(flameEffect, 'fire')
    # Using a texture to make the flame flecks larger than points
    BattleParticles.setEffectTexture(flecksEffect, 'roll-o-dex',
                                      color=Vec4(0.95, 0.95, 0.0, 1))

    sprayDelay = 1.3 # was 1.1 w/ finger-wag
    flameDelay = 3.2 # was 3.0 w/ finger-wag
    flameDuration = 2.6 # was 1.8 w/ finger-wag
    flecksDelay = flameDelay + 0.8
    flecksDuration = flameDuration - 0.8 # was 1.0 w/ finger-wag
    damageDelay = 3.6 # was 2.6
    dodgeDelay = 2.0 # was 1.7

    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, sprayDelay, 2.3, [sprayEffect, suit, 0])
    baseFlameTrack = getPartTrack(baseFlameEffect, flameDelay, flameDuration,
                                   [baseFlameEffect, toon, 0])
    flameTrack = getPartTrack(flameEffect, flameDelay, flameDuration, [flameEffect, toon, 0])
    flecksTrack = getPartTrack(flecksEffect, flecksDelay, flecksDuration,
                                [flecksEffect, toon, 0])

    def changeColor(parts): # Function to change each lod part in list parts
         track = Parallel()
         for partNum in range(0, parts.getNumPaths()):
              nextPart = parts.getPath(partNum)
              track.append(Func(nextPart.setColorScale, Vec4(0, 0, 0, 1)))
         return track

    def resetColor(parts): # Reset the color of each lod part
         track = Parallel()
         for partNum in range(0, parts.getNumPaths()):
              nextPart = parts.getPath(partNum)
              track.append(Func(nextPart.clearColorScale))
         return track

    if (dmg > 0):
        # Now create a track to change the toon's color if hit (burned), but we must
        # extract the individual parts and change their color since some particle effects
        # are parented to the toon and would be changed as well
        headParts = toon.getHeadParts()
        torsoParts = toon.getTorsoParts()
        legsParts = toon.getLegsParts()

        colorTrack = Sequence()
        colorTrack.append(Wait(4.0)) # Wait before changing the color
        colorTrack.append(Func(battle.movie.needRestoreColor))
        colorTrack.append(changeColor(headParts))
        colorTrack.append(changeColor(torsoParts))
        colorTrack.append(changeColor(legsParts))
        colorTrack.append(Wait(3.5)) # Wait while color changed
        colorTrack.append(resetColor(headParts))
        colorTrack.append(resetColor(torsoParts))
        colorTrack.append(resetColor(legsParts))
        colorTrack.append(Func(battle.movie.clearRestoreColor))

    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.7, 0.62])
    damageAnims.append(['slip-forward', 0.01, 0.4, 1.2])
    damageAnims.append(['slip-forward', 0.01, 1.0])
    # Damage animation is toon cringing as gets hit then, then falls to the floor
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_hot_air.mp3', delay=1.6, node=suit)

    if (dmg > 0): # If toon takes damage, use the flames
        return Parallel(suitTrack, toonTrack, sprayTrack, soundTrack,
                        baseFlameTrack, flameTrack, flecksTrack, colorTrack)
    else: # Else just spray the fire but don't turn into a flame
        return Parallel(suitTrack, toonTrack, sprayTrack, soundTrack)


def doPickPocket(attack): # top tm: fixed
    """ This function returns Tracks portraying the Pickpocket attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target['hp']
    bill = globalPropPool.getProp('1dollar') # Get the dollar bill from prop pool

    suitTrack = getSuitTrack(attack)
    billPosPoints = [Point3(-0.01, 0.45, -0.25), VBase3(136.424, -46.434, -129.712)]
    billPropTrack = getPropTrack(bill, suit.getRightHand(), billPosPoints, 0.6, 0.55,
                    scaleUpPoint=Point3(1.41, 1.41, 1.41))
    toonTrack = getToonTrack(attack, 0.6, ['cringe'], 0.01, ['sidestep'])


    multiTrackList = Parallel(suitTrack, toonTrack)
    if (dmg > 0): # if toon takes damage (bill was stolen)
        soundTrack = getSoundTrack('SA_pick_pocket.mp3', delay=0.2, node=suit)
        multiTrackList.append(billPropTrack) # show the bill in the suit's hand
        multiTrackList.append(soundTrack) # add the sound of bill wagging
    return multiTrackList


def doFilibuster(attack): # top gh(c): fixed
    """ This function returns Tracks portraying the Filibuster attack """
    suit = attack['suit']
    target = attack['target']
    dmg = target['hp']
    battle = attack['battle']
    BattleParticles.loadParticles()
    sprayEffect = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect2 = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect3 = BattleParticles.createParticleEffect(file='filibusterSpray')
    sprayEffect4 = BattleParticles.createParticleEffect(file='filibusterSpray')
    color = Vec4(0.4, 0, 0, 1)
    BattleParticles.setEffectTexture(sprayEffect, 'filibuster-cut', color=color)
    BattleParticles.setEffectTexture(sprayEffect2, 'filibuster-fiscal', color=color)
    BattleParticles.setEffectTexture(sprayEffect3, 'filibuster-impeach', color=color)
    BattleParticles.setEffectTexture(sprayEffect4, 'filibuster-inc', color=color)

    partDelay = 1.3
    partDuration = 1.15
    damageDelay = 2.45
    dodgeDelay = 1.70

    suitTrack = getSuitTrack(attack)
    sprayTrack = getPartTrack(sprayEffect, partDelay, partDuration,
                               [sprayEffect, suit, 0])
    sprayTrack2 = getPartTrack(sprayEffect2, partDelay+0.8, partDuration,
                                [sprayEffect2, suit, 0])
    sprayTrack3 = getPartTrack(sprayEffect3, partDelay+1.6, partDuration,
                                [sprayEffect3, suit, 0])
    sprayTrack4 = getPartTrack(sprayEffect4, partDelay+2.4, partDuration,
                                [sprayEffect4, suit, 0])
    damageAnims = []
    # Take damage for each particle attack hit (4 times)
    for i in range(0, 4):
        damageAnims.append(['cringe', 0.00001, 0.3, 0.8])
    # Damage animation is toon cringing as gets hit then, then falls to the floor
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_filibuster.mp3', delay=1.1, node=suit)

    if (dmg > 0): # Use all particle effect words
        return Parallel(suitTrack, toonTrack, soundTrack,
                        sprayTrack, sprayTrack2, sprayTrack3, sprayTrack4)
    else: # If they miss, cut off the last word
        return Parallel(suitTrack, toonTrack, soundTrack,
                        sprayTrack, sprayTrack2, sprayTrack3)


def doSchmooze(attack): # top gh(c), mingler(a): fixed
    """ This function returns Tracks portraying the Schmooze attack """
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    upperEffects = [] # Upper wave of schmooze particles
    lowerEffects = [] # Lower wave of schmooze particles
    textureNames = ['schmooze-genius', 'schmooze-instant',
                     'schmooze-master', 'schmooze-viz']
    for i in range(0, 4):
        upperEffect = BattleParticles.createParticleEffect(file='schmoozeUpperSpray')
        lowerEffect = BattleParticles.createParticleEffect(file='schmoozeLowerSpray')
        BattleParticles.setEffectTexture(upperEffect, textureNames[i],
                                          color=Vec4(0, 0, 1, 1))
        BattleParticles.setEffectTexture(lowerEffect, textureNames[i],
                                          color=Vec4(0, 0, 1, 1))
        upperEffects.append(upperEffect)
        lowerEffects.append(lowerEffect)

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): # mingler not active yet
        partDelay = 1.3
        damageDelay = 1.8
        dodgeDelay = 1.1
    elif (suitType == 'b'): # not used with type B
        partDelay = 1.3
        damageDelay = 2.5
        dodgeDelay = 1.8
    elif (suitType == 'c'): # gh
        partDelay = 1.3 # was 1.3 w/ finger-wag
        damageDelay = partDelay + 1.4 # was partDelay+1.4 w/ finger-wag
        dodgeDelay = 0.9 # was 0.9 w/ finger-wag

    suitTrack = getSuitTrack(attack)
    upperPartTracks = Parallel()
    lowerPartTracks = Parallel()
    for i in range(0, 4): # Add each particle track for all four phrases
        upperPartTracks.append(getPartTrack(upperEffects[i], partDelay + (i*0.65),
                                              0.8, [upperEffects[i], suit, 0]))
        # Extra delay to add the lower particle wave to blend the two together in one wave
        lowerPartTracks.append(getPartTrack(lowerEffects[i], partDelay + (i*0.65) + 0.7,
                                              1.0, [lowerEffects[i], suit, 0]))

    damageAnims = []
    for i in range(0, 3): # Take damage three times
        damageAnims.append(['conked', 0.01, 0.3, 0.71])
    damageAnims.append(['conked', 0.01, 0.3]) # Take damage fourth time and finish

    dodgeAnims = []
    dodgeAnims.append(['duck', 0.01, 0.2, 2.7]) # Duck for first time
    dodgeAnims.append(['duck', 0.01, 1.22, 1.28]) # Duck again
    dodgeAnims.append(['duck', 0.01, 3.16]) # Finish off the duck animation (stand up)
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, splicedDodgeAnims=dodgeAnims,
                             showMissedExtraTime=1.9, showDamageExtraTime=1.1)
#    soundTrack = getSoundTrack('SA_schmooze.mp3', delay=2.1, node=suit))

    return Parallel(suitTrack, toonTrack, upperPartTracks, lowerPartTracks)


def doQuake(attack): # group2 ms(b) special, camera shake; shake; sidestep
    """ This function returns Tracks portraying the Quake attack """
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)

    damageAnims = [['slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01], ['jump', 0.01]]
    toonTracks = getToonTracks(
        attack, damageDelay=1.8, splicedDamageAnims=damageAnims,
        dodgeDelay=1.1, splicedDodgeAnims=dodgeAnims,
        showMissedExtraTime=2.8, showDamageExtraTime=1.1)

    return Parallel(suitTrack, toonTracks)


def doShake(attack): # top ac: improve
    # falls to soon, double suit anim speed on lose (miss)
    """ This function returns Tracks portraying the Shake attack """
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)

    damageAnims = [['slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01]]
    toonTracks = getToonTracks(
        attack, damageDelay=1.1, splicedDamageAnims=damageAnims,
        dodgeDelay=0.7, splicedDodgeAnims=dodgeAnims,
        showMissedExtraTime=2.8, showDamageExtraTime=1.1)

    return Parallel(suitTrack, toonTracks)


def doTremor(attack): # group2 special, camera shake; shake; sidestep
    """ This function returns Tracks portraying the Tremor attack """
    suit = attack['suit']
    suitTrack = getSuitAnimTrack(attack)

    damageAnims = [['slip-forward'], ['slip-forward', 0.01]]
    dodgeAnims = [['jump'], ['jump', 0.01]]
    toonTracks = getToonTracks(
        attack, damageDelay=1.1, splicedDamageAnims=damageAnims,
        dodgeDelay=0.7, splicedDodgeAnims=dodgeAnims,
        showMissedExtraTime=2.8, showDamageExtraTime=1.1)
    soundTrack = getSoundTrack('SA_tremor.mp3', delay=0.9, node=suit)

    return Parallel(suitTrack, soundTrack, toonTracks)


def doHangUp(attack): # top ac: fixed
    """ This function returns Tracks portraying the HangUp attack """
    suit = attack['suit']
    battle = attack['battle']
    phone = globalPropPool.getProp('phone')
    receiver = globalPropPool.getProp('receiver')

    suitTrack = getSuitTrack(attack)

    # Some suits need different positioning and timing for the phone
    suitName = suit.getStyleName()
    if (suitName == 'tf'):
        phonePosPoints = [Point3(-0.23, 0.01, -0.26), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(-0.13, -0.07, -0.06), VBase3(-1.854, 2.434, -177.579)]
        receiverAdjustScale = Point3(0.8, 0.8, 0.8)
        pickupDelay = 0.44
        dialDuration = 3.07
        finalPhoneDelay = 0.01
        scaleUpPoint = Point3(0.75, 0.75, 0.75)
    else:
        phonePosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverPosPoints = [Point3(0.23, 0.17, -0.11), VBase3(5.939, 2.763, -177.591)]
        receiverAdjustScale = MovieUtil.PNT3_ONE
        pickupDelay = 0.74
        dialDuration = 3.07
        finalPhoneDelay = 0.69
        scaleUpPoint = MovieUtil.PNT3_ONE

    propTrack = Sequence(# Single propTrack combines both phone and receiver
        Wait(0.3), # Wait to show the phone and receiver
        Func(__showProp, phone, suit.getLeftHand(),
                         phonePosPoints[0], phonePosPoints[1]), # Show phone
        Func(__showProp, receiver, suit.getLeftHand(),
                         receiverPosPoints[0], receiverPosPoints[1]), # Show receiver
        LerpScaleInterval(phone, 0.5, scaleUpPoint, MovieUtil.PNT3_NEARZERO), # Scale up phone
        Wait(pickupDelay), # Wait until suit picks up phone
        # Now reparent receiver to suit's right hand (he picks it up)
        Func(receiver.wrtReparentTo, suit.getRightHand()),
        LerpScaleInterval(receiver, 0.01, receiverAdjustScale),
        # Jam receiver into position in case reparenting is early or late.
        # Note: These coordinates are specific for type B suits
        LerpPosHprInterval(receiver, 0.0001, Point3(-0.53, 0.21, -0.54),
                           VBase3(-99.49, -35.27, 1.84)),
        Wait(dialDuration), # Wait while suit uses the phone
        # Now put the receiver back down on the phone
        Func(receiver.wrtReparentTo, phone),
        Wait(finalPhoneDelay), # Leave the phone around a bit longer
        LerpScaleInterval(phone, 0.5, MovieUtil.PNT3_NEARZERO), # Scale down phone & child receiver
        # Now destroy the receiver and then the phone
        Func(MovieUtil.removeProps, [receiver, phone]),
        )

    toonTrack = getToonTrack(attack, 5.5, ['slip-backward'], 4.7, ['jump'])
    soundTrack = getSoundTrack('SA_hangup.mp3', delay=1.3, node=suit)

    return Parallel(suitTrack, toonTrack, propTrack, soundTrack)


def doRedTape(attack): # top ac: fixed
    """ This function returns Tracks portraying the RedTape attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    tape = globalPropPool.getProp('redtape') # Get prop from pool
    tubes = [] # Need a separate tube for each lod of the toon
    for i in range(0, 3):
        tubes.append(globalPropPool.getProp('redtape-tube')) # Get prop from pool

    suitTrack = getSuitTrack(attack) # Get standard suit track
    # Tape's positioning depends a bit on who is holding it
    suitName = suit.getStyleName()
    if (suitName == 'tf' or suitName == 'nc'):
        tapePosPoints = [Point3(-0.24, 0.09, -0.38), VBase3(-1.152, 86.581, -76.784)]
    else:
        tapePosPoints = [Point3(0.24, 0.09, -0.38), VBase3(-1.152, 86.581, -76.784)]
    tapeScaleUpPoint = Point3(0.9, 0.9, 0.24)
    propTrack = Sequence(
        getPropAppearTrack(tape, suit.getRightHand(), tapePosPoints,
                           0.8, tapeScaleUpPoint, scaleUpTime=0.5))
    propTrack.append(Wait(1.73)) # Wait while suit animates
    hitPoint = lambda toon=toon: __toonTorsoPoint(toon)
    propTrack.append(getPropThrowTrack(attack, tape, [hitPoint],
                                       [__toonGroundPoint(attack, toon, 0.7)])) # Throw paper

    hips = toon.getHipsParts()
    animal = toon.style.getAnimal()
    scale = ToontownGlobals.toonBodyScales[animal]
    legs = toon.style.legs
    torso = toon.style.torso
    torso = torso[0] # just want to examine the first letter of the torso
    animal = animal[0] # just want to examine the first letter of the animal
    tubeHeight = -0.8

    # Adjust the scale of the tube depending on the torso size of the toon
    if (torso == 's'):
        scaleUpPoint = Point3(scale*2.03, scale*2.03, scale*.7975)
    elif (torso == 'm'):
        scaleUpPoint = Point3(scale*2.03, scale*2.03, scale*.7975)
    elif (torso == 'l'):
        scaleUpPoint = Point3(scale*2.03, scale*2.03, scale*1.11)

    # The horse and the dog reduce scales a bit and lowers the tube some
    if ((animal=='h') or (animal=='d')):
        tubeHeight = -0.87
        scaleUpPoint = Point3(scale*1.69, scale*1.69, scale*.67)

    tubePosPoints = [Point3(0, 0, tubeHeight), MovieUtil.PNT3_ZERO]
    tubeTracks = Parallel()
    tubeTracks.append(Func(battle.movie.needRestoreHips))
    for partNum in range(0, hips.getNumPaths()):
        nextPart = hips.getPath(partNum)
        tubeTracks.append(getPropTrack(tubes[partNum], nextPart, tubePosPoints, 3.25,
                                        3.17, scaleUpPoint=scaleUpPoint))
    tubeTracks.append(Func(battle.movie.clearRestoreHips))

    toonTrack = getToonTrack(attack, 3.4, ['struggle'], 2.8, ['jump'])
    soundTrack = getSoundTrack('SA_red_tape.mp3', delay=2.9, node=suit)

    if (dmg > 0): # If toon takes damage, show the red tape tube
        return Parallel(suitTrack, toonTrack, propTrack, soundTrack, tubeTracks)
    else: # Otherwise, do not show the tube
        return Parallel(suitTrack, toonTrack, propTrack, soundTrack)


def doParadigmShift(attack): # m(a) group2 particle w/ 0 props; shift; sidestep
    """ This function returns Tracks portraying the Paradigm Shift attack """
    suit = attack['suit']
    battle = attack['battle']
    targets = attack['target']
    hitAtleastOneToon = 0
    for t in targets:
        if (t['hp'] > 0):
            hitAtleastOneToon = 1

    damageDelay = 1.95
    dodgeDelay = 0.95
    sprayEffect = BattleParticles.createParticleEffect('ShiftSpray')
    suitName = suit.getStyleName()
    if (suitName == 'm'):
        sprayEffect.setPos(Point3(-5.2, 4.6, 2.7))
    elif (suitName == 'sd'):
        sprayEffect.setPos(Point3(-5.2, 4.6, 2.7))
    else:
        sprayEffect.setPos(Point3(0.1, 4.6, 2.7))

    suitTrack = getSuitAnimTrack(attack) # Get suit animation track
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])

    liftTracks = Parallel()
    toonRiseTracks = Parallel()

    for t in targets:
        toon = t['toon']
        dmg = t['hp']

        if (dmg > 0):
            liftEffect = BattleParticles.createParticleEffect('ShiftLift')
            liftEffect.setPos(toon.getPos(battle))
            liftEffect.setZ(liftEffect.getZ()-1.3)
            liftTracks.append(getPartTrack(liftEffect, 1.1, 4.1, [liftEffect, battle, 0]))

            shadow = toon.dropShadow
            # We'll manipulate a fake shadow and hide the normal one so they don't conflict
            fakeShadow = MovieUtil.copyProp(shadow)

            x = toon.getX()
            y = toon.getY()
            z = toon.getZ()
            height = 3
            groundPoint = Point3(x, y, z)
            risePoint = Point3(x, y, z+height)
            shakeRight = Point3(x, y+0.7, z+height)
            shakeLeft = Point3(x, y-0.7, z+height)

            shakeTrack = Sequence()
            shakeTrack.append(Wait(damageDelay+0.25))
            shakeTrack.append(Func(shadow.hide))
            shakeTrack.append(LerpPosInterval(toon, 1.1, risePoint))
            for i in range(0, 17):
                shakeTrack.append(LerpPosInterval(toon, 0.03, shakeLeft))
                shakeTrack.append(LerpPosInterval(toon, 0.03, shakeRight))
            shakeTrack.append(LerpPosInterval(toon, 0.1, risePoint))
            shakeTrack.append(LerpPosInterval(toon, 0.1, groundPoint))
            shakeTrack.append(Func(shadow.show))

            shadowTrack = Sequence()
            shadowTrack.append(Func(battle.movie.needRestoreRenderProp,
                                                 fakeShadow))
            shadowTrack.append(Wait(damageDelay+0.25))
            shadowTrack.append(Func(fakeShadow.hide))
            shadowTrack.append(Func(fakeShadow.setScale, 0.27))
            shadowTrack.append(Func(fakeShadow.reparentTo, toon))
            shadowTrack.append(Func(fakeShadow.setPos, MovieUtil.PNT3_ZERO))
            shadowTrack.append(Func(fakeShadow.wrtReparentTo, battle))
            shadowTrack.append(Func(fakeShadow.show))
            shadowTrack.append(LerpScaleInterval(fakeShadow, 0.4, Point3(0.17, 0.17, 0.17)))
            shadowTrack.append(Wait(1.81))
            shadowTrack.append(LerpScaleInterval(fakeShadow, 0.1, Point3(0.27, 0.27, 0.27)))
            shadowTrack.append(Func(MovieUtil.removeProp,
                                                 fakeShadow))
            shadowTrack.append(Func(battle.movie.clearRenderProp,
                                                 fakeShadow))

            toonRiseTracks.append(Parallel(shakeTrack, shadowTrack))

    damageAnims = []
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.9, startTime=2.06))
    damageAnims.append(['slip-backward', 0.01, 0.5])
    dodgeAnims = [] # Dodge will be slowed down
    dodgeAnims.append(['jump', 0.01, 0, 0.6]) # Begin to jump
    # Now get animation interval with time inserted to slow down the jump at its peak
    dodgeAnims.extend(getSplicedLerpAnims('jump', 0.31, 1.0, startTime=0.6))
    dodgeAnims.append(['jump', 0, 0.91]) # Complete the jump
    toonTracks = getToonTracks(
        attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
        dodgeDelay=dodgeDelay, splicedDodgeAnims=dodgeAnims,
        showDamageExtraTime=2.7)

    if (hitAtleastOneToon == 1):
        soundTrack = getSoundTrack('SA_paradigm_shift.mp3', delay=2.1, node=suit)
        return Parallel(suitTrack, sprayTrack, soundTrack,
                        liftTracks, toonTracks, toonRiseTracks)
    else:
        return Parallel(suitTrack, sprayTrack,
                        liftTracks, toonTracks, toonRiseTracks)


def doPowerTrip(attack): # group2 particle w/ 0 props; slip-forward; jump
    """ This function returns Tracks portraying the Power Trip attack """
    suit = attack['suit']
    battle = attack['battle']

    # Set up all the particle effects, colors, and positions
    centerColor = Vec4(0.1, 0.1, 0.1, 0.4)
    edgeColor = Vec4(0.4, 0.1, 0.9, 0.7)
    powerBar1 = BattleParticles.createParticleEffect(file='powertrip')
    powerBar2 = BattleParticles.createParticleEffect(file='powertrip2')
    powerBar1.setPos(0, 6.1, 0.4)
    powerBar1.setHpr(-60, 0, 0)
    powerBar2.setPos(0, 6.1, 0.4)
    powerBar2.setHpr(60, 0, 0)
    powerBar1Particles = powerBar1.getParticlesNamed('particles-1')
    powerBar2Particles = powerBar2.getParticlesNamed('particles-1')
    powerBar1Particles.renderer.setCenterColor(centerColor)
    powerBar1Particles.renderer.setEdgeColor(edgeColor)
    powerBar2Particles.renderer.setCenterColor(centerColor)
    powerBar2Particles.renderer.setEdgeColor(edgeColor)
    waterfallEffect = BattleParticles.createParticleEffect('Waterfall')
    waterfallEffect.setScale(11)
    waterfallParticles = waterfallEffect.getParticlesNamed('particles-1')
    waterfallParticles.renderer.setCenterColor(centerColor)
    waterfallParticles.renderer.setEdgeColor(edgeColor)

    # Different suits position the waterfall effect differently
    suitName = suit.getStyleName()
    if (suitName == 'mh'):
        waterfallEffect.setPos(0, 4, 3.6)

    suitTrack = getSuitAnimTrack(attack) # Get suit animation track

    def getPowerTrack(effect, suit=suit, battle=battle):
        partTrack = Sequence(
            Wait(1.0),
            Func(battle.movie.needRestoreParticleEffect, effect),
            Func(effect.start, suit),
            Wait(0.4),
            LerpPosInterval(effect, 1.0, Point3(0, 15, 0.4)),
            LerpFunctionInterval(effect.setAlphaScale, fromData=1,
                                 toData=0, duration=0.4),
            Func(effect.cleanup),
            Func(battle.movie.clearRestoreParticleEffect,
                 effect),
            )
        return partTrack
    partTrack1 = getPowerTrack(powerBar1)
    partTrack2 = getPowerTrack(powerBar2)
    waterfallTrack = getPartTrack(waterfallEffect, 0.6, 1.3,
                                   [waterfallEffect, suit, 0])

    toonTracks = getToonTracks(attack, 1.8, ['slip-forward'], 1.29, ['jump'])


    return Parallel(suitTrack, partTrack1, partTrack2, waterfallTrack, toonTracks)


"""
def doSandtrap(attack): # particle w/ 1 prop; slip-forward; duck
    pass #later
"""

#Note: throwEndPoint set with function at runtime
#      parent= battle because render is variable.  Using suit as parent creates
#      a better bounce path, but check jumps when suit moves.
def getThrowEndPoint(suit, toon, battle, whichBounce):
    pnt = toon.getPos(toon)

    if whichBounce == 'one':
        pnt.setY(pnt[1] + 8) # adjust distance in front of toon
    elif whichBounce == 'two':
        pnt.setY(pnt[1] + 5) # adjust distance in front of toon
    elif whichBounce == 'threeHit':
        pnt.setZ(pnt[2] + toon.shoulderHeight + 0.3)#set height to the toon's face
    elif whichBounce == 'threeMiss':
        pass # do nothing, it's the toon's position
    elif whichBounce == 'four':
        pnt.setY(pnt[1] - 5) # adjust distance from toon

    return Point3(pnt)

def doBounceCheck(attack): # top pp: fixed
    """ This function returns Tracks portraying the BounceCheck attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    battle = attack['battle']
    toon = target['toon']
    dmg = target['hp']
    hitSuit = (dmg > 0)

    check = globalPropPool.getProp('bounced-check')
    checkPosPoints = [MovieUtil.PNT3_ZERO, VBase3(95.247, 79.025, 88.849)]

    bounce1Point = lambda suit=suit, toon=toon, battle=battle: \
        getThrowEndPoint(suit, toon, battle, 'one')
    bounce2Point = lambda suit=suit, toon=toon, battle=battle: \
        getThrowEndPoint(suit, toon, battle, 'two')
    hit3Point = lambda suit=suit, toon=toon, battle=battle: \
        getThrowEndPoint(suit, toon, battle, 'threeHit')
    miss3Point = lambda suit=suit, toon=toon, battle=battle: \
        getThrowEndPoint(suit, toon, battle, 'threeMiss')
    bounce4Point = lambda suit=suit, toon=toon, battle=battle: \
        getThrowEndPoint(suit, toon, battle, 'four')

    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): # PennyPincher(pp)
        throwDelay = 2.5
        dodgeDelay = 4.3
        damageDelay = 5.1
    elif (suitType == 'b'): # type b not yet used
        throwDelay = 1.8
        dodgeDelay = 3.6
        damageDelay = 4.4
    elif (suitType == 'c'): # ShortChange(sc), TightWad(tw)
        throwDelay = 1.8
        dodgeDelay = 3.6
        damageDelay = 4.4

    suitTrack = getSuitTrack(attack)

    checkPropTrack = Sequence(
        getPropAppearTrack(check, suit.getRightHand(), checkPosPoints, 0.00001,
                           Point3(8.5, 8.5, 8.5), startScale=MovieUtil.PNT3_ONE))
    checkPropTrack.append(Wait(throwDelay)) #Wait amount of time before release
    checkPropTrack.append(Func(check.wrtReparentTo, toon))
    checkPropTrack.append(Func(check.setHpr, Point3(0, -90, 0)))

    # Bounce the check twice towards the toon
    checkPropTrack.append(getThrowTrack(check, bounce1Point, duration=0.5, parent=toon))
    checkPropTrack.append(getThrowTrack(check, bounce2Point, duration=0.9, parent=toon))

    if hitSuit: # hit the toon in the face with the check
        checkPropTrack.append(getThrowTrack(check, hit3Point, duration=0.7, parent=toon))
    else: # the toon dodged, bounce right on by
        checkPropTrack.append(getThrowTrack(check, miss3Point, duration=0.7, parent=toon))
        checkPropTrack.append(getThrowTrack(check, bounce4Point, duration=0.7, parent=toon))
        checkPropTrack.append(LerpScaleInterval(check, 0.3, MovieUtil.PNT3_NEARZERO))

    checkPropTrack.append(Func(MovieUtil.removeProp, check))

    toonTrack = getToonTrack(attack, damageDelay, ['conked'], dodgeDelay, ['sidestep'])

    soundTracks = Sequence(
        getSoundTrack('SA_pink_slip.mp3', delay=throwDelay+0.5, duration=0.6, node=suit),
        getSoundTrack('SA_pink_slip.mp3', delay=0.4, duration=0.6, node=suit),
        )

    return Parallel(suitTrack, checkPropTrack, toonTrack, soundTracks)


def doWatercooler(attack): # top sc: fixed
    """ This function returns Tracks portraying the Watercooler attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    watercooler = globalPropPool.getProp('watercooler')

    def getCoolerSpout(watercooler=watercooler):
        spout = watercooler.find("**/joint_toSpray")
        return spout.getPos(render)

    hitPoint = lambda toon=toon: __toonFacePoint(toon)
    missPoint = lambda prop=watercooler, toon=toon: \
                __toonMissPoint(prop, toon, 0, parent=render)
    hitSprayTrack = MovieUtil.getSprayTrack(battle,
                 Point4(0.75, 0.75, 1.0, 0.8),
                 getCoolerSpout, hitPoint, 0.2, 0.2, 0.2, horizScale=0.3,
                 vertScale=0.3)
    missSprayTrack = MovieUtil.getSprayTrack(battle,
                 Point4(0.75, 0.75, 1.0, 0.8),
                 getCoolerSpout, missPoint, 0.2, 0.2, 0.2, horizScale=0.3,
                 vertScale=0.3)

    suitTrack = getSuitTrack(attack)
    posPoints = [Point3(0.48, 0.11, -0.92), VBase3(20.403, 33.158, 69.511)]
    propTrack = Sequence(# Build intervals for watercooler, including its spray
        Wait(1.01), # Wait the duration of appearDelay
        Func(__showProp, watercooler, suit.getLeftHand(),
                         posPoints[0], posPoints[1]),
        LerpScaleInterval(watercooler, 0.5, Point3(1.15, 1.15, 1.15)),
        Wait(1.6), # Wait until time to spray
        )

    if (dmg > 0): # If toon takes damage use the hit spray
        propTrack.append(hitSprayTrack) # Add in the spray intervals
    else: # Otherwise use the miss spray
        propTrack.append(missSprayTrack) # Add in the spray intervals
    propTrack += [# Add the rest of the prop intervals
        Wait(0.01), # Wait while suit animation continues
        LerpScaleInterval(watercooler, 0.5, MovieUtil.PNT3_NEARZERO), # Scale down the prop
        Func(MovieUtil.removeProp, watercooler),
        ]

    splashTrack = Sequence()
    if (dmg > 0): # If toon is hit
        def prepSplash(splash, targetPoint):
            splash.reparentTo(render)
            splash.setPos(targetPoint)
            scale = splash.getScale()
            splash.setBillboardPointWorld()
            splash.setScale(scale)
        splash = globalPropPool.getProp('splash-from-splat')
        splash.setColor(0.75, 0.75, 1, 0.8)
        splash.setScale(0.3)
        splashTrack = Sequence(
            Func(battle.movie.needRestoreRenderProp,
                             splash),
            Wait(3.2),
            Func(prepSplash, splash, __toonFacePoint(toon)),
            ActorInterval(splash, 'splash-from-splat'),
            Func(MovieUtil.removeProp, splash),
            Func(battle.movie.clearRenderProp, splash),
            )

    toonTrack = getToonTrack(attack, suitTrack.getDuration()-1.5, ['cringe'],
                             2.4, ['sidestep']) # Get toon track
    soundTrack = Sequence(
        Wait(1.1),
        SoundInterval(globalBattleSoundCache.getSound('SA_watercooler_appear_only.mp3'),
                      node=suit, duration=1.4722),
        Wait(0.4),
        SoundInterval(globalBattleSoundCache.getSound('SA_watercooler_spray_only.mp3'),
                      node=suit, duration=2.313),
        )

    return Parallel(suitTrack, toonTrack, propTrack, soundTrack, splashTrack)


"""
def doPennyPinch(attack): # top sc: needs: model(pincers, penny) project w/ 1 prop; conked; sidestep
    pass #later
"""

def doFired(attack): # top tw: fixed
    """ This function returns Tracks portraying the Fired attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    baseFlameEffect = BattleParticles.createParticleEffect(file='firedBaseFlame')
    flameEffect = BattleParticles.createParticleEffect('FiredFlame')
    flecksEffect = BattleParticles.createParticleEffect('SpriteFiredFlecks')
    BattleParticles.setEffectTexture(baseFlameEffect, 'fire')
    BattleParticles.setEffectTexture(flameEffect, 'fire')
    # Using textures instead of points to make the flame flecks larger
    # Reusing plain roll-o-dex texture and making it yellow
    BattleParticles.setEffectTexture(flecksEffect, 'roll-o-dex',
                                      color=Vec4(0.8, 0.8, 0.8, 1))

    # Now we create smaller flame effects for when the suit misses the toon
    baseFlameSmall = BattleParticles.createParticleEffect(file='firedBaseFlame')
    flameSmall = BattleParticles.createParticleEffect('FiredFlame')
    flecksSmall = BattleParticles.createParticleEffect('SpriteFiredFlecks')
    BattleParticles.setEffectTexture(baseFlameSmall, 'fire')
    BattleParticles.setEffectTexture(flameSmall, 'fire')
    # Using textures instead of points to make the flame flecks larger
    # Reusing plain roll-o-dex texture and making it yellow
    BattleParticles.setEffectTexture(flecksSmall, 'roll-o-dex',
                                      color=Vec4(0.8, 0.8, 0.8, 1))
    baseFlameSmall.setScale(0.7)
    flameSmall.setScale(0.7)
    flecksSmall.setScale(0.7)

    suitTrack = getSuitTrack(attack) # Get suit animation track
    baseFlameTrack = getPartTrack(baseFlameEffect, 1.0, 1.9,
                                   [baseFlameEffect, toon, 0])
    flameTrack = getPartTrack(flameEffect, 1.0, 1.9, [flameEffect, toon, 0])
    flecksTrack = getPartTrack(flecksEffect, 1.8, 1.1, [flecksEffect, toon, 0])
    baseFlameSmallTrack = getPartTrack(baseFlameSmall, 1.0, 1.9,
                                   [baseFlameSmall, toon, 0])
    flameSmallTrack = getPartTrack(flameSmall, 1.0, 1.9, [flameSmall, toon, 0])
    flecksSmallTrack = getPartTrack(flecksSmall, 1.8, 1.1, [flecksSmall, toon, 0])

    # Now create a track to change the toon's color if hit (burned), but we must
    # extract the individual parts and change their color since some particle effects
    # are parented to the toon and would be changed as well
    def changeColor(parts): # Function to change each lod part in list parts
         track = Parallel()
         for partNum in range(0, parts.getNumPaths()):
              nextPart = parts.getPath(partNum)
              track.append(Func(nextPart.setColorScale, Vec4(0, 0, 0, 1)))
         return track

    def resetColor(parts): # Reset the color of each lod part
         track = Parallel()
         for partNum in range(0, parts.getNumPaths()):
              nextPart = parts.getPath(partNum)
              track.append(Func(nextPart.clearColorScale))
         return track

    if (dmg > 0):
        headParts = toon.getHeadParts()
        torsoParts = toon.getTorsoParts()
        legsParts = toon.getLegsParts()

        colorTrack = Sequence()
        colorTrack.append(Wait(2.0)) # Wait before changing the color
        colorTrack.append(Func(battle.movie.needRestoreColor))
        colorTrack.append(changeColor(headParts))
        colorTrack.append(changeColor(torsoParts))
        colorTrack.append(changeColor(legsParts))
        colorTrack.append(Wait(3.5)) # Wait while color changed
        colorTrack.append(resetColor(headParts))
        colorTrack.append(resetColor(torsoParts))
        colorTrack.append(resetColor(legsParts))
        colorTrack.append(Func(battle.movie.clearRestoreColor))

    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.7, 0.62])
    damageAnims.append(['slip-forward', 0.00001, 0.4, 1.2])
    damageAnims.extend(getSplicedLerpAnims('slip-forward', 0.31, 0.8, startTime=1.2))
    # Damage animation is toon cringing as gets hit then, then falls to the floor
    toonTrack = getToonTrack(attack, damageDelay=1.5, splicedDamageAnims=damageAnims,
                             dodgeDelay=0.3, dodgeAnimNames=['sidestep'])

    soundTrack = getSoundTrack('SA_hot_air.mp3', delay=1.0, node=suit)
    
    if (dmg > 0): # If toon takes damage, use the flames
        return Parallel(suitTrack, baseFlameTrack, flameTrack, flecksTrack,
                        toonTrack, colorTrack, soundTrack)
    else: # Otherwise don't use the flames
        return Parallel(suitTrack, baseFlameSmallTrack, flameSmallTrack,
                        flecksSmallTrack, toonTrack, soundTrack)


def doAudit(attack): # top bc: fixed
    """ This function returns Tracks portraying the Audit attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-one',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-two',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-three',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-four',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-mult',
                                      color=Vec4(0, 0, 0, 1))

    suitTrack = getSuitTrack(attack) # Get suit animation track
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])

    # Some suits need different calculator pos points and timing
    suitName = attack['suitName']
    if (suitName == 'nc'):
        calcPosPoints = [Point3(-0.15, 0.37, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [Point3(0.35, 0.52, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)

    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 0.000001,
                                 calcDuration, scaleUpPoint=scaleUpPoint,
                                 anim=1, propName='calculator',
                                 animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 0.9, ['duck'], showMissedExtraTime=2.2)
    soundTrack = getSoundTrack('SA_audit.mp3', delay=1.9, node=suit)

    return Parallel(suitTrack, toonTrack, calcPropTrack, soundTrack,
                    partTrack, partTrack2, partTrack3, partTrack4, partTrack5)


def doCalculate(attack): # top bc: fixed
    """ This function returns Tracks portraying the Calculate attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-one',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-plus',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-mult',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-three',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-div',
                                      color=Vec4(0, 0, 0, 1))

    suitTrack = getSuitTrack(attack) # Get suit animation track
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])

    # Some suits need different calculator pos points and timing
    suitName = attack['suitName']
    if (suitName == 'nc'):
        calcPosPoints = [Point3(-0.15, 0.37, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [Point3(0.35, 0.52, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)

    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 0.000001,
                                 calcDuration, scaleUpPoint=scaleUpPoint,
                                 anim=1, propName='calculator',
                                 animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 1.8, ['sidestep'])

    return Parallel(suitTrack, toonTrack, calcPropTrack, partTrack, partTrack2,
                    partTrack3, partTrack4, partTrack5)


def doTabulate(attack): # top bc: fixed
    """ This function returns Tracks portraying the Tabulate attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    calculator = globalPropPool.getProp('calculator')
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect, 'audit-plus',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect2 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect2, 'audit-minus',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect3 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect3, 'audit-mult',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect4 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect4, 'audit-div',
                                      color=Vec4(0, 0, 0, 1))
    particleEffect5 = BattleParticles.createParticleEffect('Calculate')
    BattleParticles.setEffectTexture(particleEffect5, 'audit-one',
                                      color=Vec4(0, 0, 0, 1))

    suitTrack = getSuitTrack(attack) # Get suit animation track
    partTrack = getPartTrack(particleEffect, 2.1, 1.9, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.2, 2.0, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 2.3, 2.1, [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, 2.4, 2.2, [particleEffect4, suit, 0])
    partTrack5 = getPartTrack(particleEffect5, 2.5, 2.3, [particleEffect5, suit, 0])

    # Some suits need different calculator pos points and timing
    suitName = attack['suitName']
    if (suitName == 'nc'):
        calcPosPoints = [Point3(-0.15, 0.37, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 0.76
        scaleUpPoint = Point3(1.1, 1.85, 1.81)
    else:
        calcPosPoints = [Point3(0.35, 0.52, 0.03), VBase3(1.352, -6.518, -6.045)]
        calcDuration = 1.87
        scaleUpPoint = Point3(1.0, 1.37, 1.31)

    calcPropTrack = getPropTrack(calculator, suit.getLeftHand(), calcPosPoints, 0.000001,
                                 calcDuration, scaleUpPoint=scaleUpPoint,
                                 anim=1, propName='calculator',
                                 animStartTime=0.5, animDuration=3.4)
    toonTrack = getToonTrack(attack, 3.2, ['conked'], 1.8, ['sidestep'])

    return Parallel(suitTrack, toonTrack, calcPropTrack, partTrack, partTrack2,
                    partTrack3, partTrack4, partTrack5)


def doCrunch(attack): # nc(a) throw, multiple props; slip-forward, flatten, slip...; sidestep
    """ This function returns Tracks portraying the Crunch attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    throwDuration = 3.03

    suitTrack = getSuitTrack(attack) # Get standard suit track
    numberNames = ['one', 'two', 'three', 'four', 'five', 'six']
    BattleParticles.loadParticles()
    numberSpill1 = BattleParticles.createParticleEffect(file='numberSpill')
    numberSpill2 = BattleParticles.createParticleEffect(file='numberSpill')
    spillTexture1 = random.choice(numberNames)
    spillTexture2 = random.choice(numberNames)
    BattleParticles.setEffectTexture(numberSpill1, 'audit-'+spillTexture1)
    BattleParticles.setEffectTexture(numberSpill2, 'audit-'+spillTexture2)
    numberSpillTrack1 = getPartTrack(numberSpill1, 1.1, 2.2,
                                     [numberSpill1, suit, 0])
    numberSpillTrack2 = getPartTrack(numberSpill2, 1.5, 1.0,
                                     [numberSpill2, suit, 0])

    numberSprayTracks = Parallel()
    numOfNumbers = random.randint(5, 9)
    for i in range(0, numOfNumbers-1):
        nextSpray = BattleParticles.createParticleEffect(file='numberSpray')
        nextTexture = random.choice(numberNames)
        BattleParticles.setEffectTexture(nextSpray, 'audit-'+nextTexture)
        nextStartTime = random.random()*0.6 + throwDuration
        nextDuration = random.random()*0.4 + 1.4
        nextSprayTrack = getPartTrack(nextSpray, nextStartTime, nextDuration,
                                       [nextSpray, suit, 0])
        numberSprayTracks.append(nextSprayTrack)

    numberTracks = Parallel()
    # First create the handful of numbers in the suit's hand
    for i in range(0, numOfNumbers):
        texture = random.choice(numberNames)
        next = MovieUtil.copyProp(BattleParticles.getParticle('audit-'+texture))
        next.reparentTo(suit.getRightHand())
        next.setScale(0.01, 0.01, 0.01)
        next.setColor(Vec4(0.0, 0.0, 0.0, 1.0))
        next.setPos(random.random()*0.6-0.3,
                     random.random()*0.6-0.3,
                     random.random()*0.6-0.3)
        next.setHpr(VBase3(-1.15, 86.58, -76.78))
        numberTrack = Sequence(
            Wait(0.9),
            LerpScaleInterval(next, 0.6, MovieUtil.PNT3_ONE),
            Wait(1.7),
            Func(MovieUtil.removeProp, next),
            )
        numberTracks.append(numberTrack)

    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.14, 0.28])
    damageAnims.append(['cringe', 0.01, 0.16, 0.3])
    damageAnims.append(['cringe', 0.01, 0.13, 0.22])
    damageAnims.append(['slip-forward', 0.01, 0.6]) #, 0.9])
    toonTrack = getToonTrack(attack, damageDelay=4.7, splicedDamageAnims=damageAnims,
                             dodgeDelay=3.6, dodgeAnimNames=['sidestep'])

    return Parallel(suitTrack, toonTrack, numberSpillTrack1,
                    numberSpillTrack2, numberTracks, numberSprayTracks)


def doLiquidate(attack): # top b(b), moneybags(c) fixed
    """ This function returns Tracks portraying the Liquidate attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    dmg = target['hp']
    toon = target['toon']
    BattleParticles.loadParticles()
    rainEffect = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect2 = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect3 = BattleParticles.createParticleEffect(file='liquidate')

    # cloud = MovieUtil.copyProp(toon.cloudActors[0])
    cloud = globalPropPool.getProp('stormcloud')
    
    suitType = getSuitBodyType(attack['suitName'])
    if (suitType == 'a'): # not used with type a
        partDelay = 0.2
        damageDelay = 3.5
        dodgeDelay = 2.45
    elif (suitType == 'b'):
        partDelay = 0.2
        damageDelay = 3.5
        dodgeDelay = 2.45
    elif (suitType == 'c'):
        partDelay = 0.2
        damageDelay = 3.5
        dodgeDelay = 2.45

    suitTrack = getSuitTrack(attack, delay=0.9)
    initialCloudHeight = suit.height + 3 # Initial cloud height set to 3 meters above suit
    cloudPosPoints = [Point3(0, 3, initialCloudHeight), VBase3(180, 0, 0)]
    # Make the storm cloud appear over and slightly in front of the suit
    cloudPropTrack = Sequence()
    cloudPropTrack.append(Func(cloud.pose, 'stormcloud', 0))
    cloudPropTrack.append(getPropAppearTrack(cloud, suit, cloudPosPoints, 0.000001,
                                         Point3(3, 3, 3), scaleUpTime=0.7))
    cloudPropTrack.append(Func(battle.movie.needRestoreRenderProp,
                                       cloud))
    cloudPropTrack.append(Func(cloud.wrtReparentTo, render))
    # Now calculate the targetPoint for the cloud to move to (right over the target toon)
    targetPoint = __toonFacePoint(toon)
    targetPoint.setZ(targetPoint[2]+3)
    # Push the cloud over to the target point (whether it hits or misses)
    cloudPropTrack.append(Wait(1.1)) # Wait to be pushed by suit
    cloudPropTrack.append(LerpPosInterval(cloud, 1, pos=targetPoint))
    # Must include particle track within cloud intervals to be safe...if the cloud is on
    # a separate track and get removed before the effect is parented, it will crash
    cloudPropTrack.append(Wait(partDelay)) # Wait before rain falls from cloud

    cloudPropTrack.append(Parallel(
        Sequence(ParticleInterval(rainEffect, cloud, worldRelative=0,
                                  duration=2.1, cleanup = True)),
        Sequence(Wait(0.1),
                 ParticleInterval(rainEffect2, cloud,
                                  worldRelative=0, duration=2.0, cleanup = True)),
        Sequence(Wait(0.1),
                 ParticleInterval(rainEffect3, cloud,
                                  worldRelative=0, duration=2.0, cleanup = True)),
        Sequence(ActorInterval(cloud, 'stormcloud', startTime=3,
                               duration=0.1),
                 ActorInterval(cloud, 'stormcloud', startTime=1,
                               duration=2.3)),
        ))

    cloudPropTrack.append(Wait(0.4)) # Wait a moment before cloud goes away
    cloudPropTrack.append(LerpScaleInterval(cloud, 0.5,
                                             MovieUtil.PNT3_NEARZERO))
    # The particle effect has already been cleaned up, it's safe to remove the cloud
    cloudPropTrack.append(Func(MovieUtil.removeProp, cloud))
    cloudPropTrack.append(Func(battle.movie.clearRenderProp, cloud))

    damageAnims = [['melt'], ['jump', 1.5, 0.4]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'])
    soundTrack = getSoundTrack('SA_liquidate.mp3', delay=2.0, node=suit)

    # If toon is hit, need puddle for it to melt in
    if (dmg > 0):
        puddle = globalPropPool.getProp('quicksand')
        puddle.setColor(Vec4(0.0, 0.0, 1.0, 1))
        puddle.setHpr(Point3(120, 0, 0))
        puddle.setScale(0.01)
        puddleTrack = Sequence(
            Func(battle.movie.needRestoreRenderProp, puddle),
            Wait(damageDelay-0.7),
            Func(puddle.reparentTo, battle),
            Func(puddle.setPos, toon.getPos(battle)),
            LerpScaleInterval(puddle, 1.7, Point3(1.7, 1.7, 1.7),
                              startScale=MovieUtil.PNT3_NEARZERO),
            Wait(3.2),
            LerpFunctionInterval(puddle.setAlphaScale, fromData=1, toData=0, duration=0.8),
            Func(MovieUtil.removeProp, puddle),
            Func(battle.movie.clearRenderProp, puddle),
            )
        return Parallel(suitTrack, toonTrack, cloudPropTrack, soundTrack,
                        puddleTrack)
    else:
        return Parallel(suitTrack, toonTrack, cloudPropTrack, soundTrack)


def doMarketCrash(attack): # mb(c) fixed
    """ This function returns Tracks portraying the Market Crash attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    suitDelay = 1.32
    propDelay = 0.6
    throwDuration = 1.5
    paper = globalPropPool.getProp('newspaper')

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(-0.07, 0.17, -0.13), VBase3(161.867, -33.149, -48.086)]
    paperTrack = Sequence(
        getPropAppearTrack(paper, suit.getRightHand(), posPoints, propDelay,
                           Point3(3, 3, 3), scaleUpTime=0.5))
    paperTrack.append(Wait(suitDelay)) # Wait while suit animates

    hitPoint = toon.getPos(battle)
    hitPoint.setX(hitPoint.getX() + 1.2)
    hitPoint.setY(hitPoint.getY() + 1.5)
    # If paper hits toon, should sit on top, not pass through
    if (dmg > 0):
        hitPoint.setZ(hitPoint.getZ() + 1.1)
    # We push the paper back as it scale down
    movePoint = Point3(hitPoint.getX(), hitPoint.getY()-1.8, hitPoint.getZ()+0.2)

    paperTrack.append(Func(battle.movie.needRestoreRenderProp, paper))
    paperTrack.append(Func(paper.wrtReparentTo, battle))
    paperTrack.append(getThrowTrack(paper, hitPoint, duration=throwDuration, parent=battle))
    paperTrack.append(Wait(0.6))
    paperTrack.append(LerpPosInterval(paper, 0.4, movePoint))

    # Add in a track to spin the paper as it is tossed, and make it get larger
    spinTrack = Sequence(
        Wait(propDelay+suitDelay+0.2),
        LerpHprInterval(paper, throwDuration, Point3(-360, 0, 0)),
        )
    sizeTrack = Sequence(
        Wait(propDelay+suitDelay+0.2),
        LerpScaleInterval(paper, throwDuration, Point3(6, 6, 6)),
        Wait(0.95),
        LerpScaleInterval(paper, 0.4, MovieUtil.PNT3_NEARZERO),
        )
    propTrack = Sequence(
        Parallel(paperTrack, spinTrack, sizeTrack),
        Func(MovieUtil.removeProp, paper),
        Func(battle.movie.clearRenderProp, paper),
        )

    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.21, 0.08])
    damageAnims.append(['slip-forward', 0.01, 0.6, 0.85])
    damageAnims.extend(getSplicedLerpAnims('slip-forward', 0.31, 0.95, startTime=1.2))
    damageAnims.append(['slip-forward', 0.01, 1.51])
    toonTrack = getToonTrack(attack, damageDelay=3.8, splicedDamageAnims=damageAnims,
                             dodgeDelay=2.4, dodgeAnimNames=['sidestep'],
                             showDamageExtraTime=0.4, showMissedExtraTime=1.3)

    return Parallel(suitTrack, toonTrack, propTrack)


def doBite(attack): # ls(b) throw; conked; duck
    """ This function returns Tracks portraying the Bite attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    teeth = globalPropPool.getProp('teeth')
    propDelay = 0.8
    propScaleUpTime = 0.5
    suitDelay = 1.73
    throwDelay = propDelay + propScaleUpTime + suitDelay
    throwDuration = 0.4

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(-0.05, 0.41, -0.54), VBase3(4.465, -3.563, 51.479)]

    teethAppearTrack = Sequence(
        getPropAppearTrack(teeth, suit.getRightHand(), posPoints, propDelay,
                           Point3(3, 3, 3), scaleUpTime=propScaleUpTime))
    teethAppearTrack.append(Wait(suitDelay)) # Wait while suit animates
    teethAppearTrack.append(Func(battle.movie.needRestoreRenderProp, teeth))
    teethAppearTrack.append(Func(teeth.wrtReparentTo, battle))

    if (dmg > 0): # If strikes toon, fly to its face
        x = toon.getX(battle)
        y = toon.getY(battle)
        z = toon.getZ(battle)
        toonHeight = z + toon.getHeight()
        flyPoint = Point3(x, y + 2.7, toonHeight*0.8)

        teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
        # Chatter the teeth, then open them wide, pull them back as they rev up, then
        # chomp the toon's head
        teethAppearTrack.append(LerpPosInterval(teeth, 0.4, pos=Point3(x, y+3.2, toonHeight*0.7)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.3, pos=Point3(x, y+4.7, toonHeight*0.5)))
        teethAppearTrack.append(Wait(0.2))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y-0.2, toonHeight*0.9)))
        teethAppearTrack.append(Wait(0.4))

        scaleTrack = Sequence(
            Wait(throwDelay),
            LerpScaleInterval(teeth, throwDuration, Point3(8, 8, 8)),
            Wait(0.9),
            LerpScaleInterval(teeth, 0.2, Point3(14, 14, 14)),
            Wait(1.2),
            LerpScaleInterval(teeth, 0.3, MovieUtil.PNT3_NEARZERO),
            )
        hprTrack = Sequence(
            Wait(throwDelay),
            LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
            Wait(0.2),
            LerpHprInterval(teeth, 0.4, Point3(180, -35, 0), startHpr=Point3(180, 0, 0)),
            Wait(0.6),
            LerpHprInterval(teeth, 0.1, Point3(180, -75, 0), startHpr=Point3(180, -35, 0)),
            )
        animTrack = Sequence(
            Wait(throwDelay),
            ActorInterval(teeth, 'teeth', duration=throwDuration),
            ActorInterval(teeth, 'teeth', duration=0.3),
            Func(teeth.pose, 'teeth', 1),
            Wait(0.7),
            ActorInterval(teeth, 'teeth', duration=0.9),
            )

        propTrack = Sequence(
            Parallel(teethAppearTrack, scaleTrack, hprTrack, animTrack),
            Func(MovieUtil.removeProp, teeth),
            Func(battle.movie.clearRenderProp, teeth),
            )
    else: # Else fly past the toon
        flyPoint = __toonFacePoint(toon, parent=battle)
        flyPoint.setY(flyPoint.getY() - 7.1)
        teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
        teethAppearTrack.append(Func(MovieUtil.removeProp, teeth))
        teethAppearTrack.append(Func(battle.movie.clearRenderProp, teeth))
        propTrack = teethAppearTrack

    damageAnims = [['cringe', 0.01, 0.7, 1.2],
                    ['conked', 0.01, 0.2, 2.1],
                    ['conked', 0.01, 3.2],]
    dodgeAnims = [['cringe', 0.01, 0.7, 0.2],
                   ['duck', 0.01, 1.6],]
    toonTrack = getToonTrack(attack, damageDelay=3.2, splicedDamageAnims=damageAnims,
                             dodgeDelay=2.9, splicedDodgeAnims=dodgeAnims,
                             showDamageExtraTime=2.4)

    return Parallel(suitTrack, toonTrack, propTrack)


def doChomp(attack): # ls(b) throw; slip-backward; sidestep
    """ This function returns Tracks portraying the Chomp attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    teeth = globalPropPool.getProp('teeth')
    propDelay = 0.8
    propScaleUpTime = 0.5
    suitDelay = 1.73
    throwDelay = propDelay + propScaleUpTime + suitDelay
    throwDuration = 0.4

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(-0.05, 0.41, -0.54), VBase3(4.465, -3.563, 51.479)]

    teethAppearTrack = Sequence(
        getPropAppearTrack(teeth, suit.getRightHand(), posPoints, propDelay,
                           Point3(3, 3, 3), scaleUpTime=propScaleUpTime))
    teethAppearTrack.append(Wait(suitDelay)) # Wait while suit animates
    teethAppearTrack.append(Func(battle.movie.needRestoreRenderProp, teeth))
    teethAppearTrack.append(Func(teeth.wrtReparentTo, battle))

    if (dmg > 0): # If strikes toon, fly to its face
        x = toon.getX(battle)
        y = toon.getY(battle)
        z = toon.getZ(battle)
        toonHeight = z + toon.getHeight()
        flyPoint = Point3(x, y + 2.7, toonHeight*0.7)

        teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
        # Chatter the teeth, then open them wide, pull them back as they rev up, then
        # chomp the toon's head
        teethAppearTrack.append(LerpPosInterval(teeth, 0.4, pos=Point3(x, y+3.2, toonHeight*0.7)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.3, pos=Point3(x, y+4.7, toonHeight*0.5)))
        teethAppearTrack.append(Wait(0.2))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y, toonHeight+3)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y-1.2, toonHeight*0.7)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.1, pos=Point3(x, y-0.7, toonHeight*0.4)))
        teethAppearTrack.append(Wait(0.4))

        scaleTrack = Sequence(
            Wait(throwDelay),
            LerpScaleInterval(teeth, throwDuration, Point3(6, 6, 6)),
            Wait(0.9),
            LerpScaleInterval(teeth, 0.2, Point3(10, 10, 10)),
            Wait(1.2),
            LerpScaleInterval(teeth, 0.3, MovieUtil.PNT3_NEARZERO),
            )
        hprTrack = Sequence(
            Wait(throwDelay),
            LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
            Wait(0.2),
            LerpHprInterval(teeth, 0.4, Point3(180, -35, 0), startHpr=Point3(180, 0, 0)),
            Wait(0.6),
            LerpHprInterval(teeth, 0.1, Point3(0, -35, 0), startHpr=Point3(180, -35, 0)),
            )
        animTrack = Sequence(
            Wait(throwDelay),
            ActorInterval(teeth, 'teeth', duration=throwDuration),
            ActorInterval(teeth, 'teeth', duration=0.3),
            Func(teeth.pose, 'teeth', 1),
            Wait(0.7),
            ActorInterval(teeth, 'teeth', duration=0.9),
            )

        propTrack = Sequence(
            Parallel(teethAppearTrack, scaleTrack, hprTrack, animTrack),
            Func(MovieUtil.removeProp, teeth),
            Func(battle.movie.clearRenderProp, teeth),
            )
    else: # Else fly past the toon
        x = toon.getX(battle)
        y = toon.getY(battle)
        z = toon.getZ(battle)
        z = z + 0.2
        flyPoint = Point3(x, y - 2.1, z)
        teethAppearTrack.append(LerpPosInterval(teeth, throwDuration, pos=flyPoint))
        teethAppearTrack.append(Wait(0.2))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x+0.5, y-2.5, z)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x+1.0, y-3.0, z+0.4)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x+1.3, y-3.6, z)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x+0.9, y-3.1, z+0.4)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x+0.3, y-2.6, z)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x-0.1, y-2.2, z+0.4)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x-0.4, y-1.9, z)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x-0.7, y-2.1, z+0.4)))
        teethAppearTrack.append(LerpPosInterval(teeth, 0.2, pos=Point3(x-0.8, y-2.3, z)))
        teethAppearTrack.append(LerpScaleInterval(teeth, 0.6, MovieUtil.PNT3_NEARZERO))

        hprTrack = Sequence(
            Wait(throwDelay),
            LerpHprInterval(teeth, 0.3, Point3(180, 0, 0)),
            Wait(0.5),
            LerpHprInterval(teeth, 0.4, Point3(80, 0, 0), startHpr=Point3(180, 0, 0)),
            LerpHprInterval(teeth, 0.8, Point3(-10, 0, 0), startHpr=Point3(80, 0, 0)),
            )
        animTrack = Sequence(Wait(throwDelay),
                             ActorInterval(teeth, 'teeth', duration=3.6))

        propTrack = Sequence(
            Parallel(teethAppearTrack, hprTrack, animTrack),
            Func(MovieUtil.removeProp, teeth),
            Func(battle.movie.clearRenderProp, teeth),
            )

    damageAnims = [['cringe', 0.01, 0.7, 1.2],
                    ['spit', 0.01, 2.95, 1.47],
                    ['spit', 0.01, 4.42, 0.07],
                    ['spit', 0.08, 4.49, -0.07],
                    ['spit', 0.08, 4.42, 0.07],
                    ['spit', 0.08, 4.49, -0.07],
                    ['spit', 0.08, 4.42, 0.07],
                    ['spit', 0.08, 4.49, -0.07],
                    ['spit', 0.01, 4.42],]
    dodgeAnims = [['jump', 0.01, 0.01],]
    toonTrack = getToonTrack(attack, damageDelay=3.2, splicedDamageAnims=damageAnims,
                             dodgeDelay=2.75, splicedDodgeAnims=dodgeAnims,
                             showDamageExtraTime=1.4)

    return Parallel(suitTrack, toonTrack, propTrack)


"""
def doFiveOClockShadow(attack): # throw; slip-forward; jump
    pass #later
"""

def doEvictionNotice(attack): # top b: fixed
    """ This function returns Tracks portraying the Eviction-Notice attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    paper = globalPropPool.getProp('shredder-paper') # Get prop from pool

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(-0.04, 0.15, -1.38), VBase3(10.584, -11.945, 18.316)]
    # Now make paper appear
    propTrack = Sequence(
        getPropAppearTrack(paper, suit.getRightHand(), posPoints, 0.8,
                           MovieUtil.PNT3_ONE, scaleUpTime=0.5))
    propTrack.append(Wait(1.73)) # Wait while suit animates
    hitPoint = __toonFacePoint(toon, parent=battle)
    hitPoint.setX(hitPoint.getX() - 1.4)
    missPoint = __toonGroundPoint(attack, toon, 0.7, parent=battle)
    missPoint.setX(missPoint.getX() - 1.1)
    propTrack.append(getPropThrowTrack(attack, paper, [hitPoint],
                                       [missPoint], parent=battle))

    # Toon jumps to dodge so don't need friend toon dodge tracks
    toonTrack = getToonTrack(attack, 3.4, ['conked'], 2.8, ['jump'])

    return Parallel(suitTrack, toonTrack, propTrack)


def doWithdrawal(attack): # top b: improve: turn white
    """ This function returns Tracks portraying the Withdrawal attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect('Withdrawal')
    BattleParticles.setEffectTexture(particleEffect, 'snow-particle')

    suitTrack = getSuitAnimTrack(attack) # Get suit animation track
    partTrack = getPartTrack(particleEffect, 0.00001, suitTrack.getDuration()+1.2,
                              [particleEffect, suit, 0])
    # Toon jumps to dodge so don't need friend toon dodge tracks

    toonTrack = getToonTrack(attack, 1.2, ['cringe'], 0.2,
                             splicedDodgeAnims=[['duck', 0.00001, 0.8]],
                             showMissedExtraTime=0.8)

    # Now create a track to change the toon's color if hit (burned), but we must
    # extract the individual parts and change their color since some particle effects
    # are parented to the toon and would be changed as well
    headParts = toon.getHeadParts()
    torsoParts = toon.getTorsoParts()
    legsParts = toon.getLegsParts()

    def changeColor(parts): # Function to change each lod part in list parts
         track = Parallel()
         for partNum in range(0, parts.getNumPaths()):
              nextPart = parts.getPath(partNum)
              track.append(Func(nextPart.setColorScale,
                                             Vec4(0, 0, 0, 1)))
#              track.append(LerpFunctionInterval(nextPart.setAllColorScale,
#                            fromData = 1, toData = 0, duration=0.7))
         return track

    def resetColor(parts): # Reset the color of each lod part
         track = Parallel()
         for partNum in range(0, parts.getNumPaths()):
              nextPart = parts.getPath(partNum)
              track.append(Func(nextPart.clearColorScale))
         return track

    soundTrack = getSoundTrack('SA_withdrawl.mp3', delay=1.4, node=suit)

    if (dmg > 0): # If takes damage, change color
        colorTrack = Sequence()
        colorTrack.append(Wait(1.6)) # Wait before changing the color
        colorTrack.append(Func(battle.movie.needRestoreColor))
        colorTrack.append(Parallel(changeColor(headParts),
                                   changeColor(torsoParts),
                                   changeColor(legsParts)))

        colorTrack.append(Wait(2.9)) # Wait while color changed
        colorTrack.append(resetColor(headParts))
        colorTrack.append(resetColor(torsoParts))
        colorTrack.append(resetColor(legsParts))
        colorTrack.append(Func(battle.movie.clearRestoreColor))
        return Parallel(suitTrack, partTrack, toonTrack, soundTrack, colorTrack)
    else:
        return Parallel(suitTrack, partTrack, toonTrack, soundTrack)


def doJargon(attack): # top dt(a): fixed
    """ This function returns Tracks portraying the Jargon attack """
    suit = attack['suit']
    battle = attack['battle']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect2 = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect3 = BattleParticles.createParticleEffect(file='jargonSpray')
    particleEffect4 = BattleParticles.createParticleEffect(file='jargonSpray')
    BattleParticles.setEffectTexture(particleEffect, 'jargon-brow',
                                      color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'jargon-deep',
                                      color=Vec4(0, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect3, 'jargon-hoop',
                                      color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect4, 'jargon-ipo',
                                      color=Vec4(0, 0, 0, 1))

    damageDelay = 2.2 # was 2.4 w/ finger-wag
    dodgeDelay = 1.5 # was 1.9 w/ finger-wag
    partDelay = 1.1 # was 1.5 w/ finger-wag
    partInterval = 1.2 # was 0.2 w/ finger-wag

    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, partDelay+(partInterval*0), 2,
                              [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, partDelay+(partInterval*1), 2,
                               [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, partDelay+(partInterval*2), 2,
                               [particleEffect3, suit, 0])
    partTrack4 = getPartTrack(particleEffect4, partDelay+(partInterval*3), 1.0,
                               [particleEffect4, suit, 0])

    damageAnims = []
    damageAnims.append(['conked', 0.0001, 0, 0.4])
    damageAnims.append(['conked', 0.0001, 2.7, 0.85])
    damageAnims.append(['conked', 0.0001, 0.4, 0.09])
    damageAnims.append(['conked', 0.0001, 0.4, 0.09])
    damageAnims.append(['conked', 0.0001, 0.4, 0.66])
    damageAnims.append(['conked', 0.0001, 0.4, 0.09])
    damageAnims.append(['conked', 0.0001, 0.4, 0.09])
    damageAnims.append(['conked', 0.0001, 0.4, 0.86])
    damageAnims.append(['conked', 0.0001, 0.4, 0.14])
    damageAnims.append(['conked', 0.0001, 0.4, 0.14])
    damageAnims.append(['conked', 0.0001, 0.4])
    dodgeAnims = [['duck', 0.0001, 1.2], ['duck', 0.0001, 1.3]]
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, splicedDodgeAnims=dodgeAnims,
                             showMissedExtraTime=1.6, showDamageExtraTime=0.7)
    soundTrack = getSoundTrack('SA_jargon.mp3', delay=2.1, node=suit)

    return Parallel(suitTrack, toonTrack, soundTrack,
                    partTrack, partTrack2, partTrack3, partTrack4)


def doMumboJumbo(attack): # top dt: fixed
    """ This function returns Tracks portraying the MumboJumbo attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    BattleParticles.loadParticles()
    particleEffect = BattleParticles.createParticleEffect(file='mumboJumboSpray')
    particleEffect2 = BattleParticles.createParticleEffect(file='mumboJumboSpray')
    particleEffect3 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    particleEffect4 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    particleEffect5 = BattleParticles.createParticleEffect(file='mumboJumboSmother')
    BattleParticles.setEffectTexture(particleEffect, 'mumbojumbo-boiler',
                                      color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect2, 'mumbojumbo-creative',
                                      color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect3, 'mumbojumbo-deben',
                                      color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect4, 'mumbojumbo-high',
                                      color=Vec4(1, 0, 0, 1))
    BattleParticles.setEffectTexture(particleEffect5, 'mumbojumbo-iron',
                                      color=Vec4(1, 0, 0, 1))

    suitTrack = getSuitTrack(attack)
    partTrack = getPartTrack(particleEffect, 2.5, 2, [particleEffect, suit, 0])
    partTrack2 = getPartTrack(particleEffect2, 2.5, 2, [particleEffect2, suit, 0])
    partTrack3 = getPartTrack(particleEffect3, 3.3, 1.7, [particleEffect3, toon, 0])
    partTrack4 = getPartTrack(particleEffect4, 3.3, 1.7, [particleEffect4, toon, 0])
    partTrack5 = getPartTrack(particleEffect5, 3.3, 1.7, [particleEffect5, toon, 0])

    toonTrack = getToonTrack(attack, 3.2, ['cringe'], 2.2, ['sidestep'])
    soundTrack = getSoundTrack('SA_mumbo_jumbo.mp3', delay=2.5, node=suit)

    if (dmg > 0):
        return Parallel(suitTrack, toonTrack, soundTrack, partTrack,
                        partTrack2, partTrack3, partTrack4, partTrack5)
    else:
        return Parallel(suitTrack, toonTrack, soundTrack, partTrack, partTrack2)


def doGuiltTrip(attack): # bs(a) fixed
    """ This function returns Tracks portraying the Guilt Trip attack """
    suit = attack['suit']
    battle = attack['battle']

    # Set up all the particle effects, colors, and positions
    centerColor = Vec4(1.0, 0.2, 0.2, 0.9)
    edgeColor = Vec4(0.9, 0.9, 0.9, 0.4)
    powerBar1 = BattleParticles.createParticleEffect(file='guiltTrip')
    powerBar2 = BattleParticles.createParticleEffect(file='guiltTrip')
    powerBar1.setPos(0, 6.1, 0.4)
    powerBar1.setHpr(-90, 0, 0)
    powerBar2.setPos(0, 6.1, 0.4)
    powerBar2.setHpr(90, 0, 0)
    powerBar1.setScale(5)
    powerBar2.setScale(5)
    powerBar1Particles = powerBar1.getParticlesNamed('particles-1')
    powerBar2Particles = powerBar2.getParticlesNamed('particles-1')
    powerBar1Particles.renderer.setCenterColor(centerColor)
    powerBar1Particles.renderer.setEdgeColor(edgeColor)
    powerBar2Particles.renderer.setCenterColor(centerColor)
    powerBar2Particles.renderer.setEdgeColor(edgeColor)
    waterfallEffect = BattleParticles.createParticleEffect('Waterfall')
    waterfallEffect.setScale(11)
    waterfallParticles = waterfallEffect.getParticlesNamed('particles-1')
    waterfallParticles.renderer.setCenterColor(centerColor)
    waterfallParticles.renderer.setEdgeColor(edgeColor)

    suitTrack = getSuitAnimTrack(attack) # Get suit animation track

    def getPowerTrack(effect, suit=suit, battle=battle):
        partTrack = Sequence(
            Wait(0.7),
            Func(battle.movie.needRestoreParticleEffect, effect),
            Func(effect.start, suit),
            Wait(0.4),
            LerpPosInterval(effect, 1.0, Point3(0, 15, 0.4)),
            LerpFunctionInterval(effect.setAlphaScale, fromData=1,
                                 toData=0, duration=0.4),
            Func(effect.cleanup),
            Func(battle.movie.clearRestoreParticleEffect, effect),
            )
        return partTrack
    partTrack1 = getPowerTrack(powerBar1)
    partTrack2 = getPowerTrack(powerBar2)
    waterfallTrack = getPartTrack(waterfallEffect, 0.6, 0.6,
                                   [waterfallEffect, suit, 0])

    toonTracks = getToonTracks(attack, 1.5, ['slip-forward'], 0.86, ['jump'])
    soundTrack = getSoundTrack('SA_guilt_trip.mp3', delay=1.1, node=suit)

    return Parallel(suitTrack, partTrack1, partTrack2, soundTrack,
                    waterfallTrack, toonTracks)


def doRestrainingOrder(attack): # bs(a) throw; conked, bound; sidestep
    """ This function returns Tracks portraying the Restraining-Order attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    paper = globalPropPool.getProp('shredder-paper')

    suitTrack = getSuitTrack(attack) # Get standard suit track
    posPoints = [Point3(-0.04, 0.15, -1.38), VBase3(10.584, -11.945, 18.316)]
    # Now make paper appear
    propTrack = Sequence(
        getPropAppearTrack(paper, suit.getRightHand(), posPoints, 0.8,
                           MovieUtil.PNT3_ONE, scaleUpTime=0.5))
    propTrack.append(Wait(1.73)) # Wait while suit animates
    hitPoint = __toonFacePoint(toon, parent=battle)
    hitPoint.setX(hitPoint.getX() - 1.4)
    missPoint = __toonGroundPoint(attack, toon, 0.7, parent=battle)
    missPoint.setX(missPoint.getX() - 1.1)
    propTrack.append(getPropThrowTrack(attack, paper, [hitPoint],
                                       [missPoint], parent=battle))

    damageAnims = [['conked', 0.01, 0.3, 0.2], ['struggle', 0.01, 0.2]]
    toonTrack = getToonTrack(attack, damageDelay=3.4, splicedDamageAnims=damageAnims,
                             dodgeDelay=2.8, dodgeAnimNames=['sidestep'])

    if (dmg > 0): # If takes damage, paper sprays over the toon
        restraintCloud = BattleParticles.createParticleEffect(file='restrainingOrderCloud')
        restraintCloud.setPos(hitPoint.getX(), hitPoint.getY()+0.5, hitPoint.getZ())
        cloudTrack = getPartTrack(restraintCloud, 3.5, 0.2, [restraintCloud, battle, 0])
        return Parallel(suitTrack, cloudTrack, toonTrack, propTrack)
    else:
        return Parallel(suitTrack, toonTrack, propTrack)


def doSpin(attack): # sd(b) fixed
    """ This function returns Tracks portraying the Spin attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    damageDelay = 1.7

    sprayEffect = BattleParticles.createParticleEffect(file='spinSpray')
    spinEffect1 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect2 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect3 = BattleParticles.createParticleEffect(file='spinEffect')
    spinEffect1.reparentTo(toon)
    spinEffect2.reparentTo(toon)
    spinEffect3.reparentTo(toon)

    # To add to the randomness of the spinning effects, tinker with the numbers
    height1 = toon.getHeight() * (random.random()*0.2 + 0.7) # from 0.7-0.9
    height2 = toon.getHeight() * (random.random()*0.2 + 0.4) # from 0.4-0.6
    height3 = toon.getHeight() * (random.random()*0.2 + 0.1) # from 0.1-0.3
    spinEffect1.setPos(0.8, -0.7, height1)
    spinEffect1.setHpr(0, 0, -random.random()*10-85)
    spinEffect1.setHpr(spinEffect1, 0, 50, 0)
    spinEffect2.setPos(0.8, -0.7, height2)
    spinEffect2.setHpr(0, 0, -random.random()*10-85)
    spinEffect2.setHpr(spinEffect2, 0, 50, 0)
    spinEffect3.setPos(0.8, -0.7, height3)
    spinEffect3.setHpr(0, 0, -random.random()*10-85)
    spinEffect3.setHpr(spinEffect3, 0, 50, 0)
    spinEffect1.wrtReparentTo(battle)
    spinEffect2.wrtReparentTo(battle)
    spinEffect3.wrtReparentTo(battle)
    

    suitTrack = getSuitTrack(attack) # Get suit animation track
    sprayTrack = getPartTrack(sprayEffect, 1.0, 1.9, [sprayEffect, suit, 0])
    spinTrack1 = getPartTrack(spinEffect1, 2.1, 3.9, [spinEffect1, battle, 0])
    spinTrack2 = getPartTrack(spinEffect2, 2.1, 3.9, [spinEffect2, battle, 0])
    spinTrack3 = getPartTrack(spinEffect3, 2.1, 3.9, [spinEffect3, battle, 0])

    damageAnims = []
    damageAnims.append(['duck', 0.01, 0.01, 1.1])
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.1, startTime=2.26))
    damageAnims.extend(getSplicedLerpAnims('think', 0.66, 1.1, startTime=2.26))
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=0.91, dodgeAnimNames=['sidestep'],
                             showDamageExtraTime=2.1, showMissedExtraTime=1.0)

    if (dmg > 0): # use the spinning particle effects
        # Create the track to spin the toon around
        toonSpinTrack = Sequence(
            Wait(damageDelay+0.9),
            LerpHprInterval(toon, 0.7, Point3(-10, 0, 0)),
            LerpHprInterval(toon, 0.5, Point3(-30, 0, 0)),
            LerpHprInterval(toon, 0.2, Point3(-60, 0, 0)),
            LerpHprInterval(toon, 0.7, Point3(-700, 0, 0)),
            LerpHprInterval(toon, 1.0, Point3(-1310, 0, 0)),
            LerpHprInterval(toon, 0.4, toon.getHpr()),
            Wait(0.5),
            )
        return Parallel(suitTrack, sprayTrack, toonTrack, toonSpinTrack,
                        spinTrack1, spinTrack2, spinTrack3)
    else:
        return Parallel(suitTrack, sprayTrack, toonTrack)


def doLegalese(attack): # le(a) fixed
    """ This function returns Tracks portraying the Legalese attack """
    suit = attack['suit']

    BattleParticles.loadParticles()
    sprayEffect1 = BattleParticles.createParticleEffect(file='legaleseSpray')
    sprayEffect2 = BattleParticles.createParticleEffect(file='legaleseSpray')
    sprayEffect3 = BattleParticles.createParticleEffect(file='legaleseSpray')
    color = Vec4(0.4, 0, 0, 1)
    BattleParticles.setEffectTexture(sprayEffect1, 'legalese-hc', color=color)
    BattleParticles.setEffectTexture(sprayEffect2, 'legalese-qpq', color=color)
    BattleParticles.setEffectTexture(sprayEffect3, 'legalese-vd', color=color)

    partDelay = 1.3
    partDuration = 1.15
    damageDelay = 1.9
    dodgeDelay = 1.1

    suitTrack = getSuitTrack(attack)
    sprayTrack1 = getPartTrack(sprayEffect1, partDelay, partDuration,
                               [sprayEffect1, suit, 0])
    sprayTrack2 = getPartTrack(sprayEffect2, partDelay+0.8, partDuration,
                                [sprayEffect2, suit, 0])
    sprayTrack3 = getPartTrack(sprayEffect3, partDelay+1.6, partDuration,
                                [sprayEffect3, suit, 0])

    damageAnims = []
    damageAnims.append(['cringe', 0.00001, 0.3, 0.8])
    damageAnims.append(['cringe', 0.00001, 0.3, 0.8])
    damageAnims.append(['cringe', 0.00001, 0.3])
    # Damage animation is toon cringing as gets hit then, then falls to the floor
    toonTrack = getToonTrack(attack, damageDelay=damageDelay, splicedDamageAnims=damageAnims,
                             dodgeDelay=dodgeDelay, dodgeAnimNames=['sidestep'],
                             showMissedExtraTime=0.8)

    return Parallel(suitTrack, toonTrack, sprayTrack1, sprayTrack2, sprayTrack3)


def doPeckingOrder(attack): # throw, multiple props; duck; sidestep
    """ This function returns Tracks portraying the Pecking Order attack """
    suit = attack['suit']
    battle = attack['battle']
    target = attack['target']
    toon = target['toon']
    dmg = target['hp']
    throwDuration = 3.03
    throwDelay = 3.2

    suitTrack = getSuitTrack(attack) # Get standard suit track

    numBirds = random.randint(4, 7)
    birdTracks = Parallel()
    propDelay = 1.5
    for i in range(0, numBirds):
        next = globalPropPool.getProp('bird')
        next.setScale(0.01)
        next.reparentTo(suit.getRightHand())
        next.setPos(random.random()*0.6-0.3,
                     random.random()*0.6-0.3,
                     random.random()*0.6-0.3)

        if (dmg > 0): # If toon takes damage, hit face, otherwise go farther
            hitPoint = Point3(random.random()*5-2.5,
                               random.random()*2-1 - 6,
                               random.random()*3-1.5 + toon.getHeight() - 0.9,)
        else:
            hitPoint = Point3(random.random()*2-1,
                               random.random()*4-2 - 15,
                               random.random()*4-2 + 2.2,)

        birdTrack = Sequence(
            Wait(throwDelay),
            Func(battle.movie.needRestoreRenderProp, next),
            Func(next.wrtReparentTo, battle),
            Func(next.setHpr, Point3(90, 20, 0)),
            LerpPosInterval(next, 1.1, hitPoint),
            )

        scaleTrack = Sequence(
            Wait(throwDelay),
            LerpScaleInterval(next, 0.15, Point3(9, 9, 9)),
            )

        birdTracks.append(Sequence(
            Parallel(birdTrack, scaleTrack),
            Func(MovieUtil.removeProp, next),
            ))


    damageAnims = []
    damageAnims.append(['cringe', 0.01, 0.14, 0.21])
    damageAnims.append(['cringe', 0.01, 0.14, 0.13])
    damageAnims.append(['cringe', 0.01, 0.43])
    toonTrack = getToonTrack(attack, damageDelay=4.2, splicedDamageAnims=damageAnims,
                             dodgeDelay=2.8, dodgeAnimNames=['sidestep'],
                             showMissedExtraTime=1.1)

    return Parallel(suitTrack, toonTrack, birdTracks)


"""
def doGavel(attack): # project; slip-backward; sidestep
    pass #later

def doThrowBook(attack): # throw; conked; sidestep
    pass #later
"""

############
# End Revamped attacks using sub functions defined above.
############

