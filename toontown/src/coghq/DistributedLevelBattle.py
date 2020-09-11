from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.battle.BattleBase import *
from toontown.battle import DistributedBattle
from direct.directnotify import DirectNotifyGlobal
from toontown.toon import TTEmote
from otp.avatar import Emote
from toontown.battle import SuitBattleGlobals
import random
from toontown.suit import SuitDNA
from direct.fsm import State
from direct.fsm import ClassicFSM
from toontown.toonbase import ToontownGlobals

class DistributedLevelBattle(DistributedBattle.DistributedBattle):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedLevelBattle')

    def __init__(self, cr):
        """
        cr is a ClientRepository.
        """
        DistributedBattle.DistributedBattle.__init__(self,cr)
        self.levelRequest = None
        self.levelBattle = 1

    def setLevelDoId(self, levelDoId):
        self.levelDoId = levelDoId

    def setBattleCellId(self, battleCellId):
        self.battleCellId = battleCellId

        # This method is only called when the level is generated; it
        # is one of the required fields.  It immediately follows
        # setLevelDoId in the toon.dc file, so we should have
        # already gotten the levelDoId specified.

        # Hopefully, the actual level object already exists, so we
        # can set up our position and orientation immediately.  It is
        # important that we set up the battle position before we get
        # the call to setMembers, which will be coming momentarily.
        
        def doPlacement(levelList, self=self):
            self.levelRequest = None
            self.level = levelList[0]
            spec = self.level.getBattleCellSpec(self.battleCellId)
            self.level.requestReparent(self, spec['parentEntId'])
            self.setPos(spec['pos'])
            print "spec = %s" % (spec)
            print "h = %s" % (spec.get('h'))
            # Battles really want to be parented to render.
            self.wrtReparentTo(render)

        level = base.cr.doId2do.get(self.levelDoId)
        if level is None:
            self.notify.warning('level %s not in doId2do yet, battle %s will be mispositioned.' %
                                self.levelDoId, self.doId)
            self.levelRequest = self.cr.relatedObjectMgr.requestObjects(
                [self.levelDoId], doPlacement)

        else:
            # We already have the level, great.
            doPlacement([level])


    def setPosition(self, *args):
        # The level battle doesn't try to position itself according
        # to the AI's instructions; it has already positioned itself
        # from the level spec, above.
        pass

    def setInitialSuitPos(self, x, y, z):
        """ setInitialSuitPos(x, y, z)
        """
        self.initialSuitPos = Point3(x, y, z)

        # The level battle doesn't try to rotate itself according to
        # the initial suit pos; it has already rotated itself from the
        # level spec, above.

    def disable(self):
        # make sure we unlock the visibility
        if self.hasLocalToon():
            self.unlockLevelViz()
        if self.levelRequest is not None:
            self.cr.relatedObjectMgr.abortRequest(self.levelRequest)
            self.levelRequest = None
        DistributedBattle.DistributedBattle.disable(self)

    def delete(self):
        self.ignoreAll()
        DistributedBattle.DistributedBattle.delete(self)

    def handleBattleBlockerCollision(self):
        # send an event so it looks like we bumped into the battle
        # collision sphere
        messenger.send(self.getCollisionName(), [None])

    def lockLevelViz(self):
        level = base.cr.doId2do.get(self.levelDoId)
        if level:
            level.lockVisibility(zoneId=self.zoneId)
        else:
            self.notify.warning("lockLevelViz: couldn't find level %s" %
                                self.levelDoId)

    def unlockLevelViz(self):
        level = base.cr.doId2do.get(self.levelDoId)
        if level:
            level.unlockVisibility()
        else:
            self.notify.warning("unlockLevelViz: couldn't find level %s" %
                                self.levelDoId)

    def onWaitingForJoin(self):
        # localToon just collided with the battle and has requested
        # to join. lock down the visibility
        self.lockLevelViz()

    ##### FaceOff state #####

    def __faceOff(self, ts, name, callback):
        if (len(self.suits) == 0):
            self.notify.warning('__faceOff(): no suits.')
            return
        if (len(self.toons) == 0):
            self.notify.warning('__faceOff(): no toons.')
            return

        toon = self.toons[0]
        point = self.toonPoints[0][0]
        toonPos = point[0]
        toonHpr = VBase3(point[1], 0.0, 0.0)

        p = toon.getPos(self)
        toon.setPos(self, p[0], p[1], 0.0)
        toon.setShadowHeight(0)

        if (len(self.suits) == 1):
            # TODO: it looks like we only have the suit that we bumped
            # into at this point; he may or may not be the boss.
            # Need to add other suits before battle generate on AI
            leaderIndex = 0
        else:
            if (self.bossBattle == 1):
                for suit in self.suits:
                    if suit.boss:
                        leaderIndex = self.suits.index(suit)
                        break
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
            oneSuitTrack.append(Func(suit.headsUp, toonPos))

            # Only the suit leader taunts the toons
            if (self.suits.index(suit) == leaderIndex):
                suitLeader = suit
                suitIsLeader = 1

                # TODO: have an inside of building taunt here
                if (self.bossBattle == 1) and self.levelDoId in base.cr.doId2do:
                    level = base.cr.doId2do[self.levelDoId]
                    if suit.boss:
                        taunt = level.getBossTaunt()
                    else:
                        taunt = level.getBossBattleTaunt()
                else:
                    taunt = SuitBattleGlobals.getFaceoffTaunt(
                        suit.getStyleName(), suit.doId)

                oneSuitTrack.append(Func(suit.setChatAbsolute,
                                         taunt, CFSpeech | CFTimeout))

            # Move all suits into position after taunt delay
            destPos, destHpr = self.getActorPosHpr(suit, self.suits)
            oneSuitTrack.append(Wait(delay))
            if (suitIsLeader == 1):
                oneSuitTrack.append(Func(suit.clearChat))
            oneSuitTrack.append(self.createAdjustInterval(suit, destPos, destHpr))
            suitTrack.append(oneSuitTrack)

        suitHeight = suitLeader.getHeight()
        suitOffsetPnt = Point3(0, 0, suitHeight)

        # Do the toons faceoff 
        toonTrack = Parallel()
        for toon in self.toons:
            oneToonTrack = Sequence()
            destPos, destHpr = self.getActorPosHpr(toon, self.toons)
            oneToonTrack.append(Wait(delay))
            oneToonTrack.append(self.createAdjustInterval(
                toon, destPos, destHpr, toon=1, run=1))
            toonTrack.append(oneToonTrack)

        if (self.hasLocalToon()):
            # empirical hack to pick a mid-height view, left in to sortof match the old view
            MidTauntCamHeight = suitHeight*0.66
            MidTauntCamHeightLim = suitHeight-1.8
            if(MidTauntCamHeight < MidTauntCamHeightLim):
               MidTauntCamHeight = MidTauntCamHeightLim
            TauntCamY = 18
            TauntCamX = 0
            TauntCamHeight = random.choice((MidTauntCamHeight,1,11))

            # Put the camera somewhere
            camTrack = Sequence()
            camTrack.append(Func(camera.reparentTo, suitLeader))
            camTrack.append(Func(base.camLens.setFov, self.camFOFov))
            camTrack.append(Func(camera.setPos, TauntCamX, TauntCamY, TauntCamHeight))
            camTrack.append(Func(camera.lookAt, suitLeader, suitOffsetPnt))
            camTrack.append(Wait(delay))
            camTrack.append(Func(base.camLens.setFov, self.camFov))
            camTrack.append(Func(camera.wrtReparentTo, self))
            camTrack.append(Func(camera.setPos, self.camFOPos))
            camTrack.append(Func(camera.lookAt, suit))

        mtrack = Parallel(suitTrack, toonTrack)

        if (self.hasLocalToon()):
            # No arrows - they just get in the way
            NametagGlobals.setMasterArrowsOn(0)
            mtrack = Parallel(mtrack, camTrack)

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

    def __handleFaceOffDone(self):
        self.notify.debug('FaceOff done')
        # Only the toon that initiated the battle needs to reply
        self.d_faceOffDone(base.localAvatar.doId)

    def exitFaceOff(self):
        self.notify.debug('exitFaceOff()')
        if (len(self.toons) > 0 and base.localAvatar == self.toons[0]):
            Emote.globalEmote.releaseAll(self.toons[0], "dbattlebldg exitFaceOff")
        self.clearInterval(self.faceOffName)
        self._removeMembersKeep()

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
        self.notify.info('enterReward()')
        self.disableCollision()
        self.delayDeleteMembers()
        self.__playReward(ts, self.__handleFloorRewardDone)

    def __handleFloorRewardDone(self):
        return

    def exitReward(self):
        self.notify.info('exitReward()')
        # In case the server finished first
        self.clearInterval(self.uniqueName('floorReward'))
        self._removeMembersKeep()
        NametagGlobals.setMasterArrowsOn(1)
        for toon in self.toons:
            toon.startSmooth()
