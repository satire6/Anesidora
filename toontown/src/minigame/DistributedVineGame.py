"""DistributedVineGame module: contains the DistributedVineGame class"""
from pandac.PandaModules import Point3, ForceNode, LinearVectorForce, \
     CollisionHandlerEvent, CollisionNode, CollisionSphere, Camera, \
     PerspectiveLens, Vec4, Point2, ActorNode, Vec3, BitMask32
from direct.interval.IntervalGlobal import Sequence, Parallel, \
     Func, Wait, LerpPosInterval, ActorInterval, LerpScaleInterval, \
     ProjectileInterval, SoundInterval
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGui import DGG
from toontown.toonbase import ToontownGlobals
from direct.task.Task import Task
from direct.fsm import ClassicFSM, State
from toontown.toonbase import TTLocalizer
from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame import  SwingVine
from toontown.minigame import ArrowKeys
from toontown.minigame import VineGameGlobals
from toontown.minigame import VineTreasure
from toontown.minigame import MinigameAvatarScorePanel
from toontown.toonbase import ToontownTimer
from toontown.minigame import VineHeadFrame
from toontown.minigame import VineBat

class DistributedVineGame(DistributedMinigame):
    """Client side class for the vine game."""
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedVineGame')

    # define constants that you won't want to tweak here
    UpdateLocalToonTask = "VineGameUpdateLocalToonTask" # name of the update task called each frame
    LocalPhysicsRadius = 1.5 # in feet, the higher the easier to catch vines
    Gravity = 32  # in feet / second squared
    ToonVerticalRate = 0.25 # how fast toons move up or down the vine
    FallingNot = 0 # toon is not falling
    FallingNormal = 1 # toon jumped off a vine and falling normally
    FallingSpider = 2 # toon falling because he hit a spider
    FallingBat = 3 # toon falling because he hit a bat
    JumpingFrame = 128 # our pose when we're jumping of a vine
    ToonMaxRightFrame = 35 # which frame has the vine all the way to the right
    
    def __init__(self, cr):
        """Constructor for DistributedVineGame."""
        DistributedMinigame.__init__(self, cr)

        self.JumpSpeed = 64 # scalar speed when we jump from vine, in feet/sec
        self.TwoVineView = True
        self.ArrowToChangeFacing = True

        self.gameFSM = ClassicFSM.ClassicFSM('DistributedVineGame',
                               [
                                State.State('off',
                                            self.enterOff,
                                            self.exitOff,
                                            ['play']),
                                State.State('play',
                                            self.enterPlay,
                                            self.exitPlay,
                                            ['cleanup',
                                             'showScores',
                                             'waitShowScores']),
                                State.State('waitShowScores',
                                            self.enterWaitShowScores,
                                            self.exitWaitShowScores,
                                            ['cleanup',
                                             'showScores']),
                                State.State('showScores',
                                            self.enterShowScores,
                                            self.exitShowScores,
                                            ['cleanup']),
                                State.State('cleanup',
                                            self.enterCleanup,
                                            self.exitCleanup,
                                            []),
                                ],
                               # Initial State
                               'off',
                               # Final State
                               'cleanup',
                               )

        # it's important for the final state to do cleanup;
        # on disconnect, the ClassicFSM will be forced into the
        # final state. All states (except 'off') should
        # be prepared to transition to 'cleanup' at any time.

        # Add our game ClassicFSM to the framework ClassicFSM
        self.addChildGameFSM(self.gameFSM)

        self.cameraTopView = (17.6, 6.18756, 43.9956, 0, -89, 0)
        #self.cameraThreeQuarterView = (14.0, -8.93352, 33.4497, 0, -62.89, 0)
        #self.cameraThreeQuarterView = (0.0, -10, 33.4497, 0, -62.89, 0)
        #self.cameraThreeQuarterView = (0.0, -154, 17, 0, 0.0, 0)
        self.cameraThreeQuarterView = (0, -63.2, 16.3, 0, 0, 0)

        self.cameraSidePos = Point3(0, -63.2, 16.3)
        self.cameraTwoVineSidePos = Point3(0, -53, 17.3)
        self.cameraTwoVineAdj = 5
        self.cameraSideView = (-15, -53, 17.3, 0, 0, 0)

        # Set up a physics manager for the cables and the objects
        # falling around in the room.
        #self.geom = render.attachNewNode('geom')
    
        #self.physicsMgr = PhysicsManager()
        #integrator = LinearEulerIntegrator()
        #self.physicsMgr.attachLinearIntegrator(integrator)

        self.localPhysicsNP= None

        self.vines = []

        # WARNING comment out below or else it will leak
        # base.minigame = self

        self.physicsHandler = None

        # information for the local toon
        self.lastJumpVine = -1
        self.lastJumpPos = None
        self.lastJumpT = 0
        self.lastJumpFacingRight = True
        self.lastJumpTime = 0 # when did he jump

        # information for all toons
        # key is av Id
        # 0 vineIndex, if -1 then he's not attached to a vine is currently jumping
        # 1 vineT, where is he on the vine
        # 2 posX, - his x position when he jumped
        # 3 posZ - his z position when he jumped 
        # 4 facing right
        # 5 climb direction -1 going up, 0 standing still, 1 going down
        # 6 velX - his X velocity when he jumped
        # 7 velZ - his Z velocity when he jumped
        # 8 fallingInfo - see falling constants above
        self.toonInfo = {}

        self.otherToonPhysics = {}
        self.headFrames = {}
        self.changeFacingInterval = None
        self.attachingToVineCamIval = None
        self.localToonJumpAnimIval = None
        self.endingTracks = {}
        self.endingTrackTaskNames = []

        self.sendNewVineTUpdateAsap = False
        self.lastNewVineTUpdate = 0

        self.defaultMaxX = (VineGameGlobals.NumVines +1) * VineGameGlobals.VineXIncrement 
        
    def getClimbDir(self, avId):
        """Get the last know climb direction of this toon."""
        retval = 0
        if self.toonInfo.has_key(avId):
            retval = self.toonInfo[avId][5]
        return retval
        
    def moveCameraToSide(self):
        camera.reparentTo(render)
        p = self.cameraSideView
        camera.setPosHpr(p[0], p[1], p[2], p[3], p[4], p[5])

    def getTitle(self):
        return TTLocalizer.VineGameTitle

    def getInstructions(self):
        return TTLocalizer.VineGameInstructions

    def getMaxDuration(self):
        # how many seconds can this minigame possibly last (within reason)?
        # this is for debugging only
        return 0

    def defineConstants(self):
        self.ShowToonSpheres = 0

    def load(self):
        self.notify.debug("load")
        DistributedMinigame.load(self)
        # load resources and create objects here
        self.defineConstants()

        self.music = base.loadMusic("phase_4/audio/bgm/MG_Vine.mid")

        self.gameAssets = loader.loadModel("phase_4/models/minigames/vine_game")
        self.gameBoard = self.gameAssets.find('**/background')
        self.gameBoard.reparentTo(render)
        #gameAssets.removeNode()
        self.gameBoard.show()
        self.gameBoard.setPosHpr(0,0,0,0,0,0)
        self.gameBoard.setTransparency(1)
        self.gameBoard.setColorScale(1,1,1,0.5)
        self.gameBoard.setScale(1.0)
        self.gameBoard.hide(VineGameGlobals.RadarCameraBitmask)

        #debugAxis = loader.loadModel('models/misc/xyzAxis')
        #debugAxis.reparentTo(self.gameBoard)

        #debugFruit = loader.loadModel("phase_4/models/minigames/swimming_game_ring")
        #debugFruit.reparentTo(self.gameBoard)

        self.treasureModel = self.gameAssets.find('**/bananas')

        self.setupVineCourse()

        self.grabSound = base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_bananas.mp3")
        self.jumpSound = base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_jump.mp3")
        self.catchSound = base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_catch.mp3")
        self.spiderHitSound = base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_spider_hit.mp3")
        self.batHitVineSound = base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_bat_hit.mp3")
        self.batHitMidairSound = base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_bat_hit_midair.mp3")
        self.winSound = base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_finish.mp3")
        self.fallSound =  base.loadSfx("phase_4/audio/sfx/MG_sfx_vine_game_fall.mp3")

        self.loadBats()
        self.createBatIvals()

        #self.startPlatform = loader.loadModel('models/misc/xyzAxis')
        bothPlatform = loader.loadModel("phase_4/models/minigames/vine_game_shelf")
        self.startPlatform = bothPlatform.find('**/start1')
        self.startPlatform.setPos(-16, 0, 15)
        self.startPlatform.reparentTo(render)
        self.startPlatform.setScale(1.0, 1.0, 0.75)

        #self.endPlatform = loader.loadModel('models/misc/xyzAxis')
        self.endPlatform = bothPlatform.find('**/end1')
        endPos = self.vines[VineGameGlobals.NumVines -1].getPos()
        self.endPlatform.setPos( endPos[0] + 20, 0, 15)
        self.endPlatform.reparentTo(render)
        self.endPlatform.setScale(1.0, 1.0, 0.75)
        
    def unload(self):
        self.notify.debug("unload")
        DistributedMinigame.unload(self)
        # unload resources and delete objects from load() here
        # remove our game ClassicFSM from the framework ClassicFSM
        self.removeChildGameFSM(self.gameFSM)
        del self.gameFSM

        del self.music

        self.gameAssets.removeNode()
        self.gameBoard.removeNode()
        del self.gameBoard

        self.treasureModel.removeNode()
        del self.treasureModel

        for vine in self.vines:
            vine.unload()
            del vine
        self.vines = []

        self.destroyBatIvals() # do this before destroying the bats
        for bat in self.bats:
            bat.destroy()
            del bat
        self.bats = []

        del self.grabSound
        del self.jumpSound
        del self.catchSound
        del self.spiderHitSound
        del self.batHitVineSound
        del self.batHitMidairSound
        del self.winSound
        del self.fallSound
        
        if self.localToonJumpAnimIval:
            self.localToonJumpAnimIval.finish()
            del self.localToonJumpAnimIval

        self.startPlatform.removeNode()
        self.endPlatform.removeNode()

    def onstage(self):
        self.notify.debug("onstage")
        DistributedMinigame.onstage(self)
        # start up the minigame; parent things to render, start playing
        # music...
        # at this point we cannot yet show the remote players' toons

        for avId in self.avIdList:
            self.updateToonInfo( avId, vineIndex = 0,
                                 vineT = VineGameGlobals.VineStartingT,
                                 posX = 0, posZ =0, facingRight = 0,
                                 climbDir = 0, fallingInfo = self.FallingNot)
        
        self.scorePanels = []
        
        self.gameBoard.reparentTo(render)

        self.moveCameraToSide()

        self.arrowKeys = ArrowKeys.ArrowKeys()
        handlers =  [self.upArrowKeyHandler, self.downArrowKeyHandler, self.leftArrowKeyHandler, self.rightArrowKeyHandler, None]
        self.arrowKeys.setPressHandlers(handlers)

        # create the treasures
        self.numTreasures = len(self.vines) - 1
        self.treasures = []
        for i in xrange(self.numTreasures):
            height = self.randomNumGen.randrange( 10, 25)
            xPos = self.randomNumGen.randrange( 12, 18)
            #pos = Point3( 5, 0, 20)
            pos = Point3(self.vines[i].getX() + 15, 0, height)
            self.treasures.append(VineTreasure.VineTreasure(
                self.treasureModel, pos, i, self.doId))

        
        # set the background color to match the gameboard
        #base.setBackgroundColor(0.1875, 0.7929, 0)        

        gravityFN=ForceNode('world-forces')
        gravityFNP=render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-self.Gravity) #gravity acceleration
        gravityFN.addForce(gravityForce)
        
        base.physicsMgr.addLinearForce(gravityForce)
        self.gravityForce = gravityForce
        self.gravityForceFNP = gravityFNP

        lt = base.localAvatar
        # attach some collision spheres so that we can catch things
        # with any part of our body
        # four spheres seems to be enough for the body
        # one on the legs, one on the head, one on each hand
        # (having one on each hand is slight overkill; it's useful during the
        # falling-down animations when the hands are widely separated. meh.)
        radius = .7
        handler = CollisionHandlerEvent()
        handler.setInPattern('ltCatch-%fn')
        self.bodyColEventNames = []
        self.ltLegsCollNode = CollisionNode('catchLegsCollNode')
        self.bodyColEventNames.append('ltCatch-%s' % 'catchLegsCollNode')
        self.ltLegsCollNode.setCollideMask(VineGameGlobals.SpiderBitmask)
        self.ltTorsoCollNode = CollisionNode('catchTorsoCollNode')
        self.bodyColEventNames.append('ltCatch-%s' % 'catchTorsoCollNode')
        self.ltTorsoCollNode.setCollideMask(VineGameGlobals.SpiderBitmask)        
        self.ltHeadCollNode = CollisionNode('catchHeadCollNode')
        self.bodyColEventNames.append('ltCatch-%s' % 'catchHeadCollNode')        
        self.ltHeadCollNode.setCollideMask(VineGameGlobals.SpiderBitmask)
        self.ltLHandCollNode = CollisionNode('catchLHandCollNode')
        self.bodyColEventNames.append('ltCatch-%s' % 'catchLHandCollNode')        
        self.ltLHandCollNode.setCollideMask(VineGameGlobals.SpiderBitmask)
        self.ltRHandCollNode = CollisionNode('catchRHandCollNode')
        self.bodyColEventNames.append('ltCatch-%s' % 'catchRHandCollNode')        
        self.ltRHandCollNode.setCollideMask(VineGameGlobals.SpiderBitmask)
        legsCollNodepath = lt.attachNewNode(self.ltLegsCollNode)
        legsCollNodepath.hide()
        # get the 1000-lod head node
        head = base.localAvatar.getHeadParts().getPath(2)
        headCollNodepath = head.attachNewNode(self.ltHeadCollNode)
        headCollNodepath.hide()
        # get the 1000-lod nodes for the torso
        torso = base.localAvatar.getTorsoParts().getPath(2)
        torsoCollNodepath = torso.attachNewNode(self.ltTorsoCollNode)
        torsoCollNodepath.hide()
        self.torso = torsoCollNodepath
        # get the 1000-lod nodes for the left hand
        lHand = base.localAvatar.getLeftHands()[0]
        lHandCollNodepath = lHand.attachNewNode(self.ltLHandCollNode)
        lHandCollNodepath.hide()
        # get the 1000-lod nodes for the right hand
        rHand = base.localAvatar.getRightHands()[0]
        rHandCollNodepath = rHand.attachNewNode(self.ltRHandCollNode)
        rHandCollNodepath.hide()
        # add collision nodepaths to the traverser
        lt.cTrav.addCollider(legsCollNodepath, handler)
        lt.cTrav.addCollider(headCollNodepath, handler)
        lt.cTrav.addCollider(lHandCollNodepath, handler)
        lt.cTrav.addCollider(rHandCollNodepath, handler)
        lt.cTrav.addCollider(torsoCollNodepath, handler)        
        if self.ShowToonSpheres:
            legsCollNodepath.show()
            headCollNodepath.show()
            lHandCollNodepath.show()
            rHandCollNodepath.show()
            torsoCollNodepath.show()
            
        self.ltLegsCollNode.addSolid( CollisionSphere(0,0, radius, radius))
        self.ltHeadCollNode.addSolid( CollisionSphere(0,0,0, radius))
        self.ltLHandCollNode.addSolid( CollisionSphere(0,0,0, 2*radius/3.))
        self.ltRHandCollNode.addSolid( CollisionSphere(0,0,0, 2*radius/3.))
        self.ltTorsoCollNode.addSolid( CollisionSphere(0,0,radius, radius * 2))        
        self.toonCollNodes = [legsCollNodepath,
                              headCollNodepath,
                              lHandCollNodepath,
                              rHandCollNodepath,
                              torsoCollNodepath
                              ]
        for eventName in self.bodyColEventNames:
            self.accept(eventName, self.toonHitSomething)
            pass
        
        self.introTrack = self.getIntroTrack()
        self.introTrack.start()
        
    def offstage(self):
        self.notify.debug("offstage")
        # stop the minigame; parent things to hidden, stop the
        # music...
        for panel in self.scorePanels:
            panel.cleanup()
        del self.scorePanels

        self.gameBoard.hide()
        # the base class parents the toons to hidden, so consider
        # calling it last
        DistributedMinigame.offstage(self)

        self.arrowKeys.destroy()
        del self.arrowKeys        

        # reset the toons' LODs and show their dropshadows again
        for avId in self.avIdList:
            av = self.getAvatar(avId)
            if av:
                av.dropShadow.show()
                av.resetLOD() # we'll use the head frames instead

        for treasure in self.treasures:
            treasure.destroy()
        del self.treasures

        # cleanup gravity physics
        base.physicsMgr.removeLinearForce(self.gravityForce)
        self.gravityForceFNP.removeNode()

        # restore localToon's collision setup
        for collNode in self.toonCollNodes:
            while collNode.node().getNumSolids():
                collNode.node().removeSolid(0)
            base.localAvatar.cTrav.removeCollider(collNode)
        del self.toonCollNodes

        for eventName in self.bodyColEventNames:
            self.ignore(eventName)

        # just to be safe - grw
        self.ignoreAll()        

        if self.introTrack.isPlaying():
            self.introTrack.finish()
        del self.introTrack

        for vine in self.vines:
            vine.stopSwing()
            vine.hide()

        self.startPlatform.hide()
        self.endPlatform.hide()
        
    def handleDisabledAvatar(self, avId):
        """This will be called if an avatar exits unexpectedly"""
        self.notify.debug("handleDisabledAvatar")
        self.notify.debug("avatar " + str(avId) + " disabled")
        # clean up any references to the disabled avatar before he disappears

        # then call the base class
        DistributedMinigame.handleDisabledAvatar(self, avId)

    def updateToonInfo( self, avId, vineIndex = None, vineT =None, posX = None, posZ = None, facingRight = None, climbDir = None, velX = None, velZ = None, fallingInfo = None):
        """
        Update the toon info, if it's None don't change it
        """
        newVineIndex = vineIndex
        newVineT = vineT
        newPosX = posX
        newPosZ = posZ
        newFacingRight = facingRight
        newClimbDir = climbDir
        newVelX = velX
        newVelZ = velZ
        newFallingInfo = fallingInfo
        oldInfo = None
        if self.toonInfo.has_key(avId):
            oldInfo = self.toonInfo[avId]
            if vineIndex == None:
                newVineIndex = oldInfo[0]
            if vineT == None:
                newVineT = oldInfo[1]
            if posX == None:
                newPosX = oldInfo[2]
            if posZ == None:
                newPosZ = oldInfo[3]
            if facingRight == None:
                newFacingRight = oldInfo[4]
            if climbDir == None:
                newClimbDir = oldInfo[5]
            if velX == None:
                newVelX = oldInfo[6]
            if velZ == None:
                newVelZ = oldInfo[7]
            if fallingInfo == None:
                newFallingInfo = oldInfo[8]
            
            
        if (newVineIndex < -1) or (newVineIndex >= len(self.vines)):
            self.notify.warning('invalid vineIndex for %d, forcing 0' % avId)
            newVineIndex = 0
        if (newVineT < 0) or (newVineT > 1):
            self.notify.warning('invalid vineT for %d, setting to 0' % avId)
        if not (newFacingRight == 0 or newFacingRight == 1):
            self.notify.warning('invalid facingRight for %d, forcing to 1' % avId)
            newFacingRight = 1
        if (newPosX < -1000) or (newPosX > 2000):
            self.notify.warning('invalid posX for %d, forcing to 0' % avId)
            newPosX = 0
        if (newPosZ < -100) or (newPosZ > 1000):
            self.notify.warning('invalid posZ for %d, forcing to 0' % avId)
            newPosZ = 0
        if (newVelX < -1000) or (newVelX > 1000):
            self.notify.warning('invalid velX %s for %d, forcing to 0' % (newVelX, avId))
            newVelX = 0
        if (newVelZ < -1000) or (newVelZ > 1000):
            self.notify.warning('invalid velZ %s for %d, forcing to 0' % (newVelZ, avId))
            newVelZ = 0
        if (newFallingInfo < self.FallingNot) or (newFallingInfo > self.FallingBat):
            self.notify.warning('invalid fallingInfo for %d, forcing to 0' % avId)
            newFallingInfo = 0                
        newInfo = [newVineIndex, newVineT, newPosX, newPosZ, newFacingRight, newClimbDir, newVelX, newVelZ, newFallingInfo]
        
        self.toonInfo[avId] = newInfo

        if oldInfo:
            self.applyToonInfoChange(avId, newInfo, oldInfo)

        self.sanityCheck()            

    def applyToonInfoChange(self, avId, newInfo, oldInfo):
        """
        we have the newInfo, lets check for changes
        """
        if not self.isInPlayState():
            return

        oldVine = oldInfo[0]
        newVine = newInfo[0]
        #self.notify.debug('%s %s %s' % (avId, newInfo, oldInfo))
        if not (oldVine == newVine):
            # we have a vine change
            self.notify.debug('we have a vine change')
            if oldVine == -1:
                # we were jumping and now attaching to a new vine
                self.notify.debug(' we were jumping and now attaching to a new vine')
                newVineT = newInfo[1]
                newFacingRight = newInfo[4]
                self.vines[newVine].attachToon(avId, newVineT, newFacingRight)
                if newVine == VineGameGlobals.NumVines - 1:
                    # toon has reached the end vine, do an ending movie
                    self.doEndingTrackTask(avId)
                    pass
            elif newVine == -1:
                # we were attached to a vine and we are now jumping
                self.notify.debug('we were attached to a vine and we are now jumping')
                curInfo = self.vines[oldVine].getAttachedToonInfo(avId)
                self.vines[oldVine].detachToon(avId)
                if not (avId == self.localAvId):
                    posX = newInfo[2]
                    posZ = newInfo[3]
                    velX = newInfo[6]
                    velZ = newInfo[7]                    
                    self.makeOtherToonJump(avId, posX, posZ, velX, velZ)
            else:
                self.notify.warning('should not happen directly going from one vine to another')
                self.vines[oldVine].detachToon(avId)
                newVineT = newInfo[1]
                newFacingRight = newInfo[4]
                self.vines[newVine].attachToon(avId, newVineT, newFacingRight)
        elif newVine == oldVine and newInfo[4] != oldInfo[4]:
            self.notify.debug('# still on the same vine, but we changed facing')
            self.vines[newVine].changeAttachedToonFacing(avId,  newInfo[4])
        elif newVine >= 0:
            # still attached to a vine, changing T
            # self.notify.debug('# still attached to a vine, changing T')
            self.vines[newVine].changeAttachedToonT(avId, newInfo[1])
        else:
            # we are still falling
            self.notify.debug('we are still falling')
            # try it with physics handling falling for other toons
            if oldInfo[8] != newInfo[8]:
                #we hit a bat or a spider
                if not (avId == self.localAvId):
                    posX = newInfo[2]
                    posZ = newInfo[3]
                    velX = newInfo[6]
                    velZ = newInfo[7]                    
                    self.makeOtherToonFallFromMidair(avId, posX, posZ, velX, velZ)                

    def sanityCheck(self):
        """
        make sure the vines and the game are in agreement
        """
        if not self.isInPlayState():
            return
        
        for avId in self.toonInfo.keys():
            myVineIndex = self.toonInfo[avId][0]            
            foundVines = []
            foundVineIndex = -1
            for curVine in xrange(len(self.vines)):
                curInfo = self.vines[curVine].getAttachedToonInfo(avId)
                if curInfo:
                    foundVines.append(curVine)
                    foundVineIndex = curVine
            if len(foundVines) > 1:
                self.notify.warning('toon %d is attached to vines %s' % (avId, foundVines))
            if not (foundVineIndex == myVineIndex) and not (myVineIndex == VineGameGlobals.NumVines - 1):
                self.notify.warning('avId=%d foundVineIndex=%d != myVineIndex=%d' % (avId, foundVineIndex, myVineIndex))

    def getVineAndVineInfo(self, avId):
        """
        returns -1, None if avId is not attached to any vine
        otherwise returns vineIndex and the attachedToonInfo
        """
        retVine = -1
        retInfo = None
        for curVine in xrange(len(self.vines)):
            curInfo = self.vines[curVine].getAttachedToonInfo(avId)
            if curInfo:
                retVine = curVine
                retInfo = curInfo
                break

        #one quick sanity check
        if self.toonInfo[avId][0] != retVine:
            self.notify.warning("getVineAndVineInfo don't agree, toonInfo[%d]=%s, retVine=%d"
                                % (avId, self.toonInfo[avId][0], retVine))

        return retVine, curInfo
            
    def setGameReady(self):
        if not self.hasLocalToon: return
        self.notify.debug("setGameReady")
        if DistributedMinigame.setGameReady(self):
            return

        self.toonOffsets = {}
        self.toonOffsetsFalling = {}
        # all of the remote toons have joined the game;
        # it's safe to show them now.
        for index in xrange(self.numPlayers):
            avId = self.avIdList[index]
            # Find the actual avatar in the cr
            toon = self.getAvatar(avId)
            if toon:
                toon.reparentTo(render)
                toon.setPos(0,0,0)
                toon.setHpr(0,0,0)

                self.toonOffsets[avId] = self.calcToonOffset(toon)

                # hide their dropshadows again
                toon.dropShadow.hide()               
                newHeadFrame = VineHeadFrame.VineHeadFrame(toon)
                newHeadFrame.hide()
                self.headFrames[avId] = newHeadFrame
                toon.useLOD(1000) # make sure they show up in the radar, if we don't use head frames
                toon.setX(-100) # put him off screen
                
    def calcToonOffset(self, toon):
        """Return how much the left hand is offset from the toon."""
        offset = Point3(0,0,0)
        toon.pose('swing', 74)
        leftHand = toon.find('**/leftHand')
        if not leftHand.isEmpty():
            offset = leftHand.getPos(toon)
        return offset
                
    def setGameStart(self, timestamp):
        if not self.hasLocalToon: return
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigame.setGameStart(self, timestamp)
        # all players have finished reading the rules,
        # and are ready to start playing.
        # transition to the appropriate state
        if self.introTrack.isPlaying():
            self.introTrack.finish()
        
        self.gameFSM.request("play")

    # these are enter and exit functions for the game's
    # fsm (finite state machine)

    def enterOff(self):
        self.notify.debug("enterOff")

    def exitOff(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # hide the laff meter
        if base.localAvatar.laffMeter:
            base.localAvatar.laffMeter.stop()
        
        self.createRadar()

        # Initialize the scoreboard
        self.scores = [0] * self.numPlayers
        spacing = .4
        for i in xrange(self.numPlayers):
            avId = self.avIdList[i]
            avName = self.getAvatarName(avId)
            scorePanel = \
                       MinigameAvatarScorePanel.MinigameAvatarScorePanel(avId,
                                                                         avName)
            scorePanel.setScale(.9)
            scorePanel.setPos(.75 - spacing*((self.numPlayers - 1) - i), 0.0, .85)
            # make the panels slightly transparent
            scorePanel.makeTransparent(.75)
            self.scorePanels.append(scorePanel)

        for vine in self.vines:
            vine.show()
            vine.startSwing()

        self.startBatIvals()

        for avId in self.avIdList:
            toon = self.getAvatar(avId)
            if toon:
                pass
                if avId == self.localAvId:
                   self.attachLocalToonToVine(0, VineGameGlobals.VineStartingT)
                else:
                    self.vines[0].attachToon(avId, VineGameGlobals.VineStartingT, self.lastJumpFacingRight)

        # Start counting down the game clock,
        # call timerExpired when it reaches 0
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posInTopRightCorner()
        self.timer.setTime(VineGameGlobals.GameDuration)
        self.timer.countdown(VineGameGlobals.GameDuration, self.timerExpired)

        # Start music
        base.playMusic(self.music, looping = 1, volume = 0.9)

        self.__spawnUpdateLocalToonTask()

    def exitPlay(self):
        self.notify.debug("exitPlay")
        # show the laff meter
        if base.localAvatar.laffMeter:
            base.localAvatar.laffMeter.start()    
        self.timer.stop()
        self.timer.destroy()
        del self.timer           
        self.clearLocalPhysics()
        for ival in self.batIvals:
            ival.finish()
            del ival
        self.batIvals = []

        # Stop music
        self.music.stop()

    def enterWaitShowScores(self):
        self.notify.debug("enterWaitShowScores")
        pass

    def exitWaitShowScores(self):
        self.notify.debug("exitWaitShowScores")
        pass

    def enterShowScores(self):
        self.notify.debug("enterShowScores")

        # lerp up the goal bar, score panels
        lerpTrack = Parallel()
        lerpDur = .5
        
        # score panels
        # top/bottom Y
        tY = .6; bY = -.05
        # left/center/right X
        lX = -.5; cX = 0; rX = .5
        scorePanelLocs = (
            ((cX,bY),),
            ((lX,bY),(rX,bY)),
            ((cX,tY),(lX,bY),(rX,bY)),
            ((lX,tY),(rX,tY),(lX,bY),(rX,bY)),
            )
        scorePanelLocs = scorePanelLocs[self.numPlayers - 1]
        for i in xrange(self.numPlayers):
            panel = self.scorePanels[i]
            pos = scorePanelLocs[i]
            lerpTrack.append(Parallel(
                LerpPosInterval(panel, lerpDur, Point3(pos[0],0,pos[1]),
                                blendType='easeInOut'),
                LerpScaleInterval(panel, lerpDur,
                                  Vec3(panel.getScale())*2.,
                                  blendType='easeInOut'),
                ))

        self.showScoreTrack = Parallel(
            lerpTrack,
            Sequence(Wait(VineGameGlobals.ShowScoresDuration),
                     Func(self.gameOver),
                     ),
            )

        self.showScoreTrack.start()

    def exitShowScores(self):
        # calling finish() here would cause problems if we're
        # exiting abnormally, because of the gameOver() call
        self.showScoreTrack.pause()
        del self.showScoreTrack
        
        
    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.destroyRadar()
        self.__killUpdateLocalToonTask()
        self.cleanupEndingTracks()
        for avId in self.headFrames:
            self.headFrames[avId].destroy()

    def exitCleanup(self):
        pass

    def __spawnUpdateLocalToonTask(self):
        #self.__initPosBroadcast()
        taskMgr.remove(self.UpdateLocalToonTask)
        taskMgr.add(self.__updateLocalToonTask, self.UpdateLocalToonTask)

    def __killUpdateLocalToonTask(self):
        taskMgr.remove(self.UpdateLocalToonTask)

    def clearLocalPhysics(self):
        if self.localPhysicsNP:
            an = self.localPhysicsNP.node()
            base.physicsMgr.removePhysicalNode(an)
            self.localPhysicsNP.removeNode()
            del self.localPhysicsNP
            self.localPhysicsNP = None
        if hasattr(self, 'treasureCollNodePath') and self.treasureCollNodePath:
            self.treasureCollNodePath.removeNode()
        
    def handleLocalToonFellDown(self):
        self.notify.debug('attaching toon back to vine since he fell')
        self.fallSound.play()
        vineToAttach = self.lastJumpVine
        if self.toonInfo[self.localAvId][8] == self.FallingSpider:
            # if the vine we will connect to has a spider, move it 1 to the left
            if self.vines[vineToAttach].hasSpider:
                vineToAttach -= 1
        if vineToAttach < 0:
            vineToAttach = 0
        self.attachLocalToonToVine(vineToAttach, VineGameGlobals.VineFellDownT)
        #self.vines[0].attachToon(base.localAvatar.doId, 0.5)
        #self.clearLocalPhysics()

    def makeCameraFollowJumpingToon(self):
        camera.setHpr(0,0,0)

        if self.TwoVineView:
            camera.setPos(self.cameraTwoVineSidePos)
            
            maxVine = self.lastJumpVine + 1
            if maxVine >= len(self.vines):
                maxVine = len(self.vines) - 1
            maxX = self.defaultMaxX
            if self.vines:
                maxX = self.vines[maxVine].getX()

            minVine = self.lastJumpVine - 1
            if minVine < 0:
                minVine = 0
            minX = 0
            if self.vines:
                minX = self.vines[minVine].getX()
        
            camera.setX(base.localAvatar.getX(render))
            if camera.getX() > maxX:
                camera.setX(maxX)
            if camera.getX() < minX:
                camera.setX(minX)
        else:
            camera.setPos(self.cameraSidePos)
            
            maxVine = self.lastJumpVine + 1
            if maxVine >= len(self.vines):
                maxVine = len(self.vines) - 1
            maxX = self.vines[maxVine].getX()

            minVine = self.lastJumpVine - 1
            if minVine < 0:
                minVine = 0
            minX = self.vines[minVine].getX()
        
            camera.setX(base.localAvatar.getX(render))
            if camera.getX() > maxX:
                camera.setX(maxX)
            if camera.getX() < minX:
                camera.setX(minX)

    def __updateOtherToonsClimbing(self):
        for avId in self.toonInfo.keys():
            if avId == self.localAvId:
                continue
            toonInfo = self.toonInfo[avId]
            vineIndex = toonInfo[0]
            if vineIndex == -1:
                continue
            climbDir = toonInfo[5]
            if climbDir == None or climbDir == 0:
                continue
            curT = toonInfo[1]
            dt = globalClock.getDt()
            diffT = 0
            baseVerticalRate = self.ToonVerticalRate
            if climbDir == -1:
                diffT -= baseVerticalRate * dt
            if climbDir == 1:
                diffT += baseVerticalRate * dt

            newT = curT + diffT
            if newT > 1:
                newT = 1
            if newT < 0:
                newT = 0
            
            if not newT == curT:
                toonInfo[1] = newT
                #self.notify.debug('%s climbDir=%s newT=%s' % (avId, climbDir, newT))
                self.vines[vineIndex].changeAttachedToonT(avId, newT)
            
    def __updateLocalToonTask(self, task):
        #import pdb; pdb.set_trace()2
        dt = globalClock.getDt()

        self.updateRadar()
        self.__updateOtherToonsClimbing()
        for bat in self.bats:
            bat.checkScreech()

        #import pdb; pdb.set_trace()
        #base.localAvatar.cnode.broadcastPosHprXyh()
        #self.notify.debug('self.localPhysicsNP = %s' % self.localPhysicsNP)
        # check if we've fallen off
        if self.localPhysicsNP:
            pos = self.localPhysicsNP.getPos(render)
            #self.notify.debug('avPosInRender = %s' % pos)
            if pos[2] < 0:
                self.handleLocalToonFellDown()

        avId = self.localAvId
        curInfo = None
        for vineIndex in xrange(len(self.vines)):
            curInfo = self.vines[vineIndex].getAttachedToonInfo(avId)
            if curInfo:
                break
        if not curInfo:
            if not self.endingTracks.has_key(avId):
                # local toon is falling
                self.makeCameraFollowJumpingToon()
                #pos = base.localAvatar.getPos(render)
                if self.localPhysicsNP:
                    pos = self.localPhysicsNP.getPos(render)
                    #self.d_setFallingPos( self.localAvId, pos[0], pos[2])
        else:
            # local toon is on a vine
            curT = curInfo[0]
            diffT = 0
            baseVerticalRate = self.ToonVerticalRate
            # do not left him move once he reaches end vine
            onEndVine =  vineIndex == len(self.vines) - 1
            
            if self.arrowKeys.upPressed() and not onEndVine and self.isInPlayState():
                diffT -= baseVerticalRate * dt
            if self.arrowKeys.downPressed() and not onEndVine and self.isInPlayState():
                diffT += baseVerticalRate * dt

            #self.notify.debug('dt=%s diffT = %s' % (dt,diffT))
            newT = curT + diffT
            if newT > 1:
                newT = 1
            if newT < 0:
                newT = 0

            oldClimbDir = self.getClimbDir(avId)

            climbDir = 0
            if diffT < 0:
                climbDir = -1
            elif diffT > 0:
                climbDir = 1

            if not newT == curT:
                #self.vines[vineIndex].attachToon(avId, newT, self.lastJumpFacingRight)
                self.vines[vineIndex].changeAttachedToonT(avId, newT)
            #self.notify.debug('getClimbDir(%s) = %s' % (avId, self.getClimbDir(avId)))
            # we need to tell other clients we've stopped moving
            if newT != curT or (self.getClimbDir(avId) and not curT == 1.0) or\
               oldClimbDir != climbDir:
                if oldClimbDir != climbDir:
                    self.sendNewVineTUpdateAsap = True
                self.b_setNewVineT(avId, newT, climbDir)                
                

        return task.cont

    def setupCollisions(self, anp):
        fromObject = anp.attachNewNode(CollisionNode('colNode'))
        fromObject.node().addSolid(CollisionSphere(0, 0, 0, self.LocalPhysicsRadius))
        fromCollideMask = ToontownGlobals.PieBitmask
        #fromObject.show()
        self.notify.debug('fromCollideMask = %s' % fromCollideMask)
        fromObject.node().setFromCollideMask(fromCollideMask)

        #debugAxis = loader.loadModel('models/misc/xyzAxis')
        #debugAxis.reparentTo(base.localAvatar)
        #debugAxis.setScale(self.LocalPhysicsRadius / 10.0)

        self.handler = CollisionHandlerEvent()
        #self.handler.addInPattern('%fn-into-%in')
        self.handler.addInPattern('%fn-into')
        
        #self.handler = PhysicsCollisionHandler()
        #self.handler.setStaticFrictionCoef(0.1)
        #self.handler.setDynamicFrictionCoef(0.1)
        #self.handler.addCollider(fromObject, anp)

        base.cTrav.setRespectPrevTransform(True)
        base.cTrav.addCollider(fromObject, self.handler)
        #eventName = '%s-into-SwingVine' % fromObject.getName()
        #self.notify.debug('eventName = %s' % eventName)
        #self.accept(eventName, self.swingVineEnter)

        eventName = '%s-into' % fromObject.getName()
        self.accept(eventName, self.swingVineEnter)        

        height = base.localAvatar.getHeight()
        self.treasureSphereName = "treasureCollider" #% self.localAvId

        center = Point3(0, 0, 0)

        radius = VineTreasure.VineTreasure.RADIUS
        self.treasureCollSphere = CollisionSphere(center[0], center[1], center[2], radius)

        # Make the sphere intangible
        self.treasureCollSphere.setTangible(0)
        self.treasureCollNode = CollisionNode(self.treasureSphereName)
        self.treasureCollNode.setFromCollideMask(ToontownGlobals.WallBitmask)
        self.treasureCollNode.addSolid(self.treasureCollSphere)
        self.treasureCollNodePath = self.torso.attachNewNode(self.treasureCollNode)

        #self.treasureCollNodePath.show()
        #self.torso.show()

        self.treasureHandler = CollisionHandlerEvent()
        self.treasureHandler.addInPattern('%fn-intoTreasure')            
        base.cTrav.addCollider(self.treasureCollNodePath, self.treasureHandler)

        eventName = '%s-intoTreasure' % self.treasureCollNodePath.getName()
        self.notify.debug('eventName = %s' % eventName)
        self.accept(eventName, self.treasureEnter)

    def getFocusCameraPos(self, vineIndex, facingRight):
        retPos = Point3(0,0,0)
        if self.TwoVineView:
            pos = self.vines[vineIndex].getPos()
            retPos = Point3(self.cameraTwoVineSidePos)
            if vineIndex == 0:
                # ignore his facing
                nextVinePos = self.vines[vineIndex + 1].getPos()
                newX = (pos.getX() + nextVinePos.getX()) / 2.0
                newX -= self.cameraTwoVineAdj
                retPos.setX(newX)
            elif vineIndex == VineGameGlobals.NumVines - 1:
                # ignore his facing
                nextVinePos = self.vines[vineIndex].getPos()
                nextVinePos.setX( nextVinePos.getX() + VineGameGlobals.VineXIncrement)
                newX = (pos.getX() + nextVinePos.getX()) / 2.0
                newX += self.cameraTwoVineAdj
                retPos.setX(newX)
            else:
                otherVineIndex = vineIndex - 1
                if self.lastJumpFacingRight:
                    otherVineIndex = vineIndex + 1
                nextVinePos = self.vines[otherVineIndex].getPos()
                newX = (pos.getX() + nextVinePos.getX()) / 2.0
                if self.lastJumpFacingRight:
                    newX -= self.cameraTwoVineAdj
                else:
                    newX += self.cameraTwoVineAdj
                retPos.setX(newX)
        else:
            pos = self.vines[vineIndex].getPos()
            retPos.setX(pos.getX())
        self.notify.debug('getFocusCameraPos returning %s' % retPos)
        return retPos
            
    def focusCameraOnVine(self,vineIndex):
        """Focus the camera on a  particular vine."""
        assert self.notify.debugStateCall(self)
        camera.setHpr(0,0,0)
        newCameraPos = self.getFocusCameraPos(vineIndex,self.lastJumpFacingRight)
        camera.setPos(newCameraPos)

    def attachLocalToonToVine(self,vineIndex, vineT, focusCameraImmediately = True, playSfx = False):
        self.notify.debug('focusCameraImmediately = %s' % focusCameraImmediately)
        if playSfx:
            self.catchSound.play()
        self.clearLocalPhysics()
        vine = self.vines[vineIndex]
        # this will be done in applyToonInfoChange
        #vine.attachToon(base.localAvatar.doId, vineT, self.lastJumpFacingRight)
        self.lastJumpVine = -1
        self.lastJumpPos = None
        self.lastJumpT = 0
        if focusCameraImmediately:
            self.focusCameraOnVine(vineIndex)
        ### tell the other players our new vine
        self.b_setNewVine(self.localAvId, vineIndex, vineT,  self.lastJumpFacingRight)

    def setupJumpingTransitionIval(self, vineIndex):
        """Setup the interval that transitions the toon from attached to jumping."""
        assert self.notify.debugStateCall()
        self.doingJumpTransition = False
        self.localToonJumpAnimIval = self.createJumpingTransitionIval( vineIndex)
        if self.localToonJumpAnimIval:
            self.doingJumpTransition = True
            
    def createJumpingTransitionIval(self, vineIndex):
        """Return the interval that transitions the toon from attached to jumping."""
        retval = None
        curInfo = self.vines[vineIndex].getAttachedToonInfo(base.localAvatar.doId)
        if curInfo:
            swingSeq = curInfo[6]
            if swingSeq:
                curFrame = -1
                for i in range(len(swingSeq)):
                    self.notify.debug('testing actor interval i=%d' % i)
                    actorIval = swingSeq[i]
                    if not actorIval.isStopped():
                        testFrame = actorIval.getCurrentFrame()
                        self.notify.debug('actor ival is not stopped, testFrame=%f' % testFrame)                        
                        if testFrame:
                            curFrame = testFrame
                            break
                if curFrame > -1:
                    duration = 0.25
                    if curFrame > self.ToonMaxRightFrame:
                        desiredFps = abs(self.JumpingFrame - curFrame) / duration
                        playRate = desiredFps / 24.0
                        retval = ActorInterval( base.localAvatar,
                                                'swing',
                                                startFrame = curFrame,
                                                endFrame = self.JumpingFrame,
                                                playRate = playRate,)
                    else:
                        # stop the toon from swinging all the way to the right then a bit left
                        numFrames = curFrame +1
                        numFrames += SwingVine.SwingVine.MaxNumberOfFramesInSwingAnim - \
                                     self.JumpingFrame +1
                        desiredFps = numFrames / duration
                        playRate = desiredFps / 24.0
                        toonJump1 = ActorInterval( base.localAvatar,
                                                    'swing',
                                                    startFrame = curFrame,
                                                    endFrame = 0,
                                                    playRate = playRate,)
                        toonJump2 = ActorInterval( base.localAvatar,
                                                   'swing',
                                                   startFrame = SwingVine.SwingVine.MaxNumberOfFramesInSwingAnim - 1,
                                                   endFrame = self.JumpingFrame,
                                                   playRate = playRate,)
                        retval = Sequence(toonJump1, toonJump2)
        return retval

    def detachLocalToonFromVine(self, vineIndex, facingRight):
        """Detach the local toon from the vine."""
        vine  = self.vines[vineIndex]
        self.lastJumpVine = vineIndex
        self.lastJumpTime = self.getCurrentGameTime()
        self.curFrame = base.localAvatar.getCurrentFrame()
        curInfo = vine.getAttachedToonInfo(base.localAvatar.doId)
        if curInfo:
            self.lastJumpPos = curInfo[1]
            self.lastJumpT = curInfo[0]
        else:
            self.lastJumpPos = None
            self.lastJumpT = 0
            self.notify.warning('vine %d failed get tooninfo %d' % (vineIndex, base.localAvatar.doId))
        self.setupJumpingTransitionIval(vineIndex) # we must do this before we detach the toon
        self.vines[vineIndex].detachToon(base.localAvatar.doId)

    def treasureEnter(self, entry):
        self.notify.debug('---- treasure Enter ---- ')
        self.notify.debug('%s' % entry)
        name = entry.getIntoNodePath().getName()
        parts = name.split('-')
        if len(parts) < 3:
            self.notify.debug('collided with %s, but returning' % name)
            return
        if not int(parts[1]) == self.doId:
            self.notify.debug("collided with %s, but doId doesn't match" % name)
            return
        treasureNum = int(parts[2])
        self.__treasureGrabbed(treasureNum)
        pass
        
    def swingVineEnter(self, entry):
        self.notify.debug('%s' % entry)
        self.notify.debug('---- swingVine Enter ---- ')
        name = entry.getIntoNodePath().getName()
        parts = name.split('-')
        if len(parts) < 3:
            self.notify.debug('collided with %s, but returning' % name)
            return
        vineIndex = int(parts[1])
        if vineIndex <0 or vineIndex >= len(self.vines):
            self.notify.warning('invalid vine index %d' % vineIndex)
            return
        if vineIndex == self.lastJumpVine:
            if self.lastJumpPos:
                diff = self.lastJumpPos - entry.getSurfacePoint(render)
                # don't collide oo soon from our jump point
                if diff.length() < self.LocalPhysicsRadius:
                    return
            if self.getCurrentGameTime() - self.lastJumpTime < VineGameGlobals.JumpTimeBuffer:
                # we may get here if we have a fast moving vine,
                # lets check time  too
                return
        fallingInfo = self.toonInfo[self.localAvId][8]
        if fallingInfo == self.FallingSpider or fallingInfo== self.FallingBat:
            #don't let them catch the vine if they hit a spider or bat
            return
        if abs(self.lastJumpVine - vineIndex) > 1:
            # if we skipped a vine, don't let him catch it
            return
        vine = self.vines[vineIndex]
        vineT = vine.calcTFromTubeHit(entry)
        self.attachLocalToonToVine(vineIndex, vineT, False, playSfx = True)
        self.setupAttachingToVineCamIval(vineIndex,  self.lastJumpFacingRight)

    def makeOtherToonJump( self, avId, posX, posZ, velX, velZ):
        # assert self.notify.debugStateCall(self)
        if not self.otherToonPhysics.has_key(avId):
            an = ActorNode('other-physics%s' % avId)
            anp = render.attachNewNode(an)
            base.physicsMgr.attachPhysicalNode(an)            
            self.otherToonPhysics[avId] = (an, anp)
        an, anp = self.otherToonPhysics[avId]
        anp.setPos(posX, 0, posZ)
        av = base.cr.doId2do.get(avId)
        if av:
            av.reparentTo(anp)
            av.setPos(-self.toonOffsets[self.localAvId])
            av.pose('swing',self.JumpingFrame)
            self.notify.debug('pose set to swing jumping frame.')
        if velX >= 0:
            anp.setH(-90)
        else:
            anp.setH(90)
        physObject = an.getPhysicsObject()
        physObject.setVelocity( velX, 0, velZ)
        #physObject.setPosition( 0, 0, 0)

    def makeOtherToonFallFromMidair( self, avId, posX, posZ, velX, velZ):
        # assert self.notify.debugStateCall(self)
        if not self.otherToonPhysics.has_key(avId):
            an = ActorNode('other-physics%s' % avId)
            anp = render.attachNewNode(an)
            base.physicsMgr.attachPhysicalNode(an)            
            self.otherToonPhysics[avId] = (an, anp)
        an, anp = self.otherToonPhysics[avId]
        anp.setPos(posX, 0, posZ)
        av = base.cr.doId2do.get(avId)
        if av:
            av.reparentTo(anp)
            av.setPos(-self.toonOffsets[self.localAvId])
        if velX >= 0:
            anp.setH(-90)
        else:
            anp.setH(90)
        physObject = an.getPhysicsObject()
        physObject.setVelocity( velX, 0, velZ)
        #physObject.setPosition( 0, 0, 0)        

    def makeLocalToonJump(self, vineIndex, t, pos, normal):
        self.jumpSound.play()
        self.clearChangeFacingInterval()
        self.clearAttachingToVineCamIval()
        an = ActorNode('av-physics')
        anp = render.attachNewNode(an)
        anp.setPos(pos)
        base.localAvatar.reparentTo(anp)
        base.localAvatar.setPos(-self.toonOffsets[self.localAvId])
        #base.localAvatar.pose('swing',self.JumpingFrame)
        if normal.getX() >= 0:
            self.lastJumpFacingRight = True
            anp.setH(-90)
        else:
            anp.setH(90)
            self.lastJumpFacingRight = False
        base.physicsMgr.attachPhysicalNode(an)
        physObject = an.getPhysicsObject()

        velocity = normal * self.JumpSpeed;
        # lets make him go slower the closer he is to the top of the vine
        velocity *= t
        
        self.notify.debug('jumping from vine with velocity of %s' % velocity)
        physObject.setVelocity(velocity)        
        self.localPhysicsNP = anp
        self.setupCollisions(anp)

        # make him switch quickly to the jumping frame
        if self.doingJumpTransition:
            self.localToonJumpAnimIval.start()        
        else:
            base.localAvatar.pose('swing', self.JumpingFrame)

        self.b_setJumpingFromVine(self.localAvId, vineIndex,
                                  self.lastJumpFacingRight,
                                  pos[0], pos[2],
                                  velocity[0], velocity[2])

    def makeLocalToonFallFromVine(self, fallingInfo):
        self.clearAttachingToVineCamIval()
        self.clearChangeFacingInterval()
        vineIndex, vineInfo = self.getVineAndVineInfo(self.localAvId)
        if vineIndex == -1:
            self.notify.warning('we are not attached to a vine')
            return
        pos = vineInfo[1]
        self.detachLocalToonFromVine(vineIndex, self.lastJumpFacingRight)
        self.clearChangeFacingInterval()        
        an = ActorNode('av-physics')
        anp = render.attachNewNode(an)
        anp.setPos(vineInfo[1])        
        base.localAvatar.reparentTo(anp)
        base.localAvatar.setPos(-self.toonOffsets[self.localAvId])
        if self.lastJumpFacingRight:
            anp.setH(-90)
        else:
            anp.setH(90)
        
        base.physicsMgr.attachPhysicalNode(an)
        physObject = an.getPhysicsObject()
        velocity = Vec3(0,0,-0.1) # make him fall straight down
        physObject.setVelocity(velocity)
        self.localPhysicsNP = anp
        #deliberately do not setupCollisions

        self.b_setFallingFromVine(self.localAvId, vineIndex,
                                  self.lastJumpFacingRight,
                                  pos[0], pos[2],
                                  velocity[0], velocity[2], fallingInfo)

    def makeLocalToonFallFromMidair(self, fallingInfo):
        vineIndex, vineInfo = self.getVineAndVineInfo(self.localAvId)
        if not vineIndex == -1:
            self.notify.warning(' makeLocalToonFallFromMidair we are still attached to a vine')
            return
        if not self.localPhysicsNP:
            self.notify.warning('self.localPhysicsNP is invalid')
            return
        pos = self.localPhysicsNP.getPos()
        an = self.localPhysicsNP.node()
        physObject = an.getPhysicsObject()
        velocity = Vec3(0,0,-0.1) # make him fall straight down
        physObject.setVelocity(velocity)

        self.b_setFallingFromMidair(self.localAvId, 
                                  self.lastJumpFacingRight,
                                  pos[0], pos[2],
                                  velocity[0], velocity[2], fallingInfo)        
            

    def changeLocalToonFacing(self,vineIndex, swingVineInfo, newFacingRight):
        """
        we should only get here if we are definitely changing facing
        """
        self.lastJumpFacingRight = newFacingRight
        self.attachLocalToonToVine(vineIndex, swingVineInfo[0], focusCameraImmediately = False)
        self.setupChangeFacingInterval(vineIndex, newFacingRight)

    def upArrowKeyHandler(self):
        """Handle pressing the up arrow key."""
        self.sendNewVineTUpdateAsap = True

    def downArrowKeyHandler(self):
        """Handle pressing the down arrow key."""    
        self.sendNewVineTUpdateAsap = True    

    def rightArrowKeyHandler(self):
        #self.notify.debug('rightArrowKeyHandler')

        curInfo = None
        for vineIndex in xrange(len(self.vines)):
            curInfo = self.vines[vineIndex].getAttachedToonInfo(base.localAvatar.doId)
            if curInfo:
                break
        if not curInfo:
            return
        if vineIndex == len(self.vines) - 1:
            return
        if not self.isInPlayState():
            return

        doJump = True
        if self.ArrowToChangeFacing:
            if not self.lastJumpFacingRight:
                # we were facing left, and pressing right makes us face right
                doJump = False
                self.changeLocalToonFacing(vineIndex, curInfo, True)

        if doJump:
            self.detachLocalToonFromVine(vineIndex, 1)
            normal = curInfo[2]
            self.makeLocalToonJump(vineIndex, curInfo[0], curInfo[1],normal)


    def leftArrowKeyHandler(self):
        #self.notify.debug('leftArrowKeyHandler')
        curInfo = None
        for vineIndex in xrange(len(self.vines)):
            curInfo = self.vines[vineIndex].getAttachedToonInfo(base.localAvatar.doId)
            if curInfo:
                break        
        curInfo = self.vines[vineIndex].getAttachedToonInfo(base.localAvatar.doId)
        if not curInfo:
            return
        if vineIndex == 0:
            return
        # do not left him move once he reaches end vine
        if vineIndex == len(self.vines) - 1:
            return
        if not self.isInPlayState():
            return        

        doJump = True
        if self.ArrowToChangeFacing:
            if self.lastJumpFacingRight:
                # we were facing right, and pressing left makes us face left
                doJump = False
                self.changeLocalToonFacing(vineIndex, curInfo, False)

        if doJump:
            self.detachLocalToonFromVine(vineIndex, 0)
            normal = curInfo[2]
            normal *= -1
            self.makeLocalToonJump(vineIndex, curInfo[0], curInfo[1],normal)

    def b_setNewVine(self, avId, vineIndex, vineT, facingRight):
        self.setNewVine( avId, vineIndex, vineT, facingRight)
        self.d_setNewVine( avId, vineIndex, vineT, facingRight)
        
    def d_setNewVine(self, avId, vineIndex, vineT, facingRight):
        self.notify.debug('setNewVine avId=%d vineIndex=%s' % (avId, vineIndex))
        self.sendUpdate('setNewVine', [avId, vineIndex, vineT, facingRight])
        # in order to give partial scores, we must tell the ai each new vine
        if 0: #vineIndex == VineGameGlobals.NumVines - 1:
            # Now we just tell the AI when we reach the last vine
            self.notify.debug('sending reachedEndVine')
            self.sendUpdate('reachedEndVine', [vineIndex])

    def setNewVine( self, avId, vineIndex, vineT, facingRight):
        """
        toon jumped to a new vine
        """
        # if not avId == self.localAvId:
        # the local player should already be set correctly, but lets
        # play it safe and call this again
        self.updateToonInfo(avId, vineIndex = vineIndex, vineT = vineT,
                            facingRight =facingRight, climbDir = 0, fallingInfo = self.FallingNot)

    def b_setNewVineT(self, avId, vineT, climbDir ):
        self.setNewVineT( avId, vineT, climbDir )
        self.d_setNewVineT( avId, vineT, climbDir)
            
    def d_setNewVineT(self, avId, vineT, climbDir ):
        # we need to stop sending this every frame
        sendIt = False
        curTime = self.getCurrentGameTime()
        if self.sendNewVineTUpdateAsap:
            sendIt = True
        elif (curTime - self.lastNewVineTUpdate) > 0.2:
            sendIt = True

        if sendIt:
            assert self.notify.debugStateCall(self)            
            self.sendUpdate('setNewVineT', [avId, vineT, climbDir] )
            self.sendNewVineTUpdateAsap = False
            self.lastNewVineTUpdate = self.getCurrentGameTime()
            
    def setNewVineT( self, avId,  vineT, climbDir):
        """
        toon climbing up or down his current vine
        """
        self.updateToonInfo(avId, vineT = vineT, climbDir = climbDir)
        
    def b_setJumpingFromVine(self, avId, vineIndex, facingRight, posX, posZ, velX, velZ):
        self.setJumpingFromVine( avId, vineIndex, facingRight, posX, posZ, velX, velZ)
        self.d_setJumpingFromVine( avId, vineIndex, facingRight, posX, posZ, velX, velZ)
        
    def d_setJumpingFromVine(self, avId, vineIndex, facingRight, posX, posZ, velX, velZ):
        self.sendUpdate('setJumpingFromVine', [avId, vineIndex, facingRight, posX, posZ, velX, velZ])

    def setJumpingFromVine(self, avId, vineIndex, facingRight, posX, posZ, velX, velZ):
        # since we're jumping, we should change to -1 for our vine
        self.updateToonInfo(avId, vineIndex = -1, facingRight = facingRight,
                            posX = posX, posZ = posZ, velX = velX, velZ = velZ)

    def b_setFallingFromVine(self, avId, vineIndex, facingRight, posX, posZ, velX, velZ, fallingInfo):
        self.setFallingFromVine( avId, vineIndex, facingRight, posX, posZ, velX, velZ, fallingInfo)
        self.d_setFallingFromVine( avId, vineIndex, facingRight, posX, posZ, velX, velZ, fallingInfo)
        
    def d_setFallingFromVine(self, avId, vineIndex, facingRight, posX, posZ, velX, velZ, fallingInfo):
        self.sendUpdate('setFallingFromVine', [avId, vineIndex, facingRight, posX,
                                               posZ, velX, velZ, fallingInfo])

    def setFallingFromVine(self, avId, vineIndex, facingRight, posX, posZ, velX, velZ, fallingInfo):
        # since we're falling, we should change to -1 for our vine
        self.updateToonInfo(avId, vineIndex = -1, facingRight = facingRight,
                            posX = posX, posZ = posZ, velX = velX, velZ = velZ,
                            fallingInfo = fallingInfo)        

    def b_setFallingFromMidair(self, avId, facingRight, posX, posZ, velX, velZ, fallingInfo):
        self.setFallingFromMidair( avId,  facingRight, posX, posZ, velX, velZ, fallingInfo)
        self.d_setFallingFromMidair( avId, facingRight, posX, posZ, velX, velZ, fallingInfo)
        
    def d_setFallingFromMidair(self, avId, facingRight, posX, posZ, velX, velZ, fallingInfo):
        self.sendUpdate('setFallingFromMidair', [avId, facingRight, posX,
                                               posZ, velX, velZ, fallingInfo])

    def setFallingFromMidair(self, avId, facingRight, posX, posZ, velX, velZ, fallingInfo):
        self.updateToonInfo(avId = avId, facingRight = facingRight,
                            posX = posX, posZ = posZ, velX = velX, velZ = velZ,
                            fallingInfo = fallingInfo)        

    def d_setFallingPos( self, avId, posX, posZ):
        self.sendUpdate('setFallingPos', [avId, posX, posZ])

    def setFallingPos(self, avId, posX, posZ):
        self.updateToonInfo(avId, posX = posX, posZ = posZ)

    def __treasureGrabbed(self, treasureNum):
        """ Handle the local toon grabbing this treasure.
        
        Another toon may actually get the credit, proceed as if we got it
        """
        # make the treasure react
        self.treasures[treasureNum].showGrab()
        # play a sound
        self.grabSound.play()
        # tell the AI we're claiming this treasure
        self.sendUpdate("claimTreasure", [treasureNum])


    def setTreasureGrabbed(self, avId, treasureNum):
        """Update a treaseure being grabbed by a toon."""
        if not self.hasLocalToon: return
        self.notify.debug("treasure %s grabbed by %s" % (treasureNum, avId))

        if avId != self.localAvId:
            # destroy the treasure
            self.treasures[treasureNum].showGrab()

        # update the toon's score
        i = self.avIdList.index(avId)
        self.scores[i] += 1
        self.scorePanels[i].setScore(self.scores[i])

    def setScore(self, avId, score):
        """Update the toon's score."""
        if not self.hasLocalToon: return
        i = self.avIdList.index(avId)
        if hasattr(self,"scorePanels"):
            self.scores[i] += score
            self.scorePanels[i].setScore(score)        

    def timerExpired(self):
        """End the game. Called when the timer expires."""
        self.notify.debug("game timer expired")
        if not VineGameGlobals.EndlessGame:
            # finish the game
            #self.gameFSM.request('waitShowScores')
            if hasattr(self, 'gameFSM'):
                self.gameFSM.request('showScores')       

    def allAtEndVine(self):
        """End the game. Called when everyone is at the end vine."""
        if not self.hasLocalToon: return
        # everyone's at the end vine, move on
        self.notify.debug("all at end vine")
        if not VineGameGlobals.EndlessGame:
            self.gameFSM.request('showScores')   
            #self.gameOver()

    def clearChangeFacingInterval(self):
        """Cleanup the change facing interval."""
        if self.changeFacingInterval:
            self.changeFacingInterval.pause()
            del self.changeFacingInterval
        self.changeFacingInterval = None

    def setupChangeFacingInterval(self, vineIndex, newFacingRight):
        """Start an interval that quickly pans the camera when he changes facing."""
        assert self.notify.debugStateCall(self)
        self.clearChangeFacingInterval()
        self.changeFacingInterval = Sequence()
        if not ((vineIndex == 0) or (vineIndex == VineGameGlobals.NumVines - 1)):
            destPos = self.getFocusCameraPos(vineIndex, newFacingRight)
            self.changeFacingInterval.append(LerpPosInterval(base.camera,
                                                         0.5,
                                                         destPos))
            self.changeFacingInterval.append(Func(self.clearChangeFacingInterval))
        self.changeFacingInterval.start()

    def clearAttachingToVineCamIval(self):
        """Cleanup the attaching to vine camera interval."""
        if self.attachingToVineCamIval:
            self.attachingToVineCamIval.pause()
            del self.attachingToVineCamIval
        self.attachingToVineCamIval = None
        
    def setupAttachingToVineCamIval(self, vineIndex, facingRight):
        """Start an interval that quickly pans the camera to the focus vine position."""
        assert self.notify.debugStateCall(self)
        self.clearAttachingToVineCamIval()
        self.attachingToVineCamIval = Sequence()
        destPos = self.getFocusCameraPos(vineIndex, facingRight)
        self.attachingToVineCamIval.append(LerpPosInterval(base.camera,
                                                          0.5,
                                                          destPos))
        self.attachingToVineCamIval.append(Func(self.clearAttachingToVineCamIval))
        self.attachingToVineCamIval.start()

    def createRadar(self):
        """Show an overview of the game at the bottom of the screen.
        
        Loosely based on loadClarabelle() in CatalogScreen.py
        """
        # It gets its own camera
        self.cCamera = render.attachNewNode('cCamera')
        self.cCamNode = Camera('cCam')
        self.cCamNode.setCameraMask(VineGameGlobals.RadarCameraBitmask)
        self.cLens = PerspectiveLens()
        #self.cLens.setFov(40,2.5)
        xFov = 40
        yFov = 2.5
        self.cLens.setFov(xFov,yFov)
        self.cLens.setNear(0.1)
        self.cLens.setFar(1300.0)
        self.cCamNode.setLens(self.cLens)
        self.cCamNode.setScene(render)
        self.cCam = self.cCamera.attachNewNode(self.cCamNode)
        #self.cCam.setPos(285, -800, 16.3)
        self.cCam.setPos(300, -850, 16.3)

        #self.cDr = base.win.makeDisplayRegion(0, 1, 0, 0.0625)
        endY = yFov / xFov
        #self.cDr = base.win.makeDisplayRegion(0, 1, 0, 0.125)
        self.endZRadar = 0.09375
        self.cDr = base.win.makeDisplayRegion(0, 1, 0, self.endZRadar)
        self.cDr.setSort(1)
            
        self.cDr.setClearDepthActive(1)
        self.cDr.setClearColorActive(1)
        self.cDr.setClearColor(Vec4(0.85, 0.95, 0.95, 1))
        self.cDr.setCamera(self.cCam)

        self.radarSeparator = DirectFrame (
                             relief = None,
                             image = DGG.getDefaultDialogGeom(),
                             #image_color = ToontownGlobals.GlobalDialogColor,
                             image_color = (0.2, 0.0, 0.8, 1),
                             image_scale = (2.65, 1.0, 0.01),
                             pos = (0, 0, -0.8125),
                             )

        # we need to do this since the default camera mask has changed
        self.oldBaseCameraMask = base.camNode.getCameraMask()
        base.camNode.setCameraMask(BitMask32.bit(0))

    def destroyRadar(self):
        """Cleanup the radar."""
        base.win.removeDisplayRegion(self.cDr)
        self.cCamera.removeNode()
        del self.cCamera
        del self.cCamNode
        del self.cLens
        del self.cCam
        del self.cDr
        self.radarSeparator.destroy()
        del self.radarSeparator

        base.camNode.setCameraMask(self.oldBaseCameraMask)

    def updateRadar(self):
        """Update the toon head icons in the radar."""
        for avId in self.headFrames:
            av = base.cr.doId2do.get(avId)
            headFrameShown = False
            if av:
                avPos = av.getPos(render)
                newPoint = self.mapRadarToAspect2d(render, avPos)
                if newPoint:
                    headFrameShown = True
                    self.headFrames[avId].setPos(newPoint[0], newPoint[1], newPoint[2])
            if headFrameShown:
                self.headFrames[avId].show()
            else:
                self.headFrames[avId].hide()
                
        pass
        
    def mapRadarToAspect2d(self, node, point):
        """Maps the indicated 3-d point (a Point3), which is relative to
        the indicated NodePath, to the corresponding point in the aspect2d
        scene graph.  Returns the corresponding Point3 in aspect2d.
        Returns None if the point is not onscreen. Then do some rescaling to
        place it at the bottom of the screen."""
    
        # Convert the point to the 3-d space of the camera
        if point[0] > 26:
            pass
            #import pdb; pdb.set_trace()
        p3 = self.cCam.getRelativePoint(node, point)

        # Convert it through the lens to render2d coordinates
        p2 = Point2()
        if not self.cLens.project(p3, p2):
            return None
    
        r2d = Point3(p2[0], 0, p2[1])
        
        # And then convert it to aspect2d coordinates
        a2d = aspect2d.getRelativePoint(render2d, r2d)

        zAspect2DRadar = self.endZRadar * 2.0 - 1
        #print zAspect2DRadar
        oldZ = a2d.getZ()
        #newZ = zAspect2DRadar + ( (1-oldZ)/2.0 * (zAspect2DRadar+1))
        newZ = (oldZ + 1) / 2.0 * (zAspect2DRadar + 1)
        newZ -= 1
        a2d.setZ(newZ)
        #print oldZ
        return a2d

    def localToonHitSpider(self, colEntry):
        """Handle local toon hitting the spider in midair or on the vine."""
        self.notify.debug('toonHitSpider')
        if self.toonInfo[self.localAvId][0] == -1:
            # we hit a spider while we were jumping
            fallingInfo = self.toonInfo[self.localAvId][8]
            if not (fallingInfo == self.FallingBat or fallingInfo == self.FallingSpider):
                self.spiderHitSound.play()
                self.makeLocalToonFallFromMidair(self.FallingSpider)            
        else:
            # we hit a spider while we were holding on to a vine
            self.spiderHitSound.play()
            self.makeLocalToonFallFromVine(self.FallingSpider)


    def localToonHitBat(self, colEntry):
        """Handle local toon hitting the bat in midair or on the vine."""
        self.notify.debug('toonHitBat')
        if self.toonInfo[self.localAvId][0] == VineGameGlobals.NumVines - 1:
            # bat doesn't affect us if we are on the last vine
            return
        if self.toonInfo[self.localAvId][0] == -1:
            # we hit a bat while we were jumping
            self.batHitMidairSound.play()
            fallingInfo = self.toonInfo[self.localAvId][8]
            if not (fallingInfo == self.FallingBat or fallingInfo == self.FallingSpider):
                self.makeLocalToonFallFromMidair(self.FallingBat)
        else:
            # we hit a spider while we were holding on to a vine
            self.batHitVineSound.play()
            self.makeLocalToonFallFromVine(self.FallingBat)


    def toonHitSomething(self, colEntry):
        """Handle local toon hitting something with his body collissions."""
        # respond to spider or bat hits only when we're in the playing state
        if not self.isInPlayState():
            return
        
        # assert self.notify.debugStateCall(self)
        intoName = colEntry.getIntoNodePath().getName()
        if 'spider' in intoName:
            self.localToonHitSpider(colEntry)
        elif 'bat' in intoName:
            self.localToonHitBat(colEntry)

    def setVineSections(self, vineSections):
        """Set vineSections as dictated by the AI."""
        self.vineSections = vineSections
        # self.vineSections = [9,9,9,9] # test specific parameters
        # self.vineSections = [0,0,0,0] # test really easy        
        # self.vineSections = [3,2,1,0] # test easy
        # self.vineSections = [7,6,5,4] # test hard
        # self.vineSections = [8,7,6,5] # test hardest

    def setupVineCourse(self):
        """Create the actual swing vines from self.vineSections."""
        vineIndex = 0
        for section in self.vineSections:
            for vineInfo in VineGameGlobals.CourseSections[section]:
                length, baseAngle, vinePeriod, spiderPeriod = vineInfo
                posX = vineIndex * VineGameGlobals.VineXIncrement
                newVine = SwingVine.SwingVine( vineIndex, posX, 0,
                                               VineGameGlobals.VineHeight,
                                               length = length,
                                               baseAngle = baseAngle,
                                               period = vinePeriod,
                                               spiderPeriod = spiderPeriod
                                               )
                self.vines.append(newVine)
                vineIndex += 1
        
    def loadBats(self):
        """Create the bats, but not the bat intervals."""
        self.bats = []
        szId = self.getSafezoneId()
        self.batInfo = VineGameGlobals.BatInfo[szId]
        batIndex = 0
        for batTuple in self.batInfo:
            newBat = VineBat.VineBat(batIndex,self.batInfo[batIndex][0] )
            # position him at the right side of the course
            xPos = VineGameGlobals.VineXIncrement * VineGameGlobals.NumVines + 100
            newBat.setX(xPos)
            self.bats.append(newBat)
            batIndex += 1

    def createBatIvals(self):
        """Create all the bat intervals."""
        self.batIvals = []
        for batIndex in xrange(len(self.bats)):
            newBatIval = self.createBatIval(batIndex)
            self.batIvals.append(newBatIval)

    def startBatIvals(self):
        """Start all the bat intervals."""
        for batIval in self.batIvals:
            batIval.start()

    def destroyBatIvals(self):
        """Destroy can clean up the bat intervals."""
        for batIval in self.batIvals:
            batIval.finish()
        self.batIvals = []

    def createBatIval(self, batIndex):
        """Create and return the bat interval for the whole game."""
        timeToTraverseField = self.batInfo[batIndex][0]
        initialDelay = self.batInfo[batIndex][1]
        startMultiplier = 1
        if len(self.batInfo[batIndex]) >= 3:
            startMultiplier = 0.25
        batIval = Sequence()
        batIval.append(Wait(initialDelay))
        batIval.append(Func(self.bats[batIndex].startFlying))
        startX = VineGameGlobals.VineXIncrement * VineGameGlobals.NumVines
        endX = -VineGameGlobals.VineXIncrement
        firstInterval = True
        while batIval.getDuration() < VineGameGlobals.GameDuration:
            batHeight = self.randomNumGen.randrange(VineGameGlobals.BatMinHeight,
                                                    VineGameGlobals.BatMaxHeight)
            batIval.append(Func(self.bats[batIndex].startLap))
            if firstInterval:
                newIval = LerpPosInterval( self.bats[batIndex],
                                           duration = timeToTraverseField * startMultiplier,
                                           pos = Point3(endX, 0, batHeight),
                                           startPos = Point3(startX * startMultiplier, 0, batHeight)
                                           )
            else:
                newIval = LerpPosInterval( self.bats[batIndex],
                                           duration = timeToTraverseField,
                                           pos = Point3(endX, 0, batHeight),
                                           startPos = Point3(startX, 0, batHeight)
                                           )
            batIval.append(newIval)
            firstInterval = False
        batIval.append(Func(self.bats[batIndex].stopFlying))            
        return batIval
            
    def isInPlayState(self):
        """Return true if we are in the play state."""
        if not self.gameFSM.getCurrentState():
            return False
        if not self.gameFSM.getCurrentState().getName() == 'play':
            return False
        return True

    def getIntroTrack(self):
        """Create an intro track of the toons running and jumping to the first vine."""
        retval = Sequence()
        toonTakeoffs = Parallel()
        didCameraMove = False
        for index in xrange(len( self.avIdList)):
            avId = self.avIdList[index]
            # we are not guaranteed that the other toons are generated at this point
            # thinking if we should do it only on the local toon or on all
            # the toons we have available
            if avId != self.localAvId:
                # for now do it only on the local toon
                continue
            oneSeq = Sequence()
            oneSeqAndHowl = Parallel()
            av = base.cr.doId2do.get(avId)
            if av:
                toonOffset = self.calcToonOffset(av)
                platformPos = self.startPlatform.getPos()
                endPos = self.vines[0].getPos()
                endPos.setZ(endPos.getZ() - toonOffset.getZ() -
                            (VineGameGlobals.VineStartingT * self.vines[0].cableLength))
                xPos = platformPos[0] - 0.5 # - (index * 2) # uncomment if we are showing multiple toons
                takeOffPos = Point3(xPos, platformPos[1], platformPos[2])
                leftPos = Point3(xPos - 27, platformPos[1], platformPos[2])
                self.notify.debug('leftPos = %s platformPos=%s' % (leftPos,platformPos))
                startRunningPos = Point3(takeOffPos)
                startRunningPos.setX( startRunningPos.getX() -7)

                # show him looking at the vines confused
                oneSeq.append(Func(av.dropShadow.show))
                oneSeq.append(Func(av.setH, -90))                
                oneSeq.append(Func(av.setPos, takeOffPos[0], takeOffPos[1], takeOffPos[2]))
                exclamationSfx = av.getDialogueSfx('exclamation',0)
                oneSeq.append(Parallel(
                    ActorInterval(av, 'confused', duration = 3),
                    #keeps getting chopped off, don't use for now
                    #SoundInterval(exclamationSfx, duration = 3), # exclaim sound
                    ))
                
                # he thinks and gets an idea
                questionSfx = av.getDialogueSfx('question',0)
                oneSeq.append(Parallel(
                    ActorInterval(av, 'think', duration = 3.0),
                    SoundInterval(questionSfx, duration = 3), # question sound
                    ))

                # he walks to the left
                oneSeq.append(Func(av.setH, 90))
                oneSeq.append(Func(av.setPlayRate, 1, 'walk'))
                oneSeq.append(Func(av.loop, 'walk'))
                oneSeq.append(Parallel(
                    LerpPosInterval(av, pos = leftPos, duration =5.25,),
                    SoundInterval(av.soundWalk, loop=1, duration = 5.25)                    
                    ))

                # he runs to the right
                oneSeq.append(Func(av.setH, -90))                                
                oneSeq.append(Func(av.loop, 'run'))
                oneSeq.append(Parallel(
                    LerpPosInterval(av, pos = takeOffPos, duration =2.5,),
                    SoundInterval(av.soundRun, loop =1, duration =2.5)
                    ))

                # he takes off for the vine
                oneSeq.append(Func(av.dropShadow.hide))
                howlTime = oneSeq.getDuration()
                oneSeq.append(Parallel(
                    LerpPosInterval(av, pos = endPos, duration =0.5,),
                    Func(av.pose, 'swing', self.JumpingFrame),
                    ))

                # he swings from the vine
                attachingToVineSeq = Sequence(
                    ActorInterval(av, 'swing', startFrame= self.JumpingFrame,
                                  endFrame =143, playRate = 2.0),
                    ActorInterval(av, 'swing', startFrame=0,
                                  endFrame = 86, playRate = 2.0)
                    )
                attachingToVine = Parallel(
                    attachingToVineSeq,
                    SoundInterval(self.catchSound)
                    )
                if didCameraMove:
                    oneSeq.append(attachingToVine)
                else:
                    attachAndMoveCam = Parallel(
                        attachingToVine,
                        LerpPosInterval(base.camera, pos =self.getFocusCameraPos(0,True),
                                      duration=2))
                    oneSeq.append(attachAndMoveCam)
                oneSeq.append(Func(av.setPos, 0, 0, 0))
                oneSeq.append(Func(av.setH, 0))
                
                #oneSeq.append(Func(av.pose, 'swing', 86))                
                if 0: #avId == self.localAvId:
                   oneSeq.append(Func(self.attachLocalToonToVine, 0,
                                      VineGameGlobals.VineStartingT))
                else:
                    oneSeq.append(Func(self.vines[0].attachToon, avId,
                                       VineGameGlobals.VineStartingT, self.lastJumpFacingRight,
                                       setupAnim=False))
                oneSeq.append(Func(self.vines[0].updateAttachedToons))
                # since howl spans multiple intervals, do it here
                howlSfx = av.getDialogueSfx('special',0)
                howlSeq = Sequence(
                    Wait(howlTime),
                    SoundInterval(howlSfx))
                #we need to delay the exlamation sfx
                exclamationSeq = Sequence(
                    Wait(0.5),
                    SoundInterval(exclamationSfx))                
                oneSeqAndHowl = Parallel( oneSeq, howlSeq, exclamationSeq)

            toonTakeoffs.append(oneSeqAndHowl)
        retval.append(toonTakeoffs)

        return retval
                
        
    def doEndingTrackTask(self, avId):
        """Call setupEndingTrack after a certain amount of time."""
        taskName = 'VineGameEnding-%s' % avId
        if not self.endingTracks.has_key(avId):
            taskMgr.doMethodLater( 0.5, self.setupEndingTrack, taskName, extraArgs = (avId,) )
            self.endingTrackTaskNames.append(taskName)

    def debugCameraPos(self):
        """Print out the camera position."""
        self.notify.debug('cameraPos = %s' % base.camera.getPos())

    def setupEndingTrack(self,  avId):
        """Create and play the ending sequence where he jumps to the end platform."""
        if self.endingTracks.has_key(avId):
            self.notify.warning('setupEndingTrack duplicate call avId=%d' % avId)
            return
        # make sure we still have vines
        if len(self.vines) == 0:
            return
        endVine = VineGameGlobals.NumVines - 1
        platformPos = self.endPlatform.getPos()
        avIndex = self.avIdList.index(avId)
        landingPos = Point3(platformPos)
        landingPos.setX( landingPos.getX() + avIndex * 2)
        endingTrack = Sequence()
        av = base.cr.doId2do.get(avId)
        avPos = av.getPos(render)
        cameraPos = base.camera.getPos()
        self.notify.debug('avPos=%s cameraPos=%s' % (avPos, base.camera.getPos()))
        if av:
            midX = landingPos[0] # (landingPos[0] + avPos[0]) / 2.0
            midZ = platformPos[2] + 6
            jumpingTransition = self.createJumpingTransitionIval(endVine)
            endingTrack.append(Func(self.vines[endVine].detachToon, avId))
            endingTrack.append(Func(av.wrtReparentTo, render))
            endingTrack.append(Func(self.debugCameraPos))
            endingTrack.append(Func(av.loop, 'jump-idle'))
            landingIval = Parallel(
                ProjectileInterval( av, startPos = av.getPos(render), endZ = landingPos[2], 
                                    wayPoint = Point3(midX, 0, midZ), timeToWayPoint = 1)
                )
            endingTrack.append(landingIval)
            endingTrack.append(Func(av.dropShadow.show))
            endingTrack.append(Func(av.play, 'jump-land'))
            endingTrack.append(Func(self.winSound.play))
            endingTrack.append(Func(av.loop, 'victory'))
            
        self.endingTracks[avId] = endingTrack
        endingTrack.start()
        return Task.done

    def cleanupEndingTracks(self):
        """Cleanup ending tracks and related tasks."""
        for taskName in self.endingTrackTaskNames:
            taskMgr.remove(taskName)
        for endingTrack in self.endingTracks.values():
            endingTrack.finish
            del endingTrack
        self.endingTracks = {}
