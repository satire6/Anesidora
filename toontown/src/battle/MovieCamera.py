from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from BattleBase import *
from BattleProps import *
from toontown.toonbase.ToontownBattleGlobals import *
from SuitBattleGlobals import *

from direct.directnotify import DirectNotifyGlobal
import random
import MovieUtil

notify = DirectNotifyGlobal.directNotify.newCategory('MovieCamera')


###########################################################
##   _  _          _   ___ _        _      
##  | || |___ __ _| | / __| |_  ___| |_ ___
##  | __ / -_) _` | | \__ \ ' \/ _ \  _(_-<
##  |_||_\___\__,_|_| |___/_||_\___/\__/__/
##
###########################################################


def chooseHealShot(heals, attackDuration): 
    isUber = 0
    
    for heal in heals:
        if (heal["level"] == 6) and not (heal.get("petId")):
            isUber = 1

    # Compose the track
    if isUber:
        print("is uber")
        # Pick an open shot
        openShot = chooseHealOpenShot(heals, attackDuration, isUber)
        openDuration = openShot.getDuration()
        openName = openShot.getName()
        # if the high dive is involved we want the gag to control camera and we
        #cut straight to the closing shot.
        # Pick a close shot
        closeShot = chooseHealCloseShot(heals, 
                                         openDuration, openName, attackDuration * 3 , isUber)
        track = Sequence(closeShot)
    else:
        # Pick an open shot
        openShot = chooseHealOpenShot(heals, attackDuration, isUber)
        openDuration = openShot.getDuration()
        openName = openShot.getName()
        # Pick a close shot
        closeShot = chooseHealCloseShot(heals, 
                                         openDuration, openName, attackDuration, isUber)
        track = Sequence(openShot, closeShot)
    # Ensure we composed it to the right length
    #assert track.getDuration() == attackDuration
    # Return it
    return track

def chooseHealOpenShot(heals, attackDuration, isUber = 0):
    # Setup
    numHeals = len(heals)
    av = None
    duration = 2.8
    if isUber:
        duration = 5.0
    # General purpose shots
    shotChoices = [
        toonGroupShot,
        #allGroupLowShot, this is a bad choice
        ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track
    
def chooseHealMidShot(heals, attackDuration, isUber = 0):
    # Setup
    numHeals = len(heals)
    av = None
    duration = 2.1
    if isUber:
        duration = 2.1
    # General purpose shots
    shotChoices = [
        toonGroupHighShot,
        #allGroupLowShot, this is a bad choice
        ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track
    
def chooseHealCloseShot(heals, 
                         openDuration, openName, attackDuration, isUber = 0):
    # Setup
    av = None
    duration = attackDuration - openDuration
    # General purpose shots
    shotChoices = [
        toonGroupShot,
        # allGroupLowDiagonalShot, this is a bad choice
        ]
    if isUber:
        shotChoices = [
            allGroupLowShot,
            # allGroupLowDiagonalShot, this is a bad choice
            ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track

###########################################################
##   _____                ___ _        _      
##  |_   _| _ __ _ _ __  / __| |_  ___| |_ ___
##    | || '_/ _` | '_ \ \__ \ ' \/ _ \  _(_-<
##    |_||_| \__,_| .__/ |___/_||_\___/\__/__/
##                |_|                         
###########################################################


def chooseTrapShot(traps, attackDuration, enterDuration = 0,
                                          exitDuration = 0):
    enterShot = chooseNPCEnterShot(traps, enterDuration)
    # Pick an open shot
    openShot = chooseTrapOpenShot(traps, attackDuration)
    openDuration = openShot.getDuration()
    openName = openShot.getName()
    # Pick a close shot
    closeShot = chooseTrapCloseShot(traps, 
                                     openDuration, openName, attackDuration)
    exitShot = chooseNPCExitShot(traps, exitDuration)
    # Compose the track
    track = Sequence(enterShot, openShot, closeShot, exitShot)
    # Ensure we composed it to the right length
    #assert track.getDuration() == attackDuration
    # Return it
    return track

def chooseTrapOpenShot(traps, attackDuration):
    # Setup
    numTraps = len(traps)
    av = None
    duration = 3.0
    # General purpose shots
    shotChoices = [
        allGroupLowShot,
        ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track
    
def chooseTrapCloseShot(traps, 
                         openDuration, openName, attackDuration):
    # Setup
    av = None
    duration = attackDuration - openDuration
    # General purpose shots
    shotChoices = [
        allGroupLowShot,
        ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track

###########################################################
##   _                  ___ _        _      
##  | |  _  _ _ _ ___  / __| |_  ___| |_ ___
##  | |_| || | '_/ -_) \__ \ ' \/ _ \  _(_-<
##  |____\_,_|_| \___| |___/_||_\___/\__/__/
##
###########################################################

def chooseLureShot(lures, attackDuration, enterDuration = 0.0, 
                                          exitDuration = 0.0):
    enterShot = chooseNPCEnterShot(lures, enterDuration)
    # Pick an open shot
    openShot = chooseLureOpenShot(lures, attackDuration)
    openDuration = openShot.getDuration()
    openName = openShot.getName()
    # Pick a close shot
    closeShot = chooseLureCloseShot(lures, 
                                     openDuration, openName, attackDuration)
    exitShot = chooseNPCExitShot(lures, exitDuration)
    # Compose the track
    track = Sequence(enterShot, openShot, closeShot, exitShot)
    # Ensure we composed it to the right length
    #assert track.getDuration() == attackDuration
    # Return it
    return track

def chooseLureOpenShot(lures, attackDuration):
    # Setup
    numLures = len(lures)
    av = None
    duration = 3.0


    # General purpose shots
    shotChoices = [
        allGroupLowShot,
        ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track
    
def chooseLureCloseShot(lures, 
                         openDuration, openName, attackDuration):
    # Setup
    av = None
    duration = attackDuration - openDuration

    #figure out if any of the suits have a traintrack trap
    #if we do the shot choices should be different
    hasTrainTrackTrap = False
    battle = lures[0]['battle']
    for suit in battle.suits:
        if hasattr(suit,'battleTrap') and suit.battleTrap == UBER_GAG_LEVEL_INDEX:
            hasTrainTrackTrap = True
            
    if hasTrainTrackTrap:
        shotChoices = [
            avatarBehindHighRightShot,
            ]
        av = lures[0]['toon']
        pass
    else:
        # General purpose shots
        shotChoices = [
            allGroupLowShot,
            ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track

###########################################################
##   ___                   _   ___ _        _      
##  / __| ___ _  _ _ _  __| | / __| |_  ___| |_ ___
##  \__ \/ _ \ || | ' \/ _` | \__ \ ' \/ _ \  _(_-<
##  |___/\___/\_,_|_||_\__,_| |___/_||_\___/\__/__/
##
###########################################################                                                

def chooseSoundShot(sounds, targets, attackDuration, enterDuration = 0.0,
                                                     exitDuration = 0.0):
    enterShot = chooseNPCEnterShot(sounds, enterDuration)
    # Pick an open shot
    openShot = chooseSoundOpenShot(sounds, targets, attackDuration)
    openDuration = openShot.getDuration()
    openName = openShot.getName()
    # Pick a close shot
    closeShot = chooseSoundCloseShot(sounds, targets,
                                     openDuration, openName, attackDuration)
    exitShot = chooseNPCExitShot(sounds, exitDuration)
    # Compose the track
    track = Sequence(enterShot, openShot, closeShot, exitShot)
    # Ensure we composed it to the right length
    #assert track.getDuration() == attackDuration
    # Return it
    return track

def chooseSoundOpenShot(sounds, targets, attackDuration):
    # Setup
    duration = 3.1
    isUber = 0
    for sound in sounds:
        if sound["level"] == 6 :
            isUber = 1
            duration = 5.0
    #import pdb; pdb.set_trace()
    numSounds = len(sounds)
    av = None
    
    # The single toon case
    if numSounds == 1:
        # The attacking Toon
        av = sounds[0]['toon']
        # Single toon choices
        if isUber:
            shotChoices = [
                avatarCloseUpThreeQuarterRightShotWide,
                allGroupLowShot,
                suitGroupThreeQuarterLeftBehindShot,
                ]
        else:
            shotChoices = [
                avatarCloseUpThreeQuarterRightShot,
                allGroupLowShot,
                suitGroupThreeQuarterLeftBehindShot,
                ]
    # The multi toon case
    elif numSounds >= 2 and numSounds <= 4:
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of sounds: %s" % numSounds)
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track
    
def chooseSoundCloseShot(sounds, targets,
                         openDuration, openName, attackDuration):
    # Setup
    numSuits = len(targets)
    av = None
    duration = attackDuration - openDuration
    # The single suit case
    if numSuits == 1:
        # The attacked suit
        av = targets[0]['suit']
        # Single suit choices
        shotChoices = [
            avatarCloseUpThrowShot,
            avatarCloseUpThreeQuarterLeftShot,

            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi suit case
    elif numSuits >= 2 and numSuits <= 4:
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of suits: %s" % numSuits)
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track

###########################################################
##   _____ _                     ___ _        _      
##  |_   _| |_  _ _ _____ __ __ / __| |_  ___| |_ ___
##    | | | ' \| '_/ _ \ V  V / \__ \ ' \/ _ \  _(_-<
##    |_| |_||_|_| \___/\_/\_/  |___/_||_\___/\__/__/
##                                                  
###########################################################

def chooseThrowShot(throws, suitThrowsDict, attackDuration):
    # Pick an open shot
    openShot = chooseThrowOpenShot(throws, suitThrowsDict, attackDuration)
    openDuration = openShot.getDuration()
    openName = openShot.getName()
    # Pick a close shot
    closeShot = chooseThrowCloseShot(throws, suitThrowsDict,
                                     openDuration, openName, attackDuration)
    # Compose the track
    track = Sequence(openShot, closeShot)
    # Ensure we composed it to the right length
    #assert track.getDuration() == attackDuration
    # Return it
    return track

def chooseThrowOpenShot(throws, suitThrowsDict, attackDuration):
    # Setup
    numThrows = len(throws)
    av = None
    duration = 3.0
    # The single toon case
    if numThrows == 1:
        # The attacking Toon
        av = throws[0]['toon']
        # Single toon choices
        shotChoices = [
            avatarCloseUpThrowShot,
            avatarCloseUpThreeQuarterRightShot,
            avatarBehindShot,

            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi toon case
    elif numThrows >= 2 and numThrows <= 4:
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of throws: %s" % numThrows)
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])

    # Set up the play by play text
    # Whoops! No play by play for toons, since the multi-toon case is
    # confusing...
    #pbpText = attack['playByPlayText']
    #pbpTrack = pbpText.getShowInterval(attack['prettyName'], duration)

    #mtrack = Parallel(track, pbpTrack)
    
    return track
    
def chooseThrowCloseShot(throws, suitThrowsDict,
                         openDuration, openName, attackDuration):
    # Setup
    numSuits = len(suitThrowsDict)
    av = None
    duration = attackDuration - openDuration
    # The single suit case
    if numSuits == 1:
        # The attacked suit
        av = base.cr.doId2do[suitThrowsDict.keys()[0]]
        # Single suit choices
        shotChoices = [
            avatarCloseUpThrowShot,
            avatarCloseUpThreeQuarterLeftShot,
            
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi suit case (RAU we could get 0 for uber throw)
    elif (numSuits >= 2 and numSuits <= 4) or (numSuits==0):
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of suits: %s" % numSuits)
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track

##########################################################################
##   ___            _     _     ___ _        _      
##  / __| __ _ _  _(_)_ _| |_  / __| |_  ___| |_ ___
##  \__ \/ _` | || | | '_|  _| \__ \ ' \/ _ \  _(_-<
##  |___/\__, |\_,_|_|_|  \__| |___/_||_\___/\__/__/
##          |_|                                     
##########################################################################

def chooseSquirtShot(squirts, suitSquirtsDict, attackDuration):
    # Pick an open shot
    openShot = chooseSquirtOpenShot(squirts, suitSquirtsDict, attackDuration)
    openDuration = openShot.getDuration()
    openName = openShot.getName()
    # Pick a close shot
    closeShot = chooseSquirtCloseShot(squirts, suitSquirtsDict,
                                     openDuration, openName, attackDuration)
    # Compose the track
    track = Sequence(openShot, closeShot)
    # Ensure we composed it to the right length
    #assert track.getDuration() == attackDuration
    # Return it
    return track

def chooseSquirtOpenShot(squirts, suitSquirtsDict, attackDuration):
    # Setup
    numSquirts = len(squirts)
    av = None
    duration = 3.0
    # The single toon case
    if numSquirts == 1:
        # The attacking Toon
        av = squirts[0]['toon']
        # Single toon choices
        shotChoices = [
            avatarCloseUpThrowShot,
            avatarCloseUpThreeQuarterRightShot,
            avatarBehindShot,

            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi toon case
    elif numSquirts >= 2 and numSquirts <= 4:
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of squirts: %s" % numSquirts)
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track
    
def chooseSquirtCloseShot(squirts, suitSquirtsDict,
                          openDuration, openName, attackDuration):
    # Setup
    numSuits = len(suitSquirtsDict)
    av = None
    duration = attackDuration - openDuration
    # The single suit case
    if numSuits == 1:
        # The attacked suit
        av = base.cr.doId2do[suitSquirtsDict.keys()[0]]
        # Single suit choices
        shotChoices = [
            avatarCloseUpThrowShot,
            avatarCloseUpThreeQuarterLeftShot,
            
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi suit case
    elif numSuits >= 2 and numSuits <= 4:
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of suits: %s" % numSuits)
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track


##########################################################################
##   ___                 ___ _        _      
##  |   \ _ _ ___ _ __  / __| |_  ___| |_ ___
##  | |) | '_/ _ \ '_ \ \__ \ ' \/ _ \  _(_-<
##  |___/|_| \___/ .__/ |___/_||_\___/\__/__/
##               |_|                         
##########################################################################

def chooseDropShot(drops, suitDropsDict, attackDuration, enterDuration = 0.0,
                                                     exitDuration = 0.0):
    enterShot = chooseNPCEnterShot(drops, enterDuration)
    # Pick an open shot
    openShot = chooseDropOpenShot(drops, suitDropsDict, attackDuration)
    openDuration = openShot.getDuration()
    openName = openShot.getName()
    # Pick a close shot
    closeShot = chooseDropCloseShot(drops, suitDropsDict,
                                     openDuration, openName, attackDuration)
    exitShot = chooseNPCExitShot(drops, exitDuration)
    # Compose the track
    track = Sequence(enterShot, openShot, closeShot, exitShot)
    # Ensure we composed it to the right length
    #assert track.getDuration() == attackDuration
    # Return it
    return track

def chooseDropOpenShot(drops, suitDropsDict, attackDuration):
    # Setup
    numDrops = len(drops)
    av = None
    duration = 3.0
    # The single toon case
    if numDrops == 1:
        # The attacking Toon
        av = drops[0]['toon']
        # Single toon choices
        shotChoices = [
            avatarCloseUpThrowShot,
            avatarCloseUpThreeQuarterRightShot,
            avatarBehindShot,

            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi toon case (Uber drop gag can give 0 single drops)
    elif (numDrops >= 2 and numDrops <= 4) or (numDrops == 0):
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of drops: %s" % numDrops)
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track
    
def chooseDropCloseShot(drops, suitDropsDict,
                         openDuration, openName, attackDuration):
    # Setup
    numSuits = len(suitDropsDict)
    av = None
    duration = attackDuration - openDuration
    # The single suit case
    if numSuits == 1:
        # The attacked suit
        av = base.cr.doId2do[suitDropsDict.keys()[0]]
        # Single suit choices
        shotChoices = [
            avatarCloseUpThrowShot,
            avatarCloseUpThreeQuarterLeftShot,          
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi toon case (Uber drop gag can give 0 single drops)    
    elif (numSuits >= 2 and numSuits <= 4) or (numSuits == 0):
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of suits: %s" % numSuits)
    # Pick a shot and return it
    choice = random.choice(shotChoices)
    track = choice(av, duration)
    return track

##########################################################################
# NPC Enter and Exit Shots
##########################################################################

def chooseNPCEnterShot(enters, entersDuration):
    # Setup
    av = None
    duration = entersDuration
    # General purpose shots
    shotChoices = [
        toonGroupShot,
        ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track
    
def chooseNPCExitShot(exits, exitsDuration):
    # Setup
    av = None
    duration = exitsDuration
    # General purpose shots
    shotChoices = [
        toonGroupShot,
        ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track

##########################################################################
##   ___      _ _     ___ _        _      
##  / __|_  _(_) |_  / __| |_  ___| |_ ___
##  \__ \ || | |  _| \__ \ ' \/ _ \  _(_-<
##  |___/\_,_|_|\__| |___/_||_\___/\__/__/
##
##########################################################################

def chooseSuitShot(attack, attackDuration):
    groupStatus = attack['group']
    target = attack['target']
    # If the attack is a single attack, can focus in on the target toon
    if groupStatus == ATK_TGT_SINGLE:
        toon = target['toon']
    suit = attack['suit']
    name = attack['id']
    battle = attack['battle']
    camTrack = Sequence()
    
    # The default camera operation of a random opening and closing shot
    def defaultCamera(attack=attack, attackDuration=attackDuration,
                      openShotDuration=3.5, target=target):
        if attack['group'] == ATK_TGT_GROUP:
            return randomGroupAttackCam(attack['suit'], target, attack['battle'],
                                        attackDuration, openShotDuration)
#            return randomCameraSelection(attack['suit'], attack,
#                                         attackDuration, openShotDuration)
        else:
            return randomAttackCam(attack['suit'], target['toon'], attack['battle'],
                                   attackDuration, openShotDuration, 'suit')

    # Pick an open shot, based on the attack
    if (name == AUDIT):
        camTrack.append(defaultCamera())
    elif (name == BITE):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == BOUNCE_CHECK):
        camTrack.append(defaultCamera())
    elif (name == BRAIN_STORM):
        camTrack.append(defaultCamera(openShotDuration=2.4))
    elif (name == BUZZ_WORD):
        camTrack.append(defaultCamera(openShotDuration=4.7))
    elif (name == CALCULATE):
        camTrack.append(defaultCamera())
    elif (name == CANNED):
        camTrack.append(defaultCamera(openShotDuration=2.9))
    elif (name == CHOMP):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == CLIPON_TIE):
        camTrack.append(defaultCamera(openShotDuration=3.3))
    elif (name == CRUNCH):
        camTrack.append(defaultCamera(openShotDuration=3.4))
    elif (name == DEMOTION):
        camTrack.append(defaultCamera(openShotDuration=1.7))
    elif (name == DOUBLE_TALK):
        camTrack.append(defaultCamera(openShotDuration=3.9))
    elif (name == EVICTION_NOTICE):
        camTrack.append(defaultCamera(openShotDuration=3.2))
    elif (name == EVIL_EYE):
        camTrack.append(defaultCamera(openShotDuration=2.7))
    elif (name == FILIBUSTER):
        camTrack.append(defaultCamera(openShotDuration=2.7))
    elif (name == FILL_WITH_LEAD):
        camTrack.append(defaultCamera(openShotDuration=3.2))
    elif (name == FINGER_WAG):
        camTrack.append(defaultCamera(openShotDuration=2.3))
    elif (name == FIRED):
        camTrack.append(defaultCamera(openShotDuration=1.7))
    elif (name == FOUNTAIN_PEN):
        camTrack.append(defaultCamera(openShotDuration=2.6))
    elif (name == FREEZE_ASSETS):
        camTrack.append(defaultCamera(openShotDuration=2.5))
    elif (name == HALF_WINDSOR):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == HEAD_SHRINK):
        camTrack.append(defaultCamera(openShotDuration=1.3))
    elif (name == GLOWER_POWER):
        camTrack.append(defaultCamera(openShotDuration=1.4))
    elif (name == GUILT_TRIP):
        camTrack.append(defaultCamera(openShotDuration=0.9))
    elif (name == HANG_UP):
        camTrack.append(defaultCamera(openShotDuration=5.1))
    elif (name == HOT_AIR):
        camTrack.append(defaultCamera(openShotDuration=2.5))
    elif (name == JARGON):
        camTrack.append(defaultCamera())
    elif (name == LEGALESE):
        camTrack.append(defaultCamera(openShotDuration=1.5))
    elif (name == LIQUIDATE):
        camTrack.append(defaultCamera(openShotDuration=2.5))
    elif (name == MARKET_CRASH):
        camTrack.append(defaultCamera(openShotDuration=2.9))
    elif (name == MUMBO_JUMBO):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == PARADIGM_SHIFT):
        camTrack.append(defaultCamera(openShotDuration=1.6))
    elif (name == PECKING_ORDER):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == PLAY_HARDBALL):
        camTrack.append(defaultCamera(openShotDuration=2.3))
    elif (name == PICK_POCKET):
        camTrack.append(allGroupLowShot(suit, 2.7))
    elif (name == PINK_SLIP):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == POUND_KEY):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == POWER_TIE):
        camTrack.append(defaultCamera(openShotDuration=2.4))
    elif (name == POWER_TRIP):
        camTrack.append(defaultCamera(openShotDuration=1.1))
    elif (name == QUAKE):
        shakeIntensity = 5.15
        quake = 1 # Quake applies an extra side shake for greater damage effect
        camTrack.append(suitCameraShakeShot(suit, attackDuration,
                                             shakeIntensity, quake))
    elif (name == RAZZLE_DAZZLE):
        camTrack.append(defaultCamera(openShotDuration=2.2))
    elif (name == RED_TAPE):
        camTrack.append(defaultCamera(openShotDuration=3.5))
    elif (name == RE_ORG):
        camTrack.append(defaultCamera(openShotDuration=1.1))
    elif (name == RESTRAINING_ORDER):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == ROLODEX):
        camTrack.append(defaultCamera())
    elif (name == RUBBER_STAMP):
        camTrack.append(defaultCamera(openShotDuration=3.2))
    elif (name == RUB_OUT):
        camTrack.append(defaultCamera(openShotDuration=2.2))
    elif (name == SACKED):
        camTrack.append(defaultCamera(openShotDuration=2.9))
    elif (name == SCHMOOZE):
        camTrack.append(defaultCamera(openShotDuration=2.8))
    elif (name == SHAKE):
        shakeIntensity = 1.75
        camTrack.append(suitCameraShakeShot(suit, attackDuration,
                                             shakeIntensity))
    elif (name == SHRED):
        camTrack.append(defaultCamera(openShotDuration=4.1))
    elif (name == SPIN):
        camTrack.append(defaultCamera(openShotDuration=1.7))
    elif (name == SYNERGY):
        camTrack.append(defaultCamera(openShotDuration=1.7))
    elif (name == TABULATE):
        camTrack.append(defaultCamera())
    elif (name == TEE_OFF):
        camTrack.append(defaultCamera(openShotDuration=4.5))
    elif (name == TREMOR):
        shakeIntensity = 0.25
        camTrack.append(suitCameraShakeShot(suit, attackDuration, shakeIntensity))
    elif (name == WATERCOOLER):
        camTrack.append(defaultCamera())
    elif (name == WITHDRAWAL):
        camTrack.append(defaultCamera(openShotDuration=1.2))
    elif (name == WRITE_OFF):
        camTrack.append(defaultCamera())
    else:
        notify.warning('unknown attack id in chooseSuitShot: %d using default cam' \
                       % name)
        camTrack.append(defaultCamera())

    # Set up the play by play text
    pbpText = attack['playByPlayText']
    displayName = TTLocalizer.SuitAttackNames[attack['name']]
    pbpTrack = pbpText.getShowInterval(displayName, 3.5)
    return Parallel(camTrack, pbpTrack)

def chooseSuitCloseShot(attack,
                         openDuration, openName, attackDuration):
    # Setup
    av = None
    duration = attackDuration - openDuration
    if (duration < 0): # If the duration is negative (bug), safely make it negligible
        duration = 0.000001
    groupStatus = attack['group']
    diedTrack = None
    # The single toon case
    if groupStatus == ATK_TGT_SINGLE:
        # The attacked toon
        av = attack['target']['toon']
        # Single suit choices
        shotChoices = [
            #avatarBehindShot,
            #avatarBehindHighShot,
            avatarCloseUpThreeQuarterRightShot,
            
            #allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
        ]
        died = attack['target']['died']
        if died != 0:
            # If av died, make a parallel track
            pbpText = attack['playByPlayText']
            diedText = av.getName() + " was defeated!"
            diedTextList = [diedText]
            diedTrack = pbpText.getToonsDiedInterval(diedTextList,
                                                     duration)

    # The multi toon case
    elif groupStatus == ATK_TGT_GROUP:
        av = None
        # Multi toon choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
        deadToons = []
        targetDicts = attack['target']
        for targetDict in targetDicts:
            died = targetDict['died']
            if died != 0:
                deadToons.append(targetDict['toon'])
        if len(deadToons) > 0:
            pbpText = attack['playByPlayText']
            diedTextList = []
            for toon in deadToons:
                pbpText = attack['playByPlayText']
                diedTextList.append(toon.getName() + " was defeated!")
            diedTrack = pbpText.getToonsDiedInterval(diedTextList, duration)
    else:
        notify.error("Bad groupStatus: %s" % groupStatus)
    
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    if diedTrack == None:
        return track
    else:
        mtrack = Parallel(track, diedTrack)
        return mtrack

def makeShot(x, y, z, h, p, r, duration, other=None, name='makeShot'):
    """ makeShot() creates a held shot, with keyword arg for a relative held shot """
    if other:
        return heldRelativeShot(other, x, y, z, h, p, r, duration, name)
    else:
        return heldShot(x, y, z, h, p, r, duration, name)

def focusShot(x, y, z, duration, target, other=None, splitFocusPoint=None, name='focusShot'):
    """ focusShot() creates a held shot with camera focused on target arg """
    track = Sequence()
    if other:
        track.append(Func(camera.setPos, other, Point3(x, y, z)))
    else:
        track.append(Func(camera.setPos, Point3(x, y, z)))

    if splitFocusPoint:
        track.append(Func(focusCameraBetweenPoints, target, splitFocusPoint))
    else:
        track.append(Func(camera.lookAt, target))
    track.append(Wait(duration))

    return track

def moveShot(x, y, z, h, p, r, duration, other=None, name='moveShot'):
    """ moveShot() creates a moving shot from the current position to the args provided """
    return motionShot(x, y, z, h, p, r, duration, other, name)

def focusMoveShot(x, y, z, duration, target, other=None, name='focusMoveShot'):
    """ focusMoveShot() creates a moving shot from the current position to focus on the
        target arg provided """
    camera.setPos(Point3(x, y, z))
    camera.lookAt(target)
    hpr = camera.getHpr()
    return motionShot(x, y, z, hpr[0], hpr[1], hpr[2],
                      duration, other, name)

##########################################################################
##   ___  ___  ___   ___ _        _      
##  / __|/ _ \/ __| / __| |_  ___| |_ ___
##  \__ \ (_) \__ \ \__ \ ' \/ _ \  _(_-<
##  |___/\___/|___/ |___/_||_\___/\__/__/
##
##########################################################################

def chooseSOSShot(av, duration):
    shotChoices = [
        avatarCloseUpThreeQuarterRightShot,
        avatarBehindShot,
        avatarBehindHighShot,
        
        suitGroupThreeQuarterLeftBehindShot,
        ]
    # Pick a shot and return it
    track = apply(random.choice(shotChoices), [av, duration])
    return track


##########################################################################
##   ___                        _   ___ _        _      
##  | _ \_____ __ ____ _ _ _ __| | / __| |_  ___| |_ ___
##  |   / -_) V  V / _` | '_/ _` | \__ \ ' \/ _ \  _(_-<
##  |_|_\___|\_/\_/\__,_|_| \__,_| |___/_||_\___/\__/__/
##
##########################################################################

def chooseRewardShot(av, duration, allowGroupShot = 1):
    # We actually return an interval that chooses the reward shot
    # on-the-fly, rather than prechoosing it.  This is because the
    # avatar in question may wander away during the reward movie.

    def chooseRewardShotNow(av):
        if av.playingAnim == "victory" or not allowGroupShot:
            # The avatar is still dancing; choose an avatar shot.
            shotChoices = [(0, 8, av.getHeight() * 0.66, 179, 15, 0),
                           (5.2, 5.45, av.getHeight() * 0.66, 131.5, 3.6, 0)]
            shot = random.choice(shotChoices)
            camera.setPosHpr(av, *shot)
        else:
            # The avatar has stopped dancing; give a group shot.
            camera.setPosHpr(10, 0, 10, 115, -30, 0)

    return Sequence(Func(chooseRewardShotNow, av),
                    Wait(duration))

##########################################################################
##    ___                       _   _   _           ___ _        _      
##   / __|___ _ _  ___ _ _ __ _| | | | | |___ ___  / __| |_  ___| |_ ___
##  | (_ / -_) ' \/ -_) '_/ _` | | | |_| (_-</ -_) \__ \ ' \/ _ \  _(_-<
##   \___\___|_||_\___|_| \__,_|_|  \___//__/\___| |___/_||_\___/\__/__/
##                                                                     
##########################################################################

def heldShot(x, y, z, h, p, r, duration, name="heldShot"):
    track = Sequence(name = name)

    # Let the camera display the toons
    track.append(Func(camera.setPosHpr, x, y, z, h, p, r))

    # Hold that pose
    track.append(Wait(duration))

    return track

def heldRelativeShot(other, x, y, z, h, p, r, duration,
                     name="heldRelativeShot"):
    track = Sequence(name = name)

    # Let the camera display the toons
    track.append(Func(camera.setPosHpr, other, x, y, z, h, p, r))
    
    # Hold that pose
    track.append(Wait(duration))

    return track

def motionShot(x, y, z, h, p, r, duration, other=None, name="motionShot"):
    if other: # If an other parent exists, use it
        posTrack = LerpPosInterval(camera, duration, pos=Point3(x, y, z),
                                   other=other)
        hprTrack = LerpHprInterval(camera, duration, hpr=Point3(h, p, r),
                                   other=other)
    else:
        posTrack = LerpPosInterval(camera, duration, pos=Point3(x, y, z))
        hprTrack = LerpHprInterval(camera, duration, hpr=Point3(h, p, r))
    return Parallel(posTrack, hprTrack)
        
def allGroupShot(avatar, duration):
    return heldShot(10, 0, 10, 89, -30, 0, duration, "allGroupShot")

def allGroupLowShot(avatar, duration):
    return heldShot(15, 0, 3, 89, 0, 0, duration, "allGroupLowShot")

def allGroupLowDiagonalShot(avatar, duration):
    return heldShot(7, 5, 6, 119, -30, 0, duration, "allGroupLowShot")

def toonGroupShot(avatar, duration):
    return heldShot(10, 0, 10, 115, -30, 0, duration, "toonGroupShot")

def toonGroupHighShot(avatar, duration):
    #return heldShot(10, 0, 30, 115, -60, 0, duration, "toonGroupHighShot")
    return heldShot(5, 0, 1, 115, 45, 0, duration, "toonGroupHighShot")
        
def suitGroupShot(avatar, duration):
    return heldShot(10, 0, 10, 65, -30, 0, duration, "suitGroupShot")

def suitGroupLowLeftShot(avatar, duration):
    return heldShot(8.4, -3.85, 2.75, 36.3, 3.25, 0, duration,
                    "suitGroupLowLeftShot")

# Good for toon throws, and some suit magic attacks.
def suitGroupThreeQuarterLeftBehindShot(avatar, duration):
    if (random.random() > 0.5): # 50% chance
        x = 12.37
        h = 134.61
    else:
        x = -12.37
        h = -134.61
        
    return heldShot(x, 11.5, 8.16, h, -22.70, 0, duration,
                    "suitGroupThreeQuarterLeftBehindShot")

def suitWakeUpShot(avatar, duration):
    return heldShot(10, -5, 10, 65, -30, 0, duration, "suitWakeUpShot")

def suitCameraShakeShot(avatar, duration, shakeIntensity, quake=0):
    track = Sequence(name = "suitShakeCameraShot")
    if (quake == 1):
        shakeDelay = 1.1
        numShakes = 4
    else:
        shakeDelay = 0.3
        numShakes = 5
    postShakeDelay = 0.5
    shakeTime = (duration-shakeDelay-postShakeDelay) / numShakes
    shakeDuration = shakeTime * (1./numShakes)
    shakeWaitInterval = shakeTime * ((numShakes-1.)/numShakes)

    def shakeCameraTrack(intensity, shakeWaitInterval=shakeWaitInterval, quake=quake,
                         shakeDuration=shakeDuration, numShakes=numShakes):
        vertShakeTrack = Sequence(
            Wait(shakeWaitInterval),
            Func(camera.setZ, camera.getZ()+intensity/2),
            Wait(shakeDuration/2),
            Func(camera.setZ, camera.getZ()-intensity),
            Wait(shakeDuration/2),
            Func(camera.setZ, camera.getZ()+intensity/2),
            )
        horizShakeTrack = Sequence(
            Wait(shakeWaitInterval-shakeDuration/2),
            Func(camera.setY, camera.getY()+intensity/4),
            Wait(shakeDuration/2),
            Func(camera.setY, camera.getY()-intensity/2),
            Wait(shakeDuration/2),
            Func(camera.setY, camera.getY()+intensity/4),
            Wait(shakeDuration/2),
            Func(camera.lookAt, Point3(0, 0, 0)),
            )
            
        shakeTrack = Sequence()
        for i in range(0, numShakes):
            if (quake == 0):
                shakeTrack.append(vertShakeTrack)
            else:
                shakeTrack.append(Parallel(vertShakeTrack, horizShakeTrack))
                
        return shakeTrack
    
    # Allow a reasonable degree of randomness in the camera's positioning
    x = 10 + random.random()*3
    if (random.random() > 0.5):
        x = -x
    z = 7 + random.random()*3
    # Let the camera display the toons
    track.append(Func(camera.setPos, x, -5, z))

    # Point the camera at the center of the battle, to shoot all the actors
    track.append(Func(camera.lookAt, Point3(0, 0, 0)))
    track.append(Wait(shakeDelay)) # Wait before shaking
    # Now shake the camera (up and down)
    track.append(shakeCameraTrack(shakeIntensity))
    track.append(Wait(postShakeDelay)) # Hold pose
    return track

def avatarCloseUpShot(avatar, duration):
    return heldRelativeShot(avatar,
                            0, 8, avatar.getHeight() * 0.66,
                            179, 15, 0,
                            duration, "avatarCloseUpShot")

# Useful for throws and button pushes
def avatarCloseUpThrowShot(avatar, duration):
    return heldRelativeShot(avatar,
                            3, 8, avatar.getHeight() * 0.66,
                            159, 3.6, 0,
                            duration, "avatarCloseUpThrowShot")

# Throws, button pushes, squirt, and suit attacks
# NOTE: For the course of a battle, toons should have "right" shots,
# and suits should have "left" shots, or vice versa
def avatarCloseUpThreeQuarterRightShot(avatar, duration):
    return heldRelativeShot(avatar,
                            5.2, 5.45, avatar.getHeight() * 0.66,
                            131.5, 3.6, 0,
                            duration, "avatarCloseUpThreeQuarterRightShot")
                            
def avatarCloseUpThreeQuarterRightShotWide(avatar, duration):
    return heldRelativeShot(avatar,
                            7.2, 8.45, avatar.getHeight() * 0.66,
                            131.5, 3.6, 0,
                            duration, "avatarCloseUpThreeQuarterRightShot")

def avatarCloseUpThreeQuarterLeftShot(avatar, duration):
    return heldRelativeShot(avatar,
                            -5.2, 5.45, avatar.getHeight() * 0.66,
                            -131.5, 3.6, 0,
                            duration, "avatarCloseUpThreeQuarterLeftShot")

def avatarCloseUpThreeQuarterRightFollowShot(avatar, duration):
    track = Sequence(name = "avatarCloseUpThreeQuarterRightFollowShot")
    track.append(
        heldRelativeShot(avatar,
                         5.2, 5.45, avatar.getHeight() * 0.66,
                         131.5, 3.6, 0,
                         duration * 0.65)
        )

    track.append(
        LerpHprInterval(nodePath=camera,
                        other=avatar,
                        duration=duration * 0.2,
                        hpr=Point3(110, 3.6, 0),
                        blendType="easeInOut")
        )

    track.append(Wait(duration * 0.25))
    return track
    

def avatarCloseUpZoomShot(avatar, duration):
    track = Sequence("avatarCloseUpZoomShot")
    # Let the camera display the toons
    track.append(
        LerpPosHprInterval(nodePath=camera,
                           other=avatar,
                           duration=duration/2,
                           startPos=Point3(0, 10, avatar.getHeight()),
                           startHpr=Point3(179, -10, 0),
                           pos=Point3(0, 6, avatar.getHeight()),
                           hpr=Point3(179, -10, 0),
                           blendType="easeInOut")
        )

    track.append(Wait(duration/2))
    
    return track

def avatarBehindShot(avatar, duration):
    return heldRelativeShot(avatar,
                            5, -7, avatar.getHeight(),
                            40, -12, 0,
                            duration, "avatarBehindShot")

def avatarBehindHighShot(avatar, duration):
    return heldRelativeShot(avatar,
                            -4, -7, 5 + avatar.getHeight(),
                            -30, -35, 0,
                            duration, "avatarBehindHighShot")

def avatarBehindHighRightShot(avatar, duration):
    return heldRelativeShot(avatar,
                            4, -7, 5 + avatar.getHeight(),
                            30, -35, 0,
                            duration, "avatarBehindHighShot")

def avatarBehindThreeQuarterRightShot(avatar, duration):
    return heldRelativeShot(avatar,
                            7.67, -8.52, avatar.getHeight() * 0.66,
                            25, 7.5, 0,
                            duration, "avatarBehindThreeQuarterRightShot")

###
# Implementation of camera "packages", which are simply a series of held and
# motion shots capturing the action of an attack
###



def avatarSideFollowAttack(suit, toon, duration, battle):
    # Three part timing on an attack: the windup, the projection, the impact
    # Use slightly random range for windupDuration, between 0-20% of total duration
    windupDuration = duration * (0.1+random.random()*0.1)
    projectDuration = duration * 0.75
    impactDuration = duration - windupDuration - projectDuration

    # Choose focal points of the actors for the camera
    suitHeight = suit.getHeight()
    toonHeight = toon.getHeight()
    suitCentralPoint = suit.getPos(battle)
    suitCentralPoint.setZ(suitCentralPoint.getZ() + suitHeight*0.75)
    toonCentralPoint = toon.getPos(battle)
    toonCentralPoint.setZ(toonCentralPoint.getZ() + toonHeight*0.75)

    # Vary the x-coordinates of the camera
    initialX = random.randint(12, 14)
    finalX = random.randint(7, 8)
    # Vary the y-coordinates of the camera
    initialY = finalY = random.randint(-3, 0)
    # Vary the z-coordinates of the camera
    initialZ = suitHeight*0.5 + random.random()*suitHeight
    finalZ = toonHeight*0.5 + random.random()*toonHeight
    # 50% chance we'll view the action from stage left or stage right
    if (random.random() > 0.5):
        initialX = -initialX
        finalX = - finalX

    return Sequence(
        focusShot(initialX, initialY, initialZ, windupDuration, suitCentralPoint), # windup
        focusMoveShot(finalX, finalY, finalZ, projectDuration, toonCentralPoint), # throw
        Wait(impactDuration), # impact
        )

def focusCameraBetweenPoints(point1, point2):
    """ focusCameraBetweenPoints() finds a bisection point between the arg points provided
        and focuses the camera on this central point """
    if (point1[0] > point2[0]):
        x = point2[0] + (point1[0]-point2[0])*0.5
    else:
        x = point1[0] + (point2[0]-point1[0])*0.5
    if (point1[1] > point2[1]):
        y = point2[1] + (point1[1]-point2[1])*0.5
    else:
        y = point1[1] + (point2[1]-point1[1])*0.5
    if (point1[2] > point2[2]):
        z = point2[2] + (point1[2]-point2[2])*0.5
    else:
        z = point1[2] + (point2[2]-point1[2])*0.5
    camera.lookAt(Point3(x, y, z))


def randomCamera(suit, toon, battle, attackDuration, openShotDuration):
    """ randomCamera() places the camera in random, though effective, position to capture
        the action of an attack, first shooting the attacker and then the defender """

    return randomAttackCam(suit, toon, battle, attackDuration,
                           openShotDuration, 'suit')

def randomAttackCam(suit, toon, battle, attackDuration, openShotDuration,
                    attackerString='suit'):
    """ randomCamSuitAttack() places the camera in a random, though effective position to
        shoot the action of an attacker, if you don't specify the attacker as
        either 'toon' or 'suit', it defaults to suit """

    if openShotDuration > attackDuration: # Ensure that it's not too long
        openShotDuration = attackDuration
    closeShotDuration = attackDuration - openShotDuration

    if (attackerString == 'suit'):
        attacker = suit
        defender = toon
        defenderString = 'toon'
    else:
        attacker = toon
        defender = suit
        defenderString = 'suit'
        
    randomDouble = random.random()
    if (randomDouble > 0.6): # 40% chance
        openShot = randomActorShot(attacker, battle, openShotDuration, attackerString)
    elif (randomDouble > 0.2): # 40% chance
        openShot = randomOverShoulderShot(suit, toon, battle,
                                          openShotDuration, focus=attackerString)
    else: # 20% chance
        openShot = randomSplitShot(attacker, defender, battle, openShotDuration)

    randomDouble = random.random()
    if (randomDouble > 0.6): # 40% chance
        closeShot = randomActorShot(defender, battle, closeShotDuration, defenderString)
    elif (randomDouble > 0.2): # 40% chance
        closeShot = randomOverShoulderShot(suit, toon, battle,
                                           closeShotDuration, focus=defenderString)
    else: # 20% chance
        closeShot = randomSplitShot(attacker, defender, battle, closeShotDuration)
        
    return Sequence(openShot, closeShot)

def randomGroupAttackCam(suit, targets, battle, attackDuration, openShotDuration):
    """ randomGroupAttackCam() places the camera in a random, though effective position to
        shoot the action of a suit attacking a group of toons (targets) """

    if openShotDuration > attackDuration: # Ensure that it's not too long
        openShotDuration = attackDuration
    closeShotDuration = attackDuration - openShotDuration

    # First we shoot the attacking suit
    openShot = randomActorShot(suit, battle, openShotDuration, 'suit', groupShot=0)
    closeShot = randomToonGroupShot(targets, suit, closeShotDuration, battle)
    return Sequence(openShot, closeShot)
    
def randomActorShot(actor, battle, duration, actorType, groupShot=0):
    """ randomActorShot() creates a random though effective shot for an actor in
        a battle, specified by arg actor of type actorType ('suit' or 'toon').  This
        function defaults to single shots of the primary actor, but a groupShot will
        pull the camera out some more."""

    height = actor.getHeight()
    centralPoint = actor.getPos(battle)
    centralPoint.setZ(centralPoint.getZ() + height*0.75)

    if (actorType == 'suit'):
        x = 4 + random.random()*8
        y = -2 - random.random()*4
        z = height*0.5 + random.random()*height*1.5
        if (groupShot == 1):
            y = -4 #y - 3 # - random.random()*4
            z = height*0.5 # z + 2 # + random.random()*3
    else:
        x = 2 + random.random()*8
        y = -2 + random.random()*3
        z = height + random.random()*height*1.5
        if (groupShot == 1):
            y = y + 3 # + random.random()*4
            z = height*0.5 #z + 2 # + random.random()*3
    if (MovieUtil.shotDirection == 'left'):
        x = -x

    return focusShot(x, y, z, duration, centralPoint)

def randomSplitShot(suit, toon, battle, duration):
    """ randomSplitShot() places the camera in random, though effective, position to capture
        both primary actors in an attack """

    suitHeight = suit.getHeight()
    toonHeight = toon.getHeight()
    suitCentralPoint = suit.getPos(battle)
    suitCentralPoint.setZ(suitCentralPoint.getZ() + suitHeight*0.75)
    toonCentralPoint = toon.getPos(battle)
    toonCentralPoint.setZ(toonCentralPoint.getZ() + toonHeight*0.75)

    x = 9 + random.random()*2
    y = -2 - random.random()*2
    z = suitHeight*0.5 + random.random()*suitHeight
    if (MovieUtil.shotDirection == 'left'):
        x = -x

    return focusShot(x, y, z, duration, toonCentralPoint,
                     splitFocusPoint=suitCentralPoint)


def randomOverShoulderShot(suit, toon, battle, duration, focus):
    """ randomOverShouldShot() creates a random, though effective, camera shot for a battle
        shooting the actor specified in arg focus ('toon' or 'suit') over the shoulder of
        the other actor in the attack """

    suitHeight = suit.getHeight()
    toonHeight = toon.getHeight()
    suitCentralPoint = suit.getPos(battle)
    suitCentralPoint.setZ(suitCentralPoint.getZ() + suitHeight*0.75)
    toonCentralPoint = toon.getPos(battle)
    toonCentralPoint.setZ(toonCentralPoint.getZ() + toonHeight*0.75)

    x = 2 + random.random()*10
    if (focus == 'toon'):
        y = 8 + random.random()*6
        z = suitHeight*1.2 + random.random()*suitHeight
    else:
        y = -10 - random.random()*6
        z = toonHeight*1.5 # toonHeight*1.5 + random.random()*toonHeight
    if (MovieUtil.shotDirection == 'left'):
        x = -x

    return focusShot(x, y, z, duration, toonCentralPoint,
                     splitFocusPoint=suitCentralPoint)


def randomCameraSelection(suit, attack, attackDuration, openShotDuration):
    """ randomCameraSelection() makes a random selection from a list of possible
        camera shots """
    
    shotChoices = [
        avatarCloseUpThrowShot,
        avatarCloseUpThreeQuarterLeftShot,
        allGroupLowShot,
        suitGroupLowLeftShot,
        avatarBehindHighShot,
    ]

    if openShotDuration > attackDuration: # Ensure that its not too long
        openShotDuration = attackDuration
    closeShotDuration = attackDuration - openShotDuration

    openShot = apply(random.choice(shotChoices), [suit, openShotDuration])
    closeShot = chooseSuitCloseShot(attack, closeShotDuration,
                                    openShot.getName(), attackDuration)
    return Sequence(openShot, closeShot)


def randomToonGroupShot(toons, suit, duration, battle):
    """ randomToonGroupShot() creates a random, though effective camera shot for a group
        of toons (2, 3, or 4) in a battle """

    # Grab the average height of these toons for the best shot
    sum = 0
    for t in toons:
        toon = t['toon']
        height = toon.getHeight()
        sum = sum + height
    avgHeight = sum / len(toons) * 0.75 # multiply by 0.75 to get the chest of the toon

    # We shoot from the opposite side of the attacking suit
    suitPos = suit.getPos(battle)
    x = 1 + random.random()*6
    if (suitPos.getX() > 0):
        x = -x
        
    # We'll either shoot a close up or far back over the shoulders of the suits        
    if (random.random() > 0.5): # 50% chance
        y = 4 + random.random()*1
        z = avgHeight + random.random()*6
    else:
        y = 11 + random.random()*2
        z = 13 + random.random()*2
    focalPoint = Point3(0, -4, avgHeight)
    return focusShot(x, y, z, duration, focalPoint)
    
    
###########################################################
##
## Fire Shots
##                                                  
###########################################################

def chooseFireShot(throws, suitThrowsDict, attackDuration):
    # Pick an open shot
    openShot = chooseFireOpenShot(throws, suitThrowsDict, attackDuration)
    openDuration = openShot.getDuration()
    openName = openShot.getName()
    # Pick a close shot
    closeShot = chooseFireCloseShot(throws, suitThrowsDict,
                                     openDuration, openName, attackDuration)
    # Compose the track
    track = Sequence(openShot, closeShot)
    # Ensure we composed it to the right length
    #assert track.getDuration() == attackDuration
    # Return it
    return track

def chooseFireOpenShot(throws, suitThrowsDict, attackDuration):
    # Setup
    numThrows = len(throws)
    av = None
    duration = 3.0
    # The single toon case
    if numThrows == 1:
        # The attacking Toon
        av = throws[0]['toon']
        # Single toon choices
        shotChoices = [
            avatarCloseUpThrowShot,
            avatarCloseUpThreeQuarterRightShot,
            avatarBehindShot,

            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi toon case
    elif numThrows >= 2 and numThrows <= 4:
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of throws: %s" % numThrows)
    # Pick a shot and return it
    shotChoice = random.choice(shotChoices)
    track = apply(shotChoice, [av, duration])
    print ("chooseFireOpenShot %s" % (shotChoice))

    # Set up the play by play text
    # Whoops! No play by play for toons, since the multi-toon case is
    # confusing...
    #pbpText = attack['playByPlayText']
    #pbpTrack = pbpText.getShowInterval(attack['prettyName'], duration)

    #mtrack = Parallel(track, pbpTrack)
    
    return track
    
def chooseFireCloseShot(throws, suitThrowsDict,
                         openDuration, openName, attackDuration):
    # Setup
    numSuits = len(suitThrowsDict)
    av = None
    duration = attackDuration - openDuration
    # The single suit case
    if numSuits == 1:
        # The attacked suit
        av = base.cr.doId2do[suitThrowsDict.keys()[0]]
        # Single suit choices
        shotChoices = [
            avatarCloseUpFireShot,
            avatarCloseUpThreeQuarterLeftFireShot,
            
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    # The multi suit case (RAU we could get 0 for uber throw)
    elif (numSuits >= 2 and numSuits <= 4) or (numSuits==0):
        # Multi suit choices
        shotChoices = [
            allGroupLowShot,
            suitGroupThreeQuarterLeftBehindShot,
            ]
    else:
        notify.error("Bad number of suits: %s" % numSuits)
    # Pick a shot and return it
    shotChoice = random.choice(shotChoices)
    track = apply(shotChoice, [av, duration])
    print ("chooseFireOpenShot %s" % (shotChoice))
    return track
    
# Useful for throws and button pushes
def avatarCloseUpFireShot(avatar, duration):
    return heldRelativeShot(avatar,
                            7, 17, avatar.getHeight() * 0.66,
                            159, 3.6, 0,
                            duration, "avatarCloseUpFireShot")
                            
def avatarCloseUpThreeQuarterLeftFireShot(avatar, duration):
    return heldRelativeShot(avatar,
                            -8.2, 8.45, avatar.getHeight() * 0.66,
                            -131.5, 3.6, 0,
                            duration, "avatarCloseUpThreeQuarterLeftShot")

