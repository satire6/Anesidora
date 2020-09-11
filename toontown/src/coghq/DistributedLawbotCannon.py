from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.task.Task import Task
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import CollisionSphere, CollisionNode
from toontown.toonbase import ToontownGlobals
from toontown.estate import DistributedCannon
from toontown.estate import CannonGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toon import NPCToons
from toontown.toon import ToonHead
from toontown.toonbase import TTLocalizer
from toontown.minigame import Trajectory
from toontown.effects import DustCloud

#some constants

# lowest point we should allow the toon to fall
# (just in case he doesn't hit the terrain)
GROUND_PLANE_MIN = -15

CANNON_ROTATION_MIN = -55
CANNON_ROTATION_MAX = 50
CANNON_ROTATION_VEL = 15.0 # move 15 units every second

CANNON_ANGLE_MIN = 10
CANNON_ANGLE_MAX = 85
CANNON_ANGLE_VEL = 15.0

INITIAL_VELOCITY = 80

# send cannon movement messages for the local cannon at this frequency
CANNON_MOVE_UPDATE_FREQ = 0.5

# these determine the range of distances the camera will
# pull back, away from the toon, in-flight
CAMERA_PULLBACK_MIN = 20
CAMERA_PULLBACK_MAX = 40


#based on /src/estate/DistributedCannon.py

#class DistributedLawbotCannon (DistributedCannon.DistributedCannon):
class DistributedLawbotCannon (DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLawbotCannon")

    LOCAL_CANNON_MOVE_TASK = "localCannonMoveTask"
    
    # keyboard controls
    FIRE_KEY  = "control"
    UP_KEY    = "arrow_up"
    DOWN_KEY  = "arrow_down"
    LEFT_KEY  = "arrow_left"
    RIGHT_KEY = "arrow_right"

    # flags for objects that the toons can hit
    HIT_GROUND = 0
    
    def __init__(self, cr):
        assert  self.notify.debug("__init__")         
        #DistributedCannon.DistributedCannon.__init__(self, cr)
        DistributedObject.DistributedObject.__init__(self, cr)

        self.index = None #nth cannon out of several
        self.avId = 0 #what is the if of the avatar using this cannon
        self.av = None   #who is the avatar using this cannon
        self.localToonShooting = 0 #is the toon using this cannon currently shooting
        self.cannonsActive = 0
        
        self.cannonLocation = None #where is the cannon in the world
        self.cannonPostion = None #how is the cannon oriented
        self.cannon = None #our cannon model

        self.madeGui = 0 #have we ever made our gui before?

        self.jurorToon = None #juror toon
        self.toonModel = None # juror full body model
        self.toonHead = None #juror just the head model
        self.toonScale = None #original toon scale, candidate for nuking
        self.dustCloud = None #dustCloud effect

        # reset fly/collision info
        self.hitBumper = 0
        self.hitTarget = 0
        self.lastPos = Vec3(0,0,0)
        self.lastVel = Vec3(0,0,0)
        self.vel = Vec3(0,0,0)
        self.landingPos = Vec3(0,0,0)
        self.t = 0
        self.lastT = 0
        self.deltaT = 0
        self.hitTrack = None

        # for collisions
        self.flyColNode = None
        self.flyColNodePath = None
        

        self.localAvId = base.localAvatar.doId        

        self.model_Created = 0
        
    def disable(self):
        assert  self.notify.debug("disable")
        taskMgr.remove(self.uniqueName("fireCannon"))
        taskMgr.remove(self.uniqueName("shootTask"))
        self.__stopFlyTask(self.avId)
        taskMgr.remove(self.uniqueName("flyTask"))        
        self.ignoreAll()
        self.setMovie(CannonGlobals.CANNON_MOVIE_CLEAR, 0, 0)
        self.nodePath.detachNode()
        self.__unmakeGui()
        if self.hitTrack:
            self.hitTrack.finish()
            del self.hitTrack
            self.hitTrack = None        
        DistributedObject.DistributedObject.disable(self)
        
    def delete(self):
        assert  self.notify.debug("disable")
        self.offstage()
        self.unload()
        DistributedObject.DistributedObject.delete(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        assert(not self.boss.cannons.has_key(self.index))
        self.boss.cannons[self.index] = self
        

    def generateInit(self):
        assert  self.notify.debug("generateInit")
        DistributedObject.DistributedObject.generateInit(self)
        self.nodePath = NodePath(self.uniqueName('Cannon'))
        self.load()
        self.activateCannons()


    # The handler that catches the initial position and orientation
    # established on the AI
    def setPosHpr(self, x, y, z, h, p, r):
        assert self.notify.debug('setPosHpr x=%f y=%f z=%f h=%f' % (x,y,z,h))
        self.nodePath.setPosHpr(x, y, z, h, p, r)


    def setBossCogId(self, bossCogId):
        self.bossCogId = bossCogId

        # This would be risky if we had toons entering the zone during
        # a battle--but since all the toons are always there from the
        # beginning, we can be confident that the BossCog has already
        # been generated by the time we receive the generate for its
        # associated battles.
        self.boss = base.cr.doId2do[bossCogId]
        
    def getSphereRadius(self):
        """getSphereRadius(self)
        This method can be overwritten by an inheritor.
        """
        return 1.5

    def getParentNodePath(self):
        return render

    def setIndex(self, index):
        self.index = index
    

    def load(self):
        assert self.notify.debug("load")

        self.cannon = loader.loadModel(
            "phase_4/models/minigames/toon_cannon")        

        # Make a collision sphere to detect when an avatar enters the
        # cannon.
        self.collSphere = CollisionSphere(0, 0, 0, self.getSphereRadius())

        # Dust cloud object for when toon hits ground
        self.dustCloud = DustCloud.DustCloud(render)
        self.dustCloud.setBillboardPointEye()
        
        # Make the sphere intangible, initially.
        self.collSphere.setTangible(1)
        self.collNode = CollisionNode(self.uniqueName('CannonSphere'))
        self.collNode.setCollideMask(ToontownGlobals.WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.nodePath.attachNewNode(self.collNode)

        self.cannon.reparentTo(self.nodePath)

        self.kartColNode = CollisionNode(self.uniqueName('KartColNode'))
        self.kartNode = self.nodePath.attachNewNode(self.kartColNode)
        

        # Sound effects
        self.sndCannonMove = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_adjust.mp3")
        self.sndCannonFire = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_fire_alt.mp3")
        self.sndHitGround  = base.loadSfx(\
                                 "phase_4/audio/sfx/MG_cannon_hit_dirt.mp3")
        self.sndHitChair  = base.loadSfx(\
                                 "phase_11/audio/sfx/LB_toon_jury.mp3")

        self.cannon.hide()

        self.flashingLabel = None

    def unload(self):
        assert(self.notify.debug("unload"))

        # get rid of original cannon model
        if self.cannon:
            self.cannon.removeNode()
            del self.cannon

        # get rid of the dust cloud
        if self.dustCloud != None:
            self.dustCloud.destroy()
            del self.dustCloud

        # Get rid of audio
        del self.sndCannonMove
        del self.sndCannonFire
        del self.sndHitGround
        del self.sndHitChair

        if self.av:
            self.__resetToon(self.av)
            # Reset anim an run play rate
            self.av.loop('neutral')
            self.av.setPlayRate(1.0, 'run')
        

        # make sure the blink and lookaround tasks are cleaned up
        if (self.toonHead != None):
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead.delete()
            del self.toonHead
        if (self.toonModel != None):
            self.toonModel.removeNode()
            del self.toonModel
        if (self.jurorToon != None):
            self.jurorToon.delete()
            del self.jurorToon
        del self.toonScale


    def activateCannons(self):
        assert  self.notify.debug("activateCannons") 
        if not self.cannonsActive:
            self.cannonsActive = 1
            
            self.onstage()

            # Put the cannon in the world
            self.nodePath.reparentTo(self.getParentNodePath())
            
            # When the localToon steps up to the cannon, we call requestEnter
            self.accept(self.uniqueName('enterCannonSphere'),
                        self.__handleEnterSphere)

    def onstage(self):
        assert(self.notify.debug("onstage"))

        # show everything
        self.__createCannon()
        self.cannon.reparentTo(self.nodePath)
        self.dustCloud.reparentTo(render)        

    def offstage(self):
        assert(self.notify.debug("offstage"))
        if self.cannon:
            self.cannon.reparentTo(hidden)
        if self.dustCloud:
            self.dustCloud.reparentTo(hidden)
            self.dustCloud.stop()           

            
    def __createCannon(self):
        self.barrel = self.cannon.find("**/cannon")
        self.cannonLocation = Point3(0, 0, 0.025)
        self.cannonPosition = [0,CANNON_ANGLE_MIN]
        self.cannon.setPos(self.cannonLocation)
        self.__updateCannonPosition(self.avId)

    def updateCannonPosition(self, avId, zRot, angle):
        # the server is telling us that a cannon has moved (rotated)
        #self.notify.debug("updateCannonPosition: " + str(avId) + \
        #                  ": zRot=" + str(zRot) + ", angle=" + str(angle))
        if avId != self.localAvId:
            self.cannonPosition = [zRot, angle]
            self.__updateCannonPosition(avId)


    def __updateCannonPosition(self, avId):
        self.cannon.setHpr(self.cannonPosition[0], 0., 0.)
        self.barrel.setHpr(0., self.cannonPosition[1], 0.)
        # squish the shadow to match the barrel pos
        maxP = 90
        newP = self.barrel.getP()
        yScale = 1-.5*float(newP)/maxP
        shadow = self.cannon.find("**/square_drop_shadow")
        shadow.setScale(1,yScale,1)


    def __handleEnterSphere(self, collEntry):
        assert  self.notify.debug("__handleEnterSphere")         
        self.d_requestEnter()

    def d_requestEnter(self):
        self.sendUpdate('requestEnter', [])

    def setMovie(self, mode, avId, extraInfo):
        assert(self.notify.debug("%s setMovie(%s, %s)" % (self.doId, mode, avId)))

        wasLocalToon = self.localToonShooting
        
        self.avId = avId

        if (mode == CannonGlobals.CANNON_MOVIE_CLEAR):
            # No one is in the cannon; it's available.            
            self.setLanded()
        elif (mode == CannonGlobals.CANNON_MOVIE_LANDED):
            # Make sure toonHead is hidden.  If someone walks into
            # the zone after we have fired, they will see a setOccupied(avId)
            # message even after the av has left the cannon.
            self.setLanded()        
        elif (mode ==  CannonGlobals.CANNON_MOVIE_FORCE_EXIT):
            self.exitCannon(self.avId)
            self.setLanded()
        elif (mode == CannonGlobals.CANNON_MOVIE_LOAD):
            # The cannon is occupied; no one else may be here.            
            if (self.avId == base.localAvatar.doId):

                #TODO maybe reuse the lever/crane animations? or create new ones?
                #cache the animations we'll use

                self.cannonBallsLeft = extraInfo

                # put toon in cannon
                base.cr.playGame.getPlace().setState('crane')
                base.localAvatar.setTeleportAvailable(0)
                #base.localAvatar.collisionsOff()
                
                self.localToonShooting = 1
                self.__makeGui()
                camera.reparentTo(self.barrel)
                camera.setPos(.5,-2,2.5)
                camera.setHpr(0,0,0)

                self.boss.toonEnteredCannon(self.avId, self.index)



            if (self.cr.doId2do.has_key(self.avId)):
                # If the toon exists, look it up
                self.av = self.cr.doId2do[self.avId]
                self.acceptOnce(self.av.uniqueName('disable'), 
                                        self.__avatarGone)

                #he was probably running to the cannon, put him in neutral
                self.av.loop('neutral') 

                # Parent it to the cannon
                self.av.stopSmooth()

                self.__destroyToonModels() #this is such a hack, TODO fix this later
                self.__createToonModels()

                #make the toon stand beside cannon and rotate with it
                self.av.setPosHpr(3,0,0,90,0,0)                
                self.av.reparentTo(self.cannon)
            else:
                self.notify.warning("Unknown avatar %d in cannon %d" % (self.avId, self.doId))
        else:
            self.notify.warning('unhandled case, mode = %d' % mode)
            

            
    def __avatarGone(self):
        # Called when the avatar in the cannin vanishes.

        # The AI will call setMovie(CANNON_MOVIE_CLEAR), too, but we call it first
        # just to be on the safe side, so we don't try to access a
        # non-existent avatar.
        self.setMovie(CannonGlobals.CANNON_MOVIE_CLEAR, 0,0)

        
    def __makeGui(self):
        if self.madeGui:
            return

        NametagGlobals.setMasterArrowsOn(0)        

        # set up the cannon aiming/firing gui
        guiModel = "phase_4/models/gui/cannon_game_gui"
        cannonGui = loader.loadModel(guiModel)
        self.aimPad = DirectFrame(image = cannonGui.find("**/CannonFire_PAD"),
                                  relief = None,
                                  pos = (0.7, 0, -0.553333),
                                  scale = 0.8,
                                  )
        cannonGui.removeNode()

        # add the fire and arrow buttons
        self.fireButton = DirectButton(parent = self.aimPad,
                                       image = ((guiModel, "**/Fire_Btn_UP"),
                                                (guiModel, "**/Fire_Btn_DN"),
                                                (guiModel, "**/Fire_Btn_RLVR"),
                                                ),
                                       relief = None,
                                       pos = (0.0115741,0,0.00505051),
                                       scale = 1.,
                                       command = self.__firePressed,
                                       )
        self.upButton = DirectButton(parent = self.aimPad,
                                     image = ((guiModel, "**/Cannon_Arrow_UP"),
                                              (guiModel, "**/Cannon_Arrow_DN"),
                                              (guiModel, "**/Cannon_Arrow_RLVR"),
                                              ),
                                     relief = None,
                                     pos = (0.0115741,0,0.221717),
                                     )
        self.downButton = DirectButton(parent = self.aimPad,
                                       image = ((guiModel, "**/Cannon_Arrow_UP"),
                                                (guiModel, "**/Cannon_Arrow_DN"),
                                                (guiModel, "**/Cannon_Arrow_RLVR"),
                                                ),
                                       relief = None,
                                       pos = (0.0136112,0,-0.210101),
                                       image_hpr = (0,0,180),
                                       )
        self.leftButton = DirectButton(parent = self.aimPad,
                                       image = ((guiModel, "**/Cannon_Arrow_UP"),
                                                (guiModel, "**/Cannon_Arrow_DN"),
                                                (guiModel, "**/Cannon_Arrow_RLVR"),
                                                ),
                                       relief = None,
                                       pos = (-0.199352,0,-0.000505269),
                                       image_hpr = (0,0,-90),
                                       )
        self.rightButton = DirectButton(parent = self.aimPad,
                                        image = ((guiModel, "**/Cannon_Arrow_UP"),
                                                 (guiModel, "**/Cannon_Arrow_DN"),
                                                 (guiModel, "**/Cannon_Arrow_RLVR"),
                                                 ),
                                        relief = None,
                                        pos = (0.219167,0,-0.00101024),
                                        image_hpr = (0,0,90),
                                        )

        guiClose = loader.loadModel("phase_3.5/models/gui/avatar_panel_gui")

        if 0:
            self.closeButton = DirectButton(
                parent = self.aimPad,
                image = (guiClose.find("**/CloseBtn_UP"),
                         guiClose.find("**/CloseBtn_DN"),
                         guiClose.find("**/CloseBtn_Rllvr"),
                         guiClose.find("**/CloseBtn_UP"),
                         ),
                relief = None,
                scale = 2,
                text = TTLocalizer.LawbotBossLeaveCannon,
                text_scale = 0.04,
                text_pos = (0, -0.07),
                text_fg = VBase4(1, 1, 1, 1),
                pos = (0.5,0,-0.3),
                command = self.__leaveCannon,
                )

        cannonBallText = '%d/%d' % (self.cannonBallsLeft, \
                                    ToontownGlobals.LawbotBossCannonBallMax)
        self.cannonBallLabel = DirectLabel (
            parent = self.aimPad,
            text = cannonBallText,
            text_fg = VBase4(1,1,1,1),
            text_align = TextNode.ACenter,
            relief = None,
            #pos = (0, 0, 0.35),
            pos = (0.475, 0.0, -0.35),
            scale = 0.25)

        if (self.cannonBallsLeft < 5):
            if self.flashingLabel:
                self.flashingLabel.stop()
            flashingTrack = Sequence()
            for i in range(10):
                flashingTrack.append(LerpColorScaleInterval(self.cannonBallLabel, 0.5, VBase4(1,0,0,1)))
                flashingTrack.append(LerpColorScaleInterval(self.cannonBallLabel, 0.5, VBase4(1,1,1,1)))
                
            self.flashingLabel = flashingTrack
            self.flashingLabel.start()
        
        # set alpha on aim interface
        self.aimPad.setColor(1,1,1,0.9)

        # set up the button press/release handlers
        def bindButton(button, upHandler, downHandler):
            button.bind(DGG.B1PRESS, lambda x, handler=upHandler : handler())
            button.bind(DGG.B1RELEASE, lambda x, handler=downHandler : handler())
        bindButton(self.upButton, self.__upPressed, self.__upReleased)
        bindButton(self.downButton, self.__downPressed, self.__downReleased)
        bindButton(self.leftButton, self.__leftPressed, self.__leftReleased)
        bindButton(self.rightButton, self.__rightPressed, self.__rightReleased)

        self.__enableAimInterface()

        self.madeGui = 1

    def __unmakeGui(self):
        self.notify.debug("__unmakeGui")
        if not self.madeGui:
            return

        if self.flashingLabel:
            self.flashingLabel.finish()
            self.flashingLabel = None
        

        NametagGlobals.setMasterArrowsOn(1)

        self.__disableAimInterface()

        # Do we need to unbind?
        self.upButton.unbind(DGG.B1PRESS)
        self.upButton.unbind(DGG.B1RELEASE)
        self.downButton.unbind(DGG.B1PRESS)
        self.downButton.unbind(DGG.B1RELEASE)
        self.leftButton.unbind(DGG.B1PRESS)
        self.leftButton.unbind(DGG.B1RELEASE)
        self.rightButton.unbind(DGG.B1PRESS)
        self.rightButton.unbind(DGG.B1RELEASE)

        self.aimPad.destroy()
        del self.aimPad
        del self.fireButton
        del self.upButton
        del self.downButton
        del self.leftButton
        del self.rightButton
        self.madeGui = 0

    # UI crep
    def __enableAimInterface(self):
        self.aimPad.show()

        # listen for key presses
        self.accept(self.FIRE_KEY, self.__fireKeyPressed)
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)

        # start the local cannon move task
        self.__spawnLocalCannonMoveTask()

    def __disableAimInterface(self):
        self.aimPad.hide()

        self.ignore(self.FIRE_KEY)
        self.ignore(self.UP_KEY)
        self.ignore(self.DOWN_KEY)
        self.ignore(self.LEFT_KEY)
        self.ignore(self.RIGHT_KEY)
        self.ignore(self.FIRE_KEY + "-up")
        self.ignore(self.UP_KEY + "-up")
        self.ignore(self.DOWN_KEY + "-up")
        self.ignore(self.LEFT_KEY + "-up")
        self.ignore(self.RIGHT_KEY + "-up")

        # kill the local cannon move task
        self.__killLocalCannonMoveTask()


    # keypress handlers
    def __fireKeyPressed(self):
        self.ignore(self.FIRE_KEY)
        self.accept(self.FIRE_KEY+"-up", self.__fireKeyReleased)
        self.__firePressed()

    def __upKeyPressed(self):
        self.ignore(self.UP_KEY)
        self.accept(self.UP_KEY+"-up", self.__upKeyReleased)
        self.__upPressed()

    def __downKeyPressed(self):
        self.ignore(self.DOWN_KEY)
        self.accept(self.DOWN_KEY+"-up", self.__downKeyReleased)
        self.__downPressed()

    def __leftKeyPressed(self):
        self.ignore(self.LEFT_KEY)
        self.accept(self.LEFT_KEY+"-up", self.__leftKeyReleased)
        self.__leftPressed()

    def __rightKeyPressed(self):
        self.ignore(self.RIGHT_KEY)
        self.accept(self.RIGHT_KEY+"-up", self.__rightKeyReleased)
        self.__rightPressed()

    def __fireKeyReleased(self):
        self.ignore(self.FIRE_KEY+"-up")
        self.accept(self.FIRE_KEY, self.__fireKeyPressed)
        #self.__fireReleased() #this doesn't exist

    def __leftKeyReleased(self):
        self.ignore(self.LEFT_KEY+"-up")
        self.accept(self.LEFT_KEY, self.__leftKeyPressed)
        self.__leftReleased()

    def __rightKeyReleased(self):
        self.ignore(self.RIGHT_KEY+"-up")
        self.accept(self.RIGHT_KEY, self.__rightKeyPressed)
        self.__rightReleased()

    def __upKeyReleased(self):
        self.ignore(self.UP_KEY+"-up")
        self.accept(self.UP_KEY, self.__upKeyPressed)
        self.__upReleased()

    def __downKeyReleased(self):
        self.ignore(self.DOWN_KEY+"-up")
        self.accept(self.DOWN_KEY, self.__downKeyPressed)
        self.__downReleased()


        
    # button event handlers (also used by keyboard event handlers)
    def __leaveCannon(self):
        self.notify.debug("__leaveCannon")
        self.sendUpdate('requestLeave')
        
    def __firePressed(self):
        self.notify.debug("fire pressed")

        if not self.boss.state == 'BattleTwo':
            self.notify.debug('boss is in state=%s, not firing' % self.boss.state)
            return
        
        #return
        # make sure everyone has the correct position
        self.__broadcastLocalCannonPosition()

        self.__unmakeGui()

        # send the 'cannon lit' message and wait for the server
        # to tell us the time that our cannon will shoot
        self.sendUpdate("setCannonLit",
                        [self.cannonPosition[0],
                         self.cannonPosition[1]])

    def __upPressed(self):
        self.notify.debug("up pressed")
        self.upPressed = self.__enterControlActive(self.upPressed)

    def __downPressed(self):
        self.notify.debug("down pressed")
        self.downPressed = self.__enterControlActive(self.downPressed)

    def __leftPressed(self):
        self.notify.debug("left pressed")
        self.leftPressed = self.__enterControlActive(self.leftPressed)

    def __rightPressed(self):
        self.notify.debug("right pressed")
        self.rightPressed = self.__enterControlActive(self.rightPressed)

    def __upReleased(self):
        self.notify.debug("up released")
        self.upPressed = self.__exitControlActive(self.upPressed)

    def __downReleased(self):
        self.notify.debug("down released")
        self.downPressed = self.__exitControlActive(self.downPressed)

    def __leftReleased(self):
        self.notify.debug("left released")
        self.leftPressed = self.__exitControlActive(self.leftPressed)

    def __rightReleased(self):
        self.notify.debug("right released")
        self.rightPressed = self.__exitControlActive(self.rightPressed)

    # __enterControlActive and __exitControlActive are used
    # to update the cannon control 'press reference counts'
    # leftPressed, rightPressed, upPressed, and downPressed
    # are all counts of how many devices (button, keys) are
    # activating that particular cannon control -- so if
    # someone is pressing 'right' on the keyboard and also
    # pressing on the 'right' button with the mouse,
    # rightPressed would be set to 2. A value of zero means
    # that the cannon control is inactive.
    def __enterControlActive(self, control):
        return control + 1

    def __exitControlActive(self, control):
        return max(0, control-1)

    def __spawnLocalCannonMoveTask(self):
        self.leftPressed = 0
        self.rightPressed = 0
        self.upPressed = 0
        self.downPressed = 0

        self.cannonMoving = 0

        task = Task(self.__localCannonMoveTask)
        task.lastPositionBroadcastTime = 0.
        taskMgr.add(task, self.LOCAL_CANNON_MOVE_TASK)

    def __killLocalCannonMoveTask(self):
        taskMgr.remove(self.LOCAL_CANNON_MOVE_TASK)
        if self.cannonMoving:
            self.sndCannonMove.stop()

    def __localCannonMoveTask(self, task):
        """ this task moves the cannon
        """
        pos = self.cannonPosition

        # these are used to determine if the cannon actually moved
        oldRot = pos[0]
        oldAng = pos[1]

        # cannon rotation
        rotVel = 0
        if self.leftPressed:
            rotVel += CANNON_ROTATION_VEL
        if self.rightPressed:
            rotVel -= CANNON_ROTATION_VEL
        pos[0] += rotVel * globalClock.getDt()
        if pos[0] < CANNON_ROTATION_MIN:
            pos[0] = CANNON_ROTATION_MIN
        elif pos[0] > CANNON_ROTATION_MAX:
            pos[0] = CANNON_ROTATION_MAX

        # cannon barrel angle
        angVel = 0
        if self.upPressed:
            angVel += CANNON_ANGLE_VEL
        if self.downPressed:
            angVel -= CANNON_ANGLE_VEL
        pos[1] += angVel * globalClock.getDt()
        if pos[1] < CANNON_ANGLE_MIN:
            pos[1] = CANNON_ANGLE_MIN
        elif pos[1] > CANNON_ANGLE_MAX:
            pos[1] = CANNON_ANGLE_MAX

        if oldRot != pos[0] or oldAng != pos[1]:
            if self.cannonMoving == 0:
                self.cannonMoving = 1
                base.playSfx(self.sndCannonMove, looping=1)

            self.__updateCannonPosition(self.localAvId)

            # periodically send a position update broadcast
            if task.time - task.lastPositionBroadcastTime > \
                                         CANNON_MOVE_UPDATE_FREQ:
                task.lastPositionBroadcastTime = task.time
                self.__broadcastLocalCannonPosition()
        else:
            if self.cannonMoving:
                self.cannonMoving = 0
                self.sndCannonMove.stop()
                # make sure everyone has the correct final position
                self.__broadcastLocalCannonPosition()

        return Task.cont


    def __broadcastLocalCannonPosition(self):
        # send a position update for the local cannon
        self.sendUpdate("setCannonPosition",
                        [self.cannonPosition[0],
                         self.cannonPosition[1]])

    def __updateCannonPosition(self, avId):
        self.cannon.setHpr(self.cannonPosition[0], 0., 0.)
        self.barrel.setHpr(0., self.cannonPosition[1], 0.)
        # squish the shadow to match the barrel pos
        maxP = 90
        newP = self.barrel.getP()
        yScale = 1-.5*float(newP)/maxP
        shadow = self.cannon.find("**/square_drop_shadow")
        shadow.setScale(1,yScale,1)

    def __createToonModels(self):
        assert self.notify.debug('__createToonModels')


        self.model_Created = 1
        # create the juror toon model
        #toon = self.av
        #let's use Flippy and up for now
        self.jurorToon = NPCToons.createLocalNPC(ToontownGlobals.LawbotBossBaseJurorNpcId + self.index)
                
        # store the toon's original scale
        self.toonScale = self.jurorToon.getScale()
        
        # force use of highest LOD
        #toon.useLOD(1000)
        
        # stick the toon under an additional node
        # in order to move the toon's local origin to its waist
        jurorToonParent = render.attachNewNode("toonOriginChange")
        self.jurorToon.wrtReparentTo(jurorToonParent)
        self.jurorToon.setPosHpr(0,0,-(self.jurorToon.getHeight()/2.),0,-90,0)
        
        self.toonModel = jurorToonParent

        # create the toon head
        self.toonHead = ToonHead.ToonHead()
        self.toonHead.setupHead(self.jurorToon.style)
        self.toonHead.reparentTo(hidden)

        # attach a chat balloon to the toonhead
        #tag = NametagFloat3d()
        #tag.setContents(Nametag.CSpeech | Nametag.CThought)
        #tag.setBillboardOffset(0)
        #tag.setAvatar(self.toonHead)
        #toon.nametag.addNametag(tag)

        #tagPath = self.toonHead.attachNewNode(tag.upcastToPandaNode())
        #tagPath.setPos(0, 0, 1)
        #self.toonHead.tag = tag

        # stuff the toon into his cannon
        self.__loadToonInCannon()

        # hide the avatar's dropshadow
        #self.av.dropShadow.hide()

        # create a copy of the drop shadow
        #self.dropShadow = self.shadowNode.copyTo(hidden)

        
    def __destroyToonModels(self):
        assert self.notify.debug("__destroyToonModels")
        #if (self.av != None):
        if (0):
            # show the toons original drop shadows..
            self.av.dropShadow.show()
            # ... and destroy the one used for flight
            if (self.dropShadow != None):
                self.dropShadow.removeNode()
                self.dropShadow = None

            self.hitBumper = 0
            self.hitTarget = 0
            self.angularVel = 0
            self.vel = Vec3(0,0,0)
            self.lastVel = Vec3(0,0,0)
            self.lastPos = Vec3(0,0,0)
            self.landingPos = Vec3(0,0,0)
            self.t = 0
            self.lastT = 0
            self.deltaT = 0
            self.av = None
            self.lastWakeTime = 0
            self.localToonShooting = 0
            
        if (self.toonHead != None):
            self.toonHead.reparentTo(hidden)
            self.toonHead.stopBlink()
            self.toonHead.stopLookAroundNow()
            self.toonHead = None
        if (self.toonModel != None):
            self.toonModel.removeNode()
            self.toonModel = None
        if (self.jurorToon != None):
            self.jurorToon.delete()
            self.jurorToon = None
        self.model_Created = 0

    def __loadToonInCannon(self):
        assert self.notify.debug("__loadToonInCannon")        
        # hide the full toon model
        self.toonModel.reparentTo(hidden)
        # show the toon head
        self.toonHead.startBlink()
        self.toonHead.startLookAround()
        # parent head to the cannon barrel
        self.toonHead.reparentTo(self.barrel)
        # put it up at the muzzle of the cannon, facing down
        self.toonHead.setPosHpr(0,6,0,0,-45,0)
        # restore proper scale (wrt render)
        sc = self.toonScale
        self.toonHead.setScale(render, sc[0], sc[1], sc[2])

    def exitCannon(self, avId):
        assert self.notify.debug('exitCannon')
        self.__unmakeGui()

        # The AI is telling us that avId has been sitting in the
        # cannon too long without firing.  We'll exit him out now.
        if self.avId == avId:
            # take down the gui
            self.av.reparentTo(render)
            self.__resetToonToCannon(self.av)

    def __resetToonToCannon(self, avatar):
        pos = None
        if not avatar:
            if self.avId:
                avatar = base.cr.doId2do.get(self.avId, None)
        if avatar:
            if hasattr(self,'cannon') and self.cannon:
                avatar.reparentTo(self.cannon)
                avatar.setPosHpr(3,0,0,90,0,0)                 
                #avatar.setPos(2,-4,0)
                avatar.wrtReparentTo(render)
            self.__resetToon(avatar)
        
            
    def __resetToon(self, avatar, pos = None):
        assert(self.notify.debug("%s __resetToon" % self.doId ))
        if avatar:
            self.__stopCollisionHandler(avatar)
            self.__setToonUpright(avatar, pos)
            if self.localToonShooting:
                self.notify.debug("toon setting position to %s" % pos)
                if pos:
                    base.localAvatar.setPos(pos)
                camera.reparentTo(avatar)
                camera.setPos( self.av.cameraPositions[0][0])
                place = base.cr.playGame.getPlace()
                if place:
                    place.setState('finalBattle')
            self.b_setLanded()

    def __stopCollisionHandler(self, avatar):
        assert(self.notify.debug("%s __stopCollisionHandler" % self.doId ))

        if avatar:
            avatar.loop('neutral')
            #camera.reparentTo(avatar)
            # Reset collisions
            if self.flyColNode:
                self.flyColNode = None
            if avatar == base.localAvatar:
                avatar.collisionsOn()
            self.flyColSphere = None
            if self.flyColNodePath:
                base.cTrav.removeCollider(self.flyColNodePath)
                self.flyColNodePath.removeNode()
                self.flyColNodePath = None

            self.handler = None

    def __setToonUpright(self, avatar, pos=None):
        if avatar:
            if not pos:
                pos = avatar.getPos(render)
            avatar.setPos(render,pos)
            avatar.loop('neutral')

            #since the avatar doesn't fly, skipping the rest

    def b_setLanded(self):
        assert self.notify.debug('b_setLanded')
        self.d_setLanded()
        #self.setLanded()
            
    def d_setLanded(self):
        assert self.notify.debug("d_setLanded ocalToonshooting = %s" % self.localToonShooting)
        # The shooter can tell the server he's landed, and then the server
        # will pass the message along to all the other clients in this zone.
        if self.localToonShooting:
            self.sendUpdate("setLanded", [])


    def setLanded(self):
        assert self.notify.debug('setLanded')        
        self.removeAvFromCannon()

    def removeAvFromCannon(self):
        assert(self.notify.debug("%s removeAvFromCannon" % self.doId))
        if (self.av != None):
            assert(self.notify.debug("removeAvFromCannon: destroying toon models"))
            # make sure colliion handling is off
            self.__stopCollisionHandler(self.av)
            self.av.resetLOD()
            place = base.cr.playGame.getPlace()

            if self.av == base.localAvatar:
                if place:
                    place.setState('finalBattle')

            self.av.loop('neutral')


            self.av.setPlayRate(1.0, 'run')
            
            # this is needed for distributed toons
            if self.av.getParent().getName() == "toonOriginChange":
                self.av.wrtReparentTo(render)
                self.__setToonUpright(self.av)
            if self.av == base.localAvatar:
                self.av.startPosHprBroadcast()
            #self.av.setParent(ToontownGlobals.SPRender)
            self.av.startSmooth()
            self.av.setScale(1,1,1)
            self.ignore(self.av.uniqueName("disable"))
            self.__destroyToonModels()


    def setCannonWillFire(self, avId, fireTime, zRot, angle, timestamp):
        # the server is telling us that a cannon will fire at a specific time
        self.notify.debug("setCannonWillFire: " + str(avId)
                          + ": zRot=" + str(zRot) + ", angle=" + str(angle)
                          + ", time=" + str(fireTime))

        # we might get this message from the server before we even get a
        # chance to createToonModel...for instance if we just walked in the zone
        # If this is the case, don't create a fire task
        if not self.model_Created:
            self.notify.warning("We walked into the zone mid-flight, so we won't see it")
            return

        # set the cannon's position
        # NOTE: do this for the local toon; cannon angles may have been
        # modified by conversion to and from fixed-point, and we want
        # to have the same values that all the other clients have
        self.cannonPosition[0] = zRot
        self.cannonPosition[1] = angle
        self.__updateCannonPosition(avId)

        # create a task to fire off the cannon
        task = Task(self.__fireCannonTask)
        task.avId = avId

        # fireTime is in game time
        ts = globalClockDelta.localElapsedTime(timestamp)
        task.fireTime = fireTime - ts
        if (task.fireTime < 0.0):
            task.fireTime = 0.0
        taskMgr.add(task, self.taskName("fireCannon"))

    def __fireCannonTask(self, task):
        """
        spawn a task sequence to shoot the cannon, fly
        the avatar through the air, handle the toon's landing
        """
        launchTime = task.fireTime
        avId = task.avId

        assert(self.notify.debug("FIRING CANNON FOR AVATAR " + str(avId)))

        if self.toonHead == None or (not self.boss.state == 'BattleTwo'):
            #hopefully fix crash 18821
            return Task.done

        # calculate the trajectory
        flightResults = self.__calcFlightResults(avId, launchTime)
        # pull all the results into the local namespace
        for key in flightResults:
            exec "%s = flightResults['%s']" % (key, key)

        self.notify.debug("start position: " + str(startPos))
        self.notify.debug("start velocity: " + str(startVel))
        self.notify.debug("time of launch: " + str(launchTime))
        self.notify.debug("time of impact: " + str(timeOfImpact))
        self.notify.debug("location of impact: " +
                          str(trajectory.getPos(timeOfImpact)))
        
        #if hitWhat == self.HIT_WATER:
        #    self.notify.debug("toon will land in the water")
        #elif hitWhat == self.HIT_TOWER:
        #    self.notify.debug("toon will hit the tower")
        #else:
        #    self.notify.debug("toon will hit the ground")

        # get the toon out of the cannon
        # hide the toon's head
        head = self.toonHead
        head.stopBlink()
        head.stopLookAroundNow()
        head.reparentTo(hidden)
        
        # show the whole body, posbang it to where the
        # head was

        #av = self.toonModel
        #av.reparentTo(render)
        #av.setPos(startPos)
        juror = self.toonModel
        juror.reparentTo(render)
        juror.setPos(startPos)
        
        barrelHpr = self.barrel.getHpr(render)

        
        # subtract 90 degrees from hpr since barrels hpr measures the angle from the ground
        # and the toons hpr measures from vUp.
        #av.setHpr(startHpr)        
        juror.setHpr(startHpr)
        #avatar = self.av


        #avatar.loop('swim')
        #avatar.setPosHpr(0,0,-(avatar.getHeight()/2.),0,0,0)

        self.jurorToon.loop('swim')
        self.jurorToon.setPosHpr(0,0,-(self.jurorToon.getHeight()/2.),0,0,0)
        
        
        # stock the tasks up with the info they need
        # store the info in a shared dictionary
        info = {}
        info['avId'] = avId
        info['trajectory'] = trajectory
        info['launchTime'] = launchTime
        info['timeOfImpact'] = timeOfImpact
        info['hitWhat'] = hitWhat
        info['toon'] = self.toonModel
        info['hRot'] = self.cannonPosition[0]
        info['haveWhistled'] = 0
        info['maxCamPullback'] = CAMERA_PULLBACK_MIN

        if self.localToonShooting:
            #camera.reparentTo(self.av)
            camera.reparentTo(juror)
            camera.setP(45.0)
            camera.setZ(-10.0)

        # Set up collision test
        self.flyColSphere = CollisionSphere(0, 0, 
                                            self.av.getHeight()/2.0, 1.0)
        self.flyColNode = CollisionNode(self.uniqueName('flySphere'))
        self.flyColNode.setCollideMask(ToontownGlobals.WallBitmask  | \
                                       ToontownGlobals.FloorBitmask  \
                                       | ToontownGlobals.PieBitmask
                                      )
        self.flyColNode.addSolid(self.flyColSphere)
        #self.flyColNodePath = self.av.attachNewNode(self.flyColNode)
        self.flyColNodePath = self.jurorToon.attachNewNode(self.flyColNode)
        #self.flyColNodePath.show()
        self.flyColNodePath.setColor(1,0,0,1)
        self.handler = CollisionHandlerEvent()
        self.handler.setInPattern(self.uniqueName('cannonHit'))
        base.cTrav.addCollider(self.flyColNodePath, self.handler) 
        self.accept(self.uniqueName('cannonHit'), self.__handleCannonHit)

        # create the tasks
        shootTask = Task(self.__shootTask, self.taskName("shootTask"))
        #smokeTask = Task(self.__smokeTask, self.taskName("smokeTask"))
        flyTask = Task(self.__flyTask, self.taskName("flyTask"))
        # put the info dict on each task
        shootTask.info = info
        flyTask.info = info

        #seqTask = Task.sequence(shootTask, smokeTask, flyTask)
        seqTask = Task.sequence(shootTask,  flyTask)
        
        # spawn the new task
        taskMgr.add(seqTask, self.taskName('flyingToon') + "-" + str(avId))
        self.acceptOnce(self.uniqueName("stopFlyTask"), self.__stopFlyTask)
        return Task.done
        
    def __toRadians(self, angle):
        return angle * 2.0 * math.pi / 360.0

    def __toDegrees(self, angle):
        return angle * 360.0 / (2.0 * math.pi)

    def __calcFlightResults(self, avId, launchTime):
        """
        returns dict with keys:
        startPos, startHpr, startVel, trajectory, timeOfImpact, hitWhat
        """
        assert self.notify.debug('__calcFlightResults avId=%d launchtime=%f' % (avId, launchTime))
        head = self.toonHead
        startPos = head.getPos(render)
        startHpr = head.getHpr(render)

        # get the cannon's orientation relative to render
        hpr = self.barrel.getHpr(render)

        # calc the initial velocity in render space
        rotation = self.__toRadians(hpr[0])
        angle = self.__toRadians(hpr[1])
        horizVel = INITIAL_VELOCITY * math.cos(angle)
        xVel = horizVel * -math.sin(rotation)
        yVel = horizVel * math.cos(rotation)
        zVel = INITIAL_VELOCITY * math.sin(angle)
        startVel = Vec3(xVel, yVel, zVel)

        trajectory = Trajectory.Trajectory(launchTime, startPos, startVel)
        self.trajectory = trajectory
        # check if we hit any treasures along the way
        #hitTreasures = self.__calcHitTreasures(trajectory)

        # figure out what will be hit, and when
        timeOfImpact, hitWhat = self.__calcToonImpact(trajectory)
        
        
        return {
            'startPos' : startPos,
            'startHpr' : startHpr,
            'startVel' : startVel,
            'trajectory' : trajectory,
            'timeOfImpact' : 3*timeOfImpact,
            'hitWhat' : hitWhat,
            }

    def __calcToonImpact(self, trajectory):
        """__calcToonImpact(self, waterTower)
        calculate the result of the toon's trajectory
        check if the toon will land in the water, hit the tower, or hit
        the ground
        returns time of impact, what toon hits
        """

        assert self.notify.debug('__calcToonImpact')

        # calculate when the toon will hit the ground
        # (assume absolute lowest point of terrain is above GROUND_PLANE_MIN)
        t_groundImpact = trajectory.checkCollisionWithGround(GROUND_PLANE_MIN)
        if t_groundImpact >= trajectory.getStartTime():
            # toon will hit the ground (...he'd best...)
            return t_groundImpact, self.HIT_GROUND
        else:
            # toon won't hit the ground??
            self.notify.error("__calcToonImpact: toon never impacts ground?")
            # return something
            return 0.0, self.HIT_GROUND

    def __handleCannonHit(self, collisionEntry):
        assert(self.notify.debug("%s __handleCannonHit" % self.doId))
        if self.av == None or self.flyColNode == None:
            return

        interPt  = collisionEntry.getSurfacePoint(render)
        hitNode = collisionEntry.getIntoNode().getName()
        
        assert self.notify.debug('hitNode=%s interPt = %s' % (hitNode,interPt))
        fromNodePath = collisionEntry.getFromNodePath()
        intoNodePath = collisionEntry.getIntoNodePath()
        assert self.notify.debug('from = %s, \n into = %s' % (fromNodePath, intoNodePath))



        ignoredHits = ['NearBoss']

        for nodeName in ignoredHits:
            if hitNode == nodeName: #intoNodePath.find('**/' + nodeName):
                assert self.notify.debug('ignoring hit to %s' % nodeName)
                return

        #if we hit something, end the fly Task
        self.__stopFlyTask(self.avId)


        #self.__stopCollisionHandler(self.av)
        self.__stopCollisionHandler(self.jurorToon)

        #reparent the camera now so dustcloud works
        if self.localToonShooting:
            camera.wrtReparentTo(render)

        pos = interPt
        hpr = self.jurorToon.getHpr()

        track = Sequence()
        #track.append(Func(self.av.wrtReparentTo, render))

        if self.localToonShooting:
            pass
            #track.append(Func(self.jurorToon.collisionsOff))

        chairlist = ['trigger-chair']
        for index in range(len(ToontownGlobals.LawbotBossChairPosHprs)):
            chairlist.append('Chair-%s' % index)
            
        if hitNode in chairlist:
            track.append(Func(self.__hitChair, self.jurorToon, pos))
            track.append(Wait(1.0))
            track.append(Func(self.__setToonUpright, self.av)) #, self.landingPos))

            if (self.av == base.localAvatar):
                #figure out which chair we hit
                strs = hitNode.split('-')
                chairNum = int(strs[1])
                self.boss.sendUpdate('hitChair',[chairNum, self.index])
            
        else:
            track.append(Func(self.__hitGround, self.jurorToon, pos))
            track.append(Wait(1.0))
            track.append(Func(self.__setToonUpright, self.av)) #, self.landingPos))

        track.append(Func(self.b_setLanded))
        if self.localToonShooting:
            #track.append(Func(self.jurorToon.collisionsOn))
            #track.append(Func(camera.reparentTo,self.av))
            #track.append(Func(camera.setPos, self.av.cameraPositions[0][0]))
            pass

            
        if self.hitTrack:
            self.hitTrack.finish()
        self.hitTrack = track
        self.hitTrack.start()
                              
    def enterCannonHit(self, collisionEntry):
        assert self.notify.debug('enterCannonHit')
        pass

    def __shootTask(self, task):
        assert self.notify.debug('__shotTask')
        base.playSfx(self.sndCannonFire)

        # show the drop shadow
        #self.dropShadow.reparentTo(render)

        return Task.done

    def __flyTask(self, task):
        #assert self.notify.debug('__flyTask')
        toon = task.info['toon']
        if toon.isEmpty():
            # we have deleted this toon, before this task has been ended.  end now
            self.__resetToonToCannon(self.av)
            return Task.done

        curTime = task.time + task.info['launchTime']
        # don't overshoot past the time of landing
        t = min(curTime, task.info['timeOfImpact'])
        self.lastT = self.t
        self.t = t
        deltaT = self.t-self.lastT
        self.deltaT = deltaT
        
        if t >= task.info['timeOfImpact']:
            # we are just flying into space at this point, end the fly task
            self.__resetToonToCannon(self.av)
            return Task.done

        # get position
        pos = task.info['trajectory'].getPos(t)
            
        # update toon position
        toon.setFluidPos(pos)
        #print ("pos(%s,%s,%s)" % (pos[0],pos[1],pos[2]))

        # update drop shadow position
        #shadowPos = Point3(pos)
        #shadowPos.setZ(SHADOW_Z_OFFSET)
        #self.dropShadow.setPos(shadowPos)
        
        # set the toon's tilt based on its velocity
        # h rotation is constant, and corresponds to the cannon's
        # z rotation (left to right)
        vel = task.info['trajectory'].getVel(t)
        run = math.sqrt((vel[0] * vel[0]) + (vel[1] * vel[1])) # TODO:
                                                               #precompute this
        rise = vel[2]
        theta = self.__toDegrees(math.atan(rise/run))
        toon.setHpr(self.cannon.getH(render),-90 + theta,0)

        view = 2
        #view = 0
        #lookat = toon
        

        # move the camera above the toon, and look at him
        lookAt = task.info['toon'].getPos(render)
        hpr = task.info['toon'].getHpr(render)
        
        if self.localToonShooting:
            if view == 0:
                camera.wrtReparentTo(render)
                camera.lookAt(lookAt)
            elif view == 1: 
                # third person pt of view
                camera.reparentTo(render)
                camera.setPos(render, 100, 100, 35.25)
                camera.lookAt(render, lookAt)
            elif view == 2:
                # fly behind the toon
                if hpr[1] > -90:
                    # set the camera behind the toon (in toon coordinates)
                    camera.setPos(0,0,-30)
                    # now make sure it is always above the toon
                    if camera.getZ() < lookAt[2]:
                        camera.setZ(render, lookAt[2]+10)
                    camera.lookAt(Point3(0,0,0))
        

            # pickup treasures along the way
            #self.__pickupTreasures(t)
        
        return Task.cont

    def __stopFlyTask(self, avId):
        assert(self.notify.debug("%s(%s)" % (self.uniqueName("stopFlyTask"), avId)))
        taskMgr.remove(self.taskName('flyingToon') + "-" + str(avId))


    def __hitGround(self, avatar, pos, extraArgs=[]):
        assert(self.notify.debug("__hitGround"))
        hitP = avatar.getPos(render)
        #print "hitGround pos = %s, hitP = %s" % (pos, hitP)
        #print "avatar hpr = %s" % avatar.getHpr()
        h = self.barrel.getH(render)
        avatar.setPos(pos[0],pos[1],pos[2]+avatar.getHeight()/3.0)
        # make avatar look in direction of velocity
        avatar.setHpr(h,-135,0)

        #print "parent = %s" % avatar.getParent()
        #print "new pos,hpr = %s,%s" % (avatar.getPos(render),avatar.getHpr(render)) 
        self.dustCloud.setPos(render, pos[0], pos[1], pos[2]+avatar.getHeight()/3.0)
        self.dustCloud.setScale(0.35)
        self.dustCloud.play()
        base.playSfx(self.sndHitGround)

        #make him disappear in the dust cload
        avatar.hide()
        
        # Make him wiggle his legs
        #avatar.setPlayRate(2.0, 'run')
        #avatar.loop("run")

    def __hitChair(self, avatar, pos, extraArgs=[]):
        assert(self.notify.debug("__hitGround"))
        hitP = avatar.getPos(render)
        #print "hitGround pos = %s, hitP = %s" % (pos, hitP)
        #print "avatar hpr = %s" % avatar.getHpr()
        h = self.barrel.getH(render)
        avatar.setPos(pos[0],pos[1],pos[2]+avatar.getHeight()/3.0)
        # make avatar look in direction of velocity
        avatar.setHpr(h,-135,0)

        #print "parent = %s" % avatar.getParent()
        #print "new pos,hpr = %s,%s" % (avatar.getPos(render),avatar.getHpr(render)) 
        self.dustCloud.setPos(render, pos[0], pos[1], pos[2]+avatar.getHeight()/3.0)
        self.dustCloud.setScale(0.35)
        self.dustCloud.play()
        base.playSfx(self.sndHitGround)
        base.playSfx(self.sndHitChair)

        #make him disappear in the dustcloud
        avatar.hide()
        
        # Make him wiggle his legs                
        #avatar.setPlayRate(2.0, 'run')
        #avatar.loop("run")


    def generateCannonAppearTrack( self, avatar):
        """
        Based on DistributedStartingBlock.generateKartAppearTrack
        """
        self.cannon.setScale(0.1)
        self.cannon.show()

        kartTrack = Parallel(
            Sequence( ActorInterval(avatar, "feedPet"),
                      Func(avatar.loop,'neutral')),
            Sequence( Func(self.cannon.reparentTo,avatar.rightHand),
                      #Func(self.cannon.setPos,.1,0,-2),
                      Wait(2.1),
                      Func(self.cannon.wrtReparentTo, render),
                      Func( self.cannon.setShear, 0, 0, 0),
                      Parallel( LerpHprInterval( self.cannon,
                                                 hpr = self.nodePath.getHpr( render ),
                                                 duration = 1.2 ),
                                ProjectileInterval( self.cannon,
                                                    endPos = self.nodePath.getPos( render ),
                                                    duration = 1.2,
                                                    gravityMult = 0.45 ) ),
                      Wait( 0.2 ),
                      #Func( self.cannon.setActiveShadow, True ),
                      # Must be a cleaner way to do this.
                      Sequence( LerpScaleInterval( self.cannon,
                                                   scale = Point3( 1.1, 1.1, .1),
                                                   duration = 0.2),
                                LerpScaleInterval( self.cannon,
                                                   scale = Point3( .9, .9, .1 ),
                                                   duration = 0.1 ),
                                LerpScaleInterval( self.cannon,
                                                   scale = Point3( 1., 1., .1 ),
                                                   duration = 0.1 ),
                                LerpScaleInterval( self.cannon,
                                                   scale = Point3( 1., 1., 1.1 ),
                                                   duration = 0.2 ),
                                LerpScaleInterval( self.cannon,
                                                   scale = Point3( 1., 1., .9 ),
                                                   duration = 0.1 ),
                                LerpScaleInterval( self.cannon,
                                                   scale = Point3( 1., 1., 1. ),
                                                   duration = 0.1 ),
                                Func( self.cannon.wrtReparentTo, self.nodePath ) ) ) )

        return kartTrack
                      
                           
    
