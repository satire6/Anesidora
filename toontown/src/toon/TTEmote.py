"""TTEmote module: contains the TTEmote class

This class defines emotions that the Toon can enable
at certain times during the game.  (Times when a toon
should not be able to use an emote are: during some
parts of a battle, minigames, while running, etc)

"""



import Toon, ToonDNA
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
import types
from direct.showbase import PythonUtil
from pandac.PandaModules import *
from otp.avatar import Emote
from direct.directnotify import DirectNotifyGlobal

# The emoteHandlerFunc takes an emote name from the SpeedChat menu
# and calls setAnimState function for the toon
#def emoteHandlerFunc():

# Some emotes are Tracks which can be played, joined in progress, and stopped
# Emotes generally return a track (can be empty for simple things), and a duration (can
# be zero for simple things).  It is important that the duration is specified for most
# animations, since we will need to restart the trackToAnim task after the animation
# is played.  Exceptions are sleep, yes, no, etc, where we are not playing an
# actual animation, rather just putting the toon in sleep state, or manually moving
# it's head for yes/no.

# added later:  sometime we have something special we want to play on exiting
# the emote....add this to the exitTrack arg.

# special case behavior:
# keep track of which is the sleep index,
EmoteSleepIndex = 4

EmoteClear = -1

def doVictory(toon, volume = 1):
    duration = toon.getDuration('victory', 'legs')
    sfx = base.loadSfx("phase_3.5/audio/sfx/ENC_Win.mp3")

    # Loop this sound effect for the appropriate duration
    sfxDuration = duration - 1.0
    sfxTrack = SoundInterval(sfx, loop=1, duration=sfxDuration, node=toon, volume=volume)

    # We must include the sound interval in the overall sequence so
    # that it gets cleaned up properly should we suddenly abort, but
    # we artificially set the duration to 0 to make the Emote system
    # happy (since it expects a zero-length sequence).
    track = Sequence(Func(toon.play, 'victory'),
                     sfxTrack,
                     duration = 0)
    return track, duration, None

def doJump(toon, volume = 1):
    track = Sequence(Func(toon.play, 'jump'))
    return track, 0, None

def doDead(toon, volume = 1):
    toon.animFSM.request('Sad')
    return None, 0, None

def doAnnoyed(toon, volume = 1):
    duration = toon.getDuration('angry', 'torso')
    # This sfx is in phase 3.5 because it can be triggered during the tutorial
    sfx = None
    if (toon.style.getAnimal() == 'bear'):
        sfx = base.loadSfx("phase_3.5/audio/dial/AV_bear_exclaim.mp3")
    else:
        sfx = base.loadSfx("phase_3.5/audio/sfx/avatar_emotion_angry.mp3")
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx():
        base.playSfx(sfx, volume = volume, node = toon)
    track = Sequence(Func(toon.angryEyes),
                     Func(toon.blinkEyes),
                     Func(toon.play, 'angry'),
                     Func(playSfx)
                     )
    exitTrack = Sequence(
        Func(toon.normalEyes),
        Func(toon.blinkEyes))
    return track, duration, exitTrack

def doAngryEyes(toon, volume=1):
    track = Sequence(Func(toon.angryEyes),
                     Func(toon.blinkEyes),
                     Wait(10.0),
                     Func(toon.normalEyes))
    return track, .1, None

def doHappy(toon, volume=1):
    track = Sequence(Func(toon.play, 'jump'),
                     Func(toon.normalEyes),
                     Func(toon.blinkEyes))
    duration = toon.getDuration('jump', 'legs')
    return track, duration, None

def doSad(toon, volume=1):
    track = Sequence(Func(toon.sadEyes),
                     Func(toon.blinkEyes))
    exitTrack = Sequence(Func(toon.normalEyes), 
                         Func(toon.blinkEyes))
    return track, 3, exitTrack

# Sleep is a special case.  We don't want to set up a
# sleep track....just put the avatar to sleep, and then
# wait for any activity on the client to wake him up
def doSleep(toon, volume=1):
    #if toon == base.localAvatar:
    #    toon.gotoSleep()
    #return None, 0, None
    duration = 4
    track = Sequence(Func(toon.stopLookAround),
                     Func(toon.stopBlink),
                     Func(toon.closeEyes),
                     Func(toon.lerpLookAt, Point3(0, 1, -4)),
                     Func(toon.loop, "neutral"),
                     Func(toon.setPlayRate, 0.4, "neutral"),
                     Func(toon.setChatAbsolute, TTLocalizer.ToonSleepString, CFThought),
                     )
    def wakeUpFromSleepEmote():
        toon.startLookAround()
        toon.openEyes()
        toon.startBlink()
        toon.setPlayRate(1, "neutral")
        if toon.nametag.getChat() == TTLocalizer.ToonSleepString:
            toon.clearChat()
        toon.lerpLookAt(Point3(0, 1, 0), time=0.25)
    exitTrack = Sequence(Func(wakeUpFromSleepEmote),
                         )
    return track, duration, exitTrack


# Nodding yes or no.  These also work like sleep, since we are
# manually animating the head, there is no need to return the
# track.  Just play it, and the rest of the toons body continues
# to do whatever it was previously doing
def doYes(toon, volume = 1):
    tracks = Parallel(autoFinish = 1)
    for lod in toon.getLODNames():
        h = toon.getPart('head', lod)
        tracks.append(
            Sequence(LerpHprInterval(h, 0.1, Vec3(0,-30,0)), LerpHprInterval(h, 0.15, Vec3(0,20,0)),
                     LerpHprInterval(h, 0.15, Vec3(0,-20,0)), LerpHprInterval(h, 0.15, Vec3(0,20,0)),
                     LerpHprInterval(h, 0.15, Vec3(0,-20,0)), LerpHprInterval(h, 0.15, Vec3(0,20,0)),
                     LerpHprInterval(h, 0.1, Vec3(0,0,0)), ))
    tracks.start()
    return None, 0, None

def doNo(toon, volume = 1):
    tracks = Parallel(autoFinish = 1)
    for lod in toon.getLODNames():
        h = toon.getPart('head', lod)
        tracks.append(
            Sequence(LerpHprInterval(h, 0.1, Vec3(40,0,0)), LerpHprInterval(h, 0.15, Vec3(-40,0,0)),
                     LerpHprInterval(h, 0.15, Vec3(40,0,0)), LerpHprInterval(h, 0.15, Vec3(-40,0,0)),
                     LerpHprInterval(h, 0.15, Vec3(20,0,0)), LerpHprInterval(h, 0.15, Vec3(-20,0,0)),
                     LerpHprInterval(h, 0.1, Vec3(0,0,0)), ))
    tracks.start()
    return None, 0, None

def doOk(toon, volume = 1):
    # fill in when we have an animation ready
    return None, 0, None

def doShrug(toon, volume = 1):
    # This sfx is in phase 3.5 because it can be triggered during the tutorial
    sfx = base.loadSfx("phase_3.5/audio/sfx/avatar_emotion_shrug.mp3")
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx():
        base.playSfx(sfx, volume = volume, node = toon)
    track = Sequence(Func(toon.play, 'shrug'),
                     Func(playSfx))
    duration = toon.getDuration('shrug', 'torso')
    return track, duration, None

def doWave(toon, volume = 1):
    track = Sequence(Func(toon.play, 'wave'))
    duration = toon.getDuration('wave', 'torso')
    return track, duration, None

def doApplause(toon, volume = 1):
    sfx = base.loadSfx("phase_4/audio/sfx/avatar_emotion_applause.mp3")
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx():
        base.playSfx(sfx, volume = 1, node = toon)
    track = Sequence(Func(toon.play, 'applause'),
                     Func(playSfx))
    duration = toon.getDuration('applause', 'torso')
    return track, duration, None

def doConfused(toon, volume =1):
    sfx = base.loadSfx("phase_4/audio/sfx/avatar_emotion_confused.mp3")
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx():
        base.playSfx(sfx, node = toon, volume = volume)
    track = Sequence(Func(toon.play, 'confused'),
                     Func(playSfx))
    duration = toon.getDuration('confused', 'torso')
    return track, duration, None

def doSlipForward(toon, volume = 1):
    sfx = base.loadSfx("phase_4/audio/sfx/MG_cannon_hit_dirt.mp3")
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx():
        base.playSfx(sfx, volume = volume, node = toon)
    sfxDelay = 0.7
    track = Sequence(Func(toon.play, 'slip-forward'),
                     Wait(sfxDelay),
                     Func(playSfx))
    duration = toon.getDuration('slip-forward', 'torso') - sfxDelay
    return track, duration, None

def doBored(toon, volume = 1):
    sfx = base.loadSfx("phase_4/audio/sfx/avatar_emotion_bored.mp3")
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx():
        base.playSfx(sfx, volume = volume, node = toon)
    sfxDelay = 2.2
    track = Sequence(Func(toon.play, 'bored'),
                     Wait(sfxDelay),
                     Func(playSfx)
                     )
    # Subtract out wait to get proper wait interval in DoEmote
    duration = toon.getDuration('bored', 'torso') - sfxDelay
    return track, duration, None

def doBow(toon, volume = 1):
    if toon.style.torso[1] == 'd':
        track = Sequence(Func(toon.play, 'curtsy'))
        duration = toon.getDuration('curtsy', 'torso')
    else:
        track = Sequence(Func(toon.play, 'bow'))
        duration = toon.getDuration('bow', 'torso')
    return track, duration, None

def doSlipBackward(toon, volume = 1):
    sfx = base.loadSfx("phase_4/audio/sfx/MG_cannon_hit_dirt.mp3")
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx():
        base.playSfx(sfx, volume = volume, node = toon)
    sfxDelay = 0.7
    track = Sequence(Func(toon.play, 'slip-backward'),
                     Wait(sfxDelay),
                     Func(playSfx))
    duration = toon.getDuration('slip-backward', 'torso') - sfxDelay
    return track, duration, None

def doThink(toon, volume = 1):
    duration = (47.0 / 24.0) * 2
    animTrack = Sequence(
        ActorInterval(toon, 'think', startFrame = 0, endFrame = 46),
        ActorInterval(toon, 'think', startFrame = 46, endFrame = 0),
        )
    track = Sequence(animTrack,
                     duration = 0)
    return track, duration, None

def doCringe(toon, volume = 1):
    track = Sequence(Func(toon.play, 'cringe'))
    duration = toon.getDuration('cringe', 'torso')
    return track, duration, None

def doResistanceSalute(toon, volume = 1):
    playRate = 0.75
    duration = ((10.0 / 24.0) * ( 1 / playRate)) * 2
    animTrack = Sequence(
        Func(toon.setChatAbsolute, OTPLocalizer.CustomSCStrings[4020], CFSpeech | CFTimeout),
        Func(toon.setPlayRate, playRate, 'victory'),
        ActorInterval(toon, 'victory', playRate = playRate, startFrame = 0, endFrame = 9),
        ActorInterval(toon, 'victory', playRate = playRate, startFrame = 9, endFrame = 0),
        )
    track = Sequence(animTrack,
                     duration = 0)
    return track, duration, None

def doNothing(toon, volume =1):
    return None, 0, None

def doSurprise(toon, volume = 1):
    sfx = None
    sfx = base.loadSfx("phase_4/audio/sfx/avatar_emotion_surprise.mp3")
    
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx(volume = 1):
        base.playSfx(sfx, volume = volume, node = toon)
    
    def playAnim(anim):
        anim.start()    
    
    def stopAnim(anim):
        anim.finish()
        toon.stop()
        sfx.stop()
        
    anim = Sequence(ActorInterval(toon, 'conked', startFrame = 9, endFrame = 50),
                    ActorInterval(toon, 'conked', startFrame = 70, endFrame = 101))
                    
    track = Sequence(Func(toon.stopBlink),
                     Func(toon.surpriseEyes),
                     Func(toon.showSurpriseMuzzle),
                     Parallel(Func(playAnim, anim), Func(playSfx, volume)))
                     
    exitTrack = Sequence(Func(toon.hideSurpriseMuzzle),
                         Func(toon.openEyes),
                         Func(toon.startBlink),
                         Func(stopAnim, anim))
    
    # Adding duration of 0.1 so that we return back to the last animation.
    return track, 3., exitTrack

def doUpset(toon, volume = 1):
    sfx = None
    sfx = base.loadSfx("phase_4/audio/sfx/avatar_emotion_very_sad_1.mp3")
        
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx(volume = 1):
        base.playSfx(sfx, volume = volume, node = toon)
    
    def playAnim(anim):
        anim.start()
    
    def stopAnim(anim):
        anim.finish()
        toon.stop()
        sfx.stop()
        
    anim = Sequence(ActorInterval(toon, 'bad-putt', startFrame = 29, endFrame = 59, playRate = -0.75),
                    ActorInterval(toon, 'bad-putt', startFrame = 29, endFrame = 59, playRate = 0.75))
    
    track = Sequence(Func(toon.sadEyes),
                     Func(toon.blinkEyes),
                     Func(toon.showSadMuzzle),
                     Parallel(Func(playAnim, anim), Func(playSfx, volume)))
    exitTrack = Sequence(Func(toon.hideSadMuzzle),
                         Func(toon.normalEyes),
                         Func(stopAnim, anim))
    return track, 4., exitTrack
    
def doDelighted(toon, volume = 1):
    sfx = None
    sfx = base.loadSfx('phase_4/audio/sfx/delighted_06.mp3')
    
    def playSfx(volume = 1):
        base.playSfx(sfx, volume = volume, node = toon)
    
    def playAnim(anim):
        anim.start()
    
    def stopAnim(anim):
        anim.finish()
        toon.stop()
        sfx.stop()
        
    anim = Sequence(ActorInterval(toon, 'left'),
                    Wait(1),
                    ActorInterval(toon, 'left', playRate = -1))
    
    track = Sequence(Func(toon.blinkEyes),
                     Func(toon.showSmileMuzzle),
                     Parallel(Func(playAnim, anim), Func(playSfx, volume)))

    exitTrack = Sequence(Func(toon.hideSmileMuzzle),
                         Func(toon.blinkEyes),
                         Func(stopAnim, anim))

    return track, 2.5, exitTrack
    
def doFurious(toon, volume = 1):
    duration = toon.getDuration('angry', 'torso')
    # This sfx is in phase 3.5 because it can be triggered during the tutorial
    sfx = None
    sfx = base.loadSfx("phase_4/audio/sfx/furious_03.mp3")
    
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx(volume = 1):
        base.playSfx(sfx, volume = volume, node = toon)
    
    track = Sequence(Func(toon.angryEyes),
                     Func(toon.blinkEyes),
                     Func(toon.showAngryMuzzle),
                     Func(toon.play, 'angry'),
                     Func(playSfx, volume))
    exitTrack = Sequence(
        Func(toon.normalEyes),
        Func(toon.blinkEyes),
        Func(toon.hideAngryMuzzle))
    return track, duration, exitTrack
    
def doLaugh(toon, volume = 1):
    sfx = None
    sfx = base.loadSfx("phase_4/audio/sfx/avatar_emotion_laugh.mp3")
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx(volume = 1):
        base.playSfx(sfx, volume = volume, node = toon)
    def playAnim():
        toon.setPlayRate(10, 'neutral')
        toon.loop('neutral')
    def stopAnim():
        toon.setPlayRate(1, 'neutral')
    track = Sequence(Func(toon.blinkEyes),
                     Func(toon.showLaughMuzzle),
                     Func(playAnim),
                     Func(playSfx, volume))
    exitTrack = Sequence(Func(toon.hideLaughMuzzle),
                         Func(toon.blinkEyes),
                         Func(stopAnim))
    return track, 2, exitTrack

def getSingingNote(toon, note, volume = 1):
    """
    Returns a track of the toon singing the requested note.
    note is a string in small letters. Eg - g1, a, b, c, d, e, f, g2
    """
    sfx = None
    filePath = "phase_3.5/audio/dial/"
    filePrefix = "tt_s_dlg_sng_"
    fileSuffix = ".mp3"
    speciesName = ToonDNA.getSpeciesName(toon.style.head)
    sfx = base.loadSfx(filePath + filePrefix + speciesName + "_" + note + fileSuffix)
    # Need to use a Func interval since DoEmote expects a 0 duration track
    def playSfx(volume = 1):
        base.playSfx(sfx, volume = volume, node = toon)
    def playAnim():
        toon.loop('neutral')
    def stopAnim():
        toon.setPlayRate(1, 'neutral')
    
    track = Sequence(Func(toon.showSurpriseMuzzle),
                     Parallel(Func(playAnim), Func(playSfx, volume)))
                     
    exitTrack = Sequence(Func(toon.hideSurpriseMuzzle),
                         Func(stopAnim))
    
    return track, 0.1, exitTrack
    
def playSingingAnim(toon):
    """
    """
    pass

def stopSinginAnim(toon):
    """
    """
    pass

def singNote1(toon, volume = 1):
    if base.config.GetBool('want-octaves', True):
        if toon.style.getTorsoSize() == 'short':
            return getSingingNote(toon, 'g1')
        elif toon.style.getTorsoSize()  == 'medium':
            return getSingingNote(toon, 'g2')
        elif toon.style.getTorsoSize()  == 'long':
            return getSingingNote(toon, 'g3')

def singNote2(toon, volume = 1):
    if base.config.GetBool('want-octaves', True):
        if toon.style.getTorsoSize() == 'short':
            return getSingingNote(toon, 'a1')
        elif toon.style.getTorsoSize()  == 'medium':
            return getSingingNote(toon, 'a2')
        elif toon.style.getTorsoSize()  == 'long':
            return getSingingNote(toon, 'a3')

def singNote3(toon, volume = 1):
    if base.config.GetBool('want-octaves', True):
        if toon.style.getTorsoSize() == 'short':
            return getSingingNote(toon, 'b1')
        elif toon.style.getTorsoSize()  == 'medium':
            return getSingingNote(toon, 'b2')
        elif toon.style.getTorsoSize()  == 'long':
            return getSingingNote(toon, 'b3')

def singNote4(toon, volume = 1):
    if base.config.GetBool('want-octaves', True):
        if toon.style.getTorsoSize() == 'short':
            return getSingingNote(toon, 'c1')
        elif toon.style.getTorsoSize()  == 'medium':
            return getSingingNote(toon, 'c2')
        elif toon.style.getTorsoSize()  == 'long':
            return getSingingNote(toon, 'c3')

def singNote5(toon, volume = 1):
    if base.config.GetBool('want-octaves', True):
        if toon.style.getTorsoSize() == 'short':
            return getSingingNote(toon, 'd1')
        elif toon.style.getTorsoSize()  == 'medium':
            return getSingingNote(toon, 'd2')
        elif toon.style.getTorsoSize()  == 'long':
            return getSingingNote(toon, 'd3')

def singNote6(toon, volume = 1):
    if base.config.GetBool('want-octaves', True):
        if toon.style.getTorsoSize() == 'short':
            return getSingingNote(toon, 'e1')
        elif toon.style.getTorsoSize()  == 'medium':
            return getSingingNote(toon, 'e2')
        elif toon.style.getTorsoSize()  == 'long':
            return getSingingNote(toon, 'e3')

def singNote7(toon, volume = 1):
    if base.config.GetBool('want-octaves', True):
        if toon.style.getTorsoSize() == 'short':
            return getSingingNote(toon, 'f1')
        elif toon.style.getTorsoSize()  == 'medium':
            return getSingingNote(toon, 'f2')
        elif toon.style.getTorsoSize()  == 'long':
            return getSingingNote(toon, 'f3')

def singNote8(toon, volume = 1):
        if base.config.GetBool('want-octaves', True):
            if toon.style.getTorsoSize() == 'short':
                return getSingingNote(toon, 'g2')
            elif toon.style.getTorsoSize()  == 'medium':
                return getSingingNote(toon, 'g3')
            elif toon.style.getTorsoSize()  == 'long':
                return getSingingNote(toon, 'g4')

def singNoteEmpty(toon, volume = 0):
    track = Sequence()
    return track, 0.1, None

def returnToLastAnim(toon):
    if hasattr(toon, "playingAnim") and toon.playingAnim:
        toon.loop(toon.playingAnim)
    else:
        if not hasattr(toon, "hp") or toon.hp > 0:
            toon.loop('neutral')
        else:
            toon.loop('sad-neutral')

# Emote data is stored in the order it appears in the SpeedChat
# The integer stored is the reference count to the Emote.  If t
# count goes above zero, it means that the emote is disabled.
# a minigame might increment the reference count if it wants to
# disable emotes.

# NOTE: Missing slot for idea, may require database patch to ad
EmoteFunc = [
    [doWave, 0],     # 0
    [doHappy, 0],    # 1
    [doSad, 0],      # 2
    [doAnnoyed, 0],  # 3
    [doSleep, 0],    # 4
    [doShrug, 0],    # 5 Catalog Series 1
    [doVictory, 0],  # 6 Catalog Series 2
    [doThink, 0],    # 7 Catalog Series 4
    [doBored, 0],    # 8 Catalog Series 2
    [doApplause, 0], # 9 Catalog Series 1
    [doCringe, 0],   # 10 Catalog Series 4
    [doConfused, 0], # 11 Catalog Series 2
    [doSlipForward, 0], # 12 Catalog Series 7
    [doBow, 0],      # 13 Catalog Series 1
    [doSlipBackward, 0], # 14 Catalog Series 7
    [doResistanceSalute, 0], # 15 Toons of the World Unite!
    [doNothing, 0],  # 16 doLaugh - TBD
    [doYes, 0],      #17 doYes
    [doNo, 0],       #18 doNo
    [doOk, 0],       #19 doOk
    [doSurprise, 0], #20 doSurprise muzzle emote
    [doUpset, 0],    #21 doUpset muzzle emote
    [doDelighted, 0],#22 doDelighted muzzle emote
    [doFurious, 0],  #23 doFurious muzzle emote
    [doLaugh, 0],    #24 doLaugh muzzle emote
##    [singNote1, 0],  #25 sing c1 note of toon species
##    [singNote2, 0],  #26 sing d note of toon species
##    [singNote3, 0],  #27 sing e note of toon species
##    [singNote4, 0],  #28 sing f note of toon species
##    [singNote5, 0],  #29 sing g note of toon species
##    [singNote6, 0],  #30 sing a note of toon species
##    [singNote7, 0],  #31 sing b note of toon species
##    [singNote8, 0],  #32 sing c2 note of toon species
##    [singNoteEmpty, 0], #33 sing blank note of toon species
    ]

assert(len(EmoteFunc) == len(OTPLocalizer.EmoteList))

class TTEmote(Emote.Emote):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTEmote')
    # Store sleep index, because it is a special case
    SLEEP_INDEX = 4

    def __init__(self):
        # emoteAccess is an array of bits that tells which
        # emotes we have access to.  Must be the same size
        # as Emote.emoteFunc.  Yes, Ok, No, Bye and Hello
        # should be turned off, because they appear in a
        # different part of the SC menu

        self.emoteFunc = EmoteFunc
        # Index of "body" emotes (emotes using all of the body)
        self.bodyEmotes = [0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,20,21,22,23,24]

        # Index of "head" emotes (emotes just involving the head)
        self.headEmotes = [2,17,18,19]

        # sanity check
        if len(self.emoteFunc) != len(OTPLocalizer.EmoteList):
            self.notify.error("Emote.EmoteFunc and OTPLocalizer.EmoteList are different lengths.")

        # the current track being played
        self.track = None

        self.stateChangeMsgLocks = 0
        self.stateHasChanged = 0

    # utility functions to queue up EmoteEnableStateChanged messages

    def lockStateChangeMsg(self):
        self.stateChangeMsgLocks += 1

    def unlockStateChangeMsg(self):
        if self.stateChangeMsgLocks <= 0:
            print PythonUtil.lineTag() + ": someone unlocked too many times"
            return

        self.stateChangeMsgLocks -= 1
        if self.stateChangeMsgLocks == 0 and self.stateHasChanged:
            messenger.send(self.EmoteEnableStateChanged)
            self.stateHasChanged = 0

    def emoteEnableStateChanged(self):
        if self.stateChangeMsgLocks > 0:
            self.stateHasChanged = 1
        else:
            messenger.send(self.EmoteEnableStateChanged)

    # All emotes
    def disableAll(self, toon, msg = None):
        if toon != base.localAvatar:
            return
        # increment the reference count on all emotes
        self.disableGroup(range(len(self.emoteFunc)), toon)

        #self.printEmoteState("disableAll", msg)

    def releaseAll(self, toon, msg = None):
        if toon != base.localAvatar:
            return

        # decrement the reference count on all emotes
        self.enableGroup(range(len(self.emoteFunc)), toon)
        #self.printEmoteState("releaseAll", msg)

    # Body emotes
    def disableBody(self, toon, msg = None):
        if toon != base.localAvatar:
            return

        # increment the reference count on body emotes
        self.disableGroup(self.bodyEmotes, toon)
        #self.printEmoteState("disableBody", msg)

    def releaseBody(self, toon, msg = None):
        if toon != base.localAvatar:
            return

        # decrement the reference count on body emotes
        self.enableGroup(self.bodyEmotes, toon)
        #self.printEmoteState("releaseBody", msg)

    # Head emotes
    def disableHead(self, toon, msg = None):
        if toon != base.localAvatar:
            return
        # increment the reference count on head emotes
        self.disableGroup(self.headEmotes, toon)
        #self.printEmoteState("disableHead", msg)

    def releaseHead(self, toon, msg = None):
        if toon != base.localAvatar:
            return

        # decrement the reference count on head emotes
        self.enableGroup(self.headEmotes, toon)
        #self.printEmoteState("releaseHead", msg)

    def getHeadEmotes(self):
        return self.headEmotes

    # groups of emotes
    def disableGroup(self, indices, toon):
        self.lockStateChangeMsg()
        for i in indices:
            self.disable(i, toon)
        self.unlockStateChangeMsg()

    def enableGroup(self, indices, toon):
        self.lockStateChangeMsg()
        for i in indices:
            self.enable(i, toon)
        self.unlockStateChangeMsg()

    # Specific emotes
    def disable(self, index, toon):
        # find the emotes index if we are given a string
        if isinstance(index, types.StringType):
            index = OTPLocalizer.EmoteFuncDict[index]

        self.emoteFunc[index][1] = self.emoteFunc[index][1] + 1
        if toon is base.localAvatar:
            if self.emoteFunc[index][1] == 1:
                self.emoteEnableStateChanged()

    def enable(self, index, toon):
        # find the emotes index if we are given a string
        if isinstance(index, types.StringType):
            index = OTPLocalizer.EmoteFuncDict[index]

        self.emoteFunc[index][1] = self.emoteFunc[index][1] - 1
        if toon is base.localAvatar:
            if self.emoteFunc[index][1] == 0:
                self.emoteEnableStateChanged()

    def doEmote(self, toon, emoteIndex, ts=0, volume = 1):
        try:
            func = self.emoteFunc[emoteIndex][0]
        except:
            print "Error in finding emote func %s" % emoteIndex
            return None, None

        def clearEmoteTrack():
            base.localAvatar.emoteTrack = None
            # Send everybody a clear for this field
            # TODO: do we need to make sure we are still a valid distObj here?
            base.localAvatar.d_setEmoteState(self.EmoteClear, 1.0)
        
        # Get the track for this emotion
        if (volume == 1):
            track, duration, exitTrack = func(toon)
        else:
            track, duration, exitTrack = func(toon, volume)
        if (track != None): # and toon == base.localAvatar):
            # disable other emotes during this emote
            track = Sequence(Func(self.disableAll, toon, "doEmote"), track)
            if (duration > 0):
                track = Sequence(track,Wait(duration))
            if (exitTrack != None):
                track = Sequence(track, exitTrack)
            #if (emoteIndex != EmoteSleepIndex and duration > 0):
            if (duration > 0):
                track = Sequence(track, Func(returnToLastAnim, toon))
            # reenable emotes
            track = Sequence(track, Func(self.releaseAll, toon, "doEmote"), autoFinish = 1)
            if toon.isLocal():
                track = Sequence(track, Func(clearEmoteTrack))

        if track != None:
            if toon.emote != None:
                toon.emote.finish()
                toon.emote = None
            toon.emote = track
            track.start(ts)

        del clearEmoteTrack

        return track, duration

    def printEmoteState(self, action, msg):
        if __debug__:
            print "%s(%s), body(%s), head(%s)" % (action, msg, EmoteFunc[0][1], EmoteFunc[2][1])

Emote.globalEmote = TTEmote()

