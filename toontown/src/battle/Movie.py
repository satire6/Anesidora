from toontown.toonbase.ToontownBattleGlobals import *
from BattleBase import *
from direct.interval.IntervalGlobal import *

from direct.showbase import DirectObject
import MovieFire
import MovieSOS
import MovieNPCSOS
import MoviePetSOS
import MovieHeal
import MovieTrap
import MovieLure
import MovieSound
import MovieThrow
import MovieSquirt
import MovieDrop
import MovieSuitAttacks
import MovieToonVictory
import PlayByPlayText
import BattleParticles
from toontown.distributed import DelayDelete
import BattleExperience
from SuitBattleGlobals import *

from direct.directnotify import DirectNotifyGlobal
import RewardPanel
import random
import MovieUtil
from toontown.toon import Toon
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog
import copy
from toontown.toonbase import TTLocalizer
from toontown.toon import NPCToons

camPos = Point3(14, 0, 10)
camHpr = Vec3(89, -30, 0)

randomBattleTimestamp = base.config.GetBool('random-battle-timestamp', 0)

class Movie(DirectObject.DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('Movie')

    def __init__(self, battle):
        self.battle = battle
        self.track = None
        self.rewardPanel = None
        self.playByPlayText = PlayByPlayText.PlayByPlayText()
        self.playByPlayText.hide()
        self.renderProps = []

        self.hasBeenReset = 0
        self.reset()
        self.rewardHasBeenReset = 0
        self.resetReward()

    def cleanup(self):
        self.reset()
        self.resetReward()
        self.battle = None
        if (self.playByPlayText != None):
            self.playByPlayText.cleanup()
        self.playByPlayText = None
        if (self.rewardPanel != None):
            self.rewardPanel.cleanup()
        self.rewardPanel = None

    def needRestoreColor(self):
        self.restoreColor = 1

    def clearRestoreColor(self):
        self.restoreColor = 0

    def needRestoreHips(self):
        self.restoreHips = 1

    def clearRestoreHips(self):
        self.restoreHips = 0

    def needRestoreHeadScale(self):
        self.restoreHeadScale = 1
        
    def clearRestoreHeadScale(self):
        self.restoreHeadScale = 0
        
    def needRestoreToonScale(self):
        self.restoreToonScale = 1
        
    def clearRestoreToonScale(self):
        self.restoreToonScale = 0
        
    def needRestoreParticleEffect(self, effect):
        self.specialParticleEffects.append(effect)

    def clearRestoreParticleEffect(self, effect):
        if (self.specialParticleEffects.count(effect) > 0):
            self.specialParticleEffects.remove(effect)

    def needRestoreRenderProp(self, prop):
        self.renderProps.append(prop)

    def clearRenderProp(self, prop):
        if (self.renderProps.count(prop) > 0):
            self.renderProps.remove(prop)

    def restore(self):
        """
        This method should be called when the movie
        needs to be terminated early and we need to restore any
        toons to the state that they would be in if the movie
        had continued
        """
        # Speculation: all this work is no longer needed now that
        # interval.finish() guarantees completion.
        return
    
        assert(self.notify.debug('restore()'))
        for toon in self.battle.activeToons:
            # Undo any change in animation
            toon.loop('neutral')

            # Undo any change in position
            origPos, origHpr = self.battle.getActorPosHpr(toon)
            toon.setPosHpr(self.battle, origPos, origHpr)

            # Remove any props from the toon's hands
            hands = toon.getRightHands()[:]
            hands += toon.getLeftHands()
            for hand in hands:
                props = hand.getChildren()
                for prop in props:
                    # Don't remove the sticker book!
                    if (prop.getName() != 'book'):
                        MovieUtil.removeProp(prop)

            # Undo FillWithLead, HotAir, Fired, Withdrawal, RubOut,
            # FountainPen
            if (self.restoreColor == 1):
                assert(self.notify.debug('restore color for toon: %d' % \
                        toon.doId))
                headParts = toon.getHeadParts()
                torsoParts = toon.getTorsoParts()
                legsParts = toon.getLegsParts()
                partsList = [headParts, torsoParts, legsParts]
                for parts in partsList:
                    for partNum in range(0, parts.getNumPaths()):
                        nextPart = parts.getPath(partNum)
                        nextPart.clearColorScale()
                        nextPart.clearTransparency()

            # Undo RedTape
            if (self.restoreHips == 1):
                assert(self.notify.debug('restore hips for toon: %d' % \
                        toon.doId))
                parts = toon.getHipsParts()
                for partNum in range(0, parts.getNumPaths()):
                    nextPart = parts.getPath(partNum)
                    props = nextPart.getChildren()
                    for prop in props:
                        if (prop.getName() == 'redtape-tube.egg'):
                            MovieUtil.removeProp(prop)

            # Unshrink HeadShrink
            if (self.restoreHeadScale == 1):
                assert(self.notify.debug('restore head scale for toon: %d' % \
                        toon.doId))
                
                headScale = ToontownGlobals.toonHeadScales[toon.style.getAnimal()]
                for lod in toon.getLODNames():
                    toon.getPart('head', lod).setScale(headScale)
                    
            # Unshrink Downsize, restore toon back to proportion (1)
            if (self.restoreToonScale == 1):
                assert(self.notify.debug('restore toon scale for toon: %d' % \
                        toon.doId))
                toon.setScale(1)

            # In case the toon's head or arm parts have been altered, as with ReOrg,
            # we restore those values

            # Undo ReOrg of head parts, restore toon head parts back to correct places
            assert(self.notify.debug('restore toon head parts for toon: %d' % toon.doId))

            # Restore the position and hpr of the parts of the head, which
            # were originally pos = 0, 0, 0 and hpr = -18.435, 0, 0
            headParts = toon.getHeadParts()
            for partNum in range(0, headParts.getNumPaths()):
                part = headParts.getPath(partNum)
                part.setHpr(0, 0, 0)#, startHpr = part.getHpr())
                part.setPos(0, 0, 0)

            assert(self.notify.debug('restore toon arm parts for toon: %d' % toon.doId))
            
            # Now restore the hpr on the arm, sleeve, and hand parts,
            # which were all originally hpr = 0, 0, 0
            arms = toon.findAllMatches('**/arms')
            sleeves = toon.findAllMatches('**/sleeves')
            hands = toon.findAllMatches('**/hands')
            for partNum in range(0, arms.getNumPaths()):
                armPart = arms.getPath(partNum)
                sleevePart = sleeves.getPath(partNum)
                handsPart = hands.getPath(partNum)
                armPart.setHpr(0, 0, 0)
                sleevePart.setHpr(0, 0, 0)
                handsPart.setHpr(0, 0, 0)
                                    

        for suit in self.battle.activeSuits:
            # Kludgey hack around mystery crash. Why are we cleaning up
            # suits in this case anyway?
            if suit._Actor__animControlDict != None:
                # Undo any change in animation
                suit.loop('neutral')
                # A trap prop is no longer fresh
                suit.battleTrapIsFresh = 0

                # Undo any change in position
                origPos, origHpr = self.battle.getActorPosHpr(suit)
                suit.setPosHpr(self.battle, origPos, origHpr)

                # Remove any props from the suit's hands
                hands = [suit.getRightHand(), suit.getLeftHand()]
                for hand in hands:
                    props = hand.getChildren()
                    for prop in props:
                        MovieUtil.removeProp(prop) 

        # Clean up any special particle effects
        # RazzleDazzle, Rolodex
        for effect in self.specialParticleEffects:
            if (effect != None):
                assert(self.notify.debug('restore particle effect: %s' % \
                        effect.getName()))
                effect.cleanup() 
        self.specialParticleEffects = []

        # Remove any props that are parented to render
        for prop in self.renderProps:
            MovieUtil.removeProp(prop)
        self.renderProps = []

    def _deleteTrack(self):
        if self.track:
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None

    def reset(self, finish=0):
        if (self.hasBeenReset == 1):
            assert(self.notify.debug('reset() - movie was previously reset'))
            return
        self.hasBeenReset = 1
        self.stop()
        self._deleteTrack()
        if (finish == 1):
            self.restore()
        self.toonAttackDicts = []
        self.suitAttackDicts = []
        self.restoreColor = 0
        self.restoreHips = 0
        self.restoreHeadScale = 0
        self.restoreToonScale = 0
        self.specialParticleEffects = []
        for prop in self.renderProps:
            MovieUtil.removeProp(prop)
        self.renderProps = []

    def resetReward(self, finish=0):
        if (self.rewardHasBeenReset == 1):
            assert(self.notify.debug(
                'resetReward() - movie was previously reset'))
            return
        self.rewardHasBeenReset = 1

        self.stop()
        self._deleteTrack()
        if (finish == 1):
            self.restore()
        self.toonRewardDicts = []
        if (self.rewardPanel != None):
            self.rewardPanel.destroy()
        self.rewardPanel = None

    def play(self, ts, callback):
        """ play(ts)
            Play the toon and suit attacks and responses in order of
            increasing entertainment value
        """
        self.hasBeenReset = 0
        ptrack = Sequence()
        camtrack = Sequence()

        # Decide which side of the battle the camera should film from during this
        # series of attacks
        if (random.random() > 0.5):
            MovieUtil.shotDirection = 'left'
        else:
            MovieUtil.shotDirection = 'right'

        # Make sure that any traps on suits are not regarded as freshly thrown in this round
        for s in self.battle.activeSuits:
            s.battleTrapIsFresh = 0
            
        (tattacks, tcam) = self.__doToonAttacks()
        if (tattacks):
            ptrack.append(tattacks)
            camtrack.append(tcam)
        (sattacks, scam) = self.__doSuitAttacks()
        if (sattacks):
            ptrack.append(sattacks)
            camtrack.append(scam)
        ptrack.append(Func(callback))
        self._deleteTrack()
        self.track = Sequence(ptrack, name='movie-track-%d' % self.battle.doId)
        if (self.battle.localToonPendingOrActive()):
            self.track = Parallel(self.track,
                                  Sequence(camtrack),
                                  name='movie-track-with-cam-%d' % self.battle.doId)

        if (randomBattleTimestamp == 1):
            randNum = random.randint(0, 99)
            dur = self.track.getDuration()
            ts = (float(randNum)/100.0) * dur
            assert(self.notify.debug('play() - random timestamp: %f' % ts))

        # Store a DelayDelete object within the track for each
        # distributed object in the battle, so the track can execute
        # without running into grief.
        self.track.delayDeletes = []
        for suit in self.battle.suits:
            self.track.delayDeletes.append(DelayDelete.DelayDelete(suit, 'Movie.play'))
        for toon in self.battle.toons:
            self.track.delayDeletes.append(DelayDelete.DelayDelete(toon, 'Movie.play'))
        
        self.track.start(ts)
        return None
        
        
    def finish(self):
        """ finish()
            End the battle movie before it's done playing
        """
        self.track.finish()
        return None
        

    def playReward(self, ts, name, callback):
        self.rewardHasBeenReset = 0
        ptrack = Sequence()
        camtrack = Sequence()
        self.rewardPanel = RewardPanel.RewardPanel(name)
        self.rewardPanel.hide()

        (victory, camVictory) = MovieToonVictory.doToonVictory(
                                self.battle.localToonActive(),
                                self.battle.activeToons,
                                self.toonRewardIds,
                                self.toonRewardDicts,
                                self.deathList,
                                self.rewardPanel,
                                1,
                                self.uberList,
                                self.helpfulToonsList)
        if (victory):
            ptrack.append(victory)
            camtrack.append(camVictory)
        ptrack.append(Func(callback))
        self._deleteTrack()
        self.track = Sequence(ptrack,
                              name='movie-reward-track-%d' % self.battle.doId)
        if (self.battle.localToonActive()):
            self.track = Parallel(self.track,
                                  camtrack,
                                  name = 'movie-reward-track-with-cam-%d' % self.battle.doId)
        self.track.delayDeletes = []
        for t in self.battle.activeToons:
            self.track.delayDeletes.append(DelayDelete.DelayDelete(t, 'Movie.playReward'))
        self.track.start(ts)
        return None

    def playTutorialReward(self, ts, name, callback):
        """
        A special function for playing the tutorial reward movie after the
        tutorial battle.
        """
        # import pdb; pdb.set_trace()
        self.rewardHasBeenReset = 0
        self.rewardPanel = RewardPanel.RewardPanel(name)
        self.rewardCallback = callback
        # Generate quest progress intervals
        # These aren't needed until playTutorialReward_3 but we will generate them here
        # before the avatar's quest list is updated.  If we wait until playTutorialReward_3
        # then getQuestIntervalList will return an empty list because base.localAvatar.quests
        # will have already been updated and the number of earned cogs will compute to be zero
        self.questList = self.rewardPanel.getQuestIntervalList(
            base.localAvatar,
            # Flunky, Level 1, first toon was involved, not a skelecog
            [0, 1, 1, 0],
            [base.localAvatar],
            base.localAvatar.quests[0],
            [],
            [base.localAvatar.getDoId()])


        # Position the camera
        camera.setPosHpr(0, 8, base.localAvatar.getHeight() * 0.66,
                         179, 15, 0)
        # Start phase one of the movie
        self.playTutorialReward_1()

    def playTutorialReward_1(self):
        # Create a dialog box
        self.tutRewardDialog_1 = TTDialog.TTDialog(
            text = TTLocalizer.MovieTutorialReward1,
            command = self.playTutorialReward_2,
            style = TTDialog.Acknowledge,
            fadeScreen = None,
            pos = (0.65, 0, 0.5),
            scale = 0.8,
            )
        self.tutRewardDialog_1.hide()
        # play the first movie.
        self._deleteTrack()
        self.track = Sequence(name='tutorial-reward-1')
        self.track.append(Func(self.rewardPanel.initGagFrame,
                          base.localAvatar,
                          [0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0]))
        self.track += self.rewardPanel.getTrackIntervalList(base.localAvatar, THROW_TRACK, 0, 1, 0)
        self.track.append(Func(self.tutRewardDialog_1.show))
        self.track.start()
        return

    def playTutorialReward_2(self, value):
        self.tutRewardDialog_1.cleanup()

        # Create a dialog box
        self.tutRewardDialog_2 = TTDialog.TTDialog(
            text = TTLocalizer.MovieTutorialReward2,
            command = self.playTutorialReward_3,
            style = TTDialog.Acknowledge,
            fadeScreen = None,
            pos = (0.65, 0, 0.5),
            scale = 0.8,
            )
        self.tutRewardDialog_2.hide()
        # play the second movie.
        self._deleteTrack()
        self.track = Sequence(name='tutorial-reward-2')
        self.track.append(Wait(1.0))
        self.track += self.rewardPanel.getTrackIntervalList(base.localAvatar, SQUIRT_TRACK, 0, 1, 0)
        self.track.append(Func(self.tutRewardDialog_2.show))
        self.track.start()
        return

    def playTutorialReward_3(self, value):
        self.tutRewardDialog_2.cleanup()
        from toontown.toon import Toon
        from toontown.toon import ToonDNA
        def doneChat1(page, elapsed = 0):
            self.track2.start()
        def doneChat2(elapsed):
            self.track2.pause()
            self.track3.start()
        def uniqueName(hook):
            return "TutorialTom-" + hook
        self.tutorialTom = Toon.Toon()
        dna = ToonDNA.ToonDNA()
        dnaList = ("dll" ,"ms" ,"m" ,"m" ,7 ,0 ,7 ,7 ,2 ,6 ,2 ,6 ,2 ,16)
        dna.newToonFromProperties(*dnaList)
        self.tutorialTom.setDNA(dna)
        self.tutorialTom.setName(TTLocalizer.NPCToonNames[20000])
        self.tutorialTom.uniqueName = uniqueName

        if base.config.GetString("language", "english") == "japanese":
            self.tomDialogue03 = base.loadSfx("phase_3.5/audio/dial/CC_tom_movie_tutorial_reward01.mp3")
            self.tomDialogue04 = base.loadSfx("phase_3.5/audio/dial/CC_tom_movie_tutorial_reward02.mp3")
            self.tomDialogue05 = base.loadSfx("phase_3.5/audio/dial/CC_tom_movie_tutorial_reward03.mp3")
            self.musicVolume = base.config.GetFloat(
                "tutorial-music-volume", 0.5)
        else:
            self.tomDialogue03 = None
            self.tomDialogue04 = None
            self.tomDialogue05 = None
            self.musicVolume = 0.9

        # Need to lower battle music during dialogue
        music = base.cr.playGame.place.loader.battleMusic
        
        # import pdb; pdb.set_trace()

        # Quest list is generated in playTutorialReward before the avatar's quest description
        # is updated to reflect defeating the flunky
        if self.questList:
            self.track1 = Sequence(
                Wait(1.0),
                Func(self.rewardPanel.initQuestFrame,
                     base.localAvatar,
                     copy.deepcopy(base.localAvatar.quests)),
                Wait(1.0),
                Sequence(*self.questList),
                Wait(1.0),
                Func(self.rewardPanel.hide),
                Func(camera.setPosHpr, render,
                     34, 19.88, 3.48, -90, -2.36, 0),
                Func(base.localAvatar.animFSM.request, "neutral"),
                Func(base.localAvatar.setPosHpr,
                     40.31, 22.00, -0.47, 150.00, 360.00, 0.00),
                Wait(0.5),
                Func(self.tutorialTom.reparentTo, render),
                Func(self.tutorialTom.show),
                Func(self.tutorialTom.setPosHpr,
                     40.29, 17.9, -0.47, 11.31, 0.00, 0.07),
                Func(self.tutorialTom.animFSM.request,'TeleportIn'),
                Wait(1.5169999999999999),
                Func(self.tutorialTom.animFSM.request, 'neutral'),
                Func(self.acceptOnce,
                     self.tutorialTom.uniqueName("doneChatPage"),
                     doneChat1),
                Func(self.tutorialTom.addActive),
                Func(music.setVolume, self.musicVolume),
                Func(self.tutorialTom.setLocalPageChat,
                     TTLocalizer.MovieTutorialReward3, 0, None,
                     [self.tomDialogue03]),
                name='tutorial-reward-3a')
            self.track2 = Sequence(
                Func(self.acceptOnce,
                     self.tutorialTom.uniqueName("doneChatPage"),
                     doneChat2),
                Func(self.tutorialTom.setLocalPageChat,
                     TTLocalizer.MovieTutorialReward4, 1, None,
                     [self.tomDialogue04]),
                Func(self.tutorialTom.setPlayRate, 1.5, "right-hand-start"),
                Func(self.tutorialTom.play,"right-hand-start"),
                Wait(self.tutorialTom.getDuration("right-hand-start")/1.5),
                Func(self.tutorialTom.loop,"right-hand"),
                name='tutorial-reward-3b')
            self.track3 = Parallel(
                Sequence(
                Func(self.tutorialTom.setPlayRate, -1.8,
                     "right-hand-start"),
                Func(self.tutorialTom.play,"right-hand-start"),
                Wait(self.tutorialTom.getDuration("right-hand-start")/1.8),
                Func(self.tutorialTom.animFSM.request,'neutral'),
                name='tutorial-reward-3ca'
                ),
                Sequence(
                Wait(0.5),
                Func(self.tutorialTom.setChatAbsolute, TTLocalizer.MovieTutorialReward5,
                     CFSpeech | CFTimeout, self.tomDialogue05),
                Wait(1.0),
                Func(self.tutorialTom.animFSM.request,'TeleportOut'),
                Wait(self.tutorialTom.getDuration("teleport")),
                Wait(1.0),
                Func(self.playTutorialReward_4, 0),
                name='tutorial-reward-3cb'                
                ),
                name='tutorial-reward-3c')
                
            self.track1.start()
        else:
            self.playTutorialReward_4(0)
        return

    def playTutorialReward_4(self, value):
        # Point toon at toon headquarters
        base.localAvatar.setH(270)
        self.tutorialTom.removeActive()
        self.tutorialTom.delete()
        self.questList = None
        self.rewardCallback()
        return
        
    def stop(self):
        """ stop()
        """
        if (self.track):
            self.track.finish()
            self._deleteTrack()
        # These next two are probably not needed.
        if (self.rewardPanel):
            self.rewardPanel.hide()
        if (self.playByPlayText):
            self.playByPlayText.hide()

    def __doToonAttacks(self):
        """ __doToonAttacks()
            Create a track of all toon attacks in the proper order
        """
        assert(self.notify.debug("doToonAttacks"))
        if base.config.GetBool("want-toon-attack-anims", 1):
            track = Sequence(name='toon-attacks')
            camTrack = Sequence(name='toon-attacks-cam')
            
            (ival, camIval) = MovieFire.doFires(self.__findToonAttack(FIRE))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
                
            (ival, camIval) = MovieSOS.doSOSs(self.__findToonAttack(SOS))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            (ival, camIval) = MovieNPCSOS.doNPCSOSs(self.__findToonAttack(NPCSOS))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            (ival, camIval) = MoviePetSOS.doPetSOSs(self.__findToonAttack(PETSOS))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            hasHealBonus = self.battle.getInteractivePropTrackBonus() == HEAL
            (ival, camIval) = MovieHeal.doHeals(self.__findToonAttack(HEAL), hasHealBonus)
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            (ival, camIval) = MovieTrap.doTraps(self.__findToonAttack(TRAP))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            (ival, camIval) = MovieLure.doLures(self.__findToonAttack(LURE))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            (ival, camIval) = MovieSound.doSounds(self.__findToonAttack(SOUND))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            (ival, camIval) = MovieThrow.doThrows(self.__findToonAttack(THROW))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            (ival, camIval) = MovieSquirt.doSquirts(
                                                self.__findToonAttack(SQUIRT))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            (ival, camIval) = MovieDrop.doDrops(self.__findToonAttack(DROP))
            if (ival):
                track.append(ival)
                camTrack.append(camIval)
            if (len(track) == 0):
                return (None, None)
            else:
                return (track, camTrack)
        else:
            return (None, None)
                

    def genRewardDicts(self,
                       id0, origExp0, earnedExp0, origQuests0, items0, missedItems0,
                       origMerits0, merits0, parts0,
                       id1, origExp1, earnedExp1, origQuests1, items1, missedItems1,
                       origMerits1, merits1, parts1,
                       id2, origExp2, earnedExp2, origQuests2, items2, missedItems2,
                       origMerits2, merits2, parts2,
                       id3, origExp3, earnedExp3, origQuests3, items3, missedItems3,
                       origMerits3, merits3, parts3,
                       deathList, uberList, helpfulToonsList):
        assert(self.notify.debug("deathList: " + str(deathList)))
        self.deathList = deathList
        self.helpfulToonsList = helpfulToonsList
        entries = ((id0, origExp0, earnedExp0, origQuests0, items0, missedItems0,
                    origMerits0, merits0, parts0),
                   (id1, origExp1, earnedExp1, origQuests1, items1, missedItems1,
                    origMerits1, merits1, parts1),
                   (id2, origExp2, earnedExp2, origQuests2, items2, missedItems2,
                    origMerits2, merits2, parts2),
                   (id3, origExp3, earnedExp3, origQuests3, items3, missedItems3,
                    origMerits3, merits3, parts3))
        self.toonRewardDicts = BattleExperience.genRewardDicts(entries)
        self.toonRewardIds = [id0, id1, id2, id3]
        self.uberList = uberList
        #import pdb; pdb.set_trace()

    def genAttackDicts(self, toons, suits,
        id0, tr0, le0, tg0, hp0, ac0, hpb0, kbb0, died0, revive0,
        id1, tr1, le1, tg1, hp1, ac1, hpb1, kbb1, died1, revive1,
        id2, tr2, le2, tg2, hp2, ac2, hpb2, kbb2, died2, revive2,
        id3, tr3, le3, tg3, hp3, ac3, hpb3, kbb3, died3, revive3,
        sid0, at0, stg0, dm0, sd0, sb0, st0,
        sid1, at1, stg1, dm1, sd1, sb1, st1,
        sid2, at2, stg2, dm2, sd2, sb2, st2,
        sid3, at3, stg3, dm3, sd3, sb3, st3):
        """ genAttackDicts()
        """
        assert(self.notify.debug('genAttackDicts()'))
        if (self.track and self.track.isPlaying()):
            self.notify.warning('genAttackDicts() - track is playing!')
        toonAttacks = ((id0, tr0, le0, tg0, hp0, ac0, hpb0, kbb0, died0, revive0),
                       (id1, tr1, le1, tg1, hp1, ac1, hpb1, kbb1, died1, revive1),
                       (id2, tr2, le2, tg2, hp2, ac2, hpb2, kbb2, died2, revive2),
                       (id3, tr3, le3, tg3, hp3, ac3, hpb3, kbb3, died3, revive3))
        self.__genToonAttackDicts(toons, suits, toonAttacks)
        suitAttacks = ((sid0, at0, stg0, dm0, sd0, sb0, st0),
                       (sid1, at1, stg1, dm1, sd1, sb1, st1),
                       (sid2, at2, stg2, dm2, sd2, sb2, st2),
                       (sid3, at3, stg3, dm3, sd3, sb3, st3))
        self.__genSuitAttackDicts(toons, suits, suitAttacks)

    def __genToonAttackDicts(self, toons, suits, toonAttacks):
        """ Create a list of dictionaries for the
            toon attacks, sorted by increasing level
        """
        
        assert(self.notify.debug('genToonAttackDicts() - toons: %s suits: %s toon attacks: %s' % (toons, suits, toonAttacks)))
        for ta in toonAttacks:
            targetGone = 0
            track = ta[TOON_TRACK_COL]
            if (track != NO_ATTACK):
                adict = {}
                toonIndex = ta[TOON_ID_COL]
                assert(toonIndex < len(toons))
                toonId = toons[toonIndex]
                assert(toonId != -1)
                toon = self.battle.findToon(toonId)
                if (toon == None):
                    continue
                level = ta[TOON_LVL_COL]
                adict['toon'] = toon
                adict['track'] = track
                adict['level'] = level
                hps = ta[TOON_HP_COL]
                kbbonuses = ta[TOON_KBBONUS_COL]
                # If it's an NPCSOS with a normal toon attack, do some
                # extra prep work first
                if (track == NPCSOS):
                    # This will indicate attack was NPCSOS after we change
                    # the track
                    adict['npcId'] = ta[TOON_TGT_COL] 
                    toonId = ta[TOON_TGT_COL]
                    track, npc_level, npc_hp = NPCToons.getNPCTrackLevelHp(adict['npcId'])
                    if (track == None):
                        track = NPCSOS
                    adict['track'] = track
                    adict['level'] = npc_level
                elif (track == PETSOS):
                    petId = ta[TOON_TGT_COL]
                    adict['toonId'] = toonId
                    adict['petId'] = petId
                if (track == SOS):
                    # For an SOS, the target is a toonHandle to a friend
                    targetId = ta[TOON_TGT_COL]
                    assert(targetId != -1)
                    # We can only show the name of the toon being called
                    # to the toon calling for help and the toon being called
                    if (targetId == base.localAvatar.doId):
                        target = base.localAvatar
                        adict['targetType'] = 'callee'
                    elif (toon == base.localAvatar):
                        target = base.cr.identifyAvatar(targetId)
                        assert(target != None)
                        adict['targetType'] = 'caller'
                    else:
                        target = None
                        adict['targetType'] = 'observer'
                    adict['target'] = target
                elif (track == NPCSOS or
                      track == NPC_COGS_MISS or
                      track == NPC_TOONS_HIT or
                      track == NPC_RESTOCK_GAGS or
                      track == PETSOS):
                    adict['special'] = 1
                    toonHandles = []
                    for t in toons:
                        if (t != -1):
                            target = self.battle.findToon(t)
                            if (target == None):
                                continue
                            # NPC_TOONS_HIT is like Heal - it only works
                            # on other toons
                            if (track == NPC_TOONS_HIT and t == toonId):
                                continue
                            toonHandles.append(target)
                    adict['toons'] = toonHandles
                    suitHandles = []
                    for s in suits:
                        if (s != -1):
                            target = self.battle.findSuit(s)
                            if (target == None):
                                continue
                            suitHandles.append(target)
                    adict['suits'] = suitHandles
                    if (track == PETSOS):
                        del adict['special']
                        targets = []
                        for t in toons:
                            if (t != -1):
                                target = self.battle.findToon(t)
                                if (target == None):
                                    continue
                                tdict = {}
                                tdict['toon'] = target
                                assert(toons.index(t) < len(hps))
                                tdict['hp'] = hps[toons.index(t)]
                                self.notify.debug("PETSOS: toon: %d healed for hp: %d" % (target.doId, hps[toons.index(t)])) 
                                targets.append(tdict)
                        if (len(targets) > 0):
                            adict['target'] = targets
                elif (track == HEAL):
                    # Odd level heals affect all toons (except the caster)
                    if (levelAffectsGroup(HEAL, level)):
                        targets = []
                        for t in toons:
                            if (t != toonId and t != -1):
                                target = self.battle.findToon(t)
                                if (target == None):
                                    continue
                                tdict = {}
                                tdict['toon'] = target
                                assert(toons.index(t) < len(hps))
                                tdict['hp'] = hps[toons.index(t)]
                                self.notify.debug("HEAL: toon: %d healed for hp: %d" % (target.doId, hps[toons.index(t)])) 
                                targets.append(tdict)
                        if (len(targets) > 0):
                            adict['target'] = targets
                        else:
                            targetGone = 1
                            #import pdb; pdb.set_trace()
                    else:
                        targetIndex = ta[TOON_TGT_COL]
                        if targetIndex < 0:
                            targetGone = 1
                        else:
                            assert(targetIndex < len(toons))
                            targetId = toons[targetIndex]
                            assert(targetId != -1)
                            target = self.battle.findToon(targetId)
                            if (target != None):
                                tdict = {}
                                tdict['toon'] = target
                                assert(targetIndex < len(hps))
                                tdict['hp'] = hps[targetIndex]
                                adict['target'] = tdict
                            else:
                                targetGone = 1
                                #import pdb; pdb.set_trace()
                else:
                    # Odd level lures affect all suits
                    # Sounds affect all suits
                    # NPC drops and traps affect all suits
                    if (attackAffectsGroup(track, level, ta[TOON_TRACK_COL])):
                        targets = []
                        for s in suits:
                            if (s != -1):
                                target = self.battle.findSuit(s)
                                assert(target != None)
                                if (ta[TOON_TRACK_COL] == NPCSOS):
                                    if (track == LURE and
                                         self.battle.isSuitLured(target) == 1):
                                        continue
                                    elif (track == TRAP and
                                          (self.battle.isSuitLured(target) == 1 or
                                           target.battleTrap != NO_TRAP)):
                                        continue 
                                targetIndex = suits.index(s)
                                sdict = {}
                                sdict['suit'] = target
                                assert(targetIndex < len(hps))
                                sdict['hp'] = hps[targetIndex]
                                if (ta[TOON_TRACK_COL] == NPCSOS and
                                    track == DROP and hps[targetIndex] == 0):
                                        continue
                                sdict['kbbonus'] = kbbonuses[targetIndex]
                                sdict['died'] = ta[SUIT_DIED_COL] & \
                                                (1<<targetIndex)
                                sdict['revived'] = ta[SUIT_REVIVE_COL] & (1<<targetIndex)
                                if (sdict['died'] != 0):
                                    assert(self.notify.debug('suit: %d died' %
                                                             target.doId))
                                # leftSuits and rightSuits are used for
                                # dodging, and since only NPC drops are
                                # group drops, and NPC drops always hit,
                                # there is no need for an actual list here
                                sdict['leftSuits'] = []
                                sdict['rightSuits'] = []
                                targets.append(sdict)
                        adict['target'] = targets
                    else:
                        targetIndex = ta[TOON_TGT_COL]
                        if targetIndex < 0:
                            targetGone = 1
                        else:
                            assert(targetIndex < len(suits))
                            targetId = suits[targetIndex]
                            assert(targetId != -1)
                            target = self.battle.findSuit(targetId)
                            assert(target != None)
                            sdict = {}
                            sdict['suit'] = target
                            # MPG bandaid on crash where target is not in
                            # activeSuits for some reason
                            if (self.battle.activeSuits.count(target) == 0):
                                targetGone = 1
                                suitIndex = 0
                            else:
                                suitIndex = self.battle.activeSuits.index(target)
                            leftSuits = []
                            for si in range(0, suitIndex):
                                asuit = self.battle.activeSuits[si]
                                if (self.battle.isSuitLured(asuit) == 0):
                                    leftSuits.append(asuit)
                            lenSuits = len(self.battle.activeSuits)
                            rightSuits = []
                            if (lenSuits > (suitIndex+1)):
                                for si in range(suitIndex+1, lenSuits):
                                    asuit = self.battle.activeSuits[si]
                                    if (self.battle.isSuitLured(asuit) == 0):
                                        rightSuits.append(asuit)
                            sdict['leftSuits'] = leftSuits
                            sdict['rightSuits'] = rightSuits
                            assert(targetIndex < len(hps))
                            sdict['hp'] = hps[targetIndex]
                            sdict['kbbonus'] = kbbonuses[targetIndex]
                            sdict['died'] = ta[SUIT_DIED_COL] & (1<<targetIndex)
                            sdict['revived'] = ta[SUIT_REVIVE_COL] & (1<<targetIndex)
                            if (sdict['revived'] != 0):
                                pass
                                #import pdb; pdb.set_trace()
                            if (sdict['died'] != 0):
                                assert(self.notify.debug('suit: %d died' %
                                                         targetId))
                            # MovieDrop and MovieTrap expect a list 
                            # (because NPC drops affect groups of suits)
                            if (track == DROP or track == TRAP):
                                adict['target'] = [sdict]
                            else:
                                adict['target'] = sdict
                adict['hpbonus'] = ta[TOON_HPBONUS_COL]
                adict['sidestep'] = ta[TOON_ACCBONUS_COL]
                # NPC heals need to always succeed
                if (adict.has_key('npcId')):
                    adict['sidestep'] = 0
                adict['battle'] = self.battle
                adict['playByPlayText'] = self.playByPlayText
                if (targetGone == 0):
                    self.toonAttackDicts.append(adict)
                else:
                    self.notify.warning('genToonAttackDicts() - target gone!')

        # Sort the dictionaries by ascending toon level ([TOON_LVL_COL])
        # I think this doesnt cause a problem similar to 'cogsmack' because
        # the AI uses  BattleBase.py's findToonAttack() to also do sorting 
        # by toon level
        def compFunc(a, b):
            alevel = a['level']
            blevel = b['level']
            if (alevel > blevel):
                return 1
            elif (alevel < blevel):
                return -1
            return 0
        self.toonAttackDicts.sort(compFunc)

    def __findToonAttack(self, track):
        """ Return a list of dictionaries for the
            specified track, sorted by increasing level
        """
        assert(self.notify.debug("__findToonAttack"))
        setCapture = 0
        tp = []
        for ta in self.toonAttackDicts:
            if (ta['track'] == track or
                (track == NPCSOS and ta.has_key('special'))):
                assert self.notify.debug("tp.append(ta)")
                tp.append(ta)
                if track == SQUIRT:
                    setCapture = 1
                    #import pdb; pdb.set_trace()
                
        # Do a special sort for TRAP attacks to ensure all non-NPC
        # traps happen before NPC traps (if any)
        if (track == TRAP):
            sortedTraps = []
            for attack in tp:
                if (not attack.has_key('npcId')):
                    sortedTraps.append(attack)
            for attack in tp:
                if (attack.has_key('npcId')):
                    sortedTraps.append(attack)
            assert(len(sortedTraps) == len(tp))
            tp = sortedTraps
            
        if setCapture:
            #import pdb; pdb.set_trace()
            pass
            
        return tp

    def __genSuitAttackDicts(self, toons, suits, suitAttacks):
        """ Create a list of dictionaries for the suit attacks, sorted
            by increasing level
        """
        assert(self.notify.debug('genSuitAttackDicts() - toons: %s suits: %s suit attacks: %s' % (toons, suits, suitAttacks)))
        for sa in suitAttacks:
            targetGone = 0
            attack = sa[SUIT_ATK_COL]
            if (attack != NO_ATTACK):
                suitIndex = sa[SUIT_ID_COL]
                assert(suitIndex < len(suits))
                suitId = suits[suitIndex]
                assert(suitId != -1)
                suit = self.battle.findSuit(suitId)
                if (suit == None):
                    self.notify.error('suit: %d not in battle!' % suitId)
                adict = getSuitAttack(suit.getStyleName(), suit.getLevel(),
                                      attack)
                adict['suit'] = suit
                adict['battle'] = self.battle
                adict['playByPlayText'] = self.playByPlayText
                adict['taunt'] = sa[SUIT_TAUNT_COL]
                hps = sa[SUIT_HP_COL]
                if (adict['group'] == ATK_TGT_GROUP):
                    assert(self.notify.debug(
                        'genSuitAttackDicts() - group: %s' % toons))
                    targets = []
                    for t in toons:
                        if (t != -1):
                            target = self.battle.findToon(t)
                            if (target == None):
                                continue
                            targetIndex = toons.index(t)
                            tdict = {}
                            tdict['toon'] = target
                            assert(targetIndex < len(hps))
                            tdict['hp'] = hps[targetIndex]
                            self.notify.debug("DAMAGE: toon: %d hit for hp: %d" % (target.doId, hps[targetIndex]))
                            toonDied = sa[TOON_DIED_COL] & (1<<targetIndex)
                            tdict['died'] = toonDied
                            targets.append(tdict)
                    if (len(targets) > 0):
                        adict['target'] = targets
                    else:
                        targetGone = 1
                elif (adict['group'] == ATK_TGT_SINGLE):
                    targetIndex = sa[SUIT_TGT_COL]
                    assert(targetIndex < len(toons))
                    targetId = toons[targetIndex]
                    assert(targetId != -1)
                    target = self.battle.findToon(targetId)
                    if (target == None):
                        targetGone = 1
                        break
                    tdict = {}
                    tdict['toon'] = target
                    assert(targetIndex < len(hps))
                    tdict['hp'] = hps[targetIndex]
                    self.notify.debug("DAMAGE: toon: %d hit for hp: %d" % (target.doId, hps[targetIndex]))
                    toonDied = sa[TOON_DIED_COL] & (1<<targetIndex)
                    tdict['died'] = toonDied
                    # Grab neighboring toons for sidestepping
                    toonIndex = self.battle.activeToons.index(target)
                    rightToons = []
                    for ti in range(0, toonIndex):
                        rightToons.append(self.battle.activeToons[ti])
                    lenToons = len(self.battle.activeToons)
                    leftToons = []
                    if (lenToons > (toonIndex+1)):
                        for ti in range(toonIndex+1, lenToons):
                            leftToons.append(self.battle.activeToons[ti])
                    tdict['leftToons'] = leftToons
                    tdict['rightToons'] = rightToons
                    adict['target'] = tdict
                else:
                    self.notify.warning('got suit attack not group or single!')
                if (targetGone == 0):
                    self.suitAttackDicts.append(adict)
                else:
                    self.notify.warning('genSuitAttackDicts() - target gone!')

        """
        # this sort needs to be done by the AI or it will result
        # in a bug where multiple anims that kill a toon are played
        # in the wrong order ('cogsmack')

        # Sort the dictionaries by the level of the attacking suit
        def compFunc(a, b):
            alevel = a['suit'].getActualLevel()
            blevel = b['suit'].getActualLevel()
            if (alevel > blevel):
                return 1
            elif (alevel < blevel):
                return -1
            return 0
        self.suitAttackDicts.sort(compFunc)
        """

    def __doSuitAttacks(self):
        """ __doSuitAttacks()
            Create a track of all suit attacks
        """
        if base.config.GetBool("want-suit-anims", 1):
            track = Sequence(name = 'suit-attacks')
            camTrack = Sequence(name = 'suit-attacks-cam')
            for a in self.suitAttackDicts:
                (ival, camIval) = MovieSuitAttacks.doSuitAttack(a)
                if (ival):
                    track.append(ival)
                    camTrack.append(camIval)
            if (len(track) == 0):
                return (None, None)
            return (track, camTrack)
        else:
            return (None, None)




