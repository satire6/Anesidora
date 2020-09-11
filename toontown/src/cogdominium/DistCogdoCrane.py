from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.fsm import FSM
from direct.distributed import DistributedObject
from direct.showutil import Rope
from direct.showbase import PythonUtil
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPGlobals
from toontown.cogdominium import CogdoCraneGameConsts as GameConsts
import random

class DistCogdoCrane(DistributedObject.DistributedObject, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistCogdoCrane')

    firstMagnetBit = 21

    craneMinY = 8
    craneMaxY = 25

    armMinH = -45
    armMaxH = 45

    # How high to place the shadows.  We can put these pretty high
    # because we play that trick with the bins to make them render
    # after other stuff.
    shadowOffset = 7

    # The properties when the magnet is unencumbered.
    emptyFrictionCoef = 0.1
    emptySlideSpeed = 10     # feet per second
    emptyRotateSpeed = 20    # degrees per second

    # These points will be useful for sticking the control stick into
    # the toon's hands.
    lookAtPoint = Point3(0.3, 0, 0.1)
    lookAtUp = Vec3(0, -1, 0)

    neutralStickHinge = VBase3(0, 90, 0)

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistCogdoCrane')

        self.craneGame = None
        self.index = None
        self.avId = 0
        
        self.cableLength = 20
        self.numLinks = 3
        self.initialArmPosition = (0, 20, 0)

        self.slideSpeed = self.emptySlideSpeed
        self.rotateSpeed = self.emptyRotateSpeed

        # This number increments each time we change direction on the
        # crane controls.  It's used to update the animation
        # appropriately.
        self.changeSeq = 0
        self.lastChangeSeq = 0

        # This is the sound effect currently looping for the crane
        # controls.
        self.moveSound = None

        self.links = []
        self.activeLinks = []
        self.collisions = NodePathCollection()
        self.physicsActivated = 0
        self.snifferActivated = 0
        self.magnetOn = 0
        self.root = NodePath('root')
        self.hinge = self.root.attachNewNode('hinge')
        self.hinge.setPos(0, -17.6, 38.5)
        self.controls = self.root.attachNewNode('controls')
        self.controls.setPos(0, -4.9, 0)
        self.arm = self.hinge.attachNewNode('arm')
        self.crane = self.arm.attachNewNode('crane')
        self.cable = self.hinge.attachNewNode('cable')
        self.topLink = self.crane.attachNewNode('topLink')
        self.topLink.setPos(0, 0, -1)
        self.shadow = None

        # These are goot to pre-compute for __rotateMagnet().
        self.p0 = Point3(0, 0, 0)
        self.v1 = Vec3(1, 1, 1)

        # Smoothers.
        self.armSmoother = SmoothMover()
        self.armSmoother.setSmoothMode(SmoothMover.SMOn)
        self.linkSmoothers = []
        self.smoothStarted = 0
        self.__broadcastPeriod = 0.2

        # Since the cable might not calculate its bounding volume
        # correctly, let's say that anything that passes the outer
        # bounding volume passes everything.
        self.cable.node().setFinal(1)

        self.crane.setPos(*self.initialArmPosition)
        self.heldObject = None

        self.craneAdviceLabel = None
        self.magnetAdviceLabel = None

        self.atLimitSfx = base.loadSfx(
            "phase_4/audio/sfx/MG_cannon_adjust.mp3")

        self.magnetOnSfx = base.loadSfx(
            "phase_10/audio/sfx/CBHQ_CFO_magnet_on.mp3")

        # We prefer a wav file for this looping sound effect, since
        # looping an mp3 always introduces some stutter.
        self.magnetLoopSfx = base.loadSfx(
            "phase_10/audio/sfx/CBHQ_CFO_magnet_loop.wav")

        # Make these overlap just a bit.
        self.magnetSoundInterval = Parallel(
            SoundInterval(self.magnetOnSfx),
            Sequence(Wait(0.5),
                     Func(base.playSfx, self.magnetLoopSfx, looping=1)))

        self.craneMoveSfx = base.loadSfx(
            "phase_9/audio/sfx/CHQ_FACT_elevator_up_down.mp3")

        self.fadeTrack = None

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.name = 'crane-%s' % (self.doId)
        self.root.setName(self.name)

        self.root.setPosHpr(*GameConsts.CranePosHprs[self.index])

        self.rotateLinkName = self.uniqueName('rotateLink')
        self.snifferEvent = self.uniqueName('sniffer')
        self.triggerName = self.uniqueName('trigger')
        self.triggerEvent = 'enter%s' % (self.triggerName)
        self.shadowName = self.uniqueName('shadow')
        self.flickerName = self.uniqueName('flicker')

        self.smoothName = self.uniqueName('craneSmooth')
        self.posHprBroadcastName = self.uniqueName('craneBroadcast')

        self.craneAdviceName = self.uniqueName('craneAdvice')
        self.magnetAdviceName = self.uniqueName('magnetAdvice')

        # Load up the control model and the stick.  We have to do some
        # reparenting so we can set things up to slide and scale
        # pieces around to accomodate toons of various sizes.
        self.controlModel = self.craneGame.controls.copyTo(self.controls)
        self.cc = NodePath('cc')
        column = self.controlModel.find('**/column')
        column.getChildren().reparentTo(self.cc)
        self.cc.reparentTo(column)
        self.stickHinge = self.cc.attachNewNode('stickHinge')
        self.stick = self.craneGame.stick.copyTo(self.stickHinge)
        self.stickHinge.setHpr(self.neutralStickHinge)
        self.stick.setHpr(0, -90, 0)
        self.stick.flattenLight()
        self.bottom = self.controlModel.find('**/bottom')
        self.bottom.wrtReparentTo(self.cc)
        self.bottomPos = self.bottom.getPos()

        # Make a trigger sphere so we can detect when the local avatar
        # runs up to the controls.  We bury the sphere mostly under
        # the floor to minimize accidental collisions.
        cs = CollisionSphere(0, -5, -2, 3)
        cs.setTangible(0)
        cn = CollisionNode(self.triggerName)
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        self.trigger = self.root.attachNewNode(cn)
        self.trigger.stash()

        # Also, a solid tube to keep us from running through the
        # control stick itself.  This one scales with the control
        # model.
        cs = CollisionTube(0, 2.7, 0, 0, 2.7, 3, 1.2)
        cn = CollisionNode('tube')
        cn.addSolid(cs)
        cn.setIntoCollideMask(OTPGlobals.WallBitmask)
        self.tube = self.controlModel.attachNewNode(cn)

        # And finally, a safe-proof bubble we put over the whole thing
        # to keep safes from falling on us while we're on the controls
        # (or from occupying the spot when the controls are vacant).
        cs = CollisionSphere(0, 0, 2, 3)
        cn = CollisionNode('safetyBubble')
        cn.addSolid(cs)
        cn.setIntoCollideMask(ToontownGlobals.PieBitmask)
        self.controls.attachNewNode(cn)

        arm = self.craneGame.craneArm.copyTo(self.crane)

        assert(not self.craneGame.cranes.has_key(self.index))
        self.craneGame.cranes[self.index] = self

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        assert(self.craneGame.cranes.get(self.index) == self)
        del self.craneGame.cranes[self.index]
        self.cleanup()

    def cleanup(self):
        if self.state != 'Off':
            self.demand('Off')
        self.craneGame = None

    def accomodateToon(self, toon):
        # This method has two effects:

        # (1) It computes and returns an interval to scale and slide
        # the crane controls to suit the indicated toon.

        # (2) As a side effect, when it returns, the crane controls are
        # *already* scaled and slid to accomodate the toon, and the toon
        # has been positioned in place to operate the controls.

        # Thus, you can use it either by calling it and playing the
        # interval that it returns to get a smooth lerp, or simply by
        # calling it and ignoring the return value, to jump to
        # position.


        # We start by figuring out where we are going by setting the
        # scale and position appropriately, and then we generate a
        # lerp interval to take us there.
        origScale = self.controlModel.getSz()
        origCcPos = self.cc.getPos()
        origBottomPos = self.bottom.getPos()
        origStickHingeHpr = self.stickHinge.getHpr()
        
        # First, scale the thing overall to match the toon's scale,
        # including cheesy effect scales.
        scale = toon.getGeomNode().getChild(0).getSz(render)
        self.controlModel.setScale(scale)

        # Then get the position of the toon's right hand when he's
        # standing at the controls in a leverNeutral pose.
        self.cc.setPos(0, 0, 0)
        toon.setPosHpr(self.controls, 0, 0, 0, 0, 0, 0)
        toon.pose('leverNeutral', 0)
        toon.update()
        pos = toon.rightHand.getPos(self.cc)

        # Now set the control column to the right height and position
        # to put the top of the stick approximately in his hand.
        self.cc.setPos(pos[0], pos[1], pos[2] - 1)

        # And put the bottom piece back on the floor, wherever that
        # is from here.
        self.bottom.setZ(toon, 0.0)
        self.bottom.setPos(self.bottomPos[0], self.bottomPos[1], self.bottom.getZ())

        # Also put the joystick in his hand.
        self.stickHinge.lookAt(toon.rightHand, self.lookAtPoint, self.lookAtUp)

        # Ok, now we can generate the lerp.
        lerpTime = 0.5
        return Parallel(
            self.controlModel.scaleInterval(lerpTime, scale, origScale, blendType = 'easeInOut'),
            self.cc.posInterval(lerpTime, self.cc.getPos(), origCcPos, blendType = 'easeInOut'),
            self.bottom.posInterval(lerpTime, self.bottom.getPos(), origBottomPos, blendType = 'easeInOut'),
            self.stickHinge.quatInterval(lerpTime, self.stickHinge.getHpr(), origStickHingeHpr, blendType = 'easeInOut'),
            )

    def getRestoreScaleInterval(self):
        # This undoes the effect of accomodateToon(), to restore the
        # controls' scale to neutral position.  Unlike
        # accomodateToon(), it has no side effects; you must play (or
        # immediately finish) the interval to restore the scale.
        
        lerpTime = 1
        return Parallel(
            self.controlModel.scaleInterval(lerpTime, 1, blendType = 'easeInOut'),
            self.cc.posInterval(lerpTime, Point3(0, 0, 0), blendType = 'easeInOut'),
            self.bottom.posInterval(lerpTime, self.bottomPos, blendType = 'easeInOut'),
            self.stickHinge.quatInterval(lerpTime, self.neutralStickHinge, blendType = 'easeInOut'),
            )

    def makeToonGrabInterval(self, toon):
        # Generates an interval showing the crane controls scaling to
        # match the toon and the toon simultaneously reaching to grab
        # the controls.  Thenceforth, the toon will animate with the
        # controls.
        origPos = toon.getPos()
        origHpr = toon.getHpr()
        a = self.accomodateToon(toon)
        newPos = toon.getPos()
        newHpr = toon.getHpr()
        origHpr.setX(PythonUtil.fitSrcAngle2Dest(origHpr[0], newHpr[0]))
        toon.setPosHpr(origPos, origHpr)

        walkTime = 0.2
        reach = ActorInterval(toon, 'leverReach')
        if reach.getDuration() < walkTime:
            reach = Sequence(ActorInterval(toon, 'walk', loop = 1,
                                           duration = walkTime - reach.getDuration()),
                             reach)
            
        i = Sequence(
            Parallel(toon.posInterval(walkTime, newPos, origPos),
                     toon.hprInterval(walkTime, newHpr, origHpr),
                     reach),
            Func(self.startWatchJoystick, toon))
        i = Parallel(i, a)

        return i

    def __toonPlayWithCallback(self, animName, numFrames):
        # Plays the indicated animation on self.toon, and after the
        # indicated time has elapsed calls __toonPlayCallback().

        duration = numFrames / 24.
        self.toon.play(animName)
        taskMgr.doMethodLater(duration, self.__toonPlayCallback,
                              self.uniqueName('toonPlay'))

    def __toonPlayCallback(self, task):
        # The animation has finished playing; play the next one.
        if self.changeSeq == self.lastChangeSeq:
            self.__toonPlayWithCallback('leverNeutral', 40)
        else:
            self.__toonPlayWithCallback('leverPull', 40)
            self.lastChangeSeq = self.changeSeq

    def startWatchJoystick(self, toon):
        self.toon = toon
        taskMgr.add(self.__watchJoystick, self.uniqueName('watchJoystick'))
        self.__toonPlayWithCallback('leverNeutral', 40)

        self.accept(toon.uniqueName('disable'),
                    self.__handleUnexpectedExit, extraArgs = [toon.doId])

    def stopWatchJoystick(self):
        taskMgr.remove(self.uniqueName('toonPlay'))
        taskMgr.remove(self.uniqueName('watchJoystick'))

        if self.toon:
            self.ignore(self.toon.uniqueName('disable'))
        self.toon = None
        
    def __watchJoystick(self, task):
        # Ensure the toon is still standing at the controls.
        self.toon.setPosHpr(self.controls, 0, 0, 0, 0, 0, 0)
        self.toon.update()
        self.stickHinge.lookAt(self.toon.rightHand, self.lookAtPoint,
                               self.lookAtUp)
        return Task.cont

    def __handleUnexpectedExit(self, toonId):
        self.notify.warning('%s: unexpected exit for %s' % (self.doId, toonId))
        if self.toon and self.toon.doId == toonId:
            self.stopWatchJoystick()
        

    def __activatePhysics(self):
        if not self.physicsActivated:
            for an, anp, cnp in self.activeLinks:
                self.craneGame.physicsMgr.attachPhysicalNode(an)
                base.cTrav.addCollider(cnp, self.handler)
            self.collisions.unstash()
            self.physicsActivated = 1

    def __deactivatePhysics(self):
        if self.physicsActivated:
            for an, anp, cnp in self.activeLinks:
                self.craneGame.physicsMgr.removePhysicalNode(an)
                base.cTrav.removeCollider(cnp)
            self.collisions.stash()
            self.physicsActivated = 0

    def __straightenCable(self):
        # Arbitrarily drops the cable right where it stands.
        for linkNum in range(self.numLinks):
            an, anp, cnp = self.activeLinks[linkNum]
            
            an.getPhysicsObject().setVelocity(0, 0, 0)
            z = float(linkNum + 1) / float(self.numLinks) * self.cableLength
            anp.setPos(self.crane.getPos(self.cable))
            anp.setZ(-z)

    def setCableLength(self, length):
        self.cableLength = length
        linkWidth = float(length) / float(self.numLinks)
        self.shell.setRadius(linkWidth + 1)

    def setupCable(self):
        activated = self.physicsActivated
        self.clearCable()

        self.handler = PhysicsCollisionHandler()
        self.handler.setStaticFrictionCoef(0.1)
        self.handler.setDynamicFrictionCoef(self.emptyFrictionCoef)

        linkWidth = float(self.cableLength) / float(self.numLinks)
        self.shell = CollisionInvSphere(0, 0, 0, linkWidth + 1)

        # The list of links is built up to pass to the Rope class, to
        # make a renderable spline for the cable.
        self.links = []
        self.links.append((self.topLink, Point3(0, 0, 0)))

        anchor = self.topLink
        for linkNum in range(self.numLinks):
            anchor = self.__makeLink(anchor, linkNum)

        # Now that we've made a bunch of collisions, stash 'em all
        # (we're initially deactivated).
        self.collisions.stash()

        # Make the magnet swing naturally on the end of the cable.
        self.bottomLink = self.links[-1][0]
        self.middleLink = self.links[-2][0]
        self.magnet = self.bottomLink.attachNewNode('magnet')
        self.wiggleMagnet = self.magnet.attachNewNode('wiggleMagnet')
        taskMgr.add(self.__rotateMagnet, self.rotateLinkName)

        magnetModel = self.craneGame.magnet.copyTo(self.wiggleMagnet)
        magnetModel.setHpr(90, 45, 90)

        # And a node to hold stuff.
        self.gripper = magnetModel.attachNewNode('gripper')
        self.gripper.setPos(0, 0, -4)

        # Not to mention a bubble to detect stuff to grab.
        cn = CollisionNode('sniffer')
        self.sniffer = magnetModel.attachNewNode(cn)
        self.sniffer.stash()
        cs = CollisionSphere(0, 0, -10, 6)
        cs.setTangible(0)
        cn.addSolid(cs)
        cn.setIntoCollideMask(BitMask32(0))
        cn.setFromCollideMask(ToontownGlobals.CashbotBossObjectBitmask)
        self.snifferHandler = CollisionHandlerEvent()
        self.snifferHandler.addInPattern(self.snifferEvent)
        self.snifferHandler.addAgainPattern(self.snifferEvent)

        rope = self.makeSpline()
        rope.reparentTo(self.cable)
        rope.setTexture(self.craneGame.cableTex)

        # Texture coordinates on the cable should be in the range
        # (0.83, 0.01) - (0.98, 0.14).
        ts = TextureStage.getDefault()
        rope.setTexScale(ts, 0.15, 0.13)
        rope.setTexOffset(ts, 0.83, 0.01)

        if activated:
            self.__activatePhysics()

    def clearCable(self):
        self.__deactivatePhysics()
        taskMgr.remove(self.rotateLinkName)
        self.links = []
        self.activeLinks = []
        self.linkSmoothers = []
        self.collisions.clear()
        self.cable.getChildren().detach()
        self.topLink.getChildren().detach()
        self.gripper = None

    def makeSpline(self):
        # Use the Rope class to draw a spline between the joints of
        # the cable.
        
        rope = Rope.Rope()
        rope.setup(min(len(self.links), 4), self.links)
        rope.curve.normalizeKnots()
            
        rn = rope.ropeNode
        rn.setRenderMode(RopeNode.RMTube)
        rn.setNumSlices(3)
        rn.setTubeUp(Vec3(0, -1, 0))
        rn.setUvMode(RopeNode.UVParametric)
        rn.setUvDirection(1)
        rn.setThickness(0.5)

        return rope

    def startShadow(self):
        self.shadow = self.craneGame.geomRoot.attachNewNode('%s-shadow' % (self.name))
        self.shadow.setColor(1, 1, 1, 0.3)
        self.shadow.setDepthWrite(0)
        self.shadow.setTransparency(1)
        self.shadow.setBin('shadow', 0)

        # Hack to fix the bounding volume on the cable.  If it got
        # within the shadow node, render it.
        self.shadow.node().setFinal(1)

        self.magnetShadow = loader.loadModel("phase_3/models/props/drop_shadow")
        self.magnetShadow.reparentTo(self.shadow)

        self.craneShadow = loader.loadModel("phase_3/models/props/square_drop_shadow")
        self.craneShadow.setScale(0.5, 4, 1)
        self.craneShadow.setPos(0, -12, 0)
        self.craneShadow.flattenLight()
        self.craneShadow.reparentTo(self.shadow)

        taskMgr.add(self.__followShadow, self.shadowName)

        rope = self.makeSpline()
        rope.reparentTo(self.shadow)
        rope.setColor(1, 1, 1, 0.2)

        tex = self.craneShadow.findTexture('*')
        rope.setTexture(tex)

        rn = rope.ropeNode
        rn.setRenderMode(RopeNode.RMTape)
        rn.setNumSubdiv(6)
        rn.setThickness(0.8)
        rn.setTubeUp(Vec3(0, 0, 1))
        rn.setMatrix(Mat4.translateMat(0, 0, self.shadowOffset) * Mat4.scaleMat(1, 1, 0.01))
        

    def stopShadow(self):
        if self.shadow:
            self.shadow.removeNode()
            self.shadow = None
            self.magnetShadow = None
            self.craneShadow = None

        taskMgr.remove(self.shadowName)

    def __followShadow(self, task):
        p = self.magnet.getPos(self.craneGame.geomRoot)
        self.magnetShadow.setPos(p[0], p[1], self.shadowOffset)

        self.craneShadow.setPosHpr(self.crane, 0, 0, 0, 0, 0, 0)
        self.craneShadow.setZ(self.shadowOffset)
        
        return Task.cont

    def __makeLink(self, anchor, linkNum):
        an = ActorNode('link%s' % (linkNum))
        anp = NodePath(an)

        cn = CollisionNode('cn')
        sphere = CollisionSphere(0, 0, 0, 1)
        cn.addSolid(sphere)
        cnp = anp.attachNewNode(cn)

        self.handler.addCollider(cnp, anp)

        self.activeLinks.append((an, anp, cnp))
        self.linkSmoothers.append(SmoothMover())

        anp.reparentTo(self.cable)
        z = float(linkNum + 1) / float(self.numLinks) * self.cableLength
        anp.setPos(self.crane.getPos())
        anp.setZ(-z)

        mask = BitMask32.bit(self.firstMagnetBit + linkNum)
        cn.setFromCollideMask(mask)
        cn.setIntoCollideMask(BitMask32(0))

        shellNode = CollisionNode('shell%s' % (linkNum))
        shellNode.addSolid(self.shell)
        shellNP = anchor.attachNewNode(shellNode)
        shellNode.setIntoCollideMask(mask)

        self.collisions.addPath(shellNP)
        self.collisions.addPath(cnp)

        self.links.append((anp, Point3(0, 0, 0)))

        return anp

    def __rotateMagnet(self, task):
        # Rotate the magnet to the penultimate link, so that the
        # magnet seems to swing realistically (instead of always
        # hanging straight down).

        self.magnet.lookAt(self.middleLink, self.p0, self.v1)
        return Task.cont


    def __enableControlInterface(self):
        gui = loader.loadModel("phase_3.5/models/gui/avatar_panel_gui")

        self.accept('control', self.__controlPressed)
        self.accept('control-up', self.__controlReleased)
        self.accept('InputState-forward', self.__upArrow)
        self.accept('InputState-reverse', self.__downArrow)
        self.accept('InputState-turnLeft', self.__leftArrow)
        self.accept('InputState-turnRight', self.__rightArrow)

        taskMgr.add(self.__watchControls, 'watchCraneControls')

        # In case they don't figure it out, hit them over the head
        # with it after a few seconds.
        taskMgr.doMethodLater(5, self.__displayCraneAdvice,
                              self.craneAdviceName)
        taskMgr.doMethodLater(10, self.__displayMagnetAdvice,
                              self.magnetAdviceName)

        # Up in the sky, it's hard to read what people are saying.
        NametagGlobals.setOnscreenChatForced(1)

        self.arrowVert = 0
        self.arrowHorz = 0

    def __disableControlInterface(self):
        self.__turnOffMagnet()

        self.__cleanupCraneAdvice()
        self.__cleanupMagnetAdvice()

        self.ignore('escape')
        self.ignore('control')
        self.ignore('control-up')
        self.ignore('InputState-forward')
        self.ignore('InputState-reverse')
        self.ignore('InputState-turnLeft')
        self.ignore('InputState-turnRight')

        self.arrowVert = 0
        self.arrowHorz = 0

        NametagGlobals.setOnscreenChatForced(0)

        taskMgr.remove('watchCraneControls')
        self.__setMoveSound(None)

    def __displayCraneAdvice(self, task):
        if self.craneAdviceLabel == None:
            self.craneAdviceLabel = DirectLabel(
                text = TTLocalizer.CashbotCraneAdvice,
                text_fg = VBase4(1,1,1,1),
                text_align = TextNode.ACenter,
                relief = None,
                pos = (0, 0, 0.69),
                scale = 0.1)

    def __cleanupCraneAdvice(self):
        if self.craneAdviceLabel:
            self.craneAdviceLabel.destroy()
            self.craneAdviceLabel = None
        taskMgr.remove(self.craneAdviceName)

    def __displayMagnetAdvice(self, task):
        if self.magnetAdviceLabel == None:
            self.magnetAdviceLabel = DirectLabel(
                text = TTLocalizer.CashbotMagnetAdvice,
                text_fg = VBase4(1,1,1,1),
                text_align = TextNode.ACenter,
                relief = None,
                pos = (0, 0, 0.55),
                scale = 0.1)

    def __cleanupMagnetAdvice(self):
        if self.magnetAdviceLabel:
            self.magnetAdviceLabel.destroy()
            self.magnetAdviceLabel = None
        taskMgr.remove(self.magnetAdviceName)

    def __watchControls(self, task):
        if self.arrowHorz or self.arrowVert:
            self.__moveCraneArcHinge(self.arrowHorz, self.arrowVert)
        else:
            self.__setMoveSound(None)
        return Task.cont

    def __incrementChangeSeq(self):
        self.changeSeq = (self.changeSeq + 1) & 0xff

    def __controlPressed(self):
        self.__cleanupMagnetAdvice()
        self.__turnOnMagnet()

    def __controlReleased(self):
        self.__turnOffMagnet()

    def __turnOnMagnet(self):
        if not self.magnetOn:
            self.__incrementChangeSeq()
            self.magnetOn = 1
            if not self.heldObject:
                self.__activateSniffer()

    def __turnOffMagnet(self):
        if self.magnetOn:
            self.magnetOn = 0
            self.__deactivateSniffer()
            self.releaseObject()

    def __upArrow(self, pressed):
        self.__incrementChangeSeq()
        self.__cleanupCraneAdvice()
        if pressed:
            self.arrowVert = 1
        elif self.arrowVert > 0:
            self.arrowVert = 0

    def __downArrow(self, pressed):
        self.__incrementChangeSeq()
        self.__cleanupCraneAdvice()
        if pressed:
            self.arrowVert = -1
        elif self.arrowVert < 0:
            self.arrowVert = 0

    def __rightArrow(self, pressed):
        self.__incrementChangeSeq()
        self.__cleanupCraneAdvice()
        if pressed:
            self.arrowHorz = 1
        elif self.arrowHorz > 0:
            self.arrowHorz = 0

    def __leftArrow(self, pressed):
        self.__incrementChangeSeq()
        self.__cleanupCraneAdvice()
        if pressed:
            self.arrowHorz = -1
        elif self.arrowHorz < 0:
            self.arrowHorz = 0
        
    def __moveCraneArcHinge(self, xd, yd):
        dt = globalClock.getDt()

        h = self.arm.getH() - xd * self.rotateSpeed * dt
        limitH = max(min(h, self.armMaxH), self.armMinH)
        self.arm.setH(limitH)

        y = self.crane.getY() + yd * self.slideSpeed * dt
        limitY = max(min(y, self.craneMaxY), self.craneMinY)

        atLimit = (limitH != h) or (limitY != y)

        if atLimit:
            # Wiggle the crane up and down and left and right to show
            # that it is struggling against its limits of motion.
            now = globalClock.getFrameTime()
            x = math.sin(now * 79) * 0.05
            z = math.sin(now * 70) * 0.02
            self.crane.setPos(x, limitY, z)
            self.__setMoveSound(self.atLimitSfx)

        else:
            self.crane.setPos(0, limitY, 0)
            self.__setMoveSound(self.craneMoveSfx)

    def __setMoveSound(self, sfx):
        # Starts looping the indicated sound effect, or stops it.
        if sfx != self.moveSound:
            if self.moveSound:
                self.moveSound.stop()
            self.moveSound = sfx
            if self.moveSound:
                base.playSfx(self.moveSound, looping=1, volume = 0.5)

    def __activateSniffer(self):
        # Turns on the sniffer on the end of the magnet, looking for
        # something to grab.
        if not self.snifferActivated:
            self.sniffer.unstash()
            base.cTrav.addCollider(self.sniffer, self.snifferHandler)
            self.accept(self.snifferEvent, self.__sniffedSomething)
            self.startFlicker()
            self.snifferActivated = 1
            
    def __deactivateSniffer(self):
        if self.snifferActivated:
            base.cTrav.removeCollider(self.sniffer)
            self.sniffer.stash()
            self.ignore(self.snifferEvent)
            self.stopFlicker()
            self.snifferActivated = 0

    def startFlicker(self):
        # Starts the lightning bolt effect flashing.
        
        self.magnetSoundInterval.start()

        self.lightning = []
        for i in range(4):
            t = (float(i) / 3.0 - 0.5)
            l = self.craneGame.lightning.copyTo(self.gripper)
            l.setScale(random.choice([1, -1]), 1, 5)
            l.setZ(random.uniform(-5, -5.5))
            l.flattenLight()
            l.setTwoSided(1)
            l.setBillboardAxis()
            l.setScale(random.uniform(0.5, 1.0))
            if t < 0:
                l.setX(t - 0.7)
            else:
                l.setX(t + 0.7)
            l.setR(-20 * t)
            l.setP(random.uniform(-20, 20))
            self.lightning.append(l)

        taskMgr.add(self.__flickerLightning, self.flickerName)

    def stopFlicker(self):
        # Stops the lightning bolt effect flashing.  This must pair
        # with a previous call to startFlicker().

        self.magnetSoundInterval.finish()
        self.magnetLoopSfx.stop()

        taskMgr.remove(self.flickerName)
        for l in self.lightning:
            l.detachNode()
        self.lightning = None

    def __flickerLightning(self, task):
        for l in self.lightning:
            if random.random() < 0.5:
                l.hide()
            else:
                l.show()
        return Task.cont

    def __sniffedSomething(self, entry):
        # Something was sniffed as grabbable.
        np = entry.getIntoNodePath()
        doId = int(np.getNetTag('object'))

        obj = base.cr.doId2do.get(doId)
        if obj and obj.state != 'LocalDropped' and \
           (obj.state != 'Dropped' or obj.craneId != self.doId):
            obj.d_requestGrab()
            obj.demand('LocalGrabbed', localAvatar.doId, self.doId)

    def grabObject(self, obj):
        # This is only called by DistributedCashbotBossObject.enterGrabbed().
        assert(self.notify.debug('%s.grabObject(%s)' % (self.doId, obj.doId)))
        assert(self.heldObject == None)

        if self.state == 'Off':
            return

        # This condition is just for sake of the publish, in case we
        # have gotten into some screwy state.  In the dev environment,
        # we should have verified this already with the above
        # assertion.
        if self.heldObject != None:
            self.releaseObject()

        self.__deactivateSniffer()

        obj.wrtReparentTo(self.gripper)

        if obj.lerpInterval:
            obj.lerpInterval.finish()
        
        obj.lerpInterval = Parallel(
            obj.posInterval(ToontownGlobals.CashbotBossToMagnetTime, Point3(*obj.grabPos)),
            obj.quatInterval(ToontownGlobals.CashbotBossToMagnetTime, VBase3(obj.getH(), 0, 0)),
            obj.toMagnetSoundInterval)
        obj.lerpInterval.start()
        
        self.heldObject = obj
        self.handler.setDynamicFrictionCoef(obj.craneFrictionCoef)
        self.slideSpeed = obj.craneSlideSpeed
        self.rotateSpeed = obj.craneRotateSpeed

        if self.avId == localAvatar.doId and not self.magnetOn:
            # We got a late grab.  Grab it, then immediately drop it.
            self.releaseObject()

    def dropObject(self, obj):
        # This is only called by DistributedCashbotBossObject.exitGrabbed().
        assert(self.notify.debug('%s.dropObject(%s)' % (self.doId, obj.doId)))
        assert(self.heldObject == obj)
        assert(not self.snifferActivated)

        if obj.lerpInterval:
            obj.lerpInterval.finish()
        
        obj.wrtReparentTo(render)

        obj.lerpInterval = Parallel(
            obj.quatInterval(ToontownGlobals.CashbotBossFromMagnetTime, VBase3(obj.getH(), 0, 0), blendType = 'easeOut'),
            )
        obj.lerpInterval.start()

        p1 = self.bottomLink.node().getPhysicsObject()
        v = render.getRelativeVector(self.bottomLink, p1.getVelocity())
        obj.physicsObject.setVelocity(v * 1.5)

        # This condition is just for sake of the publish, in case we
        # have gotten into some screwy state.  In the dev environment,
        # we should have verified this already with the above
        # assertion.
        if self.heldObject == obj:
            self.heldObject = None
            self.handler.setDynamicFrictionCoef(self.emptyFrictionCoef)
            self.slideSpeed = self.emptySlideSpeed
            self.rotateSpeed = self.emptyRotateSpeed

    def releaseObject(self):
        # Don't confuse this method with dropObject.  That method
        # implements the object's request to move out of the Grabbed
        # state, and is called only by the object itself, while
        # releaseObject() is called by the crane and asks the object
        # to drop itself, so that the object will set its state
        # appropriately.  A side-effect of this call will be an
        # eventual call to dropObject() by the newly-released object.
        
        assert(self.avId == localAvatar.doId)
        
        if self.heldObject:
            obj = self.heldObject
            obj.d_requestDrop()

            if obj.state == 'Grabbed':
                # Go ahead and move the local object instance into the
                # 'LocalDropped' state--presumably the AI will grant our
                # request shortly anyway, and we can avoid a hitch by
                # not waiting around for it.  However, we can't do
                # this if the object is just in 'LocalGrabbed' state,
                # because we can't start broadcasting updates on the
                # object's position until we *know* we're the object's
                # owner.
                obj.demand('LocalDropped', localAvatar.doId, self.doId)

    def __hitTrigger(self, event):
        #self.d_requestControl()
        pass



    ##### Messages To/From The Server #####

    def setCraneGameId(self, craneGameId):
        self.craneGameId = craneGameId

        # This would be risky if we had toons entering the zone during
        # a battle--but since all the toons are always there from the
        # beginning, we can be confident that the BossCog has already
        # been generated by the time we receive the generate for its
        # associated battles.
        self.craneGame = base.cr.doId2do[craneGameId]

    def setIndex(self, index):
        self.index = index

    def setState(self, state, avId):
        if state == 'C':
            self.demand('Controlled', avId)
        elif state == 'F':
            self.demand('Free')
        else:
            self.notify.error("Invalid state from AI: %s" % (state))

    def d_requestControl(self):
        self.sendUpdate('requestControl')

    def d_requestFree(self):
        self.sendUpdate('requestFree')

    ### Handle smoothing of distributed updates.  This is similar to
    ### code in DistributedSmoothNode, but streamlined for our
    ### purposes.

    def b_clearSmoothing(self):
        self.d_clearSmoothing()
        self.clearSmoothing()
    def d_clearSmoothing(self):
        self.sendUpdate("clearSmoothing", [0])

    def clearSmoothing(self, bogus = None):
        # Call this to invalidate all the old position reports
        # (e.g. just before popping to a new position).
        self.armSmoother.clearPositions(1)
        for smoother in self.linkSmoothers:
            smoother.clearPositions(1)

    def reloadPosition(self):
        """reloadPosition(self)

        This function re-reads the position from the node itself and
        clears any old position reports for the node.  This should be
        used whenever show code bangs on the node position and expects
        it to stick.

        """
        self.armSmoother.clearPositions(0)
        self.armSmoother.setPos(self.crane.getPos())
        self.armSmoother.setHpr(self.arm.getHpr())
        self.armSmoother.setPhonyTimestamp()

        for linkNum in range(self.numLinks):
            smoother = self.linkSmoothers[linkNum]
            an, anp, cnp = self.activeLinks[linkNum]

            smoother.clearPositions(0)
            smoother.setPos(anp.getPos())
            smoother.setPhonyTimestamp()

    def doSmoothTask(self, task):
        """
        This function updates the position of the node to its computed
        smoothed position.  This may be overridden by a derived class
        to specialize the behavior.
        """
        self.armSmoother.computeAndApplySmoothPosHpr(self.crane, self.arm)

        for linkNum in range(self.numLinks):
            smoother = self.linkSmoothers[linkNum]
            anp = self.activeLinks[linkNum][1]
            smoother.computeAndApplySmoothPos(anp)

        return Task.cont

    def startSmooth(self):
        """
        This function starts the task that ensures the node is
        positioned correctly every frame.  However, while the task is
        running, you won't be able to lerp the node or directly
        position it.
        """
        if not self.smoothStarted:
            taskName = self.smoothName
            taskMgr.remove(taskName)
            self.reloadPosition()
            taskMgr.add(self.doSmoothTask, taskName)
            self.smoothStarted = 1

    def stopSmooth(self):
        """
        This function stops the task spawned by startSmooth(), and
        allows show code to move the node around directly.
        """
        if self.smoothStarted:
            taskName = self.smoothName
            taskMgr.remove(taskName)
            self.forceToTruePosition()
            self.smoothStarted = 0


    def forceToTruePosition(self):
        """forceToTruePosition(self)

        This forces the node to reposition itself to its latest known
        position.  This may result in a pop as the node skips the last
        of its lerp points.

        """
        if self.armSmoother.getLatestPosition():
            self.armSmoother.applySmoothPos(self.crane)
            self.armSmoother.applySmoothHpr(self.arm)
        self.armSmoother.clearPositions(1)

        for linkNum in range(self.numLinks):
            smoother = self.linkSmoothers[linkNum]
            an, anp, cnp = self.activeLinks[linkNum]

            if smoother.getLatestPosition():
                smoother.applySmoothPos(anp)
            smoother.clearPositions(1)


    def setCablePos(self, changeSeq, y, h, links, timestamp):
        self.changeSeq = changeSeq
        if self.smoothStarted:
            now = globalClock.getFrameTime()
            local = globalClockDelta.networkToLocalTime(timestamp, now)

            self.armSmoother.setY(y)
            self.armSmoother.setH(h)
            self.armSmoother.setTimestamp(local)
            self.armSmoother.markPosition()

            for linkNum in range(self.numLinks):
                smoother = self.linkSmoothers[linkNum]
                lp = links[linkNum]
                
                smoother.setPos(*lp)
                smoother.setTimestamp(local)
                smoother.markPosition()

        else:
            self.crane.setY(y)
            self.arm.setH(h)

    def d_sendCablePos(self):
        timestamp = globalClockDelta.getFrameNetworkTime()

        links = []
        for linkNum in range(self.numLinks):
            an, anp, cnp = self.activeLinks[linkNum]

            p = anp.getPos()
            links.append((p[0], p[1], p[2]))
        
        self.sendUpdate('setCablePos', [
            self.changeSeq, self.crane.getY(), self.arm.getH(), links, timestamp])

    def stopPosHprBroadcast(self):
        taskName = self.posHprBroadcastName
        taskMgr.remove(taskName)

    def startPosHprBroadcast(self):
        taskName = self.posHprBroadcastName

        # Broadcast our initial position
        self.b_clearSmoothing()
        self.d_sendCablePos()

        # remove any old tasks
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(self.__broadcastPeriod,
                              self.__posHprBroadcast, taskName)

    def __posHprBroadcast(self, task):
        self.d_sendCablePos()
        taskName = self.posHprBroadcastName
        taskMgr.doMethodLater(self.__broadcastPeriod,
                              self.__posHprBroadcast, taskName)
        return Task.done

    ### FSM States ###

    def enterOff(self):
        self.clearCable()
        self.root.detachNode()

    def exitOff(self):
        if self.craneGame:
            self.setupCable()
        self.root.reparentTo(render)

    def enterControlled(self, avId):
        self.avId = avId
        toon = base.cr.doId2do.get(avId)
        if not toon:
            return

        self.grabTrack = self.makeToonGrabInterval(toon)

        if avId == localAvatar.doId:
            # The local toon is beginning to control the crane.

            self.craneGame.toCraneMode()

            camera.reparentTo(self.hinge)
            camera.setPosHpr(0, -20, -5, 0, -20, 0)
            self.tube.stash()

            localAvatar.setPosHpr(self.controls, 0, 0, 0, 0, 0, 0)
            localAvatar.sendCurrentPosition()

            self.__activatePhysics()
            self.__enableControlInterface()
            self.startPosHprBroadcast()
            self.startShadow()

        else:
            self.startSmooth()
            toon.stopSmooth()
            self.grabTrack = Sequence(self.grabTrack,
                                      Func(toon.startSmooth))

        self.grabTrack.start()

    def exitControlled(self):
        self.grabTrack.finish()
        del self.grabTrack

        if self.toon and not self.toon.isDisabled():
            self.toon.loop('neutral')
            self.toon.startSmooth()
        self.stopWatchJoystick()
        
        self.stopPosHprBroadcast()
        self.stopShadow()
        self.stopSmooth()
        
        if self.avId == localAvatar.doId:
            # The local toon is no longer in control of the crane.

            self.__disableControlInterface()
            self.__deactivatePhysics()
            self.tube.unstash()

            camera.reparentTo(base.localAvatar)
            camera.setPos(base.localAvatar.cameraPositions[0][0])
            camera.setHpr(0, 0, 0)

        self.__straightenCable()

    def enterFree(self):
        if self.fadeTrack:
            self.fadeTrack.finish()
            self.fadeTrack = None

        # Wait a few seconds before neutralizing the scale; maybe the
        # same avatar wants to come right back (after his 5-second
        # timeout).
        self.restoreScaleTrack = Sequence(Wait(6),
                                          self.getRestoreScaleInterval())
        self.restoreScaleTrack.start()

        if self.avId == localAvatar.doId:
            # Five second timeout on grabbing the same crane again.  Go
            # get a different crane!
            self.controlModel.setAlphaScale(0.3)
            self.controlModel.setTransparency(1)
            taskMgr.doMethodLater(5, self.__allowDetect, self.triggerName)

            self.fadeTrack = Sequence(
                Func(self.controlModel.setTransparency, 1),
                self.controlModel.colorScaleInterval(0.2, VBase4(1,1,1,0.3)))
            self.fadeTrack.start()

        else:
            # Other players can grab this crane immediately.
            self.trigger.unstash()
            self.accept(self.triggerEvent, self.__hitTrigger)

        self.avId = 0

    def __allowDetect(self, task):
        if self.fadeTrack:
            self.fadeTrack.finish()
        self.fadeTrack = Sequence(
            self.controlModel.colorScaleInterval(0.2, VBase4(1,1,1,1)),
            Func(self.controlModel.clearColorScale),
            Func(self.controlModel.clearTransparency))
        self.fadeTrack.start()

        self.trigger.unstash()
        self.accept(self.triggerEvent, self.__hitTrigger)

    def exitFree(self):
        if self.fadeTrack:
            self.fadeTrack.finish()
            self.fadeTrack = None

        self.restoreScaleTrack.pause() # We just pause, to leave it where it is.
        del self.restoreScaleTrack

        taskMgr.remove(self.triggerName)
        self.controlModel.clearColorScale()
        self.controlModel.clearTransparency()
        
        self.trigger.stash()
        self.ignore(self.triggerEvent)

    def enterMovie(self):
        # This is used to enable a movie mode (particularly for
        # playing the cutscene showing the resistance toon using the
        # crane).  In this mode, lerps on the crane will apply physics
        # to the cable in the expected way.

        self.__activatePhysics()

    def exitMovie(self):
        self.__deactivatePhysics()
        self.__straightenCable()
