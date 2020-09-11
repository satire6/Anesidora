from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from toontown.toonbase import ToontownGlobals
import math
from math import *
import random

class SkyHolder:
    SomeCounter = 0
    def __init__(self, sky = None):
        self.skyNumber = self.SomeCounter
        self.SomeCounter += 1
        
        self.skyIn = sky
        
        self.setup()
        
    def setup(self):
        self.baseNode = camera.attachNewNode("sky object")
        self.baseNode.show()
        self.skyGN = GeomNode("Sky Geometry")
        self.skyNodePathGeom = self.baseNode.attachNewNode(self.skyGN)
        self.skyIn.reparentTo(self.baseNode)
        self.skyIn.setDepthTest(0)
        self.skyIn.setDepthWrite(0)
        self.skyIn.setBin("background", 100)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.baseNode.node().setEffect(ce)
        
        taskMgr.add(self.redraw, ("recreateBand %s" % (self.skyNumber)), priority=0)

        

        
    def delete(self):
        taskMgr.remove(("recreateBand %s" % (self.skyNumber)))
        self.skyGN.removeAllGeoms()
        self.baseNode.remove()
        
    def redraw(self, task):
        return task.cont
        
        
        
