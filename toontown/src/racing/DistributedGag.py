from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.interval.ProjectileInterval import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from DroppedGag import *
#This class is primarily for any gags whose target is not deterministically
#know.

class DistributedGag(DistributedObject.DistributedObject):
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.nodePath=None
        self.billboard=False
        self.scale=1
        self.shadow=True
        self.dropShadow=None
        self.type = 0
        

            

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        self.nodePath.delete()
        self.ignoreAll()

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        if not self.nodePath:
            self.makeNodePath()
        self.delta=-globalClockDelta.networkToLocalTime(self.initTime, globalClock.getFrameTime(), 16, 100)+globalClock.getFrameTime()
        #print self.delta

        if self.type == 0: #banana
            self.name=self.uniqueName("banana")
        elif self.type == 1: #pie
            self.name=self.uniqueName("pie")

        self.nodePath.reparentTo(self.race.geom)
        if(self.ownerId==localAvatar.doId):
            base.race.thrownGags[0].remove()
            base.race.thrownGags=base.race.thrownGags[1:]
            self.nodePath.setPos(self.pos[0], self.pos[1], self.pos[2])
        else:
            startPos=base.cr.doId2do[self.ownerId].getPos(render)
            endPos=Vec3(self.pos[0], self.pos[1], self.pos[2])
            throwIt=ProjectileInterval(self.nodePath, startPos=startPos, endPos=endPos, duration=1)
            throwIt.start()
        taskMgr.doMethodLater(.8-self.delta, self.addCollider, self.uniqueName("addCollider"))


    def addCollider(self, t):
        bs=CollisionSphere(0, 0, 0, 2)
        bn=CollisionNode(self.name)
        self.bnp=NodePath(bn)
        self.bnp.reparentTo(self.nodePath)
        self.bnp.node().addSolid(bs)
        self.bnp.node().setIntoCollideMask(BitMask32(0x8000))
        self.bnp.node().setFromCollideMask(BitMask32(0x8000))
        #self.bnp.show()
        self.accept("imIn-"+self.name, self.b_imHit)

    def b_imHit(self, cevent):
        self.ignoreAll()
        self.sendUpdate("hitSomebody", [base.race.localKart.doId, globalClockDelta.getFrameNetworkTime(16, 100)])
        if self.type==0:
            base.race.localKart.hitBanana()
        elif self.type==1:
            base.race.localKart.hitPie()
        self.nodePath.hide()
        if(hasattr(self, "bnp")):
            self.bnp.remove()

    def hitSomebody(self, kartId, timeStamp):
        if(base.race.localKart.doId!=kartId):
            assert kartId in base.cr.doId2do
            #Okay, this is correct
            self.nodePath.hide()
            if(hasattr(self, "bnp")):
                self.bnp.remove()
            base.cr.doId2do[kartId].playSpin(timeStamp)

    def setActivateTime(self, actTime):
        self.activateTime=actTime

    def setInitTime(self, initTime):
        self.initTime=initTime

    def setRace(self, doId):
        self.race = base.cr.doId2do.get(doId)

    # The handler that catches the initial position established on the AI
    def setPos(self, x, y, z):
        #print x, ": ", y, ": ", z
        self.pos=(x, y, z)


    def makeNodePath(self):
        if self.type == 0: #banana
            self.nodePath = DroppedGag(self.uniqueName("gag"), base.race.banana)
            if self.billboard:
                self.nodePath.setBillboardPointEye()
            self.nodePath.setScale(0.9*self.scale)
        if self.type == 1: #pie
            self.nodePath = DroppedGag(self.uniqueName("gag"), base.race.banana)
            if self.billboard:
                self.nodePath.setBillboardPointEye()
            self.nodePath.setScale(4.0*self.scale)

    def setOwnerId(self, ownerId):
        self.ownerId=ownerId

    def setType(self, type):
        self.type = type; #0 banana #1 pie

