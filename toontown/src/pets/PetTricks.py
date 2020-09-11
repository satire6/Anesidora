"""PetTricks.py"""

from direct.showbase.PythonUtil import Enum, invertDictLossless
from direct.interval.IntervalGlobal import *
import types
import random

# ONLY ADD TRICKS JUST BEFORE 'BALK'
# BALK is not really a trick; it's what the pets do if they don't do the trick
# correctly. Keep it at the end of the Enum.
Tricks = Enum('JUMP, BEG, PLAYDEAD, ROLLOVER, BACKFLIP, DANCE, SPEAK, BALK,')
assert Tricks.BALK == len(Tricks)-1

# these are what aptitude 0. and 1. map to in an actual random range of [0,1]
NonHappyMinActualTrickAptitude = .1
NonHappyMaxActualTrickAptitude = .6
MinActualTrickAptitude = .5
MaxActualTrickAptitude = .97

AptitudeIncrementDidTrick = .0005
MaxAptitudeIncrementGotPraise = .0003

# these are values in [0..1] that will be added to the pet's fatigue ([0..1])
# when the pet does a trick. The actual value that will be used will be an
# interpolation of these values, based on how good the pet is at the trick.
# Note that the value in [0..1] at which the pet becomes fatigued (the
# fatigueThreshold) is different from pet to pet; see PetTraits.TraitDescs.
MaxTrickFatigue = .65
MinTrickFatigue = .1

# Trick ID to SpeedChat static-text phrase
ScId2trickId = {
    21200: Tricks.JUMP,
    21201: Tricks.BEG,
    21202: Tricks.PLAYDEAD,
    21203: Tricks.ROLLOVER,
    21204: Tricks.BACKFLIP,
    21205: Tricks.DANCE,
    21206: Tricks.SPEAK,
    }
# multiple SC entries may map to the same trick ID. This dict contains
# lists of SC IDs for each trick ID.
TrickId2scIds = invertDictLossless(ScId2trickId)

TrickAnims = {
    Tricks.JUMP: 'jump',
    Tricks.BEG:  ('toBeg', 'beg', 'fromBeg'),
    Tricks.PLAYDEAD: ('playDead', 'fromPlayDead'),
    Tricks.ROLLOVER: 'rollover',
    Tricks.BACKFLIP: 'backflip',
    Tricks.DANCE: 'dance',
    Tricks.SPEAK: 'speak',
    Tricks.BALK: 'neutral',
    }
assert len(TrickAnims) == len(Tricks)

TrickLengths = {
    Tricks.JUMP: 2.,
    Tricks.BEG:  5.167,
    Tricks.PLAYDEAD: 15.21,
    Tricks.ROLLOVER: 8.,
    Tricks.BACKFLIP: 4.88,
    Tricks.DANCE: 7.42,
    Tricks.SPEAK: 0.75,
    Tricks.BALK: 1.,
    }
assert len(TrickLengths) == len(Tricks)

TrickAccuracies = {
    Tricks.JUMP: 1.0,
    Tricks.BEG:  0.9,
    Tricks.PLAYDEAD: 0.8,
    Tricks.ROLLOVER: 0.7,
    Tricks.BACKFLIP: 0.6,
    Tricks.DANCE: 0.5,
    Tricks.SPEAK: 0.4,
    Tricks.BALK: 1.0,
    }
assert len(TrickAccuracies) == len(Tricks)

TrickHeals = {
    Tricks.JUMP: (5, 10),
    Tricks.BEG: (6, 12),
    Tricks.PLAYDEAD: (7, 14),
    Tricks.ROLLOVER: (8, 16),
    Tricks.BACKFLIP: (9, 18),
    Tricks.DANCE: (10, 20),
    Tricks.SPEAK: (11, 22),
    Tricks.BALK: (0, 0),
    }
assert len(TrickHeals) == len(Tricks)

"""
TrickHeals = {
    Tricks.JUMP: 5,
    Tricks.BEG:  6,
    Tricks.PLAYDEAD: 5,
    Tricks.ROLLOVER: 5,
    Tricks.BACKFLIP: 5,
    Tricks.DANCE: 7,
    Tricks.SPEAK: 5,
    Tricks.BALK: 0,
    }
assert len(TrickHeals) == len(Tricks)
"""

TrickSounds = {
    Tricks.BACKFLIP: 'phase_5/audio/sfx/backflip.mp3',
    Tricks.ROLLOVER: 'phase_5/audio/sfx/rollover.mp3',
    Tricks.PLAYDEAD: 'phase_5/audio/sfx/play_dead.mp3',
    Tricks.BEG: 'phase_5/audio/sfx/beg.mp3',
    Tricks.DANCE: 'phase_5/audio/sfx/heal_dance.mp3',
    Tricks.JUMP: 'phase_5/audio/sfx/jump.mp3',
    Tricks.SPEAK: 'phase_5/audio/sfx/speak_v1.mp3'
    }

def getSoundIval(trickId):
    sounds = TrickSounds.get(trickId, None)
    if sounds:
        if type(sounds) == types.StringType:
            sound = loader.loadSfx(sounds)
            return SoundInterval(sound)
        else:
            soundIval = Sequence()
            for s in sounds:
                sound = loader.loadSfx(s)
                soundIval.append(SoundInterval(sound))
            return soundIval
    return None

def getTrickIval(pet, trickId):
    anims = TrickAnims[trickId]

    # Jitter the animation rate and stagger the trick playback
    # with a Wait call. Primarily done for the case when multiple
    # pets perform a trick.
    animRate = random.uniform(.9, 1.1)
    waitTime = random.uniform(0.0, 1.0)
    
    if type(anims) == types.StringType:
        # If-Else statement to construct animation intervals based-on
        # specific tricks that cannot be generated generically, ie the jump
        # because the z-offset was left out of the animation.
        if trickId == Tricks.JUMP:
            animIval = Parallel()
            animIval.append(ActorInterval(pet, anims, playRate=animRate))
            animIval.append(Sequence(Wait(.36),
                                    ProjectileInterval(pet,
                                                       startPos = pet.getPos(),
                                                       endPos = pet.getPos(),
                                                       duration = 1.,
                                                       gravityMult = 0.5 )
                                    )
                           )
        elif trickId == Tricks.ROLLOVER:
            animIval = Sequence()
            animIval.append(ActorInterval(pet, anims, playRate=animRate))
            animIval.append(ActorInterval(pet, anims, playRate=-1.0*animRate))
        elif trickId == Tricks.SPEAK:
            animIval = ActorInterval(pet, anims, startFrame = 10, playRate=animRate)
        else:
            animIval = ActorInterval(pet, anims, playRate=animRate)
    else:
        animIval = Sequence()
        for anim in anims:
            animIval.append(ActorInterval(pet, anim, playRate=animRate))

    # Setup the Trick Interval
    trickIval = Parallel(animIval)

    soundIval = getSoundIval(trickId)
    if soundIval:
        trickIval.append(soundIval)
    
    return Sequence(
        Func(pet.lockPet),
        Wait(waitTime),
        trickIval,
        Func(pet.unlockPet)
        )
