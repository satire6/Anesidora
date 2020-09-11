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

def doThrows(throws):
    
    """ Throws occur in the following order:
        a) by suit, in order of increasing number of throws per suit
          1) level 1 throws, right to left, (TOON_THROW_DELAY later)
          2) level 2 throws, right to left, (TOON_THROW_DELAY later)
          3) level 3 throws, right to left, (TOON_THROW_DELAY later)
          etc.
        b) next suit, (TOON_THROW_SUIT_DELAY later)
    """

    #import pdb; pdb.set_trace()
    if (len(throws) == 0):
        return (None, None)

    # Group the throws by targeted suit
    suitThrowsDict = {}
    # throw['toon'] is the thrower. 
    for throw in throws:
        # TODO: Count suits, and if there is only one, save that variable.
        if attackAffectsGroup( throw['track'], throw['level']):
            #hmmm lets try throwing at all of them
            #for target in throw['target']:
            #    suitId = targett['suit'].doId
            #    if (suitThrowsDict.has_key(suitId)):
            #        suitThrowsDict[suitId].append(throw)
            #    else:
            #        suitThrowsDict[suitId] = [throw]                
            pass
        else:
            suitId = throw['target']['suit'].doId
            if (suitThrowsDict.has_key(suitId)):
                suitThrowsDict[suitId].append(throw)
            else:
                suitThrowsDict[suitId] = [throw]
    # A list of lists of throws grouped by suit
    suitThrows = suitThrowsDict.values()
    # Sort the suits based on the number of throws per suit
    def compFunc(a, b):
        if (len(a) > len(b)):
            return 1
        elif (len(a) < len(b)):
            return -1
        return 0
    suitThrows.sort(compFunc)

    #since we have group throws now, we calculate how
    #many times each suit gets hit over here
    totalHitDict = {}
    singleHitDict = {}
    groupHitDict = {}
    
    for throw in throws:
        if attackAffectsGroup( throw['track'], throw['level']):
            for i in range(len (throw['target'])):
                target= throw['target'][i]
                suitId = target['suit'].doId
                if target['hp'] > 0:
                    addHit(groupHitDict,suitId,1)
                    addHit(totalHitDict,suitId,1)
                else:
                    addHit(groupHitDict,suitId,0)
                    addHit(totalHitDict,suitId,0)                    
                    
        else:
            suitId = throw['target']['suit'].doId            
            if throw['target']['hp'] > 0:
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
    for st in suitThrows:
        if (len(st) > 0):
            ival = __doSuitThrows(st)
            if (ival):
                mtrack.append(Sequence(Wait(delay), ival))
            delay = delay + TOON_THROW_SUIT_DELAY

    retTrack = Sequence()
    retTrack.append(mtrack)


    #we've done the single target throws, handle the group throws
    groupThrowIvals = Parallel()        
    groupThrows = []    
    for throw in throws:
        # TODO: Count suits, and if there is only one, save that variable.
        if attackAffectsGroup( throw['track'], throw['level']):
            groupThrows.append(throw)

    for throw in groupThrows:
        tracks = None
        tracks = __throwGroupPie(throw, 0, groupHitDict)
            
        if (tracks ):
            #groupThrowIvals.append(Sequence(Wait(delay), ival))
            for track in tracks:
                groupThrowIvals.append(track)            
        #delay = delay + TOON_THROW_SUIT_DELAY

    retTrack.append(groupThrowIvals)
            

    camDuration = retTrack.getDuration()
    camTrack = MovieCamera.chooseThrowShot(throws, suitThrowsDict,
                                           camDuration)
    return (retTrack, camTrack)

def __doSuitThrows(throws):
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
    for throw in throws:
        if throw['target']['hp'] > 0:
            # Hit, continue counting
            hitCount += 1
        else:
            # Miss, no need to think about stun effect
            break
    for throw in throws:
        tracks = __throwPie(throw, delay, hitCount)
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


def __getWeddingCakeSoundTrack(level, hitSuit, node=None):
    throwTrack = Sequence()
    if hitSuit:
        throwSound = globalBattleSoundCache.getSound('AA_throw_wedding_cake.mp3')
        songTrack = Sequence()
        songTrack.append(Wait(1.0))
        songTrack.append (  SoundInterval(throwSound, node=node))

        splatSound = globalBattleSoundCache.getSound('AA_throw_wedding_cake_cog.mp3')
        splatTrack = Sequence()
        splatTrack.append(Wait(tPieHitsSuit))
        splatTrack.append (  SoundInterval(splatSound, node=node))

        throwTrack.append(Parallel(
            songTrack,
            splatTrack,
            ))
        
    else:
        throwSound = globalBattleSoundCache.getSound('AA_throw_wedding_cake_miss.mp3')
        throwTrack.append(Wait(tSuitDodges))
        throwTrack.append (  SoundInterval(throwSound, node=node))
    
    
    return throwTrack
    


def __getSoundTrack(level, hitSuit, node=None):
    #level: the level of attack, int 0-5
    #hitSuit: does the attack hit toon, bool
    if level == UBER_GAG_LEVEL_INDEX:
        return __getWeddingCakeSoundTrack(level, hitSuit, node)

    throwSound = globalBattleSoundCache.getSound('AA_pie_throw_only.mp3')

    throwTrack = Sequence(Wait(2.6), SoundInterval(throwSound, node=node))
    
    if hitSuit: # Add in impact sound if throw hits
        hitSound = globalBattleSoundCache.getSound(hitSoundFiles[level])
        hitTrack = Sequence(Wait(tPieLeavesHand),
                            SoundInterval(hitSound, node=node))
        return Parallel(throwTrack, hitTrack)
    else: # Just returns the sound of the throw if you miss
        return throwTrack


def __throwPie(throw, delay, hitCount):
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

    pieName = pieNames[level]

    hitSuit = (hp > 0)

    pie = globalPropPool.getProp(pieName)
    pieType = globalPropPool.getPropType(pieName)
    pie2 = MovieUtil.copyProp(pie)
    pies = [pie, pie2]
    hands = toon.getRightHands()

    splatName = 'splat-' + pieName
    if pieName == 'wedding-cake':
        splatName = 'splat-birthday-cake'
    splat = globalPropPool.getProp(splatName)
    splatType = globalPropPool.getPropType(splatName)

    # make the toon throw the pie
    toonTrack = Sequence()
    toonFace = Func(toon.headsUp, battle, suitPos)
    toonTrack.append(Wait(delay))
    toonTrack.append(toonFace)
    toonTrack.append(ActorInterval(toon, 'throw'))
    toonTrack.append(Func(toon.loop, 'neutral'))
    toonTrack.append(Func(toon.setHpr, battle, origHpr))

    # take the pie from the toon and make it fly
    pieShow = Func(MovieUtil.showProps, pies, hands)
    pieAnim = Func(__animProp, pies, pieName, pieType)
    pieScale1 = LerpScaleInterval(pie, 1.0, pie.getScale(), 
                                  startScale=MovieUtil.PNT3_NEARZERO)
    pieScale2 = LerpScaleInterval(pie2, 1.0, pie2.getScale(), 
                                  startScale=MovieUtil.PNT3_NEARZERO)
    pieScale = Parallel(pieScale1, pieScale2)
    piePreflight = Func(__propPreflight, pies, suit, toon, battle)

    pieTrack = Sequence(
        Wait(delay),
        pieShow,
        pieAnim,
        pieScale,
        Func(battle.movie.needRestoreRenderProp, pies[0]),
        Wait(tPieLeavesHand - 1.0),
        piePreflight,
        )

    soundTrack = __getSoundTrack(level, hitSuit, toon)

    if hitSuit:
        # make the pie fly up to the suit's face and disappear
        pieFly = LerpPosInterval(pie, tPieHitsSuit - tPieLeavesHand,
                                 pos=MovieUtil.avatarFacePoint(suit, other=battle),
                                 name=pieFlyTaskName, other=battle)
        pieHide = Func(MovieUtil.removeProps, pies)
        # play the splat animation
        splatShow = Func(__showProp, splat, suit, Point3(0, 0, suit.getHeight()))
        splatBillboard = Func(__billboardProp, splat)
        splatAnim = ActorInterval(splat, splatName)
        splatHide = Func(MovieUtil.removeProp, splat)
        pieTrack.append(pieFly)
        pieTrack.append(pieHide)
        pieTrack.append(Func(battle.movie.clearRenderProp, pies[0]))
        pieTrack.append(splatShow)
        pieTrack.append(splatBillboard)
        pieTrack.append(splatAnim)
        pieTrack.append(splatHide)
    else:
        # the suit is going to dodge, or we missed
        # make the pie fly past the suit's face, and shrink to nothing
        missDict = {}
        if sidestep:
            suitPoint = MovieUtil.avatarFacePoint(suit, other=battle)
        else:
            suitPoint = __suitMissPoint(suit, other=battle)
        piePreMiss = Func(__piePreMiss, missDict, pie, suitPoint, battle)
        pieMiss = LerpFunctionInterval(
            __pieMissLerpCallback, 
            extraArgs=[missDict],
            duration = ((tPieHitsSuit - tPieLeavesHand)*ratioMissToHit))
        pieHide = Func(MovieUtil.removeProps, pies)
        pieTrack.append(piePreMiss)
        pieTrack.append(pieMiss)
        pieTrack.append(pieHide)
        pieTrack.append(Func(battle.movie.clearRenderProp, pies[0]))

    if hitSuit:
        suitResponseTrack = Sequence()
        showDamage = Func(suit.showHpText, -hp, openEnded=0, attackTrack = THROW_TRACK)
        updateHealthBar = Func(suit.updateHealthBar, hp)
        # If the suit gets knocked back, animate it
        # No stun animation shown here
        sival = [] # Suit interval of its animation
        if (kbbonus > 0):
            suitPos, suitHpr = battle.getActorPosHpr(suit)
            suitType = getSuitBodyType(suit.getStyleName())
            animTrack = Sequence()
            animTrack.append(ActorInterval(suit, 'pie-small-react', duration=0.2))
            if (suitType == 'a'):
                animTrack.append(ActorInterval(suit, 'slip-forward', startTime=2.43))
            elif (suitType == 'b'):
                animTrack.append(ActorInterval(suit, 'slip-forward', startTime=1.94))
            elif (suitType == 'c'):
                animTrack.append(ActorInterval(suit, 'slip-forward', startTime=2.58))
            # Be sure to unlure the suit so it doesn't walk back (already knocked back)
            animTrack.append(Func(battle.unlureSuit, suit))

            moveTrack = Sequence(
                Wait(0.2),
                LerpPosInterval(suit, 0.6, pos=suitPos, other=battle),
                )
            sival = Parallel(animTrack, moveTrack)
        else:
            if (hitCount == 1):
                sival = Parallel(
                    ActorInterval(suit, 'pie-small-react'),
                    MovieUtil.createSuitStunInterval(suit, 0.3, 1.3),
                    )
            else:
                sival = ActorInterval(suit, 'pie-small-react')
            #sival = ActorInterval(suit, 'pie-small-react')
        suitResponseTrack.append(Wait(delay + tPieHitsSuit))
        suitResponseTrack.append(showDamage)
        suitResponseTrack.append(updateHealthBar)
        suitResponseTrack.append(sival)
        # Make a bonus track for any hp bonus
        bonusTrack = Sequence(Wait(delay + tPieHitsSuit))
        if (kbbonus > 0):
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -kbbonus, 2, openEnded=0, attackTrack = THROW_TRACK))
        if (hpbonus > 0):
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -hpbonus, 1, openEnded=0, attackTrack = THROW_TRACK))
            
        if (revived != 0):
            suitResponseTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle))
        elif (died != 0):
            suitResponseTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle))
        else:
            suitResponseTrack.append(Func(suit.loop, 'neutral'))
            
        suitResponseTrack = Parallel(suitResponseTrack, bonusTrack)

    else:
        # suit dodges
        # other suits may need to dodge as well
        suitResponseTrack = MovieUtil.createSuitDodgeMultitrack(delay + tSuitDodges,
                                                                suit, leftSuits, rightSuits)

    # Since it's possible for there to be simultaneous throws, we only
    # want the suit to dodge one time at most.  Thus if the suit is
    # not hit (dodges) and that dodge is not from the first dodge
    # (which has delay=0) then we don't add another suit reaction.
    # Otherwise, we add the suit track as normal
    
    if (not hitSuit and delay > 0):
        return [toonTrack, soundTrack, pieTrack]
    else:
        return [toonTrack, soundTrack, pieTrack, suitResponseTrack]






def __createWeddingCakeFlight(throw,  groupHitDict, pie, pies):
    toon = throw['toon']
    battle = throw['battle']
    level = throw['level']
    sidestep = throw['sidestep']
    hpbonus = throw['hpbonus']    
    numTargets = len(throw['target'])
    pieName = pieNames[level]

    #so loop through our targets, and throw 1 layer of the wedding cake at each one
    splatName = 'splat-' + pieName
    if pieName == 'wedding-cake':
        splatName = 'splat-birthday-cake'
    splat = globalPropPool.getProp(splatName)
    splats = [splat]
    for i in range (numTargets-1):
        splats.append( MovieUtil.copyProp(splat) )
    
    splatType = globalPropPool.getPropType(splatName)
            
    cakePartStrs = ['cake1','cake2','cake3','caketop']
    cakeParts = []
    for part in cakePartStrs:
        cakeParts.append(pie.find('**/%s' % part))

    #figure out which cake part goes to which suit
    cakePartDivisions = {}
    cakePartDivisions[1] = [[cakeParts[0], cakeParts[1], cakeParts[2], cakeParts[3] ],]
    cakePartDivisions[2] = [ [cakeParts[0], cakeParts[1]], [cakeParts[2], cakeParts[3]] ]
    cakePartDivisions[3] = [ [cakeParts[0], cakeParts[1]], [cakeParts[2],], [cakeParts[3],] ]
    cakePartDivisions[4] = [ [cakeParts[0],], [cakeParts[1],], [cakeParts[2],], [cakeParts[3],] ]    
                           
    cakePartDivToUse = cakePartDivisions[len(throw['target'])]
    groupPieTracks = Parallel()
    for i in range(numTargets):
        target = throw['target'][i]
        suit = target['suit']
        hitSuit = (target['hp'] > 0)
        
        singlePieTrack = Sequence()
        if hitSuit:
            # make the pie fly up to the suit's face and disappear
            piePartReparent = Func( reparentCakePart, pie, cakePartDivToUse[i])
            singlePieTrack.append(piePartReparent)

            cakePartTrack = Parallel()
            for cakePart in cakePartDivToUse[i]:
                pieFly = LerpPosInterval(cakePart, tPieHitsSuit - tPieLeavesHand,
                                         pos=MovieUtil.avatarFacePoint(suit, other=battle),
                                         name=pieFlyTaskName, other=battle)            
                cakePartTrack.append(pieFly)
            singlePieTrack.append(cakePartTrack)

            pieRemoveCakeParts = Func(MovieUtil.removeProps, cakePartDivToUse[i])

            pieHide = Func(MovieUtil.removeProps, pies)            

            # play the splat animation
            splatShow = Func(__showProp, splats[i], suit, Point3(0, 0, suit.getHeight()))
            splatBillboard = Func(__billboardProp, splats[i])
            splatAnim = ActorInterval(splats[i], splatName)
            splatHide = Func(MovieUtil.removeProp, splats[i])            


            singlePieTrack.append(pieRemoveCakeParts)            
            singlePieTrack.append(pieHide)
            singlePieTrack.append(Func(battle.movie.clearRenderProp, pies[0]))
            singlePieTrack.append(splatShow)
            singlePieTrack.append(splatBillboard)
            singlePieTrack.append(splatAnim)
            singlePieTrack.append(splatHide)
        else:
            # the suit is going to dodge, or we missed
            # make the pie fly past the suit's face, and shrink to nothing
            #untested for now
        
            missDict = {}
            if sidestep:
                suitPoint = MovieUtil.avatarFacePoint(suit, other=battle)
            else:
                suitPoint = __suitMissPoint(suit, other=battle)
            piePartReparent = Func( reparentCakePart, pie, cakePartDivToUse[i])
            piePreMiss = Func(__piePreMissGroup, missDict, cakePartDivToUse[i], suitPoint, battle)
            pieMiss = LerpFunctionInterval(
                __pieMissGroupLerpCallback, 
                extraArgs=[missDict],
                duration = ((tPieHitsSuit - tPieLeavesHand)*ratioMissToHit) ) 
            pieHide = Func(MovieUtil.removeProps, pies)
            pieRemoveCakeParts = Func(MovieUtil.removeProps, cakePartDivToUse[i])

            singlePieTrack.append(piePartReparent)
            singlePieTrack.append(piePreMiss)
            singlePieTrack.append(pieMiss)
            singlePieTrack.append(pieRemoveCakeParts) 
            singlePieTrack.append(pieHide)
            singlePieTrack.append(Func(battle.movie.clearRenderProp, pies[0]))

        groupPieTracks.append(singlePieTrack)

    return groupPieTracks

def __throwGroupPie(throw, delay, groupHitDict):
    """
    TODO this can be made to __throwGroupPie and wedding cake stuff is called in a diff function
    """
    toon = throw['toon']
    battle = throw['battle']
    level = throw['level']
    sidestep = throw['sidestep']
    hpbonus = throw['hpbonus']    
    numTargets = len(throw['target'])
    
    avgSuitPos = calcAvgSuitPos(throw)
    
    # make the toon throw the wedding cake
    origHpr = toon.getHpr(battle)  
    
    toonTrack = Sequence()
    toonFace = Func(toon.headsUp, battle, avgSuitPos)
    toonTrack.append(Wait(delay))
    toonTrack.append(toonFace)
    toonTrack.append(ActorInterval(toon, 'throw'))
    toonTrack.append(Func(toon.loop, 'neutral'))
    toonTrack.append(Func(toon.setHpr, battle, origHpr))    


    # take the pie from the toon and make it fly
    suits = []
    for i in range(numTargets):
        suits.append ( throw['target'][i]['suit'])
    pieName = pieNames[level]
    pie = globalPropPool.getProp(pieName)
    pieType = globalPropPool.getPropType(pieName)    
    pie2 = MovieUtil.copyProp(pie)    
    pies = [pie, pie2]
    hands = toon.getRightHands()    
    pieShow = Func(MovieUtil.showProps, pies, hands)
    pieAnim = Func(__animProp, pies, pieName, pieType)
    pieScale1 = LerpScaleInterval(pie, 1.0, pie.getScale() * 1.5, 
                                  startScale=MovieUtil.PNT3_NEARZERO)
    pieScale2 = LerpScaleInterval(pie2, 1.0, pie2.getScale() *1.5, 
                                  startScale=MovieUtil.PNT3_NEARZERO)
    pieScale = Parallel(pieScale1, pieScale2)
    piePreflight = Func(__propPreflightGroup, pies, suits, toon, battle)

    pieTrack = Sequence(
        Wait(delay),
        pieShow,
        pieAnim,
        pieScale,
        Func(battle.movie.needRestoreRenderProp, pies[0]),
        Wait(tPieLeavesHand - 1.0),
        piePreflight,
        )

    #create the pie flight interval
    if level == UBER_GAG_LEVEL_INDEX:    
        groupPieTracks = __createWeddingCakeFlight(throw, groupHitDict, pie, pies)
    else:
        notify.error('unhandled throw level %d' % level)       
    
    pieTrack.append(groupPieTracks)


    didThrowHitAnyone = False
    for i in range(numTargets):
        target = throw['target'][i]
        hitSuit = (target['hp'] > 0)
        if hitSuit:
            didThrowHitAnyone = True            
    soundTrack = __getSoundTrack(level, didThrowHitAnyone, toon)        
                      
    groupSuitResponseTrack = Parallel()
    #handle the suit response
    for i in range(numTargets):
        target = throw['target'][i]
        suit = target['suit']
        hitSuit = (target['hp'] > 0)
        leftSuits = target['leftSuits']
        rightSuits = target['rightSuits']
        hp = target['hp']
        kbbonus = target['kbbonus']
        died = target['died']    
        revived = target['revived'] 
        if hitSuit:
            singleSuitResponseTrack = Sequence()
            showDamage = Func(suit.showHpText, -hp, openEnded=0, attackTrack=THROW_TRACK)
            updateHealthBar = Func(suit.updateHealthBar, hp)
            # If the suit gets knocked back, animate it
            # No stun animation shown here
            sival = [] # Suit interval of its animation
            if (kbbonus > 0):
                suitPos, suitHpr = battle.getActorPosHpr(suit)
                suitType = getSuitBodyType(suit.getStyleName())
                animTrack = Sequence()
                animTrack.append(ActorInterval(suit, 'pie-small-react', duration=0.2))
                if (suitType == 'a'):
                    animTrack.append(ActorInterval(suit, 'slip-forward', startTime=2.43))
                elif (suitType == 'b'):
                    animTrack.append(ActorInterval(suit, 'slip-forward', startTime=1.94))
                elif (suitType == 'c'):
                    animTrack.append(ActorInterval(suit, 'slip-forward', startTime=2.58))
                # Be sure to unlure the suit so it doesn't walk back (already knocked back)
                animTrack.append(Func(battle.unlureSuit, suit))

                moveTrack = Sequence(
                    Wait(0.2),
                    LerpPosInterval(suit, 0.6, pos=suitPos, other=battle),
                    )
                sival = Parallel(animTrack, moveTrack)
            else:
                if (groupHitDict[suit.doId] == 1):
                    sival = Parallel(
                        ActorInterval(suit, 'pie-small-react'),
                        MovieUtil.createSuitStunInterval(suit, 0.3, 1.3),
                        )
                else:
                    sival = ActorInterval(suit, 'pie-small-react')
                #sival = ActorInterval(suit, 'pie-small-react')
            singleSuitResponseTrack.append(Wait(delay + tPieHitsSuit))
            singleSuitResponseTrack.append(showDamage)
            singleSuitResponseTrack.append(updateHealthBar)
            singleSuitResponseTrack.append(sival)
        
            # Make a bonus track for any hp bonus
            bonusTrack = Sequence(Wait(delay + tPieHitsSuit))
            if (kbbonus > 0):
                bonusTrack.append(Wait(0.75))
                bonusTrack.append(Func(suit.showHpText, -kbbonus, 2, openEnded=0, attackTrack = THROW_TRACK))
            if (hpbonus > 0):
                bonusTrack.append(Wait(0.75))
                bonusTrack.append(Func(suit.showHpText, -hpbonus, 1, openEnded=0, attackTrack = THROW_TRACK))
                
            if (revived != 0):
                singleSuitResponseTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle))
                        
            elif (died != 0):
                singleSuitResponseTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle))
            else:
                singleSuitResponseTrack.append(Func(suit.loop, 'neutral'))
            
            singleSuitResponseTrack = Parallel(singleSuitResponseTrack, bonusTrack)

        else:
            #if none of the group throws hit at all, we can do a dodge
            groupHitValues = groupHitDict.values()
            if groupHitValues.count(0) == len(groupHitValues):
                singleSuitResponseTrack = MovieUtil.createSuitDodgeMultitrack(delay + tSuitDodges,
                                                                suit, leftSuits, rightSuits)
            else:
                #because all the group pies fire at the same time, do not dodge at all
                #in case one toon hits and another toon misses
                singleSuitResponseTrack = Sequence(Wait(tPieHitsSuit - 0.1),
                                               Func(MovieUtil.indicateMissed,
                                                    suit, 1.0))
            

        groupSuitResponseTrack.append(singleSuitResponseTrack)

    return [toonTrack,pieTrack, soundTrack, groupSuitResponseTrack]


def reparentCakePart(pie, cakeParts):
    pieParent = pie.getParent()
    notify.debug('pieParent = %s' % pieParent)
    for cakePart in cakeParts:
        cakePart.wrtReparentTo(pieParent)
