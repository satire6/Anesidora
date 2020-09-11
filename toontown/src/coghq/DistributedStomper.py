"""Stomper module: contains the Stomper class"""

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from StomperGlobals import *
from direct.distributed import ClockDelta
from direct.showbase.PythonUtil import lerp
import math
import DistributedCrusherEntity
import MovingPlatform
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from toontown.toonbase import ToontownGlobals

class DistributedStomper(DistributedCrusherEntity.DistributedCrusherEntity):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedStomper')

    stomperSounds = ['phase_4/audio/sfx/CHQ_FACT_stomper_small.mp3',
                     'phase_9/audio/sfx/CHQ_FACT_stomper_med.mp3',
                     'phase_9/audio/sfx/CHQ_FACT_stomper_large.mp3']

    stomperModels = ['phase_9/models/cogHQ/square_stomper',]
    
    
    def __init__(self, cr):
        self.stomperModels = ['phase_9/models/cogHQ/square_stomper',]
        self.lastPos = Point3(0,0,0)
        self.model = None
        self.smokeTrack = None
        self.ival = None
        self.smoke = None
        self.shadow = None
        self.sound = None
        self.crushSurface = None
        self.cogStyle = 0
        self.loaded = 0
        self.crushedList = []
        self.sounds = []
        self.wantSmoke = 1
        self.wantShadow = 1
        self.animateShadow = 1
        # if true, and we're pointing downward, we get rid of the floor
        # collisions on the top of the stomper head so that it doesn't trap
        # the camera above it.
        self.removeHeadFloor = 0
        self.removeCamBarrierCollisions = 0
        for s in self.stomperSounds:
            self.sounds.append(loader.loadSfx(s))
        DistributedCrusherEntity.DistributedCrusherEntity.__init__(self, cr)
        
    def generateInit(self):
        self.notify.debug('generateInit')
        DistributedCrusherEntity.DistributedCrusherEntity.generateInit(self)

    def generate(self):
        self.notify.debug('generate')
        DistributedCrusherEntity.DistributedCrusherEntity.generate(self)
        
    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        DistributedCrusherEntity.DistributedCrusherEntity.announceGenerate(self)
        # at this point all the entity attributes have been initialized
        # we can load the model now.

        self.loadModel()

        # listen for stunned toons so we can disable the stomper collision surface
        #self.accept("toonStunned-" + str(base.localAvatar.doId), self.stashCrushSurface)

    def disable(self):
        self.notify.debug('disable')
        # stop things
        self.ignoreAll()

        if self.ival:
            self.ival.pause()
            del self.ival
            self.ival = None
  
        if self.smokeTrack:
            self.smokeTrack.pause()
            del self.smokeTrack
            self.smokeTrack = None
            
        DistributedCrusherEntity.DistributedCrusherEntity.disable(self)

    def delete(self):
        self.notify.debug('delete')
        # unload things
        self.unloadModel()
        taskMgr.remove(self.taskName("smokeTask"))
        DistributedCrusherEntity.DistributedCrusherEntity.delete(self)

    def loadModel(self):
        self.loaded = 1
        self.stomperModels = ['phase_9/models/cogHQ/square_stomper',]
        if self.cogStyle == 1:
            self.stomperModels = ['phase_11/models/lawbotHQ/LB_square_stomper',]
        self.notify.debug("loadModel")
        shadow = None
        self.sound = self.sounds[self.soundPath]
        # rotate the model to make it vertical or horizontal, and preserve
        # the 'forward' direction of the model as +Y regardless of orientation
        self.rotateNode = self.attachNewNode('rotate')
        stomperModel = loader.loadModel(self.stomperModels[self.modelPath])

        if self.style == 'vertical':
            #self.setHpr(self.hpr[0],-90,self.hpr[2])
            # don't make a moving platform out of the vertical stomper, it seems
            # to work fine as a regular model
            model = stomperModel

            self.rotateNode.setP(-90)
            
            # stash the up/side collisions
            sideList = model.findAllMatches("**/collSide")
            for side in sideList:
                side.stash()
            upList = model.findAllMatches("**/collUp")
            for up in upList:
                up.stash()

            # store the crushSurface so we can stash it when the toon is stunned
            head = model.find("**/head")
            shaft = model.find("**/shaft")
            self.crushSurface = head.find("**/collDownWalls")

            # stash the crush surface on vertical stompers so the stomper collision
            # surface doesn't push the toon sideways before he is squished.  We should
            # probably only do this right before the toon is crushed, since now we have
            # a problem of the toon jumping through the bottom of the stomper
            #self.stashCrushSurface(1)

            # add shadow
            self.shadow = None
            if self.wantShadow:
                shadow = loader.loadModel("phase_3/models/props/square_drop_shadow").getChild(0)
                shadow.setScale(0.3 * self.headScale[0], 0.3 * self.headScale[2], 1)
                shadow.setAlphaScale(.8)
                shadow.flattenMedium()
                shadow.reparentTo(self)
                shadow.setPos(0,0,.025)
                #shadow.setP(90)
                shadow.setTransparency(1)
                self.shadow = shadow

            # we have to explicitly set the normals of the floor polys now
            # since we rotated the thing and the definition of "up" has changed
            floorHeadNp = model.find("**/head_collisions/**/collDownFloor")
            floorHead = floorHeadNp.node()
            if self.removeHeadFloor:
                floorHeadNp.stash()
            else:
                for i in range(floorHead.getNumSolids()):
                    floorHead.modifySolid(i).setEffectiveNormal(Vec3(0.0,-1.0,0.0))

            floorShaft = model.find("**/shaft_collisions/**/collDownFloor").node()
            for i in range(floorShaft.getNumSolids()):
                floorShaft.modifySolid(i).setEffectiveNormal(Vec3(0.0,-1.0,0.0))
                
            # listen for our own stomperClosed event.  we only need to
            # do this for vertical stompers, since the floor is the other
            # "stomping" surface.  horizontal stompers actually need a stomperPair
            # object to listen for this event.
            self.accept(self.crushMsg, self.checkSquashedToon)

        elif self.style == 'horizontal':
            #self.setHpr(self.hpr[0],0,self.hpr[2])
            # create a moving platform out of the floor surfaces
            model = MovingPlatform.MovingPlatform()
            model.setupCopyModel(self.getParentToken(), stomperModel,
                                 'collSideFloor')

            #model.setR(90)
            # move the model up and make the new origin be at the bottom of
            # the stomper head
            head = model.find('**/head')
            head.node().setPreserveTransform(0)
            head.setZ(1.)
            # allow flatten to modify the transforms of our child ModelNodes
            # to compensate for flattening their parents' transforms
            for child in head.findAllMatches('+ModelNode'):
                child.node().setPreserveTransform(ModelNode.PTNet)
            model.flattenLight()
            
            # stash the up/down collisions
            upList = model.findAllMatches("**/collUp")
            for up in upList:
                up.stash()
            downList = model.findAllMatches("**/collDown")
            for down in downList:
                down.stash()
            
            # store the crushSurface so we can stash it when the toon is stunned
            # SDN: maybe we don't want to do this for horizontal stompers
            self.crushSurface = model.find("**/head_collisions/**/collSideWalls")

        # should we get rid of the camera bit on the barrier collisions?
        if self.removeCamBarrierCollisions:
            walls = model.findAllMatches("**/collDownWalls")
            for wall in walls:
                node = wall.node()
                bitmask = node.getIntoCollideMask()
                invBitmask = BitMask32(ToontownGlobals.CameraBitmask)
                invBitmask.invertInPlace()
                bitmask &= invBitmask
                node.setIntoCollideMask(bitmask)

        # scale the shaft and head
        shaft = model.find("**/shaft")
        shaft.setScale(self.shaftScale)
        head.setScale(self.headScale)

        # now that the dimensions are set, we need to get rid of the
        # DCS flag on the shaft so we can flatten the model
        model.find("**/shaft").node().setPreserveTransform(0)
        model.flattenLight()
        self.model = model

        # If the stomper is a switch controlled stomper, put it in it's
        # up state by default
        if self.motion == MotionSwitched:
            self.model.setPos(0,-self.range, 0)
            
        self.model.reparentTo(self.rotateNode)

        if self.wantSmoke:
            self.smoke = loader.loadModel(
                "phase_4/models/props/test_clouds")
            self.smoke.setColor(.8,.7,.5,1)
            self.smoke.setBillboardPointEye()

    def stashCrushSurface(self, isStunned):
        self.notify.debug("stashCrushSurface(%s)" % isStunned)
        # stash the crush surface when the toon is stunned, so he
        # doesn't get pushed around by the stomper
        if self.crushSurface and not self.crushSurface.isEmpty():
            if isStunned:
                self.crushSurface.stash()
            else:
                self.crushSurface.unstash()
            
    def unloadModel(self):
        if self.ival:
            self.ival.pause()
            del self.ival
            self.ival = None
            
        if self.smoke:
            self.smoke.removeNode()
            del self.smoke
            self.smoke = None

        if self.shadow:
            self.shadow.removeNode()
            del self.shadow
            self.shadow = None

        if self.model:
            if isinstance(self.model, MovingPlatform.MovingPlatform):
                self.model.destroy()
            else:
                self.model.removeNode()
            del self.model
            self.model = None

    def sendStompToon(self):
        messenger.send(self.crushMsg)

    def doCrush(self):
        # This function should be called when the stomper is registerd as a crusher
        # with a crushCell.
        self.notify.debug("doCrush, crushedList = %s" % self.crushedList)
        # check crushCell's contents
        for crushableId in self.crushedList:
            crushable = self.level.entities.get(crushableId)
            if crushable:
                if self.style == 'vertical':
                    axis = 2
                else:
                    axis = 0
                # crush the occupant of the crusherCell
                # along the given axis
                crushable.playCrushMovie(self.entId, axis)
        self.crushedList = []
        
    def getMotionIval(self, mode = STOMPER_START):
        if self.range == 0.:
            return (None, 0)
        # we have to return wantSound, because of the one case
        # of a switched stomper, where the motion ival might be a rising motion
        wantSound = self.soundOn
        
        # stomper should hit at t=0
        if self.motion is MotionLinear:
            motionIval = Sequence(
                LerpPosInterval(self.model, self.period/2.,
                                Point3(0,-self.range,0),
                                startPos=Point3(0,0,0),
                                fluid = 1),
                WaitInterval(self.period/4.),
                LerpPosInterval(self.model, self.period/4.,
                                Point3(0,0,0),
                                startPos=Point3(0,-self.range,0),
                                fluid = 1),
                )
        elif self.motion is MotionSinus:
            def sinusFunc(t, self=self):
                # t: 0..1
                # cos(pi) == -1 (hit/down)
                # theta: pi..3*pi
                theta = math.pi + (t * 2.*math.pi)
                # c: -1..1
                c = math.cos(theta)
                # y: 0..-self.range
                self.model.setFluidY((.5 + (c*.5)) * -self.range)
            motionIval = Sequence(
                LerpFunctionInterval(sinusFunc, duration=self.period),
                )
        elif self.motion is MotionSlowFast:
            def motionFunc(t, self=self):
                # t: 0..1
                stickTime = .2
                turnaround = .95
                t = t % 1
                if t < stickTime:
                    self.model.setFluidY(0)
                elif t < turnaround:
                    # t: 0..turnaround
                    self.model.setFluidY((t-stickTime) * -self.range/(turnaround-stickTime))
                elif t > turnaround:
                    # t: turnaround..1
                    self.model.setFluidY(-self.range + (t-turnaround) * self.range/(1-turnaround))
            motionIval = Sequence(
                LerpFunctionInterval(motionFunc, duration=self.period),
                )
        elif self.motion is MotionCrush:
            def motionFunc(t, self=self):
                # t: 0..1
                stickTime = .2
                pauseAtTopTime = .5
                turnaround = .85
                t = t % 1
                if t < stickTime:
                    self.model.setFluidY(0)
                elif t <= turnaround - pauseAtTopTime:
                    # t: 0 ..(turnaround-pauseAtTop)
                    self.model.setFluidY((t-stickTime) * -self.range/(turnaround- pauseAtTopTime - stickTime))
                elif t > (turnaround - pauseAtTopTime) and t <= turnaround:
                    # t: (turnaround-pauseAtTop).. turnaround
                    self.model.setFluidY(-self.range)
                elif t > turnaround:
                    # t: turnaround..1
                    self.model.setFluidY(-self.range + (t-turnaround) * self.range/(1-turnaround))

            tStick = .2 * self.period
            tUp = .45 * self.period
            tPause = .2 * self.period
            tDown = .15 * self.period
            motionIval = Sequence(
                Wait(tStick),
                LerpPosInterval(self.model, tUp,
                                Vec3(0, -self.range, 0),
                                blendType = 'easeInOut',
                                fluid=1),
                Wait(tPause),
                Func(self.doCrush),
                LerpPosInterval(self.model, tDown,
                                Vec3(0, 0, 0),
                                blendType = 'easeInOut',
                                fluid=1),
                )
        elif self.motion is MotionSwitched:
            if mode == STOMPER_STOMP:
                # create a track that forces the stomper to stomp
                # from the current position
                motionIval = Sequence(
                    Func(self.doCrush),
                    LerpPosInterval(self.model, .35,
                                    Vec3(0, 0, 0),
                                    blendType = 'easeInOut',
                                    fluid=1),
                    )
            elif mode == STOMPER_RISE:
                # create a track that forces the stomper to rise
                # from the current position
                motionIval = Sequence(
                    LerpPosInterval(self.model, .5,
                                    Vec3(0, -self.range, 0),
                                    blendType = 'easeInOut',
                                    fluid=1),
                    )
                wantSound = 0
            else:
                # This should only happen when we are editing the stomper
                # in the factory editor.  Otherwise there should not be a
                # time when self.motion == MotionSwitched and mode != (STOMPER_RISE|STOMP)
                motionIval = None
        else:
            def halfSinusFunc(t, self=self):
                # t: 0..1
                self.model.setFluidY(math.sin(t * math.pi) * -self.range)
            motionIval = Sequence(
                LerpFunctionInterval(halfSinusFunc, duration=self.period),
                )
        return (motionIval,wantSound)
    
    def startStomper(self, startTime, mode = STOMPER_START):
        if self.ival:
            self.ival.pause()
            del self.ival
            self.ival = None
            
        # Get the motion track for this stomper
        motionIval,wantSound = self.getMotionIval(mode)

        if motionIval == None:
            # this should only happen in editor mode or if range is zero
            return
        
        # put the motion interval into a Parallel so that we can easily add
        # concurrent ivals on (like sound, etc)
        self.ival = Parallel(
            Sequence(motionIval,
                     Func(self.__startSmokeTask),
                     Func(self.sendStompToon)),
            name=self.uniqueName('Stomper'),
            )

        # 'stomp' sound
        if wantSound:
            # make sure we don't play a sound that's too long; cap the
            # sound length to the motion period
            #if self.soundLen == 0.:
            #    sndDur = motionIval.getDuration()
            #else:
            #    sndDur = min(self.soundLen, motionIval.getDuration())
            #self.ival.append(
            #    SoundInterval(self.sound, duration=sndDur, node=self.model))
            sndDur = motionIval.getDuration()
            self.ival.append(
                Sequence(Wait(sndDur),
                         Func(base.playSfx, self.sound, node=self.model, volume=.45)))
            
        # shadow
        if self.shadow is not None and self.animateShadow:
            def adjustShadowScale(t, self=self):
                # scale the shadow according to the position of the
                # stomper
                modelY = self.model.getY()
                # a=0..1, 0=down, 1=up
                # cap the height, so the shadow disappears for all stompers
                # at the same height
                maxHeight = 10
                a = min(-modelY/maxHeight,1.0)
                self.shadow.setScale(lerp(1, .2, a))
                self.shadow.setAlphaScale(lerp(1,.2, a))
            self.ival.append(
                LerpFunctionInterval(adjustShadowScale, duration=self.period))

        if mode == STOMPER_START:
            self.ival.loop()
            self.ival.setT((globalClock.getFrameTime() - self.level.startTime) +
                           (self.period * self.phaseShift))
        else:
            # we got this message from the AI, so the startTime is
            # the elapsed time since the AI generated the stomp message
            self.ival.start(startTime)
            

    def stopStomper(self):
        if self.ival:
            self.ival.pause()
        if self.smokeTrack:
            self.smokeTrack.finish()
            del self.smokeTrack
            self.smokeTrack = None
            
    def setMovie(self, mode, timestamp, crushedList):
        self.notify.debug("setMovie %d" % mode)
        timestamp = ClockDelta.globalClockDelta.networkToLocalTime(timestamp)
        now = globalClock.getFrameTime()
        
        if (mode == STOMPER_START or
            mode == STOMPER_RISE or
            mode == STOMPER_STOMP):
            # the AI is telling the stomper how to move.
            # STOMPER_START will start a repeating motion
            # STOMPER_RISE/STOMP will force the stomper to rise/stomp
            # from it's current position
            self.crushedList = crushedList
            self.startStomper(timestamp, mode)

    def __startSmokeTask(self):
        taskMgr.remove(self.taskName("smokeTask"))
        if self.wantSmoke:
            taskMgr.add(self.__smokeTask, self.taskName("smokeTask"))
        
    def __smokeTask(self, task):
        # smoke cloud after the cannon fires
        self.smoke.reparentTo(self)
        self.smoke.setScale(1)
        # reparent to render, so the smoke doesn't get darker in the nighttime
        #self.smoke.wrtReparentTo(render)
        if self.smokeTrack:
            self.smokeTrack.finish()
            del self.smokeTrack

        self.smokeTrack = Sequence(Parallel(LerpScaleInterval(self.smoke, .2, Point3(4,1,4)),
                                            LerpColorScaleInterval(self.smoke, 1, Vec4(1,1,1,0))),
                                   Func(self.smoke.reparentTo, hidden),
                                   Func(self.smoke.clearColorScale),
                                   )
        self.smokeTrack.start()
        return Task.done

    def checkSquashedToon(self):
        if self.style == 'vertical':
            # if toon is within a head size of the center of this thing,
            # he is squashed
            tPos = base.localAvatar.getPos(self.rotateNode)
            # Note:  the current model has a head that is 2x2 by default.
            zRange = self.headScale[2]
            xRange = self.headScale[0]
            yRange = 5
            if (tPos[2] < zRange and tPos[2] > -zRange and
                tPos[0] < xRange and tPos[0] > -xRange and
                tPos[1] < yRange/10. and tPos[1] > -yRange):
                #print "(%s) Squashed!! %s" % (self.entId, tPos)
                self.level.b_setOuch(self.damage, 'Squish')
                base.localAvatar.setZ(self.getZ(render)+.025)
            else:
                #print "(%s) toon is far enough away: %s" % (self.entId, tPos)
                pass

    ## Setters
    ## This could be optimized so the whole model doesn't unload and reload
    ## for every changed attribute
    if __dev__:
        def attribChanged(self, *args):
            self.stopStomper()
            self.unloadModel()
            self.loadModel()
            self.startStomper(0)
