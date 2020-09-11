#-------------------------------------------------------------------------------
# Contact: Edmundo Ruiz (Schell Games)
# Created: Oct 2008
#
# Purpose: DistributedPartyCannon handles the relationship between a distributed
#          toon and a cannon, including local function such as moving the cannon
#          with the keys/gui and firing the cannon.
#          Note that he Cannon class contains the data/presentation code.
#          Also note that this class doesn't handle the flying toon.
#          DistributedPartyCannonActivity does. 
#-------------------------------------------------------------------------------

from pandac.PandaModules import *

from direct.distributed.DistributedObject import DistributedObject
from direct.task.Task import Task

from toontown.minigame import CannonGameGlobals
from toontown.minigame.CannonGameGlobals import *

from toontown.parties.Cannon import Cannon
from toontown.parties.CannonGui import CannonGui
from toontown.parties import PartyGlobals
from toontown.parties.DistributedPartyCannonActivity import DistributedPartyCannonActivity

# some constants
LAND_TIME = 2

WORLD_SCALE = 2.

GROUND_SCALE = 1.4 * WORLD_SCALE
CANNON_SCALE = 1.0

FAR_PLANE_DIST = 600 * WORLD_SCALE

# lowest point we should allow the toon to fall
# (just in case he doesn't hit the terrain)
GROUND_PLANE_MIN = -15

CANNON_Y = -int((CannonGameGlobals.TowerYRange/2)*1.3)
CANNON_X_SPACING = 12
CANNON_Z = 20

CANNON_ROTATION_MIN = -55
CANNON_ROTATION_MAX = 50
CANNON_ROTATION_VEL = 15.0 # move 15 units every second

ROTATIONCANNON_ANGLE_MIN = 15
CANNON_ANGLE_MAX = 85
CANNON_ANGLE_VEL = 15.0

# send cannon movement messages for the local cannon at this frequency
CANNON_MOVE_UPDATE_FREQ = 0.5

# these determine the range of distances the camera will
# pull back, away from the toon, in-flight
CAMERA_PULLBACK_MIN = 20
CAMERA_PULLBACK_MAX = 40

# this is the maximum offset of the lookAt point, along
# the ground, in a direction perpendicular to the toon's
# flight path
MAX_LOOKAT_OFFSET = 80

# when the toon is this close to the tower (or closer),
# in feet, the camera will pull back, and the lookAt
# point will extend away from the tower (see above)
TOON_TOWER_THRESHOLD = 150

SHADOW_Z_OFFSET = 0.5

TOWER_HEIGHT = 43.85
TOWER_RADIUS = 10.5
BUCKET_HEIGHT = 36 # collide only with the bucket at the top of
                   # the tower, not with the legs

# this is how far away the tower is on the axis that points
# straight out in front of the cannons
TOWER_Y_RANGE = CannonGameGlobals.TowerYRange
# this gets tapered as the tower gets closer to the cannons in Y
TOWER_X_RANGE = int(TOWER_Y_RANGE / 2.)

INITIAL_VELOCITY = 80.0

# this is how fast you have to be falling to generate a whistling sound
WHISTLE_SPEED = INITIAL_VELOCITY * 0.35

class DistributedPartyCannon(DistributedObject, Cannon):
    notify = directNotify.newCategory("DistributedPartyCannon")
    
    LOCAL_CANNON_MOVE_TASK = "localCannonMoveTask"
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        Cannon.__init__(self, parent = self.getParentNodePath())
        
        self.localCannonMoving = False
        self.active = False
        self.activityDoId = 0
        self.activity = None
        self.gui = None # Gui will come from the activity DO
        self.toonInsideAvId = 0
        self.sign = None
        self.controllingToonAvId = None
    
    def generateInit(self):
        self.load()
        self.activate()
        
    def load(self):
        self.notify.debug("load")
        Cannon.load(self, self.uniqueName("Cannon"))
        if base.cr and base.cr.partyManager and base.cr.partyManager.getShowDoid():
            nameText = TextNode('nameText')
            nameText.setCardAsMargin(0.1, 0.1, 0.1, 0.1)
            nameText.setCardDecal(True)
            nameText.setCardColor(1.0, 1.0, 1.0, 0.0)
            r = 232.0 /255.0 
            g = 169.0 / 255.0 
            b = 23.0 / 255.0 
            nameText.setTextColor(r,g,b,1)
            nameText.setAlign(nameText.ACenter)
            nameText.setShadowColor(0, 0, 0, 1)
            #nameText.setBin('fixed')
            nameText.setText(str(self.doId))
            namePlate = self.parentNode.attachNewNode(nameText)
            namePlate.setDepthWrite(0)
            namePlate.setPos(0,0,8)
            namePlate.setScale(3)

        
    def announceGenerate(self):
        # Duplicate the sign:
        self.sign = self.activity.sign.instanceUnderNode(
             self.activity.getParentNodePath(),
             self.uniqueName("sign")
             )
        self.sign.reparentTo(self.activity.getParentNodePath())
        self.sign.setPos(self.parentNode, self.sign.getPos())
        
    def unload(self):
        self.notify.debug("unload")
                   
        if self.gui is not None:
            self.gui.unload()
            del self.gui
            
        Cannon.unload(self)
        
        if self.sign is not None:
            self.sign.removeNode()
            self.sign = None
        
        self.ignoreAll()
    
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
       
    def disable(self):
        self.notify.debug("disable")
        self.ignoreAll()
        self.__disableCannonControl()
        self.setMovie(PartyGlobals.CANNON_MOVIE_CLEAR, 0)
    
    def delete(self):
        self.deactivate()
        self.unload()
        DistributedObject.delete(self)
        
    def destroy(self):
        self.notify.debug("destroy")
        DistributedObject.destroy(self)
    
    # Distributed (required broadcast ram)
    def setPosHpr(self, x, y, z, h, p, r):
        self.parentNode.setPosHpr(x, y, z, h, p, r)
        
    # Distributed (required broadcast ram)
    def setActivityDoId(self, doId):
        self.activityDoId = doId
        self.activity = base.cr.doId2do[doId]
        
        
    def activate(self):
        """
        Display cannon and enable for collisions
        """
        self.accept(self.getEnterCollisionName(),
                    self.__handleToonCollisionWithCannon)
        
        Cannon.show(self)
        
        self.active = True
    
    def deactivate(self):
        """
        Hide cannon and disable collisions.
        """
        self.ignore(self.getEnterCollisionName())
        
        Cannon.hide(self)
        
        self.active = False
    
    # Distributed (broadcast ram)
    def setMovie(self, mode, avId):
        """
        Used to inform the state of this cannon to all clients
        """
        self.notify.debug("%s setMovie(%s, %s)" % (self.doId, avId, mode))

        if mode == PartyGlobals.CANNON_MOVIE_CLEAR:
            # No one is in the cannon; it's available.
            self.setClear()
        elif mode == PartyGlobals.CANNON_MOVIE_FORCE_EXIT:
            self.exitCannon(avId)
            self.setClear()       
        elif mode == PartyGlobals.CANNON_MOVIE_LOAD:
            self.enterCannon(avId)
        elif (mode == PartyGlobals.CANNON_MOVIE_LANDED):
            # Make sure toonHead is hidden.  If someone walks into
            # the zone after we have fired, they will see a setOccupied(avId)
            # message even after the av has left the cannon.
            self.setLanded(avId)
        else:
            self.notify.error("setMovie Unhandled case mode=%d avId=%d" % (mode, avId))

#===============================================================================
# Enter / Exit Cannon
#===============================================================================

    def __handleToonCollisionWithCannon(self, collEntry):
        """
        Handle collision between a toon and a cannon
        If running Toon collides with cannon, they might be able to use the cannon
        """
        self.notify.debug('collEntry: %s' % collEntry)

        if base.cr.playGame.getPlace().getState() == "walk" and self.toonInsideAvId == 0:
            base.cr.playGame.getPlace().setState("activity")
            self.d_requestEnter()
        
    # Distributed (clsend airecv)
    def d_requestEnter(self):
        self.sendUpdate("requestEnter", [])

    # Distributed (broadcast)
    def requestExit(self):
        self.notify.debug('requestExit')
        base.localAvatar.reparentTo(render)
        base.cr.playGame.getPlace().setState("walk")

    def __avatarGone(self,avId):
        # The AI will call setMovie(FORCE_EXIT), too, but we call it first
        # just to be on the safe side, so we don't try to access a
        # non-existent avatar.
        if self.toonInsideAvId == avId:
            self.notify.debug("__avatarGone in if")
            if self.toonInside and not self.toonInside.isEmpty():
                self.removeToonDidNotFire()
            self.setMovie(PartyGlobals.CANNON_MOVIE_CLEAR, 0)
        else:
            self.notify.debug("__avatarGone in else, self.toonInsideAvId=%s avId=%s" % (self.toonInsideAvId, avId))
        
    def enterCannon(self, avId):
        """
        Prepare toon for cannon, make cannon active for movement and firing if
        it's the local toon entering.
        """
        if avId == base.localAvatar.doId:
            # cache the animations we'll use
            # TODO: needs to be moved to distributed party cannon activity
            base.localAvatar.pose('lose', 110)
            base.localAvatar.pose('slip-forward', 25)

            # put toon in cannon
            base.cr.playGame.getPlace().setState('activity')
            base.localAvatar.collisionsOff()
            
            camera.reparentTo(self.barrelNode)
            camera.setPos(0,-2,5)
            camera.setP(-20)
            
            if not self.activity.hasPlayedBefore():
                self.activity.displayRules()
                self.acceptOnce(
                    DistributedPartyCannonActivity.RULES_DONE_EVENT,
                    self.__enableCannonControl
                    )
            else:
                self.__enableCannonControl()
                
            self.controllingToonAvId = avId
        
            
        # Place toon inside cannon
        if self.cr.doId2do.has_key(avId):
            # If the toon exists, look it up
            self.toonInsideAvId = avId
            self.notify.debug("enterCannon self.toonInsideAvId=%d" % self.toonInsideAvId)
            toon = base.cr.doId2do[avId]
            if toon:
                self.acceptOnce(toon.uniqueName('disable'), self.__avatarGone,  extraArgs=[avId])
            
                toon.stopSmooth()
                toon.dropShadow.hide()
                self.placeToonInside(toon)
            else:
                self.__avatarGone(avId)
        else:
            self.notify.warning("Unknown avatar %d in cannon %d" % (avId, self.doId))


    def exitCannon(self, avId):
        """
        The AI is telling us that avId has been sitting in the
        cannon too long without firing.  We'll exit him out now.
        """
        if avId == base.localAvatar.doId:
            self.activity.finishRules()
            self.ignore(DistributedPartyCannonActivity.RULES_DONE_EVENT)

        self.ignoreDisableForAvId(avId)
            
        if self.gui and (avId == base.localAvatar.doId):
            self.gui.unload()
        
        toon = base.cr.doId2do.get(avId)
        if toon and self.getToonInside() == toon:
            self.resetToon()
        else:
            self.notify.debug("not resetting toon, toon=%s, self.getToonInside()=%s" % (toon, self.getToonInside()))
        
    def resetToon(self, pos = None):
        """
        Takes Toon out of cannon and places the toon next to it.
        """
        self.notify.debug("resetToon")
        toon = self.getToonInside()
        toonInsideAvId = self.toonInsideAvId
        self.notify.debug("%d resetToon self.toonInsideAvId=%d" % (self.doId,self.toonInsideAvId))
        self.removeToonDidNotFire()
        self.__setToonUpright(toon, pos)
        
        if toonInsideAvId == base.localAvatar.doId:
            self.notify.debug("%d resetToon toonInsideAvId ==localAvatar.doId" % (self.doId))
            if pos:
                self.notify.debug("toon setting position to %s" % pos)
                base.localAvatar.setPos(pos)
            camera.reparentTo(base.localAvatar)
            base.localAvatar.collisionsOn()             
            base.localAvatar.startPosHprBroadcast()
            base.localAvatar.enableAvatarControls()
            self.notify.debug("currentState=%s, requesting walk" % base.cr.playGame.getPlace().getState())
            base.cr.playGame.getPlace().setState('walk')
            self.notify.debug("after request walk currentState=%s," % base.cr.playGame.getPlace().getState())
        toon.dropShadow.show()
        
        self.d_setLanded()
        
    def __setToonUpright(self, toon, pos=None):
        """
        Straighten up toon.
        """
        if not pos:
            pos = toon.getPos(render)
        
        toon.setPos(render, pos)
        toon.loop('neutral')

        toon.lookAt(self.parentNode)
            
        toon.setP(0)
        toon.setR(0)
        toon.setScale(1,1,1)
        
    def d_setLanded(self):
        # The shooter can tell the server he's landed, and then the server
        # will pass the message along to all the other clients in this zone.
        self.notify.debugStateCall(self)
        if self.toonInsideAvId == base.localAvatar.doId:
            self.sendUpdate("setLanded", [base.localAvatar.doId])

    # Distributed (clsend airecv)
    def setLanded(self, avId):
        self.removeAvFromCannon(avId)
        self.ignoreDisableForAvId(avId)
        pass

    def removeAvFromCannon(self, avId):
        place = base.cr.playGame.getPlace()
        av = base.cr.doId2do.get(avId)
        print("removeAvFromCannon")
        if place:
            # this is crashing LIVE
            if not hasattr(place, 'fsm'):
                return
            placeState = place.fsm.getCurrentState().getName()
            print placeState
            if (placeState != "fishing"):
                if (av != None):
                    av.startSmooth()
                    self.__destroyToonModels(avId)
                    return
                    
        self.notify.debug("%s removeAvFromCannon" % self.doId)
        if (av != None):
            self.notify.debug("%d removeAvFromCannon: destroying toon models" % self.doId)
            # make sure colliion handling is off

            av.resetLOD()
            
            if av == base.localAvatar:
                if place :
                    #place.setState('walk')
                    place.fsm.request("walk")
                else:
                   #av.loop('neutral')
                    pass

            #self.inWater = 0
            av.setPlayRate(1.0, 'run')
            if av.nametag and self.toonHead:
                av.nametag.removeNametag(self.toonHead.tag)
            # this is needed for distributed toons
            if av.getParent().getName() == "toonOriginChange":
                av.wrtReparentTo(render)
                self.__setToonUpright(av)
            if av == base.localAvatar:
                av.startPosHprBroadcast()
            #self.av.setParent(ToontownGlobals.SPRender)
            av.startSmooth()
            av.setScale(1,1,1)
            ## if av == base.localAvatar:
##                 print("enable controls")
##                 try:
##                     base.localAvatar.enableAvatarControls()
##                 except:
##                     self.notify.debug("couldn't enable avatar controls")
            self.ignore(av.uniqueName("disable"))
            self.__destroyToonModels(avId)

    def __destroyToonModels(self,avId):
        av = base.cr.doId2do.get(avId)
        if not av:
            return
        assert(self.notify.debug("__destroyToonModels"))
        if (av != None):
            # show the toons original drop shadows..
            av.dropShadow.show()
            

            self.hitBumper = 0
            self.hitTarget = 0
            self.angularVel = 0
            self.vel = Vec3(0,0,0)
            self.lastVel = Vec3(0,0,0)
            self.lastPos = Vec3(0,0,0)
            self.landingPos = Vec3(0,0,0)
            self.t = 0
            self.lastT = 0
            self.deltaT = 0
            av = None
            self.lastWakeTime = 0
            self.localToonShooting = 0
            
        if (self.toonHead != None):
            self.toonHead.reparentTo(hidden)
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead.delete()
            self.toonHead = None

        self.model_Created = 0
    
    def setClear(self):
        toon = base.cr.doId2do.get(self.toonInsideAvId)
        toonName = "None"
        self.ignoreDisableForAvId(self.toonInsideAvId)
        if toon and self.isToonInside():
            toonName = toon.getName()
            # make sure collision handling is off
            #self.__stopCollisionHandler(toon)
            toon.resetLOD()
            
            toon.setPlayRate(1.0, 'run')

            # this is needed for distributed toons
            if toon.getParent().getName() == "toonOriginChange":
                toon.wrtReparentTo(render)
                self.__setToonUpright(toon)
                
            toon.startSmooth()
            toon.setScale(1,1,1)
            self.ignore(toon.uniqueName("disable"))
            
            if self.toonInsideAvId == base.localAvatar.doId:
                toon.startPosHprBroadcast()
                try:
                    base.localAvatar.enableAvatarControls()
                except:
                    self.notify.warning("couldn't enable avatar controls")
                base.cr.playGame.getPlace().setState("walk")
        else:
            self.notify.debug("setClear in else toon=%s, self.isToonInsde()=%s" % (toonName, self.isToonInside()))
                
        # handle the new fields                
        self.toonInsideAvId = 0
        self.notify.debug("setClear self.toonInsideAvId=%d" % self.toonInsideAvId)
        if self.controllingToonAvId == base.localAvatar.doId:
            self.notify.debug("set_clear turning off cannon control")
            self.__disableCannonControl()
        self.controllingToonAvId = 0
            
#===============================================================================
# Move Cannon
#===============================================================================

    def __enableCannonControl(self):
        """
        Allows/Disallows localAvatar's control of the cannon.
        """
        if not self.gui:
            self.gui = self.activity.gui
        self.gui.load()
        self.gui.enable(timer = PartyGlobals.CANNON_TIMEOUT )
        self.d_setTimeout()
        self.accept(CannonGui.FIRE_PRESSED, self.__handleFirePressed)
        self.__startLocalCannonMoveTask()
        
    # clsend airecv
    def d_setTimeout(self):
        """
        Activates timeout task on the AI side. Called when the gui is activated.
        This happens because rules show up first.
        """
        self.sendUpdate("setTimeout")

    def __disableCannonControl(self):
        if self.gui:
            self.gui.unload()
        self.ignore(CannonGui.FIRE_PRESSED)
        self.__stopLocalCannonMoveTask()
        
    def __startLocalCannonMoveTask(self):
        """
        Starts the cannon move task for the local toon.
        """
        self.localCannonMoving = False

        task = Task(self.__localCannonMoveTask)
        task.lastPositionBroadcastTime = 0.0
        taskMgr.add(task, self.LOCAL_CANNON_MOVE_TASK)

    def __stopLocalCannonMoveTask(self):
        """
        Stops the local avatar from controlling the cannon.
        """
        taskMgr.remove(self.LOCAL_CANNON_MOVE_TASK)
        if self.localCannonMoving:
            self.localCannonMoving = False
            self.stopMovingSound()

    def __localCannonMoveTask(self, task):
        """
        This task moves changes the cannon on the client side. It runs while
        local toon is inside the cannon.
        Returns: Task.cont
        """
        
        # cannon rotation
        rotVel = 0
        if self.gui.leftPressed:
            rotVel += CANNON_ROTATION_VEL
        if self.gui.rightPressed:
            rotVel -= CANNON_ROTATION_VEL
        self.setRotation(self.getRotation() + rotVel * globalClock.getDt())
            
        # cannon barrel angle
        angVel = 0
        if self.gui.upPressed:
            angVel += CANNON_ANGLE_VEL
        if self.gui.downPressed:
            angVel -= CANNON_ANGLE_VEL
        self.setAngle(self.getAngle() + angVel * globalClock.getDt())
        
        if self.hasMoved():
            if not self.localCannonMoving:
                self.localCannonMoving = True
                self.loopMovingSound()
                
            self.updateModel()

            # periodically send a position update broadcast
            if task.time - task.lastPositionBroadcastTime > CANNON_MOVE_UPDATE_FREQ:
                self.notify.debug("Broadcast local cannon %s position" % self.doId)
                task.lastPositionBroadcastTime = task.time
                self.__broadcastLocalCannonPosition()
        elif self.localCannonMoving:
                self.localCannonMoving = False
                self.stopMovingSound()
                
                # Broadcast the final stopped position
                self.__broadcastLocalCannonPosition()
                self.notify.debug("Cannon Rot = %s, Angle = %s" % (self._rotation,
                                                                   self._angle))

        return Task.cont

    # Distributed (clsend airecv)
    def __broadcastLocalCannonPosition(self):
        """
        Broadcast position of local cannon to all clients
        """
        self.d_setCannonPosition(self._rotation, self._angle)
        
    # Distributed (clsend airecv)
    def d_setCannonPosition(self, zRot, angle):
        self.sendUpdate("setCannonPosition", [zRot, angle])

    # Distributed (broadcast ram)
    def updateCannonPosition(self, avId, zRot, angle):
        """
        AI is telling us that the cannon has moved.
        Update all except if the local toon is controlling.
        """
        if avId and avId == self.toonInsideAvId and avId != base.localAvatar.doId:
            self.notify.debug("update cannon %s position zRot = %d, angle = %d" % (self.doId, zRot, angle))
            self.setRotation(zRot)
            self.setAngle(angle)
            self.updateModel()
            
#===============================================================================
# Fire Cannon
#===============================================================================

    def __handleFirePressed(self):
        """
        Event handler called when the fire button or key is pressed.
        """
        self.notify.debug("fire pressed")
        self.__disableCannonControl()
        self.__broadcastLocalCannonPosition()

        # send the 'cannon is lit' message and wait for the server
        # to tell us the time that our cannon will shoot
        # DistributedPartyCannonActivity will take care of the firing
        self.d_setCannonLit(self._rotation, self._angle)
    
    # Distributed (clsend airecv)
    def d_setCannonLit(self, zRot, angle):
        self.sendUpdate("setCannonLit", [zRot, angle])
        
    def fire(self):
        if base.localAvatar.doId == self.controllingToonAvId:
            self.__disableCannonControl()
            self.d_setFired()
        
        self.playFireSequence()
        self.controllingToonAvId = None
    
    # Distributed (clsend airecv)
    def d_setFired(self):
        self.sendUpdate("setFired", [])
    
    def ignoreDisableForAvId(self, avId):
        """Safely ignore the disable for a given avId"""
        toon = base.cr.doId2do.get(avId)
        if toon:
            self.notify.debug("ignoring %s" % toon.uniqueName("disable"))
            self.ignore(toon.uniqueName("disable"))
        else:
            self.notify.debug("ignoring disable-%s" % self.toonInsideAvId)
            self.ignore("disable-%s" % self.toonInsideAvId)
