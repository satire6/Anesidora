from pandac.PandaModules import NodePath, Point3, CollisionSphere, CollisionNode, Vec4
from direct.interval.IntervalGlobal import Sequence, LerpPosInterval, Parallel, LerpScaleInterval, Track,\
     ParticleInterval, Wait, Func
from toontown.toonbase import ToontownGlobals
from toontown.coghq import MoleFieldBase
from direct.particles import ParticleEffect
from toontown.battle import BattleParticles
from toontown.battle import BattleProps


class MoleHill(NodePath):
    """Represents one mole hill in a mole field. Exists only on the client."""

    
    def __init__(self, x, y, z, moleField, index):
        """Construct the mole hill."""
        NodePath.__init__(self, 'MoleHill-%d' % index)
        self.moleField= moleField
        self.index = index
        self.loadModel()
        self.setPos(x, y, z)
        self.schedule = []
        self.popIval = None
        self.downIval = None
        self.popupNum = 0 # how many times has this hill popped up
        self.hillType = None
        self.isUp = 0

    def loadModel(self):
        """Load the necessary assets."""
        self.hill = loader.loadModel("phase_12/models/bossbotHQ/mole_hole")
        self.hill.setZ(0.0)
        self.hill.reparentTo(self)
        #self.hill.setScale(20.0)
        # find the collision node of the hill and rename it
        #hillCollision = self.hill.find('**/dirt_collision')
        self.hillColName = 'moleHillCol-%d-%d' % (self.moleField.doId, self.index)
        #hillCollision.setName(self.hillColName)
        self.moleField.accept('enter' + self.hillColName, self.moleField.handleEnterHill)
        self.mole = self.attachNewNode("mole")#loader.loadModel("phase_12/models/bossbotHQ/mole_norm")
        self.mole.reparentTo(self)
        self.mole.setScale(0.75)
        self.mole.setZ(-2.5)
        self.moleHead = loader.loadModel("phase_12/models/bossbotHQ/mole_norm")
        self.moleHead.reparentTo(self.mole)
        # setup mole collision
        moleColName = "moleCol-%d-%s" % (self.moleField.doId,self.index)
        moleSphere = CollisionSphere(0, 0, 0, 1.0)
        collNode = CollisionNode(moleColName)
        collNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
        collNode.addSolid(moleSphere)
        self.moleColNodePath = self.mole.attachNewNode(collNode)
        self.moleColNodePath.stash()
        self.moleColNodePath.setScale(1.0)
        self.moleField.accept('enter' + moleColName, self.moleField.handleEnterMole)

    def destroy(self):
        """Cleanup and destroy self."""
        if self.popIval:
            self.popIval.pause()
            self.popIval = None
        if self.downIval:
            self.downIval.pause()
            self.downIval = None
        self.removeNode()
        pass
        
    def switchUp(self):
        self.isUp = 1
        
    def switchDown(self):\
        self.isUp = 0
        
        
    def setHillType(self, type):
        if self.isUp and (((self.hillType == MoleFieldBase.HILL_MOLE) and (type == MoleFieldBase.HILL_BOMB)) or ((self.hillType == MoleFieldBase.HILL_BOMB ) and (type == MoleFieldBase.HILL_MOLE))):
            return
        self.hillType = type
        self.moleHead.remove()
        if type == MoleFieldBase.HILL_MOLE:
            self.moleHead = loader.loadModel("phase_12/models/bossbotHQ/mole_norm")
            self.moleColNodePath.setScale(3.0)
            self.moleHead.setH(0)
            self.mole.setBillboardAxis(localAvatar, 0)
        if type == MoleFieldBase.HILL_BOMB or type == MoleFieldBase.HILL_COGWHACKED:
            self.moleHead = loader.loadModel("phase_12/models/bossbotHQ/mole_cog")
            self.moleColNodePath.setScale(1.0)
            self.mole.setBillboardAxis(localAvatar, 0)
            if type == MoleFieldBase.HILL_COGWHACKED:
                self.doMoleDown()
                BattleParticles.loadParticles()
                #smallGears = BattleParticles.createParticleEffect(file='gearExplosionSmall')
                singleGear = BattleParticles.createParticleEffect('GearExplosion', 
                                                                            numParticles=1)
                smallGearExplosion = BattleParticles.createParticleEffect('GearExplosion',
                                                                          numParticles=10)
                bigGearExplosion = BattleParticles.createParticleEffect('BigGearExplosion',
                                                                          numParticles=30)
                #gearPoint = Point3(self.hill.getX(render), self.hill.getY(render), self.hill.getZ(render))
                #smallGears.setPos(gearPoint)
                #singleGear.setPos(gearPoint)
                #smallGears.setDepthWrite(False)
                #singleGear.setDepthWrite(False)
                #smallGearExplosion.setPos(gearPoint)
                #bigGearExplosion.setPos(gearPoint)
                #smallGearExplosion.setDepthWrite(False)
                #bigGearExplosion.setDepthWrite(False)
                gears2MTrack = Track(
                    (0.0, ParticleInterval(singleGear, self.hill, worldRelative=1,
                                           duration=5.7, cleanup = True)),
                    (0.0, ParticleInterval(smallGearExplosion, self.hill,
                                           worldRelative=0, duration=1.2, cleanup = True)),
                    (0.3, ParticleInterval(bigGearExplosion, self.hill,
                                           worldRelative=0, duration=1.0, cleanup = True)),
                    name='gears2MTrack')
                #gearTrack = Parallel(gears2MTrack)
                #gearTrack.start()
                gears2MTrack.start()
                
                self.popIval = Sequence(
                    Parallel(
                        Sequence(
                            LerpPosInterval(self.moleHead, 0.05, Point3(0.28,0.0,0.0)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(0.0,-0.23,0.0)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.0,0.28)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(-0.35,0.0,0.0)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.28,0.0)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(0.31,0.0,0.0)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(0.0,-0.32,0.0)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.0,0.48)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(-0.28,0.0,0.0)),
                            LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.29,0.0)),
                            ),
                        ),
                    
                    LerpPosInterval(self.mole, 0.5, Point3(0,0,-2.5)),
       
                    Func(self.setHillType, MoleFieldBase.HILL_BOMB),
                    )
                self.popIval.start()
                
            else:
                self.moleHead.setH(0)
                
        if type == MoleFieldBase.HILL_WHACKED:
            self.moleHead = loader.loadModel("phase_12/models/bossbotHQ/mole_hit")
            self.mole.setBillboardAxis(0)
            self.moleColNodePath.setScale(0.0)
            if self.popIval:
                self.popIval.finish()
            if self.downIval:
                self.downIval.finish()
            self.mole.setPos(0.0,0.0,0.0)
            self.popIval = Sequence(
                Parallel(
                    Sequence(
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.18,0.0,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,-0.13,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.0,0.18)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(-0.15,0.0,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.18,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.11,0.0,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,-0.12,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.0,0.18)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(-0.18,0.0,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.13,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.18,0.0,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,-0.15,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.0,0.18)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(-0.16,0.0,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.18,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.11,0.0,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,-0.18,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.0,0.17)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(-0.18,0.0,0.0)),
                        LerpPosInterval(self.moleHead, 0.05, Point3(0.0,0.0,0.0)),
                        ),
                        Sequence(
                            LerpScaleInterval(self.moleHead, 0.5, 3.5),
                            LerpScaleInterval(self.moleHead, 0.5, 1.0),
                        ),
                    ),
                
                LerpPosInterval(self.mole, 0.5, Point3(0,0,-2.5)),
   
                Func(self.setHillType, MoleFieldBase.HILL_MOLE),
                )
            self.popIval.start()
        self.moleHead.reparentTo(self.mole)

    def doMolePop(self, startTime, timeToMoveUp, timeToStayUp, timeToMoveDown, moleType):
        """Show a mole popping up.
        
        startTime = will be based from startupTime
        timeToMoveUp = number of seconds it takes to go up
        timeToStayUp = how long will the mole stay up
        timeToMoveDown = how long it will take for the mole to move down
        """
        if self.hillType == MoleFieldBase.HILL_WHACKED or self.hillType == MoleFieldBase.HILL_COGWHACKED:
            return
        if self.popIval:
            self.popIval.pause()
        if self.downIval:
            self.downIval.pause()
            self.downIval = None
            
        moleColor = None
        #if moleType == MoleFieldBase.HILL_BOMB:
        #    moleColor = Vec4(1,0,0,1)
        #    self.moleColNodePath.setScale(5.0)
        #else:
        #    moleColor = Vec4(1,1,1,1)
        #    self.moleColNodePath.setScale(1.0)
        self.switchUp()

        self.popupNum += 1
        if self.hillType == MoleFieldBase.HILL_BOMB:
            self.popIval = Sequence(
                #Func(self.mole.setColorScale, moleColor),
                Func(self.setHillType, moleType),
                Func(self.moleColNodePath.unstash),
                LerpPosInterval(self.mole, timeToMoveUp, Point3(0,0,0.0)),
                Wait(timeToStayUp),
                LerpPosInterval(self.mole, timeToMoveDown, Point3(0,0,-2.5)),
                Func(self.stashMoleCollision),
                Func(self.switchDown),
                )
        else:
            self.popIval = Sequence(
                #Func(self.mole.setColorScale, moleColor),
                Func(self.setHillType, moleType),
                LerpPosInterval(self.mole, timeToMoveUp, Point3(0,0,0.0)),
                Func(self.moleColNodePath.unstash),
                Wait(timeToStayUp),
                Func(self.stashMoleCollision),
                LerpPosInterval(self.mole, timeToMoveDown, Point3(0,0,-2.5)),
                Func(self.switchDown),
                )
        self.popIval.start()
        

    def setGameStartTime(self, gameStartTime):
        """Set the game start time as dictated by parent mole field."""
        self.gameStartTime = gameStartTime
        self.popupNum = 0 # how many times has this hill popped up

    def stashMoleCollision(self):
        """Stash the mole collision."""
        self.moleColNodePath.stash()

    def getPopupNum(self):
        """Return the how many times the mole has popped up from this hill."""
        return self.popupNum

    def doMoleDown(self):
        if self.hillType == MoleFieldBase.HILL_WHACKED or self.hillType == MoleFieldBase.HILL_COGWHACKED:
            return
        """Show a mole going down."""
        if self.popIval:
            self.popIval.pause()
            self.popIval = None
        if self.downIval:
            self.downIval.pause()
        self.downIval = Sequence(
            Func(self.stashMoleCollision),
            LerpPosInterval(self.mole, 1, Point3(0,0,-2.5)),
            Func(self.switchDown),
            )
        self.downIval.start()

    def forceMoleDown(self):
        """Instantly force a mole down."""
        if self.popIval:
            self.popIval.pause()
            self.popIval = None
        if self.downIval:
            self.downIval.pause()
            self.downIval = None
        self.stashMoleCollision()
        self.switchDown()
        self.mole.setPos(0, 0, -2.5)
