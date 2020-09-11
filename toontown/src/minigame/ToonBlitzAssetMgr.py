"""ToonBlitzAssetMgr module: contains the ToonBlitzAssetMgr class"""

from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from toontown.toonbase.ToonBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.minigame import ToonBlitzGlobals, TwoDBlock
from pandac.PandaModules import CardMaker

class ToonBlitzAssetMgr(DirectObject):
    """
    This class controls all the art and sound assets of Toon Blitz minigame.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonBlitzAssets')
    # define constants that you won't want to tweak here

    def __init__(self, game):
        self.__defineConstants()
        self.game = game
        self.load()
    
    def __defineConstants(self):
        '''Define all the Toon Blitz contants here.'''
        pass

    def load(self):
        assert self.notify.debugStateCall(self)
        
        # Create top node for the world. Reparent all the assets to this.
        self.world = NodePath('ToonBlitzWorld')
        
        # Loading the models
        self.background = loader.loadModel("phase_4/models/minigames/toonblitz_game")
        self.background.reparentTo(self.world)
        
        self.startingWall = loader.loadModel("phase_4/models/minigames/toonblitz_game_wall")
        self.startingPipe = loader.loadModel("phase_4/models/minigames/toonblitz_game_start")
        self.exitElevator = loader.loadModel("phase_4/models/minigames/toonblitz_game_elevator")
        self.arrow = loader.loadModel("phase_4/models/minigames/toonblitz_game_arrow")
        self.sprayProp = loader.loadModel("phase_4/models/minigames/prop_waterspray")
        
        self.treasureModelList = []
        salesIcon = loader.loadModel("phase_4/models/minigames/salesIcon")
        self.treasureModelList.append(salesIcon)
        moneyIcon = loader.loadModel("phase_4/models/minigames/moneyIcon")
        self.treasureModelList.append(moneyIcon)
        legalIcon = loader.loadModel("phase_4/models/minigames/legalIcon")
        self.treasureModelList.append(legalIcon)
        corpIcon = loader.loadModel("phase_4/models/minigames/corpIcon")
        self.treasureModelList.append(corpIcon)
        
        self.particleGlow = loader.loadModel("phase_4/models/minigames/particleGlow")
        
        self.blockTypes = []
        for i in xrange(4):
            blockType = loader.loadModel("phase_4/models/minigames/toonblitz_game_block0" + str(i))
            self.blockTypes.append(blockType)
            
        self.stomper = loader.loadModel("phase_4/models/minigames/toonblitz_game_stomper")
        
        # Creating bottom floor
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -50)))
        dropPlane = CollisionNode('dropPlane')
        dropPlane.addSolid(plane)
        dropPlane.setCollideMask(ToontownGlobals.FloorBitmask)
        self.world.attachNewNode(dropPlane)
        
        # Loading the music
        self.gameMusic = base.loadMusic("phase_4/audio/bgm/MG_TwoDGame.mid")
        self.treasureGrabSound = loader.loadSfx("phase_4/audio/sfx/SZ_DD_treasure.mp3")
        self.sndOof = base.loadSfx('phase_4/audio/sfx/MG_cannon_hit_dirt.mp3')
        self.soundJump = base.loadSfx('phase_4/audio/sfx/MG_sfx_vine_game_jump.mp3')
        self.fallSound =  base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_fall.mp3")
        self.watergunSound = base.loadSfx("phase_4/audio/sfx/AA_squirt_seltzer_miss.mp3")
        self.splashSound = base.loadSfx("phase_4/audio/sfx/Seltzer_squirt_2dgame_hit.mp3")
        self.threeSparkles = loader.loadSfx("phase_4/audio/sfx/threeSparkles.mp3")
        self.sparkleSound = loader.loadSfx("phase_4/audio/sfx/sparkly.mp3")
        self.headCollideSound = loader.loadSfx("phase_3.5/audio/sfx/AV_collision.mp3")
        
        # Card for the progress line
        self.faceStartPos = Vec3(-0.80, 0, -0.87)
        self.faceEndPos = Vec3(0.80 ,0 ,-0.87)
        self.aspect2dRoot = aspect2d.attachNewNode('TwoDGuiAspect2dRoot')
        self.aspect2dRoot.setDepthWrite(1)
        self.cardMaker = CardMaker('card')
        self.cardMaker.reset()
        self.cardMaker.setName('ProgressLine')
        self.cardMaker.setFrame(-0.5, 0.5, -0.5, 0.5)
        self.progressLine = self.aspect2dRoot.attachNewNode(self.cardMaker.generate())
        self.progressLine.setScale(self.faceEndPos[0]-self.faceStartPos[0], 1, 0.01)
        self.progressLine.setPos(0, 0, self.faceStartPos[2])
        
        self.cardMaker.setName('RaceProgressLineHash')
        for n in xrange(ToonBlitzGlobals.NumSections[self.game.getSafezoneId()] + 1):
            hash = self.aspect2dRoot.attachNewNode(self.cardMaker.generate())
            hash.setScale(self.progressLine.getScale()[2],1,self.progressLine.getScale()[2] * 5)
            t = float(n) / ToonBlitzGlobals.NumSections[self.game.getSafezoneId()]
            hash.setPos(self.faceStartPos[0] * (1 - t) + self.faceEndPos[0] * t,
                        self.faceStartPos[1],
                        self.faceStartPos[2])
        
    def destroy(self):
        assert self.notify.debugStateCall(self)
        while len(self.blockTypes):
            blockType = self.blockTypes[0]
            self.blockTypes.remove(blockType)
            del blockType
        self.blockTypes = None
        
        while len(self.treasureModelList):
            treasureModel = self.treasureModelList[0]
            self.treasureModelList.remove(treasureModel)
            del treasureModel
        self.treasureModelList = None
        
        self.startingWall.removeNode()
        del self.startingWall        
        self.startingPipe.removeNode()
        del self.startingPipe        
        self.exitElevator.removeNode()
        del self.exitElevator        
        self.stomper.removeNode()
        del self.stomper
        self.arrow.removeNode()
        del self.arrow
        self.sprayProp.removeNode()
        del self.sprayProp
        self.aspect2dRoot.removeNode()
        del self.aspect2dRoot
        self.world.removeNode()
        del self.world
        
        del self.gameMusic
        del self.treasureGrabSound
        del self.sndOof
        del self.soundJump
        del self.fallSound
        del self.watergunSound
        del self.splashSound
        del self.threeSparkles
        del self.sparkleSound
        del self.headCollideSound
        
        self.game = None

    def onstage(self):
        assert self.notify.debugStateCall(self)
        # parent things to render, start playing music...
        self.world.reparentTo(render)
        base.playMusic(self.gameMusic, looping = 1, volume = 0.9)

    def offstage(self):
        assert self.notify.debugStateCall(self)
        # parent things to hidden, stop the music...
        self.world.hide()
        self.gameMusic.stop()
        
    def enterPlay(self):
        """ This function is called when the minigame enters the play state."""
        pass
    
    def exitPlay(self):
        """ This function will be called when the minigame exits the play state."""
        pass
    
    def enterPause(self):
        pass
            
    def exitPause(self):
        pass
            
    def playJumpSound(self):
        base.localAvatar.soundRun.stop()
        base.playSfx(self.soundJump, looping = 0)
        
    def playWatergunSound(self):
        self.watergunSound.stop()
        base.playSfx(self.watergunSound, looping = 0)
        
    def playSplashSound(self):
        self.splashSound.stop()
        base.playSfx(self.splashSound, looping = 0)
        
    def playHeadCollideSound(self):
        self.headCollideSound.stop()
        base.playSfx(self.headCollideSound, looping = 0)
        