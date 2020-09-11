"""TwoDEnemy module: contains the TwoDEnemy class"""

from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from direct.showbase import PythonUtil
from direct.interval.IntervalGlobal import *
from toontown.minigame import ToonBlitzGlobals
from toontown.toonbase import ToontownGlobals
from toontown.suit import Suit
from toontown.suit import SuitDNA
from toontown.battle.BattleProps import *
from toontown.battle import MovieUtil
from toontown.battle import BattleParticles, BattleProps
from direct.particles import ParticleEffect
import math

COLOR_RED = VBase4(1, 0, 0, 0.3)

class TwoDEnemy(DirectObject):
    """
    The TwoDEnemy class controls each enemy in a 2D Scroller game.
    All the positions are got from ToonBlitzGlobals.py
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('TwoDEnemy')
    
    def __init__(self, enemyMgr, index, suitAttribs):
        self.enemyMgr = enemyMgr 
        self.game = self.enemyMgr.section.sectionMgr.game
        # The index is a compound number string Eg: 1-2. The 1st no. is the section no. and the 2nd no. is the enemy no.
        self.index = index
        
        self.moveIval = None
        self.propTrack = None
        self.animTrack = None
        self.shotTrack = None
        self.deathTrack = None
        self.deathSuit = None
        self.suitSound = None
        self.deleteMeCallback = None
        self.isMovingUpDown = False
        self.isMovingLeftRight = False
        self.showCollSpheres = False
        self.isDestroyed = False
        self.isGoingUp = False
        
        self.setupEnemy(suitAttribs)
        BattleParticles.loadParticles()
    
    def destroy(self):
        if self.isDestroyed:
            return                   
        self.isDestroyed = True    
        
        if hasattr(self.suit, 'prop') and self.suit.prop:
            self.suit.prop.stash()
        if self.propTrack:
            self.propTrack.finish()
            self.propTrack = None
            
        if self.suitSound:
            self.suitSound.stop()
            del self.suitSound
            
        if self.animTrack:
            self.animTrack.finish()
            self.animTrack = None
        
        if (self.shotTrack != None):
            self.shotTrack.finish()
            self.shotTrack = None
        
        if (self.deathTrack != None):
            self.deathTrack.finish()
            self.deathTrack = None
            
        if self.deathSuit:
            self.deathSuit.detachNode()
            self.suit.cleanupLoseActor()
            self.deathSuit = None
                        
        if self.moveIval:
            self.moveIval.pause()
            del self.moveIval
        if self.suit:
            self.suit.delete()
            self.suit = None
            
        BattleParticles.unloadParticles()
        self.ignore(self.game.uniqueName('enter' + self.suitName))
        self.game = None
        self.enemyMgr = None
    
    def setupEnemy(self, suitAttribs):
##        suitAttribs = ToonBlitzGlobals.EnemyList[self.index]
        suitType = suitAttribs[0]
        
        self.suit = Suit.Suit()
        suitDNA = SuitDNA.SuitDNA()
        suitDNA.newSuit(suitType)
        self.suit.setDNA(suitDNA)
        self.suit.pose('walk', 0)
        self.suitName = 'Enemy-%s' %self.index
        self.suit.setName(self.suitName)
        
        suitPosAttribs = suitAttribs[1]
        initX, initY, initZ = suitPosAttribs[0]
        initPos = Point3(initX, initY, initZ)
        if (len(suitPosAttribs) == 3):
            finalX, finalY, finalZ = suitPosAttribs[1]
            finalPos = Point3(finalX, finalY, finalZ)
            posIvalDuration = suitPosAttribs[2]                
            
            # Setup the interval that makes the block move back and forth between initPos and finalPos
            self.clearMoveIval()
                                          
            def getForwardIval(blendTypeStr, self = self):
                forwardIval = LerpPosInterval(self.suit, posIvalDuration, 
                                          pos = finalPos,
                                          startPos = initPos,
                                          name='%s-moveFront' % self.suitName,
                                          blendType = blendTypeStr,
                                          fluid = 1)
                return forwardIval
            
            def getBackwardIval(blendTypeStr, self = self):
                backwardIval = LerpPosInterval(self.suit, posIvalDuration, 
                                          pos = initPos,
                                          startPos = finalPos,
                                          name='%s-moveBack' % self.suitName,
                                          blendType = blendTypeStr,
                                          fluid = 1)
                return backwardIval
            
            if (abs(finalZ - initZ)  > 0.):
                def setIsGoingUp(value):
                    self.isGoingUp = value
                # Cog has up down motion, get the propellers animation
                self.isMovingUpDown = True
                self.suit.setH(90)
                self.suit.prop = None
                if self.suit.prop == None:
                    self.suit.prop = BattleProps.globalPropPool.getProp('propeller')
                    self.suit.prop.setScale(1.1)
                    self.suit.prop.setColor(1, 1, 0.6, 1)
                head = self.suit.find("**/joint_head")
                self.suit.prop.reparentTo(head)                
                self.propTrack = Sequence(
                    ActorInterval(self.suit.prop, 'propeller', startFrame = 8, endFrame = 25, playRate = 2.))
                self.animTrack = Sequence(ActorInterval(self.suit, 'landing', startFrame = 8, endFrame = 28, playRate = 0.5),
                                          ActorInterval(self.suit, 'landing', startFrame = 8, endFrame = 28, playRate = -0.5))
                self.moveIval = Sequence(Func(setIsGoingUp, True), getForwardIval('easeInOut'),
                                    	 Func(setIsGoingUp, False), getBackwardIval('easeInOut'))
                self.suitSound = base.loadSfx('phase_4/audio/sfx/TB_propeller.wav')
            else:
                # Cog has left right motion
                self.isMovingLeftRight = True
                self.moveIval = Sequence(Func(self.setHeading, finalPos, initPos),
                                         getForwardIval('noBlend'),
                                         Func(self.setHeading, initPos, finalPos),
                                         getBackwardIval('noBlend'))
                                         
        self.suit.setPos(initX, initY, initZ)
        # Hide suit's drop shadow
        self.suit.dropShadow.hide()
        self.setupCollision()
    
    def setupCollision(self):
        """ 
        Make a sphere, give it a unique name, and attach it to the enemy
        To create a unique name, we need to be a DistributedObject, so we create
        a unique name using the minigame's id (the class that instantiated me).
        """
        collSphere = CollisionSphere(0, 0, 2, 2)
        collSphere.setTangible(1)
        collNode = CollisionNode(self.game.uniqueName(self.suitName))
        collNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
        collNode.addSolid(collSphere)
        self.collNodePath = self.suit.attachNewNode(collNode)
        self.collNodePath.hide()
        if self.showCollSpheres:
            self.collNodePath.show()
        self.accept(self.game.uniqueName('enter' + self.suitName), self.handleEnemyCollision)
    
    def clearMoveIval(self):
        """Cleanup the block move interval."""
        if self.moveIval:
            self.moveIval.pause()
            del self.moveIval
        self.moveIval = None
        
    def start(self, elapsedTime):
        if self.moveIval:
            self.moveIval.loop()
            self.moveIval.setT(elapsedTime)
        if self.isMovingLeftRight:
            self.suit.loop('walk')
        elif self.isMovingUpDown:
            self.propTrack.loop()
            self.animTrack.loop()
            base.playSfx(self.suitSound, node = self.suit, looping = 1)
            
    def enterPause(self):
        """ This function is called when the minigame is paused in the debug mode."""
        if hasattr(self, 'moveIval') and self.moveIval:
            self.moveIval.pause()
            self.suit.loop('neutral')
        if self.suitSound:
            self.suitSound.stop()
        
    def exitPause(self):
        """ This function is called when the minigame is unpaused in the debug mode."""
        if hasattr(self, 'moveIval') and self.moveIval:
            self.moveIval.resume()
            if self.isMovingLeftRight:
                self.suit.loop('walk')
            elif self.isMovingUpDown:
                self.propTrack.loop()
                self.animTrack.loop()
                base.playSfx(self.suitSound, node = self.suit, looping = 1, volume = 0.1)
            
    def handleEnemyCollision(self, cevent):
##        self.notify.debug('enemy: %s' %cevent)
        messenger.send('enemyHit')
        
    def setHeading(self, finalPos, initPos):
        diffX = finalPos.getX() - initPos.getX()
##        self.suit.setH(-90 * diffX / math.fabs(diffX))
        angle = -90 * diffX / math.fabs(diffX)
        
        startAngle = self.suit.getH()
        startAngle = PythonUtil.fitSrcAngle2Dest(startAngle,angle)
        dur = .1 * abs(startAngle-angle)/90
        self.suitTurnIval = LerpHprInterval(self.suit, dur, Point3(angle,0,0),
                                            startHpr = Point3(startAngle,0,0),
                                            name='SuitLerpHpr')
        self.suitTurnIval.start()
        
    def blinkColor(self, color, duration):
        blink = Sequence(LerpColorScaleInterval(self.suit, 0.5, color, startColorScale = VBase4(1,1,1,1)),
                         LerpColorScaleInterval(self.suit, 0.5, VBase4(1,1,1,1), startColorScale = color))
        track = Sequence(Func(blink.loop), Wait(duration), Func(blink.finish))
        return track
    
    def doShotTrack(self):
        blinkRed = self.blinkColor(COLOR_RED, 2)
    
##        point = Point3(0, 0, self.suit.height / 2. + 1.)
        point = Point3(self.suit.getX(render), self.suit.getY(render), self.suit.getZ(render) + self.suit.height / 2.)
        scale = 0.3
        splashHold = 0.1
        
        def prepSplash(splash, point):
            if callable(point):
                point = point()
            splash.reparentTo(render)
            splash.setPos(point)
            scale = splash.getScale()
            splash.setBillboardPointWorld()
            splash.setScale(scale)
        splash = globalPropPool.getProp('splash-from-splat')
        splash.setScale(scale)
        
        splashTrack =  Sequence(
            Func(prepSplash, splash, point),
            ActorInterval(splash, 'splash-from-splat'),
            Wait(splashHold),
            Func(MovieUtil.removeProp, splash),
        )

        self.shotTrack = Parallel(Func(self.game.assetMgr.playSplashSound), blinkRed, splashTrack)
        self.shotTrack.start()
    
    def doDeathTrack(self):
        def removeDeathSuit(suit, deathSuit):
            if (not deathSuit.isEmpty()):
                deathSuit.detachNode()
                suit.cleanupLoseActor()
        
        # Stop the suit sound
        if self.suitSound:
            self.suitSound.stop()
        
        self.deathSuit = self.suit.getLoseActor()
        self.deathSuit.reparentTo(self.enemyMgr.enemiesNP)
        self.deathSuit.setPos(render, self.suit.getPos(render))
        self.deathSuit.setHpr(render, self.suit.getHpr(render))
        self.suit.hide()
        # We don't need a collision for the suit, so we reparent it to the deathSuit
        self.collNodePath.reparentTo(self.deathSuit)
        
        treasureSpawnPoint = Point3(self.suit.getX(), self.suit.getY(), self.suit.getZ() + self.suit.height / 2.)
        gearPoint = Point3(0, 0, self.suit.height / 2. + 2.)
        spinningSound = base.loadSfx("phase_3.5/audio/sfx/Cog_Death.mp3")
        deathSound = base.loadSfx("phase_3.5/audio/sfx/ENC_cogfall_apart.mp3")
        
        smallGears = BattleParticles.createParticleEffect(file='gearExplosionSmall')
        singleGear = BattleParticles.createParticleEffect('GearExplosion', numParticles = 1)
        smallGearExplosion = BattleParticles.createParticleEffect('GearExplosion', numParticles = 10)
        bigGearExplosion = BattleParticles.createParticleEffect('BigGearExplosion', numParticles = 30)
    
        smallGears.setPos(gearPoint)
        singleGear.setPos(gearPoint)
        smallGearExplosion.setPos(gearPoint)
        bigGearExplosion.setPos(gearPoint)
        smallGears.setDepthWrite(False)
        singleGear.setDepthWrite(False)
        smallGearExplosion.setDepthWrite(False)
        bigGearExplosion.setDepthWrite(False)
        
        if self.isMovingLeftRight:
            self.enterPause()
            suitTrack = Sequence(
                Func(self.collNodePath.stash),
                ActorInterval(self.deathSuit, 'lose', startFrame = 80, endFrame = 140),
                Func(removeDeathSuit, self.suit, self.deathSuit, name = 'remove-death-suit')
            )
            
            explosionTrack = Sequence(
                Wait(1.5),
                MovieUtil.createKapowExplosionTrack(self.deathSuit, explosionPoint = gearPoint),
            )
            
            soundTrack = Sequence(
                SoundInterval(spinningSound, duration = 1.6, startTime = 0.6, volume=0.8, node=self.deathSuit),
                SoundInterval(deathSound, volume = 0.32, node=self.deathSuit)
            )
            
            gears1Track = Sequence(
                ParticleInterval(smallGears, self.deathSuit, worldRelative = 0, duration = 4.3, cleanup = True),
                name='gears1Track'
            )
            
            gears2MTrack = Track(
                (0.0, explosionTrack),
                (0.7, ParticleInterval(singleGear, self.deathSuit, worldRelative = 0, duration = 5.7, cleanup = True)),
                (5.2, ParticleInterval(smallGearExplosion, self.deathSuit, worldRelative = 0, duration = 1.2, cleanup = True)),
                (5.4, ParticleInterval(bigGearExplosion, self.deathSuit, worldRelative = 0, duration = 1.0, cleanup = True)),
                name='gears2MTrack'
            )
            
        elif self.isMovingUpDown:
            def getFinalPos():
                if self.isGoingUp:
                    direction = 1.
                else:
                    direction = -1.            
                pos = Point3(self.deathSuit.getX(),
                             self.deathSuit.getY(),
                             self.deathSuit.getZ() + 2. * direction)
                return pos
            
            deathMoveIval = LerpPosInterval(self.deathSuit, 1.5, 
                                          pos = getFinalPos(),
                                          name='%s-deathSuitMove' % self.suitName,
                                          blendType = 'easeInOut',
                                          fluid = 1)
            
            suitTrack = Sequence(
                Func(self.collNodePath.stash),
                Parallel(ActorInterval(self.deathSuit, 'lose', startFrame = 80, endFrame = 140),
                         deathMoveIval),                
                Func(removeDeathSuit, self.suit, self.deathSuit, name = 'remove-death-suit')
            )
        
            explosionTrack = Sequence(
                Wait(1.5),
                MovieUtil.createKapowExplosionTrack(self.deathSuit, explosionPoint = gearPoint),
            )
        
            soundTrack = Sequence(
                SoundInterval(spinningSound, duration = 1.6, startTime = 0.6, volume=0.8, node=self.deathSuit),
                SoundInterval(deathSound, volume = 0.32, node=self.deathSuit)
            )
        
            gears1Track = Sequence(
                ParticleInterval(smallGears, self.deathSuit, worldRelative = 0, duration = 4.3, cleanup = True),
                name='gears1Track'
            )
        
            gears2MTrack = Track(
                (0.0, explosionTrack),
                (0.0, ParticleInterval(singleGear, self.deathSuit, worldRelative = 0, duration = 5.7, cleanup = True)),
                (2.7, ParticleInterval(smallGearExplosion, self.deathSuit, worldRelative = 0, duration = 1.2, cleanup = True)),
                (2.9, ParticleInterval(bigGearExplosion, self.deathSuit, worldRelative = 0, duration = 1.0, cleanup = True)),
                name='gears2MTrack'
            )
        
        def removeParticle(particle):
            # Adding a wrapper because I think a particle is trying to get cleaned up twice
            if particle and hasattr(particle, 'renderParent'):
                particle.cleanup()
                del particle
        
        removeParticles = Parallel(Func(removeParticle, smallGears),
                                   Func(removeParticle, singleGear),
                                   Func(removeParticle, smallGearExplosion),
                                   Func(removeParticle, bigGearExplosion))
        
        # Spawning the treasure after 1.5 seconds was breaking with multiple clients
        # and heavy lag. So we are generating the treasure as soon as the cog starts
        # exploding and we do visual tricks to show it after 2.4 seconds.
        self.deathTrack = Sequence(Parallel(suitTrack, gears2MTrack, gears1Track, soundTrack),
                                   removeParticles, 
                                   Func(self.destroy))
        self.deathTrack.start()