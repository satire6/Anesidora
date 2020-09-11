#-------------------------------------------------------------------------------
# Contact: Rob Gordon, Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: Client-side Tug of War for a parties. This class borrowed code
#          heavily from DistributedTugOfWarGame.py
# Chagnes:
# - Nov 2009 Migrated to use DistributedPartyTeamActivity.py
#-------------------------------------------------------------------------------
import math

from pandac.PandaModules import CollisionTube
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import Point3
from pandac.PandaModules import VBase3
from pandac.PandaModules import RopeNode

from direct.interval.IntervalGlobal import LerpPosHprInterval
from direct.interval.IntervalGlobal import LerpPosInterval
from direct.interval.IntervalGlobal import Wait
from direct.interval.IntervalGlobal import ActorInterval
from direct.interval.MetaInterval import Sequence
from direct.interval.MetaInterval import Parallel
from direct.interval.FunctionInterval import Func
from direct.showutil.Rope import Rope
from direct.showbase.PythonUtil import fitDestAngle2Src
from direct.fsm.StatePush import StateVar, FunctionCall

from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.effects import Splash
from toontown.minigame.MinigamePowerMeter import MinigamePowerMeter
from toontown.minigame.ArrowKeys import ArrowKeys

import PartyGlobals
import PartyUtils
from DistributedPartyTeamActivity import DistributedPartyTeamActivity

class DistributedPartyTugOfWarActivity(DistributedPartyTeamActivity):

    notify = directNotify.newCategory("DistributedPartyTugOfWarActivity")
    
    def __init__(self, cr):
        """
        cr: instance of ClientRepository
        """
        DistributedPartyTeamActivity.__init__(
            self,
            cr,
            PartyGlobals.ActivityIds.PartyTugOfWar,
            startDelay = PartyGlobals.TugOfWarStartDelay
        )
        assert(self.notify.debug("__init__"))
        
        # these are the indices of the active buttons
        self.buttons = [0,1]
        
        # these variables are used for calculation how fast the player is pressing the keys
        self.arrowKeys = None
        self.keyTTL = []
        self.idealRate = 0.0
        self.keyRate = 0
        self.allOutMode = False
        self.rateMatchAward = 0.0 # bonus for consistently hitting the ideal rate
        
        self.toonIdsToStartPositions = {} # initial positions of toons
        self.toonIdsToIsPullingFlags = {} # whether or not a toon is pulling
        self.toonIdsToRightHands = {} # used for setting up ropes
        self.fallenToons = [] # toons in the water
        self.fallenPositions = []
        self.unusedFallenPositionsIndices = [0,1,2,3]
        self.toonIdsToAnimIntervals = {}
        self.tugRopes = []


    def generate(self):
        DistributedPartyTeamActivity.generate(self)
        assert(self.notify.debug("generate"))

        self._hopOffFinishedSV = StateVar(True)
        self._rewardFinishedSV = StateVar(True)
        self._isWalkStateReadyFC = FunctionCall(self._testWalkStateReady,
                                                self._hopOffFinishedSV, self._rewardFinishedSV)
        
    def delete(self):
        self._isWalkStateReadyFC.destroy()
        self._hopOffFinishedSV.destroy()
        self._rewardFinishedSV.destroy()

        DistributedPartyTeamActivity.delete(self)
            

    def handleToonJoined(self, toonId):
        DistributedPartyTeamActivity.handleToonJoined(self, toonId)

        self.toonIdsToAnimIntervals[toonId] = None
        
        if toonId == base.localAvatar.doId:
            base.cr.playGame.getPlace().fsm.request("activity")

            # set camera to a 3rd person view of play area
            camera.wrtReparentTo(self.root)
            self.cameraMoveIval = LerpPosHprInterval(
                camera,
                1.5,
                PartyGlobals.TugOfWarCameraPos,
                PartyGlobals.TugOfWarCameraInitialHpr,
                other=self.root,
            )
            self.cameraMoveIval.start()
            
            self.localToonPosIndex = self.getIndex(base.localAvatar.doId, self.localToonTeam)
            self.notify.debug("posIndex: %d" %self.localToonPosIndex)
            
            toon = self.getAvatar(toonId)
            targetPos = self.dockPositions[self.localToonTeam][self.localToonPosIndex]
            # prevent toons from clipping through the dock by warping them to dock height
            if toon.getZ(self.root) < PartyGlobals.TugOfWarToonPositionZ:
                toon.setZ(self.root, PartyGlobals.TugOfWarToonPositionZ)
            targetH = fitDestAngle2Src(toon.getH(self.root), PartyGlobals.TugOfWarHeadings[self.localToonTeam])
            travelVector = targetPos - toon.getPos(self.root)
            duration = travelVector.length() / 5.0
            if self.toonIdsToAnimIntervals[toonId] is not None:
                self.toonIdsToAnimIntervals[toonId].finish()
            self.toonIdsToAnimIntervals[toonId] = Sequence(
                Func( toon.startPosHprBroadcast, 0.1 ),
                Func( toon.b_setAnimState, "run" ),
                LerpPosHprInterval( toon, duration, targetPos, VBase3( targetH, 0.0, 0.0 ), other=self.root ),
                Func( toon.stopPosHprBroadcast ),
                Func( toon.b_setAnimState, "neutral" ),
            )
            self.toonIdsToAnimIntervals[toonId].start()

        
    def handleToonExited(self, toonId):
        DistributedPartyTeamActivity.handleToonExited(self, toonId)
        
        # clean up local toon stuff
        if toonId == base.localAvatar.doId:
            self.cameraMoveIval.pause()

            # make toon jump off the dock if needed
            if toonId not in self.fallenToons:
                # finish any existing interval for that toon
                if toonId in self.toonIdsToAnimIntervals and \
                   self.toonIdsToAnimIntervals[toonId] is not None:
                    self.toonIdsToAnimIntervals[toonId].finish()
                toon = self.getAvatar(toonId)
                # clamp targetHeading to minimize spin
                targetH = fitDestAngle2Src(toon.getH(self.root), 180.0)
                targetPos = self.hopOffPositions[self.getTeam(toonId)][self.getIndex(toonId, self.getTeam(toonId))]
                hopOffAnim = Sequence(
                    Func( toon.startPosHprBroadcast, 0.1 ),
                    toon.hprInterval( 0.2, VBase3( targetH, 0.0, 0.0 ), other=self.root ),
                    Func( toon.b_setAnimState, "jump", 1.0 ),
                    Wait( 0.4 ),
                    PartyUtils.arcPosInterval( 0.75, toon, targetPos, 5.0, self.root ),
                    Func( toon.stopPosHprBroadcast ),
                    # make sure toon ends up on the ground on remote clients
                    Func( toon.sendCurrentPosition ),
                    Func( self.hopOffFinished, toonId ),
                )
                self.toonIdsToAnimIntervals[toonId] = hopOffAnim
                self._hopOffFinishedSV.set(False)
                self.toonIdsToAnimIntervals[toonId].start()
            # local toons not on the dock are put back into the walk state
            else:
                self._hopOffFinishedSV.set(True)
                del self.toonIdsToAnimIntervals[toonId]
        

    def handleRewardDone(self):
        # don't call down, it puts the toon in a bad state because it interferes with
        # the 'hopOffAnim'
        self._rewardFinishedSV.set(True)

    def _testWalkStateReady(self, hoppedOff, rewardFinished):
        assert(self.notify.debug("_testWalkStateReady %d %d" % (hoppedOff, rewardFinished)))
            
        if hoppedOff and rewardFinished:
            DistributedPartyTeamActivity.handleRewardDone(self)
    
    def hopOffFinished(self, toonId):
        assert(self.notify.debug("hopOffFinished( toonId=%d )" %toonId))
        
        if hasattr(self,"toonIdsToAnimIntervals") and \
           toonId in self.toonIdsToAnimIntervals:
            del self.toonIdsToAnimIntervals[toonId] # clean up anim dictionary
            
        if toonId == base.localAvatar.doId:
            if hasattr(self._hopOffFinishedSV,'_value'):
                self._hopOffFinishedSV.set(True)


    def handleToonShifted(self, toonId):
        assert(self.notify.debug("handleToonShifted( toonId=%d )" %toonId))
        
        if toonId == base.localAvatar.doId:
            # update local toon's position on the dock if they got shifted
            self.localToonPosIndex = self.getIndex( base.localAvatar.doId, self.localToonTeam )
            if self.toonIdsToAnimIntervals[toonId] is not None:
                self.toonIdsToAnimIntervals[toonId].finish()
            toon = self.getAvatar(toonId)
            targetPos = self.dockPositions[self.localToonTeam][self.localToonPosIndex]
            self.toonIdsToAnimIntervals[toonId] = Sequence(
                Wait( 0.6 ), # give leaving toon time to jump off dock
                Func( toon.startPosHprBroadcast, 0.1 ),
                Func( toon.b_setAnimState, "run" ),
                toon.posInterval( 0.5, targetPos, other=self.root ),
                Func( toon.stopPosHprBroadcast ),
                Func( toon.b_setAnimState, "neutral" ),
            )
            self.toonIdsToAnimIntervals[toonId].start()

            
    def handleToonDisabled(self, toonId):
        """
        A toon dropped unexpectedly from the game. Handle it!
        """
        assert(self.notify.debug("handleToonDisabled( toonId:%d )" %toonId ))
        
        if self.toonIdsToAnimIntervals.has_key(toonId):
            if self.toonIdsToAnimIntervals[toonId]:
                if self.toonIdsToAnimIntervals[toonId].isPlaying():
                    self.toonIdsToAnimIntervals[toonId].finish()
            else:
                self.notify.debug("self.toonIdsToAnimIntervals[%d] is none" % toonId)

    def setToonsPlaying(self, leftTeamToonIds, rightTeamToonIds):
        """Overrides DistributedPartyActivity's setToonsPlaying"""
        DistributedPartyTeamActivity.setToonsPlaying(self, leftTeamToonIds, rightTeamToonIds)

        # update table of right hands
        self.toonIdsToRightHands.clear()
        for toonId in self.getToonIdsAsList():
            toon = self.getAvatar(toonId)
            if toon:
                self.toonIdsToRightHands[toonId] = toon.getRightHands()[0]
    
    def load(self):
        """
        Load the necessary assets
        """
        DistributedPartyTeamActivity.load(self)
        
        assert(self.notify.debug("load"))
        
        self.loadModels()
        self.loadGuiElements()
        self.loadSounds()
        self.loadIntervals()
        self.arrowKeys = ArrowKeys()
        
    
    def loadModels(self):
        # load the tug of war play area
        self.playArea = loader.loadModel("phase_13/models/parties/partyTugOfWar")
        # reparent to the party ground root
        self.playArea.reparentTo(self.root)
        
        # place the activity sign
        self.sign.reparentTo( self.playArea.find("**/TugOfWar_sign_locator") )
        
        # define initial positions, with index 0 being closest to the other team
        self.dockPositions = [
            [], # left team positions
            [], # right team positions
        ]
        for i in range(4):
            self.dockPositions[0].append(
                Point3(
                    -PartyGlobals.TugOfWarInitialToonPositionsXOffset - PartyGlobals.TugOfWarToonPositionXSeparation*i,
                    0.0,
                    PartyGlobals.TugOfWarToonPositionZ,
                )
            )
        for i in range(4):
            self.dockPositions[1].append(
                Point3(
                    PartyGlobals.TugOfWarInitialToonPositionsXOffset + PartyGlobals.TugOfWarToonPositionXSeparation*i,
                    0.0,
                    PartyGlobals.TugOfWarToonPositionZ,
                )
            )
        self.hopOffPositions = [
            [], # left team positions
            [], # right team positions
        ]
        for i in range(1,5):
            self.hopOffPositions[PartyGlobals.TeamActivityTeams.LeftTeam].append(
                self.playArea.find("**/leftTeamHopOff%d_locator" %i).getPos()
            )
            self.hopOffPositions[PartyGlobals.TeamActivityTeams.RightTeam].append(
                self.playArea.find("**/rightTeamHopOff%d_locator" %i).getPos()
            )
        
        # load positions for when toons fall into the water
        for i in range(1, 5):
            pos = self.playArea.find("**/fallenToon%d_locator" %i).getPos()
            self.fallenPositions.append(pos)
        
        # load collision that allows toons to play the game
        # create one for each dock that lets toons join a particular team
        self.joinCollision = []
        self.joinCollisionNodePaths = []
        for i in range( len( PartyGlobals.TeamActivityTeams ) ):
            collShape = CollisionTube(
                PartyGlobals.TugOfWarJoinCollisionEndPoints[0],
                PartyGlobals.TugOfWarJoinCollisionEndPoints[1],
                PartyGlobals.TugOfWarJoinCollisionRadius
            )
            collShape.setTangible(True)
            
            self.joinCollision.append( CollisionNode( "TugOfWarJoinCollision%d" %i ) )
            self.joinCollision[i].addSolid( collShape )
            tubeNp = self.playArea.attachNewNode( self.joinCollision[i] )
            tubeNp.node().setCollideMask(ToontownGlobals.WallBitmask)
            self.joinCollisionNodePaths.append( tubeNp )
            self.joinCollisionNodePaths[i].setPos( PartyGlobals.TugOfWarJoinCollisionPositions[i] )
        self.__enableCollisions()
        
        # Get the rope texture by extracting it from its model.
        ropeModel = loader.loadModel("phase_4/models/minigames/tug_of_war_rope")
        self.ropeTexture = ropeModel.findTexture("*")
        ropeModel.removeNode()
        
        # create as many ropes as we will ever need
        for i in range(PartyGlobals.TugOfWarMaximumPlayersPerTeam*2 - 1):
            rope = Rope(self.uniqueName("TugRope%d" %i))
            if rope.showRope:
                rope.ropeNode.setRenderMode(RopeNode.RMBillboard)
                rope.ropeNode.setThickness(0.2)
                rope.setTexture(self.ropeTexture)
                rope.ropeNode.setUvMode(RopeNode.UVDistance)
                rope.ropeNode.setUvDirection(1)
                rope.setTransparency(1)
                rope.setColor(0.89, 0.89, 0.6, 1.0)
                rope.reparentTo(self.root)
                rope.stash()
            self.tugRopes.append(rope)
        
        # Splash object for when toon hits the water
        self.splash = Splash.Splash(self.root)
        self.splash.setScale(2.0, 4.0, 1.0)
        pos = self.fallenPositions[0]
        self.splash.setPos(pos[0], pos[1], PartyGlobals.TugOfWarSplashZOffset)
        self.splash.hide()
        
    
    def loadGuiElements(self):
        # load gui power meter
        self.powerMeter = MinigamePowerMeter(PartyGlobals.TugOfWarPowerMeterSize)
        self.powerMeter.reparentTo(aspect2d)
        self.powerMeter.setPos(0.0, 0.0, 0.6)
        self.powerMeter.hide()
        
        # Load the arrows for button indicator
        self.arrows = [None] * 2
        for x in range(len(self.arrows)):
            self.arrows[x] = loader.loadModel('phase_3/models/props/arrow')
            self.arrows[x].reparentTo(self.powerMeter)
            self.arrows[x].setScale(.2-.4*x,.2,.2)
            self.arrows[x].setPos(.12-.24*x,0,-.26)
    
    
    def loadSounds(self):
        self.splashSound = base.loadSfx("phase_4/audio/sfx/MG_cannon_splash.mp3")
        self.whistleSound = base.loadSfx("phase_4/audio/sfx/AA_sound_whistle.mp3")
    
    
    def loadIntervals(self):
        # create an interval that updates the ideal key press rate for each stage
        self.updateIdealRateInterval = Sequence()
        # other code handles setting the initial ideal rate, so only add the
        # wait for the first state
        self.updateIdealRateInterval.append(
            Wait(PartyGlobals.TugOfWarTargetRateList[0][0]),
        )
        # for each stage after the first
        for i in range( 1, len( PartyGlobals.TugOfWarTargetRateList ) ):
            duration = PartyGlobals.TugOfWarTargetRateList[i][0]
            idealRate = PartyGlobals.TugOfWarTargetRateList[i][1]
            # set ideal speed
            self.updateIdealRateInterval.append(
                Func(self.setIdealRate, idealRate)
            )
            # add delay for stage's length or set last stage flag
            if i == (len(PartyGlobals.TugOfWarTargetRateList) - 1):
                self.updateIdealRateInterval.append(
                    Func(setattr, self, "allOutMode", True)
                )
            else:
                self.updateIdealRateInterval.append(
                    Wait(duration),
                )
        # create an interval that updates the local player's key press rate
        self.updateKeyPressRateInterval = Sequence(
            Wait(PartyGlobals.TugOfWarKeyPressUpdateRate),
            Func(self.updateKeyPressRate),
        )
        # create an interval that updates the local player's force and tells the
        # server
        self.reportToServerInterval = Sequence(
            Wait(PartyGlobals.TugOfWarKeyPressReportRate),
            Func(self.reportToServer),
        )
        
        self.setupInterval = Parallel()
        # run this even if the local toon is not playing
        self.globalSetupInterval = Sequence(
            Wait(PartyGlobals.TugOfWarReadyDuration + PartyGlobals.TugOfWarGoDuration),
            Func(self.tightenRopes),
        )
        # only run this when a local toon is playing
        self.localSetupInterval = Sequence(
            Func(self.setStatus, TTLocalizer.PartyTugOfWarReady),
            Func(self.showStatus),
            Wait(PartyGlobals.TugOfWarReadyDuration),
            Func(base.playSfx, self.whistleSound),
            Func(self.setStatus, TTLocalizer.PartyTugOfWarGo),
            Wait(PartyGlobals.TugOfWarGoDuration),
            Func(self.enableKeys),
            Func(self.hideStatus),
            Func(self.updateIdealRateInterval.start),
            Func(self.updateKeyPressRateInterval.loop),
            Func(self.reportToServerInterval.loop),
        )
        
        # interval for playing the splash sound and showing the splash visual effect
        self.splashInterval = Sequence(
            Func(base.playSfx, self.splashSound),
            Func(self.splash.play),
        )
        
    def unload(self):
        DistributedPartyTeamActivity.unload(self)
        
        self.arrowKeys.destroy()
        self.unloadIntervals()
        self.unloadModels()
        self.unloadGuiElements()
        self.unloadSounds()
        
        
        # delete variables
        if hasattr(self, "toonIds"):
            del self.toonIds
        del self.buttons
        del self.arrowKeys
        del self.keyTTL
        del self.idealRate
        del self.keyRate
        del self.allOutMode
        del self.rateMatchAward
        
        del self.toonIdsToStartPositions
        del self.toonIdsToIsPullingFlags
        del self.toonIdsToRightHands
        del self.fallenToons
        del self.fallenPositions
        del self.unusedFallenPositionsIndices
        self.toonIdsToAnimIntervals.clear()
        del self.toonIdsToAnimIntervals
        

        
    def unloadModels(self):
        self.playArea.removeNode()
        del self.playArea
        
        del self.dockPositions
        del self.hopOffPositions
        
        self.__disableCollisions()
        while len(self.joinCollision) > 0:
            collNode = self.joinCollision.pop()
            del collNode
        while len(self.joinCollisionNodePaths) > 0:
            collNodePath = self.joinCollisionNodePaths.pop()
            collNodePath.removeNode()
            del collNodePath
        
        while len(self.tugRopes) > 0:
            rope = self.tugRopes.pop()
            if rope is not None:
                rope.removeNode()
            del rope
        del self.tugRopes
        
        self.splash.destroy()
        del self.splash
    
    
    def unloadGuiElements(self):
        for arrow in self.arrows:
            if arrow is not None:
                arrow.removeNode()
                del arrow
        del self.arrows
        
        if self.powerMeter is not None:
            self.powerMeter.cleanup()
            del self.powerMeter
    
    
    def unloadSounds(self):
        del self.splashSound
        del self.whistleSound
    

    def unloadIntervals(self):
        self.updateIdealRateInterval.pause()
        del self.updateIdealRateInterval
        
        self.updateKeyPressRateInterval.pause()
        del self.updateKeyPressRateInterval
        
        self.reportToServerInterval.pause()
        del self.reportToServerInterval
        
        self.setupInterval.pause()
        del self.setupInterval
        
        self.globalSetupInterval.pause()
        del self.globalSetupInterval
        
        self.localSetupInterval.pause()
        del self.localSetupInterval
        
        self.splashInterval.pause()
        del self.splashInterval
    
    
    def __enableCollisions(self):
        assert(self.notify.debug("__enableCollisions"))
        
        for i in range( len( PartyGlobals.TeamActivityTeams ) ):
            self.accept( "enterTugOfWarJoinCollision%d" %i, getattr(self, "_join%s" % PartyGlobals.TeamActivityTeams.getString(i)))


    def __disableCollisions(self):
        assert(self.notify.debug("__disableCollisions"))
        
        for i in range( len( PartyGlobals.TeamActivityTeams ) ):
            self.ignore( "enterTugOfWarJoinCollision%d" %i )
    
    
    # FSM transition methods
    def startWaitForEnough(self):
        DistributedPartyTeamActivity.startWaitForEnough(self)

        self.__enableCollisions()
    
    
    def finishWaitForEnough(self):
        DistributedPartyTeamActivity.finishWaitForEnough(self)
        
        self.__disableCollisions()
        
        
    def startWaitToStart(self, waitStartTimestamp):
        DistributedPartyTeamActivity.startWaitToStart(self, waitStartTimestamp)
        
        self.__enableCollisions()
    
    
    def finishWaitToStart(self):
        DistributedPartyTeamActivity.finishWaitToStart(self)

        self.__disableCollisions()
        
        
    def startRules(self):
        DistributedPartyTeamActivity.startRules(self)
        
        self.setUpRopes()
        # display rules to the local toon if we have one
        if self.isLocalToonPlaying:
            self.showControls()
            
    
    def finishRules(self):
        DistributedPartyTeamActivity.finishRules(self)
         
        # check for a non-standard transition and do additional cleanup as needed
        if self.activityFSM.getCurrentOrNextState() == "WaitForEnough":
            self.hideRopes()
            self.hideControls()
        
        
    def finishWaitForServer(self):
        DistributedPartyTeamActivity.finishWaitForServer(self)
        
        # check for a non-standard transition and do additional cleanup as needed
        if self.activityFSM.getCurrentOrNextState() == "WaitForEnough":
            self.hideRopes()
            self.hideControls()
        
        
    def startActive(self):
        DistributedPartyTeamActivity.startActive(self)
        
        # reset active variables
        self.toonIdsToStartPositions.clear()
        self.toonIdsToIsPullingFlags.clear()
        
        for toonId in self.getToonIdsAsList():
            self.toonIdsToIsPullingFlags[toonId] = False
            toon = self.getAvatar(toonId)
        
            if toon:
                self.toonIdsToStartPositions[toonId] = toon.getPos(self.root)
            else:
                # what the heck do we do at this point? lets try 0,0,0 
                self.notify.warning("couldn't find toon %d assigning 0,0,0 to startPos" % toonId)
                self.toonIdsToStartPositions[toonId] = Point3(0,0,0)
                
        self.unusedFallenPositionsIndices = [0,1,2,3]
        self.setupInterval = Parallel(self.globalSetupInterval)
        
        if self.isLocalToonPlaying:
            self.keyTTL = []
            self.idealForce = 0.0
            self.keyRate = 0
            self.rateMatchAward = 0.0
            self.allOutMode = False
            self.setIdealRate(PartyGlobals.TugOfWarTargetRateList[0][1])
            self.setupInterval.append(self.localSetupInterval)
        
        self.setupInterval.start()
        
        
    def finishActive(self):
        DistributedPartyTeamActivity.finishActive(self)
         
        self.hideControls()
        self.disableKeys()
        self.setupInterval.pause()
        self.reportToServerInterval.pause()
        self.updateKeyPressRateInterval.pause()
        self.updateIdealRateInterval.pause()
        self.hideRopes()
        
        
    def startConclusion(self, losingTeam):
        DistributedPartyTeamActivity.startConclusion(self, losingTeam)
        
        if self.isLocalToonPlaying:
            self._rewardFinishedSV.set(False)
            
            if losingTeam == PartyGlobals.TeamActivityNeitherTeam:
                self.setStatus(TTLocalizer.PartyTeamActivityGameTie)
            else:
                self.setStatus(TTLocalizer.PartyTugOfWarGameEnd)
            
            self.showStatus()
            
        if losingTeam == PartyGlobals.TeamActivityNeitherTeam:
            # tie
            for toonId in self.getToonIdsAsList():
                if self.getAvatar(toonId):
                    self.getAvatar(toonId).loop("neutral")
        else:
            # winning and losing team
            for toonId in self.toonIds[losingTeam]:
                if self.getAvatar(toonId):
                    self.getAvatar(toonId).loop("neutral")
            for toonId in self.toonIds[1 - losingTeam]:
                if self.getAvatar(toonId):
                    self.getAvatar(toonId).loop("victory")
        
        for ival in self.toonIdsToAnimIntervals.values():
            if ival is not None:
                ival.finish()
    
    
    def finishConclusion(self):
        DistributedPartyTeamActivity.finishConclusion(self)
        
        self.fallenToons = []
    
    
    def getTitle(self):
        return TTLocalizer.PartyTugOfWarTitle


    def getInstructions(self):
        return TTLocalizer.TugOfWarInstructions
    
    
    def showControls(self):
        # show the power meter and arrows so player can see them while they
        # read the rules 
        for arrow in self.arrows:
            arrow.setColor(PartyGlobals.TugOfWarDisabledArrowColor)
        # set meter to first stage values
        self.powerMeter.setTarget(PartyGlobals.TugOfWarTargetRateList[0][1])
        self.powerMeter.setPower(PartyGlobals.TugOfWarTargetRateList[0][1])
        self.powerMeter.setBarColor((0.0, 1.0, 0.0, 0.5))
        self.powerMeter.clearTooSlowTooFast()
        self.powerMeter.show()
        
        
    def hideControls(self):
        self.powerMeter.hide()
    
    
    def setUpRopes(self):
        self.notify.debug("setUpRopes")
        ropeIndex = 0
        # setup rope linking the left team to the right team
        leftToonId = -1
        if self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam]:
            leftToonId = self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam][0]
        rightToonId = -1
        if self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam]:
            rightToonId = self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam][0]
        if leftToonId in self.toonIdsToRightHands and \
           rightToonId in self.toonIdsToRightHands:
            self.tugRopes[ropeIndex].setup(
                3,
                (
                    (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam][0]], (0, 0, 0)),
                    (self.root, (0.0, 0.0, 2.5)),
                    (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam][0]], (0, 0, 0)),
                ),
                [0,0,0,1,1,1],
            )
            self.tugRopes[ropeIndex].unstash()
            ropeIndex += 1
        
        # setup ropes linking toons on the left team
        if len(self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam]) > 1:
            for i in range(len(self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam]) - 1, 0, -1):
                self.notify.debug("Connecting rope between toon %d and toon %d of left team." %(i, i-1))
                self.tugRopes[ropeIndex].setup(
                    3,
                    (
                        (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam][i]], (0, 0, 0)),
                        (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam][i]], (0, 0, 0)),
                        (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam][i-1]], (0, 0, 0)),
                    ),
                    [0,0,0,1,1,1],
                )
                self.tugRopes[ropeIndex].unstash()
                ropeIndex += 1
        
        # setup ropes linking toons on the right team
        if len(self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam]) > 1:
            for i in range(len(self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam]) - 1):
                self.notify.debug("Connecting rope between toon %d and toon %d of left team." %(i, i+1))
                self.tugRopes[ropeIndex].setup(
                    3,
                    (
                        (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam][i]], (0, 0, 0)),
                        (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam][i]], (0, 0, 0)),
                        (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam][i+1]], (0, 0, 0)),
                    ),
                    [0,0,0,1,1,1],
                )
                self.tugRopes[ropeIndex].unstash()
                ropeIndex += 1
    
    
    def tightenRopes(self):
        """
        The pulling part has started. Make the rope between the teams taut.
        """
        self.notify.debug("tightenRopes")
        self.tugRopes[0].setup(
            3,
            (
                (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam][0]], (0, 0, 0)),
                (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.LeftTeam][0]], (0, 0, 0)),
                (self.toonIdsToRightHands[self.toonIds[PartyGlobals.TeamActivityTeams.RightTeam][0]], (0, 0, 0)),
            ),
            [0,0,0,1,1,1],
        )
    
    
    def hideRopes(self):
        self.notify.debug("hideRopes")
        for rope in self.tugRopes:
            rope.stash()
    
    
    def handleGameTimerExpired(self):
        assert(self.notify.debug("game timer expired"))
        
        self.disableKeys() # do not allow any more input
    
    
    def setIdealRate(self, idealRate):
        self.notify.debug("setIdealRate( %d )" %idealRate)
        self.idealRate = idealRate
        self.idealForce = self.advantage*(4 + 0.4*self.idealRate)
    
    
    def updateKeyPressRate(self):
        # decrement times to live for each key press entry in keyTTL
        for i in range(len(self.keyTTL)):
            self.keyTTL[i] -= PartyGlobals.TugOfWarKeyPressUpdateRate

        # remove all key presses that have run out of time to live
        # I think this only removes at most 1 item from the list, which is not
        # what we want, but worked for Trolley tug of war so I'm afraid to "fix" it
        for i in range(len(self.keyTTL)):
            if self.keyTTL[i] <= 0.0:
                a = self.keyTTL[0:i]
                del self.keyTTL
                self.keyTTL = a
                break

        self.keyRate = len(self.keyTTL)
        
        # if the user has matched the idealRate several times in a row, add
        # a little bit to their power
        if self.keyRate == self.idealRate or self.keyRate == self.idealRate+1:
            self.rateMatchAward += 0.3
        else:
            self.rateMatchAward = 0.0
    
    
    def reportToServer(self):
        self.currentForce = self.computeForce(self.keyRate)
        self.sendUpdate("reportKeyRateForce", [self.keyRate, self.currentForce])
        self.setSpeedGauge()
        self.setAnimState(base.localAvatar.doId, self.keyRate)

    
    def computeForce(self, keyRate):
        # return a force in the range 0-self.idealRate
        F = 0
        # if this is the last stage, make force directly proportional to keyrate
        if self.allOutMode:
            F = 0.75*keyRate
        # otherwise, make force proportional to how close you are to ideal key rate
        else:
            stdDev = 0.25*self.idealRate
            F = self.advantage * (self.rateMatchAward + 4 + 0.4*self.idealRate) * math.pow(math.e, -math.pow(keyRate - self.idealRate, 2)/(2.0*math.pow(stdDev,2)))
        return F
    
    
    def setSpeedGauge(self):
        # update the power meter to show the toon's speed and the target speed
        self.powerMeter.setPower(self.keyRate)
        self.powerMeter.setTarget(self.idealRate)

        # change the color of the power meter to indicate how well the toon is doing
        # the color should be dark if you are doing badly, and green if you are doing well
        if not self.allOutMode:
            # tell the toon if he is pulling too fast or too slow
            self.powerMeter.updateTooSlowTooFast()
            index = float(self.currentForce)/self.idealForce
            bonus = 0.0
            if index > 1.0:
                bonus = max(1.0, index - 1.0)
                index = 1.0
            color = (0, 0.75*index + 0.25*bonus, 0.75*(1 - index), 0.5)
            self.powerMeter.setBarColor(color)
        else:
            self.powerMeter.setBarColor((0.0, 1.0, 0.0, 0.5))
    
    
    def updateToonKeyRate(self, toonId, keyRate):
        # since we set the local toon's pulling animation locally, don't do it
        # here
        if toonId != base.localAvatar.doId:
            self.setAnimState(toonId, keyRate)
    
    
    def setAnimState(self, toonId, keyRate):
        if self.activityFSM.state != "Active":
            return
        toon = self.getAvatar(toonId)
        if not self.toonIdsToIsPullingFlags.has_key(toonId):
            if self.getTeam(toonId) == None:
                self.notify.warning("setAnimState called with toonId (%d) that wasn't in self.toonIds" %toonId)
                return
            else:
                self.notify.warning("setAnimState called with toonId (%d) that was in self.toonIds but not in self.toonIdsToIsPullingFlags. Adding it." %toonId)
                self.toonIdsToIsPullingFlags[toonId] = False

        if keyRate > 0 and not self.toonIdsToIsPullingFlags[toonId]:
            if toon:
                toon.loop('tug-o-war')
            else:
                self.notify.warning("toon %d is None, skipping toon.loop(tugowar)" % toonId)
            self.toonIdsToIsPullingFlags[toonId] = True
        if keyRate <= 0 and self.toonIdsToIsPullingFlags[toonId]:
            if toon:
                toon.pose('tug-o-war',3)
                toon.startLookAround()
            else:
                self.notify.warning("toon %d is None, skipping toon.startLookAround" % toonId)
            self.toonIdsToIsPullingFlags[toonId] = False

    
    def enableKeys(self):
        self.notify.debug("enableKeys")
        # Change the order of the press handlers because we are only using 2 keys    
        self.arrowKeys.setPressHandlers(
            [
                lambda : self.__pressHandler(2),
                lambda : self.__pressHandler(3),
                lambda : self.__pressHandler(1),
                lambda : self.__pressHandler(0),
            ]
        )
        self.arrowKeys.setReleaseHandlers(
            [
                lambda : self.__releaseHandler(2),
                lambda : self.__releaseHandler(3),
                lambda : self.__releaseHandler(1),
                lambda : self.__releaseHandler(0),
            ]
        )
        for arrow in self.arrows:
            arrow.setColor(PartyGlobals.TugOfWarEnabledArrowColor)

            
    def disableKeys(self):
        self.arrowKeys.setPressHandlers(self.arrowKeys.NULL_HANDLERS)
        self.arrowKeys.setReleaseHandlers(self.arrowKeys.NULL_HANDLERS)


    # callbacks for when the buttons are pressed and released
    def __pressHandler(self, index):
        if index == self.buttons[0]:
            self.arrows[index].setColor(PartyGlobals.TugOfWarHilightedArrowColor)
            self.keyTTL.insert(0, PartyGlobals.TugOfWarKeyPressTimeToLive)
            self.buttons.reverse()
    
            
    def __releaseHandler(self, index):
        if index in self.buttons:
            self.arrows[index].setColor(PartyGlobals.TugOfWarEnabledArrowColor)
            
            
    def updateToonPositions(self, offset):
        # Since the timer expires locally, we may still get a few
        # messages from the AI that were on the wire when we left
        # the play state, just ignore it
        if self.activityFSM.state != "Active":
            return
        
        # adjust the camera angle
        if self.isLocalToonPlaying:
            camera.lookAt(self.root, offset, 0.0, PartyGlobals.TugOfWarCameraLookAtHeightOffset)
        
        # this client sets the position of all toons playing
        for toonId in self.getToonIdsAsList():
            if hasattr(self,"fallenToons") and \
               toonId not in self.fallenToons:
                toon = self.getAvatar(toonId)
                if toon is not None:
                    origPos = self.toonIdsToStartPositions[toonId]
                    curPos = toon.getPos(self.root)
                    newPos = Point3(origPos[0] + offset, curPos[1], curPos[2])
                    # finish any existing animation interval
                    if self.toonIdsToAnimIntervals[toonId] != None:
                        if self.toonIdsToAnimIntervals[toonId].isPlaying():
                            self.toonIdsToAnimIntervals[toonId].finish()
                            self.checkIfFallen(toonId)

                    if toonId not in self.fallenToons:
                        self.toonIdsToAnimIntervals[toonId] = Sequence(
                            LerpPosInterval(
                                toon,
                                duration=PartyGlobals.TugOfWarKeyPressReportRate,
                                pos=newPos,
                                other=self.root,
                            ),
                            Func(self.checkIfFallen, toonId)
                        )
                        self.toonIdsToAnimIntervals[toonId].start()

    
    def checkIfFallen(self, toonId):
        # check if toon has fallen
        if hasattr(self,"fallenToons") and \
           toonId not in self.fallenToons:
            toon = self.getAvatar(toonId)
            if toon:
                curPos = toon.getPos(self.root)
                team = self.getTeam(toonId)
                if ((team == PartyGlobals.TeamActivityTeams.LeftTeam  and curPos[0] > -2.0) or
                    (team == PartyGlobals.TeamActivityTeams.RightTeam and curPos[0] <  2.0)):
                    # throw all toons from this side in the water
                    losingTeam = self.getTeam(toonId)
                    self.throwTeamInWater(losingTeam)
                    # tell AI that a team fell in the water
                    self.sendUpdate("reportFallIn", [losingTeam])


    def throwTeamInWater(self, losingTeam):
        self.notify.debug("throwTeamInWater( %s )" %PartyGlobals.TeamActivityTeams.getString(losingTeam))
        splashSet = False
        for toonId in self.toonIds[losingTeam]:
            # throw toon in water
            self.fallenToons.append(toonId)
            toon = self.getAvatar(toonId)
            # getting a a crash of popping from empty list
            #fallenPosIndex = self.unusedFallenPositionsIndices.pop(0)
            fallenPosIndex = self.toonIds[losingTeam].index(toonId)
            if (fallenPosIndex < 0) or (fallenPosIndex >= 4):
                fallenPosIndex = 0
            newPos = self.fallenPositions[fallenPosIndex]
        
            # animate the toons falling into the water
            if self.toonIdsToAnimIntervals[toonId] is not None:
                if self.toonIdsToAnimIntervals[toonId].isPlaying():
                    self.toonIdsToAnimIntervals[toonId].finish()

            # Fall into water
            if toon:
                parallel = Parallel(
                    ActorInterval(actor=toon, animName='slip-forward', duration=2.0),
                    LerpPosInterval(toon, duration=2.0, pos=newPos, other=self.root),
                    )
            else:
                self.notify.warning("toon %d is none, skipping slip-forward" % toonId)
                parallel = Parallel()
                
            # only setup splash for the first toon
            if not splashSet:
                splashSet = True
                parallel.append(self.splashInterval)

            if toon:
                self.toonIdsToAnimIntervals[toonId] = Sequence(
                    parallel,
                    Func(toon.loop, 'neutral'),
                    )
            else:
                self.notify.warning("toon %d is none, skipping toon.loop(neutral)" % toonId)
                self.toonIdsToAnimIntervals[toonId] = parallel
            self.toonIdsToAnimIntervals[toonId].start()
            
    def setAdvantage(self, advantage):
        DistributedPartyTeamActivity.setAdvantage(self, advantage)
        
        if self.isLocalToonPlaying:
            self.setIdealRate(PartyGlobals.TugOfWarTargetRateList[0][1])
