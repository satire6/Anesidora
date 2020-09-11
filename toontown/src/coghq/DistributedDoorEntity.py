"""
DistributedEntityDoor module: contains the DistributedCogHqDoor
class, the client side representation of a DistributedCogHqDoorAI.
"""

from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *

from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
import DistributedDoorEntityBase
from direct.fsm import FourState
from direct.fsm import ClassicFSM
from otp.level import DistributedEntity
from toontown.toonbase import TTLocalizer
from otp.level import BasicEntities
from direct.fsm import State
from otp.level import VisibilityBlocker



class DistributedDoorEntityLock(DistributedDoorEntityBase.LockBase, FourState.FourState):
    """
    The Lock is not distributed itself, instead it relies on the door
    to get messages and state changes to and from the server.
    
    This was a nested class in DistributedDoorEntity, but the class 
    reloader that I'm using doesn't work with nested classes.  Until
    that gets changed I've moved this here.
    
    See Also: class DistributedDoorEntity
    """
    slideLeft = Vec3(-7.5, 0.0, 0.0)
    slideRight = Vec3(7.5, 0.0, 0.0)
    
    def __init__(self, door, lockIndex, lockedNodePath, leftNodePath, rightNodePath, stateIndex):
        assert door is not None
        assert 0 <= lockIndex <= 3
        assert not lockedNodePath.isEmpty()
        assert not leftNodePath.isEmpty()
        assert not rightNodePath.isEmpty()
        assert 0 <= stateIndex <= 4

        self.door = door # used in debugPrint.
        self.lockIndex = lockIndex # used in debugPrint.

        self.lockedNodePath = lockedNodePath
        self.leftNodePath = leftNodePath
        self.rightNodePath = rightNodePath
        self.initialStateIndex = stateIndex

        assert(self.debugPrint(
            "Lock(door=%s, lockIndex=%s, lockedNodePath=%s, leftNodePath=%s, rightNodePath=%s, stateIndex=%s)"%
            (door, lockIndex, lockedNodePath, leftNodePath, rightNodePath, stateIndex)))
        FourState.FourState.__init__(self, self.stateNames, self.stateDurations)

    def delete(self):
        self.takedown()
        del self.door
        #FourState.FourState.delete(self)
        #DistributedDoorEntityBase.LockBase.delete(self)
            
    def setup(self):
        assert(self.debugPrint("setup()"))
        self.setLockState(self.initialStateIndex)
        del self.initialStateIndex
            
    def takedown(self):
        assert(self.debugPrint("takedown()"))
        if self.track is not None:
            self.track.pause()
            self.track = None
        for i in self.states.keys():
            del self.states[i]
        self.states = []
        self.fsm = None           

    def setLockState(self, stateIndex):
        assert(self.debugPrint("setLockState(stateIndex=%s)"%(stateIndex,)))
        assert 0 <= stateIndex <= 4
        #self.stateTime = globalClockDelta.localElapsedTime(timeStamp)
        if self.stateIndex != stateIndex:
            state = self.states.get(stateIndex)
            if state is not None:
                self.fsm.request(state)
                #messenger.send(self.getName(), [self.isUnlocked()])
            else:
                assert(self.debugPrint("setLockState() ...State Not Found!"))
        #else:
        #    assert(self.debugPrint("setLockState() ...already in that state."))

    def isUnlocked(self):
        assert(self.debugPrint("isUnlocked() returning %s"%(self.isOn(),)))
        return self.isOn()

    def enterState1(self):
        """
        Animate the lock locking.
        """
        assert self.debugPrint("lockingTrack()")
        FourState.FourState.enterState1(self)
        beat=self.duration*0.05
        slideSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_arms_retracting.mp3")
        self.setTrack(
            Sequence(
                Wait(beat*2.0),
                Parallel(
                    SoundInterval(
                        slideSfx, node=self.door.node, volume=0.8),
                    Sequence(
                        ShowInterval(self.leftNodePath),
                        ShowInterval(self.rightNodePath),
                        Parallel(
                            LerpPosInterval(
                                nodePath=self.leftNodePath,
                                other=self.lockedNodePath,
                                duration=beat*16.0,
                                pos=Vec3(0.0),
                                blendType="easeIn"),
                            LerpPosInterval(
                                nodePath=self.rightNodePath,
                                other=self.lockedNodePath,
                                duration=beat*16.0,
                                pos=Vec3(0.0),
                                blendType="easeIn"),
                            ),
                        HideInterval(self.leftNodePath),
                        HideInterval(self.rightNodePath),
                        ShowInterval(self.lockedNodePath),
                        ),
                    ),
                # fyi: Wait(beat*2),
                )
            )

    def enterState2(self):
        """
        The duration is ignored (it is there to match the interface of
        the other track states).
        
        Setup the animation in the locked position.
        """
        assert self.debugPrint("locked()")
        FourState.FourState.enterState2(self)
        self.setTrack(None)
        self.leftNodePath.setPos(self.lockedNodePath, Vec3(0.0))
        self.rightNodePath.setPos(self.lockedNodePath, Vec3(0.0))
        self.leftNodePath.hide()
        self.rightNodePath.hide()
        self.lockedNodePath.show()

    def enterState3(self):
        """
        Animate the lock unlocking.
        """
        assert self.debugPrint("unlockingTrack()")
        FourState.FourState.enterState3(self)
        unlockSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_unlock.mp3")
        slideSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_arms_retracting.mp3")
        beat=self.duration*0.05
        self.setTrack(
            Sequence(
                Wait(beat*2),
                Parallel(
                    SoundInterval(
                        unlockSfx, node=self.door.node, volume=0.8),
                    SoundInterval(
                        slideSfx, node=self.door.node, volume=0.8),
                    Sequence(
                        HideInterval(self.lockedNodePath),
                        ShowInterval(self.leftNodePath),
                        ShowInterval(self.rightNodePath),
                        Parallel(
                            LerpPosInterval(
                                nodePath=self.leftNodePath,
                                other=self.lockedNodePath,
                                duration=beat*16,
                                pos=self.slideLeft,
                                blendType="easeOut"),
                            LerpPosInterval(
                                nodePath=self.rightNodePath,
                                other=self.lockedNodePath,
                                duration=beat*16,
                                pos=self.slideRight,
                                blendType="easeOut"),
                            ),
                        HideInterval(self.leftNodePath),
                        HideInterval(self.rightNodePath),
                        ),
                    ),
                # fyi: Wait(beat*2),
                )
            )

    def enterState4(self):
        """
        The duration is ignored (it is there to match the interface of
        the other track states).
        
        Setup the animation in the unlocked position.
        """
        assert self.debugPrint("unlocked()")
        FourState.FourState.enterState4(self)
        self.setTrack(None)
        self.leftNodePath.setPos(self.lockedNodePath, self.slideLeft)
        self.rightNodePath.setPos(self.lockedNodePath, self.slideRight)
        self.leftNodePath.hide()
        self.rightNodePath.hide()
        self.lockedNodePath.hide()

    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.door.notify.debug(
                    "%s (%s) %s"%(self.door.__dict__.get('entId', '?'), 
                                  self.lockIndex,
                                  message))



class DistributedDoorEntity(
        DistributedDoorEntityBase.DistributedDoorEntityBase,
        DistributedEntity.DistributedEntity,
        BasicEntities.NodePathAttribsProxy,
        FourState.FourState,
        VisibilityBlocker.VisibilityBlocker):
    """
    DistributedDoorEntity class:  The client side 
    representation of a Cog HQ door.
    
    See Also: "FactoryEntityTypes.py", class DistributedDoorEntityLock
    """
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
                'DistributedDoorEntity')

    def __init__(self, cr):
        """
        constructor for the DistributedDoorEntity
        """
        assert(self.debugPrint("DistributedDoorEntity()"))
        self.innerDoorsTrack = None
        self.isVisReady = 0
        self.isOuterDoorOpen = 0
        DistributedEntity.DistributedEntity.__init__(self, cr)
        FourState.FourState.__init__(self, self.stateNames, self.stateDurations)
        VisibilityBlocker.VisibilityBlocker.__init__(self)
        self.locks = []
        # self.generate will be called automatically.

    def generate(self):
        """
        This method is called when the DistributedDoorEntity is reintroduced
        to the world, either for the first time or from the cache.
        """
        assert(self.debugPrint("generate()"))
        DistributedEntity.DistributedEntity.generate(self)
    
    def announceGenerate(self):
        assert(self.debugPrint("announceGenerate()"))
        self.doorNode = hidden.attachNewNode('door-%s' % self.entId)
        DistributedEntity.DistributedEntity.announceGenerate(self)
        BasicEntities.NodePathAttribsProxy.initNodePathAttribs(self)
        self.setup()
    
    def disable(self):
        assert(self.debugPrint("disable()"))
        self.takedown()
        self.doorNode.removeNode()
        del self.doorNode
        DistributedEntity.DistributedEntity.disable(self)
        #?  BasicEntities.NodePathAttribsProxy.destroy(self)
        # self.delete() will automatically be called.
    
    def delete(self):
        assert(self.debugPrint("delete()"))
        DistributedEntity.DistributedEntity.delete(self)

    def setup(self):
        self.setupDoor()
        for i in self.locks:
            i.setup()
        self.accept("exit%s"%(self.getName(),), self.exitTrigger)
        self.acceptAvatar()
        if __dev__:
            self.initWantDoors()
        
    def takedown(self):
        if __dev__:
            self.shutdownWantDoors()
        #self.ignore("exit%s"%(self.getName(),))
        #self.ignore("enter%s"%(self.getName(),))
        self.ignoreAll()
        if self.track is not None:
            self.track.finish()
        self.track = None
        if self.innerDoorsTrack is not None:
            self.innerDoorsTrack.finish()
        self.innerDoorsTrack = None
        for i in self.locks:
            i.takedown()
        self.locks = []
        self.fsm = None
        for i in self.states.keys():
            del self.states[i]
        self.states = []
    
    # These stubbed out functions are not used on the client (AI Only):
    setUnlock0Event = DistributedDoorEntityBase.stubFunction
    setUnlock1Event = DistributedDoorEntityBase.stubFunction
    setUnlock2Event = DistributedDoorEntityBase.stubFunction
    setUnlock3Event = DistributedDoorEntityBase.stubFunction
    setIsOpenEvent = DistributedDoorEntityBase.stubFunction
    setIsLock0Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock1Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock2Unlocked = DistributedDoorEntityBase.stubFunction
    setIsLock3Unlocked = DistributedDoorEntityBase.stubFunction
    setIsOpen = DistributedDoorEntityBase.stubFunction
    setSecondsOpen = DistributedDoorEntityBase.stubFunction
            
    def acceptAvatar(self):
        self.accept("enter%s"%(self.getName(),), self.enterTrigger)
        #self.acceptOnce("enter%s"%(self.getName(),), self.enterTrigger)
    
    def rejectInteract(self):
        DistributedEntity.DistributedEntity.rejectInteract(self)
        self.acceptAvatar()

    def avatarExit(self, avatarId):
        DistributedEntity.DistributedEntity.avatarExit(self, avatarId)
        self.acceptAvatar()
    
    def enterTrigger(self, args=None):
        assert(self.debugPrint("enterTrigger(args="+str(args)+")"))
        messenger.send("DistributedInteractiveEntity_enterTrigger")
        # This might be a good spot to add a door sound effect.
        self.sendUpdate("requestOpen")
        # the AI server will not reply directly.  We may get a fsm opening
        # state that could be a result of this call or something else.
    
    def exitTrigger(self, args=None):
        assert(self.debugPrint("exitTrigger(args="+str(args)+")"))
        messenger.send("DistributedInteractiveEntity_exitTrigger")

    def okToUnblockVis(self):
        assert(self.debugPrint("okToUnblockVis()"))
        VisibilityBlocker.VisibilityBlocker.okToUnblockVis(self)
        self.isVisReady = 1
        self.openInnerDoors()
    
    def changedOnState(self, isOn):
        assert(self.debugPrint("changedOnState(isOn=%s)"%(isOn,)))
        # The open state is the inverse of the FourState's On value.
        messenger.send(self.getOutputEventName(), [not isOn])
    
    def setLocksState(self, stateBits):
        """
        stateBits:
            15 through 12: lock 3 state
            11 through  8: lock 2 state
             7 through  4: lock 1 state
             3 through  0: lock 0 state

        Set the state for all four locks.
        Required dc field.
        """
        assert(self.debugPrint("setLocksState(stateBits=0x%x)"%(stateBits)))
        lock0 =  stateBits & 0x0000000f
        lock1 = (stateBits & 0x000000f0) >>  4
        lock2 = (stateBits & 0x00000f00) >>  8
        #lock3 = (stateBits & 0x0000f000) >> 12 # fourth lock not yet used.
        if self.isGenerated():
            self.locks[0].setLockState(lock0)
            self.locks[1].setLockState(lock1)
            self.locks[2].setLockState(lock2)
            #self.locks[3].setLockState(lock3) # fourth lock not yet used.
        else:            
            self.initialLock0StateIndex = lock0
            self.initialLock1StateIndex = lock1
            self.initialLock2StateIndex = lock2
            #self.initialLock3StateIndex = lock3 # fourth lock not yet used.
    
    def setDoorState(self, stateIndex, timeStamp):
        """
        Required dc field.
        """
        assert(self.debugPrint("setDoorState(stateIndex=%s, timeStamp=%s)"%(stateIndex, timeStamp)))
        assert 0 <= stateIndex <= 4
        self.stateTime = globalClockDelta.localElapsedTime(timeStamp)
        if self.isGenerated():
            if self.stateIndex != stateIndex:
                state = self.states.get(stateIndex)
                if state is not None:
                    self.fsm.request(state)
                else:
                    assert(self.debugPrint("setDoorState() ...invalid state (stateIndex=%s)"%(stateIndex,)))
            #else:
            #    assert(self.debugPrint("setDoorState() ...already in that state."))
        else:
            self.initialState=stateIndex
            self.initialStateTimestamp=timeStamp
    
    def getName(self):
        return "switch-%s"%str(self.entId)

    def getNodePath(self):
        if hasattr(self, 'doorNode'):
            return self.doorNode
        return None
    
    def setupDoor(self):
        assert(self.debugPrint("setupDoor()"))
        model=loader.loadModel("phase_9/models/cogHQ/CogDoorHandShake")
        assert not model.isEmpty()
        if model:
            doorway = model.find("**/Doorway1")
            assert not doorway.isEmpty()

            rootNode=self.doorNode.attachNewNode(self.getName()+"-root")           
            rootNode.setPos(self.pos)
            rootNode.setHpr(self.hpr)
            rootNode.setScale(self.scale)
            rootNode.setColor(self.color)

            change=rootNode.attachNewNode("changePos")
            #change.setPos(0.0, 0.0, 0.0)
            #change.setHpr(0.0, 0.0, 0.0)
            #change.setScale(0.5, 0.5, 0.5)
            #change.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
            doorway.reparentTo(change)

            self.node=rootNode
            self.node.show()

            self.locks.append(DistributedDoorEntityLock(
                    self,
                    0,
                    doorway.find("**/Slide_One_Closed"),
                    doorway.find("**/Slide_One_Left_Open"),
                    doorway.find("**/Slide_One_Right_Open"),
                    self.initialLock0StateIndex))
            self.locks.append(DistributedDoorEntityLock(
                    self,
                    1,
                    doorway.find("**/Slide_Two_Closed"),
                    doorway.find("**/Slide_Two_Left_Open"),
                    doorway.find("**/Slide_Two_Right_Open"),
                    self.initialLock1StateIndex))
            self.locks.append(DistributedDoorEntityLock(
                    self,
                    2,
                    doorway.find("**/Slide_Three_Closed"),
                    doorway.find("**/Slide_Three_Left_Open"),
                    doorway.find("**/Slide_Three_Right_Open"),
                    self.initialLock2StateIndex))
            del self.initialLock0StateIndex
            del self.initialLock1StateIndex
            del self.initialLock2StateIndex
            #del self.initialLock3StateIndex # fourth lock not yet used.

            # Top Door:
            door = doorway.find("doortop")
            if door.isEmpty(): #Hack#*#
                print "doortop hack"
                door = doorway.attachNewNode("doortop")
                doorway.find("doortop1").reparentTo(door)
                doorway.find("doortop2").reparentTo(door)
            assert not door.isEmpty()

            rootNode=self.doorNode.attachNewNode(self.getName()+"-topDoor")           
            rootNode.setPos(self.pos)
            rootNode.setHpr(self.hpr)
            rootNode.setScale(self.scale)
            rootNode.setColor(self.color)

            change=rootNode.attachNewNode("changePos")
            #change.setPos(0.0, 0.0, 0.0)
            #change.setHpr(0.0, 0.0, 0.0)
            #change.setScale(1.0, 0.8, 1.0)
            #change.setColor(Vec4(0.9, 0.9, 0.9, 1.0))
            door.reparentTo(change)

            self.doorTop=rootNode
            self.doorTop.show()

            # Left Door:
            rootNode=self.doorTop.getParent().attachNewNode(self.getName()+"-leftDoor")           
            change=rootNode.attachNewNode("change")
            door = doorway.find("**/doorLeft")
            assert not door.isEmpty()
            door = door.reparentTo(change)

            self.doorLeft=rootNode
            self.doorLeft.show()
            
            change.setPos(self.pos)
            change.setHpr(self.hpr)
            change.setScale(self.scale)
            change.setColor(self.color)

            # Bottom Door:
            door = doorway.find("doorbottom")
            if door.isEmpty(): #Hack#*#
                print "doorbottom hack"
                door = doorway.attachNewNode("doorbottom")
                doorway.find("doorbottom1").reparentTo(door)
                doorway.find("doorbottom2").reparentTo(door)
            assert not door.isEmpty()

            change=render.attachNewNode("changePos")
            #change.setPos(0.0, 0.0, 0.0)
            #change.setHpr(0.0, 0.0, 0.0)
            #change.setScale(1.0, 0.8, 1.0)
            #change.setColor(Vec4(0.9, 0.9, 0.9, 1.0))
            
            door.reparentTo(change)

            rootNode=self.doorNode.attachNewNode(self.getName()+"-bottomDoor")           
            rootNode.setPos(self.pos)
            rootNode.setHpr(self.hpr)
            rootNode.setScale(self.scale)
            rootNode.setColor(self.color)

            change.reparentTo(rootNode)

            self.doorBottom=rootNode
            self.doorBottom.show()

            # Right Door:
            rootNode=self.doorTop.getParent().attachNewNode(self.getName()+"-rightDoor")           
            change=rootNode.attachNewNode("change")
            door = doorway.find("**/doorRight")
            assert not door.isEmpty()
            door = door.reparentTo(change)

            self.doorRight=rootNode
            self.doorRight.show()
            
            change.setPos(self.pos)
            change.setHpr(self.hpr)
            change.setScale(self.scale)
            change.setColor(self.color)

            if 1:
                # Name Collisions:
                collision = self.doorLeft.find("**/doorLeft_collision1")
                assert not collision.isEmpty()
                collision.setName(self.getName())
                collision = self.doorLeft.find("**/doorLeft_collision2")
                assert not collision.isEmpty()
                collision.setName(self.getName())
                collision = self.doorRight.find("**/doorRight_collision1")
                assert not collision.isEmpty()
                collision.setName(self.getName())
                collision = self.doorRight.find("**/doorRight_collision2")
                assert not collision.isEmpty()
                collision.setName(self.getName())
                # Name Inner Collisions:
                collision = self.doorLeft.find("**/doorLeft_innerCollision")
                assert not collision.isEmpty()
                collision.setName(self.getName())
                self.leftInnerCollision = collision
                collision = self.doorRight.find("**/doorRight_innerCollision")
                assert not collision.isEmpty()
                collision.setName(self.getName())
                self.rightInnerCollision = collision
            elif 0:
                # Add Collision Flat:
                size = 15,.0
                cSphere = CollisionPolygon(
                    Point3(-7.5,-3,15.0),
                    Point3(7.5,-3,15.0),
                    Point3(7.5,-3,0),
                    Point3(-7.5,-3,0))
                cSphere.setTangible(0)
                cSphereNode = CollisionNode(self.getName())
                cSphereNode.addSolid(cSphere)
                cSphereNode.setFromCollideMask(BitMask32.allOff())
                cSphereNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
                self.cSphereNodePath = self.node.attachNewNode(cSphereNode)
                self.cSphereNodePath.show()
            else:
                # Add Collision Sphere:
                radius = 8.0
                cSphere = CollisionSphere(0.0, 0.0, 0.0, radius)
                cSphere.setTangible(0)
                cSphereNode = CollisionNode(self.getName())
                cSphereNode.addSolid(cSphere)
                cSphereNode.setFromCollideMask(BitMask32.allOff())
                cSphereNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
                self.cSphereNodePath = self.node.attachNewNode(cSphereNode)
                #self.cSphereNodePath.show()
            
            if 1:
                # Flatten for speed and to avoid scale changes when reparenting:
                self.node.flattenMedium()
                self.doorTop.flattenMedium()
                self.doorBottom.flattenMedium()
                self.doorLeft.flattenMedium()
                self.doorRight.flattenMedium()
        self.setDoorState(self.initialState, self.initialStateTimestamp)
        del self.initialState
        del self.initialStateTimestamp
    
    def setInnerDoorsTrack(self, track):
        assert(self.debugPrint("setTrack(track=%s)"%(track,)))
        if self.innerDoorsTrack is not None:
            self.innerDoorsTrack.pause()
            self.innerDoorsTrack = None
        if track is not None:
            track.start(0.0) # The inner doors are local, so they start at 0.0.
            self.innerDoorsTrack = track
    
    def openInnerDoors(self):
        """
        Animate the door opening.
        """
        print("openInnerDoors")
        assert(self.debugPrint("openInnerDoors() self.isVisBlocker=%s, self.isVisReady=%s, self.isOuterDoorOpen=%s"%(
            self.isVisBlocker, self.isVisReady, self.isOuterDoorOpen)))
        if (not self.level.complexVis()) or (self.isOuterDoorOpen and (not self.isVisBlocker or self.isVisReady)):
            print("openInnerDoors stage Two")
            duration=self.duration
            slideSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3")
            finalSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3")
            # Each door is 7.5 high, we move them a bit more and then hide them:
            moveDistance=8.0
            self.setInnerDoorsTrack(
                Sequence(
                    Func(self.leftInnerCollision.unstash),
                    Func(self.rightInnerCollision.unstash),
                    Parallel(                    
                        SoundInterval(
                            slideSfx, node=self.node, duration=duration*.4, volume=0.8),
                        LerpPosInterval(
                            nodePath=self.doorLeft,
                            duration=duration*.4,
                            pos=Vec3(-moveDistance, 0.0, 0.0),
                            blendType="easeOut"),
                        LerpPosInterval(
                            nodePath=self.doorRight,
                            duration=duration*.4,
                            pos=Vec3(moveDistance, 0.0, 0.0),
                            blendType="easeOut"),
                        Sequence(
                            Wait(duration*.375),
                            SoundInterval(
                                finalSfx, node=self.node, duration=1.0, volume=0.8),
                            ),
                        ),
                    Func(self.doorLeft.stash),
                    Func(self.doorRight.stash),
                    # fyi: Wait(duration*.6),
                    )
                )
        else:
            pass
            #import pdb; pdb.set_trace()
    
    def closeInnerDoors(self):
        """
        Animate the door opening.
        """
        assert(self.debugPrint("closeInnerDoors()"))
        duration=self.duration
        slideSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3")
        finalSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3")
        # Each door is 7.5 high, we move them a bit more and then hide them:
        moveDistance=8.0
        self.setInnerDoorsTrack(
            Sequence(
                Func(self.doorLeft.unstash),
                Func(self.doorRight.unstash),
                Parallel(
                    SoundInterval(
                        slideSfx, node=self.node, duration=duration*.4, volume=0.8),
                    LerpPosInterval(
                        nodePath=self.doorLeft,
                        duration=duration*.4,
                        pos=Vec3(0.0),
                        blendType="easeIn"),
                    LerpPosInterval(
                        nodePath=self.doorRight,
                        duration=duration*.4,
                        pos=Vec3(0.0),
                        blendType="easeIn"),
                    Sequence(
                        Wait(duration*.375),
                        SoundInterval(
                            finalSfx, node=self.node, duration=1.0, volume=0.8),
                        ),
                    ),
                Func(self.leftInnerCollision.stash),
                Func(self.rightInnerCollision.stash),
                # fyi: Wait(duration*.6),
                )
            )
    
    def setisOuterDoorOpen(self, isOpen):
        self.isOuterDoorOpen = isOpen
    
    def enterState1(self):
        print("doors enter state 1")
        """
        Animate the outer door opening.
        """
        assert(self.debugPrint("openingTrack()"))
        FourState.FourState.enterState1(self)
        self.isOuterDoorOpen = 0
        if self.isVisBlocker:
            if not self.isVisReady:
                self.requestUnblockVis()
        else:
            self.okToUnblockVis()
        duration=self.duration
        slideSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3")
        finalSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3")
        # Each door is 7.5 high, we move them a bit more and then hide them:
        moveDistance=8.0
        self.setTrack(
            Sequence(
                Wait(duration*.1),
                Parallel(                    
                    SoundInterval(
                        slideSfx, node=self.node, duration=duration*.4, volume=0.8),
                    LerpPosInterval(
                        nodePath=self.doorTop,
                        duration=duration*.4,
                        pos=Vec3(0.0, 0.0, moveDistance),
                        blendType="easeOut"),
                    LerpPosInterval(
                        nodePath=self.doorBottom,
                        duration=duration*.4,
                        pos=Vec3(0.0, 0.0, -moveDistance),
                        blendType="easeOut"),
                    Sequence(
                        Wait(duration*.375),
                        SoundInterval(
                            finalSfx, node=self.node, duration=1.0, volume=0.8),
                        ),
                    ),
                Func(self.doorTop.stash),
                Func(self.doorBottom.stash),
                Func(self.setisOuterDoorOpen, 1),
                Func(self.openInnerDoors),
                # fyi: Wait(duration*.5),
                )
            )
    
    def enterState2(self):
        """
        Setup the animation in the open position.
        """
        assert(self.debugPrint("openTrack()"))
        FourState.FourState.enterState2(self)
        self.isOuterDoorOpen = 1
        self.setTrack(None)
        moveDistance=7.5
        self.doorTop.setPos(Vec3(0.0, 0.0, moveDistance)),
        self.doorBottom.setPos(Vec3(0.0, 0.0, -moveDistance)),
        self.doorTop.stash()
        self.doorBottom.stash()

        if not self.isVisBlocker or not self.isWaitingForUnblockVis():
            assert(self.debugPrint("openTrack() ...forcing inner doors open."))
            self.setInnerDoorsTrack(None)
            self.doorLeft.setPos(Vec3(-moveDistance, 0.0, 0.0))
            self.doorRight.setPos(Vec3(moveDistance, 0.0, 0.0))
            self.doorLeft.stash()
            self.doorRight.stash()
        # else: let the pending unblock handle the doors.
    
    def exitState2(self):
        assert(self.debugPrint("exitOpenTrack()"))
        FourState.FourState.exitState2(self)
        self.cancelUnblockVis()
    
    def enterState3(self):
        """
        Animate the door closing.
        """
        assert(self.debugPrint("closingTrack()"))
        FourState.FourState.enterState3(self)
        duration=self.duration
        slideSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_sliding.mp3")
        finalSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_door_open_final.mp3")
        self.setTrack(
            Sequence(
                Wait(duration*.1),
                Func(self.closeInnerDoors),
                Wait(duration*.4),
                Func(self.doorTop.unstash),
                Func(self.doorBottom.unstash),
                Parallel(
                    SoundInterval(
                        slideSfx, node=self.node, duration=duration*.4, volume=0.8),
                    LerpPosInterval(
                        nodePath=self.doorTop,
                        #other=self,
                        duration=duration*.4,
                        pos=Vec3(0.0),
                        blendType="easeIn"),
                    LerpPosInterval(
                        nodePath=self.doorBottom,
                        #other=self,
                        duration=duration*.4,
                        pos=Vec3(0.0),
                        blendType="easeIn"),
                    Sequence(
                        Wait(duration*.375),
                        SoundInterval(
                            finalSfx, node=self.node, duration=duration*.4, volume=0.8),
                        ),
                    ),
                Func(self.setisOuterDoorOpen, 0),
                # fyi: Wait(duration*.1), # remaining time
                )
            )
    
    def enterState4(self):
        """
        Setup the animation in the closed position.
        """
        assert(self.debugPrint("closedTrack()"))
        FourState.FourState.enterState4(self)
        self.setisOuterDoorOpen(0)
        self.isVisReady = 0
        self.setTrack(None)
        self.doorTop.unstash()
        self.doorBottom.unstash()
        self.doorTop.setPos(Vec3(0.0))
        self.doorBottom.setPos(Vec3(0.0))

        self.setInnerDoorsTrack(None)
        self.leftInnerCollision.stash()
        self.rightInnerCollision.stash()
        self.doorLeft.unstash()
        self.doorRight.unstash()
        self.doorLeft.setPos(Vec3(0.0))
        self.doorRight.setPos(Vec3(0.0))

    if __debug__:
        def debugPrint(self, message):
            """for debugging"""
            return self.notify.debug(
                    str(self.__dict__.get('entId', '?'))+' '+message)

    if __dev__:
        def initWantDoors(self):
            self.accept('wantDoorsChanged', self.onWantDoorsChanged)
            self.onWantDoorsChanged()

        def shutdownWantDoors(self):
            self.ignore('wantDoorsChanged')

        def onWantDoorsChanged(self):
            if self.level.levelMgrEntity.wantDoors:
                self.getNodePath().unstash()
            else:
                self.getNodePath().stash()

        def attribChanged(self, attrib, value):
            self.takedown()
            self.setup()
