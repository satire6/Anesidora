from otp.level.BasicEntities import DistributedNodePathEntity
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from toontown.toonbase.ToontownGlobals import *
import random
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
import DistributedBarrelBase
from otp.level.BasicEntities import DistributedNodePathEntity
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownTimer
from direct.task import Task
from direct.gui.DirectGui import DGG, DirectFrame, DirectLabel

class DistributedMaze(DistributedNodePathEntity):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMaze')
    
    ScheduleTaskName = 'mazeScheduler'

    RemoveBlocksDict = {
        2: ( ('HedgeBlock_0_1'),),
        4: ( ('HedgeBlock_0_1','HedgeBlock_1_3','HedgeBlock_2_3'),
             ('HedgeBlock_0_2','HedgeBlock_2_3','HedgeBlock_1_3'),
             ('HedgeBlock_0_1','HedgeBlock_0_2','HedgeBlock_1_3','HedgeBlock_2_3'),
             )
        }
        
    def __init__(self, cr):
        """Construct the maze."""
        DistributedNodePathEntity.__init__(self, cr)
        self.numSections = 0
        self.GameDuration = 35.0 + (self.numSections * 15.0)
        self.timer = None
        self.frame2D = None
        self.gameLabel = None
        self.gameStarted = 0
        self.finished = 0
        self.timedOut = 0
        self.toonFinishedText = TTLocalizer.toonFinishedHedgeMaze
        self.toonEnteredText = TTLocalizer.enterHedgeMaze

    def announceGenerate(self):
        """Handle all required fields being set."""
        DistributedNodePathEntity.announceGenerate(self)
        self.addHints(self.roomHold)
        self.loadGui()
        
    def disable(self):
        """Remove us from the cache."""
        assert self.notify.debugStateCall(self)
        DistributedNodePathEntity.disable(self)
        self.unloadGui()
        self.cleanupTimer()
        self.ignoreAll()

    def delete(self):
        """Totally delete ourself."""
        assert self.notify.debugStateCall(self)
        self.cleanupTimer()
        DistributedNodePathEntity.delete(self)

    def setRoomDoId(self, roomDoId):
        """Handle the AI telling us the room doId this maze is in."""
        self.roomDoId = roomDoId
        room = self.cr.doId2do.get(roomDoId)
        if room:
            self.gotRoom([room])
        else:
            self.roomRequest = self.cr.relatedObjectMgr.requestObjects(
                [roomDoId], allCallback = self.gotRoom, timeout = 5)
        
    def gotRoom(self, rooms):
        """Handle getting the actual room object we are in."""
        self.roomRequest = None
        room = rooms[0]
        self.roomHold = room
        rotations = [0,0,90,90,180,180,270,270]
        self.getRng().shuffle(rotations)
        self.numSections = 0
        for i in xrange(0,4):
            maze = room.getGeom().find('**/Maze_Inside_%d' % i)
            if not maze.isEmpty():
                self.numSections += 1
                if rotations:
                    maze.setH(rotations.pop())
        self.GameDuration = 35.0 + (self.numSections * 15.0)
        self.removeHedgeBlocks(room)
        
        
    def addHints(self, room):
        self.focusPoint = self.attachNewNode("GolfGreenGameFrame")
        hintList = room.getGeom().findAllMatches('**/dead*')
        for hint in hintList:
            #print ("adding hint!!! foo!")
            self.actSphere = CollisionSphere(0,0,0,7.0)
            self.actSphereNode = CollisionNode("mazegame_hint-%s-%s" %
                                             (self.level.getLevelId(), self.entId))
            self.actSphereNode.addSolid(self.actSphere)
            self.actSphereNodePath = hint.attachNewNode(self.actSphereNode)
            self.actSphereNode.setCollideMask(WallBitmask)
            self.actSphere.setTangible(0)
    
            self.enterEvent = "enter" + self.actSphereNode.getName()
            self.accept(self.enterEvent, self.__handleToonEnterHint)
            
            self.exitEvent = "exit" + self.actSphereNode.getName()
            self.accept(self.exitEvent, self.__handleToonExitHint)
            
        enterance = room.getGeom().find('**/ENTRANCE')
        self.enterSphere = CollisionSphere(0,0,0,8.0)
        self.enterSphereNode = CollisionNode("mazegame_enter-%s-%s" %
                                         (self.level.getLevelId(), self.entId))
        self.enterSphereNode.addSolid(self.enterSphere)
        self.enterSphereNodePath = enterance.attachNewNode(self.enterSphereNode)
        self.enterSphereNode.setCollideMask(WallBitmask)
        self.enterSphere.setTangible(0)

        self.enteranceEvent = "enter" + self.enterSphereNode.getName()
        self.accept(self.enteranceEvent, self.__handleToonEnterance)
        
        finish = room.getGeom().find('**/finish')
        self.finishSphere = CollisionSphere(0,0,0,15.0)
        self.finishSphereNode = CollisionNode("mazegame_finish-%s-%s" %
                                         (self.level.getLevelId(), self.entId))
        self.finishSphereNode.addSolid(self.finishSphere)
        self.finishSphereNodePath = finish.attachNewNode(self.finishSphereNode)
        self.finishSphereNode.setCollideMask(WallBitmask)
        self.finishSphere.setTangible(0)

        self.finishEvent = "enter" + self.finishSphereNode.getName()
        self.accept(self.finishEvent, self.__handleToonFinish)
        

        
    def __handleToonEnterance(self, collEntry):
        #print "toon enterance"
        #self.setGameStart(0)
        if not self.gameStarted:
            self.notify.debug('sending clientTriggered for %d' % self.doId)
            self.sendUpdate('setClientTriggered',[])
            self.level.countryClub.showInfoText(self.toonEnteredText)
        
    def __handleToonFinish(self, collEntry):
        #print "toon finish"
        self.sendUpdate("setFinishedMaze", [])
        self.finished = 1
        
    def __handleToonEnterHint(self, collEntry):
        #print "hint enter"
        camHeight = base.localAvatar.getClampedAvatarHeight()
        heightScaleFactor = (camHeight * 0.3333333333)
        defLookAt = Point3(0.0, 1.5, camHeight)
                     
        cameraPoint = Point3(0.0, (-22.0 * heightScaleFactor), (camHeight + 54.0))

        #base.localAvatar.setCameraSettings(cameraSetting[0])
        
        base.localAvatar.stopUpdateSmartCamera()
        base.localAvatar.startUpdateSmartCamera(push = 0)
        base.localAvatar.setIdealCameraPos(cameraPoint)
        
    def __handleToonExitHint(self, collEntry):
        #print "hint exit"
        base.localAvatar.stopUpdateSmartCamera()
        base.localAvatar.startUpdateSmartCamera()
        base.localAvatar.setCameraPositionByIndex(base.localAvatar.cameraIndex)
        self.cameraHold = None

    def getRng(self):
        """Return a deterministic random number generator."""
        return random.Random(self.entId * self.doId)

    def removeHedgeBlocks(self, room):
        """Remove the hedge blocks so the player can exit the maze."""
        if self.numSections in self.RemoveBlocksDict:
            blocksToRemove = self.getRng().choice( self.RemoveBlocksDict[self.numSections])
            for blockName in blocksToRemove:
                block = room.getGeom().find('**/%s' % blockName)
                if not block.isEmpty():
                    block.removeNode()
                    
    def setGameStart(self, timestamp):
        """
        This method gets called from the AI when all avatars are ready
        Ready usually means they have read the rules
        Inheritors should call this plus the code to start the game
        """
        self.notify.debug("%d setGameStart: Starting game" % self.doId)
        self.gameStartTime = \
                    globalClockDelta.networkToLocalTime(timestamp)
        self.gameStarted = True
        curGameTime = self.getCurrentGameTime()
        timeLeft =  self.GameDuration - curGameTime
        self.cleanupTimer()
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posBelowTopRightCorner()
        self.timer.setTime(timeLeft) 
        self.timer.countdown(timeLeft, self.timerExpired)
        
        self.startScheduleTask()
        self.frame2D.show()
        
    def setGameOver(self):
        #print "game over"
        
        #import pdb; pdb.set_trace()
        
        self.timedOut = 1
        if not self.finished:
            self.sendUpdate("damageMe", [])
            roomNum = self.level.roomNum
            club = self.level.countryClub
            
            self.gameOverTrack = Sequence()
            self.gameOverTrack.append(localAvatar.getTeleportOutTrack())
            self.gameOverTrack.append(Func(localAvatar.setPos, self.finishSphereNodePath.getPos(render)))
            self.gameOverTrack.append(Func(localAvatar.play, 'jump'))
            self.gameOverTrack.append(Func(self.level.countryClub.camEnterRoom, roomNum))
            self.gameOverTrack.start()
            
 
            
            
        self.timerExpired()
        
                    
    # time-related utility functions
    def local2GameTime(self, timestamp):
        """
        given a local-time timestamp, returns the corresponding
        timestamp relative to the start of the game
        """
        return timestamp - self.gameStartTime

    def game2LocalTime(self, timestamp):
        """
        given a game-time timestamp, returns the corresponding
        local timestamp
        """
        return timestamp + self.gameStartTime

    def getCurrentGameTime(self):
        return self.local2GameTime(globalClock.getFrameTime())

    def startScheduleTask(self):
        taskMgr.add(self.scheduleTask, self.ScheduleTaskName)

    def stopScheduleTask(self):
        taskMgr.remove(self.ScheduleTaskName)

    def scheduleTask(self, task):
        curTime = self.getCurrentGameTime()
                    
    def cleanupTimer(self):
        """Stop and remove the molefield timer."""        
        if self.timer:
            self.timer.stop()
            self.timer.destroy()
            self.timer = None      

    def timerExpired(self):
        """Show something when the timer expires."""
        assert self.notify.debugStateCall(self)
        self.cleanupTimer()
        self.unloadGui()
        
        
    def loadGui(self):
        """Create the GUI."""
        self.frame2D =  DirectFrame(scale = 1.0,
                                    pos = (0.0, 0, 0.90),
                                    relief = DGG.FLAT,
                                    parent = aspect2d,
                                    frameSize = (-0.3, 0.3, -0.05, 0.05),
                                    frameColor = (0.737, 0.573, 0.345, 0.300))
        self.frame2D.hide()
        self.gameLabel = DirectLabel(
            parent = self.frame2D,
            relief = None,
            #image = gui2.find("**/QuitBtn_UP"),
            pos = (0, 0, 0),
            scale = 1.0,
            text = TTLocalizer.mazeLabel,
            text_font = ToontownGlobals.getSignFont(),
            text0_fg = (1, 1, 1, 1),
            text_scale = 0.075,
            text_pos = (0, -0.02),         
            )

    def unloadGui(self):
        """Cleanup the GUI."""
        if self.frame2D:
            self.frame2D.destroy()
        self.frame2D = None
        if self.gameLabel:
            self.gameLabel.destroy()
        self.gameLabel = None
            
    def toonFinished(self, avId, place, lastToon):
        #print("toonFinished received")
        toon = base.cr.doId2do.get(avId)
        if toon and not self.timedOut:
            self.level.countryClub.showInfoText(self.toonFinishedText % (toon.getName(), TTLocalizer.hedgeMazePlaces[place]))
        if lastToon:
            self.setGameOver()
            pass
            
