from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from BattleSounds import *
from toontown.toon.ToonDNA import *
from toontown.suit.SuitDNA import *


import MovieUtil
import MovieCamera
from direct.directnotify import DirectNotifyGlobal
import BattleParticles
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
import random

notify = DirectNotifyGlobal.directNotify.newCategory('MovieSquirt')

hitSoundFiles = ('AA_squirt_flowersquirt.mp3',
              'AA_squirt_glasswater.mp3',
              'AA_squirt_neonwatergun.mp3',
              'AA_squirt_seltzer.mp3',
              'firehose_spray.mp3',
              'AA_throw_stormcloud.mp3',
              'AA_squirt_Geyser.mp3') #UBER

missSoundFiles = ('AA_squirt_flowersquirt_miss.mp3',
              'AA_squirt_glasswater_miss.mp3',
              'AA_squirt_neonwatergun_miss.mp3',
              'AA_squirt_seltzer_miss.mp3',
              'firehose_spray.mp3',
              'AA_throw_stormcloud_miss.mp3',
              'AA_squirt_Geyser.mp3') #UBER

sprayScales = [0.2, 0.3, 0.1, 0.6, 0.8, 1.0, 2.0] #UBER

WaterSprayColor = Point4(0.75, 0.75, 1.0, 0.8)

def doSquirts(squirts):
    """ Squirts occur in the following order:
        a) by suit, in order of increasing number of squirts per suit
          1) level 1 squirts, right to left, (TOON_SQUIRT_DELAY later)
          2) level 2 squirts, right to left, (TOON_SQUIRT_DELAY later)
          3) level 3 squirts, right to left, (TOON_SQUIRT_DELAY later)
          etc.
        b) next suit, (TOON_SQUIRT_SUIT_DELAY later)
    """
    if (len(squirts) == 0):
        return (None, None)

    # Group the squirts by targeted suit
    suitSquirtsDict = {}
    doneUber = 0
    skip = 0

    for squirt in squirts:
        skip = 0
        #if squirt["level"] >= ToontownBattleGlobals.UBER_GAG_LEVEL_INDEX:
        #    if doneUber:
        #        skip = 1
        #    doneUber = 1
        if skip:
            pass
        else:
            #print("squirt in squirts")
            if type(squirt['target']) == type([]): #if target is a list
                #for target in squirt['target']:
                if 1:
                    target = squirt['target'][0]
                    suitId = target['suit'].doId
                    if (suitSquirtsDict.has_key(suitId)):
                        suitSquirtsDict[suitId].append(squirt)
                    else:
                        suitSquirtsDict[suitId] = [squirt]
            else:
                suitId = squirt['target']['suit'].doId
                if (suitSquirtsDict.has_key(suitId)):
                    suitSquirtsDict[suitId].append(squirt)
                else:
                    suitSquirtsDict[suitId] = [squirt]
    suitSquirts = suitSquirtsDict.values()

    # Sort the suits based on the number of squirts per suit
    def compFunc(a, b):
        if (len(a) > len(b)):
            return 1
        elif (len(a) < len(b)):
            return -1
        return 0
    suitSquirts.sort(compFunc)
    delay = 0.0
    mtrack = Parallel()
    for st in suitSquirts:
        #print("st in suitSquirts")
        if (len(st) > 0):
            ival = __doSuitSquirts(st)
            if (ival):
                mtrack.append(Sequence(Wait(delay), ival))
            delay = delay + TOON_SQUIRT_SUIT_DELAY

    camDuration = mtrack.getDuration()
    camTrack = MovieCamera.chooseSquirtShot(squirts, suitSquirtsDict,
                                            camDuration)

    return (mtrack, camTrack)

def __doSuitSquirts(squirts):
    """ __doSuitSquirts(squirts)
        Create the intervals for the attacks on one suit.
        1 or more toons can squirt at the same target suit
        Note: attacks are sorted by increasing level (as are toons)
        Returns a multitrack with toon squirts in the following order:
        1) level 1 squirts, right to left, (TOON_SQUIRT_DELAY later)
        2) level 2 squirts, right to left, (TOON_SQUIRT_DELAY later)
        etc.
    """
    uberClone = 0
    toonTracks = Parallel()
    delay = 0.0

    # Determine how many times the suit is hit, if only once, play stun effect
    if type(squirts[0]['target']) == type([]): #is target is a list?
        for target in squirts[0]['target']:
            if ((len(squirts) == 1) and (target['hp'] > 0)):
                fShowStun = 1
            else:
                fShowStun = 0
    else:
        if ((len(squirts) == 1) and (squirts[0]['target']['hp'] > 0)):
            fShowStun = 1
        else:
            fShowStun = 0
    #import pdb; pdb.set_trace()
    for s in squirts:
        #print("s in squirts")
        tracks = __doSquirt(s, delay, fShowStun, uberClone)
        if s["level"] >= ToontownBattleGlobals.UBER_GAG_LEVEL_INDEX:
            uberClone = 1
        if tracks:
            for track in tracks:
                toonTracks.append(track)
        delay = delay + TOON_SQUIRT_DELAY
    return toonTracks

def __doSquirt(squirt, delay, fShowStun, uberClone = 0):
    #print("__doSquirt")
    squirtSequence = Sequence(Wait(delay))
    if type(squirt['target']) == type([]): #is target is a list?
        for target in squirt['target']:
            notify.debug('toon: %s squirts prop: %d at suit: %d for hp: %d' % \
                     (squirt['toon'].getName(), squirt['level'],
                      target['suit'].doId, target['hp']))
    else:
        notify.debug('toon: %s squirts prop: %d at suit: %d for hp: %d' % \
                     (squirt['toon'].getName(), squirt['level'],
                      squirt['target']['suit'].doId, squirt['target']['hp']))
    if uberClone:
        ival = squirtfn_array[squirt['level']](squirt, delay, fShowStun, uberClone)
        if ival:
            squirtSequence.append(ival)
    else:
        ival = squirtfn_array[squirt['level']](squirt, delay, fShowStun)
        if ival:
            squirtSequence.append(ival)
    return [squirtSequence]

def __suitTargetPoint(suit):
    pnt = suit.getPos(render)
    pnt.setZ(pnt[2] + suit.getHeight()*0.66)
    return Point3(pnt)

def __getSplashTrack(point, scale, delay, battle, splashHold=0.01):
    # TODO: we should be using the real splash animated texture
    # as soon as the visibility is fixed

    def prepSplash(splash, point):
        if callable(point):
            point = point()
        splash.reparentTo(render)
        splash.setPos(point)
        scale = splash.getScale()
        splash.setBillboardPointWorld()
        splash.setScale(scale)
    splash = globalPropPool.getProp('splash-from-splat')
    splash.setScale(scale)
    return Sequence(
        Func(battle.movie.needRestoreRenderProp, splash),
        Wait(delay),
        Func(prepSplash, splash, point),
        ActorInterval(splash, 'splash-from-splat'),
        Wait(splashHold),
        Func(MovieUtil.removeProp, splash),
        Func(battle.movie.clearRenderProp, splash))

def __getSuitTrack(suit, tContact, tDodge, hp, hpbonus, kbbonus, anim,
                   died, leftSuits, rightSuits, battle, toon, fShowStun,
                   beforeStun = 0.5, afterStun = 1.8, geyser = 0, uberRepeat = 0, revived = 0):
    if (hp > 0):
        suitTrack = Sequence()
        sival = ActorInterval(suit, anim)
        sival = [] # Suit interval of its animation
        if (kbbonus > 0) and not geyser: # If there's a knockback, then animate the suit falling back
            suitPos, suitHpr = battle.getActorPosHpr(suit)
            suitType = getSuitBodyType(suit.getStyleName())
            animTrack = Sequence()
            animTrack.append(ActorInterval(suit, anim, duration=0.2))
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
        elif geyser:
            #print("getting suit geyser track")
            suitStartPos = suit.getPos()
            suitFloat = Point3(0,0,14)
            suitEndPos = Point3(suitStartPos[0] + suitFloat[0],
                                suitStartPos[1] + suitFloat[1],
                                suitStartPos[2] + suitFloat[2])
            #sival = ActorInterval(suit, 'slip-backward', playRate = 0.50)
            #sival = ActorInterval(suit, 'flail', playRate = 0.50)
            suitType = getSuitBodyType(suit.getStyleName())
            if suitType == 'a':
                startFlailFrame = 16
                endFlailFrame = 16#27

            elif suitType == 'b':
                startFlailFrame = 15
                endFlailFrame = 15#22

            else:
                startFlailFrame = 15
                endFlailFrame = 15#20


            sival = Sequence(
                            ActorInterval(suit, 'slip-backward', playRate = 0.5, startFrame=0, endFrame=startFlailFrame-1),
                            Func(suit.pingpong, 'slip-backward', fromFrame=startFlailFrame, toFrame=endFlailFrame),
                            Wait(0.5),
                            ActorInterval(suit, 'slip-backward', playRate = 1.00, startFrame = endFlailFrame),
                            )

            sUp = LerpPosInterval(suit, 1.1,
                                suitEndPos,
                                startPos=suitStartPos,
                                fluid = 1)
            sDown = LerpPosInterval(suit, 0.6,
                                suitStartPos,
                                startPos=suitEndPos,
                                fluid = 1)

        else:
            if fShowStun == 1:
                sival = Parallel(
                    ActorInterval(suit, anim),
                    MovieUtil.createSuitStunInterval(
                    suit, beforeStun, afterStun),
                    )
            else:
                sival = ActorInterval(suit, anim)
        showDamage = Func(suit.showHpText, -hp, openEnded=0, attackTrack=SQUIRT_TRACK)
        updateHealthBar = Func(suit.updateHealthBar, hp)
        suitTrack.append(Wait(tContact))
        suitTrack.append(showDamage)
        suitTrack.append(updateHealthBar)
        if not geyser:
            suitTrack.append(sival)
        else:
            if not uberRepeat:
                geyserMotion = Sequence(sUp, Wait(0.0), sDown)
                suitLaunch = Parallel(sival, geyserMotion)
                suitTrack.append(suitLaunch)
            else:
                suitTrack.append(Wait(5.5))

        # Make a bonus track for any hp bonus
        bonusTrack = Sequence(Wait(tContact))
        if (kbbonus > 0):
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -kbbonus, 2, openEnded=0, attackTrack=SQUIRT_TRACK))
        if (hpbonus > 0):
            bonusTrack.append(Wait(0.75))
            bonusTrack.append(Func(suit.showHpText, -hpbonus, 1, openEnded=0, attackTrack=SQUIRT_TRACK))
        if (died != 0):
            suitTrack.append(MovieUtil.createSuitDeathTrack(suit, toon, battle))
        else:
            suitTrack.append(Func(suit.loop, 'neutral'))
        if (revived != 0):
            suitTrack.append(MovieUtil.createSuitReviveTrack(suit, toon, battle))

        return Parallel(suitTrack, bonusTrack)

    else:
        # suit dodges
        # other suits may need to dodge as well
        return MovieUtil.createSuitDodgeMultitrack(tDodge, suit,
                                                   leftSuits, rightSuits)

def say(statement):
    print(statement)

def __getSoundTrack(level, hitSuit, delay, node=None):
    #level: the level of attack, int 0-5
    #hitSuit: does the attack hit toon, bool
    #delay: time delay before playing sound

    if hitSuit:
        soundEffect = globalBattleSoundCache.getSound(hitSoundFiles[level])
    else:
        soundEffect = globalBattleSoundCache.getSound(missSoundFiles[level])

    soundTrack = Sequence()
    if soundEffect:
        soundTrack.append(Wait(delay))
        soundTrack.append(SoundInterval(soundEffect, node=node))

    return soundTrack

def __doFlower(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = (hp > 0)

    scale = sprayScales[level]

    tTotalFlowerToonAnimationTime = 2.5  # hardcoded by the animation
    tFlowerFirstAppears = 1.0            # set the flower to appear after this time
    dFlowerScaleTime    = 0.5            # total time it will take flower to scale up/dwn

    tSprayStarts = tTotalFlowerToonAnimationTime
    dSprayScale = 0.2
    dSprayHold = 0.1
    tContact = tSprayStarts + dSprayScale
    tSuitDodges = tTotalFlowerToonAnimationTime

    tracks = Parallel()

    button = globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    hands = toon.getLeftHands()

    toonTrack = Sequence(
        Func(MovieUtil.showProps, buttons, hands),
        Func(toon.headsUp, battle, suitPos),
        ActorInterval(toon, 'pushbutton'),
        Func(MovieUtil.removeProps, buttons),
        Func(toon.loop, 'neutral'),
        Func(toon.setHpr, battle, origHpr),
        )

    tracks.append(toonTrack)

    # create sound track
    tracks.append(__getSoundTrack(level, hitSuit, tTotalFlowerToonAnimationTime-0.4, toon))

    # show the flower
    flower = globalPropPool.getProp('squirting-flower')
    flower.setScale(1.5, 1.5, 1.5)

    # prepare the spray
    targetPoint = lambda suit=suit: __suitTargetPoint(suit)

    def getSprayStartPos(flower=flower):
        # flower is parented to LOD 0 path, so make sure this LOD is being animated
        # before we get the flower position
        # should I parent to LOD 2 instead to reduce expense of update()?

        #note:  dont have to call toon.pose() since getSprayStartPos isnt called
        #       until the exact frame we need the flower pos
        toon.update(0)  # force update of LOD 0 to current animation frame (dont know if it is being displayed or not)
        return flower.getPos(render)

    sprayTrack = MovieUtil.getSprayTrack(
        battle, WaterSprayColor,
        getSprayStartPos, targetPoint,
        dSprayScale, dSprayHold, dSprayScale,
        horizScale = scale, vertScale = scale)
    lodnames = toon.getLODNames()

    # dont bother with LOD 2 intervals for now since viewer will be very far away flower will be too small to see
    toonlod0 = toon.getLOD(lodnames[0])
    toonlod1 = toon.getLOD(lodnames[1])
    if base.config.GetBool('want-new-anims', 1):
        if not toonlod0.find('**/def_joint_attachFlower').isEmpty():
            flower_joint0 = toonlod0.find('**/def_joint_attachFlower')
    else:
        flower_joint0 = toonlod0.find('**/joint_attachFlower')

    if base.config.GetBool('want-new-anims', 1):
        if not toonlod1.find('**/def_joint_attachFlower').isEmpty():
            flower_joint1 = toonlod1.find('**/def_joint_attachFlower')
    else:
        flower_joint1 = toonlod1.find('**/joint_attachFlower')

    # scale flower only once, use instances to create nodepaths attaching
    # all LOD joints to the 1 flower
    flower_jointpath0 = flower_joint0.attachNewNode('attachFlower-InstanceNode')
    flower_jointpath1 = flower_jointpath0.instanceTo(flower_joint1)

    # show the flower
    flowerTrack = Sequence( # this series of intervals will take tTotalFlowerToonAnimationTime
        # wait
        Wait(tFlowerFirstAppears),

        # parent the flower to the toon joint LOD 0 only (this is used by getSprayStartPos)
        Func(flower.reparentTo, flower_jointpath0),
        # scale the flower up
        LerpScaleInterval(flower, dFlowerScaleTime,
                          flower.getScale(), startScale=MovieUtil.PNT3_NEARZERO),
        # wait until toon presses the button
        Wait(tTotalFlowerToonAnimationTime-dFlowerScaleTime-tFlowerFirstAppears),
        )

    if hp <= 0:
        # If we're going to miss, give the suit a chance to dodge.
        flowerTrack.append(Wait(0.5))
    flowerTrack.append(sprayTrack) # Add in the spray
    # Now scale down and delete the flower
    flowerTrack.append(LerpScaleInterval(flower, dFlowerScaleTime, MovieUtil.PNT3_NEARZERO))

    # must get rid of stuff created by attachNewNode and instanceTo
    # eventually would like to just create these once and parent to joint at load time
    flowerTrack.append(Func(flower_jointpath1.removeNode))
    flowerTrack.append(Func(flower_jointpath0.removeNode))
    flowerTrack.append(Func(MovieUtil.removeProp, flower))

    tracks.append(flowerTrack)

    # do the splash
    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, scale,
                                       tSprayStarts + dSprayScale, battle))

    # Do the suit reaction
    # If the suit takes damage (hp > 0) or this squirt is the first one to strike (delay = 0)
    # then we naturally add a suit track, otherwise we don't so that a suit won't dodge
    # multiple times on sequential squirts in the same attack
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp,
                                     hpbonus, kbbonus, 'squirt-small-react',
                                     died, leftSuits, rightSuits, battle,
                                     toon, fShowStun, revived = revived))

    return tracks

def __doWaterGlass(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = (hp > 0)

    scale = sprayScales[level]

    dGlassHold  = 5.
    dGlassScale = 0.5
    tSpray = (82. / toon.getFrameRate('spit'))
    sprayPoseFrame = 88
    dSprayScale = 0.1
    dSprayHold = 0.1
    tContact = tSpray + dSprayScale
    tSuitDodges = max(tSpray - 0.5, 0.)

    tracks = Parallel()

    # toon
    tracks.append(ActorInterval(toon, 'spit'))

    # sound
    soundTrack = __getSoundTrack(level, hitSuit, 1.7, toon)
    tracks.append(soundTrack)

    glass = globalPropPool.getProp('glass')
    hands = toon.getRightHands()

    # scale glass only once, use instances to create nodepaths attaching
    # all LOD hand joints to the 1 glass.  would like to do this once at init time eventually
    hand_jointpath0 = hands[0].attachNewNode('handJoint0-path')
    hand_jointpath1 = hand_jointpath0.instanceTo(hands[1])

    glassTrack = Sequence(
        Func(MovieUtil.showProp, glass, hand_jointpath0),
        ActorInterval(glass,'glass'),
        # must get rid of stuff created by attachNewNode and instanceTo
        # eventually would like to just create these once and parent to joint at load time
        Func(hand_jointpath1.removeNode),
        Func(hand_jointpath0.removeNode),
        Func(MovieUtil.removeProp, glass),
        )
    tracks.append(glassTrack)

    # do the spray
    targetPoint = lambda suit=suit: __suitTargetPoint(suit)
    def getSprayStartPos(toon=toon):
        toon.update(0)   # force update of LOD 0 to current animation frame (dont know if it is being displayed or not)
        lod0 = toon.getLOD(toon.getLODNames()[0])

        if base.config.GetBool('want-new-anims', 1):
            if not lod0.find("**/def_head").isEmpty():
                joint = lod0.find("**/def_head")
            else:
                joint = lod0.find("**/joint_head")
        else:
            joint = lod0.find("**/joint_head")

        n = hidden.attachNewNode('pointInFrontOfHead')
        n.reparentTo(toon)
        n.setPos(joint.getPos(toon) + Point3(0, 0.3, -0.2))  # TODO: adjust this based on snout length
        p = n.getPos(render)
        n.removeNode()
        del n
        return p

    sprayTrack = MovieUtil.getSprayTrack(
        battle, WaterSprayColor,
        getSprayStartPos, targetPoint,
        dSprayScale, dSprayHold, dSprayScale,
        horizScale = scale, vertScale = scale)

    tracks.append(Sequence(Wait(tSpray), sprayTrack))

    # do the splash
    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, scale,
                                       tSpray + dSprayScale, battle))

    # Do the suit reaction
    # If the suit takes damage (hp > 0) or this squirt is the first one to strike (delay = 0)
    # then we naturally add a suit track, otherwise we don't so that a suit won't dodge
    # multiple times on sequential squirts in the same attack
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp,
                                     hpbonus, kbbonus, 'squirt-small-react',
                                     died, leftSuits, rightSuits, battle,
                                     toon, fShowStun, revived = revived))

    return tracks

def __doWaterGun(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = (hp > 0)

    scale = sprayScales[level]

    tPistol = 0.
    dPistolScale = 0.5
    dPistolHold = 1.8
    tSpray = 48.0 / toon.getFrameRate('water-gun')
    sprayPoseFrame = 63
    dSprayScale = 0.1
    dSprayHold = 0.3
    tContact = tSpray + dSprayScale
    tSuitDodges = 1.1

    tracks = Parallel()

    # animate the toon
    toonTrack = Sequence(
        Func(toon.headsUp, battle, suitPos),
        ActorInterval(toon, 'water-gun'),
        Func(toon.loop, 'neutral'),
        Func(toon.setHpr, battle, origHpr),
        )
    tracks.append(toonTrack)

    # add the sound
    soundTrack = __getSoundTrack(level, hitSuit, 1.8, toon)
    tracks.append(soundTrack)

    # prepare the water pistol
    pistol = globalPropPool.getProp('water-gun')
    hands = toon.getRightHands()

    # scale gun only once, use instances to create nodepaths attaching
    # all LOD hand joints to the 1 gun
    hand_jointpath0 = hands[0].attachNewNode('handJoint0-path')
    hand_jointpath1 = hand_jointpath0.instanceTo(hands[1])

    # prepare the spray
    targetPoint = lambda suit=suit: __suitTargetPoint(suit)

    def getSprayStartPos(pistol=pistol, toon=toon):
        #note:  dont have to call toon.pose() since getSprayStartPos isnt called
        #       until the exact frame we need the posn, so the animation has already been updated
        toon.update(0)   # force update of LOD 0 to current animation frame (dont know if it is being displayed or not)
        joint = pistol.find("**/joint_nozzle")
        p = joint.getPos(render)
        return p

    sprayTrack = MovieUtil.getSprayTrack(
        battle, WaterSprayColor,
        getSprayStartPos, targetPoint,
        dSprayScale, dSprayHold, dSprayScale,
        horizScale = scale, vertScale = scale)

    # Must include the spray intervals with the gun
    # to avoid parenting to a null node
    pistolPos = Point3(0.28, 0.10, 0.08)
    pistolHpr = VBase3(85.60, -4.44, 94.43)

    pistolTrack = Sequence(
        Func(MovieUtil.showProp,
             pistol, hand_jointpath0, pistolPos, pistolHpr),
        LerpScaleInterval(pistol, dPistolScale, pistol.getScale(),
                          startScale=MovieUtil.PNT3_NEARZERO),
        Wait(tSpray-dPistolScale), # Wait before spraying
        )

    pistolTrack.append(sprayTrack)
    pistolTrack.append(Wait(dPistolHold))# Wait before losing the pistol
    pistolTrack.append(LerpScaleInterval(pistol, dPistolScale, MovieUtil.PNT3_NEARZERO))

    # must get rid of stuff created by attachNewNode and instanceTo
    # eventually would like to just create these once and parent to joint at load time
    pistolTrack.append(Func(hand_jointpath1.removeNode))
    pistolTrack.append(Func(hand_jointpath0.removeNode))
    pistolTrack.append(Func(MovieUtil.removeProp, pistol))

    tracks.append(pistolTrack)

    if hp > 0: # do the splash
        tracks.append(__getSplashTrack(targetPoint, 0.3,
                                       tSpray + dSprayScale, battle))

    # Do the suit reaction
    # If the suit takes damage (hp > 0) or this squirt is the first one to strike (delay = 0)
    # then we naturally add a suit track, otherwise we don't so that a suit won't dodge
    # multiple times on sequential squirts in the same attack
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp,
                                     hpbonus, kbbonus, 'squirt-small-react',
                                     died, leftSuits, rightSuits, battle,
                                     toon, fShowStun, revived = revived))

    return tracks

def __doSeltzerBottle(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = (hp > 0)

    scale = sprayScales[level]

    tBottle = 0.
    dBottleScale = 0.5
    dBottleHold = 3.
    tSpray = (53.0 / toon.getFrameRate('hold-bottle')) + 0.05
    dSprayScale = 0.2
    dSprayHold = 0.1
    tContact = tSpray + dSprayScale
    tSuitDodges = max(tContact - 0.7, 0.)

    tracks = Parallel()

    # animate the toon
    toonTrack = Sequence(
        Func(toon.headsUp, battle, suitPos),
        ActorInterval(toon, 'hold-bottle'),
        Func(toon.loop, 'neutral'),
        Func(toon.setHpr, battle, origHpr),
        )
    tracks.append(toonTrack)

    # add sound
    soundTrack = __getSoundTrack(level, hitSuit, tSpray - 0.1, toon)
    tracks.append(soundTrack)

    # do the seltzer bottle
    bottle = globalPropPool.getProp('bottle')
    hands = toon.getRightHands()

    # make the spray interval
    targetPoint = lambda suit=suit: __suitTargetPoint(suit)
    def getSprayStartPos(bottle=bottle, toon=toon):
        #note:  dont have to call toon.pose() since getSprayStartPos isnt called
        #       until the exact frame we need the posn, so the animation has already been updated
        toon.update(0)   # force update of LOD 0 to current animation frame (dont know if it is being displayed or not)
        joint = bottle.find("**/joint_toSpray")
        n = hidden.attachNewNode('pointBehindSprayProp')
        n.reparentTo(toon)
        n.setPos(joint.getPos(toon) + Point3(0, -0.4, 0))
        p = n.getPos(render)
        n.removeNode()
        del n
        return p

    sprayTrack = MovieUtil.getSprayTrack(
        battle, WaterSprayColor,
        getSprayStartPos, targetPoint,
        dSprayScale, dSprayHold, dSprayScale,
        horizScale = scale, vertScale = scale)

    # scale bottle only once, use instances to create nodepaths attaching
    # all LOD hand joints to the 1 bottle
    hand_jointpath0 = hands[0].attachNewNode('handJoint0-path')
    hand_jointpath1 = hand_jointpath0.instanceTo(hands[1])

    bottleTrack = Sequence(
         Func(MovieUtil.showProp, bottle, hand_jointpath0),
         LerpScaleInterval(bottle, dBottleScale,
                           bottle.getScale(), startScale=MovieUtil.PNT3_NEARZERO),
         Wait(tSpray-dBottleScale), # Wait before spraying
         )

    bottleTrack.append(sprayTrack)
    bottleTrack.append(Wait(dBottleHold))  # Wait before losing the bottle
    bottleTrack.append(LerpScaleInterval(bottle, dBottleScale, MovieUtil.PNT3_NEARZERO))

    # must get rid of stuff created by attachNewNode and instanceTo
    # eventually would like to just create these once and parent to joint at load time
    bottleTrack.append(Func(hand_jointpath1.removeNode))
    bottleTrack.append(Func(hand_jointpath0.removeNode))
    bottleTrack.append(Func(MovieUtil.removeProp, bottle))

    tracks.append(bottleTrack)

    # do the splash
    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, scale,
                                       tSpray + dSprayScale, battle))

    # Do the suit reaction
    # If the suit takes damage (hp > 0) or this squirt is the first one to strike (delay = 0)
    # then we naturally add a suit track, otherwise we don't so that a suit won't dodge
    # multiple times on sequential squirts in the same attack
    if (hp > 0 or delay <= 0) and suit:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp,
                                     hpbonus, kbbonus, 'squirt-small-react',
                                     died, leftSuits, rightSuits, battle,
                                     toon, fShowStun, revived = revived))

    return tracks

def __doFireHose(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = (hp > 0)
    scale = 0.3

    tAppearDelay = 0.7
    dHoseHold = 0.7
    dAnimHold = 5.1
    tSprayDelay = 2.8
    tSpray = 0.2
    dSprayScale = 0.1
    dSprayHold = 1.8
    tContact = 2.9
    tSuitDodges = 2.1

    tracks = Parallel()

    # animate the toon
    toonTrack = Sequence(
        Wait(tAppearDelay), # Wait a bit for the hydrant and hose to appear
        Func(toon.headsUp, battle, suitPos),
        ActorInterval(toon, 'firehose'),
        Func(toon.loop, 'neutral'),
        Func(toon.setHpr, battle, origHpr),
        )
    tracks.append(toonTrack)

    # add sound
    soundTrack = __getSoundTrack(level, hitSuit, tSprayDelay, toon)
    tracks.append(soundTrack)

    # prepare the fire hose and hydrant.
    hose = globalPropPool.getProp('firehose')
    hydrant = globalPropPool.getProp('hydrant')
    hose.reparentTo(hydrant)
    hose.pose('firehose', 2),

    # Create a node to inherit any animal scale and cheesy effect
    # scale.
    hydrantNode = toon.attachNewNode('hydrantNode')
    hydrantNode.clearTransform(toon.getGeomNode().getChild(0))

    # And another node to animate the scale.
    hydrantScale = hydrantNode.attachNewNode('hydrantScale')
    hydrant.reparentTo(hydrantScale)

    # Temporarily pose the toon to the action frame so we can get the
    # transform from his legs.  This allows us to account for leg
    # style and cheesy effect legs.
    toon.pose('firehose', 30)
    toon.update(0)
    torso = toon.getPart('torso', '1000')

    # The destination Z value of the hydrant depends on the torso.
    if toon.style.torso[0] == 'm':
        # Medium torso, down here
        hydrant.setPos(torso, 0, 0, -1.85)
    else:
        # Small or large torso, up here
        hydrant.setPos(torso, 0, 0, -1.45)

    hydrant.setPos(0, 0, hydrant.getZ())

    base = hydrant.find('**/base')
    base.setColor(1, 1, 1, 0.5)
    base.setPos(toon, 0, 0, 0)

    toon.loop('neutral')

    # prepare the spray and create its intervals
    targetPoint = lambda suit=suit: __suitTargetPoint(suit)
    def getSprayStartPos(hose=hose, toon=toon, targetPoint=targetPoint):
        toon.update(0)  # force update of LOD 0 to current animation frame (dont know if it is being displayed or not)
        # If the hose is not present for the spray, effectively hide the spray by
        # making the origin the same as the target
        if (hose.isEmpty() == 1):
            if callable(targetPoint):
                return targetPoint()
            else:
                return targetPoint

        joint = hose.find("**/joint_water_stream")
        n = hidden.attachNewNode('pointBehindSprayProp')
        n.reparentTo(toon)
        # Now push the point back behind the nozzle for when the gun moves back
        n.setPos(joint.getPos(toon) + Point3(0, -0.55, 0))
        p = n.getPos(render)
        n.removeNode()
        del n
        return p

    sprayTrack = Sequence()
    sprayTrack.append(Wait(tSprayDelay))
    sprayTrack.append(MovieUtil.getSprayTrack(
        battle, WaterSprayColor,
        getSprayStartPos, targetPoint, dSprayScale, dSprayHold,
        dSprayScale, horizScale = scale, vertScale = scale))
    tracks.append(sprayTrack)

    # Unparent the hydrant for now; we'll put it back in when the
    # movie starts.
    hydrantNode.detachNode()

    propTrack = Sequence(# Use firehose, hydrant, and spray in the same track
        Func(battle.movie.needRestoreRenderProp, hydrantNode),
        Func(hydrantNode.reparentTo, toon),

        LerpScaleInterval(hydrantScale, tAppearDelay*0.5, Point3(1, 1, 1.4),
                           startScale=Point3(1, 1, 0.01),
                           ),
        LerpScaleInterval(hydrantScale, tAppearDelay*0.3, Point3(1, 1, 0.8),
                           startScale=Point3(1, 1, 1.4),
                           ),
        LerpScaleInterval(hydrantScale, tAppearDelay*0.1, Point3(1, 1, 1.2),
                           startScale=Point3(1, 1, 0.8),
                           ),
        LerpScaleInterval(hydrantScale, tAppearDelay*0.1, Point3(1, 1, 1),
                           startScale=Point3(1, 1, 1.2),
                           ),

        ActorInterval(hose, 'firehose', duration=dAnimHold), # Animate hose
        Wait(dHoseHold-0.2), # Wait before losing the hose
        LerpScaleInterval(hydrantScale, 0.2, Point3(1, 1, 0.01),
                           startScale=Point3(1, 1, 1),
                           ),

        Func(MovieUtil.removeProps, [hydrantNode, hose]),
        Func(battle.movie.clearRenderProp, hydrantNode),
    )
    tracks.append(propTrack)

    if hp > 0:
        tracks.append(__getSplashTrack(targetPoint, 0.4, 2.7, battle, splashHold=1.5))

    # Do the suit reaction
    # If the suit takes damage (hp > 0) or this squirt is the first one to strike (delay = 0)
    # then we naturally add a suit track, otherwise we don't so that a suit won't dodge
    # multiple times on sequential squirts in the same attack
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp,
                                     hpbonus, kbbonus, 'squirt-small-react',
                                     died, leftSuits, rightSuits, battle,
                                     toon, fShowStun, revived = revived))


    return tracks

def __doStormCloud(squirt, delay, fShowStun):
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    target = squirt['target']
    suit = target['suit']
    hp = target['hp']
    kbbonus = target['kbbonus']
    died = target['died']
    revived = target['revived']
    leftSuits = target['leftSuits']
    rightSuits = target['rightSuits']
    battle = squirt['battle']
    suitPos = suit.getPos(battle)
    origHpr = toon.getHpr(battle)
    hitSuit = (hp > 0)
    scale = sprayScales[level]

    tButton = 0.
    dButtonScale = 0.5
    dButtonHold = 3.
    tContact = 2.9
    tSpray = 1
    tSuitDodges = 1.8

    tracks = Parallel()

    # add sound
    soundTrack = __getSoundTrack(level, hitSuit, 2.3, toon)
    soundTrack2 = __getSoundTrack(level, hitSuit, 4.6, toon)
    tracks.append(soundTrack)
    tracks.append(soundTrack2)

    # do the button
    button = globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    hands = toon.getLeftHands()

    toonTrack = Sequence(
        Func(MovieUtil.showProps, buttons, hands),
        Func(toon.headsUp, battle, suitPos),
        ActorInterval(toon, 'pushbutton'),
        Func(MovieUtil.removeProps, buttons),
        Func(toon.loop, 'neutral'),
        Func(toon.setHpr, battle, origHpr),
        )
    tracks.append(toonTrack)

    # do the storm cloud and raining effect
    cloud = globalPropPool.getProp('stormcloud')
    cloud2 = MovieUtil.copyProp(cloud)
    # cloud = MovieUtil.copyProp(toon.cloudActors[0])
    # cloud2 = MovieUtil.copyProp(toon.cloudActors[1])
    BattleParticles.loadParticles()
    trickleEffect = BattleParticles.createParticleEffect(file='trickleLiquidate')
    rainEffect = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect2 = BattleParticles.createParticleEffect(file='liquidate')
    rainEffect3 = BattleParticles.createParticleEffect(file='liquidate')
    cloudHeight = suit.height + 3
    cloudPosPoint = Point3(0, 0, cloudHeight)
    scaleUpPoint = Point3(3, 3, 3)
    rainEffects = [rainEffect, rainEffect2, rainEffect3]
    rainDelay = 1
    effectDelay = 0.3

    # The cloud rains for much longer when it actually hits
    if hp > 0:
        cloudHold = 4.7
    else:
        cloudHold = 1.7

    def getCloudTrack(cloud, suit, cloudPosPoint, scaleUpPoint, rainEffects, rainDelay,
                      effectDelay, cloudHold, useEffect, battle=battle,
                      trickleEffect=trickleEffect):
        track = Sequence(
            Func(MovieUtil.showProp, cloud, suit, cloudPosPoint),
            Func(cloud.pose, 'stormcloud', 0),
            LerpScaleInterval(cloud, 1.5, scaleUpPoint,
                              startScale=MovieUtil.PNT3_NEARZERO),
            Wait(rainDelay), # Wait until button is pushed to rain
            )

        if (useEffect == 1):
            ptrack = Parallel()
            delay = trickleDuration = cloudHold * 0.25
            trickleTrack = Sequence(
                Func(battle.movie.needRestoreParticleEffect, trickleEffect),
                ParticleInterval(trickleEffect, cloud, worldRelative=0,
                                 duration=trickleDuration, cleanup = True),
                Func(battle.movie.clearRestoreParticleEffect, trickleEffect)
                )
            track.append(trickleTrack)
            for i in range(0, 3):
                dur = cloudHold - 2*trickleDuration
                ptrack.append(Sequence(
                    Func(battle.movie.needRestoreParticleEffect,
                         rainEffects[i]),
                    Wait(delay),
                    ParticleInterval(rainEffects[i],
                                     cloud, worldRelative=0, duration=dur, cleanup = True),
                    Func(battle.movie.clearRestoreParticleEffect,
                         rainEffects[i]),
                    ))
                delay += effectDelay
            ptrack.append(Sequence(Wait(3 * effectDelay),
                                   ActorInterval(cloud, 'stormcloud',
                                                 startTime=1, duration=cloudHold)))
            track.append(ptrack)
        else:
            track.append(ActorInterval(cloud, 'stormcloud', startTime=1,
                                       duration=cloudHold))

        track.append(LerpScaleInterval(cloud, 0.5, MovieUtil.PNT3_NEARZERO))
        track.append(Func(MovieUtil.removeProp, cloud))
        return track

    tracks.append(getCloudTrack(cloud, suit, cloudPosPoint,
                                scaleUpPoint, rainEffects, rainDelay,
                                effectDelay, cloudHold, useEffect=1))
    tracks.append(getCloudTrack(cloud2, suit, cloudPosPoint,
                                scaleUpPoint, rainEffects, rainDelay,
                                effectDelay, cloudHold, useEffect=0))

    # Do the suit reaction
    # If the suit takes damage (hp > 0) or this squirt is the first one to strike (delay = 0)
    # then we naturally add a suit track, otherwise we don't so that a suit won't dodge
    # multiple times on sequential squirts in the same attack
    if hp > 0 or delay <= 0:
        tracks.append(__getSuitTrack(suit, tContact, tSuitDodges, hp,
                                     hpbonus, kbbonus, 'soak', died,
                                     leftSuits, rightSuits, battle, toon,
                                     fShowStun, beforeStun = 2.6,
                                     afterStun = 2.3, revived = revived))

    return tracks

def __doGeyser(squirt, delay, fShowStun, uberClone = 0):
    #print("__doGeyser %s" % (uberClone))
    toon = squirt['toon']
    level = squirt['level']
    hpbonus = squirt['hpbonus']
    tracks = Parallel()
    tButton = 0.
    dButtonScale = 0.5
    dButtonHold = 3.
    tContact = 2.9
    tSpray = 1
    tSuitDodges = 1.8

    # do the button
    button = globalPropPool.getProp('button')
    button2 = MovieUtil.copyProp(button)
    buttons = [button, button2]
    hands = toon.getLeftHands()
    battle = squirt['battle']
    origHpr = toon.getHpr(battle)
    suit = squirt['target'][0]['suit']
    suitPos = suit.getPos(battle)

    toonTrack = Sequence(
        Func(MovieUtil.showProps, buttons, hands),
        Func(toon.headsUp, battle, suitPos),
        ActorInterval(toon, 'pushbutton'),
        Func(MovieUtil.removeProps, buttons),
        Func(toon.loop, 'neutral'),
        Func(toon.setHpr, battle, origHpr),
        )
    tracks.append(toonTrack)

    for target in squirt['target']:
        #target = squirt['target']
        suit = target['suit']
        hp = target['hp']
        kbbonus = target['kbbonus']
        died = target['died']
        revived = target['revived']
        leftSuits = target['leftSuits']
        rightSuits = target['rightSuits']
        suitPos = suit.getPos(battle)
        hitSuit = (hp > 0)
        scale = sprayScales[level]

        # add sound
        soundTrack = __getSoundTrack(level, hitSuit, 1.8, toon)
        #soundTrack2 = __getSoundTrack(level, hitSuit, 4.6, toon)
        delayTime = random.random()
        tracks.append(Wait(delayTime))
        tracks.append(soundTrack)
        #tracks.append(soundTrack2)

        # do the storm cloud and raining effect
        cloud = globalPropPool.getProp('geyser')
        cloud2 = MovieUtil.copyProp(cloud)
        # cloud = MovieUtil.copyProp(toon.cloudActors[0])
        # cloud2 = MovieUtil.copyProp(toon.cloudActors[1])
        BattleParticles.loadParticles()
        #trickleEffect = BattleParticles.createParticleEffect(file='trickleLiquidate')
        #rainEffect = BattleParticles.createParticleEffect(file='liquidate')
        #rainEffect2 = BattleParticles.createParticleEffect(file='liquidate')
        #rainEffect3 = BattleParticles.createParticleEffect(file='liquidate')
        #geyserHeight =  0.0 #suit.height + 3
        geyserHeight = battle.getH()
        geyserPosPoint = Point3(0, 0, geyserHeight)
        scaleUpPoint = Point3(1.8, 1.8, 1.8)
        rainEffects = []#rainEffect, rainEffect2, rainEffect3]
        rainDelay = 2.5
        effectDelay = 0.3

        # The geyser goes for much longer when it actually hits
        if hp > 0:
            geyserHold = 1.5
        else:
            geyserHold = 0.5

        def getGeyserTrack(geyser, suit, geyserPosPoint, scaleUpPoint, rainEffects, rainDelay,
                          effectDelay, geyserHold, useEffect, battle=battle):
                          #,trickleEffect=trickleEffect):

            geyserMound = MovieUtil.copyProp(geyser)
            geyserRemoveM = geyserMound.findAllMatches("**/Splash*")
            geyserRemoveM.addPathsFrom(geyserMound.findAllMatches("**/spout"))
            for i in range(geyserRemoveM.getNumPaths()):
                geyserRemoveM[i].removeNode()
            #geyserMound.wrtReparentTo(render)


            geyserWater = MovieUtil.copyProp(geyser)
            geyserRemoveW = geyserWater.findAllMatches("**/hole")
            geyserRemoveW.addPathsFrom(geyserWater.findAllMatches("**/shadow"))
            #import pdb; pdb.set_trace()
            for i in range(geyserRemoveW.getNumPaths()):
                geyserRemoveW[i].removeNode()
            #geyserWater.wrtReparentTo(render)

            #import pdb; pdb.set_trace()
            track = Sequence(
                Wait(rainDelay), # Wait until button is pushed to rain
                #Wait(delayTime),
               #Func(MovieUtil.showProp, geyserMound, suit, geyserPosPoint),
               #Func(MovieUtil.showProp, geyserWater, suit, geyserPosPoint),
                Func(MovieUtil.showProp, geyserMound, battle, suit.getPos(battle)),
                Func(MovieUtil.showProp, geyserWater, battle, suit.getPos(battle)),
                LerpScaleInterval(geyserWater, 1.0, scaleUpPoint,
                                  startScale=MovieUtil.PNT3_NEARZERO),
                Wait(geyserHold * 0.5),
                LerpScaleInterval(geyserWater, 0.5, MovieUtil.PNT3_NEARZERO,
                                  startScale=scaleUpPoint),
                 )

            track.append(LerpScaleInterval(geyserMound, 0.5, MovieUtil.PNT3_NEARZERO))
            track.append(Func(MovieUtil.removeProp, geyserMound))
            track.append(Func(MovieUtil.removeProp, geyserWater))
            track.append(Func(MovieUtil.removeProp, geyser))
            return track

        if not uberClone:
            tracks.append(Sequence(Wait(delayTime),
                                    getGeyserTrack(cloud, suit, geyserPosPoint,
                                        scaleUpPoint, rainEffects, rainDelay,
                                        effectDelay, geyserHold, useEffect=1),
                                        ))
       # tracks.append(getGeyserTrack(cloud2, suit, cloudPosPoint,
       #                             scaleUpPoint, rainEffects, rainDelay,
       #                             effectDelay, cloudHold, useEffect=0))

        # Do the suit reaction
        # If the suit takes damage (hp > 0) or this squirt is the first one to strike (delay = 0)
        # then we naturally add a suit track, otherwise we don't so that a suit won't dodge
        # multiple times on sequential squirts in the same attack
        if hp > 0 or delay <= 0:
            tracks.append(Sequence(Wait(delayTime),
                                    __getSuitTrack(suit, tContact, tSuitDodges, hp,
                                         hpbonus, kbbonus, 'soak', died,
                                         leftSuits, rightSuits, battle, toon,
                                         fShowStun, beforeStun = 2.6,
                                         afterStun = 2.3, geyser = 1, uberRepeat = uberClone, revived = revived),))

    return tracks

squirtfn_array = (__doFlower, __doWaterGlass,
                  __doWaterGun, __doSeltzerBottle,
                  __doFireHose, __doStormCloud,
                  __doGeyser) #UBER


