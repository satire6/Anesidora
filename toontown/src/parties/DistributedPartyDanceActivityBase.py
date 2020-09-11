#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: Party Dance Activity. Loads up the dance floor and plays the rotation
#          sequences, as well as handles dance moves and toons currently dancing.
#          Toon animation states are handled by PartyDanceActivityToonFSM
#          Dance pattern input is handled through KeyCodes
#          Dance pattern visual is handled through keyCodesGui
#-------------------------------------------------------------------------------
import random

from pandac.PandaModules import *

from direct.interval.FunctionInterval import Wait, Func
from direct.interval.MetaInterval import Sequence, Parallel
from direct.showbase.PythonUtil import lerp, Enum
from direct.fsm import FSM

from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.minigame.OrthoDrive import OrthoDrive
from toontown.minigame.OrthoWalk import OrthoWalk

from toontown.parties.activityFSMs import DanceActivityFSM
from toontown.parties.PartyGlobals import ActivityIds, ActivityTypes
from toontown.parties.PartyGlobals import DancePatternToAnims, DanceAnimToName
from toontown.parties.DistributedPartyActivity import DistributedPartyActivity
from toontown.parties.PartyDanceActivityToonFSM import PartyDanceActivityToonFSM
from toontown.parties.PartyDanceActivityToonFSM import ToonDancingStates
from toontown.parties.KeyCodes import KeyCodes
from toontown.parties.KeyCodesGui import KeyCodesGui
from toontown.parties import PartyGlobals

DANCE_FLOOR_COLLISION = "danceFloor_collision"

DanceViews = Enum(("Normal",
                   "Dancing",
                   "Isometric",
                   ))

class DistributedPartyDanceActivityBase(DistributedPartyActivity):
    notify = directNotify.newCategory("DistributedPartyDanceActivity")
        
    def __init__(self, cr, actId, dancePatternToAnims):
        DistributedPartyActivity.__init__(self,
                                          cr,
                                          actId,
                                          ActivityTypes.Continuous
                                          )
        self.danceFloor = None
        
        self.localToonDancing = False
        self.keyCodes = None
        self.gui = None
        self.currentCameraMode = None
        self.orthoWalk = None
        self.cameraParallel = None
        self.localToonDanceSequence = None
        self.localPatternsMatched = []
        self.dancePatternToAnims = dancePatternToAnims
        # Map of toonIds to PartyDanceActivityToonFSMs
        self.dancingToonFSMs = {}
        
    def generateInit(self):
        self.notify.debug("generateInit")
        DistributedPartyActivity.generateInit(self)
        
        self.keyCodes = KeyCodes(patterns = self.dancePatternToAnims.keys())
        self.gui = KeyCodesGui(self.keyCodes)
        self.__initOrthoWalk()
        self.activityFSM = DanceActivityFSM(self)
        
    def announceGenerate(self):
        DistributedPartyActivity.announceGenerate(self)
        self.activityFSM.request("Active")
    
    def load(self):
        """
        Loads the dance floor and place it in the right spot.
        """
        DistributedPartyActivity.load(self)
        
        self.danceFloor = loader.loadModel("phase_13/models/parties/danceFloor")
        self.danceFloor.reparentTo(self.getParentNodePath())
        self.danceFloor.setPos(self.x, self.y, 0.0)
        self.danceFloor.setH(self.h)
        
        # Reparent to render so that when the fireworks are on, it "glows" in the dark
        self.danceFloor.wrtReparentTo(render)
        
        self.sign.setPos(22, -22, 0)
        
        # Initialize programatic animation sequences
        floor = self.danceFloor.find("**/danceFloor_mesh")
        self.danceFloorSequence = Sequence(Wait(0.3),
                                           Func(floor.setH, floor, 36))
        
        # Spin the ball around while bobbing up and down
        # (since it's being held by balloons!)
        # spinning the disco ball moved to the child classes,
        # to deal with 10 and 20 on the ball
        discoBall = self.danceFloor.find("**/discoBall_mesh")
        self.discoBallSequence = Parallel(
            discoBall.hprInterval(6.0, Vec3(360, 0, 0)),
            Sequence(discoBall.posInterval(3, Point3(0, 0, 1), blendType="easeInOut"),
                     discoBall.posInterval(3, Point3(0, 0, 0), blendType="easeInOut")
                     ),
            )

        
        
    def unload(self):
        """
        Unloads the dance floor.
        """
        DistributedPartyActivity.unload(self)
        self.activityFSM.request("Disabled")
        
        if self.localToonDanceSequence is not None:
            self.localToonDanceSequence.finish()
        
        if self.localToonDancing:
            self.__localStopDancing()
            
        self.ignoreAll()
        
        if self.discoBallSequence is not None:
            self.discoBallSequence.finish()
            
        if self.danceFloorSequence is not None:
            self.danceFloorSequence.finish()
        
        del self.danceFloorSequence
        del self.discoBallSequence
        del self.localToonDanceSequence
        
        if self.danceFloor is not None:
            self.danceFloor.removeNode()
            self.danceFloor = None
            
        self.__destroyOrthoWalk()
        
        for toonId in self.dancingToonFSMs.keys():
            self.dancingToonFSMs[toonId].destroy()
            del self.dancingToonFSMs[toonId]
        del self.dancingToonFSMs
        
        del self.cameraParallel
        del self.currentCameraMode
            
        if self.keyCodes is not None:
            self.keyCodes.destroy()
            del self.keyCodes
        
        del self.activityFSM
        del self.gui
        
        del self.localPatternsMatched
        
    def handleToonDisabled(self, toonId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleToonDisabled avatar " + str(toonId) + " disabled")
        # clean up any references to the disabled avatar before he disappears
        if self.dancingToonFSMs.has_key(toonId):
            self.dancingToonFSMs[toonId].request("cleanup")
            self.dancingToonFSMs[toonId].destroy()
            del self.dancingToonFSMs[toonId]
        
    def getTitle(self):
        self.notify.warning("define title for this dance activity")
        return TTLocalizer.PartyDanceActivityTitle

    def getInstructions(self):
        self.notify.warning("define instructions for this dance activity")
        return TTLocalizer.PartyDanceActivityInstructions
        
#===============================================================================
# FSM States
#===============================================================================

    def startActive(self):
        self.accept('enter' + DANCE_FLOOR_COLLISION, self.__handleEnterDanceFloor)
        self.accept('exit' + DANCE_FLOOR_COLLISION, self.__handleExitDanceFloor)
        
        self.danceFloorSequence.loop()
        self.discoBallSequence.loop()
        
    def finishActive(self):
        pass
    
    def startDisabled(self):
        self.ignore('enter' + DANCE_FLOOR_COLLISION)
        self.ignore('exit' + DANCE_FLOOR_COLLISION)
        self.discoBallSequence.pause()
        self.danceFloorSequence.pause()
    
    def finishDisabled(self):
        pass
            
#===============================================================================
# Ortho movement
#===============================================================================
 
    # Orthowalk init/shutdown
    def __initOrthoWalk(self):
        """
        Initializes ortho walk movement for the local toon.
        Orthowalk is movement where up is +y and right is +x in relation to the toon's parent
        """
        self.notify.debug("Initialize Ortho Walk")

        orthoDrive = OrthoDrive(9.778) # run speed = run frames (15) / fps (24fps) * avg. run speed (14.667 ft./s)
        self.orthoWalk = OrthoWalk(orthoDrive, broadcast=True)

    def __destroyOrthoWalk(self):
        self.notify.debug("Destroy Ortho Walk")
        self.orthoWalk.stop()
        self.orthoWalk.destroy()
        del self.orthoWalk
        
    def __disableLocalControl(self):
        self.orthoWalk.stop()
        self.keyCodes.disable()
        self.keyCodesGui.disable()
        
    def __enableLocalControl(self):
        self.orthWalk.start()
        self.keyCodes.enable()
        self.keyCodesGui.enable()
        self.keyCodesGui.hideAll()
      
#===============================================================================
# Enter / Exit Dance Floor
#===============================================================================
            
    def __handleEnterDanceFloor(self, collEntry):
        """
        Triggered when the local toon enters the dance floor collision.
        """
        if not self.isLocalToonInActivity() and not self.localToonDancing:
            self.notify.debug("Toon enters dance floor collision area.")
            place = base.cr.playGame.getPlace()
            if place and hasattr(place, "fsm"):
                place.fsm.request("activity")
            self.d_toonJoinRequest()
            place = base.cr.playGame.getPlace()
            if place and hasattr(place,"fsm"):
                place.fsm.request("activity")
    
    def joinRequestDenied(self, reason):
        DistributedPartyActivity.joinRequestDenied(self, reason)
        
        self.showMessage(TTLocalizer.PartyActivityDefaultJoinDeny)
        place = base.cr.playGame.getPlace()
        if place and hasattr(place,"fsm"):
            place.fsm.request("walk")
    
    # Distributed (broadcast ram)
    def setToonsPlaying(self, toonIds, toonHeadings):
        """
        Overrides DistributedPartyActivity's setToonsPlaying because it needs
        heading information for each toon.
        """
        self.notify.debug("setToonsPlaying" )
        self.notify.debug("\ttoonIds: %s" % toonIds)
        self.notify.debug("\ttoonHeadings: %s" % toonHeadings)
        
        (exitedToons, joinedToons) = self.getToonsPlayingChanges(self.toonIds, toonIds)
        self.notify.debug("\texitedToons: %s" % exitedToons)
        self.notify.debug("\tjoinedToons: %s" % joinedToons)
        
        self.setToonIds(toonIds)
        self._processExitedToons(exitedToons)
                    
        # Handle the joining toons
        for toonId in joinedToons:
            
            # Only trigger handleToonJoined if it isn't the local Toon
            # or if the local Toon is joining this activity.
            if (toonId != base.localAvatar.doId or
                (toonId == base.localAvatar.doId and 
                self.isLocalToonRequestStatus(PartyGlobals.ActivityRequestStatus.Joining))):
                
                self._enableHandleToonDisabled(toonId)
                self.handleToonJoined(toonId, toonHeadings[toonIds.index(toonId)])
                
                if toonId == base.localAvatar.doId:
                    self._localToonRequestStatus = None

    def handleToonJoined(self, toonId, h):
        """
        Called when toon is allowed to enter dance floor.
        """
        self.notify.debug("handleToonJoined( toonId=%d, h=%.2f )" %(toonId, h))
        if base.cr.doId2do.has_key(toonId):
            toonFSM = PartyDanceActivityToonFSM(toonId, self, h)
            toonFSM.request("Init")
            self.dancingToonFSMs[toonId] = toonFSM
            
            if toonId == base.localAvatar.doId:
                self.__localStartDancing(h)
            
    def __localStartDancing(self, h):
        """
        Local toon is entering dance floor. Listen for extra events and enable
        ortho movement.
        """
        if not self.localToonDancing:
            place = base.cr.playGame.getPlace()
            if place and hasattr(place,"fsm"):
                self.localToonDancing = True
                place.fsm.request("activity")
                self.__updateLocalToonState(ToonDancingStates.Run)
                self.__setViewMode(DanceViews.Dancing)
                self.gui.load()

                self.startRules()
                self.__localEnableControls()
            else:
                self.notify.warning("__localStartDancing, failed in playGame.getPlace()")
            
    def handleRulesDone(self):
        self.finishRules()
        
    def __localEnableControls(self):
        if not self.dancingToonFSMs.has_key(base.localAvatar.doId):
            self.notify.debug("no dancing FSM for local avatar, not enabling controls")
            return
        self.accept(KeyCodes.PATTERN_MATCH_EVENT, self.__doDanceMove)
        self.accept(KeyCodes.PATTERN_NO_MATCH_EVENT, self.__noDanceMoveMatch)
        self.acceptOnce(KeyCodes.KEY_DOWN_EVENT, self._handleKeyDown)
        self.accept(KeyCodes.KEY_UP_EVENT, self._handleKeyUp)

        self.keyCodes.enable()
        self.orthoWalk.start()
        self.gui.enable()
        self.gui.hideAll()
        
    def __localDisableControls(self):
        self.orthoWalk.stop()
        self.keyCodes.disable()
        self.gui.disable()
                 
        self.ignore(KeyCodes.PATTERN_MATCH_EVENT)
        self.ignore(KeyCodes.PATTERN_NO_MATCH_EVENT)
        self.ignore(KeyCodes.KEY_DOWN_EVENT)
        self.ignore(KeyCodes.KEY_UP_EVENT)
            
    def __handleExitDanceFloor(self, collEntry):
        """
        Triggered when the local toon exits the dance floor collision.
        """
        if self.localToonDanceSequence is not None:
            self.notify.debug("finishing %s" % self.localToonDanceSequence)
            self.localToonDanceSequence.finish()
            self.localToonDanceSequence = None
        self.finishRules()
        self.notify.debug("Toon exits dance floor collision area.")
        self.d_toonExitRequest()
        
    def exitRequestDenied(self, reason):
        DistributedPartyActivity.exitRequestDenied(self, reason)
        if reason != PartyGlobals.DenialReasons.SilentFail:
            self.showMessage(TTLocalizer.PartyActivityDefaultExitDeny)
        
    def handleToonExited(self, toonId):
        """
        Stops the local toon from dancing.
        Called when when the client gets an exit response from the server.
        """
        self.notify.debug("exitDanceFloor %s" % toonId)
        if toonId == base.localAvatar.doId:
            self.__localStopDancing()
        
    def __localStopDancing(self):
        """
        Cleans up local dancing toon and broadcasts final state to all clients
        """
        if self.localToonDancing:           
            self.__localDisableControls()
            self.gui.unload()
            self.__setViewMode(DanceViews.Normal)
            
            self.__updateLocalToonState(ToonDancingStates.Cleanup)
            if base.cr.playGame.getPlace():
                if hasattr(base.cr.playGame.getPlace(),'fsm'):
                    base.cr.playGame.getPlace().fsm.request("walk")            
            self.localToonDancing = False
    
#===============================================================================
# Dance!
#===============================================================================
    
    def __doDanceMove(self, pattern):
        """
        Handler called when there is a pattern match
        """
        self.notify.debug("Dance move! %s" % pattern)
        
        anim = self.dancePatternToAnims.get(pattern)
        if anim:
            self.__updateLocalToonState(ToonDancingStates.DanceMove, anim)
            
            self.gui.setColor(0, 1, 0)
            self.gui.showText(DanceAnimToName.get(anim, anim))
            
            # Local toon just matched this pattern for the first time
            # play fancier animation.
            self.finishRules()
            if pattern not in self.localPatternsMatched:
                camNode = NodePath(self.uniqueName("danceCamNode"))
                camNode.reparentTo(base.localAvatar)
                camNode.lookAt(camera)
                camNode.setHpr(camNode.getH(), 0, 0)
                
                node2 = NodePath("tempCamNode")
                node2.reparentTo(camNode)
                node2.setPos(Point3(0, 15, 10))
                node2.lookAt(camNode)
                h = node2.getH() * (camera.getH(camNode) / abs(camera.getH(camNode)))
                node2.removeNode
                del node2
                
                hpr = camera.getHpr()
                pos = camera.getPos()
                camParent = camera.getParent()
    
                camera.wrtReparentTo(camNode)
                self.localToonDanceSequence = Sequence(
                    Func(self.__localDisableControls),
                    Parallel(
                        camera.posInterval(0.5,
                                           Point3(0, 15, 10),
                                           blendType="easeIn"),
                        camera.hprInterval(0.5,
                                           Point3(h, -20, 0),
                                           blendType="easeIn"),
                        ),
                    camNode.hprInterval(4.0,
                                        Point3(camNode.getH() - 360, 0, 0)
                                        ),
                    Func(camera.wrtReparentTo, camParent),
                    Func(camNode.removeNode),
                    Parallel(
                        camera.posInterval(0.5,
                                           pos,
                                           blendType="easeOut"),
                        camera.hprInterval(0.5,
                                           hpr,
                                           blendType="easeOut")
                        ),
                    Func(self.__localEnableControls)
                    )
            else:
                self.localToonDanceSequence = Sequence(
                    Func(self.__localDisableControls),
                    Wait(2.0),
                    Func(self.__localEnableControls),
                    )
                
            self.localToonDanceSequence.start()
            self.localPatternsMatched.append(pattern)
            
    def __noDanceMoveMatch(self):
        """
        Called when a match fails.
        """
        self.gui.setColor(1, 0, 0)
        self.gui.showText("No Match!")
        
        
        self.__updateLocalToonState(ToonDancingStates.DanceMove)
        self.localToonDanceSequence = Sequence(
            Func(self.__localDisableControls),
            Wait(1.0),
            Func(self.__localEnableControls),
            )
                
        self.localToonDanceSequence.start()
        
    def _handleKeyDown(self, key, index):
        """
        Called when a key in KeyCodes is pressed down.
        """
        self.__updateLocalToonState(ToonDancingStates.Run)
        
    def _handleKeyUp(self, key):
        """
        Called when a key in KeyCodes is pressed up.
        """
        if not self.keyCodes.isAnyKeyPressed():
            self.__updateLocalToonState(ToonDancingStates.DanceMove)
            self.acceptOnce(KeyCodes.KEY_DOWN_EVENT, self._handleKeyDown)
        
#===============================================================================
# Dancing Toon State
#===============================================================================
        
    def __updateLocalToonState(self, state, anim=""):
        """
        Sets the dancing toon's local and remote fsm. This is done immediately
        in the local side, while the state is sent to the AI for the other clients.
        """
        self._requestToonState(base.localAvatar.doId, state, anim)
        self.d_updateDancingToon(state, anim)
        
    # Distributed (clsend airecv)
    def d_updateDancingToon(self, state, anim):
        self.sendUpdate("updateDancingToon", [state, anim])
    
    # Distributed (broadcast ram)
    def setDancingToonState(self, toonId, state, anim):
        """
        From AI, it sets a dancing toon's FSM
        """
        if toonId != base.localAvatar.doId and self.dancingToonFSMs.has_key(toonId):
            self._requestToonState(toonId, state, anim)
            
    def _requestToonState(self, toonId, state, anim):
        if self.dancingToonFSMs.has_key(toonId):
            state = ToonDancingStates.getString(state)
            curState = self.dancingToonFSMs[toonId].getCurrentOrNextState()
            assert(self.notify.debug("requestToonState toonId=%s, state=%s, anim=%s" % (toonId, state, anim)))
            try:
                self.dancingToonFSMs[toonId].request(state, anim)
            except FSM.RequestDenied:
                self.notify.warning("could not go from state=%s to state %s" % (curState, state))
            if state == ToonDancingStates.getString(ToonDancingStates.Cleanup):
                self.notify.debug("deleting this fsm %s" % (self.dancingToonFSMs[toonId]))
                del self.dancingToonFSMs[toonId]
                # the local Toon dance sequence has camera reparents, which is bad if
                # we're not in the dance floor anymore.
                if self.localToonDanceSequence:
                    self.notify.debug("forcing a finish of localToonDanceSequence")
                    self.localToonDanceSequence.finish()
                    self.localToonDanceSequence = None
                
#===============================================================================
# Camera
#===============================================================================

    def __setViewMode(self, mode):
        """
        Changes the camera mode and controls according to the camera.
        Called typically when toon enters/exits the dance floor.
        """
        assert(self.notify.debug("Set camera mode to %d" % mode))
        toon = base.localAvatar
        
        if mode == DanceViews.Normal:
            """
            if self.currentCameraMode == DanceViews.Isometric:
                base.cam.node().setLens(self.clens)
            """
            
            if self.cameraParallel is not None:
                self.cameraParallel.pause()
                self.cameraParallel = None
            
            camera.reparentTo(toon)
            base.localAvatar.startUpdateSmartCamera()
            
        elif mode == DanceViews.Dancing:
            base.localAvatar.stopUpdateSmartCamera()
            camera.wrtReparentTo(self.danceFloor)
            
            # Get the destination of the camera
            # based on the orientation of the toon parent dance node.
            node = NodePath("temp")
            node.reparentTo(toon.getParent())
            node.setPos(Point3(0, -40, 20))
            
            node2 = NodePath("temp2")
            node2.reparentTo(self.danceFloor)
            node.reparentTo(node2)
            node2.setH(render, toon.getParent().getH())
            pos = node.getPos(self.danceFloor)
            
            node2.removeNode()
            node.removeNode()
            
            self.cameraParallel = Parallel(
                camera.posInterval(0.5, pos, blendType="easeIn"),
                camera.hprInterval(0.5, Point3(0, -27, 0), other=toon.getParent(), blendType="easeIn")
                )
            self.cameraParallel.start()
            
        """
        if mode == DanceViews.Isometric:
            if not hasattr(self, 'olens'):
                self.olens = OrthographicLens()
                self.olens.setFilmSize(20, 15)  # or whatever is appropriate for your scene
                self.clens = base.cam.node().getLens()
            base.cam.node().setLens(self.olens)
            
            def handleF1Pressed(self):
                if base.cam.node().getLens() == self.clens:
                    base.cam.node().setLens(self.olens)
                else:
                    base.cam.node().setLens(self.clens)
            self.accept('f1', handleF1Pressed)
        """
        
        self.currentCameraMode = mode
        
