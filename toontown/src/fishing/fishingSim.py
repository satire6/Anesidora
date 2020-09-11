# CREATE A TOON
from toontown.toon import NPCToons
from toontown.toon import ToonDNA
from toontown.toon import Toon
from direct.actor import Actor
import random
from direct.task import Task
import math
from toontown.effects import Ripples
import random
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directtools.DirectGeometry import LineNodePath

class SlotMachine2D(DirectObject):
    def __init__(self, numLines = 6):
        self.numLines = numLines
        self.fishList = [[],[],[],[]]
        self.labelList = [[],[],[],[]]
        xOffset = -0.3
        self.frame = DirectFrame()
        for j in range(4):
            yOffset = 0.2
            for i in range(numLines):
                l = DirectLabel(parent = self.frame, text = '',
                                text_align = TextNode.ACenter,
                                relief = DGG.RAISED,
                                scale = 0.1,
                                frameSize = (-1, 1, -.2, 0.75),
                                pos = (xOffset, 0, yOffset)
                                )
                self.labelList[j].append(l)
                yOffset -= 0.1
            xOffset += 0.2
        self.accept('caughtFish', self.updateMachine)
    def updateMachine(self, id, fishNum):
        # Update fish list
        self.fishList[id].append((id, fishNum))
        self.fishList[id] = self.fishList[id][-self.numLines:]
        self.checkForTriples(id,fishNum)
        self.checkForGroupBonus()
    def checkForTriples(self,id,fishNum):
        tripleCount = 1
        lastFish = -1
        for i in range(len(self.fishList[id])):
            self.labelList[id][i]['text'] = '%d-%d' % self.fishList[id][i]
            if self.fishList[id][i][1] == lastFish:
                tripleCount += 1
            else:
                tripleCount = 1
                lastFish = self.fishList[id][i][1]
            if tripleCount >= 3:
                for j in range(3):
                    self.labelList[id][i - j]['text_fg'] = (1,0,0,1)
                lastFish = self.fishList[id][i][1]
            else:
                self.labelList[id][i]['text_fg'] = (0,0,0,1)
    def checkForGroupBonus(self):
        for i in range(self.numLines):
            if ((i >= len(self.fishList[0])) or
                (i >= len(self.fishList[1])) or
                (i >= len(self.fishList[2])) or
                (i >= len(self.fishList[3]))):
                return
            fish = self.fishList[0][i][1]
            fMatch = 1
            for id in range(1,4):
                if self.fishList[id][i][1] != fish:
                    fMatch = 0
                    break
            if fMatch:
                # Must have matched
                for id in range(4):
                    self.labelList[id][i]['frameColor'] = (.5,.5,.5,1)
            else:
                # Must have matched
                for id in range(4):
                    self.labelList[id][i]['frameColor'] = (.8,.8,.8,1)
    def reset(self):
        for i in range(4):
            for l in self.labelList[i]:
                l['text'] = ''
        self.fishList = [[],[],[],[]]
    def destroy(self):
        self.ignore('caughtFish')
        for i in range(4):
            for l in self.labelList[i]:
                l.destroy()

sm2d = SlotMachine2D()
sm2d.frame.setPos(0.8, 0, 0.6)
sm2d.frame.setScale(.7)

class SlotMachine(DirectObject):
    def __init__(self, numLines = 6):
        self.numLines = numLines
        self.fishList = []
        self.labelList = []
        xOffset = -1.1
        yOffset = 0.8
        self.frame = DirectFrame()
        for i in range(numLines):
            l = DirectLabel(parent = self.frame,
                            text = '',
                            text_align = TextNode.ACenter,
                            relief = DGG.RAISED,
                            scale = 0.1,
                            frameSize = (-1, 1, -.2, 0.75),
                            pos = (xOffset, 0, yOffset)
                            )
            self.labelList.append(l)
            yOffset -= 0.1
        self.accept('caughtFish', self.updateMachine)
    def updateMachine(self, fishermanId, fishNum):
        self.fishList.append((fishermanId, fishNum))
        self.fishList = self.fishList[-self.numLines:]
        tripleCount = 1
        lastFish = -1
        for i in range(len(self.fishList)):
            self.labelList[i]['text'] = '%d-%d' % self.fishList[i]
            if self.fishList[i][1] == lastFish:
                tripleCount += 1
            else:
                tripleCount = 1
                lastFish = self.fishList[i][1]
            if tripleCount >= 3:
                for j in range(3):
                    self.labelList[i - j]['text_fg'] = (1,0,0,1)
                lastFish = self.fishList[i][1]
            else:
                self.labelList[i]['text_fg'] = (0,0,0,1)
    def reset(self):
        for l in self.labelList:
            l['text'] = ''
        self.fishList = []
    def destroy(self):
        self.ignore('caughtFish')
        for l in self.labelList:
            l.destroy()

sm = SlotMachine()
sm.frame.setScale(.7)
sm.frame.setPos(2.0,0,.18)

class Fisherman(Toon.Toon):
    numFishTypes = 3
    def __init__(self, id, toNpcId = 20001, fAutonomous = 1):
        # Default NPC ID is Flippy
        Toon.Toon.__init__(self)
        self.id = id 
        self.fAutonomous = fAutonomous
        npcInfo = NPCToons.NPCToonDict[toNpcId]
        dnaList = npcInfo[2]
        gender = npcInfo[3]
        dna = ToonDNA.ToonDNA()
        dna.newToonFromProperties(*dnaList)
        self.setDNA(dna)
        self.reparentTo(render)
        self.angleNP = self.find('**/actorGeom')
        # Create pole
        self.pole = Actor.Actor()
        self.pole.loadModel('phase_4/models/props/fishing-pole-mod')
        self.pole.loadAnims(
            {'cast' : 'phase_4/models/props/fishing-pole-chan'})
        # Get the top of the pole.
        self.ptop = self.pole.find('**/joint_attachBill')
        self.pole.pose('cast', 0)
        # Prepare Pole
        self.poleNode = []
        self.holdPole()
        self.createCastTrack()
        self.castIval = None
        # Prepare actor
        self.setupNeutralBlend()
        self.targetInterval = None
        # Start automatic casting or create cast button
        if self.fAutonomous:
            self.castButton = None
            self.targetButton = None
            self.startCasting()
        else:
            # Starts casting mode when mouse enters button region
            self.castButton = DirectButton(text = 'CAST',
                                           relief = None,
                                           scale = 0.1,
                                           pos = (0,0,-0.2))
            self.castButton.bind(DGG.ENTER, self.showCancelFrame)
            # A big screen encompassing frame to catch the button releases
            self.cancelFrame = DirectFrame(parent = self.castButton,
                                           frameSize = (-1,1,-1,1),
                                           relief = None,
                                           state = 'normal')
            # Make sure this is on top of all the other widgets
            self.cancelFrame.setBin('gui-popup', 0)
            self.cancelFrame.bind(DGG.B1PRESS, self.startAdjustingCastTask)
            self.cancelFrame.bind(DGG.B1RELEASE, self.finishCast)
            self.cancelFrame.hide()
                    # Create bob
            self.bob = loader.loadModel('phase_4/models/props/fishing_bob')
            self.bobSpot = Point3(0)
            # Parameters to control bob motion
            self.vZeroMax = 30.0
            self.angleMax = 30.0
            # Ripple effect
            self.ripples = Ripples.Ripples(self.angleNP)
            self.ripples.hide()
            # Target
            self.buttonFrame = DirectFrame()
            self.target = base.distributedFishingTarget.fishingTargetNode

            self.fishPivot = self.attachNewNode('fishPivot')
            self.fish = loader.loadModel('models/misc/smiley')
            self.fish.reparentTo(self.fishPivot)
            self.fish.setScale(0.3,1,0.3)
            self.wiggleIval = None
            self.circleIval = None
            self.initFish()
            
            self.targetButton = DirectButton(parent = self.buttonFrame,
                                             text = 'MOVE',
                                             relief = DGG.RAISED,
                                             scale = 0.1,
                                             pos = (0,0,-0.9),
                                             command = self.moveTarget)
            self.targetTypeButton = DirectCheckButton(
                parent = self.buttonFrame,
                text = 'MOVING',
                relief = DGG.RAISED,
                scale = 0.085,
                pos = (0.4,0,-0.895),
                command = self.setfMove)
            self.fMovingTarget = 0
            self.targetModeButton = DirectCheckButton(
                parent = self.buttonFrame,
                text = 'dTASK',
                relief = DGG.RAISED,
                scale = 0.085,
                pos = (0.8,0,-0.895),
                command = self.setfTargetMode)
            self.fTargetMode = 0
            # Vector line
            self.line = LineNodePath(render2d)
            self.line.setColor(VBase4(1,0,0,1))
            self.line.moveTo(0,0,0)
            self.line.drawTo(1,0,0)
            self.line.create()
            self.moveTarget()

    def showCancelFrame(self, event):
        # Also display cancel frame to catch clicks outside of the popup
        self.cancelFrame.show()
    def startAdjustingCastTask(self, event):
        # Start task to adjust power of cast
        self.getMouse()
        self.initMouseX = self.mouseX
        self.initMouseY = self.mouseY
        self.initMouseX = 0
        self.initMouseY = -0.2
        self.line.lineSegs.setVertex(0, self.initMouseX, 0, self.initMouseY)
        self.angleNP.setH(0)
        self.__hideBob()
        taskMgr.remove('distCheck')
        # Position and scale cancel frame to fill entire window
        self.cancelFrame.setPos(render2d,0,0,0)
        self.cancelFrame.setScale(render2d,1,1,1)
        self.castTrack.finish()
        self.castTrack.setT(0)
        self.castTrack.start(startT = 0, endT=0.4)
        self.castIval = Sequence(
            Wait(0.4),
            Func(taskMgr.add, self.adjustingCastTask, 'adjustCastTask')
            )
        self.castIval.start()
    def adjustingCastTask(self, state):
        self.getMouse()
        deltaX = self.mouseX - self.initMouseX
        deltaY = self.mouseY - self.initMouseY
        self.line.lineSegs.setVertex(1, self.mouseX, 0, self.mouseY)
        dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)
        delta = (dist/0.5)
        if deltaY > 0:
            delta *= -1
        p = max(min(delta, 1.0), 0.0)
        self.power = p
        self.castTrack.setT(0.4 + p * 0.5)
        self.bobSpot = Point3(0, 6.5 + p * 25.0, -1.9)
        # Calc angle
        if deltaY == 0:
            angle = 0
        else:
            angle = rad2Deg(math.atan(deltaX/deltaY))
        self.angleNP.setH(-angle)
        return Task.cont
    def stopAdjustingCastTask(self):
        taskMgr.remove('adjustingTask')
    def setupNeutralBlend(self):
        self.stop()
        self.loop('neutral')
        self.enableBlend()
        self.pose('cast', 0)
        self.setControlEffect('neutral', 0.2)
        self.setControlEffect('cast', 0.8)
    def startCasting(self):
        if self.fAutonomous:
            self.castIval = Sequence(
                ActorInterval(self, 'cast'),
                Func(self.catchFish),
                Parallel(ActorInterval(self, 'neutral', loop = 1,
                                       duration = 100),
                         Sequence(Wait(random.random() * 20.0),
                                  Func(self.startCasting),
                                  )
                         )
                )
        else:
            self.castIval = Sequence(
                ActorInterval(self, 'cast'),
                Func(self.catchFish),
                ActorInterval(self, 'neutral', loop = 1, duration = 100)
                )
        self.castIval.play()
    def stopCasting(self):
        if self.castIval:
            self.castIval.pause()
        if self.targetInterval:
            self.stopTargetInterval()
        taskMgr.remove('distCheck')
    def catchFish(self):
        fishNum = int(round(random.random() * self.numFishTypes))
        messenger.send('caughtFish', sentArgs = [self.id, fishNum])
    def setupNeutralBlend(self):
        self.stop()
        self.loop('neutral')
        self.enableBlend()
        self.pose('cast', 0)
        self.setControlEffect('neutral', 0.2)
        self.setControlEffect('cast', 0.8)
    def getPole(self):
        toonTrack = Sequence(
            # Blend in neutral anim
            Func(self.setupNeutralBlend),
            # Pull out pole
            Func(self.holdPole),
            Parallel(ActorInterval(self, 'cast', playRate = 0.5,
                                   duration = 27./12.),
                     ActorInterval(self.pole, 'cast', playRate = 0.5,
                                   duration = 27./12.),
                     LerpScaleInterval(self.pole,
                                       duration = 2.0,
                                       scale = 1.0,
                                       startScale = 0.01)),
            )
        toonTrack.play()
    def putAwayPole(self):
        Sequence(
            Parallel(ActorInterval(self, 'cast',
                                   duration = 1.0, startTime = 1.0,
                                   endTime = 0.0),
                     ActorInterval(self.pole, 'cast',
                                   duration = 1.0, startTime = 1.0,
                                   endTime = 0.0),
                     LerpScaleInterval(self.pole,
                                       duration = 0.5,
                                       scale = 0.01,
                                       startScale = 1.0)),
            Func(self.dropPole)).start()
    def holdPole(self):
        if self.poleNode != []:
            self.dropPole()

        # One node, instanced to each of the toon's three right hands,
        # will hold the pole.
        np = NodePath('pole-holder')
        hands = self.getRightHands()
        for h in hands:
            self.poleNode.append(np.instanceTo(h))

        self.pole.reparentTo(self.poleNode[0])
    def dropPole(self):
        self.__hideBob()
        #self.__hideLine()
        if self.pole != None:
            self.pole.clearMat()
            self.pole.detachNode()

        for pn in self.poleNode:
            pn.removeNode()
        self.poleNode = []
    def createCastTrack(self):
        self.castTrack = Sequence(
            Parallel(ActorInterval(self, 'cast',
                                   duration = 2.0, startTime = 1.0),
                     ActorInterval(self.pole, 'cast',
                                   duration = 2.0, startTime = 1.0),
                     )
            )
    def cast(self):
        self.castTrack.start()
    def finishCast(self, event = None):
        #self.line.lineSegs.setVertex(1,self.initMouseX,0,self.initMouseY)
        self.cancelFrame.hide()
        if not self.castTrack:
            self.createCastTrack()
        self.castIval.finish()
        taskMgr.remove('adjustCastTask')
        taskMgr.remove('moveBobTask')
        self.castTrack.pause()
        #self.castTrack.start(self.castTrack.getT())
        p = self.power
        startT = 0.9 + (1 - p) * 0.3
        self.castTrack.start(startT)
        self.bobStartPos = Point3(0.017568, 7.90371, 6.489)
        Sequence(Wait(1.2 - startT),
                 Func(self.startMoveBobTask)
                 ).start()
    def startMoveBobTask(self):
        self.__showBob()
        self.bobStartT = globalClock.getFrameTime()
        taskMgr.add(self.moveBobTask, 'moveBobTask')
    def moveBobTask(self, state):
        # Accel due to gravity
        g = 32.2
        # Elapsed time of cast
        t = globalClock.getFrameTime() - self.bobStartT
        # Scale bob velocity and angle based on power of cast
        vZero = self.power * self.vZeroMax
        angle = deg2Rad(self.power * self.angleMax)
        # How far has bob moved from start point?
        deltaY = vZero * math.cos(angle) * t
        deltaZ = vZero * math.sin(angle) * t - (g * t * t)/2.0
        deltaPos = Point3(0, deltaY, deltaZ)
        # Current bob position
        pos = self.bobStartPos + deltaPos
        # Have we reached end condition?
        if pos[2] < -1.9:
            pos.setZ(-1.9)
            self.ripples.reparentTo(self.angleNP)
            self.ripples.setPos(pos)
            self.ripples.play()
            returnVal = Task.done
            if self.fTargetMode:
                taskMgr.add(self.distCheck, 'distCheck')
            else:
                self.distCheck()
        else:
            returnVal = Task.cont
        self.bob.setPos(pos)
        return returnVal
    def distCheck(self, state = None):
        # Check to see if we hit the target
        bPos = self.bob.getPos()
        # Check target
        returnVal = self.__distCheck(bPos, self.target)
        if returnVal == Task.done:
            return returnVal
        # Check fish
        return self.__distCheck(bPos, self.fish)
    def __distCheck(self, bPos, target):
        def flashTarget():
            self.stopTargetInterval()
            self.target.getChild(0).setColor(0,0,1)
        def flashFish():
            taskMgr.remove('turnTask')
            self.fish.lerpScale(Point3(0.01), 0.5, task = 'flashFish')
        tPos = target.getPos(self.angleNP)
        tDist = Vec3(tPos - bPos)
        tDist.setZ(0)
        dist = tDist.length()
        if target == self.target:
            flashFunc = flashTarget
            moveFunc = self.moveTarget
        else:
            flashFunc = flashFish
            moveFunc = self.turnFish
        if dist < 2.5:
            fBite = (random.random() < 0.4) or (not self.fTargetMode)
            delay = self.fTargetMode * 0.25
            if fBite:
                print 'BITE'
                Sequence(Wait(random.random() * delay),
                         Func(flashFunc),
                         Func(self.catchFish),
                         Wait(2.0),
                         Func(moveFunc),
                         ).play()
            else:
                print 'MISS'
                def moveIt():
                    moveFunc(targetPos = target.getPos())
                Sequence(Wait(random.random() * delay),
                         Func(moveIt)
                         ).play()
            return Task.done
        return Task.cont
    def stopTargetInterval(self):
        if self.targetInterval:
            self.targetInterval.pause()
        self.targetInterval = None
    def __showBob(self):
        # Put the bob in the water and make it gently float.
        self.__hideBob()
        self.bob.reparentTo(self.angleNP)
        self.bob.setPos(self.ptop, 0,0,0)
    def __hideBob(self):
        if self.bob != None:
            self.bob.detachNode()
    def getMouse(self):
        if (base.mouseWatcherNode.hasMouse()):
            self.mouseX = base.mouseWatcherNode.getMouseX()
            self.mouseY = base.mouseWatcherNode.getMouseY()
        else:
            self.mouseX = 0
            self.mouseY = 0
    def setfMove(self, fMoving):
        self.fMovingTarget = fMoving
    def setfTargetMode(self, fTargetMode):
        self.fTargetMode = fTargetMode
    def moveTarget(self, targetPos = None):
        base.distributedFishingTarget.sendUpdate('bobEnter', [])
#        self.stopTargetInterval()
#        self.target.clearColor()
#        if not targetPos:
#            x = -87.0 + random.random() * 15.0
#            y = 25.0 + random.random() * 20.0
#            z = -4.8
#            self.targetPos = Point3(x,y,z)
#        else:
#            self.targetPos.assign(targetPos)
#        if self.fMovingTarget:
#            self.makeTargetInterval()
#        else:
#            #self.target.setPos(self.targetPos)
    def initFish(self):
        x = -10.0 + random.random() * 20.0
        y = 00.0 + random.random() * 30.0
        z = -1.6
        self.fishPivot.setPos(x,y,z)
        self.turningRadius = 5.0 + random.random() * 5.0
        self.fish.setPos(self.turningRadius,0,-0.4)
        if self.wiggleIval:
            self.wiggleIval.pause()
        self.wiggleIval = Sequence(
            self.fish.hprInterval(0.5,
                                     hpr = Point3(10,0,0),
                                     startHpr=Point3(-10,0,0),
                                     blendType = 'easeInOut'),
            self.fish.hprInterval(0.5,
                                     hpr = Point3(-10,0,0),
                                     startHpr = Point3(10,0,0),
                                     blendType = 'easeInOut'))
        self.wiggleIval.loop()
        if self.circleIval:
            self.circleIval.pause()
        self.circleIval = self.fishPivot.hprInterval(
            20, Point3(360,0,0), startHpr = Point3(0))
        self.circleIval.loop()
        taskMgr.remove('turnTask')
        taskMgr.doMethodLater(3.0 + random.random() * 3.0,
                              self.turnFish,
                              'turnTask')
        taskMgr.remove('fishBoundsCheck')
        taskMgr.add(self.fishBoundsCheck, 'fishBoundsCheck')
    def fishBoundsCheck(self, state):
        pos = self.fish.getPos(self)
        if pos[0] < -20:
            self.fishPivot.setX(self.fishPivot.getX() + 40.0)
        elif pos[0] > 20:
            self.fishPivot.setX(self.fishPivot.getX() - 40.0)
        if pos[1] < -10:
            self.fishPivot.setY(self.fishPivot.getY() + 50.0)
        elif pos[1] > 40:
            self.fishPivot.setY(self.fishPivot.getY() - 50.0)
        return Task.cont
    def turnFish(self,state = None, targetPos = None):
        self.fish.setScale(0.3,1,0.3)
        if self.circleIval:
            self.circleIval.pause()
        newTurningRadius = 5.0 + random.random() * 5.0
        fRightTurn = random.random() < 0.5
        if fRightTurn:
            newTurningRadius *= -1.0
        offset = self.turningRadius - newTurningRadius
        self.fishPivot.setX(self.fishPivot, offset)
        self.turningRadius = newTurningRadius
        self.fish.setX(self.turningRadius)
        currH = self.fishPivot.getH() % 360.0
        if fRightTurn:
            self.circleIval = self.fishPivot.hprInterval(
                20, Point3(currH - 360,0,0),
                startHpr = Point3(currH,0,0))
        else:
            self.circleIval = self.fishPivot.hprInterval(
                20, Point3(currH + 360,0,0),
                startHpr = Point3(currH,0,0))
        self.circleIval.loop()
        taskMgr.doMethodLater(3.0 + random.random() * 3.0,
                              self.turnFish,
                              'turnTask')
        return Task.done
    def makeTargetInterval(self):
        x = -10.0 + random.random() * 20.0
        y = 0.0 + random.random() * 30.0
        z = -1.6
        self.targetEndPos = Point3(x,y,z)
        dist = Vec3(self.targetEndPos - self.targetPos).length()
        dur = dist/1.5
        dur = dur * (0.75 + random.random() * 0.5)
        self.targetInterval = Sequence(
            self.target.posInterval(dur,
                                    self.targetEndPos,
                                    startPos = self.targetPos,
                                    blendType = 'easeInOut'),
            self.target.posInterval(dur,
                                    self.targetPos,
                                    startPos = self.targetEndPos,
                                    blendType = 'easeInOut'),
            name = 'moveInterval'
            )
        offsetDur = dur/random.randint(1,4)
        amplitude = 0.1 + random.random() * 1.0
        self.targetInterval.loop()
    def destroy(self):
        if not self.fAutonomous:
            self.castButton.destroy()
            self.buttonFrame.destroy()
            self.line.removeNode()
            taskMgr.remove('turnTask')
            taskMgr.remove('fishBoundsCheck')
        self.stopCasting()
        self.removeNode()


f1 = Fisherman(0)
f1.setPosHpr(-77.89, 46.82, -3.18, 183.81, 0.00, 0.00)

f2 = Fisherman(1)
f2.setPosHpr(-91.00, 42.83, -3.18, 211.61, 0.00, 0.00)

f3 = Fisherman(2, fAutonomous = 0)
f3.setPosHpr(-95.28, 31.55, -3.18, 251.57, 0.00, 0.00)

f4 = Fisherman(3)
f4.setPosHpr(-97.49, 18.91, -3.48, 270.00, 0.00, 0.00)

fList = [f1,f2,f3,f4]


def kill():
    for f in fList:
        f.destroy()

def stopCasting():
    for f in fList:
        f.stopCasting()

def startCasting():
    for f in fList:
        f.startCasting()

