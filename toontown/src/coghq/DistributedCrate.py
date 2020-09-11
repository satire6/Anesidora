
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
from CrateGlobals import *

from direct.showbase.PythonUtil import fitSrcAngle2Dest
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
import MovingPlatform
from direct.task.Task import Task
import DistributedCrushableEntity

class DistributedCrate(DistributedCrushableEntity.DistributedCrushableEntity):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedCrate")
    # keyboard controls
    UP_KEY    = "arrow_up"
    DOWN_KEY  = "arrow_down"
    LEFT_KEY  = "arrow_left"
    RIGHT_KEY = "arrow_right"

    ModelPaths = (
        "phase_9/models/cogHQ/woodCrateB",
        'phase_10/models/cashbotHQ/CBWoodCrate',
        )

    def __init__(self, cr):
        DistributedCrushableEntity.DistributedCrushableEntity.__init__(self, cr)

        # DistributedCrushableEntity inherits from NodePath, but doesn't call
        # NodePath's constructor to avoid multiple calls to it that
        # result from multiple inheritance along the Actor tree
        self.initNodePath()

        self.modelType = 0
        #self.modelPath = "phase_9/models/cogHQ/woodCrateB"
        #self.modelPath = "phase_9/models/cogHQ/metal_crateB"
        self.crate = None
        self.gridSize = 3.0
        self.tContact = 0
        self.tStick = .01
        self.moveTrack = None
        self.avMoveTrack = None
        self.avPushTrack = None        
        self.crate = None
        self.crushTrack = None

        # state of the local toon
        self.isLocalToon = 0
        self.stuckToCrate = 0
        self.upPressed = 0
        self.isPushing = 0

        self.creakSound = loader.loadSfx("phase_9/audio/sfx/CHQ_FACT_crate_effort.mp3")
        self.pushSound = loader.loadSfx("phase_9/audio/sfx/CHQ_FACT_crate_sliding.mp3")
        
    def disable(self):
        self.ignoreAll()
        if self.moveTrack:
            self.moveTrack.pause()
            del self.moveTrack

        if self.avMoveTrack:
            self.avMoveTrack.pause()
            del self.avMoveTrack

        if self.avPushTrack:
            self.avPushTrack.pause()
            del self.avPushTrack

        if self.crate:
            self.crate.destroy()
            del self.crate

        if self.crushTrack:
            self.crushTrack.pause()
            del self.crushTrack

        taskMgr.remove(self.taskName("crushTask"))
        if self.pushable:
            self.__listenForCollisions(0)
            self.ignore("arrow_up")
            self.ignore("arrow_up-up")
            
        DistributedCrushableEntity.DistributedCrushableEntity.disable(self)

    def delete(self):
        DistributedCrushableEntity.DistributedCrushableEntity.delete(self)
        del self.creakSound
        del self.pushSound

    def generateInit(self):
        """generateInit(self)
        This method is called when the DistributedEntity is first introduced
        to the world... Not when it is pulled from the cache.
        """
        DistributedCrushableEntity.DistributedCrushableEntity.generateInit(self)

        # Make a collision sphere
        #self.collSphere = CollisionSphere(0, 0, 0, self.gridSize)
        # Make the sphere intangible
        #self.collSphere.setTangible(0)
        #self.collNode = CollisionNode(self.uniqueName("crateSphere"))
        #self.collNode.setIntoCollideMask(WallBitmask)
        #self.collNode.addSolid(self.collSphere)
        #self.collNodePath = self.crate.attachNewNode(self.collNode)
        #self.collNodePath.hide()
    
    def generate(self):
        """generate(self)
        This method is called when the DistributedEntity is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedCrushableEntity.DistributedCrushableEntity.generate(self)
        # Add a hook looking for collisions with localToon, and call
        # requestGrab.
        #self.accept(self.uniqueName('entercrateSphere'),
        #            self.handleEnterSphere)
        
    def announceGenerate(self):
        # This is called when the DistributedEntity has filled out all the required
        # fields.
        self.notify.debug('announceGenerate')
        DistributedCrushableEntity.DistributedCrushableEntity.announceGenerate(self)

        # Load the model and child it to the nodepath
        self.loadModel()
        self.modCrateCollisions()
        
        if self.pushable:
            self.__listenForCollisions(1)
            self.accept("arrow_up", self.__upKeyPressed)

    def modCrateCollisions(self):
        # make it easier to jump on crates
        # Uniquify the collision name
        cNode = self.find("**/wall")
        cNode.setName(self.uniqueName("crateCollision"))
        cNode.setZ(-.80)

        # duplicate the floor and move it down to crate a
        # catch effect for low-hopped toons
        colNode = self.find("**/collision")
        floor = colNode.find("**/MovingPlatform*")
        floor2 = floor.copyTo(colNode)
        floor2.setZ(-.80)

    def __upKeyPressed(self):
        self.ignore("arrow_up")
        self.accept("arrow_up-up", self.__upKeyReleased)
        self.upPressed = 1

    def __upKeyReleased(self):
        self.ignore("arrow_up-up")
        self.accept("arrow_up", self.__upKeyPressed)
        self.upPressed = 0
        if self.stuckToCrate:
            self.__resetStick()
        
    def loadModel(self):
        # Load the sound effect
        crateModel = loader.loadModel(
            DistributedCrate.ModelPaths[self.modelType])
        self.crate = MovingPlatform.MovingPlatform()
        self.crate.setupCopyModel(self.getParentToken(), crateModel, 'floor')

        # take the scale off of the nodepath and put it on the model
        self.setScale(1.0)
        self.crate.setScale(self.scale)
        self.crate.reparentTo(self)

        # Flatten out any scale on the crate so the moving platform doesn't get cranky
        self.crate.flattenLight()
        

    def setScale(self, scale):
        if self.crate:
            self.crate.setScale(scale)
            
    def __listenForCollisions(self, on):
        if on:
            self.accept(self.uniqueName("entercrateCollision"),
                        self.handleCollision)
        else:
            self.ignore(self.uniqueName("entercrateCollision"))
        
    def setPosition(self, x, y, z):
         self.setPos(x,y,z)
        
    def handleCollision(self, collEntry=None):
        if not self.upPressed:
            return
        # The local toon is colliding with the box.  If he is facing the
        # box, start a timer and after some time start moving the box in
        # the direction the toon is facing
        crateNormal = Vec3(collEntry.getSurfaceNormal(self))
        relativeVec = base.localAvatar.getRelativeVector(self,
                                                         crateNormal)
        relativeVec.normalize()
        worldVec = render.getRelativeVector(self,
                                            crateNormal)
        worldVec.normalize()
        offsetVec = Vec3(base.localAvatar.getPos(render) - self.getPos(render))
        offsetVec.normalize()
        offsetDot = (offsetVec[0] * worldVec[0]) + (offsetVec[1] * worldVec[1])
        self.notify.debug("offsetDot = %s, world = %s, rel = %s" % (offsetDot, worldVec, offsetVec))
        # if the avatar's direction is +- 30 degrees from the normal
        # consider him pushing the crate
        if relativeVec.getY() < -0.7 and offsetDot > .9 and offsetVec.getZ() < .05:
            self.getCrateSide(crateNormal)
            # start a task to make the toon "stick" to the crate
            # until he accumulates enough force to push it.
            self.tContact = globalClock.getFrameTime()
            self.__listenForCollisions(0)
            # before starting the stick task, listen for a
            # keyup event on the up arrow.  this means the user
            # is no longer intersted in pushing this crate
            self.__listenForCancelEvents(1)
            self.__startStickTask(crateNormal, base.localAvatar.getPos(render))

    def setReject(self):
        # AI tells localToon that sent requestPush that it isn't possible to
        # move the crate in this direction.
        self.notify.debug("setReject")
        self.sentRequest = 0

        # Maybe emit a sound here from the toon
        # that indicates that it can't be pushed
        #base.localAvatar.playDialogueForString("!")

        # Unstick the toon
        if self.stuckToCrate:
            self.__resetStick()
        
    def __startStickTask(self, crateNormal, toonPos):
        self.__killStickTask()
        
        # start the stick task
        self.stuckToCrate = 1
        sTask = Task(self.__stickTask)
        sTask.crateNormal = crateNormal
        sTask.toonPos = toonPos
        taskMgr.add(sTask,
                    self.taskName("stickTask"))

    def __killStickTask(self):
        taskMgr.remove(self.taskName("stickTask"))
        
    def __stickTask(self, task):
        tElapsed = globalClock.getFrameTime() - self.tContact
        if tElapsed > self.tStick:
            # The toon is definitely trying to push this block.
            # Tell the AI.
            lToon = base.localAvatar
            self.isLocalToon = 1

            # Set toons pos/hpr relative to crate
            crateNormal = task.crateNormal
            crateWidth = 2.75 * self.scale
            offset = crateWidth + 1.5 + TorsoToOffset[lToon.style.torso]
            newPos = crateNormal * offset

            if self.avPushTrack:
                self.avPushTrack.pause()
            place = base.cr.playGame.getPlace()
            newHpr = CrateHprs[self.crateSide]

            # figure out what heading the toon should start from, to avoid
            # spinning
            h = lToon.getH(self)
            h = fitSrcAngle2Dest(h, newHpr[0])
            startHpr = Vec3(h,0,0)
            
            # put toon perpendicular to crate
            self.avPushTrack = Sequence(
                LerpPosHprInterval(lToon, .25,
                                   newPos, newHpr, startHpr=startHpr,
                                   other = self,
                                   blendType = 'easeInOut'),
                Func(place.fsm.request, 'push'),
                Func(self.__sendPushRequest, task.crateNormal),
                SoundInterval(self.creakSound, node=self))

            self.avPushTrack.start()
            return Task.done
        else:
            # zero out the tangential velocity so the toon
            # doesn't slide off the crate
            pos = task.toonPos
            base.localAvatar.setPos(task.toonPos)
            return Task.cont

    def getCrateSide(self, crateNormal):
        for i in range(len(CrateNormals)):
            # allow for some numerical error
            dotP = CrateNormals[i].dot(crateNormal)
            if dotP > .9:
                self.crateSide = i
        
    def __sendPushRequest(self, crateNormal):
        self.notify.debug("__sendPushRequest")
        if self.crateSide != None:
            self.sentRequest = 1
            self.sendUpdate("requestPush", [self.crateSide])
        else:
            self.notify.debug("didn't send request")

    def __listenForCancelEvents(self, on):
        self.notify.debug("%s, __listenForCancelEvents(%s)" % (self.doId, on))
        if on:
            self.accept("arrow_down", self.__resetStick)
            self.accept("arrow_left", self.__resetStick)
            self.accept("arrow_right", self.__resetStick)
        else:
            self.ignore("arrow_down")
            self.ignore("arrow_left")
            self.ignore("arrow_right")

    def setMoveTo(self,avId,x0,y0,z0,x1,y1,z1):
        self.notify.debug("setMoveTo")
        self.__moveCrateTo(Vec3(x0,y0,z0),Vec3(x1,y1,z1))
        isLocal = (base.localAvatar.doId == avId)
        if (isLocal and self.stuckToCrate) or not isLocal:
            self.__moveAvTo(avId,Vec3(x0,y0,z0),Vec3(x1,y1,z1))

    def __moveCrateTo(self, startPos, endPos):
        if self.moveTrack:
            self.moveTrack.finish()
            self.moveTrack = None

        self.moveTrack = Parallel(Sequence(LerpPosInterval(self,
                                                           T_PUSH,
                                                           endPos,
                                                           startPos=startPos,
                                                           fluid = 1)),
                                  SoundInterval(self.creakSound, node=self),
                                  SoundInterval(self.pushSound, node=self, duration=T_PUSH, volume = .2),
                                  )
        self.moveTrack.start()

    def __moveAvTo(self, avId, startPos, endPos):
        if self.avMoveTrack:
            self.avMoveTrack.finish()
            self.avMoveTrack = None

        av = base.cr.doId2do.get(avId)
        if av:
            # move the avatar in the same direction as the crate.  To
            # make this look smoother for the localToon, we'll use the current
            # pos of our toon as the startPos, instead of using calculated
            # oldToonPos
            avMoveTrack = Sequence()
            moveDir = endPos - startPos

            crateNormal = startPos - endPos
            crateNormal.normalize()
            crateWidth = 2.75 * self.scale
            offset = crateWidth + 1.5 + TorsoToOffset[av.style.torso]
            toonOffset = crateNormal * offset

            # continually lerp the toon to the same position relative to
            # the crate; don't want to deal with problems associated with
            # parenting the Toon to things that might be scaled etc. etc.
            avMoveTrack.append(Sequence(LerpPosInterval(av,
                                                        T_PUSH,
                                                        toonOffset,
                                                        startPos=toonOffset,
                                                        other=self,),
                                        )
                               )
            self.avMoveTrack = avMoveTrack
            self.avMoveTrack.start()

    def __resetStick(self):
        self.notify.debug("__resetStick")
        # reset crate properties
        self.__killStickTask()
        self.__listenForCancelEvents(0)
        self.__listenForCollisions(1)
        self.sendUpdate("setDone")

        # stop push and avMoveTrack and let moveTrack finish on it's own
        if self.avPushTrack:
            self.avPushTrack.pause()
            del self.avPushTrack
            self.avPushTrack = None

        if self.avMoveTrack:
            self.avMoveTrack.pause()
            del self.avMoveTrack
            self.avMoveTrack = None

        base.cr.playGame.getPlace().fsm.request('walk')
        self.crateSide = None
        self.crateNormal = None
        self.isLocalToon = 0
        self.stuckToCrate = 0
        
    def playCrushMovie(self, crusherId, axis):
        self.notify.debug("playCrushMovie")
        taskMgr.remove(self.taskName("crushTask"))
        taskMgr.add(self.crushTask,
                    self.taskName("crushTask"),
                    extraArgs = (crusherId, axis),
                    priority = 25)
        
    def crushTask(self, crusherId, axis):
        crusher = self.level.entities.get(crusherId, None)
        if crusher:
            crusherHeight = crusher.model.getPos(self)[2]
            #crusherHeight = -crusher.model.getPos(crusher)[1]
            maxHeight = self.pos[2] + self.scale
            minHeight = crusher.getPos(self)[2]
            minScale = minHeight/maxHeight
            assert(minHeight < maxHeight)
            self.notify.debug("cHeight= %s" % crusherHeight)
            if crusherHeight < maxHeight and crusherHeight >= minHeight:
                if crusherHeight == minHeight:
                    # once this gets small enough, end the task
                    self.setScale(Vec3(1.2, 1.2, minScale))
                    taskMgr.doMethodLater(2, self.setScale, "resetScale", extraArgs = (1,))
                    return Task.done
                else:
                    k = crusherHeight / maxHeight
                    sx = min(1/k,.2)
                    self.setScale(Vec3(1+sx, 1+sx, k))
        return Task.cont

    def originalTry(self, axis):
        tSquash = .4
        if self.crushTrack:
            self.crushTrack.finish()
            del self.crushTrack
            self.crushTrack = None
            
        self.crushTrack = Sequence(
            LerpScaleInterval(self, tSquash, VBase3(1.2,1.2,.25), blendType = 'easeInOut'),
            LerpColorScaleInterval(self, 2.0, VBase4(1,1,1,0), blendType = 'easeInOut'),
            Wait(2.0),
            LerpScaleInterval(self, 0.1, VBase3(1,1,1), blendType = 'easeInOut'),
            LerpColorScaleInterval(self, 0.1, VBase4(1,1,1,0), blendType = 'easeInOut'),
            )
        self.crushTrack.start()
        #self.crushTrack = Sequence(
        #    LerpScaleInterval(self, tSquash, VBase3(2,2,.05), blendType = 'easeInOut'),
        #   LerpColorScaleInterval(self, 2.0, VBase4(1,1,1,0), blendType = 'easeInOut'),
        #   Func(self.hide))
    
