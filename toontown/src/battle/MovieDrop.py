from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from BattleSounds import *

import MovieCamera
from direct.directnotify import DirectNotifyGlobal
import MovieUtil
import MovieNPCSOS
from MovieUtil import calcAvgSuitPos
from direct.showutil import Effects

notify = DirectNotifyGlobal.directNotify.newCategory('MovieDrop')


hitSoundFiles = ('AA_drop_flowerpot.mp3',
                 'AA_drop_sandbag.mp3',
                 'AA_drop_anvil.mp3',
                 'AA_drop_bigweight.mp3',
                 'AA_drop_safe.mp3',
                 'AA_drop_piano.mp3',
                 'AA_drop_boat.mp3') #UBER

missSoundFiles = ('AA_drop_flowerpot_miss.mp3',
                  'AA_drop_sandbag_miss.mp3',
                  'AA_drop_anvil_miss.mp3',
                  'AA_drop_bigweight_miss.mp3',
                  'AA_drop_safe_miss.mp3',
                  'AA_drop_piano_miss.mp3', #UBER
                  'AA_drop_boat_miss.mp3')

# time offsets
tDropShadow = 1.3
tSuitDodges = 2.45 + tDropShadow
tObjectAppears = 3.0 + tDropShadow
tButtonPressed = 2.44

# durations
dShrink = 0.3
dShrinkOnMiss = 0.1

dPropFall = 0.6

objects = ('flowerpot',
           'sandbag',
           'anvil',
           'weight',
           'safe',
           'piano',
           'ship') #Uber
objZOffsets = (0.75, 0.75, 0., 0., 0., 0., 0.0) #UBER
objStartingScales = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0)  #UBER            

landFrames = (12, 4, 1, 11, 11, 11, 2)
shoulderHeights = {'a': 13.28 / 4.,
                   'b': 13.74 / 4.,
                   'c': 10.02 / 4.}

def doDrops(drops):
    """ Drops occur in the following order:
        a) by suit, in order of increasing number of drops per suit
          1) level 1 drops, right to left, (TOON_DROP_DELAY later)
          2) level 2 drops, right to left, (TOON_DROP_DELAY later)
          3) level 3 drops, right to left, (TOON_DROP_DELAY later)
          etc.
        b) next suit, (TOON_DROP_SUIT_DELAY later)
    """
    if (len(drops) == 0):
        return (None, None)


    npcArrivals, npcDepartures, npcs = MovieNPCSOS.doNPCTeleports(drops)

    # Group the drops by targeted suit
    suitDropsDict = {}
    groupDrops = []
    for drop in drops:
        track = drop['track']
        level = drop['level']
        targets = drop['target']
        if (len(targets) == 1):
            suitId = targets[0]['suit'].doId
            if (suitDropsDict.has_key(suitId)):
                suitDropsDict[suitId].append((drop, targets[0]))
            else:
                suitDropsDict[suitId] = [(drop, targets[0])]
        elif level <= MAX_LEVEL_INDEX and attackAffectsGroup(track,level):
            groupDrops.append(drop)
        else:
            # We're dealing with an NPC drop, which can have multiple
            # targets
            for target in targets:
                suitId = target['suit'].doId
                if (suitDropsDict.has_key(suitId)):
                    otherDrops = suitDropsDict[suitId]
                    alreadyInList = 0
                    for oDrop in otherDrops:
                        if (oDrop[0]['toon'] == drop['toon']):
                            alreadyInList = 1        
                    if (alreadyInList == 0):
                        suitDropsDict[suitId].append((drop, target))
                else:
                    suitDropsDict[suitId] = [(drop, target)]
    suitDrops = suitDropsDict.values()

    # Sort the suits based on the number of drops per suit
    def compFunc(a, b):
        if (len(a) > len(b)):
            return 1
        elif (len(a) < len(b)):
            return -1
        return 0
    suitDrops.sort(compFunc)
    delay = 0.0
    mtrack = Parallel(name = 'toplevel-drop')
    npcDrops = {}
    for st in suitDrops:
        if (len(st) > 0):
            ival = __doSuitDrops(st, npcs, npcDrops)
            if (ival):
                mtrack.append(Sequence(Wait(delay), ival))
            delay = delay + TOON_DROP_SUIT_DELAY

    dropTrack = Sequence(npcArrivals, mtrack, npcDepartures)
    camDuration = mtrack.getDuration()

    #we do the group drops after all the single drops have gone
    if groupDrops:
        ival = __doGroupDrops(groupDrops)
        dropTrack.append(ival)
        camDuration += ival.getDuration()


    enterDuration = npcArrivals.getDuration()
    exitDuration = npcDepartures.getDuration()
    camTrack = MovieCamera.chooseDropShot(drops, suitDropsDict, camDuration,
                                          enterDuration, exitDuration)
    
    
    return (dropTrack, camTrack)

def __getSoundTrack(level, hitSuit, node=None):
    #level: the level of attack, int 0-5
    #hitSuit: does the attack hit toon, bool

    if hitSuit: 
        soundEffect = globalBattleSoundCache.getSound(hitSoundFiles[level])
    else:
        soundEffect = globalBattleSoundCache.getSound(missSoundFiles[level])

    soundTrack = Sequence()
    
    if soundEffect:
        buttonSound = globalBattleSoundCache.getSound('AA_drop_trigger_box.mp3')
        fallingSound = None
        buttonDelay = tButtonPressed - 0.3
        fallingDuration = 1.5        
        if not level == UBER_GAG_LEVEL_INDEX:
            #boat drop has the whistle built in
            fallingSound = globalBattleSoundCache.getSound('incoming_whistleALT.mp3')

        soundTrack.append(Wait(buttonDelay))
        soundTrack.append(SoundInterval(buttonSound, duration = 0.67, node=node))
        if fallingSound:
            soundTrack.append(SoundInterval(fallingSound, duration=fallingDuration, node=node))
        if not level == UBER_GAG_LEVEL_INDEX:
            #the dropping effects seems to be timed at the start of the press, not after
            soundTrack.append(SoundInterval(soundEffect, node=node))

        if level == UBER_GAG_LEVEL_INDEX:
            if hitSuit:
                uberDelay = tButtonPressed
            else:
                uberDelay = tButtonPressed - 0.1
            oldSoundTrack = soundTrack
            soundTrack = Parallel()
            soundTrack.append(oldSoundTrack)

            uberTrack = Sequence()
            uberTrack.append(Wait(uberDelay))
            uberTrack.append(SoundInterval(soundEffect, node=node))

            soundTrack.append(uberTrack)
    else:
        soundTrack.append(Wait(0.1)) # dummy interval

    return soundTrack

def __doSuitDrops(dropTargetPairs, npcs, npcDrops):
    """ __doSuitDrops(drops) 
        1 or more toons drop at the same target suit
        Note: attacks are sorted by increasing level (as are toons)
        Returns a track with toon drops in the following order:
        1) level 1 drops, right to left, (TOON_DROP_DELAY later)
        2) level 2 drops, right to left, (TOON_DROP_DELAY later)
        etc.
    """
    toonTracks = Parallel()
    delay = 0.0
    alreadyDodged = 0
    alreadyTeased = 0
    for dropTargetPair in dropTargetPairs:
        drop = dropTargetPair[0]
        level = drop['level']
        objName = objects[level]
        target = dropTargetPair[1]
        track = __dropObjectForSingle(drop, delay, objName, level, alreadyDodged, 
                                      alreadyTeased, npcs, target, npcDrops)
        if (track):
            toonTracks.append(track)
            delay += TOON_DROP_DELAY
        hp = target['hp']
        if (hp <= 0):
            if (level >= 3):
                alreadyTeased = 1
            else:
                alreadyDodged = 1
    return toonTracks

def __doGroupDrops(groupDrops):
    """ __doSuitDrops(drops) 
        1 or more toons drop at the same target suit
        Note: attacks are sorted by increasing level (as are toons)
        Returns a track with toon drops in the following order:
        1) level 1 drops, right to left, (TOON_DROP_DELAY later)
        2) level 2 drops, right to left, (TOON_DROP_DELAY later)
        etc.
    """
    #import pdb; pdb.set_trace()

    toonTracks = Parallel()
    delay = 0.0
    alreadyDodged = 0
    alreadyTeased = 0

    for drop in groupDrops:
        battle = drop['battle']
        level = drop['level']
        #calculate center position, then figure out which suit is closest to it
        centerPos = calcAvgSuitPos(drop)
        targets = drop['target']
        numTargets = len(targets)
        closestTarget = -1
        nearestDistance = 100000.0
        for i in range(numTargets):
            suit = drop['target'][i]['suit']
            suitPos = suit.getPos(battle)
            displacement = Vec3(centerPos)
            displacement -= suitPos
            distance = displacement.lengthSquared()
            if distance < nearestDistance:
                closestTarget = i
                nearestDistance = distance

        #we have the suit to drop on
        track = __dropGroupObject(drop,delay, closestTarget, alreadyDodged, alreadyTeased)
        if (track):
            toonTracks.append(track)
            #delay += TOON_DROP_DELAY
            delay = delay + TOON_DROP_SUIT_DELAY
        hp = drop['target'][closestTarget]['hp']
        if (hp <= 0):
            if (level >= 3):
                alreadyTeased = 1
            else:
                alreadyDodged = 1            
        pass
    
    
    #for dropTargetPair in dropTargetPairs:
    #    drop = dropTargetPair[0]
    #    level = drop['level']
    #    objName = objects[level]
    #    target = dropTargetPair[1]
    #    track = __dropObject(drop, delay, objName, level, alreadyDodged, 
    #                             alreadyTeased, npcs, target, npcDrops)
    #    if (track):
    #        toonTracks.append(track)
    #        delay += TOON_DROP_DELAY
    #    hp = target['hp']
    #    if (hp <= 0):
    #        if (level >= 3):
    #            alreadyTeased = 1
    #        else:
    #            alreadyDodged = 1
    
    return toonTracks

def __dropGroupObject(drop, delay, closestTarget, alreadyDodged, alreadyTeased):

    level = drop['level']
    objName = objects[level]
    target = drop['target'][closestTarget]
    suit = drop['target'][closestTarget]['suit']
    npcDrops = {}    
    npcs = []
    
    returnedParallel = __dropObject(drop, delay, objName, level, alreadyDodged, 
                         alreadyTeased, npcs, target, npcDrops)    

    for i in range(len(drop['target'])):
        target = drop['target'][i]
        suitTrack =__createSuitTrack(drop, delay, level, alreadyDodged, alreadyTeased, target, npcs)
        if suitTrack:
            returnedParallel.append(suitTrack)
        

    return returnedParallel

def __dropObjectForSingle(drop, delay, objName, level, alreadyDodged, alreadyTeased, 
                              npcs, target, npcDrops):
    #import pdb; pdb.set_trace()
    singleDropParallel = __dropObject( drop, delay, objName, level, alreadyDodged, alreadyTeased,
                                    npcs, target, npcDrops)
    suitTrack = __createSuitTrack(drop, delay, level, alreadyDodged, alreadyTeased, target, npcs)

    if suitTrack:
        singleDropParallel.append(suitTrack)

    return singleDropParallel

def __dropObject(drop, delay, objName, level, alreadyDodged, alreadyTeased, 
                              npcs, target, npcDrops):
    toon = drop['toon']
    repeatNPC = 0
    battle = drop['battle']
    if (drop.has_key('npc')):
        toon = drop['npc']
        if (npcDrops.has_key(toon)):
            repeatNPC = 1
        else:
            npcDrops[toon] = 1
        origHpr = Vec3(0, 0, 0)
    else:
        origHpr = toon.getHpr(battle)
    hpbonus = drop['hpbonus']
    suit = target['suit']
    hp = target['hp']
    hitSuit = (hp > 0)
    died = target['died']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    kbbonus = target['kbbonus']
    suitPos = suit.getPos(battle)

    majorObject = (level >= 3)

    if (repeatNPC == 0):
        button = globalPropPool.getProp('button')
        buttonType = globalPropPool.getPropType('button')
        button2 = MovieUtil.copyProp(button)
        buttons = [button, button2]
        hands = toon.getLeftHands()

    object = globalPropPool.getProp(objName)
    objectType = globalPropPool.getPropType(objName)

    # The safe and weight are a bit too big
    if (objName == 'weight'):
        object.setScale(object.getScale()*0.75)
    elif (objName == 'safe'):
        object.setScale(object.getScale()*0.85)

    # The object will likely animate far from its initial bounding
    # volume while it drops.  To work around this bug, we artificially
    # change the object's bounding volume to be really big.  In fact,
    # we make it infinite, so it will never be culled while it's
    # onscreen.
    node = object.node()
    node.setBounds(OmniBoundingVolume())
    node.setFinal(1)

    # create the soundTrack
    soundTrack = __getSoundTrack(level, hitSuit, toon)

    # toon pulls the button out, presses it, and puts it away
    toonTrack = Sequence()
    if (repeatNPC == 0):
        toonFace = Func(toon.headsUp, battle, suitPos)
        toonTrack.append(Wait(delay))
        toonTrack.append(toonFace)
        toonTrack.append(ActorInterval(toon, 'pushbutton'))
        toonTrack.append(Func(toon.loop, 'neutral'))
        toonTrack.append(Func(toon.setHpr, battle, origHpr))

    # button scales up in toon's hand as he takes it out, and
    # scales down to nothing as it is put away
    buttonTrack = Sequence()
    if (repeatNPC == 0):
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


    # object appears above suit
    objectTrack = Sequence()

    def posObject(object, suit, level, majorObject, miss,
                  battle=battle):
        object.reparentTo(battle)
        # Options for positioning a drop:
        #   1) Any successful drop on an unlured suit - strikes at suit battle pos
        #   2) Unsuccessful drops on an unlured suit that are of the largest three -
        #      these strike behind the suit (who shouldn't dodge)
        #   3) The first three (smallest drops) on a lured suit strike the battle pos,
        #      where the larger ones get bumped back a bit.
        if (battle.isSuitLured(suit)):
            # suit is lured, strike at battle position
            suitPos, suitHpr = battle.getActorPosHpr(suit)
            object.setPos(suitPos)
            object.setHpr(suitHpr)
            if (level >= 3): # bump back larger drops
                object.setY(object.getY() + 2)
        else:
            object.setPos(suit.getPos(battle))
            object.setHpr(suit.getHpr(battle))
            if (miss and level >= 3):
                object.setY(object.getY(battle) + 5)

        if not majorObject:
            if not miss:
                shoulderHeight = shoulderHeights[suit.style.body] * suit.scale
                object.setZ(object.getPos(battle)[2] + shoulderHeight)
        # fix up the Z offset of the prop
        object.setZ(object.getPos(battle)[2] + objZOffsets[level])

    # the object will need to scale down to nothing at some point
    # and then it will immediately get deleted
    # since we already have an animation interval playing,
    # we need to put the scale on a separate track.
    # to avoid cases where the object has been deleted,
    # and the scale interval is still trying to scale the
    # object, we'll put the animation and scale intervals into
    # separate tracks, combine them into a track, and
    # put the hide interval after the track.
    objectTrack.append(Func(battle.movie.needRestoreRenderProp, object))
    objInit = Func(posObject, object, suit, level, majorObject, (hp <= 0))
    objectTrack.append(Wait(delay + tObjectAppears))
    objectTrack.append(objInit)

    # we can assume that all drop props are animated
    if hp > 0 or (level == 1 or level == 2):
        # prop hits the suit
        #import pdb; pdb.set_trace()
        if hasattr(object,'getAnimControls'):
            animProp = ActorInterval(object, objName)
            shrinkProp = LerpScaleInterval(object, dShrink, Point3(0.01, 0.01, 0.01), startScale = object.getScale())
            objAnimShrink = ParallelEndTogether(animProp, shrinkProp)
            objectTrack.append(objAnimShrink)
        else:
            # donald boat currently does not have animation
            startingScale = objStartingScales[level]
            object2 = MovieUtil.copyProp(object)
            posObject(object2, suit, level, majorObject, (hp <= 0))
            endingPos = object2.getPos()
            startPos = Point3( endingPos[0], endingPos[1] , endingPos[2] + 5)
            startHpr = object2.getHpr()
            endHpr = Point3( startHpr[0] + 90, startHpr[1], startHpr[2])

            animProp = LerpPosInterval(object, landFrames[level]/24.0,
                                       endingPos, startPos = startPos)
            shrinkProp = LerpScaleInterval(object, dShrink, Point3(0.01, 0.01, 0.01), startScale = startingScale)
 
            bounceProp = Effects.createZBounce(object, 2, endingPos,  0.5, 1.5)
           
            #objAnimShrink = ParallelEndTogether(animProp, shrinkProp)
            objAnimShrink = Sequence( Func(object.setScale, startingScale),
                                      Func(object.setH, endHpr[0]),
                                      animProp,
                                      bounceProp,
                                      Wait(1.5),
                                      shrinkProp)
            

            objectTrack.append(objAnimShrink)

            MovieUtil.removeProp( object2)

            
    else:
        # prop misses the suit
        # only play the animation up to the point where it lands
        if hasattr(object,'getAnimControls'):        
            animProp = ActorInterval(object, objName, duration=landFrames[level]/24.)
            def poseProp(prop, animName, level):
                prop.pose(animName, landFrames[level])
            poseProp = Func(poseProp, object, objName, level)
            wait = Wait(1.0)
            shrinkProp = LerpScaleInterval(object, dShrinkOnMiss, Point3(0.01, 0.01, 0.01), startScale = object.getScale())
            objectTrack.append(animProp)
            objectTrack.append(poseProp)
            objectTrack.append(wait)
            objectTrack.append(shrinkProp)
        else:
            #donald boat currently does not have animation            
            startingScale = objStartingScales[level]
            object2 = MovieUtil.copyProp(object)
            posObject(object2, suit, level, majorObject, (hp <= 0))
            endingPos = object2.getPos()
            startPos = Point3( endingPos[0], endingPos[1] , endingPos[2] + 5)
            startHpr = object2.getHpr()
            endHpr = Point3( startHpr[0] + 90, startHpr[1], startHpr[2])
            
            
            animProp = LerpPosInterval(object, landFrames[level]/24.0,
                                       endingPos, startPos = startPos)
            shrinkProp = LerpScaleInterval(object, dShrinkOnMiss, Point3(0.01, 0.01, 0.01), startScale = startingScale)

            bounceProp = Effects.createZBounce(object, 2, endingPos,  0.5, 1.5)

            #objAnimShrink = ParallelEndTogether(animProp, shrinkProp)
            objAnimShrink = Sequence( Func(object.setScale, startingScale),
                                      Func(object.setH, endHpr[0]),
                                      animProp,
                                      bounceProp,
                                      Wait(1.5),
                                      shrinkProp)
            objectTrack.append(objAnimShrink)
            MovieUtil.removeProp( object2)            
            

    objectTrack.append(Func(MovieUtil.removeProp, object))
    objectTrack.append(Func(battle.movie.clearRenderProp, object))

    # we will see a shadow scale up before the object drops
    dropShadow = MovieUtil.copyProp(suit.getShadowJoint())
    if (level == 0):
        dropShadow.setScale(0.5)
    elif (level <= 2):
        dropShadow.setScale(0.8)
    elif (level == 3):
        dropShadow.setScale(2.0)
    elif (level == 4):
        dropShadow.setScale(2.3)
    else:
        dropShadow.setScale(3.6)

    def posShadow(dropShadow=dropShadow, suit=suit, battle=battle, hp=hp, level=level):
        dropShadow.reparentTo(battle)
        if (battle.isSuitLured(suit)):
            # suit is lured, shadow at battle position
            suitPos, suitHpr = battle.getActorPosHpr(suit)
            dropShadow.setPos(suitPos)
            dropShadow.setHpr(suitHpr)
            if (level >= 3): # bump back larger drops
                dropShadow.setY(dropShadow.getY() + 2)
        else:
            dropShadow.setPos(suit.getPos(battle))
            dropShadow.setHpr(suit.getHpr(battle))
            if (hp <= 0 and level >= 3):
                dropShadow.setY(dropShadow.getY(battle) + 5)
        # Raise the drop shadow to curb level
        dropShadow.setZ(dropShadow.getZ() + 0.5)

    shadowTrack = Sequence(
        Wait(delay+tButtonPressed),
        Func(battle.movie.needRestoreRenderProp, dropShadow),
        Func(posShadow),
        LerpScaleInterval(dropShadow, tObjectAppears - tButtonPressed,
                          dropShadow.getScale(), startScale = Point3(0.01, 0.01, 0.01)),
        Wait(0.3),
        Func(MovieUtil.removeProp, dropShadow),
        Func(battle.movie.clearRenderProp, dropShadow),
        )

    return Parallel(toonTrack, soundTrack, buttonTrack, objectTrack, shadowTrack)
        
def __createSuitTrack(drop, delay,level, alreadyDodged, alreadyTeased,
                      target, npcs):
    toon = drop['toon']
    if (drop.has_key('npc')):
        toon = drop['npc']
    battle = drop['battle']
    
    majorObject = (level >= 3)    
    suit = target['suit']
    hp = target['hp']
    hitSuit = (hp > 0)
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    kbbonus = target['kbbonus']
    hpbonus = drop['hpbonus']
    
    # 4 options for a suit in a drop attack:
    #  1) It takes damage and reacts (hp > 0)
    #  2) It is lured, thus drop misses so suit does nothing (kbbonus == 0).  This is
    #     detected using a hack in the kbbonus.  There is no actual kickback bonus involved
    #     for drops, but if this kbbonus value is set to 0 instead of -1 (in the battle
    #     calculator), then we've specified that the suit is lured
    #  3) The suit dodges and is reacting to the first drop to dodge, detected when the
    #     variable alreadyDodged == 0
    #  4) The suit would dodge but is already dodging first drop, detected when the
    #     variable alreadyDodged == 1
    if (hp > 0):
        # Suit takes damage (for each drop that hits)
        suitTrack = Sequence()
        showDamage = Func(suit.showHpText, -hp, openEnded=0)
        updateHealthBar = Func(suit.updateHealthBar, hp)
        if majorObject:
            anim = 'flatten'
        else:
            anim = 'drop-react'
        suitReact = ActorInterval(suit, anim)
        suitTrack.append(Wait(delay+tObjectAppears))
        suitTrack.append(showDamage)
        suitTrack.append(updateHealthBar)
        suitGettingHit = Parallel( suitReact)
        if level == UBER_GAG_LEVEL_INDEX:
            gotHitSound = globalBattleSoundCache.getSound('AA_drop_boat_cog.mp3')
            suitGettingHit.append(SoundInterval(gotHitSound,  node=toon))
        suitTrack.append(suitGettingHit)        
        # Create a bonus track if there is an hp bonus
        bonusTrack = None
        if (hpbonus > 0):
            bonusTrack = Sequence(Wait(delay + tObjectAppears + 0.75),
                                  Func(suit.showHpText,
                                       -hpbonus, 1, openEnded=0))
        if (revived != 0):
            suitTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, 
                                                battle, npcs))
        elif (died != 0):
            suitTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, 
                                                battle, npcs))
        else:
            suitTrack.append(Func(suit.loop, 'neutral'))
            

        if (bonusTrack != None):
            suitTrack = Parallel(suitTrack, bonusTrack)

    elif (kbbonus == 0):
        # If suit is lured, doesn't need to dodge and certainly won't get hit
        suitTrack = Sequence(
            Wait(delay+tObjectAppears),
            Func(MovieUtil.indicateMissed, suit, 0.6),
            Func(suit.loop, 'neutral'),
            )
    else:
        # Conditions regarding dodging:
        #    1) The suit will dodge only once with multiple drops in the same attack,
        #       so we only dodge if we haven't already (alreadyDodged==0)
        #    2) The suit will not NEED to dodge if attacked by a larger drop (which fall
        #       behind the suit on a miss rather than having the suit dodge
        # Special conditions:
        #    1) If there's a large drop followed by a small one at some point, we can allow
        #       the suit to start teasing and then dogde, this looks fine
        #    2) If there's a small drop followed by a large drop at some point, we don't allow
        #       the suit to tease, doesn't look right
        # other suits may need to dodge as well

        # First check if suit started dodging, if so, do not add any another reaction
        if (alreadyDodged > 0):
            return None #Parallel(toonTrack, soundTrack, buttonTrack, objectTrack, shadowTrack)

        # Check for large drops
        if (level >= 3): # the larger drops, suit doesn't dodge, but teases instead
            # But if we've already started to tease, don't tease more than once
            if (alreadyTeased > 0):
                return None #Parallel(toonTrack, soundTrack, buttonTrack, objectTrack, shadowTrack)
            else:
                suitTrack = MovieUtil.createSuitTeaseMultiTrack(
                    suit, delay=delay+tObjectAppears)

        else: # small drop, so dodge
            suitTrack = MovieUtil.createSuitDodgeMultitrack(
                delay + tSuitDodges, suit, leftSuits, rightSuits)
        
    return suitTrack

