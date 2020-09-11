#-------------------------------------------------------------------------------
# Contact: Sam Polglase (Schell Games)
# Created: March 2010
#
# Purpose: This module currently contains all the classes necessary to run the Congdo
#          minigame.  Soon all these classes will get split into their own modules
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Config Overrides:
# cogdo-flying-game-disable-death bool
#    Allows the dev to run the flying game without the death state
#------------------------------------------------------------------------------

from direct.showbase.DirectObject import DirectObject
from direct.showbase.PythonUtil import bound as clamp
from direct.fsm.FSM import FSM

from pandac.PandaModules import NodePath, VBase3, Vec3, VBase4, Fog

from toontown.minigame.DistributedMinigame import DistributedMinigame
from toontown.minigame import ArrowKeys
from toontown.toonbase import ToontownTimer

import CogdoFlyingGameGlobals

def loadMockup(fileName, dmodelsAlt="coffin"):
    try:
        model = loader.loadModel(fileName)
    except IOError:
        model = loader.loadModel("phase_4/models/props/%s" % dmodelsAlt)

    return model

class DistCogdoFlyingGame(DistributedMinigame):
    """
    Flying Cogdominium Minigame client Distributed Object!
    """
    notify = directNotify.newCategory("DistCogdoFlyingGame")

    def __init__(self, cr):
        DistributedMinigame.__init__(self, cr)
        #print "adding onCodeReload"
        self.accept("onCodeReload", self.codeReload)

        #print "FLYING COGDO GAME CREATED!"
        self.game = CogdoFlyingGame(self)

    def codeReload(self):
        reload(CogdoFlyingGameGlobals)

    def load(self):
        DistributedMinigame.load(self)
        self.game.load()

    # This isn't get called, that seems bad!
    def unload(self):
        self.game.unload()
        del self.game
        self.ignore("onCodeReload")

        print "Unload Distributed Game"

        DistributedMinigame.unload(self)

    def onstage(self):
        self.game.onstage()
        DistributedMinigame.onstage(self)

    # This isn't get called, that seems bad!
    def offstage(self):
        self.game.offstage()
        DistributedMinigame.offstage(self)

    def announceGenerate(self):
        DistributedMinigame.announceGenerate(self)

    # broadcast
    def setGameStart(self, timestamp):
        DistributedMinigame.setGameStart(self, timestamp)
        self.acceptOnce("escape", self.d_requestExit)
        self.game.enable()
        #self.fsm.request('Game')
        #print "setGameStart"

    def delete(self):
        pass


class CogdoFlyingGame(DirectObject):
    UPDATE_TASK_NAME = "CogdoFlyingGameUpdate"
    GAME_COMPLETE_TASK_NAME = "CogdoFlyingGameCompleteTask"

    def __init__(self, distGame):
        self.distGame = distGame

        # Unused currently
        self.players = {}
        self.localPlayer = CogdoFlyingLocalPlayer(self, base.localAvatar)

        # Unused currently
        self.toonDropShadows = []
        
        self.startPlatform = None
#        self.currentPlatform = None
        self.endPlatform = None
        self.fuelPlatforms = {}
        self.isGameComplete = False
        
        self.upLimit = 0.0
        self.downLimit = 0.0
        self.leftLimit = 0.0
        self.rightLimit = 0.0

    def load(self):
        self.root = NodePath('root')
        self.root.reparentTo(render)
        self.root.stash()

        self.world = loadMockup("cogdominium/mockup.egg")
        self.world.reparentTo(self.root)
        self.world.stash()
        
        # Setup and placement of starting platform
        self.startPlatform = loadMockup("cogdominium/start_platform.egg")
        startPlatformLoc = self.world.find("**/start_platform_loc")
        self.startPlatform.reparentTo(startPlatformLoc)
        colModel = self.startPlatform.find("**/col_floor")
        colModel.setTag('start_platform', '%s' % base.localAvatar.doId)
        
        # Here we set the current platform for the local player
        self.localPlayer.setCheckpointPlatform(self.startPlatform)
        
        # Setup and placement of the end platform
        self.endPlatform = loadMockup("cogdominium/end_platform.egg")
        endPlatformLoc = self.world.find("**/end_platform_loc")
        self.endPlatform.reparentTo(endPlatformLoc)
        colModel = self.endPlatform.find("**/col_floor")
        colModel.setTag('end_platform', '%s' % base.localAvatar.doId)
        
        # Setup and placement for all the fuel platforms
        fuelPlatformModel = loadMockup("cogdominium/fuel_platform.egg")
        fuelIndex = 1
        fuelLoc = self.world.find('**/fuel_platform_loc_%d' % fuelIndex)
        while not fuelLoc.isEmpty():
            fuelModel = NodePath("fuel_platform_%d" % fuelIndex)
            fuelPlatformModel.copyTo(fuelModel)
            fuelModel.reparentTo(fuelLoc)
            colModel = fuelModel.find("**/col_floor")
            colModel.setTag('fuel_platform', '%s' % base.localAvatar.doId)
            colModel.setTag('isUsed', '%s' % 0)
            self.fuelPlatforms[fuelModel.getName()] = fuelModel
            fuelIndex += 1
            fuelLoc = self.world.find('**/fuel_platform_loc_%d' % fuelIndex)
            
        
        self.accept("entercol_floor", self.handleCollision)
        
        self.skybox = self.world.find("**/skybox")
        self.upLimit = self.world.find("**/limit_up").getPos(render).getZ()
        self.downLimit = self.world.find("**/limit_down").getPos(render).getZ()
        self.leftLimit = self.world.find("**/limit_left").getPos(render).getX()
        self.rightLimit = self.world.find("**/limit_right").getPos(render).getX()

        del fuelPlatformModel

        self._initFog()


    def unload(self):
        self.__stopUpdateTask()
        self.__stopGameCompleteTask()
        self._destroyFog()
#        print "Unload Flying CogdoGame"
        self.localPlayer.unload()
        del self.localPlayer

        self.fuelPlatforms.clear()
        self.endPlatform = None

        self.world.detachNode()
        del self.world

        self.root.detachNode()
        del self.root
        
        self.ignore("entercol_floor")
    
    def handleCollision(self, collEntry):
        fromNodePath = collEntry.getFromNodePath()
        intoNodePath = collEntry.getIntoNodePath()
        intoName = intoNodePath.getName()
        fromName = fromNodePath.getName()
        
        if intoNodePath.getTag('fuel_platform') != "":
            if not int(intoNodePath.getTag('isUsed')) or CogdoFlyingGameGlobals.FlyingGame.MULTIPLE_REFUELS_PER_STATION:
                intoNodePath.setTag('isUsed','%s' % 1)
                self.localPlayer.setCheckpointPlatform(intoNodePath.getParent())
                self.localPlayer.request("Refuel")
        if intoNodePath.getTag('end_platform') != "":
            self.localPlayer.request("WaitingForWin")
    
    def enable(self):
        self.localPlayer.request("FreeFly")
        self.__startUpdateTask()
        self.isGameComplete = False

    def disable(self):
        self.__stopUpdateTask()
        self.__stopGameCompleteTask()
        self.localPlayer.request("Inactive")

    def _initFog(self):
        self.fog = Fog("FlyingFog")
        self.fog.setColor(VBase4(0.8, 0.8, 0.8, 1.0))
        self.fog.setLinearRange(100.0, 400.0)

        self._renderFog = render.getFog()
        render.setFog(self.fog)

    def _destroyFog(self):
        render.clearFog()
        del self.fog
        del self._renderFog

    def onstage(self):
        self.root.unstash()
        self.world.unstash()

        self.localPlayer.onstage()

    def offstage(self):
        self.__stopUpdateTask()
        self.world.stash()
        self.root.stash()
        self.localPlayer.offstage()

        #TODO: Temp solution, this is supposed to come from the minigame
        # Which means the minigame isn't getting cleaned up properly look into this
        self.unload()

    def handleToonJoined(self, toon):
        # Not used, no multiplayer support in yet
        if toon == base.localAvatar:
            player = CogdoFlyingLocalPlayer(toon)
            player.entersActivity()

            self.localPlayer = player
        else:
            player = CogdoFlyingPlayer(toon)
            player.entersActivity()

        self.players[toon.doId] = player

    def __startUpdateTask(self):
        self.__stopUpdateTask()
        taskMgr.add(self.__updateTask, CogdoFlyingGame.UPDATE_TASK_NAME, 45)

    def __stopUpdateTask(self):
        taskMgr.remove(CogdoFlyingGame.UPDATE_TASK_NAME)
    
    def __stopGameCompleteTask(self):
        taskMgr.remove(CogdoFlyingGame.GAME_COMPLETE_TASK_NAME)
    
    def gameComplete(self):
        self.localPlayer.request("Win")
    
    def __updateTask(self, task):
        self.localPlayer.update()

        #TODO:flying: make this win condition stuff work for multiple toons
        if self.localPlayer.state == "WaitingForWin" and not self.isGameComplete:
            self.isGameComplete = True
            taskMgr.doMethodLater(6.0, self.gameComplete, CogdoFlyingGame.GAME_COMPLETE_TASK_NAME, extraArgs=[])
    
        self.skybox.setPos(self.skybox.getPos().getX(),
                           self.localPlayer.toon.getPos().getY(),
                           self.skybox.getPos().getZ())
        return Task.cont

from direct.directnotify import DirectNotifyGlobal

class CogdoFlyingPlayer(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory( "CogdoFlyingPlayer" )

    def __init__(self, toon):
        FSM.__init__(self, "CogdoFlyingPlayer")

        self.defaultTransitions = {
            "Inactive" : ["FreeFly", "Inactive"],
            "FreeFly" : ["Inactive", "FlyingUp", "Death", "Refuel", "WaitingForWin"],
            "FlyingUp" : ["Inactive", "FreeFly", "Death", "Refuel", "WaitingForWin"],
            "Death" : ["FreeFly", "Inactive"],
            "Refuel" : ["FreeFly", "Inactive"],
            "WaitingForWin" : ["Win", "Inactive"],
            "Win" : ["Inactive"],
        }

        self.toon = toon
        self.toon.setActiveShadow(True)

    def enable(self):
        pass

    def unload(self):
        del self.toon

    def onstage(self):
        self.request("Inactive")

    def offstage(self):
        self.request("Inactive")

    def enterInactive(self):
        CogdoFlyingPlayer.notify.info( "enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState) )

    def exitInactive(self):
        CogdoFlyingPlayer.notify.debug( "exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState) )

    def enterFreeFly(self):
        CogdoFlyingPlayer.notify.info( "enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState) )

    def exitFreeFly(self):
        CogdoFlyingPlayer.notify.debug( "exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState) )

    def enterFlyingUp(self):
        CogdoFlyingPlayer.notify.info( "enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState) )

    def exitFlyingUp(self):
        CogdoFlyingPlayer.notify.debug( "exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState) )

    def enterDeath(self):
        CogdoFlyingPlayer.notify.info( "enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState) )

    def exitDeath(self):
        CogdoFlyingPlayer.notify.debug( "exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState) )
        
    def enterRefuel(self):
        CogdoFlyingPlayer.notify.info( "enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState) )

    def exitRefuel(self):
        CogdoFlyingPlayer.notify.debug( "exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState) )

    def enterWaitingForWin(self):
        CogdoFlyingPlayer.notify.info( "enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState) )

    def exitWaitingForWin(self):
        CogdoFlyingPlayer.notify.debug( "exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState) )

    def enterWin(self):
        CogdoFlyingPlayer.notify.info( "enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState) )

    def exitWin(self):
        CogdoFlyingPlayer.notify.debug( "exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState) )


from direct.task.Task import Task
from direct.interval.FunctionInterval import Wait
from direct.interval.IntervalGlobal import Func, LerpHprInterval, LerpFunctionInterval, ActorInterval
from direct.interval.MetaInterval import Sequence, Parallel

from toontown.battle import BattleProps

class CogdoFlyingLocalPlayer(CogdoFlyingPlayer):

    def __init__(self, game, toon):
        CogdoFlyingPlayer.__init__(self, toon)
        self.velocity = Vec3(0.0,0.0,0.0)
        self.lastVelocity = Vec3(0.0,0.0,0.0)
        self.instantaneousVelocity = Vec3(0.0,0.0,0.0)
        self.oldPos = Vec3(0.0,0.0,0.0)
        self.game = game
        self.inputMgr = CogdoFlyingInputManager()
        self.cameraMgr = CogdoFlyingCameraManager(self, camera, render)
        self.guiMgr = CogdoFlyingGuiManager(self)
        
        self.checkpointPlatform = None
        
        self.fuel = 0.0
        self.props = {}
        
        self.initModels()
        self.initIntervals()
        
        self.propSound = base.loadSfx('phase_4/audio/sfx/TB_propeller.wav')


    def initModels(self):
        # We place the propeller prop on all 3 lod's
        self.placePropeller('1000')
        self.placePropeller('500')
        self.placePropeller('250')

    def placePropeller(self, lod):
        prop = BattleProps.globalPropPool.getProp('propeller')
        prop.setScale(1.1)
        
        self.props[lod] = prop
        
        head = base.localAvatar.getPart('head', lod)
        
        if head.isEmpty():
            return

        prop.reparentTo(head)
        animal = base.localAvatar.style.getAnimal()
        if (animal == 'dog') or (animal == 'bear') or (animal == 'horse'):
            torso = base.localAvatar.style.torso
            legs = base.localAvatar.style.legs
            if ((torso == 'ls') or (torso == 'ld')) and (legs == 'l'):
                prop.setZ(-1.3)
            else:
                prop.setZ(-0.7)
        elif (animal == 'mouse') or (animal == 'duck'):
            prop.setZ(0.5)
        elif (animal == 'cat'):
            prop.setZ(-0.3)
        elif (animal == 'rabbit'):
            prop.setZ(-0.5)
        elif (animal == 'monkey'):
            prop.setZ(0.3)
        elif (animal == 'pig'):
            prop.setZ(-0.7)

    def initIntervals(self):
        self.deathInterval = Sequence(
            Func(self.inputMgr.disable),
            Parallel(
                LerpHprInterval(self.toon, 1.0, Vec3(720,0,0)),
                LerpFunctionInterval(self.toon.setScale, fromData=1.0, toData=0.0, duration=1.0)
            ),
            Func(self.resetToon),
            Wait(0.5), # Added this because with no pause here the FreeFly prop sound was attached to the old toon pos
            Func(self.request, "FreeFly"),
            name="%s.deathInterval" % (self.__class__.__name__)
        )
        
        self.refuelInterval = Sequence(
            Func(self.guiMgr.setRefuelLerpFromData),
            Func(self.guiMgr.messageLabel.unstash),
            Parallel(
                self.guiMgr.refuelLerp,
                Sequence(
                    Func(self.guiMgr.setMessageLabelText, "Refueling"),
                    Wait(0.5),
                    Func(self.guiMgr.setMessageLabelText, "Refueling."),
                    Wait(0.5),
                    Func(self.guiMgr.setMessageLabelText, "Refueling.."),
                    Wait(0.5),
                    Func(self.guiMgr.setMessageLabelText, "Refueling..."),
                    Wait(0.5),
                ),
            ),
            Func(self.resetFuel),
            Func(self.guiMgr.messageLabel.stash),
            Func(self.request, "FreeFly"),
            name="%s.refuelInterval" % (self.__class__.__name__)
        )
        
        self.waitingForWinInterval = Sequence(
            Func(self.guiMgr.setMessageLabelText, "Waiting for other players"),
            Wait(1.5),
            Func(self.guiMgr.setMessageLabelText, "Waiting for other players."),
            Wait(1.5),
            Func(self.guiMgr.setMessageLabelText, "Waiting for other players.."),
            Wait(1.5),
            Func(self.guiMgr.setMessageLabelText, "Waiting for other players..."),
            Wait(1.5),
            name="%s.waitingForWinInterval" % (self.__class__.__name__)
        )
        
        self.winInterval = Sequence(
            Func(self.guiMgr.setMessageLabelText, ""),
            Wait(1.0),
            Func(self.guiMgr.winLabel.unstash),
            Wait(2.0),
            Func(self.guiMgr.winLabel.stash),
            Wait(0.5),
            Func(messenger.send, "escape"),
            name="%s.waitingForWinInterval" % (self.__class__.__name__)
        )

        self.slowPropTrack = Parallel(
            ActorInterval(self.props['1000'], 'propeller', startFrame = 8, endFrame = 23, playRate = 1.0),
            ActorInterval(self.props['500'], 'propeller', startFrame = 8, endFrame = 23, playRate = 1.0),
            ActorInterval(self.props['250'], 'propeller', startFrame = 8, endFrame = 23, playRate = 1.0),
        )
        self.fastPropTrack = Parallel(
            ActorInterval(self.props['1000'], 'propeller', startFrame = 8, endFrame = 23, playRate = 2.0),
            ActorInterval(self.props['500'], 'propeller', startFrame = 8, endFrame = 23, playRate = 2.0),
            ActorInterval(self.props['250'], 'propeller', startFrame = 8, endFrame = 23, playRate = 2.0),
        )

    def onstage(self):
#        print "local player onstage"
        CogdoFlyingPlayer.onstage(self)
        self.toon.reparentTo(render)
        self.toon.hideName()
        self.toon.setSpeed(0, 0)
#        self.toon.setAnimState('Happy',1.0)
        self.toon.loop('jump-idle')
        # When we had the toon in anim state swim we needed this so that the
        # player wasn't getting stuck to floors
        self.toon.controlManager.currentControls.setGravity(0)
#        print "setting gravity to 0"
        self.resetToon()
        self.cameraMgr.enable()
        self.cameraMgr.update()

    def offstage(self):
        #print "local player offstage"
        CogdoFlyingPlayer.offstage(self)
        self.cameraMgr.disable()
        base.localAvatar.controlManager.currentControls.setGravity(32.174*2.0)
        self.toon.showName()

        #self.unload()

    def unload(self):
#        print "unloading CogdoFlyingLocalPlayer"
        self.toon.showName()
        CogdoFlyingPlayer.unload(self)
        
        self.checkpointPlatform = None
        
        self.cameraMgr.disable()
        del self.cameraMgr

        base.localAvatar.controlManager.currentControls.setGravity(32.174*2.0)
        del self.game
        
        self.inputMgr.destroy()
        del self.inputMgr
        
        self.props['1000'].detachNode()
        self.props['500'].detachNode()
        self.props['250'].detachNode()
        self.props.clear()

        self.slowPropTrack.clearToInitial()
        del self.slowPropTrack

        self.fastPropTrack.clearToInitial()
        del self.fastPropTrack

        del self.propSound
        
        self.deathInterval.clearToInitial()
        del self.deathInterval
        
        self.refuelInterval.clearToInitial()
        del self.refuelInterval
        
        self.guiMgr.destroy()
        self.guiMgr = None
    
    def setCheckpointPlatform(self, platform):
        self.checkpointPlatform = platform
    
    def resetToon(self):
#        print "Reset toon"
#        print "------------------------"
#        self.checkpointPlatform.ls()
        self.toon.setPos(render, self.checkpointPlatform.find("**/start_p1").getPos(render))
        self.toon.setHpr(render, 0, 0, 0)
        self.toon.setScale(1.0)
#        self.toon.loop('jump-idle')
        self.toon.collisionsOn()
#        self.toon.stopBobSwimTask()
#        self.toon.getGeomNode().setZ(1.0)
        self.resetFuel()

    def resetFuel(self):
        self.fuel = CogdoFlyingGameGlobals.FlyingGame.FUEL_START_AMT

    def isFuelLeft(self):
        return self.fuel > 0.0

    def __updateToonMovement(self):
        # move the local toon
        dt = globalClock.getDt()
        leftPressed = self.inputMgr.arrowKeys.leftPressed()
        rightPressed = self.inputMgr.arrowKeys.rightPressed()
        upPressed = self.inputMgr.arrowKeys.upPressed()
        downPressed = self.inputMgr.arrowKeys.downPressed()
        jumpPressed = self.inputMgr.arrowKeys.jumpPressed()

#        print leftPressed,rightPressed,upPressed,downPressed,jumpPressed
        self.instantaneousVelocity = (self.toon.getPos() - self.oldPos)/dt
        self.oldPos = self.toon.getPos()
        toonPos = self.toon.getPos()

        self.lastVelocity = Vec3(self.velocity)

        # Adds boost to velocity values and calculates toon pos changes
        if leftPressed:
            self.velocity[0] -= CogdoFlyingGameGlobals.FlyingGame.TOON_ACCELERATION["turning"]*dt
        if rightPressed:
            self.velocity[0] += CogdoFlyingGameGlobals.FlyingGame.TOON_ACCELERATION["turning"]*dt
        if upPressed:
            self.velocity[1] += CogdoFlyingGameGlobals.FlyingGame.TOON_ACCELERATION["forward"]*dt
        if downPressed:
            self.velocity[1] -= CogdoFlyingGameGlobals.FlyingGame.TOON_ACCELERATION["backward"]*dt


#        print jumpPressed
        if jumpPressed and self.isFuelLeft():
            self.velocity[2] += CogdoFlyingGameGlobals.FlyingGame.TOON_ACCELERATION["vertical"]*dt
            if self.state == "FreeFly" and self.isInTransition() == False:
                #print "Going to flying up"
                self.request("FlyingUp")
        else:
            if self.state == "FlyingUp" and self.isInTransition() == False:
                #print "Going to free fly"
                self.request("FreeFly")

        toonPos += self.velocity*dt
        
        # TODO:flying: death probably needs to happen on the server...
        if (CogdoFlyingGameGlobals.FlyingGame.DISABLE_DEATH) or \
           (base.config.GetBool('cogdo-flying-game-disable-death', 0)):
            pass
        else:
            # Tests to see whether the toon has dropped low enough to die
            if toonPos[2] < 0.0 and self.state in ["FreeFly","FlyingUp"]:
                self.request("Death")

        toonPos[2] = clamp(toonPos[2], self.game.downLimit, self.game.upLimit)
        toonPos[0] = clamp(toonPos[0], self.game.leftLimit, self.game.rightLimit)

        # Sets toon position based on velocity
        self.toon.setPos(toonPos)

        #print "Before degrades:",self.velocity

        # Degrades left/right velocity values back to normal
        minVal = -CogdoFlyingGameGlobals.FlyingGame.TOON_VEL_MAX["turning"]
        maxVal = CogdoFlyingGameGlobals.FlyingGame.TOON_VEL_MAX["turning"]
        if (not leftPressed and not rightPressed) or (self.velocity[0] > maxVal or self.velocity[0] < minVal):
            if self.velocity[0] > 0.0:
                self.velocity[0] -= CogdoFlyingGameGlobals.FlyingGame.TOON_DECELERATION["turning"] * dt
                self.velocity[0] = clamp(self.velocity[0], 0.0, maxVal)
            elif self.velocity[0] < 0.0:
                self.velocity[0] += CogdoFlyingGameGlobals.FlyingGame.TOON_DECELERATION["turning"] * dt
                self.velocity[0] = clamp(self.velocity[0], minVal, 0.0)

        # Degrades forward/backward velocity values back to normal
        minVal = -CogdoFlyingGameGlobals.FlyingGame.TOON_VEL_MAX["backward"]
        maxVal = CogdoFlyingGameGlobals.FlyingGame.TOON_VEL_MAX["forward"]
        if (not upPressed and not downPressed) or (self.velocity[1] > maxVal or self.velocity[1] < minVal):
            if self.velocity[1] > 0.0:
                self.velocity[1] -= CogdoFlyingGameGlobals.FlyingGame.TOON_DECELERATION["forward"] * dt
                self.velocity[1] = clamp(self.velocity[1], 0.0, maxVal)
            elif self.velocity[1] < 0.0:
                self.velocity[1] += CogdoFlyingGameGlobals.FlyingGame.TOON_DECELERATION["backward"] * dt
                self.velocity[1] = clamp(self.velocity[1], minVal, 0.0)

        # Degrades boost/fall velocity values back to normal
        minVal = -CogdoFlyingGameGlobals.FlyingGame.TOON_VEL_MAX["vertical"]
        maxVal = CogdoFlyingGameGlobals.FlyingGame.TOON_VEL_MAX["vertical"]
        if self.velocity[2] > minVal:
            if not self.inputMgr.arrowKeys.jumpPressed():
                self.velocity[2] -= CogdoFlyingGameGlobals.FlyingGame.TOON_DECELERATION["vertical"] * dt

            self.velocity[2] = clamp(self.velocity[2], minVal, maxVal)

        #print self.lastVelocity, self.velocity
#        if self.lastVelocity != self.velocity:
#            print "Velocity:",self.velocity

    def __updateFuel(self):
        dt = globalClock.getDt()
        
        if CogdoFlyingGameGlobals.FlyingGame.INFINITE_FUEL:
            self.fuel = CogdoFlyingGameGlobals.FlyingGame.FUEL_START_AMT
        else:
            if self.fuel > 0.0:
                self.fuel -= CogdoFlyingGameGlobals.FlyingGame.FUEL_BURN_RATE * dt
            elif self.fuel < 0.0:
                self.fuel = 0.0
            

    def update(self):
        if self.state not in ["Inactive","Refuel","WaitingForWin","Win"]:
            self.__updateToonMovement()
            self.__updateFuel()
            self.cameraMgr.update()
            self.guiMgr.update()

    def enterInactive(self):
        CogdoFlyingPlayer.enterInactive(self)
        self.inputMgr.disable()

    def exitInactive(self):
        CogdoFlyingPlayer.exitInactive(self)
        self.inputMgr.enable()

    def enterRefuel(self):
        CogdoFlyingPlayer.enterInactive(self)
        self.inputMgr.disable()
        self.refuelInterval.start()

    def exitRefuel(self):
        CogdoFlyingPlayer.exitInactive(self)
        self.inputMgr.enable()

    def enterFreeFly(self):
        CogdoFlyingPlayer.enterFreeFly(self)
        self.slowPropTrack.loop()
        base.playSfx(self.propSound, node = self.toon, looping = 1)
        self.propSound.setPlayRate(0.9)

    def exitFreeFly(self):
        CogdoFlyingPlayer.exitFreeFly(self)
        self.slowPropTrack.clearToInitial()
        self.propSound.stop()

    def enterFlyingUp(self):
        CogdoFlyingPlayer.enterFlyingUp(self)
        self.fastPropTrack.loop()
        base.playSfx(self.propSound, node = self.toon, looping = 1)
        self.propSound.setPlayRate(1.1)

    def exitFlyingUp(self):
        CogdoFlyingPlayer.exitFlyingUp(self)
        self.fastPropTrack.clearToInitial()
        self.propSound.stop()

    def enterDeath(self):
        CogdoFlyingPlayer.enterDeath(self)
        self.inputMgr.disable()
        self.deathInterval.start()

    def exitDeath(self):
        CogdoFlyingPlayer.exitDeath(self)
        self.inputMgr.enable()
        
    def enterWaitingForWin(self):
        CogdoFlyingPlayer.enterDeath(self)
        self.inputMgr.disable()
        self.guiMgr.messageLabel.unstash()
        self.waitingForWinInterval.loop()

    def exitWaitingForWin(self):
        CogdoFlyingPlayer.exitDeath(self)
        self.waitingForWinInterval.clearToInitial()
        self.guiMgr.messageLabel.stash()
        self.inputMgr.enable()
        
    def enterWin(self):
        CogdoFlyingPlayer.enterDeath(self)
        self.inputMgr.disable()
        self.winInterval.start()

    def exitWin(self):
        CogdoFlyingPlayer.exitDeath(self)
        self.inputMgr.enable()


class CogdoFlyingInputManager:
    def __init__(self):
        self.arrowKeys = ArrowKeys.ArrowKeys()
        self.arrowKeys.disable()
        
    def enable(self):
        #print "CogdoFlyingInputManager.enable()"
        self.arrowKeys.setPressHandlers([
            self.__upArrowPressed,
            self.__downArrowPressed,
            self.__leftArrowPressed,
            self.__rightArrowPressed,
            self.__controlPressed])
        self.arrowKeys.enable()

    def disable(self):
        self.arrowKeys.clearPressHandlers()
        self.arrowKeys.disable()

    def destroy(self):
        print "Destroying CogdoFlyingInputManager"
        self.disable()
        self.arrowKeys.destroy()
        self.arrowKeys = None
        
        self.refuelLerp = None

    def __upArrowPressed(self):
        """Handle up arrow being pressed."""
        pass
        #print "__upArrowPressed"

    def __downArrowPressed(self):
        """Handle down arrow being pressed."""
        pass
#        print "__downArrowPressed"

    def __leftArrowPressed(self):
        """Handle left arrow being pressed."""
        pass
#        print "__leftArrowPressed"

    def __rightArrowPressed(self):
        """Handle right arrow being pressed."""
        pass
#        print "__rightArrowPressed"

    def __controlPressed(self):
        """Handle control key being pressed."""
        pass
#        print "__controlPressed"

import math
from toontown.parties.PartyCogUtils import CameraManager

inverse_e = 1.0/math.e

class FlyingCamera(CameraManager):
    def __init__(self, cameraNP):
        CameraManager.__init__(self,cameraNP)
        self.vecRate = Vec3(self.rate, self.rate, self.rate)
        
    def rateInterpolate(self, currentPos, targetPos):
        dt = globalClock.getDt()
        vec = currentPos - targetPos
        return Vec3(targetPos[0] + vec[0]*(inverse_e**(dt*self.vecRate[0])),
                    targetPos[1] + vec[1]*(inverse_e**(dt*self.vecRate[1])),
                    targetPos[2] + vec[2]*(inverse_e**(dt*self.vecRate[2]))
                    )

class CogdoFlyingCameraManager:
    def __init__(self, player, cam, root):
        self.player = player
        self.toon = player.toon
        self.camera = cam
        self.root = root

        self.camOffset = VBase3(0, -12, 5)
        self.cameraManager = FlyingCamera(self.camera)
        self.cameraManager.vecRate = Vec3(3.0, 2.0, 1.8)
        self.cameraManager.otherNP = self.root

    def enable(self):
        self.camera.reparentTo(self.cameraManager.otherNP)
        self.cameraManager.setPos(self.toon.getPos() + self.camOffset)
        self.cameraManager.setLookAtPos(self.toon.getPos())
        self.cameraManager.setEnabled(True)

    def setCameraOffset(self, offset):
        self.camera.setPos(offset)
        self.camera.lookAt(self.toon)

    def disable(self):
        self.camera.wrtReparentTo(render)
        self.cameraManager.setEnabled(False)


    def update(self):
        toonPos = self.toon.getPos()
        newOffset = Vec3(self.player.instantaneousVelocity.getX()*0.1,self.player.instantaneousVelocity.getY()*2.0,self.player.velocity.getZ())
        targetPos = toonPos + self.camOffset + Vec3(0,0,-newOffset.getZ()*0.3)
        targetLookAt = toonPos + Vec3(0,35,0) + newOffset
        
        if self.player.instantaneousVelocity.getY() < 0.0 or (self.player.instantaneousVelocity.getY() <= 0.0 and self.player.instantaneousVelocity.getZ() < 0.0):
            targetPos = targetPos + Vec3(0, +2.0, abs(self.player.instantaneousVelocity.getZ()*0.4))
            targetLookAt = targetLookAt + Vec3(0,0,-abs(self.player.instantaneousVelocity.getZ()*0.2))
            targetLookAt[1] = toonPos[1]

        p = 0.90
        targetPos[0] = clamp(targetPos[0], self.player.game.leftLimit*p, self.player.game.rightLimit*p)
        targetLookAt[0] = clamp(targetLookAt[0], self.player.game.leftLimit*p, self.player.game.rightLimit*p)

        #targetPos[2] = clamp(targetPos[2], self.player.game.downLimit*p, self.player.game.upLimit*p)
        p = 0.95
        targetLookAt[2] = clamp(targetLookAt[2], self.player.game.downLimit*p, self.player.game.upLimit*p)

        self.cameraManager.setTargetPos(targetPos)
        self.cameraManager.setTargetLookAtPos(targetLookAt)


from pandac.PandaModules import CardMaker, TextNode
from direct.gui.DirectGui import DirectLabel
from toontown.toonbase import ToontownGlobals

class CogdoFlyingGuiManager:
    def __init__(self, player):
        
        self.player = player
        
        self.root = NodePath("CogdoFlyingGui")
        self.root.reparentTo(aspect2d)
        
        self.fuelMeter = NodePath("scrubMeter")
        self.fuelMeter.reparentTo(self.root)
        self.fuelMeter.setPos(1.1, 0.0, -0.7)
        self.fuelMeter.setSz(2.0)
        
        cm = CardMaker('card')
        cm.setFrame( -0.07, 0.07, 0.0, 0.75 )
        self.fuelMeterBar = self.fuelMeter.attachNewNode(cm.generate())
        self.fuelMeterBar.setColor(0.95, 0.95, 0.0, 1.0)
        
        
        self.fuelLabel = DirectLabel(
            parent = self.root,
            relief = None,
            pos = (1.1,0,-0.8),
            scale = 0.075,
            text = "Fuel",
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = ToontownGlobals.getInterfaceFont(),
        )
        
        self.messageLabel = DirectLabel(
            parent = self.root,
            relief = None,
            pos = (0.0,0.0,-0.9),
            scale = 0.1,
            text = "                ",
            text_align = TextNode.ACenter,
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = ToontownGlobals.getInterfaceFont(),
            textMayChange = 1,
        )
        self.messageLabel.stash()
        
        self.winLabel = DirectLabel(
            parent = self.root,
            relief = None,
            pos = (0.0,0.0,0.0),
            scale = 0.25,
            text = "You win!",
            text_align = TextNode.ACenter,
            text_fg = (0.95, 0.95, 0, 1),
            text_shadow = (0, 0, 0, 1),
            text_font = ToontownGlobals.getInterfaceFont(),
        )
        self.winLabel.stash()
        
        self.refuelLerp = LerpFunctionInterval(self.fuelMeterBar.setSz, fromData=0.0, toData=1.0, duration=2.0)
        
    def setRefuelLerpFromData(self):
        startScale = self.fuelMeterBar.getSz()
        self.refuelLerp.fromData = startScale
    
    def setMessageLabelText(self,text):
        self.messageLabel["text"] = text
        self.messageLabel.setText()
    
    def update(self):
        self.fuelMeterBar.setSz(self.player.fuel)

    def destroy(self):
#        print "Destroying GUI"
        self.fuelMeterBar.detachNode()
        self.fuelMeterBar = None
        
        self.fuelLabel.detachNode()
        self.fuelLabel = None
        
        self.fuelMeter.detachNode()
        self.fuelMeter = None
        
        self.winLabel.detachNode()
        self.winLabel = None
        
        self.root.detachNode()
        self.root = None
        
        self.player = None


