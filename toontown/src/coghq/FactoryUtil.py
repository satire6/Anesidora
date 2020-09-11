"""FactoryUtil module: contains useful stuff for factory mockup"""

from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals
import MovingPlatform
from direct.task.Task import Task
from toontown.suit import Suit
from toontown.suit import SuitDNA

class Ouch(DirectObject.DirectObject):
    def __init__(self, keyEvent, callback):
        DirectObject.DirectObject.__init__(self)
        self.accept(keyEvent, callback)

    def destroy(self):
        self.ignoreAll()

    
class CyclePlacer(DirectObject.DirectObject):
    def __init__(self, locations, keyEvent, startIndex=0):
        """
        locations is list of ((x,y,z),h) pairs
        keyEvent is something like 'f3-up'
        """
        DirectObject.DirectObject.__init__(self)
        self.locations = locations
        self.index = startIndex
        self.accept(keyEvent, self.gotoNextLocation)
    def destroy(self):
        self.locations = None
        self.ignoreAll()
    def gotoNextLocation(self):
        self.index = (self.index + 1) % len(self.locations)
        self.gotoLocation()
    def gotoLocation(self, index=None):
        if index is None:
            index = self.index
        pos, h = self.locations[index]
        base.localAvatar.reparentTo(render)
        base.localAvatar.setPos(*pos)
        base.localAvatar.setH(h)

class ToonLifter(DirectObject.DirectObject):
    SerialNum = 0
    def __init__(self, keyDownEvent, speed=2):
        """
        keyDownEvent must have a corresponding '-up' event
        e.g. for 'f3' there must be a 'f3-up'
        """
        DirectObject.DirectObject.__init__(self)
        self.serialNum = ToonLifter.SerialNum
        ToonLifter.SerialNum += 1
        self.taskName = 'ToonLifter%s' % self.serialNum
        self.keyDownEvent = keyDownEvent
        self.keyUpEvent = self.keyDownEvent + '-up'
        self.speed = speed
        self.accept(self.keyDownEvent, self.startLifting)
    def destroy(self):
        self.ignoreAll()
        taskMgr.remove(self.taskName)
    def startLifting(self):
        def liftTask(task, self=self):
            base.localAvatar.setZ(base.localAvatar.getZ() + self.speed)
            return Task.cont
        def stopLifting(self=self):
            taskMgr.remove(self.taskName)
            self.ignore(self.keyUpEvent)
            self.accept(self.keyDownEvent, self.startLifting)
        self.ignore(self.keyDownEvent)
        self.accept(self.keyUpEvent, stopLifting)
        taskMgr.add(liftTask, self.taskName)

"""
class FactoryPlatform(MovingPlatform.MovingPlatform):
    def __init__(self, index, startPos, endPos, speed, waitDur,
                 model, floorNodeName=None):
        MovingPlatform.MovingPlatform.__init__(self, index,
                                               model, floorNodeName)
        self.index = index
        self.startPos = startPos
        self.endPos = endPos
        self.speed = speed
        self.waitDur = waitDur

    def destroy(self):
        MovingPlatform.MovingPlatform.destroy(self)

    def start(self, startTime):
        distance = Vec3(self.startPos-self.endPos).length()
        duration = distance/self.speed
        self.moveIval = Sequence(
            WaitInterval(self.waitDur),
            LerpPosInterval(self, duration,
                            self.endPos, startPos=self.startPos,
                            name='siloPlatOut%s' % self.index),
            WaitInterval(self.waitDur),
            LerpPosInterval(self, duration,
                            self.startPos, startPos=self.endPos,
                            name='siloPlatBack%s' % self.index),
            name='siloPlatIval%s' % self.index,
            )
        self.moveIval.loop()
        self.moveIval.setT(globalClock.getFrameTime() - startTime)

    def stop(self):
        self.ignoreAll()
        self.moveIval.pause()
        del self.moveIval

class WalkingSuit:
    SerialNum = 0
    def __init__(self, wayPoints, dna=None):
        self.serialNum = WalkingSuit.SerialNum
        WalkingSuit.SerialNum += 1
        self.wayPoints = wayPoints
        if dna is None:
            dna = 'f' # flunky
        self.suit = Suit.Suit()
        d = SuitDNA.SuitDNA()
        d.newSuit(dna)
        self.suit.setDNA(d)

    def destroy(self):
        self.suit.delete()
        del self.suit
    
    def start(self, startTime):
        self.walkIval = Sequence(name='factorySuitWalk%s' % self.serialNum)
        for i in range(len(self.wayPoints)):
            distance = Vec3(self.wayPoints[i-1][0] -
                            self.wayPoints[i][0]).length()
            speed = ToontownGlobals.SuitWalkSpeed
            duration = distance / speed
            self.walkIval += [
                Func(self.suit.setH, self.wayPoints[i-1][1]),
                LerpPosInterval(self.suit, duration, self.wayPoints[i][0],
                                startPos=self.wayPoints[i-1][0]),
                ]
        self.suit.reparentTo(render)
        self.suit.loop('walk')
        self.walkIval.loop()
        self.walkIval.setT(globalClock.getFrameTime() - startTime)

    def stop(self):
        self.walkIval.finish()
        del self.walkIval
"""
