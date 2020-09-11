from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from toontown.suit.SuitBase import *
from toontown.toon.ToonDNA import *
from BattleSounds import *

import MovieCamera
from direct.directnotify import DirectNotifyGlobal
import MovieUtil
from toontown.toonbase import ToontownBattleGlobals
import BattleParticles
import BattleProps
import MovieNPCSOS

notify = DirectNotifyGlobal.directNotify.newCategory('MovieLures')

def safeWrtReparentTo(nodePath, parent):
    if nodePath and not nodePath.isEmpty():
        nodePath.wrtReparentTo(parent)

def doLures(lures):
    """ doLures(lures)
        Lures occur in the following order:
        1) level 1 lures one at a time, from right to left
        2) level 2 lures one at a time, from right to left
        etc.
    """
    if (len(lures) == 0):
        return (None, None)

    npcArrivals, npcDepartures, npcs = MovieNPCSOS.doNPCTeleports(lures)

    mtrack = Parallel()
    for l in lures:
        ival = __doLureLevel(l, npcs)
        if (ival):
            mtrack.append(ival)

    lureTrack = Sequence(npcArrivals, mtrack, npcDepartures)

    camDuration = mtrack.getDuration()
    enterDuration = npcArrivals.getDuration()
    exitDuration = npcDepartures.getDuration()
    camTrack = MovieCamera.chooseLureShot(lures, camDuration, enterDuration,
                                                              exitDuration)
    return (lureTrack, camTrack)

def __doLureLevel(lure, npcs):
    """ __doLureLevel(lure)
    """
    level = lure['level']
    if (level == 0):
        return __lureOneDollar(lure)
    elif (level == 1):
        return __lureSmallMagnet(lure)
    elif (level == 2):
        return __lureFiveDollar(lure)
    elif (level == 3):
        return __lureLargeMagnet(lure)
    elif (level == 4):
        return __lureTenDollar(lure)
    elif (level == 5):
        return __lureHypnotize(lure, npcs)
    elif (level == 6):
        return __lureSlideshow(lure, npcs) #UBER
    return None

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


def __createFishingPoleMultiTrack(lure, dollar, dollarName):
    toon = lure['toon']
    target = lure['target']
    battle = lure['battle']
    sidestep = lure['sidestep']
    hp = target['hp']
    kbbonus = target['kbbonus']
    suit = target['suit']
    targetPos = suit.getPos(battle)
    died = target['died']
    revived = target['revived']
    reachAnimDuration = 3.5
    trapProp = suit.battleTrapProp
    pole = globalPropPool.getProp('fishing-pole')
    pole2 = MovieUtil.copyProp(pole)
    poles = [pole, pole2]
    hands = toon.getRightHands()
    def positionDollar(dollar, suit):
        dollar.reparentTo(suit)
        dollar.setPos(0, MovieUtil.SUIT_LURE_DOLLAR_DISTANCE, 0)

    dollarTrack = Sequence(
        Func(positionDollar, dollar, suit),
        Func(dollar.wrtReparentTo, battle),
        ActorInterval(dollar, dollarName, duration=3),
        # Slowly lower dollar in front of the suit
        getSplicedLerpAnimsTrack(dollar, dollarName, 0.7, 2.0, startTime=3),
        # Quickly rip the dollar away before the suit has a change to grab it
        LerpPosInterval(dollar, 0.2, Point3(0, -10, 7)),
        Func(MovieUtil.removeProp, dollar),
        )
    
    poleTrack = Sequence(
        Func(MovieUtil.showProps, poles, hands),
        ActorInterval(pole, 'fishing-pole'),
        Func(MovieUtil.removeProps, poles),
        )

    toonTrack = Sequence(
        Func(toon.headsUp, battle, targetPos), # Face toon
        ActorInterval(toon, 'battlecast'), # perform the casting animation
        Func(toon.loop, 'neutral'), # Face toon
        )
    
    tracks = Parallel(dollarTrack, poleTrack, toonTrack)
    # See if lure succeeds
    if (sidestep == 0):
        # See if suit animates to this particular lure (or another one that
        # also succeeds on the same suit)
        if (kbbonus == 1 or hp > 0):
            suitTrack = Sequence()
            opos, ohpr = battle.getActorPosHpr(suit)
            # The suit travels during the reach animation, so we must renew 
            # its position to where it ends up after reaching
            reachDist = MovieUtil.SUIT_LURE_DISTANCE
            reachPos = Point3(opos[0], opos[1]-reachDist, opos[2])
            suitTrack.append(Func(suit.loop, 'neutral'))
            # Wait before reaching for the dollar
            suitTrack.append(Wait(3.5))

            # Special case, if the suit is "big and tall" (type C and not
            # 'mm' or 'sc'), then the suit appears to travel more during the
            # reach animation (3.5 instead of 2.6).  Therefore, we must
            # actually push these suits back slightly as they move forward to
            # make sure they get to the correct spot but still look right
            # doing so
            suitName = suit.getStyleName()
            retardPos, retardHpr = battle.getActorPosHpr(suit)
            retardPos.setY(retardPos.getY() + MovieUtil.SUIT_EXTRA_REACH_DISTANCE)

            if (suitName in MovieUtil.largeSuits):
                moveTrack = lerpSuit(suit, 0.0, reachAnimDuration/2.5, retardPos,
                                     battle, trapProp)
                reachTrack = ActorInterval(suit, 'reach',
                                           duration=reachAnimDuration)# Reach for the dollar
                suitTrack.append(Parallel(moveTrack, reachTrack))
            else: # Otherwise just do the reach animation with no 
                  # artificial movement
                suitTrack.append(ActorInterval(suit, 'reach',
                        duration=reachAnimDuration)) # Reach for the dollar

            # Be sure to reparent the trapProp properly away from the
            # suit during movement and then back to the suit once
            # completed
            if trapProp:
                suitTrack.append(Func(trapProp.wrtReparentTo, battle))
            suitTrack.append(Func(suit.setPos, battle, reachPos))
            if trapProp:
                suitTrack.append(Func(trapProp.wrtReparentTo, suit))
                suit.battleTrapProp = trapProp

            suitTrack.append(Func(suit.loop, 'neutral'))
            suitTrack.append(Func(battle.lureSuit, suit))

            if (hp > 0):
                suitTrack.append(__createSuitDamageTrack(battle, suit, hp, lure, trapProp))
                
            if (revived != 0):
                suitTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle))
            if (died != 0):
                suitTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle))
            tracks.append(suitTrack)
            
    else: # If the lure fails
        tracks.append(Sequence(Wait(3.7),
                               Func(MovieUtil.indicateMissed, suit)))
    tracks.append(getSoundTrack('TL_fishing_pole.mp3', delay=0.5, node=toon))
        
    return tracks

def __createMagnetMultiTrack(lure, magnet, pos, hpr, scale, isSmallMagnet=1):
    toon = lure['toon']
    battle = lure['battle']
    sidestep = lure['sidestep']
    targets = lure['target']
    tracks = Parallel()

    # Create a track for the toon
    tracks.append(Sequence(
        ActorInterval(toon, 'hold-magnet'),
        Func(toon.loop, 'neutral'),
        ))

    # Create a track for the magnet
    hands = toon.getLeftHands()
    magnet2 = MovieUtil.copyProp(magnet)
    magnets = [magnet, magnet2]
    magnetTrack = Sequence(
        Wait(0.7), # Wait before showing the magnet
        Func(MovieUtil.showProps, magnets,
             hands, pos, hpr, scale),
        Wait(6.3), # Wait while magnet is being used
        Func(MovieUtil.removeProps, magnets))
    tracks.append(magnetTrack)

    for target in targets:
        suit = target['suit']
        trapProp = suit.battleTrapProp
        # See if lure succeeds
        if (sidestep == 0):
            hp = target['hp']
            kbbonus = target['kbbonus']
            died = target['died']
            revived = target['revived']
            # See if suit animates to this particular lure (or another one that
            # also succeeds on the same suit)
            if (kbbonus == 1 or hp > 0):
                suitDelay = 2.6
                suitMoveDuration = 0.8
                suitTrack = Sequence()
                opos, ohpr = battle.getActorPosHpr(suit)
                reachDist = MovieUtil.SUIT_LURE_DISTANCE
                reachPos = Point3(opos[0], opos[1]-reachDist, opos[2])
                numShakes = 3
                shakeTotalDuration = 0.8
                shakeDuration = shakeTotalDuration / float(numShakes)

                suitTrack.append(Func(suit.loop, 'neutral'))
                suitTrack.append(Wait(suitDelay))
                suitTrack.append(ActorInterval(suit, 'landing', startTime=2.37,
                                               endTime=1.82))
                for i in range(0, numShakes):
                    suitTrack.append(ActorInterval(
                        suit, 'landing', startTime=1.82, endTime=1.16,
                        duration=shakeDuration))

                suitTrack.append(ActorInterval(
                    suit, 'landing', startTime=1.16, endTime=0.7))
                suitTrack.append(ActorInterval(
                    suit, 'landing', startTime=0.7, duration=1.3))

                suitTrack.append(Func(suit.loop, 'neutral'))
                suitTrack.append(Func(battle.lureSuit, suit))
                if (hp > 0):
                    suitTrack.append(__createSuitDamageTrack(battle, suit, 
                                                                hp, lure, trapProp))
                if (revived != 0):
                    suitTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle))
                elif (died != 0):
                    suitTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle))

                tracks.append(suitTrack)
                # Must lerp the suit during the magnet animation
                tracks.append(lerpSuit(suit, suitDelay+0.55+shakeTotalDuration,
                                       suitMoveDuration, reachPos, battle, trapProp))
        else: # If lure fails
            tracks.append(Sequence(Wait(3.7),
                                   Func(MovieUtil.indicateMissed, suit)))

    if (isSmallMagnet == 1): # using the small magnet
        tracks.append(getSoundTrack('TL_small_magnet.mp3', delay=0.7, node=toon))
    else:
        tracks.append(getSoundTrack('TL_large_magnet.mp3', delay=0.7, node=toon))

    return tracks

def __createHypnoGogglesMultiTrack(lure, npcs = []):
    toon = lure['toon']
    if (lure.has_key('npc')):
        toon = lure['npc']
    targets = lure['target']
    battle = lure['battle']
    sidestep = lure['sidestep']
    goggles = globalPropPool.getProp('hypno-goggles')
    goggles2 = MovieUtil.copyProp(goggles)
    bothGoggles = [goggles, goggles2]
    pos = Point3(-1.03, 1.04, -0.30)
    hpr = Point3(-96.55, 36.14, -170.59)
    scale = Point3(1.5, 1.5, 1.5)
    hands = toon.getLeftHands()

    gogglesTrack = Sequence(
        Wait(0.6), # Wait a bit to appear
        Func(MovieUtil.showProps, bothGoggles,
             hands, pos, hpr, scale),
        ActorInterval(goggles, 'hypno-goggles', duration=2.2),
        Func(MovieUtil.removeProps, bothGoggles),
        )

    toonTrack = Sequence(
        ActorInterval(toon, 'hypnotize'),
        Func(toon.loop, 'neutral'),
        )
    tracks = Parallel(gogglesTrack, toonTrack)
    
    #print "hypno!!!!"
    #print targets

    for target in targets:
        suit = target['suit']
        trapProp = suit.battleTrapProp
        # See if lure succeeds
        if (sidestep == 0):
            hp = target['hp']
            kbbonus = target['kbbonus']
            died = target['died']
            revived = target['revived']
            # See if suit animates to this particular lure (or another one that
            # also succeeds on the same suit)
            if (kbbonus == 1 or hp > 0):
                suitTrack = Sequence()
                suitDelay = 1.6
                suitAnimDuration = 1.5
                opos, ohpr = battle.getActorPosHpr(suit)
                reachDist = MovieUtil.SUIT_LURE_DISTANCE
                reachPos = Point3(opos[0], opos[1]-reachDist, opos[2])
                suitTrack.append(Func(suit.loop, 'neutral'))
                # Wait before being hypnotized
                suitTrack.append(Wait(suitDelay))
                suitTrack.append(ActorInterval(suit, 'hypnotized', duration=3.1))
                suitTrack.append(Func(suit.setPos, battle, reachPos))
                suitTrack.append(Func(suit.loop, 'neutral'))
                suitTrack.append(Func(battle.lureSuit, suit))
                if (hp > 0):
                    suitTrack.append(__createSuitDamageTrack(battle, suit, 
                                                        hp, lure, trapProp))
                if (revived != 0):
                    suitTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle, npcs))
                elif (died != 0):
                    suitTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle, npcs))

                tracks.append(suitTrack)
                # Must lerp the suit during the hypnotize animation
                tracks.append(lerpSuit(suit, suitDelay+1.7, 0.7, reachPos,
                                        battle, trapProp))
        else: # If lure fails
            tracks.append(Sequence(Wait(2.3),
                                   Func(MovieUtil.indicateMissed, suit, 1.1)))
    tracks.append(getSoundTrack('TL_hypnotize.mp3', delay=0.5, node=toon))
    

    return tracks

def __lureOneDollar(lure):
    """ __lureOneDollar(lure)
    """
    dollarProp = '1dollar'
    dollar = globalPropPool.getProp(dollarProp)
    return __createFishingPoleMultiTrack(lure, dollar, dollarProp)

def __lureSmallMagnet(lure):
    """ __lureSmallMagnet(lure)
    """
    magnet = globalPropPool.getProp('small-magnet')
    pos = Point3(-0.27, 0.19, 0.29)
    hpr = Point3(-90.0, 84.17, -180.0)
    scale = Point3(0.85, 0.85, 0.85)
    return __createMagnetMultiTrack(lure, magnet, pos, hpr, scale, isSmallMagnet=1)

def __lureFiveDollar(lure):
    """ __lureFiveDollar(lure)
    """
    dollarProp = '5dollar'
    dollar = globalPropPool.getProp(dollarProp)
    return __createFishingPoleMultiTrack(lure, dollar, dollarProp)

def __lureLargeMagnet(lure):
    """ __lureLargeMagnet(lure)
    """
    magnet = globalPropPool.getProp('big-magnet')
    pos = Point3(-0.27, 0.08, 0.29)
    hpr = Point3(-90.0, 84.17, -180)
    scale = Point3(1.32, 1.32, 1.32)
    return __createMagnetMultiTrack(lure, magnet, pos, hpr, scale, isSmallMagnet=0)

def __lureTenDollar(lure):
    """ __lureTenDollar(lure)
    """
    dollarProp = '10dollar'
    dollar = globalPropPool.getProp(dollarProp)
    return __createFishingPoleMultiTrack(lure, dollar, dollarProp)

def __lureHypnotize(lure, npcs = []):
    """ __lureHypnotize(lure)
    """
    return __createHypnoGogglesMultiTrack(lure, npcs)


def __lureSlideshow(lure, npcs):
    """ __lureSlideshow(lure, npcs)
    """
    return __createSlideshowMultiTrack(lure, npcs)


def __createSuitDamageTrack(battle, suit, hp, lure, trapProp):
    """ __createSuitDamageIvals(suit, hp, battle)
    """
    # This function creates intervals for the suit taking damage
    # If trapProp doesn't exist, do nothing, with no reaction
    #import pdb; pdb.set_trace()
    if ((trapProp == None) or trapProp.isEmpty()):
         return Func(suit.loop, 'neutral')
    
    # Make sure to leave the trapProp in place (not parented to the suit)
    # while the suit performs its animation
    trapProp.wrtReparentTo(battle)

    # Now we learn which level trap we're using to use the appropriate suit reaction
    trapTrack = ToontownBattleGlobals.TRAP_TRACK
    trapLevel = suit.battleTrap
    trapTrackNames = ToontownBattleGlobals.AvProps[trapTrack]
    trapName = trapTrackNames[trapLevel]

    result = Sequence()
    def reparentTrap(trapProp=trapProp, battle=battle):
        if trapProp and not trapProp.isEmpty():
            trapProp.wrtReparentTo(battle)
    result.append(Func(reparentTrap))

    # Now detect if our trap was just thrown in this round, or leftover from before.
    # If just thrown, our cordinates for the banana, marbles, and tnt will be based off of
    # render, not battle, thus we make parent equal to render instead of the default battle.
    # And if the trap is fresh and is the quicksand, trapdoor, or rake, we create a hidden
    # dummy trapProp in the right position to obtain the correct coordinates for those
    # animations.
    parent = battle
    if (suit.battleTrapIsFresh == 1):
        if (trapName == 'quicksand' or trapName == 'trapdoor'):
            trapProp.hide()
            trapProp.reparentTo(suit)
            trapProp.setPos(Point3(0, MovieUtil.SUIT_TRAP_DISTANCE, 0))
            trapProp.setHpr(Point3(0, 0, 0))
            trapProp.wrtReparentTo(battle)
        elif (trapName == 'rake'):
            trapProp.hide()
            trapProp.reparentTo(suit)
            trapProp.setPos(0, MovieUtil.SUIT_TRAP_RAKE_DISTANCE, 0)
            # reorient the rake correctly to be stepped on
            trapProp.setHpr(Point3(0, 270, 0))
            trapProp.setScale(Point3(0.7, 0.7, 0.7))
            # The rake must be a specific distance from each suit for that
            # suit to be able to walk into the rake
            rakeOffset = MovieUtil.getSuitRakeOffset(suit)
            trapProp.setY(trapProp.getY() + rakeOffset)
        else:
            parent = render
    
    # Now decide which trap this is and use the different suit animation reactions
    if (trapName == 'banana'):
        slidePos = trapProp.getPos(parent)
        slidePos.setY(slidePos.getY() - 5.1)
        moveTrack = Sequence(
            Wait(0.1), # Wait before sliding the peel
            LerpPosInterval(trapProp, 0.1, slidePos, other=battle),
            )
        animTrack = Sequence(
            ActorInterval(trapProp, 'banana', startTime=3.1), # Animate banana spinning
            Wait(1.1), # Wait a bit before scaling banana away
            LerpScaleInterval(trapProp, 1, Point3(0.01, 0.01, 0.01)),
            )
        suitTrack = ActorInterval(suit, 'slip-backward')
        damageTrack = Sequence(
            Wait(0.5),
            Func(suit.showHpText, -hp, openEnded=0),
            Func(suit.updateHealthBar, hp),
            )
        soundTrack = Sequence(
            SoundInterval(globalBattleSoundCache.getSound('AA_pie_throw_only.mp3'), duration=0.55, node=suit),
            SoundInterval(globalBattleSoundCache.getSound('Toon_bodyfall_synergy.mp3'), node=suit),
            )
        result.append(Parallel(moveTrack, animTrack, suitTrack, damageTrack, soundTrack))
    elif ((trapName == 'rake') or (trapName == 'rake-react')):
        # Also need to make the rake pop up when stepped on, then fall back down
        hpr = trapProp.getHpr(parent)
        upHpr = Vec3(hpr[0], 179.9999, hpr[2])
        bounce1Hpr = Vec3(hpr[0], 120, hpr[2])
        bounce2Hpr = Vec3(hpr[0], 100, hpr[2])
                    
        rakeTrack = Sequence(
            Wait(0.5),
            LerpHprInterval(trapProp, 0.1, upHpr, startHpr=hpr),
            Wait(0.7),
            LerpHprInterval(trapProp, 0.4, hpr, startHpr=upHpr),
            LerpHprInterval(trapProp, 0.15, bounce1Hpr, startHpr=hpr),
            LerpHprInterval(trapProp, 0.05, hpr, startHpr=bounce1Hpr),
            LerpHprInterval(trapProp, 0.15, bounce2Hpr, startHpr=hpr),
            LerpHprInterval(trapProp, 0.05, hpr, startHpr=bounce2Hpr),
            Wait(0.2),
            LerpScaleInterval(trapProp, 0.2, Point3(0.01, 0.01, 0.01)),
            )
        rakeAnimDuration = 3.125
        suitTrack = ActorInterval(suit, 'rake-react',
                                  duration=rakeAnimDuration)
        damageTrack = Sequence(
            Wait(0.5),
            Func(suit.showHpText, -hp, openEnded=0),
            Func(suit.updateHealthBar, hp),
            )
        soundTrack = getSoundTrack('TL_step_on_rake.mp3', delay=0.6, node=suit)
        result.append(Parallel(rakeTrack, suitTrack, damageTrack, soundTrack))
    elif (trapName == 'marbles'):
        slidePos = trapProp.getPos(parent)
        slidePos.setY(slidePos.getY() - 6.5)
        moveTrack = Sequence(
            Wait(0.1), # Wait a bit before sliding the marbles
            LerpPosInterval(trapProp, 0.8, slidePos, other=battle),
            Wait(1.1),
            LerpScaleInterval(trapProp, 1, Point3(0.01, 0.01, 0.01)),
            )
        animTrack = ActorInterval(trapProp, 'marbles', startTime=3.1)
        suitTrack = ActorInterval(suit, 'slip-backward')
        damageTrack = Sequence(
            Wait(0.5),
            Func(suit.showHpText, -hp, openEnded=0),
            Func(suit.updateHealthBar, hp),
            )
        soundTrack = Sequence(
            SoundInterval(globalBattleSoundCache.getSound('AA_pie_throw_only.mp3'), duration=0.55, node=suit),
            SoundInterval(globalBattleSoundCache.getSound('Toon_bodyfall_synergy.mp3'), node=suit),
            )
        result.append(Parallel(moveTrack, animTrack, suitTrack, damageTrack, soundTrack))
    elif (trapName == 'quicksand'):
        sinkPos1 = trapProp.getPos(battle)
        sinkPos2 = trapProp.getPos(battle)
        dropPos = trapProp.getPos(battle) # Where suit drops from after the quicksand
        landPos = trapProp.getPos(battle) # Where the suit lands from the drop
        sinkPos1.setZ(sinkPos1.getZ() - 3.1)
        sinkPos2.setZ(sinkPos2.getZ() - 9.1)
        dropPos.setZ(dropPos.getZ() + 15)

        # We grab the name tag so we can hide it while the suit is in the quicksand
        nameTag = suit.find("**/joint_nameTag")
        trapTrack = Sequence(
            Wait(2.4),
            LerpScaleInterval(trapProp, 0.8, Point3(0.01, 0.01, 0.01)),
            )
        moveTrack = Sequence(
            Wait(0.9), # Wait before starting to sink
            LerpPosInterval(suit, 0.9, sinkPos1, other=battle), # Start to sink a bit
            LerpPosInterval(suit, 0.4, sinkPos2, other=battle), # Fall in quicksand
            Func(suit.setPos, battle, dropPos),
            Func(suit.wrtReparentTo, hidden),
            Wait(1.1), # Wait while stuck in the quicksand
            Func(suit.wrtReparentTo, battle),
            LerpPosInterval(suit, 0.3, landPos, other=battle), # Drop back down
            )
        animTrack = Sequence(
            ActorInterval(suit, 'flail'),
            ActorInterval(suit, 'flail', startTime=1.1),
            Wait(0.7),
            ActorInterval(suit, 'slip-forward', duration=2.1),
            )
        damageTrack = Sequence(
            Wait(3.5),
            Func(suit.showHpText, -hp, openEnded=0),
            Func(suit.updateHealthBar, hp),
            )
        soundTrack = Sequence(
            Wait(0.7),
            SoundInterval(globalBattleSoundCache.getSound('TL_quicksand.mp3'), node=suit),
            Wait(0.1),
            SoundInterval(globalBattleSoundCache.getSound('Toon_bodyfall_synergy.mp3'), node=suit),
            )
        result.append(Parallel(trapTrack, moveTrack, animTrack, damageTrack, soundTrack))
    elif (trapName == 'trapdoor'):
        sinkPos = trapProp.getPos(battle)
        dropPos = trapProp.getPos(battle) # Where suit drops from after the trap door
        landPos = trapProp.getPos(battle) # Where the suit lands from the drop
        sinkPos.setZ(sinkPos.getZ() - 9.1)
        dropPos.setZ(dropPos.getZ() + 15)
        
        trapTrack = Sequence(
            Wait(2.4),
            LerpScaleInterval(trapProp, 0.8, Point3(0.01, 0.01, 0.01))
            )
        moveTrack = Sequence(
            Wait(2.2), # Wait before falling through the trap door
            LerpPosInterval(suit, 0.4, sinkPos, other=battle), # Fall through trap door
            Func(suit.setPos, battle, dropPos),
            Func(suit.wrtReparentTo, hidden),
            Wait(1.6), # Wait while through the trap door
            Func(suit.wrtReparentTo, battle),
            LerpPosInterval(suit, 0.3, landPos, other=battle), # Drop back down
            )

        animTrack = Sequence(
            # Suit quickly looks down
            getSplicedLerpAnimsTrack(suit, 'flail', 0.7, 0.25),
            # Spring the trap door (make it go black)
            Func(trapProp.setColor, Vec4(0, 0, 0, 1)),
            # Suit slowly looks back up with resignation
            ActorInterval(suit, 'flail', startTime=0.7, endTime=0),
            # Suspenseful wait
            ActorInterval(suit, 'neutral', duration=0.5),
            # Suit falls through the trap door
            ActorInterval(suit, 'flail', startTime=1.1),
            Wait(1.1),
            ActorInterval(suit, 'slip-forward', duration=2.1),
            )

        damageTrack = Sequence(
            Wait(3.5),
            Func(suit.showHpText, -hp, openEnded=0),
            Func(suit.updateHealthBar, hp),
            )
        soundTrack = Sequence(
            Wait(0.8),
            SoundInterval(globalBattleSoundCache.getSound('TL_trap_door.mp3'), node=suit),
            Wait(0.8),
            SoundInterval(globalBattleSoundCache.getSound('Toon_bodyfall_synergy.mp3'), node=suit),
            )
        result.append(Parallel(trapTrack, moveTrack, animTrack, damageTrack, soundTrack))
    elif (trapName == 'tnt'):
        tntTrack = ActorInterval(trapProp, 'tnt')
        explosionTrack = Sequence(
            Wait(2.3),
            createTNTExplosionTrack(battle, trapProp=trapProp,
                                    relativeTo=parent),
            )
        suitTrack = Sequence(
            ActorInterval(suit, 'flail', duration=0.7),
            ActorInterval(suit, 'flail', startTime=0.7, endTime=0.0),
            ActorInterval(suit, 'neutral', duration=0.4),
            ActorInterval(suit, 'flail', startTime=0.6, endTime=0.7),
            Wait(0.4),
            ActorInterval(suit, 'slip-forward', startTime=2.48, duration=0.1),
            Func(battle.movie.needRestoreColor),
            Func(suit.setColorScale, Vec4(0, 0, 0, 1)),
            Func(trapProp.reparentTo, hidden),
            ActorInterval(suit, 'slip-forward', startTime=2.58),
            Func(suit.clearColorScale),
            Func(trapProp.sparksEffect.cleanup),
            Func(battle.movie.clearRestoreColor),
            )
        damageTrack = Sequence(
            Wait(2.3),
            Func(suit.showHpText, -hp, openEnded=0),
            Func(suit.updateHealthBar, hp),
            )
        explosionSound = base.loadSfx("phase_3.5/audio/sfx/ENC_cogfall_apart.mp3")
        soundTrack = Sequence(
            SoundInterval(globalBattleSoundCache.getSound('TL_dynamite.mp3'), duration=2.0, node=suit),
            SoundInterval(explosionSound, duration=0.6, node=suit),
            )
        result.append(Parallel(tntTrack, suitTrack, damageTrack,
                              explosionTrack, soundTrack))

    elif trapName == 'traintrack':
        trainInterval = createIncomingTrainInterval(battle, suit, hp, lure, trapProp)
        result.append(trainInterval) 
    else:
        notify.warning('unknown trapName: %s detected on suit: %s' % (trapName, suit))
        
    suit.battleTrapProp = trapProp
    assert notify.debug('adding battle.removeTrap for suit %d' % suit.doId)
    result.append(Func(battle.removeTrap, suit, True))
    result.append(Func(battle.unlureSuit, suit))
    result.append(__createSuitResetPosTrack(suit, battle))
    result.append(Func(suit.loop, 'neutral'))

    if trapName == 'traintrack':
        #a bit of a hack, when a suit is joining, the train track still stays, really make sure it goes away
        #TODO this nukes the train tunnels shrinking, figure out a better way
        result.append(Func(MovieUtil.removeProp, trapProp))    

    return result

def __createSuitResetPosTrack(suit, battle):
    resetPos, resetHpr = battle.getActorPosHpr(suit)
    moveDist = Vec3(suit.getPos(battle) - resetPos).length()
    moveDuration = 0.5
    walkTrack = Sequence(
        # First face the right direction, then walk backwards
        Func(suit.setHpr, battle, resetHpr),
        ActorInterval(suit, 'walk', startTime=1, duration=moveDuration, endTime=0.0001),
        Func(suit.loop, 'neutral')
        )
    # Actually move the suit
    moveTrack = LerpPosInterval(suit, moveDuration, resetPos, other=battle)
    return Parallel(walkTrack, moveTrack)

def getSplicedLerpAnimsTrack(object, animName, origDuration, newDuration,
                             startTime=0, fps=30):
    """
    This function returns a Sequence splicing together an animation
    over a modified frame of time.  This allows an animation to be
    shortened or lengthened (if you can tolerate any resulting rushed
    or choppy animation. This function increases an animation time by
    inserting a uniform time interval before successive ActorInterval
    calls. It decreases time by progressing the animation time forward
    faster than real-time (basically uniformly skipping frames).
    
    Arguments:
        object = object to perform th animation
        animName = name of the animation to lengthen/shorten
        origDuration = original time duration the animation should normally play in
        newDuration = lengthened or shortened time for the new animation
        startTime = startTime for the animation
        fps = usually held constant, helps determine number of actor intervals to use
    """
    track = Sequence()
    addition = 0 # Addition will be added to the startTime to move animation forward
    numIvals = origDuration * fps # Number of actor intervals to use
    # The timeInterval is what to add before each actor interval to delay time
    timeInterval = newDuration / numIvals
    # The animInterval is how much the animation progresses forward each interval
    animInterval = origDuration / numIvals
    for i in range(0, numIvals):
        track.append(Wait(timeInterval))
        track.append(ActorInterval(object, animName, startTime=startTime+addition,
                                   duration=animInterval))
        addition += animInterval # Add addition to push the animation forward
    return track


def lerpSuit(suit, delay, duration, reachPos, battle, trapProp):
    """ This function moves a suit, taking care to reparent a trap prop (if there)
        so that it doesn't slide with the suit"""

    track = Sequence()
    # If trapProp does exist, reparent it to the battle
    if trapProp:
        # we need to use safeWrtReparentTo, the trap may disappear
        # due to a collision with the railroad
        track.append(Func(safeWrtReparentTo,trapProp, battle))

    track.append(Wait(delay))
    track.append(LerpPosInterval(suit, duration, reachPos, other=battle))

    if trapProp:
        if trapProp.getName() == 'traintrack':
            notify.debug('UBERLURE MovieLure.lerpSuit deliberately not parenting trainTrack to suit')
        else:
            track.append(Func(safeWrtReparentTo,trapProp, suit))
        suit.battleTrapProp = trapProp

    return track

def createTNTExplosionTrack(parent, explosionPoint=None, trapProp=None, relativeTo=render):
    explosionTrack = Sequence()
    explosion = BattleProps.globalPropPool.getProp('kapow')
    explosion.setBillboardPointEye()
    if not explosionPoint:
        if trapProp:
            explosionPoint = trapProp.getPos(relativeTo)
            explosionPoint.setZ(explosionPoint.getZ() + 2.3)
        else:
            explosionPoint = Point3(0, 3.6, 2.1)
    explosionTrack.append(Func(explosion.reparentTo, parent))
    explosionTrack.append(Func(explosion.setPos, explosionPoint))
    explosionTrack.append(Func(explosion.setScale, 0.11))
    explosionTrack.append(ActorInterval(explosion, 'kapow'))
    explosionTrack.append(Func(MovieUtil.removeProp, explosion))
    return explosionTrack


TRAIN_STARTING_X = -7.131 #-7.13081 #feet empirically determined to be tunnel distance
TRAIN_TUNNEL_END_X = 7.1 #7.09926
TRAIN_TRAVEL_DISTANCE = 45 #feet
TRAIN_SPEED = 35.0 #feet per second
TRAIN_DURATION = TRAIN_TRAVEL_DISTANCE / TRAIN_SPEED #feet
TRAIN_MATERIALIZE_TIME = 3 # seconds
TOTAL_TRAIN_TIME = TRAIN_DURATION + TRAIN_MATERIALIZE_TIME

def createSuitReactionToTrain(battle, suit,hp,lure,trapProp):
    toon = lure['toon']    
    retval = Sequence()
    suitPos, suitHpr = battle.getActorPosHpr(suit)
    distance = suitPos.getX() - TRAIN_STARTING_X
    timeToGetHit = distance / TRAIN_SPEED

    suitTrack = Sequence()
    showDamage = Func(suit.showHpText, -hp, openEnded=0)
    updateHealthBar = Func(suit.updateHealthBar, hp)
    anim = 'flatten'
    suitReact = ActorInterval(suit, anim)
    cogGettingHit = getSoundTrack('TL_train_cog.mp3', node = toon)
    
    suitTrack.append(Func(suit.loop, 'neutral'))
    suitTrack.append(Wait(timeToGetHit + TRAIN_MATERIALIZE_TIME))
    suitTrack.append(updateHealthBar)        
    suitTrack.append(Parallel(suitReact,cogGettingHit))
    suitTrack.append(showDamage)


    curDuration = suitTrack.getDuration()

    timeTillEnd = TOTAL_TRAIN_TIME - curDuration
    if timeTillEnd > 0:
        suitTrack.append(Wait(timeTillEnd))

    retval.append(suitTrack)

    return retval

def createIncomingTrainInterval(battle, suit, hp, lure, trapProp):
    """
    create the interval of a train going across the track and flattening the cogs
    """
    toon = lure['toon']    
    retval = Parallel()

    #nope we still need to react correctly to it
    suitTrack = createSuitReactionToTrain(battle, suit,hp,lure,trapProp)
    retval.append(suitTrack)

    #make sure we only call this once
    if not trapProp.find('**/train_gag').isEmpty():
        return retval



    # Set up a pair of clipping planes to cut off the train before and
    # after the tunnels.
    clipper = PlaneNode('clipper')
    clipper.setPlane(Plane(Vec3(+1, 0, 0), Point3(TRAIN_STARTING_X, 0, 0)))
    clipNP = trapProp.attachNewNode(clipper)
    trapProp.setClipPlane(clipNP)

    clipper2 = PlaneNode('clipper2')
    clipper2.setPlane(Plane(Vec3(-1, 0, 0), Point3(TRAIN_TUNNEL_END_X, 0, 0)))
    clipNP2 = trapProp.attachNewNode(clipper2)
    trapProp.setClipPlane(clipNP2)    
    
    train = globalPropPool.getProp('train')
    train.hide()
    train.reparentTo(trapProp)
    #train.setBin('')
    tempScale = trapProp.getScale()
    trainScale = Vec3(1.0/tempScale[0], 1.0/tempScale[1], 1.0 / tempScale[2])
    #import pdb; pdb.set_trace()

    trainIval = Sequence()
    trainIval.append(Func(train.setScale, trainScale))
    trainIval.append(Func(train.setH, 90))
    trainIval.append(Func(train.setX, TRAIN_STARTING_X))
    trainIval.append(Func(train.setTransparency,1))
    trainIval.append(Func(train.setColorScale, Point4(1,1,1,0)))
    trainIval.append(Func(train.show))

    tunnel2 = trapProp.find('**/tunnel3')
    tunnel3 = trapProp.find('**/tunnel2')
    tunnels = [tunnel2, tunnel3]
    #import pdb; pdb.set_trace()
    for tunnel in tunnels:
        trainIval.append(Func(tunnel.setTransparency,1))
        trainIval.append(Func(tunnel.setColorScale, Point4(1,1,1,0)))
        trainIval.append(Func(tunnel.setScale, Point3(1.0,0.01,0.01)))
        trainIval.append(Func(tunnel.show))                         
    
    materializeIval = Parallel()
    materializeIval.append(LerpColorScaleInterval(train, TRAIN_MATERIALIZE_TIME, Point4(1,1,1,1)))
    for tunnel in tunnels:
        materializeIval.append(LerpColorScaleInterval(tunnel, TRAIN_MATERIALIZE_TIME, Point4(1,1,1,1)))


    for tunnel in tunnels:
        tunnelScaleIval = Sequence()
        tunnelScaleIval.append(LerpScaleInterval(tunnel, TRAIN_MATERIALIZE_TIME - 1.0, Point3(1.0, 2.0, 2.5)))
        tunnelScaleIval.append(LerpScaleInterval(tunnel, 0.5, Point3(1.0, 3.0, 1.5)))
        tunnelScaleIval.append(LerpScaleInterval(tunnel, 0.5, Point3(1.0, 2.5, 2.0)))
        materializeIval.append(tunnelScaleIval)
        
    trainIval.append(materializeIval)
    
    endingX = TRAIN_STARTING_X + TRAIN_TRAVEL_DISTANCE
    trainIval.append( LerpPosInterval(train, TRAIN_DURATION, Point3(endingX,0,0), other=battle ))
    trainIval.append(LerpColorScaleInterval(train, TRAIN_MATERIALIZE_TIME, Point4(1,1,1,0)))
    
    retval.append(trainIval)

    #incoming train sound effect
    trainSoundTrack = getSoundTrack('TL_train.mp3',node=toon)
    retval.append(trainSoundTrack)
    return retval



def __createSlideshowMultiTrack(lure, npcs = []):
    toon = lure['toon']
    battle = lure['battle']
    sidestep = lure['sidestep']    
    origHpr = toon.getHpr(battle)
    slideshowDelay = 2.5
    hands = toon.getLeftHands()
    endPos = toon.getPos(battle)
    endPos.setY( endPos.getY() + 4)

    button = globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]

    #do the toon track
    toonTrack = Sequence()
    toonTrack.append(Func(MovieUtil.showProps, buttons, hands))
    toonTrack.append(Func(toon.headsUp, battle, endPos))
    toonTrack.append(ActorInterval(toon, 'pushbutton'))
    toonTrack.append(Func(MovieUtil.removeProps, buttons))
    toonTrack.append(Func(toon.loop, 'neutral'))
    toonTrack.append(Func(toon.setHpr, battle, origHpr))

    # do the slideshow popping up

    slideShowProp = globalPropPool.getProp('slideshow')
    propTrack = Sequence()
    propTrack.append(Wait(slideshowDelay))
    propTrack.append(Func(slideShowProp.show))
    propTrack.append(Func(slideShowProp.setScale, Point3(0.1, 0.1, 0.1)))
    propTrack.append(Func(slideShowProp.reparentTo, battle))
    propTrack.append(Func(slideShowProp.setPos, endPos))
    propTrack.append(LerpScaleInterval(slideShowProp, 1.2, Point3(1.0, 1.0, 1.0)))
    # shrink it to nothing
    shrinkDuration = 0.4
    totalDuration = 7.1
    propTrackDurationAtThisPoint = propTrack.getDuration()
    waitTime = totalDuration - propTrackDurationAtThisPoint - shrinkDuration
    if waitTime > 0:
        propTrack.append(Wait(waitTime))
    propTrack.append( LerpScaleInterval(nodePath = slideShowProp, scale = Point3(1.0,1.0,0.1),
                                         duration = shrinkDuration, ))    
    propTrack.append(Func(MovieUtil.removeProp, slideShowProp))

    tracks = Parallel(propTrack, toonTrack)
    
    targets = lure['target']
    for target in targets:
        suit = target['suit']
        trapProp = suit.battleTrapProp
        # See if lure succeeds
        if (sidestep == 0):
            hp = target['hp']
            kbbonus = target['kbbonus']
            died = target['died']
            revived = target['revived']
            # See if suit animates to this particular lure (or another one that
            # also succeeds on the same suit)
            if (kbbonus == 1 or hp > 0):
                suitTrack = Sequence()
                suitDelay = 3.8
                suitAnimDuration = 1.5
                opos, ohpr = battle.getActorPosHpr(suit)
                reachDist = MovieUtil.SUIT_LURE_DISTANCE
                reachPos = Point3(opos[0], opos[1]-reachDist, opos[2])
                suitTrack.append(Func(suit.loop, 'neutral'))
                # Wait before being hypnotized
                suitTrack.append(Wait(suitDelay))
                suitTrack.append(ActorInterval(suit, 'hypnotized', duration=3.1))
                suitTrack.append(Func(suit.setPos, battle, reachPos))
                suitTrack.append(Func(suit.loop, 'neutral'))
                suitTrack.append(Func(battle.lureSuit, suit))
                if (hp > 0):
                    suitTrack.append(__createSuitDamageTrack(battle, suit, 
                                                        hp, lure, trapProp))
                if (revived != 0):
                    suitTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle, npcs))
                elif (died != 0):
                    suitTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle, npcs))

                tracks.append(suitTrack)
                # Must lerp the suit during the hypnotize animation
                tracks.append(lerpSuit(suit, suitDelay+1.7, 0.7, reachPos,
                                        battle, trapProp))
        else: # If lure fails
            tracks.append(Sequence(Wait(2.3),
                                   Func(MovieUtil.indicateMissed, suit, 1.1)))
    #TODO sound effects
    tracks.append(getSoundTrack('TL_presentation.mp3', delay=2.3, node=toon))
    tracks.append(getSoundTrack('AA_drop_trigger_box.mp3', delay=slideshowDelay, node=toon))

    return tracks
