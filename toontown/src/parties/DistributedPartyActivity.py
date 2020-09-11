#-------------------------------------------------------------------------------
# Contact: Shawn Patton, Rob Gordon, Edmundo Ruiz (Schell Games)
# Created: Sep 2008
#
# Purpose: DistributedPartyActivity is the base class for all party activities.
#          It loads up the sign and lever (where applicable)
#-------------------------------------------------------------------------------
#from pandac.PandaModules import VBase4
from pandac.PandaModules import CollisionSphere, CollisionNode, CollisionTube
from pandac.PandaModules import TextNode, NodePath, Vec3, Point3

from direct.distributed.ClockDelta import globalClockDelta
#from direct.gui.DirectGui import DirectLabel
from direct.distributed import DistributedObject
from direct.showbase import RandomNumGen
from direct.showbase import PythonUtil
from direct.interval.IntervalGlobal import Sequence, Parallel, ActorInterval
from direct.interval.FunctionInterval import Wait

from otp.avatar import Emote
from otp.otpbase import OTPGlobals

from toontown.toonbase import TTLocalizer
from toontown.parties import PartyGlobals
from toontown.minigame.MinigameRulesPanel import MinigameRulesPanel
from toontown.toontowngui import TTDialog
from toontown.parties.JellybeanRewardGui import JellybeanRewardGui
from toontown.parties.PartyUtils import getPartyActivityIcon, getCenterPosFromGridSize

class DistributedPartyActivity(DistributedObject.DistributedObject):
    """
    Base class for Distributed Party Activity objects on the client side. A distributed
    party activity constitutes of any game or area at a party that involves multiple toons
    interacting with it at the same time.
    
    Note that a new notify category is not created here as this class expects
    subclasses to create it.
    """
    
    def __init__(self, cr, activityId, activityType, wantLever=False, wantRewardGui=False):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.activityId = activityId
        self.activityName = PartyGlobals.ActivityIds.getString(self.activityId)
        self.activityType = activityType
        self.wantLever = wantLever
        self.wantRewardGui = wantRewardGui
        self.messageGui = None
        self.rewardGui = None
        self.toonIds = [] # list of doIds of toons in this activity
        # related-object requests
        self._toonId2ror = {}
        # Put a reference to this activity on base, for easy debugging
        # access, this will get cleaned up in DistributedPartyActivity
        childName = "%s"%self
        childName = childName[childName.rfind(".DistributedParty")+len(".DistributedParty"):childName.rfind("Activity instance")]
        if not hasattr(base, "partyActivityDict"):
            base.partyActivityDict = {}
        base.partyActivityDict[childName] = self

        self.root = NodePath('root')
        
        # This label is used to give status of the activity to the player
#        self.activityStatusLabel = DirectLabel(
#            text = TTLocalizer.PartyActivityWaitingForOtherPlayers,
#            text_fg = VBase4(1,1,1,1),
#            relief = None,
#            pos = (-0.6, 0, -0.75),
#            scale = 0.075)   
#        self.activityStatusLabel.hide()

        # Play Activity's party activity state data throws this when the local toon
        # is done reading the rules
        self.rulesDoneEvent = "rulesDone"

        # for the load bar
        self.modelCount = 500

        self.cleanupActions = []

        # these are flags that the subclass can manipulate to keep
        # this base class from messing with the toons as the activity
        # starts up; see setUsesSmoothing and setUsesLookAround below
        self.usesSmoothing = 0
        self.usesLookAround = 0

        # difficulty debug overrides
        self.difficultyOverride  = None
        self.trolleyZoneOverride = None
        
        self._localToonRequestStatus = None

#-------------------------------------------------------------------------------
# join/exit request functions
#-------------------------------------------------------------------------------
    def localToonExiting(self):
        assert self.notify.debugStateCall(self)
        self._localToonRequestStatus = PartyGlobals.ActivityRequestStatus.Exiting
    
    def localToonJoining(self):
        assert self.notify.debugStateCall(self)
        self._localToonRequestStatus = PartyGlobals.ActivityRequestStatus.Joining

    # Distributed (clsend airecv)
    def d_toonJoinRequest(self):
        """
        Send request for local toon to join the activity. Expect a
        joinRequestDenied or handleToonJoined in reply.
        """
        if self._localToonRequestStatus is None:
            assert(self.notify.debug("d_toonJoinRequest"))
            self.localToonJoining()
            self.sendUpdate("toonJoinRequest")
        else:
            assert(self.notify.debug("d_toonJoinRequest not sending request as _localToonRequest=%d" %
                                     self._localToonRequest))

    # Distributed (clsend airecv)
    def d_toonExitRequest(self):
        """
        Requests to for local toon to drop out of the activity. Expect a
        exitRequestDenied or handleToonExited in reply.
        """
        if self._localToonRequestStatus is None:
            assert(self.notify.debug("d_toonExitRequest"))
            self.localToonExiting()
            self.sendUpdate("toonExitRequest")
        else:
            assert(self.notify.debug("d_toonExitRequest not sending request as _localToonRequest=%d" %
                                     self._localToonRequest))

    # Distributed (clsend airecv)
    def d_toonExitDemand(self):
        """
        Tells AI that the local toon is leaving the activity. Expect a
        toonExitResponse in reply.
        """
        assert(self.notify.debug("d_toonExitDemand"))
        self.localToonExiting()
        self.sendUpdate("toonExitDemand")
        
#-------------------------------------------------------------------------------
# join/exit functions that subclasses should override
#-------------------------------------------------------------------------------
    def joinRequestDenied(self, reason):
        """
        Called when the client's request to join an activity has been denied.
        Subclasses can override this function.
        
        Parameters:
            reason -- a PartyGlobals.DenailReasons value
        """
        self._localToonRequestStatus = None
        
    def exitRequestDenied(self, reason):
        """
        Called when the client's request to exit an activity has been denied.
        Subclasses can override this function.
        
        Parameters:
            reason -- a PartyGlobals.DenailReasons value
        """
        self._localToonRequestStatus = None
        
    def handleToonJoined(self, toonId):
        """
        Whenever a new toon joins the activity, this function is called.
        Subclasses should override this function.
        
        Parameters:
            toonId -- doId of the toon that joined
        """
        self.notify.error("BASE: handleToonJoined should be overridden %s" % self.activityName)

    def handleToonExited(self, toonId):
        """
        Whenever a toon exits the activity, this function is called.
        Subclasses should override this function.
        
        Parameters:
            toonId -- doId of the toon that exited
        """
        self.notify.error("BASE: handleToonExited should be overridden %s" % self.activityName)
        
    def handleToonDisabled(self, toonId):
        """
        A toon dropped unexpectedly from the game. Handle it!
        """
        self.notify.error("BASE: handleToonDisabled should be overridden %s" % self.activityName)
        
#-------------------------------------------------------------------------------

    # Distributed (broadcast ram)
    def setToonsPlaying(self, toonIds):
        """
        Broadcast response from the server that sends out the list of toons
        currently in the party activity. This is for all clients to properly sync up
        states for the toons in the activity.
        
        Parameters:
            toonIds -- is a list of all the toons in the activity
        """
        
        assert(self.notify.debug("BASE: setToonsPlaying = %s" % toonIds))
        
        # Split list into who joined and who exited:
        (exitedToons, joinedToons) = self.getToonsPlayingChanges(self.toonIds, toonIds)
        
        assert(self.notify.debug("\texitedToons: %s" % exitedToons))
        assert(self.notify.debug("\tjoinedToons: %s" % joinedToons))
        
        self.setToonIds(toonIds)
        
        self._processExitedToons(exitedToons)
        self._processJoinedToons(joinedToons)
                    
    def _processExitedToons(self, exitedToons):
        """Handle the exited toons"""
        for toonId in exitedToons:
            if (toonId != base.localAvatar.doId or
                (toonId == base.localAvatar.doId and 
                self.isLocalToonRequestStatus(PartyGlobals.ActivityRequestStatus.Exiting))):
                
                toon = self.getAvatar(toonId)
                if toon is not None:
                    self.ignore(toon.uniqueName("disable"))
                
                self.handleToonExited(toonId)
                
                if toonId == base.localAvatar.doId:
                    self._localToonRequestStatus = None

                if toonId in self._toonId2ror:
                    self.cr.relatedObjectMgr.abortRequest(self._toonId2ror[toonId])
                    del self._toonId2ror[toonId]
    
    def _processJoinedToons(self, joinedToons):
        """Handle the joining toons"""
        for toonId in joinedToons:
            
            # Only trigger handleToonJoined if it isn't the local Toon
            # or if the local Toon is joining this activity.
            if (toonId != base.localAvatar.doId or
                (toonId == base.localAvatar.doId and 
                self.isLocalToonRequestStatus(PartyGlobals.ActivityRequestStatus.Joining))):
                if toonId not in self._toonId2ror:
                    request = self.cr.relatedObjectMgr.requestObjects(
                        [toonId], allCallback=self._handlePlayerPresent)
                    if toonId in self._toonId2ror:
                        # toon is already here
                        del self._toonId2ror[toonId]
                    else:
                        self._toonId2ror[toonId] = request
                    
    def _handlePlayerPresent(self, toons):
        toon = toons[0]
        toonId = toon.doId
        if toonId in self._toonId2ror:
            del self._toonId2ror[toonId]
        else:
            # toon is already here
            self._toonId2ror[toonId] = None

        self._enableHandleToonDisabled(toonId)
        self.handleToonJoined(toonId)

        if toonId == base.localAvatar.doId:
            self._localToonRequestStatus = None
 
    def _enableHandleToonDisabled(self, toonId):
        toon = self.getAvatar(toonId)
        if toon is not None:
            self.acceptOnce(
                toon.uniqueName("disable"),
                self.handleToonDisabled,
                [toonId],
            )
        else:
            self.notify.warning("BASE: unable to get handle to toon with toonId:%d. Hook for handleToonDisabled not set." % toonId)
                    
    def isLocalToonRequestStatus(self, requestStatus):
        return (self._localToonRequestStatus == requestStatus)
    
    def setToonIds(self, toonIds):
        """Updates the list of toon ids in the activity"""
        self.toonIds = toonIds
                    
    def getToonsPlayingChanges(self, oldToonIds, newToonIds):
        """
        Returns
            a tuple of (list of doIds of toons who exited, list of doIds of toons who joined)
        """
        oldToons = set(oldToonIds)
        newToons = set(newToonIds)
        # find toons that are no longer in the game
        exitedToons = oldToons.difference(newToons)
        # find toons that just joined the game
        joinedToons = newToons.difference(oldToons)
        # return results
        return(list(exitedToons), list(joinedToons))

    def setUsesSmoothing(self):
        self.usesSmoothing = True

    def setUsesLookAround(self):
        self.usesLookAround = True
    
#    def getTitle(self):
#        """
#        Return the title of the party activity.
#        Subclasses should redefine. 
#        """
#        return TTLocalizer.DefaultPartyActivityTitle

    def getInstructions(self):
        """
        Return the instructions for the party activity.
        Subclasses should redefine.
        """
        return TTLocalizer.DefaultPartyActivityInstructions
    
    def getParentNodePath(self):
        """
        Overwritten: Originally returns render.
        Returns Place NodePath.
        """        
        if hasattr(base.cr.playGame, "hood") and base.cr.playGame.hood and \
        hasattr(base.cr.playGame.hood, "loader") and base.cr.playGame.hood.loader \
        and hasattr(base.cr.playGame.hood.loader, "geom") and base.cr.playGame.hood.loader.geom:
            return base.cr.playGame.hood.loader.geom            
        else:        
            self.notify.warning("Hood or loader not created, defaulting to render")            
            return render

    def __createRandomNumGen(self):
        self.notify.debug("BASE: self.doId=0x%08X" % self.doId)
        # seed the random number generator with the party activity doId
        self.randomNumGen = RandomNumGen.RandomNumGen(self.doId)
        def destroy(self=self):
            self.notify.debug("BASE: destroying random num gen")
            del self.randomNumGen
        self.cleanupActions.append(destroy)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.notify.debug("BASE: generate, %s" % self.getTitle())
        self.__createRandomNumGen()

    def announceGenerate(self):
        """
        announceGenerate is called after all of the required fields are
        filled in
        """
        DistributedObject.DistributedObject.announceGenerate(self)
        self.notify.debug("BASE: announceGenerate %s" % self.activityName)
        # update root's name and position within the party grounds
        self.root.setName(self.activityName + "Root")
        centeredX, centeredY = getCenterPosFromGridSize(self.x, self.y, PartyGlobals.ActivityInformationDict[self.activityId]["gridsize"])
        self.root.setPos( centeredX, centeredY, 0.0 )
        self.root.setH( self.h )

        # if this flag is set to zero, we won't notify the server that
        # we've left at the end of the activity
        self.normalExit = True

        if self.wantLever:
            self.leverTriggerEvent = self.uniqueName('leverTriggerEvent')
        self.load()

        def cleanup(self=self):
            self.notify.debug("BASE: cleanup: normalExit=%s" % self.normalExit)

            # make sure we clear the screen
            base.cr.renderFrame()
            
            # If we didn't abort, tell the AI we are exiting
            if self.normalExit:
                self.sendUpdate("toonExitRequest")
        self.cleanupActions.append(cleanup)

    def disable(self):
        self.notify.debug("BASE: disable")
        DistributedObject.DistributedObject.disable(self)
        rorToonIds = self._toonId2ror.keys()
        for toonId in rorToonIds:
            self.cr.relatedObjectMgr.abortRequest(self._toonId2ror[toonId])
            del self._toonId2ror[toonId]
        self.ignore(self.messageDoneEvent)
        if self.messageGui is not None and not self.messageGui.isEmpty():
            self.messageGui.cleanup()
            self.messageGui = None

    def delete(self):
        self.notify.debug("BASE: delete")
        self.unload()
        # make sure we're not accepting any events
        self.ignoreAll()
        DistributedObject.DistributedObject.delete(self)

    def load(self):
        self.notify.debug("BASE: load")
        # Load the sign for this activity
        self.loadSign()
        # Load the lever (if applicable)
        if self.wantLever:
            self.loadLever()
        if self.wantRewardGui:
            self.showRewardDoneEvent = self.uniqueName("showRewardDoneEvent")
            self.rewardGui = JellybeanRewardGui(self.showRewardDoneEvent)
        self.messageDoneEvent = self.uniqueName("messageDoneEvent") 
        self.root.reparentTo(self.getParentNodePath())
        self._enableCollisions()

    def loadSign(self):
        actNameForSign = self.activityName
        if self.activityId == PartyGlobals.ActivityIds.PartyJukebox40:
            actNameForSign = PartyGlobals.ActivityIds.getString(PartyGlobals.ActivityIds.PartyJukebox)
        elif self.activityId == PartyGlobals.ActivityIds.PartyDance20:
            actNameForSign = PartyGlobals.ActivityIds.getString(PartyGlobals.ActivityIds.PartyDance)
        self.sign = self.root.attachNewNode('%sSign'%self.activityName)
        self.signModel = self.party.defaultSignModel.copyTo(self.sign)
        self.signFlat = self.signModel.find("**/sign_flat")
        self.signFlatWithNote = self.signModel.find("**/sign_withNote")
        self.signTextLocator = self.signModel.find("**/signText_locator")
        
        textureNodePath = getPartyActivityIcon(self.party.activityIconsModel, actNameForSign)
                
        textureNodePath.setPos(0.0, -0.02, 2.2)
        textureNodePath.setScale(2.35)
        textureNodePath.copyTo(self.signFlat)
        textureNodePath.copyTo(self.signFlatWithNote)

        text = TextNode("noteText")
        text.setTextColor(0.2, 0.1, 0.7, 1.0)
        text.setAlign(TextNode.ACenter)
        text.setFont(OTPGlobals.getInterfaceFont())
        text.setWordwrap( 10.0 )
        text.setText("")
        self.noteText = self.signFlatWithNote.attachNewNode(text)
        self.noteText.setPosHpr(self.signTextLocator, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0)
        self.noteText.setScale(0.2)

        self.signFlatWithNote.stash()
        self.signTextLocator.stash()

    def loadLever(self):
        """
        SubClasses can override this if they want to move their lever somewhere
        special... call this, then change the position.
        """
        self.lever = self.root.attachNewNode('%sLever'%self.activityName)
        self.leverModel = self.party.defaultLeverModel.copyTo(self.lever)
        # Do some crazy reparenting so you can scale the whole thing nicely
        self.controlColumn = NodePath('cc')
        column = self.leverModel.find('**/column')
        column.getChildren().reparentTo(self.controlColumn)
        self.controlColumn.reparentTo(column)
        self.stickHinge = self.controlColumn.attachNewNode('stickHinge')
        self.stick = self.party.defaultStickModel.copyTo(self.stickHinge)
        self.stickHinge.setHpr(0.0, 90.0, 0.0)
        self.stick.setHpr(0, -90.0, 0)
        self.stick.flattenLight()
        self.bottom = self.leverModel.find('**/bottom')
        self.bottom.wrtReparentTo(self.controlColumn)
        self.bottomPos = self.bottom.getPos()

        # Make a trigger sphere so we can detect when the local avatar
        # runs up to the lever.
        cs = CollisionSphere(0.0, 1.35, 2.0, 1.0)
        cs.setTangible(False)
        cn = CollisionNode(self.leverTriggerEvent)
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        self.leverTrigger = self.root.attachNewNode(cn)
        self.leverTrigger.reparentTo(self.lever)
        self.leverTrigger.stash()

        # Also, a solid tube to keep us from running through the
        # lever itself.  This one scales with the control
        # model.
        cs = CollisionTube(0.0, 2.7, 0.0, 0.0, 2.7, 3.0, 1.2)
        cn = CollisionNode('levertube')
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        self.leverTube = self.leverModel.attachNewNode(cn)

        # Let's set the height of the lever to the height of the host
        host = base.cr.doId2do.get(self.party.partyInfo.hostId)
        if host is None:
            self.notify.debug("%s loadLever : Host has left the game before lever could be created."%self.activityName)
            return

        # We start by figuring out where we are going by setting the
        # scale and position appropriately
#        origScale = self.leverModel.getSz()
#        origCcPos = self.controlColumn.getPos()
#        origBottomPos = self.bottom.getPos()
#        origStickHingeHpr = self.stickHinge.getHpr()
        
        # First, scale the thing overall to match the host's scale,
        # including cheesy effect scales.
        scale = host.getGeomNode().getChild(0).getSz(render)
        self.leverModel.setScale(scale)

        # Then get the position of the host's right hand when he's
        # standing at the controls in a leverNeutral pose.
        self.controlColumn.setPos(0, 0, 0)
        host.setPosHpr(self.lever, 0, 0, 0, 0, 0, 0)
        host.pose('leverNeutral', 0)
        host.update()
        pos = host.rightHand.getPos(self.controlColumn)

        # Now set the control column to the right height and position
        # to put the top of the stick approximately in his hand.
        self.controlColumn.setPos(pos[0], pos[1], pos[2] - 1)

        # And put the bottom piece back on the floor, wherever that
        # is from here.
        self.bottom.setZ(host, 0.0)
        self.bottom.setPos(self.bottomPos[0], self.bottomPos[1], self.bottom.getZ())

        # Also put the joystick in his hand.
        lookAtPoint = Point3(0.3, 0, 0.1)
        lookAtUp = Vec3(0, -1, 0)
        self.stickHinge.lookAt(host.rightHand, lookAtPoint, lookAtUp)
        
        host.play('walk')
        host.update()

    
    def unloadLever(self):
        self.lever.removeNode()
        self.leverModel.removeNode()
        self.controlColumn.removeNode()
        self.stickHinge.removeNode()
        self.stick.removeNode()
        self.bottom.removeNode()
        self.leverTrigger.removeNode()
        self.leverTube.removeNode()
        del self.bottomPos
        del self.lever
        del self.leverModel
        del self.controlColumn
        del self.stickHinge
        del self.stick
        del self.bottom
        del self.leverTrigger
        del self.leverTube

    def _enableCollisions(self):
        if self.wantLever:
            self.leverTrigger.unstash()
            self.accept("enter%s"%self.leverTriggerEvent, self._leverPulled)


    def _disableCollisions(self):
        if self.wantLever:
            self.leverTrigger.stash()
            self.ignore("enter%s"%self.leverTriggerEvent)


    def _leverPulled(self, collEntry):
        """
        This method is called when a toon collides with the activity's lever.

        Returns False if the activity should not be allowed to start due to it
        being a host initiated activity.

        Returns True otherwise.

        Subclasses should override, check the result of this method, and
        take appropriate action.
        """
        self.notify.debug("_leverPulled : Someone pulled the lever!!! ")

        if (self.activityType == PartyGlobals.ActivityTypes.HostInitiated) and \
           (base.localAvatar.doId != self.party.partyInfo.hostId):
            return False

        return True


    def getToonPullingLeverInterval(self, toon):
        walkTime = 0.2
        reach = ActorInterval(toon, 'leverReach', playRate=2.0)
        pull = ActorInterval(toon, 'leverPull', startFrame=6)
        origPos = toon.getPos(render)
        origHpr = toon.getHpr(render)
        newPos = self.lever.getPos(render)
        newHpr = self.lever.getHpr(render)
        origHpr.setX(PythonUtil.fitSrcAngle2Dest(origHpr[0], newHpr[0]))
        toon.setPosHpr(origPos, origHpr)
        reachAndPull = Sequence(ActorInterval(toon, 'walk', loop=True, duration=walkTime - reach.getDuration()), reach, pull)
        leverSeq = Sequence(
            Wait(walkTime + reach.getDuration()-0.1),
            self.stick.hprInterval(0.55, Point3(0.0, 25.0, 0.0), Point3(0.0, 0.0, 0.0)),
            Wait(0.3),
            self.stick.hprInterval(0.4, Point3(0.0, 0.0, 0.0), Point3(0.0, 25.0, 0.0)),
        )
        returnSeq = Sequence(
            Parallel(
                toon.posInterval(walkTime, newPos, origPos),
                toon.hprInterval(walkTime, newHpr, origHpr),
                leverSeq,
                reachAndPull,
            ),
        )
        return returnSeq


    def showMessage(self, message, endState='walk'):
        assert self.notify.debug("showMessage (endState=%s)" % endState)

        base.cr.playGame.getPlace().fsm.request("activity")
        self.acceptOnce(self.messageDoneEvent, self.__handleMessageDone)
        self.messageGui = TTDialog.TTGlobalDialog(
            doneEvent = self.messageDoneEvent,
            message = message,
            style = TTDialog.Acknowledge,
        )
        
        self.messageGui.endState = endState

    def __handleMessageDone(self):
        self.ignore(self.messageDoneEvent)
        if hasattr(base.cr.playGame.getPlace(), 'fsm'):
            if self.messageGui and hasattr(self.messageGui, 'endState'):
                self.notify.info("__handleMessageDone (endState=%s)" % self.messageGui.endState)
                base.cr.playGame.getPlace().fsm.request(self.messageGui.endState)
            else:
                self.notify.warning("messageGui has no endState, defaulting to 'walk'")
                base.cr.playGame.getPlace().fsm.request('walk')
        if self.messageGui is not None and not self.messageGui.isEmpty():
            self.messageGui.cleanup()
            self.messageGui = None
        
    def showJellybeanReward(self, earnedAmount, jarAmount, message):
        """
        Subclasses may call this to show the local player how many jellybeans
        they got for participating in an activity. 
        
        Parameters:
          earnedAmount -- How many jellybeans the toon gets
          jarAmount -- Amount in their pocketbook jar 
          message -- Activity-specific information to display while showing the
                     jellybean reward animation.
        """
        # If the local toon is not in any activity or in this activity.
        if (not self.isLocalToonInActivity()) or (base.localAvatar.doId in self.getToonIdsAsList()):
            # pop up a gui element that shows the message and has room to display
            # a jellybean animation
            messenger.send('DistributedPartyActivity-showJellybeanReward')
            base.cr.playGame.getPlace().fsm.request("activity")
            self.acceptOnce(self.showRewardDoneEvent, self.__handleJellybeanRewardDone)
            self.rewardGui.showReward(earnedAmount, jarAmount, message)
        
        
    def __handleJellybeanRewardDone(self):
        """
        The player is done viewing their jellybean reward. Clean up.
        """
        self.ignore(self.showRewardDoneEvent)
        self.handleRewardDone()

    def handleRewardDone(self):
        if base.cr.playGame.getPlace() and \
           hasattr(base.cr.playGame.getPlace(), "fsm"):
            base.cr.playGame.getPlace().fsm.request('walk')

    def setSignNote(self, note):
        self.noteText.node().setText( note )
        if len( note.strip() ) > 0:
            self.signFlat.stash()
            self.signFlatWithNote.unstash()
            self.signTextLocator.unstash()
        else:
            self.signFlat.unstash()
            self.signFlatWithNote.stash()
            self.signTextLocator.stash()


    def unload(self):
        self.notify.debug("BASE: unload")
        self.finishRules()
        self._disableCollisions()
#        self.activityStatusLabel.destroy()
#        del self.activityStatusLabel
        self.signModel.removeNode()
        del self.signModel
        self.sign.removeNode()
        del self.sign
        self.ignoreAll()
        if self.wantLever:
            self.unloadLever()
        self.root.removeNode()
        del self.root
        del self.activityId
        del self.activityName
        del self.activityType
        del self.wantLever
        del self.messageGui
        if self.rewardGui is not None:
            self.rewardGui.destroy()
        del self.rewardGui
        # some subclasses redefine this, so they might have already cleaned it
        # up at this point
        if hasattr(self, "toonIds"):
            del self.toonIds 
        del self.rulesDoneEvent
        del self.modelCount
        del self.cleanupActions
        del self.usesSmoothing
        del self.usesLookAround
        del self.difficultyOverride
        del self.trolleyZoneOverride
        if hasattr(base, 'partyActivityDict'):
            del base.partyActivityDict

    # Distributed (required broadcast)
    def setPartyDoId(self, partyDoId):
        self.party = base.cr.doId2do[partyDoId]


    # Distributed (required broadcast)
    def setX(self, x):
        self.x = x
        
        
    # Distributed (required broadcast)
    def setY(self, y):
        self.y = y
        
        
    # Distributed (required broadcast)
    def setH(self, h):
        self.h = h
    
    
    # Distributed (broadcast ram)
    def setState(self, newState, timestamp):
        """
        Subclasses must extend this function to make the actual request to
        its activityFSM. We do not do it here as we do not know which parameters
        beyond newState that each activity's fsm's states will need.
        """
        if newState == "Active":
            self.activityStartTime = globalClockDelta.networkToLocalTime(timestamp)


    def turnOffSmoothingOnGuests(self):
        # Disable smoothing, etc. for all the toons in the activity by default.
        # Some activities (e.g. the tag activity) may want to turn this back
        # on, but most activitys want full control over the toons'
        # placement onscreen.
        for toonId in self.toonIds:
            # Find the actual avatar in the cr
            avatar = self.getAvatar(toonId)
            if avatar:
                if not self.usesSmoothing:
                    avatar.stopSmooth()
                if not self.usesLookAround:
                    avatar.stopLookAround()


    def getAvatar(self, toonId):
        """
        Instead of all the party activitys writing code to do avatar lookups
        based on toonIds, they should use this function. It returns a toon
        if that toon is in the doId2do. If the ID cannot be resolved
        for some reason, a warning is logged and we return None. Each
        activity will have to deal with this.
        Why would an avatar not be in the doId2do? It can happen when
        an avatar quits the activity early but we still get an activity update
        afterwards.
        """

        # If it is an avatar, look it up in the doid2do
        if self.cr.doId2do.has_key(toonId):
            return self.cr.doId2do[toonId]
        # I do not know what this toonId is
        else:
            self.notify.warning(
                "BASE: getAvatar: No avatar in doId2do with id: " + str(toonId)
            )
            return None


    def getAvatarName(self, toonId):
        avatar = self.getAvatar(toonId)
        if avatar:
            return avatar.getName()
        else:
            return "Unknown"
        
        
    def isLocalToonInActivity(self):
        """
        Returns True if the local toon is in an activity, False otherwise.
        
        Sub-classes should use this to ensure the local toon isn't in another
        activity when they request to join this activity. This is mostly to
        prevent bug associated with hitting another activity when flying after
        being shot from the cannon.
        """
        result = False
        place = base.cr.playGame.getPlace()
        # fsm will be missing if this is called after the Party place obj is unloaded
        if (place and (place.__class__.__name__ == 'Party') and
            hasattr(place, 'fsm') and place.fsm):
            result = place.fsm.getCurrentState().getName() == "activity"
        return result


    def getToonIdsAsList(self):
        """
        Returns a list of doId's of all toons in this activity.
        
        Sub-classes should override this if they change how toon doId's are
        stored.
        """
        return self.toonIds


    def startRules(self, timeout=PartyGlobals.DefaultRulesTimeout):
        self.notify.debug("BASE: startRules")
        self.accept(self.rulesDoneEvent, self.handleRulesDone)
        # The rules panel is an onscreen panel
        self.rulesPanel = MinigameRulesPanel(
            "PartyRulesPanel",
            self.getTitle(),
            self.getInstructions(),
            self.rulesDoneEvent,
            timeout,
        )
        # turn off use of all the bottom cells, and the cell nearest the bottom
        # on each side
        base.setCellsAvailable(base.bottomCells + [base.leftCells[0], base.rightCells[1]], False)
        self.rulesPanel.load()
        self.rulesPanel.enter()


    def finishRules(self):
        self.notify.debug("BASE: finishRules")
        # Hide the rules
        self.ignore(self.rulesDoneEvent)
        if hasattr(self, "rulesPanel"):
            self.rulesPanel.exit()
            self.rulesPanel.unload()
            del self.rulesPanel
            
            base.setCellsAvailable(base.bottomCells + [base.leftCells[0], base.rightCells[1]], True)


    def handleRulesDone(self):
        self.notify.error("BASE: handleRulesDone should be overridden")

    def getTitle( self ):
        # Used by rulesPanel
        return TTLocalizer.PartyActivityNameDict[self.activityId]["generic"]

    # time-related utility functions
    def local2ActivityTime(self, timestamp):
        """
        given a local-time timestamp, returns the corresponding
        timestamp relative to the start of the activity
        """
        return timestamp - self.activityStartTime


    def activity2LocalTime(self, timestamp):
        """
        given a activity-time timestamp, returns the corresponding
        local timestamp
        """
        return timestamp + self.activityStartTime


    def getCurrentActivityTime(self):
        return self.local2ActivityTime(globalClock.getFrameTime())


    # disableEmotes and enableEmotes can be overidden by the base
    # classes if different settings are wanted.  But for most
    # party activities, we don't want emotes to be enabled
    # That is, we don't want toons going into different animations when they
    # speedchat...
    def disableEmotes(self):
        Emote.globalEmote.disableAll(base.localAvatar)

    def enableEmotes(self):
        Emote.globalEmote.releaseAll(base.localAvatar)
