from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from BattleSounds import *
from toontown.toon.ToonDNA import *
from toontown.suit.SuitDNA import *

from direct.directnotify import DirectNotifyGlobal
import random
import MovieCamera
import MovieUtil
from MovieUtil import calcAvgSuitPos

notify = DirectNotifyGlobal.directNotify.newCategory('MovieThrow')

# still need miss 'hitting' sounds to be separated from the 'throw' sounds
# for creampie and fruitpie, wholecreampie and whole fruitpie and bdaycake
# so the sound and animation can be synced at the end of variable-length throw
# until we get these sounds, we just use these 'only' sounds as placeholders
hitSoundFiles = ('AA_tart_only.mp3',
                 'AA_slice_only.mp3',
                 'AA_slice_only.mp3',
                 'AA_slice_only.mp3',
                 'AA_slice_only.mp3',
                 'AA_wholepie_only.mp3',
                 'AA_wholepie_only.mp3',) #UBER

# need miss 'hitting' sounds to be separated from the 'throw' sounds
# so the sound and animation can be synced at the end of variable-length throw
# until we get these sounds, we just use 'AA_pie_throw_only.mp3' for all misses
#missSoundFiles = ('AA_pie_throw_only.mp3',
#                  'AA_pie_throw_only.mp3',
#                  'AA_pie_throw_only.mp3',
#                  'AA_pie_throw_only.mp3',
#                  'AA_pie_throw_only.mp3',
#                  'AA_pie_throw_only.mp3',)

#tPieLeavesHand = 2.755
tPieLeavesHand = 2.7
tPieHitsSuit   = 3.0
tSuitDodges    = 2.45

# length of pie flight path when you miss relative to length
# of pie flight when you hit the suit
ratioMissToHit = 1.5
# this is based on the [0..1] time range of the pie flight when it misses
tPieShrink     = 0.7

pieFlyTaskName = "MovieThrow-pieFly"


def addHit (dict, suitId, hitCount):
    if (dict.has_key(suitId)):
        dict[suitId] += hitCount
    else:
        dict[suitId] = hitCount

def doFires(fires):
    
    """ Throws occur in the following order:
        a) by suit, in order of increasing number of throws per suit
          1) level 1 throws, right to left, (TOON_THROW_DELAY later)
          2) level 2 throws, right to left, (TOON_THROW_DELAY later)
          3) level 3 throws, right to left, (TOON_THROW_DELAY later)
          etc.
        b) next suit, (TOON_THROW_SUIT_DELAY later)
    """

    #import pdb; pdb.set_trace()
    if (len(fires) == 0):
        return (None, None)

    # Group the throws by targeted suit
    suitFiresDict = {}
    # throw['toon'] is the thrower. 
    
    for fire in fires:
        suitId = fire['target']['suit'].doId
        if (suitFiresDict.has_key(suitId)):
            suitFiresDict[suitId].append(fire)
        else:
            suitFiresDict[suitId] = [fire]
        
    # A list of lists of throws grouped by suit
    suitFires = suitFiresDict.values()
    # Sort the suits based on the number of throws per suit
    def compFunc(a, b):
        if (len(a) > len(b)):
            return 1
        elif (len(a) < len(b)):
            return -1
        return 0
    suitFires.sort(compFunc)

    #since we have group throws now, we calculate how
    #many times each suit gets hit over here
    totalHitDict = {}
    singleHitDict = {}
    groupHitDict = {}
    
    for fire in fires:
        if 1:
            suitId = fire['target']['suit'].doId            
            if fire['target']['hp'] > 0:
                addHit(singleHitDict,suitId,1)
                addHit(totalHitDict,suitId,1)
            else:
                addHit(singleHitDict,suitId,0)
                addHit(totalHitDict,suitId,0)                

    notify.debug('singleHitDict = %s' % singleHitDict)
    notify.debug('groupHitDict = %s' % groupHitDict)
    notify.debug('totalHitDict = %s' % totalHitDict)

    
    # Apply attacks in order
    delay = 0.0
    mtrack = Parallel()
    firedTargets = []
    for sf in suitFires:
        if (len(sf) > 0):
            ival = __doSuitFires(sf)
            if (ival):
                mtrack.append(Sequence(Wait(delay), ival))
            delay = delay + TOON_FIRE_SUIT_DELAY

    retTrack = Sequence()
    retTrack.append(mtrack)


            

    camDuration = retTrack.getDuration()
    camTrack = MovieCamera.chooseFireShot(fires, suitFiresDict,
                                           camDuration)
    return (retTrack, camTrack)

def __doSuitFires(fires):
    """ __doSuitThrows(throws)
        Create the intervals for the attacks on a particular suit.
        1 or more toons can throw at the same target suit
        Note: attacks are sorted by increasing level (as are toons)
        Returns a multitrack with toon throws in the following order:
        1) level 1 throws, right to left, (TOON_THROW_DELAY later)
        2) level 2 throws, right to left, (TOON_THROW_DELAY later)
        etc.
        The intervals actually overlap in the case of multiple hits,
        prematurely cutting off the end of the react animation.
    """
    toonTracks = Parallel()
    delay = 0.0
    # See if suit is hit multiple times, if it is, don't show stun animation
    hitCount = 0
    for fire in fires:
        if fire['target']['hp'] > 0:
            # Hit, continue counting
            hitCount += 1
        else:
            # Miss, no need to think about stun effect
            break
    suitList = []        
            
    for fire in fires:
        if not (fire['target']['suit'] in suitList):
            suitList.append(fire['target']['suit'])
            
    for fire in fires:
        showSuitCannon = 1
        if not (fire['target']['suit'] in suitList):
            showSuitCannon = 0
        else:
            suitList.remove(fire['target']['suit'])
        tracks = __throwPie(fire, delay, hitCount, showSuitCannon)
        if (tracks):
            for track in tracks:
                toonTracks.append(track)
        delay = delay + TOON_THROW_DELAY
    return toonTracks

def __showProp(prop, parent, pos):
    prop.reparentTo(parent)
    prop.setPos(pos)

def __animProp(props, propName, propType):
    if 'actor' == propType:
        for prop in props:
            prop.play(propName)
    elif 'model' == propType:
        pass
    else:
        notify.error("No such propType as: %s" % propType)

def __billboardProp(prop):
    scale = prop.getScale()
    #prop.lookAt(camera)
    prop.setBillboardPointWorld()
    prop.setScale(scale)

def __suitMissPoint(suit, other=render):
    # this is a point just above the suit's head
    pnt = suit.getPos(other)
    pnt.setZ(pnt[2] + (suit.getHeight() * 1.3))
    return pnt

def __propPreflight(props, suit, toon, battle):
    assert(len(props) >= 2)
    prop = props[0]
    # make sure the 0 lod toon is in the right pose of the animation
    toon.update(0)
    # take the prop from the toon
    prop.wrtReparentTo(battle)
    props[1].reparentTo(hidden)

    # make the top of the pie point along +Y
    for ci in range(prop.getNumChildren()):
        prop.getChild(ci).setHpr(0, -90, 0)

    # figure out where it's going to end up
    targetPnt = MovieUtil.avatarFacePoint(suit, other=battle)

    # make the pie point towards the suit's face
    prop.lookAt(targetPnt)

def __propPreflightGroup(props, suits, toon, battle):
    """
    same as __propPreflight, but face the avg suit pt
    """
    assert(len(props) >= 2)
    prop = props[0]
    # make sure the 0 lod toon is in the right pose of the animation
    toon.update(0)
    # take the prop from the toon
    prop.wrtReparentTo(battle)
    props[1].reparentTo(hidden)

    # make the top of the pie point along +Y
    for ci in range(prop.getNumChildren()):
        prop.getChild(ci).setHpr(0, -90, 0)

    # figure out where it's going to end up
    avgTargetPt = Point3(0,0,0)
    for suit in suits:
        avgTargetPt += MovieUtil.avatarFacePoint(suit, other=battle)
    avgTargetPt /= len(suits)

    # make the pie point towards the suit's face
    prop.lookAt(avgTargetPt)


def __piePreMiss(missDict, pie, suitPoint, other=render):
    # called after propPreFlight
    missDict['pie'] = pie
    missDict['startScale'] = pie.getScale()
    missDict['startPos'] = pie.getPos(other)
    v = Vec3(suitPoint - missDict['startPos'])
    endPos = missDict['startPos'] + (v * ratioMissToHit)
    missDict['endPos'] = endPos

def __pieMissLerpCallback(t, missDict):
    pie = missDict['pie']
    newPos = (missDict['startPos'] * (1.0 - t)) + (missDict['endPos'] * t)
    if t < tPieShrink:
        tScale = 0.0001
    else:
        tScale = (t - tPieShrink) / (1.0 - tPieShrink)
    newScale = (missDict['startScale'] * max((1.0 - tScale), 0.01))
    pie.setPos(newPos)
    pie.setScale(newScale)


def __piePreMissGroup(missDict, pies, suitPoint, other=render):
    """
    Same as __piePreMiss, but handles multiple pie parts
    # called after propPreFlight
    """

    missDict['pies'] = pies
    missDict['startScale'] = pies[0].getScale()
    missDict['startPos'] = pies[0].getPos(other)
    v = Vec3(suitPoint - missDict['startPos'])
    endPos = missDict['startPos'] + (v * ratioMissToHit)
    missDict['endPos'] = endPos

    notify.debug('startPos=%s' % missDict['startPos'])
    notify.debug('v=%s'  % v)
    notify.debug('endPos=%s' % missDict['endPos'])    

def __pieMissGroupLerpCallback(t, missDict):
    """
    Same as __pieMissLerpCallback, but handles multiple pie parts
    """
    
    pies = missDict['pies']
    newPos = (missDict['startPos'] * (1.0 - t)) + (missDict['endPos'] * t)
    if t < tPieShrink:
        tScale = 0.0001
    else:
        tScale = (t - tPieShrink) / (1.0 - tPieShrink)
    newScale = (missDict['startScale'] * max((1.0 - tScale), 0.01))

    for pie in pies:
        pie.setPos(newPos)
        pie.setScale(newScale)    


    


def __getSoundTrack(level, hitSuit, node=None):

    throwSound = globalBattleSoundCache.getSound('AA_drop_trigger_box.mp3')

    throwTrack = Sequence(Wait(2.15), SoundInterval(throwSound, node=node))

    return throwTrack


def __throwPie(throw, delay, hitCount, showCannon = 1):
    #print ("__throwPie %s" % (showCannon))

    toon = throw['toon']
    hpbonus = throw['hpbonus']
    target = throw['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    sidestep = throw['sidestep']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    level = throw['level']
    battle = throw['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    notify.debug('toon: %s throws tart at suit: %d for hp: %d died: %d' % \
            (toon.getName(), suit.doId, hp, died))

    pieName = pieNames[0]

    hitSuit = (hp > 0)

    #pie = globalPropPool.getProp(pieName)
    #pieType = globalPropPool.getPropType(pieName)
    #pie2 = MovieUtil.copyProp(pie)
    #pies = [pie, pie2]
    #hands = toon.getRightHands()

    #splatName = 'splat-' + pieName
    #if pieName == 'wedding-cake':
    #    splatName = 'splat-birthday-cake'
    #splat = globalPropPool.getProp(splatName)
    #splatType = globalPropPool.getPropType(splatName)
    
    
    button = globalPropPool.getProp('button')
    buttonType = globalPropPool.getPropType('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    hands = toon.getLeftHands()
    

    # make the toon throw the pie
    toonTrack = Sequence()
    toonFace = Func(toon.headsUp, battle, suitPos)
    toonTrack.append(Wait(delay))
    toonTrack.append(toonFace)
    toonTrack.append(ActorInterval(toon, 'pushbutton'))
    toonTrack.append(ActorInterval(toon, 'wave', duration= 2.0))
    toonTrack.append(ActorInterval(toon, 'duck'))
    toonTrack.append(Func(toon.loop, 'neutral'))
    toonTrack.append(Func(toon.setHpr, battle, origHpr))

    buttonTrack = Sequence()

    buttonShow = Func(MovieUtil.showProps, buttons, hands)
    buttonScaleUp = LerpScaleInterval(button, 1.0, button.getScale(), startScale = Point3(0.01, 0.01, 0.01))
    buttonScaleDown = LerpScaleInterval(button, 1.0, Point3(0.01, 0.01, 0.01), startScale = button.getScale())
    buttonHide = Func(MovieUtil.removeProps, buttons)
    buttonTrack.append(Wait(delay))
    buttonTrack.append(buttonShow)
    buttonTrack.append(buttonScaleUp)
    buttonTrack.append(Wait(2.5))
    buttonTrack.append(buttonScaleDown)
    buttonTrack.append(buttonHide)
    
    soundTrack = __getSoundTrack(level, hitSuit, toon)

    suitResponseTrack = Sequence()
    reactIval = Sequence()
    if showCannon:
        showDamage = Func(suit.showHpText, -hp, openEnded=0)
        updateHealthBar = Func(suit.updateHealthBar, hp)
        # If the suit gets knocked back, animate it
        # No stun animation shown here
        cannon = loader.loadModel("phase_4/models/minigames/toon_cannon")
        barrel = cannon.find("**/cannon")
        barrel.setHpr(0,90,0)
        
        cannonHolder = render.attachNewNode('CannonHolder')
        cannon.reparentTo(cannonHolder)
        cannon.setPos(0,0,-8.6)
        cannonHolder.setPos(suit.getPos(render))
        cannonHolder.setHpr(suit.getHpr(render))
        cannonAttachPoint = barrel.attachNewNode('CannonAttach')
        kapowAttachPoint = barrel.attachNewNode('kapowAttach')
        scaleFactor = 1.6
        iScale = 1 / scaleFactor
        barrel.setScale(scaleFactor,1,scaleFactor)
        cannonAttachPoint.setScale(iScale, 1, iScale)
        cannonAttachPoint.setPos(0,6.7,0)
        kapowAttachPoint.setPos(0,-0.5,1.9)
        suit.reparentTo(cannonAttachPoint)
        suit.setPos(0,0,0)
        suit.setHpr(0,-90,0)
        suitLevel = suit.getActualLevel()
        deep = 2.5 + (suitLevel * 0.20)
        
        #import pdb; pdb.set_trace()
        
        #print "Fire anim suit name: %s" % (suit.dna.name)
        suitScale = 0.90
        import math
        suitScale = 0.9 - (math.sqrt(suitLevel) * 0.10)
        #if suit.dna.name == 'bf':
        #    suitScale = 0.80
        #elif suit.dna.name == 'cr':
        #    suitScale = 0.75
        sival = [] # Suit interval of its animation
        posInit = cannonHolder.getPos()
        posFinal = Point3(posInit[0] + 0.0, posInit[1] + 0.0, posInit[2] + 7.0)
        kapow = globalPropPool.getProp('kapow')
    
        kapow.reparentTo(kapowAttachPoint)
        kapow.hide()
        kapow.setScale(0.25)
        kapow.setBillboardPointEye()
        
        
        smoke = loader.loadModel(
        "phase_4/models/props/test_clouds")
        smoke.reparentTo(cannonAttachPoint)
        smoke.setScale(.5)
        smoke.hide()
        smoke.setBillboardPointEye()
        
        soundBomb = base.loadSfx("phase_4/audio/sfx/MG_cannon_fire_alt.mp3")
        playSoundBomb = SoundInterval(soundBomb,node=cannonHolder)
        
        soundFly = base.loadSfx("phase_4/audio/sfx/firework_whistle_01.mp3")
        playSoundFly = SoundInterval(soundFly,node=cannonHolder)
        
        soundCannonAdjust = base.loadSfx("phase_4/audio/sfx/MG_cannon_adjust.mp3")
        playSoundCannonAdjust = SoundInterval(soundCannonAdjust, duration = 0.6 ,node=cannonHolder)
        
        soundCogPanic = base.loadSfx("phase_5/audio/sfx/ENC_cogafssm.mp3")
        playSoundCogPanic = SoundInterval(soundCogPanic,node=cannonHolder)
    
    
        reactIval = Parallel(   ActorInterval(suit, 'pie-small-react'),
                                Sequence(
                                    Wait(0.0),
                                    LerpPosInterval(cannonHolder, 2.0, posFinal,
                                             startPos = posInit, blendType='easeInOut'),
                                    Parallel(
                                        LerpHprInterval(barrel, 0.6, Point3(0,45,0), startHpr=Point3(0,90,0) , blendType='easeIn'),
                                        playSoundCannonAdjust,
                                        ),
                                    Wait(2.0),
                                    Parallel(
                                        LerpHprInterval(barrel, 0.6, Point3(0,90,0), startHpr=Point3(0,45,0) , blendType='easeIn'),
                                        playSoundCannonAdjust,
                                        ),
                                    LerpPosInterval(cannonHolder, 1.0, posInit,
                                             startPos = posFinal, blendType='easeInOut'),
                                    
                                         ),
                                Sequence(
                                    Wait(0.0),
                                    Parallel(
                                                ActorInterval(suit, 'flail'),
                                                suit.scaleInterval(1.0, suitScale),
                                                LerpPosInterval(suit, 0.25, Point3(0,-1.0,0.0)),
                                                Sequence(
                                                    Wait(0.25),
                                                    Parallel(
                                                        playSoundCogPanic,
                                                        LerpPosInterval(suit, 1.50, Point3(0,-deep,0.0), blendType='easeIn'),
                                                             ),
                                                         ),
                                             ),
                                    Wait(2.5),
                                    
                                    Parallel(
                                        playSoundBomb,
                                        playSoundFly,
                                        Sequence( 
                                            Func(smoke.show),
                                            Parallel(LerpScaleInterval(smoke, .5, 3),
                                            LerpColorScaleInterval(smoke, .5, Vec4(2,2,2,0))),
                                            Func(smoke.hide),
                                        ),
                                        Sequence( 
                                            Func(kapow.show),
                                            ActorInterval(kapow, 'kapow'),
                                            Func(kapow.hide),
                                        ),
                                        LerpPosInterval(suit, 3.00, Point3(0,150.0,0.0)),
                                        suit.scaleInterval(3.0, 0.01),
                                        ),
                                    Func(suit.hide),
                                    )
                            )
        
        if (hitCount == 1):
            sival = Sequence(
                    Parallel(
                        reactIval,
                        MovieUtil.createSuitStunInterval(suit, 0.3, 1.3),
                        ),
                    Wait(0.0),
                    Func(cannonHolder.remove),
                )
        else:
            sival = reactIval
            #sival = ActorInterval(suit, 'pie-small-react')
        suitResponseTrack.append(Wait(delay + tPieHitsSuit))
        suitResponseTrack.append(showDamage)
        suitResponseTrack.append(updateHealthBar)
        suitResponseTrack.append(sival)
        # Make a bonus track for any hp bonus
        bonusTrack = Sequence(Wait(delay + tPieHitsSuit))
        if (kbbonus > 0):
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -kbbonus, 2, openEnded=0))
        if (hpbonus > 0):
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -hpbonus, 1, openEnded=0))
            
        if 0:
            if (revived != 0):
                suitResponseTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle))
            elif (died != 0):
                suitResponseTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle))
            else:
                suitResponseTrack.append(Func(suit.loop, 'neutral'))
            
        suitResponseTrack = Parallel(suitResponseTrack, bonusTrack)
    
      
    
        # Since it's possible for there to be simultaneous throws, we only
        # want the suit to dodge one time at most.  Thus if the suit is
        # not hit (dodges) and that dodge is not from the first dodge
        # (which has delay=0) then we don't add another suit reaction.
        # Otherwise, we add the suit track as normal
    

    return [toonTrack, soundTrack, buttonTrack, suitResponseTrack]







