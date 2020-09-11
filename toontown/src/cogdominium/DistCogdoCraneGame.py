from pandac import PandaModules as PM
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task.Task import Task
from otp.level import LevelConstants
from otp.otpbase import OTPGlobals
from toontown.cogdominium.DistCogdoLevelGame import DistCogdoLevelGame
from toontown.cogdominium import CogdoCraneGameConsts as GameConsts
from toontown.cogdominium.CogdoCraneGameBase import CogdoCraneGameBase
from toontown.toonbase import ToontownTimer
from toontown.toonbase import TTLocalizer as TTL
from toontown.toonbase import ToontownGlobals

class DistCogdoCraneGame(DistCogdoLevelGame, CogdoCraneGameBase):
    notify = directNotify.newCategory("DistCogdoCraneGame")

    def __init__(self, cr):
        DistCogdoLevelGame.__init__(self, cr)
        self.cranes = {}

    def getTitle(self):
        return TTL.CogdoCraneGameTitle

    def getInstructions(self):
        return TTL.CogdoCraneGameInstructions

    def announceGenerate(self):
        DistCogdoLevelGame.announceGenerate(self)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.stash()
        if __dev__:
            self._durationChangedEvent = self.uniqueName('durationChanged')

    def disable(self):
        self.timer.destroy()
        self.timer = None
        DistCogdoLevelGame.disable(self)

    def enterLoaded(self):
        DistCogdoLevelGame.enterLoaded(self)
        
        self.lightning = loader.loadModel('phase_10/models/cogHQ/CBLightning.bam')
        self.magnet = loader.loadModel('phase_10/models/cogHQ/CBMagnet.bam')
        self.craneArm = loader.loadModel('phase_10/models/cogHQ/CBCraneArm.bam')
        self.controls = loader.loadModel('phase_10/models/cogHQ/CBCraneControls.bam')
        self.stick = loader.loadModel('phase_10/models/cogHQ/CBCraneStick.bam')
        self.cableTex = self.craneArm.findTexture('MagnetControl')

        self.geomRoot = PM.NodePath('geom')
        
        # Set up a physics manager for the cables and the objects
        # falling around in the room.

        self.physicsMgr = PM.PhysicsManager()
        integrator = PM.LinearEulerIntegrator()
        self.physicsMgr.attachLinearIntegrator(integrator)

        fn = PM.ForceNode('gravity')
        self.fnp = self.geomRoot.attachNewNode(fn)
        gravity = PM.LinearVectorForce(0, 0, -32)
        fn.addForce(gravity)
        self.physicsMgr.addLinearForce(gravity)

    def privGotSpec(self, levelSpec):
        DistCogdoLevelGame.privGotSpec(self, levelSpec)

        levelMgr = self.getEntity(LevelConstants.LevelMgrEntId)
        self.endVault = levelMgr.geom
        self.endVault.reparentTo(self.geomRoot)

        # Clear out unneeded backstage models from the EndVault, if
        # they're in the file.
        self.endVault.findAllMatches('**/MagnetArms').detach()
        self.endVault.findAllMatches('**/Safes').detach()
        self.endVault.findAllMatches('**/MagnetControlsAll').detach()

        # Flag the collisions in the end vault so safes and magnets
        # don't try to go through the wall.
        cn = self.endVault.find('**/wallsCollision').node()
        cn.setIntoCollideMask(OTPGlobals.WallBitmask | ToontownGlobals.PieBitmask |
                              (PM.BitMask32.lowerOn(3) << 21))        

        # Find all the wall polygons and replace them with planes,
        # which are solid, so there will be zero chance of safes or
        # toons slipping through a wall.
        walls = self.endVault.find('**/RollUpFrameCillison')
        walls.detachNode()
        self.evWalls = self.replaceCollisionPolysWithPlanes(walls)
        self.evWalls.reparentTo(self.endVault)

        # Initially, these new planar walls are stashed, so they don't
        # cause us trouble in the intro movie or in battle one.  We
        # will unstash them when we move to battle three.
        self.evWalls.stash()

       
        # Also replace the floor polygon with a plane, and rename it
        # so we can detect a collision with it.
        floor = self.endVault.find('**/EndVaultFloorCollision')
        floor.detachNode()
        self.evFloor = self.replaceCollisionPolysWithPlanes(floor)
        self.evFloor.reparentTo(self.endVault)
        self.evFloor.setName('floor')

        # Also, put a big plane across the universe a few feet below
        # the floor, to catch things that fall out of the world.
        plane = PM.CollisionPlane(PM.Plane(PM.Vec3(0, 0, 1), PM.Point3(0, 0, -50)))
        planeNode = PM.CollisionNode('dropPlane')
        planeNode.addSolid(plane)
        planeNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.geomRoot.attachNewNode(planeNode)

    def replaceCollisionPolysWithPlanes(self, model):
        newCollisionNode = PM.CollisionNode('collisions')
        newCollideMask = PM.BitMask32(0)
        planes = []

        collList = model.findAllMatches('**/+CollisionNode')
        if not collList:
            collList = [model]
            
        for cnp in collList:
            cn = cnp.node()
            if not isinstance(cn, PM.CollisionNode):
                self.notify.warning("Not a collision node: %s" % (repr(cnp)))
                break
            
            newCollideMask = newCollideMask | cn.getIntoCollideMask()
            for i in range(cn.getNumSolids()):
                solid = cn.getSolid(i)
                if isinstance(solid, PM.CollisionPolygon):
                    # Save the plane defined by this polygon
                    plane = PM.Plane(solid.getPlane())
                    planes.append(plane)
                else:
                    self.notify.warning("Unexpected collision solid: %s" % (repr(solid)))
                    newCollisionNode.addSolid(plane)

        newCollisionNode.setIntoCollideMask(newCollideMask)
        
        # Now sort all of the planes and remove the nonunique ones.
        # We can't use traditional dictionary-based tricks, because we
        # want to use Plane.compareTo(), not Plane.__hash__(), to make
        # the comparison.
        threshold = 0.1
        planes.sort(lambda p1, p2: p1.compareTo(p2, threshold))
        lastPlane = None
        for plane in planes:
            if lastPlane == None or plane.compareTo(lastPlane, threshold) != 0:
                cp = PM.CollisionPlane(plane)
                newCollisionNode.addSolid(cp)
                lastPlane = plane

        return PM.NodePath(newCollisionNode)

    def exitLoaded(self):
        self.fnp.removeNode()
        self.physicsMgr.clearLinearForces()

        self.geomRoot.removeNode()

        DistCogdoLevelGame.exitLoaded(self)

    def toCraneMode(self):
        # Move the localToon to 'crane' mode: we're not walking the
        # avatar around, but we're still controlling something
        # in-game, e.g. to move the cranes in the CFO battle.
        # Collisions are still active.
        if self.cr:
            place = self.cr.playGame.getPlace()
            if place and hasattr(place, 'fsm'):
                place.setState('crane')

    def enterIntro(self):
        DistCogdoLevelGame.enterIntro(self)
        self.geomRoot.reparentTo(render)

    def enterGame(self):
        DistCogdoLevelGame.enterGame(self)
        self._physicsTask = taskMgr.add(self._doPhysics, self.uniqueName('physics'), priority=25)

        self.evWalls.stash()

        self._startTimer()

        if __dev__:
            self.accept(self._durationChangedEvent, self._startTimer)

    def _startTimer(self):
        timeLeft = GameConsts.Settings.GameDuration.get() - (globalClock.getRealTime() - self.getStartTime())
        self.timer.posInTopRightCorner()
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    def _doPhysics(self, task):
        dt = globalClock.getDt()
        self.physicsMgr.doPhysics(dt)
        return Task.cont

    def exitGame(self):
        if __dev__:
            self.ignore(self._durationChangedEvent)
        DistCogdoLevelGame.exitGame(self)
        self._physicsTask.remove()

    def enterFinish(self):
        DistCogdoLevelGame.enterFinish(self)
        timeLeft = 10 - (globalClock.getRealTime() - self.getFinishTime())
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    def timerExpired(self):
        pass

    if __dev__:
        def _handleGameDurationChanged(self, gameDuration):
            messenger.send(self._durationChangedEvent)
            
