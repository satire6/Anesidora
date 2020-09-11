from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from BattleBase import *

from direct.actor import Actor
from toontown.suit import SuitDNA
from direct.directnotify import DirectNotifyGlobal
import DistributedBattleBase
from toontown.toon import TTEmote
from otp.avatar import Emote
from toontown.toonbase import TTLocalizer
import MovieUtil
from direct.fsm import State
from toontown.suit import Suit
import SuitBattleGlobals
import random
from toontown.toonbase import ToontownGlobals

class DistributedBattleBldg(DistributedBattleBase.DistributedBattleBase):

    notify = DirectNotifyGlobal.directNotify.newCategory(
                                                'DistributedBattleBldg')

    camFOFov = 30.0
    camFOPos = Point3(0, -10, 4)

    def __init__(self, cr):
        """__init__(cr)
        """
        #townBattle = cr.playGame.hood.place.townBattle
        townBattle = cr.playGame.getPlace().townBattle
        DistributedBattleBase.DistributedBattleBase.__init__(self, cr,
                                                  townBattle)
        self.streetBattle = 0

        # Add a new reward state to the battle ClassicFSM
        self.fsm.addState(State.State('BuildingReward',
                                        self.enterBuildingReward,
                                        self.exitBuildingReward,
                                        ['Resume']))
        offState = self.fsm.getStateNamed('Off')
        offState.addTransition('BuildingReward')
        playMovieState = self.fsm.getStateNamed('PlayMovie')
        playMovieState.addTransition('BuildingReward')

    def generate(self):
        """ generate()
        """
        DistributedBattleBase.DistributedBattleBase.generate(self)
        #dbgBattleMarkers = loader.loadModel("dbgBattleMarkers.egg")
        #dbgBattleMarkers.reparentTo(self)

    def setBossBattle(self, value):
        self.bossBattle = value
        if self.bossBattle:
            self.battleMusic = base.loadMusic(
                'phase_7/audio/bgm/encntr_suit_winning_indoor.mid')
        else:
            self.battleMusic = base.loadMusic(
                'phase_7/audio/bgm/encntr_general_bg_indoor.mid')
        base.playMusic(self.battleMusic, looping=1, volume=0.9)
            
    def disable(self):
        """ disable()
        """
        DistributedBattleBase.DistributedBattleBase.disable(self)
        self.battleMusic.stop()        

    def delete(self):
        """ delete()
        """
        DistributedBattleBase.DistributedBattleBase.delete(self)
        del self.battleMusic

    def buildJoinPointList(self, avPos, destPos, toon=0):
        """ buildJoinPointList(avPos, destPos, toon)

        This function is called when suits or toons ask to join the
        battle and need to figure out how to walk to their selected
        pending point (destPos).  It builds a list of points the
        avatar should walk through in order to get there.  If the list
        is empty, the avatar will walk straight there.
        """
        # For building battles, suits and toons are already set up to
        # walk pretty much straight to their join spot.  Always return
        # an empty list here.
        return []

    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### Off state #####

    ##### FaceOff state #####

    def __faceOff(self, ts, name, callback):
        if (len(self.suits) == 0):
            self.notify.warning('__faceOff(): no suits.')
            return
        if (len(self.toons) == 0):
            self.notify.warning('__faceOff(): no toons.')
            return

        # Do the suits faceoff
        # TODO: get the actual position of the elevator door
        elevatorPos = self.toons[0].getPos()

        if (len(self.suits) == 1):
            leaderIndex = 0
        else:
            if (self.bossBattle == 1):
                leaderIndex = 1 # __genSuitInfos ensures that multi-suit boss battles will have boss in index 1 (a middle position)
            else:
                # otherwise __genSuitInfos ensures nothing, so pick the suit with the highest type to be the leader
                maxTypeNum = -1
                for suit in self.suits:
                    suitTypeNum = SuitDNA.getSuitType(suit.dna.name)
                    if (maxTypeNum < suitTypeNum):
                        maxTypeNum = suitTypeNum
                        leaderIndex = self.suits.index(suit)

        delay = FACEOFF_TAUNT_T
        suitTrack = Parallel()
        suitLeader = None

        for suit in self.suits:
            suit.setState('Battle')
            suitIsLeader = 0
            oneSuitTrack = Sequence()
            # Suits stop what they're doing and look at the toons
            oneSuitTrack.append(Func(suit.loop, 'neutral'))
            oneSuitTrack.append(Func(suit.headsUp, elevatorPos))

            # Only the suit leader taunts the toons
            if (self.suits.index(suit) == leaderIndex):
                suitLeader = suit
                suitIsLeader = 1

                # TODO: have an inside of building taunt here
                if (self.bossBattle == 1):
                    taunt = TTLocalizer.BattleBldgBossTaunt
                else:
                    taunt = SuitBattleGlobals.getFaceoffTaunt(suit.getStyleName(), suit.doId)

                oneSuitTrack.append(Func(suit.setChatAbsolute,
                                         taunt, CFSpeech | CFTimeout))

            # Move all suits into position after taunt delay
            destPos, destHpr = self.getActorPosHpr(suit, self.suits)
            oneSuitTrack.append(Wait(delay))
            if (suitIsLeader == 1):
                oneSuitTrack.append(Func(suit.clearChat))
            oneSuitTrack.append(self.createAdjustInterval(suit, destPos, destHpr))
            suitTrack.append(oneSuitTrack)


        # Do the toons faceoff 
        toonTrack = Parallel()
        for toon in self.toons:
            oneToonTrack = Sequence()
            destPos, destHpr = self.getActorPosHpr(toon, self.toons)
            oneToonTrack.append(Wait(delay))
            oneToonTrack.append(self.createAdjustInterval(
                toon, destPos, destHpr, toon=1, run=1))
            toonTrack.append(oneToonTrack)

        # Put the camera somewhere
        camTrack = Sequence()
        def setCamFov(fov):
            base.camLens.setFov(fov)
        camTrack.append(Func(camera.wrtReparentTo, suitLeader))

        camTrack.append(Func(setCamFov, self.camFOFov))

        suitHeight = suitLeader.getHeight()
        suitOffsetPnt = Point3(0, 0, suitHeight)

        # empirical hack to pick a mid-height view, left in to sortof match the old view
        MidTauntCamHeight = suitHeight*0.66
        MidTauntCamHeightLim = suitHeight-1.8
        if (MidTauntCamHeight < MidTauntCamHeightLim):
           MidTauntCamHeight = MidTauntCamHeightLim

        TauntCamY = 18
        TauntCamX = 0
        TauntCamHeight = random.choice((MidTauntCamHeight, 1, 11))

        camTrack.append(Func(camera.setPos,
                             TauntCamX, TauntCamY, TauntCamHeight))
        camTrack.append(Func(camera.lookAt, suitLeader, suitOffsetPnt))

        camTrack.append(Wait(delay))
        camPos = Point3(0, -6, 4)
        camHpr = Vec3(0, 0, 0)
        camTrack.append(Func(camera.reparentTo, base.localAvatar))
        camTrack.append(Func(setCamFov, ToontownGlobals.DefaultCameraFov))
        camTrack.append(Func(camera.setPosHpr, camPos, camHpr))

        mtrack = Parallel(suitTrack, toonTrack, camTrack)
        done = Func(callback)
        track = Sequence(mtrack, done, name = name)
        track.start(ts)
        self.storeInterval(track, name)

    def enterFaceOff(self, ts):
        assert(self.notify.debug('enterFaceOff()'))
        if (len(self.toons) > 0 and
            base.localAvatar == self.toons[0]):
            Emote.globalEmote.disableAll(self.toons[0], "dbattlebldg, enterFaceOff")
        self.delayDeleteMembers()
        self.__faceOff(ts, self.faceOffName, self.__handleFaceOffDone)
        return None

    def __handleFaceOffDone(self):
        self.notify.debug('FaceOff done')
        # Only the toon that initiated the battle needs to reply
        self.d_faceOffDone(base.localAvatar.doId)

    def exitFaceOff(self):
        self.notify.debug('exitFaceOff()')
        if (len(self.toons) > 0 and
            base.localAvatar == self.toons[0]):
            Emote.globalEmote.releaseAll(self.toons[0], "dbattlebldg exitFaceOff")
        self.clearInterval(self.faceOffName)
        self._removeMembersKeep()
        camera.wrtReparentTo(self)
        base.camLens.setFov(self.camFov)
        return None

    ##### WaitForInput state #####

    ##### PlayMovie state #####

    ##### Reward state #####

    def __playReward(self, ts, callback):
        toonTracks = Parallel()
        for toon in self.toons:
            toonTracks.append(Sequence(Func(toon.loop, 'victory'),
                                       Wait(FLOOR_REWARD_TIMEOUT),
                                       Func(toon.loop, 'neutral')))
        name = self.uniqueName('floorReward')
        track = Sequence(toonTracks,
                         Func(callback), name=name)
        camera.setPos(0, 0, 1)
        camera.setHpr(180, 10, 0)
        self.storeInterval(track, name)
        track.start(ts)

    def enterReward(self, ts):
        self.notify.debug('enterReward()')
        self.delayDeleteMembers()
        self.__playReward(ts, self.__handleFloorRewardDone)
        return None

    def __handleFloorRewardDone(self):
        return None

    def exitReward(self):
        self.notify.debug('exitReward()')
        # In case the server finished first
        self.clearInterval(self.uniqueName('floorReward'))
        self._removeMembersKeep()
        NametagGlobals.setMasterArrowsOn(1)
        for toon in self.toons:
            toon.startSmooth()
        return None

    ##### BuildingReward state #####

    def enterBuildingReward(self, ts):
        assert(self.notify.debug('enterBuildingReward()'))
        self.delayDeleteMembers()
        if (self.hasLocalToon()):
            NametagGlobals.setMasterArrowsOn(0)
        self.movie.playReward(ts, self.uniqueName('building-reward'),
                                        self.__handleBuildingRewardDone)
        return None

    def __handleBuildingRewardDone(self):
        assert(self.notify.debug('Building reward done'))
        if (self.hasLocalToon()):
            self.d_rewardDone(base.localAvatar.doId)
        self.movie.resetReward()

        # Now request our local battle object enter the Resume state,
        # which frees us from the battle.  The distributed object may
        # not enter the Resume state yet (it has to wait until all the
        # toons involved have reported back up), but there's no reason
        # we have to wait around for that.
        self.fsm.request('Resume')

    def exitBuildingReward(self):
        # In case we're observing and the server cuts us off
        # this guarantees all final animations get started and things
        # get cleaned up
        self.movie.resetReward(finish=1)
        self._removeMembersKeep()
        NametagGlobals.setMasterArrowsOn(1)
        return None

    ##### Resume state #####

    def enterResume(self, ts=0):
        assert(self.notify.debug('enterResume()'))
        if (self.hasLocalToon()):
            self.removeLocalToon()
        return None

    def exitResume(self):
        return None
