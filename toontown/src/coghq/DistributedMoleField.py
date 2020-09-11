from pandac.PandaModules import *
from otp.level.BasicEntities import DistributedNodePathEntity
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import MoleHill
from toontown.coghq import MoleFieldBase
from direct.distributed.ClockDelta import globalClockDelta
from toontown.toonbase import ToontownTimer
from direct.gui.DirectGui import DGG, DirectFrame, DirectLabel
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.task import Task
import random
from toontown.minigame import Trajectory
from direct.interval.IntervalGlobal import *
from toontown.battle import MovieUtil

class DistributedMoleField(DistributedNodePathEntity, MoleFieldBase.MoleFieldBase):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMoleField')
 
    ScheduleTaskName = 'moleFieldScheduler'
        
    def __init__(self, cr):
        """Construct the mole field."""
        DistributedNodePathEntity.__init__(self, cr)
        self.gameStarted = False
        self.moleHills = []
        self.numMolesWhacked = 0
        self.timer = None
        self.frame2D = None
        self.isToonInRange = 0
        self.detectCount = 0
        self.cameraHold = None
        self.activeField = 1
        self.dimensionX = 0.0
        self.dimensionY = 0.0
        self.gameText = TTLocalizer.MolesInstruction
        self.winText = TTLocalizer.MolesFinished
        self.pityWinText = TTLocalizer.MolesPityWin
        self.restartedText = TTLocalizer.MolesRestarted
        self.toonHitTracks = {}
        self.hasRestarted = 0
        self.hasEntered = 0
        self.MolesWhackedTarget = 1000
        self.GameDuration = 1000
        
    def disable(self):
        """Disable the mole field."""
        self.cleanupTimer()
        for ival in self.toonHitTracks.values():
            ival.finish()
        self.toonHitTracks = {}
        DistributedNodePathEntity.disable(self)
        taskMgr.remove(self.detectName)
        self.ignoreAll()

    def delete(self):
        """Delete the mole field."""
        self.soundBomb = None
        self.soundBomb2 = None
        self.soundCog = None
        DistributedNodePathEntity.delete(self)
        self.stopScheduleTask()
        for mole in self.moleHills:
            mole.destroy()
        self.moleHills = []
        self.cleanupTimer()
        self.unloadGui()
    
    def announceGenerate(self):
        """Load fields dependent on required fields."""
        DistributedNodePathEntity.announceGenerate(self)
        self.loadModel()
        self.loadGui()
        self.detectName = (("moleField %s") % (self.doId))
        taskMgr.doMethodLater(0.1, self.__detect, self.detectName)
        self.calcDimensions()
        self.notify.debug('announceGenerate doId=%d entId=%d' % (self.doId, self.entId))
        
    def setNumSquaresX(self, num):
        self.numSquaresX = num
        self.calcDimensions()
        
    def setNumSquaresY(self, num):
        self.numSquaresY = num
        self.calcDimensions()
        
    def setSpacingX(self, num):
        self.spacingX = num
        self.calcDimensions()
        
    def setSpacingY(self, num):
        self.spacingY = num
        self.calcDimensions()
        
    def calcDimensions(self):
        self.dimensionX = self.numSquaresX * self.spacingX
        self.dimensionY = self.numSquaresY * self.spacingY
        self.centerCenterNode()
        
        

    def loadModel(self):
        """Create the field and load the assets."""
        moleIndex = 0
        self.moleHills = []
        for indexY in xrange(self.numSquaresY):
            for indexX in xrange(self.numSquaresX):
                xPos = indexX * self.spacingX
                yPos = indexY * self.spacingY
                newMoleHill = MoleHill.MoleHill(xPos, yPos, 0, self, moleIndex)
                newMoleHill.reparentTo(self)
                self.moleHills.append(newMoleHill)
                moleIndex += 1
        self.numMoles = len(self.moleHills)
        self.centerNode = self.attachNewNode('center')
        self.centerCenterNode()
        self.soundBomb = base.loadSfx("phase_12/audio/sfx/Mole_Surprise.mp3")
        self.soundBomb2 = base.loadSfx("phase_3.5/audio/dial/AV_pig_howl.mp3")
        self.soundCog = base.loadSfx("phase_12/audio/sfx/Mole_Stomp.mp3")
        self.soundUp = base.loadSfx("phase_4/audio/sfx/MG_Tag_C.mp3")
        self.soundDown = base.loadSfx("phase_4/audio/sfx/MG_cannon_whizz.mp3")
        upInterval = SoundInterval(self.soundUp,loop = 0)
        downInterval = SoundInterval(self.soundDown,loop = 0)
        self.soundIUpDown = Sequence(upInterval, downInterval)


    def centerCenterNode(self):
        self.centerNode.setPos(self.dimensionX * 0.5, self.dimensionY * 0.5, 0.0)

    def loadGui(self):
        """Create the GUI."""
        self.frame2D =  DirectFrame(scale = 1.0,
                                    pos = (0.0, 0, 0.90),
                                    relief = DGG.FLAT,
                                    parent = aspect2d,
                                    frameSize = (-0.3, 0.3, -0.05, 0.05),
                                    frameColor = (0.737, 0.573, 0.345, 0.300))
        self.scoreLabel = DirectLabel(
            parent = self.frame2D,
            relief = None,
            #image = gui2.find("**/QuitBtn_UP"),
            pos = (0, 0, 0),
            scale = 1.0,
            text = "",
            text_font = ToontownGlobals.getSignFont(),
            text0_fg = (1, 1, 1, 1),
            text_scale = 0.075,
            text_pos = (0, -0.02),         
            )
        self.updateGuiScore()
        self.frame2D.hide()

    def unloadGui(self):
        """Cleanup the GUI."""
        self.frame2D.destroy()
        self.frame2D = None

    def setGameStart(self, timestamp, molesWhackTarget, totalTime):
        """
        This method gets called from the AI when all avatars are ready
        Ready usually means they have read the rules
        Inheritors should call this plus the code to start the game
        """
        self.GameDuration = totalTime
        self.MolesWhackedTarget = molesWhackTarget
        self.activeField = 1
        self.isToonInRange = 0
        self.scheduleMoles()
        self.notify.debug("%d setGameStart: Starting game" % self.doId)
        self.gameStartTime = \
                    globalClockDelta.networkToLocalTime(timestamp)
        self.gameStarted = True
        for hill in self.moleHills:
            hill.setGameStartTime(self.gameStartTime)
        curGameTime = self.getCurrentGameTime()
        timeLeft =  self.GameDuration - curGameTime
        self.cleanupTimer()
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.posBelowTopRightCorner()
        self.timer.setTime(timeLeft) 
        self.timer.countdown(timeLeft, self.timerExpired)
        
        self.startScheduleTask()
        self.frame2D.show()
        if self.hasRestarted:
            self.level.countryClub.showInfoText(self.restartedText)
            self.sendUpdate("damageMe", [])
        else:
            self.hasRestarted = 1
            
        self.updateGuiScore()
        

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
    
        # start all the drops thatpopups should already be happening
        # the drop schedule is a time-ordered list of
        # (time, moleIndex, curMoveUpTime, curStayUpTime, curMoveDownTime) tuples    
        while self.schedule and self.schedule[0][0] <= curTime and self.activeField:
            popupInfo = self.schedule[0]
            # pop this one off the front
            self.schedule = self.schedule[1:]
            startTime, moleIndex, curMoveUpTime, curStayUpTime, curMoveDownTime, moleType = popupInfo
            hill = self.moleHills[moleIndex]
            hill.doMolePop(startTime, curMoveUpTime, curStayUpTime, curMoveDownTime, moleType)
            #self.notify.debug('popping mole=%d' % moleIndex)

        if self.schedule:
            return task.cont
        else:
            return task.done
        
    def handleEnterHill(self,  colEntry):
        """Handle the toon hitting one of the mole hills."""
        if not self.gameStarted:
            self.notify.debug('sending clientTriggered for %d' % self.doId)
            self.sendUpdate('setClientTriggered',[])

    def handleEnterMole(self,  colEntry):
        """Handle the toon hitting one of the moles."""
        if not self.gameStarted:
            self.notify.debug('sending clientTriggered for %d' % self.doId)
            self.sendUpdate('setClientTriggered',[])
        surfaceNormal = colEntry.getSurfaceNormal(render)
        self.notify.debug('surfaceNormal=%s' % surfaceNormal)
        into = colEntry.getIntoNodePath()
        moleIndex = int(into.getName().split('-')[-1])
        self.notify.debug('hit mole %d' % moleIndex)
        moleHill = self.moleHills[moleIndex]
        moleHill.stashMoleCollision()
        popupNum = moleHill.getPopupNum()
        if moleHill.hillType == MoleFieldBase.HILL_MOLE:
            #print "blamO!"
            #self.__showToonHitByBomb(localAvatar.doId)
            timestamp = globalClockDelta.getFrameNetworkTime()
            moleHill.setHillType(MoleFieldBase.HILL_WHACKED)
            self.sendUpdate('whackedBomb', [moleIndex, popupNum, timestamp])
            self.__showToonHitByBomb(localAvatar.doId, moleIndex, timestamp)
        elif moleHill.hillType == MoleFieldBase.HILL_BOMB:
            #print ("type %s" % (moleHill.hillType))
            moleHill.setHillType(MoleFieldBase.HILL_COGWHACKED)
            self.soundCog.play()
            self.sendUpdate('whackedMole', [moleIndex, popupNum])

    def updateMole(self, moleIndex, status):
        """Handle the AI telling us a mole has been whacked."""
        assert self.notify.debugStateCall(self)
        if status == self.WHACKED:
            moleHill = self.moleHills[moleIndex]
            if not moleHill.hillType == MoleFieldBase.HILL_COGWHACKED:
                moleHill.setHillType(MoleFieldBase.HILL_COGWHACKED)
                self.soundCog.play()
            #self.soundCog.play()
            moleHill.doMoleDown()

    def updateGuiScore(self):
        """Show the score on the gui."""
        molesLeft = self.MolesWhackedTarget - self.numMolesWhacked
        if self.frame2D and hasattr(self,'scoreLabel') and (molesLeft >=0): 
            newText = TTLocalizer.MolesLeft % molesLeft
            self.scoreLabel['text'] = newText
            
    def setScore(self, score):
        """Handle the AI telling us the new score."""
        self.notify.debug('score=%d' % score)
        self.numMolesWhacked = score
        self.updateGuiScore()
        molesLeft = self.MolesWhackedTarget - self.numMolesWhacked
        if molesLeft == 0:
            self.gameWon()

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
        self.cleanDetect()
        

    def gameWon(self):
        """Handle the toons winning the game."""
        for hill in self.moleHills:
            hill.forceMoleDown()
        self.cleanupTimer()
        self.frame2D.hide()
        self.level.countryClub.showInfoText(self.winText)
        self.cleanDetect()

    def setPityWin(self):
        """He's lost 4 times in a row, open the doors for him."""
        for hill in self.moleHills:
            hill.forceMoleDown()
        self.cleanupTimer()
        self.frame2D.hide()
        self.level.countryClub.showInfoText(self.pityWinText)
        self.cleanDetect()
        
    def cleanDetect(self):
        self.activeField = 0
        self.doToonOutOfRange()        
        
    def __detect(self, task):
        #print "detect beat"
        
        distance = self.centerNode.getDistance(localAvatar)
        greaterDim = self.dimensionX
        if self.dimensionY > self.dimensionX:
            greaterDim = self.gridScaleY
            
        self.detectCount += 1
        if self.detectCount > 5:   
            #print("Range:%s Dimension:%s" % (distance, greaterDim * 0.75))
            self.detectCount = 0
            
        if distance < (greaterDim * 0.75):
            if not self.isToonInRange:
                self.doToonInRange()
        else:
            if self.isToonInRange:
                self.doToonOutOfRange()

        taskMgr.doMethodLater(0.1, self.__detect, self.detectName)
        return Task.done
        
        
    def doToonInRange(self):
        #print("toon in Range")
        if not self.gameStarted:
            self.notify.debug('sending clientTriggered for %d' % self.doId)
            self.sendUpdate('setClientTriggered',[])
            
        self.isToonInRange = 1
        if self.activeField:
            #self.cameraHold = base.localAvatar.getIdealCameraPos()
            self.setUpCamera()
            
            if not self.hasEntered:
                self.level.countryClub.showInfoText(self.gameText)
                self.hasEntered = 1
 
            
    def setUpCamera(self):
        camHeight = base.localAvatar.getClampedAvatarHeight()
        heightScaleFactor = (camHeight * 0.3333333333)
        defLookAt = Point3(0.0, 1.5, camHeight)
                     
        cameraPoint = Point3(0.0, (-22.0 * heightScaleFactor), (camHeight + 12.0))

        #base.localAvatar.setCameraSettings(cameraSetting[0])
        base.localAvatar.setIdealCameraPos(cameraPoint)
        
    def doToonOutOfRange(self):
        #print("toon out of Range")
        self.isToonInRange = 0
        #base.localAvatar.setIdealCameraPos(self.cameraHold)
        base.localAvatar.setCameraPositionByIndex(base.localAvatar.cameraIndex)
        self.cameraHold = None
        
    def reportToonHitByBomb(self, avId, moleIndex,timestamp):
        if avId != localAvatar.doId:
            self.__showToonHitByBomb(avId, moleIndex,timestamp)
            moleHill = self.moleHills[moleIndex]
            if not moleHill.hillType == MoleFieldBase.HILL_WHACKED:
                moleHill.setHillType(MoleFieldBase.HILL_WHACKED)
                self.soundCog.play()
            #self.soundCog.play()
            moleHill.doMoleDown()
        
    def __showToonHitByBomb(self, avId, moleIndex, timestamp = 0):
        toon = base.cr.doId2do.get(avId)
        moleHill = self.moleHills[moleIndex]
        if toon == None:
            return
            
        #print("Toon info")
        #print("Pos %s" % (toon.getPos()))
        #print("Parent %s" % (toon.getParent()))
        rng = random.Random(timestamp)

        # make sure this toon's old track is done
        curPos = toon.getPos(render)
        oldTrack = self.toonHitTracks.get(avId)
        if oldTrack:
            if oldTrack.isPlaying():
                oldTrack.finish()
        # preserve the toon's current position, in case he gets hit
        # by two suits at a time
        toon.setPos(curPos)
        toon.setZ(self.getZ())

        # put the toon under a new node
        assert (toon.getParent() == render)
        parentNode = render.attachNewNode('mazeFlyToonParent-'+`avId`)
        parentNode.setPos(toon.getPos(render))
        toon.reparentTo(parentNode)
        toon.setPos(0,0,0)

        # shoot the toon up into the air
        startPos = parentNode.getPos()

        # make a copy of the toon's dropshadow
        dropShadow = toon.dropShadow.copyTo(parentNode)
        dropShadow.setScale(toon.dropShadow.getScale(render))
        
        trajectory = Trajectory.Trajectory(0,
                                           Point3(0,0,0),
                                           Point3(0,0,50),
                                           gravMult=1.)
        flyDur = trajectory.calcTimeOfImpactOnPlane(0.)
        assert(flyDur > 0)

        # choose a random landing point
  
        endTile = [rng.randint(0,self.numSquaresX-1),
                   rng.randint(0,self.numSquaresY-1)]


        endWorldCoords = (self.getX(render) + (endTile[0] * self.spacingX), self.getY(render) + (endTile[1] * self.spacingY))
        endPos = Point3(endWorldCoords[0], endWorldCoords[1], startPos[2])

        def flyFunc(t, trajectory, startPos=startPos, endPos=endPos,
                    dur=flyDur, moveNode=parentNode, flyNode=toon):
            u = (t/dur)
            moveNode.setX(startPos[0] + (u * (endPos[0]-startPos[0])))
            moveNode.setY(startPos[1] + (u * (endPos[1]-startPos[1])))
            # set the full position, since the toon might get banged
            # by telemetry
            if flyNode and not flyNode.isEmpty():
                # flyNode could be empty if we teleported out and another toon was flying
                flyNode.setPos(trajectory.getPos(t))

        def safeSetHpr(node, hpr):
            if node and not node.isEmpty():
                node.setHpr(hpr)

        flyTrack = Sequence(
            LerpFunctionInterval(flyFunc,
                                 fromData=0., toData=flyDur,
                                 duration=flyDur,
                                 extraArgs=[trajectory]),
            name=toon.uniqueName("hitBySuit-fly"))

        # if localtoon, move the camera to get a better view
        if avId != localAvatar.doId:
            cameraTrack = Sequence()
        else:
            # keep the camera parent node on the ground
            # with the toon parent node
            base.localAvatar.stopUpdateSmartCamera()
            self.camParentHold = camera.getParent()
            self.camParent = base.localAvatar.attachNewNode('iCamParent')
            self.camParent.setPos(self.camParentHold.getPos())
            self.camParent.setHpr(self.camParentHold.getHpr())
            camera.reparentTo(self.camParent)
            self.camParent.reparentTo(parentNode)
            startCamPos = camera.getPos()

            destCamPos = camera.getPos()
            # trajectory starts at Z==0, ends at Z==0
            zenith = trajectory.getPos(flyDur/2.)[2]
            # make the camera go up above the toon's zenith...
            destCamPos.setZ(zenith * 1.3)
            # and pull in fairly far towards the toon
            destCamPos.setY(destCamPos[1] * .3)

            # make sure the camera keeps looking at the toon
            def camTask(task, zenith=zenith,
                              flyNode=toon,
                              startCamPos=startCamPos,
                              camOffset=destCamPos-startCamPos):
                # move the camera proportional to the current height
                # of the toon wrt the height of its total trajectory
                u = flyNode.getZ() / zenith
                #camera.setPos(startCamPos + (camOffset * u))
                camera.lookAt(toon)
                return Task.cont

            camTaskName = "mazeToonFlyCam-"+`avId`
            taskMgr.add(camTask, camTaskName, priority=20)

            def cleanupCamTask(self=self, toon=toon,
                               camTaskName=camTaskName,
                               startCamPos=startCamPos):
                taskMgr.remove(camTaskName)
                self.camParent.reparentTo(toon)
                camera.setPos(startCamPos)
                camera.lookAt(toon)
                camera.reparentTo(self.camParentHold)
                base.localAvatar.startUpdateSmartCamera()
                self.setUpCamera()

            cameraTrack = Sequence(
                Wait(flyDur),
                Func(cleanupCamTask),
                name="hitBySuit-cameraLerp")

        # make the toon spin in H and P
        # it seems like we need to put the rotations on two different
        # nodes in order to avoid interactions between the rotations
        geomNode = toon.getGeomNode()
        
        # apply the H rotation around the geomNode, since it's OK
        # to spin the toon in H at a node at his feet
        startHpr = geomNode.getHpr()
        destHpr = Point3(startHpr)
        # make the toon rotate in h 1..7 times
        hRot = rng.randrange(1,8)
        if rng.choice([0,1]):
            hRot = -hRot
        destHpr.setX(destHpr[0]+(hRot*360))
        spinHTrack = Sequence(
            LerpHprInterval(geomNode, flyDur, destHpr, startHpr=startHpr),
            Func(safeSetHpr, geomNode, startHpr),
            name=toon.uniqueName("hitBySuit-spinH"))
        
        # put an extra node above the geomNode, so we can spin the
        # toon in P around his waist
        parent = geomNode.getParent()
        rotNode = parent.attachNewNode('rotNode')
        geomNode.reparentTo(rotNode)
        rotNode.setZ(toon.getHeight()/2.)
        oldGeomNodeZ = geomNode.getZ()
        geomNode.setZ(-toon.getHeight()/2.)

        # spin the toon in P around his waist
        startHpr = rotNode.getHpr()
        destHpr = Point3(startHpr)
        # make the toon rotate in P 1..2 times
        pRot = rng.randrange(1,3)
        if rng.choice([0,1]):
            pRot = -pRot
        destHpr.setY(destHpr[1]+(pRot*360))
        spinPTrack = Sequence(
            LerpHprInterval(rotNode, flyDur, destHpr, startHpr=startHpr),
            Func(safeSetHpr, rotNode, startHpr),
            name=toon.uniqueName("hitBySuit-spinP"))

        # play some sounds
        #i = self.avIdList.index(avId)
        soundTrack = Sequence()
        #    Func(base.playSfx, self.sndTable['hitBySuit'][i]),
        #    Wait(flyDur * (2./3.)),
        #    SoundInterval(self.sndTable['falling'][i],
        #                  duration=(flyDur*(1./3.))),
        #    name=toon.uniqueName("hitBySuit-soundTrack"))
            
        def preFunc(self=self, avId=avId, toon=toon, dropShadow=dropShadow):
            forwardSpeed = toon.forwardSpeed
            rotateSpeed = toon.rotateSpeed

            if avId == localAvatar.doId:
                # disable control of local toon
                #self.orthoWalk.stop()
                toon.stopSmooth()
                base.cr.playGame.getPlace().fsm.request('stopped')
            else:
                toon.stopSmooth()
            
            # preserve old bug/feature where toon would be running in the air
            # if toon was moving, make him continue to run
            if forwardSpeed or rotateSpeed:
                toon.setSpeed(forwardSpeed, rotateSpeed)

            # set toon's speed to zero to stop any walk animations
            # leave it, it's funny to see toon running in mid-air
            #toon.setSpeed(0,0)

            # hide the toon's dropshadow
            toon.dropShadow.hide()

        def postFunc(self=self, avId=avId, oldGeomNodeZ=oldGeomNodeZ,
                     dropShadow=dropShadow, parentNode=parentNode):
            if avId == localAvatar.doId:
                base.localAvatar.setPos(endPos)
                # game may have ended by now, check
                if hasattr(self, 'orthoWalk'):
                    # re-enable control of local toon
                    self.orthoWalk.start()

            # get rid of the dropshadow
            dropShadow.removeNode()
            del dropShadow

            # show the toon's dropshadow
            if toon and toon.dropShadow:
                toon.dropShadow.show()

            # get rid of the extra nodes
            geomNode = toon.getGeomNode()
            rotNode = geomNode.getParent()
            baseNode = rotNode.getParent()
            geomNode.reparentTo(baseNode)
            rotNode.removeNode()
            del rotNode
            geomNode.setZ(oldGeomNodeZ)

            toon.reparentTo(render)
            toon.setPos(endPos)
            parentNode.removeNode()
            del parentNode

            if avId == localAvatar.doId:
                toon.startSmooth()
                place = base.cr.playGame.getPlace()
                if place and hasattr(place,'fsm'):
                    place.fsm.request('walk')
            else:
                toon.startSmooth()

        # call the preFunc _this_frame_ to ensure that the local toon
        # update task does not run this frame
        preFunc()

        hitTrack = Sequence(
            Func(toon.setPos, Point3(0.0,0.0,0.0)),
            Wait(0.25),
            Parallel(flyTrack, cameraTrack, self.soundIUpDown,
            #Parallel(flyTrack, self.soundIUpDown,
                     spinHTrack, spinPTrack, soundTrack),
            Func(postFunc),
            name=toon.uniqueName("hitBySuit"))

        self.toonHitTracks[avId] = hitTrack
        hitTrack.start()#globalClockDelta.localElapsedTime(timestamp))
        posM = moleHill.getPos(render)
        posN = Point3(posM[0], posM[1], posM[2] + 4.0)
        #kapow = MovieUtil.createKapowExplosionTrack(render, posN, 3.0)
        #kapow.start()
        self.soundBomb.play()
        self.soundBomb2.play()
        
