""" DistributedButton module: contains the DistributedCogHqButton
    class, the client side representation of a DistributedCogHqButtonAI."""

from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *

import MovingPlatform
from toontown.toonbase import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM
import DistributedSwitch
from toontown.toonbase import TTLocalizer

class DistributedButton(DistributedSwitch.DistributedSwitch):
    """
    DistributedButton class:  The client side 
    representation of a Cog HQ button.
    """
    countdownSeconds = 3.0

    def __init__(self, cr):
        assert(self.debugPrint("DistributedButton()"))
        self.countdownTrack = None
        DistributedSwitch.DistributedSwitch.__init__(self, cr)

    def setSecondsOn(self, secondsOn):
        self.secondsOn = secondsOn

    def avatarExit(self, avatarId):
        assert(self.debugPrint("DistributedButton.avatarExit(avatarId=%s)"%(avatarId,)))
        DistributedSwitch.DistributedSwitch.avatarExit(self, avatarId)
        if (self.secondsOn != -1.0
                and self.secondsOn > 0.0
                and self.countdownSeconds > 0.0
                and self.countdownSeconds < self.secondsOn
                and self.fsm.getCurrentState().getName() == 'playing'):
            track = self.switchCountdownTrack()
            if track is not None:
                track.start(0.0)
                #assert self.countdownTrack == None
                self.countdownTrack = track
    
    def setupSwitch(self):
        assert(self.debugPrint("setupSwitch()"))
        model=loader.loadModel('phase_9/models/cogHQ/CogDoor_Button')
        assert not model.isEmpty()
        if model:
            buttonBase = model.find("**/buttonBase")
            assert not buttonBase.isEmpty()

            change=render.attachNewNode("changePos")
            #change.setPos(-17.5, 0.0, 0.0)
            #change.setHpr(0.0, 0.0, 0.0)
            #change.setScale(0.25, 0.25, 0.1)
            #change.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
            buttonBase.reparentTo(change)

            rootNode=render.attachNewNode(self.getName()+"-buttonBase_root")           
            #rootNode.setPos(self.pos)
            #rootNode.setHpr(self.hpr)
            #rootNode.setScale(self.scale)
            #rootNode.setColor(self.color)
            change.reparentTo(rootNode)

            self.buttonFrameNode=rootNode
            self.buttonFrameNode.show()

            button = model.find("**/button")
            assert not button.isEmpty()

            change=render.attachNewNode("change")
            #change.setPos(0.0, 0.0, -0.4)
            #change.setHpr(0.0, 0.0, 0.0)
            #change.setScale(0.25, 0.25, 0.25)
            #change.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
            button.reparentTo(change)

            rootNode=render.attachNewNode(self.getName()+"-button_root")           
            #rootNode.setPos(self.pos)
            #rootNode.setHpr(self.hpr)
            #rootNode.setScale(self.scale)
            rootNode.setColor(self.color)
            change.reparentTo(rootNode)
            
            self.buttonNode=rootNode
            self.buttonNode.show()

            #self.platform = MovingPlatform.MovingPlatform()
            #self.platform.setupEntity(self.entId, self, self.getName())

            self.buttonFrameNode.reparentTo(self)
            self.buttonNode.reparentTo(self)

            if 1:
                radius = 0.5
                cSphere = CollisionSphere(0.0, 0.0, radius, radius)
                cSphere.setTangible(0)
                cSphereNode = CollisionNode(self.getName())
                cSphereNode.addSolid(cSphere)
                #cSphereNode.setFromCollideMask(BitMask32.allOff())
                #cSphereNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
                cSphereNode.setCollideMask(ToontownGlobals.WallBitmask)
                self.cSphereNodePath = rootNode.attachNewNode(cSphereNode)
                #self.cSphereNodePath.show()
            if 1:
                collisionFloor = button.find("**/collision_floor")
                if collisionFloor.isEmpty():
                    # Add Collision Flat:
                    top = 0.475
                    size = 0.5
                    floor = CollisionPolygon(
                        Point3(-size,-size,top),
                        Point3(size,-size,top),
                        Point3(size,size,top),
                        Point3(-size,size,top))
                    floor.setTangible(1)
                    floorNode = CollisionNode("collision_floor")
                    floorNode.addSolid(floor)
                    collisionFloor = button.attachNewNode(floorNode)
                else:
                    change=collisionFloor.getParent().attachNewNode("changeFloor")
                    #change.setPos(-17.5, 0.0, 0.0)
                    #change.setHpr(0.0, 0.0, 0.0)
                    change.setScale(0.5, 0.5, 1.0)
                    #change.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
                    collisionFloor.reparentTo(change)
                collisionFloor.node().setFromCollideMask(BitMask32.allOff())
                collisionFloor.node().setIntoCollideMask(ToontownGlobals.FloorBitmask)

            # Flatten for speed and to avoid scale changes when reparenting:
            #self.platform.flattenMedium()
            # this messes with this entity's position (sets it 0,0,0),
            # which screws up entity parenting
            #self.flattenMedium()
            self.buttonFrameNode.flattenMedium()
            self.buttonNode.flattenMedium()

    def delete(self):
        DistributedSwitch.DistributedSwitch.delete(self)
        #self.platform.destroy()
        #del self.platform
    
    def enterTrigger(self, args=None):
        assert(self.debugPrint("enterTrigger(args="+str(args)+")"))
        DistributedSwitch.DistributedSwitch.enterTrigger(self, args)
    
    def exitTrigger(self, args=None):
        assert(self.debugPrint("exitTrigger(args="+str(args)+")"))
        DistributedSwitch.DistributedSwitch.exitTrigger(self, args)
        
    def switchOnTrack(self):
        """
        Animate the button turning on.
        """
        assert self.debugPrint("switchOnTrack()")
        onSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_switch_pressed.mp3")
        duration = 0.8
        halfDur = duration*0.5
        pos=Vec3(0.0, 0.0, -0.2)
        color=Vec4(0.0, 1.0, 0.0, 1.0)
        track=Sequence(
                Func(self.setIsOn, 1),
                Parallel(
                    SoundInterval(
                        onSfx, node=self.node, volume=0.9),
                    LerpPosInterval(
                        nodePath=self.buttonNode,
                        duration=duration,
                        pos=pos,
                        blendType="easeInOut"),
                    Sequence(
                        Wait(halfDur),
                        # override to counter effects of flattening
                        LerpColorInterval(
                            nodePath=self.buttonNode,
                            duration=halfDur,
                            color=color,
                            override=1,
                            blendType="easeOut")),
                )
            )
        return track
    
    def switchCountdownTrack(self):
        """
        Animate the button turning off.
        """
        assert self.debugPrint("switchCountdownTrack()")
        wait = self.secondsOn - self.countdownSeconds
        countDownSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_switch_depressed.mp3")
        track=Parallel(
                SoundInterval(countDownSfx),
                Sequence( # 3.0 seconds.
                    Wait(wait),
                    Wait(0.5),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=self.color,
                        override=1,
                        blendType="easeIn"),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=Vec4(0.0, 1.0, 0.0, 1.0),
                        override=1,
                        blendType="easeOut"),
                    Wait(0.5),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=self.color,
                        override=1,
                        blendType="easeIn"),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=Vec4(0.0, 1.0, 0.0, 1.0),
                        override=1,
                        blendType="easeOut"),
                    Wait(0.4),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=self.color,
                        override=1,
                        blendType="easeIn"),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=Vec4(0.0, 1.0, 0.0, 1.0),
                        override=1,
                        blendType="easeOut"),
                    Wait(0.3),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=self.color,
                        override=1,
                        blendType="easeIn"),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=Vec4(0.0, 1.0, 0.0, 1.0),
                        override=1,
                        blendType="easeOut"),
                    Wait(0.2),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        color=self.color,
                        override=1,
                        blendType="easeIn"),
                    LerpColorInterval(
                        nodePath=self.buttonNode,
                        duration=0.1,
                        override=1,
                        color=Vec4(0.0, 1.0, 0.0, 1.0),
                        blendType="easeOut"),
                    Wait(0.1),
                    )
                )
        return track
    
    def switchOffTrack(self):
        """
        Animate the button turning off.
        """
        assert self.debugPrint("switchOffTrack()")
        offSfx = base.loadSfx("phase_9/audio/sfx/CHQ_FACT_switch_popup.mp3")
        duration = 1.0
        halfDur = duration*0.5
        pos=Vec3(0.0)
        #pos.addZ(-0.33*self.scale.getZ())
        track=Sequence(
                Parallel(
                    SoundInterval(
                        offSfx, node=self.node, volume=1.0),
                    LerpPosInterval(
                        nodePath=self.buttonNode,
                        #other=avatar,
                        duration=duration,
                        pos=pos,
                        blendType="easeInOut"),
                    Sequence(
                        Wait(halfDur),
                        LerpColorInterval(
                            nodePath=self.buttonNode,
                            duration=halfDur,
                            color=self.color,
                            override=1,
                            blendType="easeIn")),
                ),
                Func(self.setIsOn, 0),
            )
        return track
    
    def exitPlaying(self):
        if self.countdownTrack:
            self.countdownTrack.finish()
        self.countdownTrack = None
        DistributedSwitch.DistributedSwitch.exitPlaying(self)
