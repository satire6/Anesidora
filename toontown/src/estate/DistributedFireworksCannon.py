from toontown.toonbase.ToontownGlobals import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from HouseGlobals import *
from toontown.effects import DistributedFireworkShow
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode
import FireworksGui

class DistributedFireworksCannon(DistributedFireworkShow.DistributedFireworkShow):

    notify = directNotify.newCategory("DistributedFireworksCannon")

    def __init__(self, cr):
        DistributedFireworkShow.DistributedFireworkShow.__init__(self,cr)
        self.fireworksGui = None
        self.load()
        
    def generateInit(self):
        DistributedFireworkShow.DistributedFireworkShow.generateInit(self)
        """generateInit(self)
        This method is called when the DistributedObject is first introduced
        to the world... Not when it is pulled from the cache.
        """
        self.fireworksSphereEvent = self.uniqueName("fireworksSphere")
        self.fireworksSphereEnterEvent = "enter" + self.fireworksSphereEvent
        self.fireworksGuiDoneEvent = "fireworksGuiDone"
        self.shootEvent = "fireworkShootEvent"

        self.collSphere = CollisionSphere(0, 0, 0, 2.5)
        # Make the sphere intangible
        self.collSphere.setTangible(1)
        self.collNode = CollisionNode(self.fireworksSphereEvent)
        self.collNode.setIntoCollideMask(ToontownGlobals.WallBitmask)
        self.collNode.addSolid(self.collSphere)
        self.collNodePath = self.geom.attachNewNode(self.collNode)

    def generate(self):
        """generate(self)
        This method is called when the DistributedObject is reintroduced
        to the world, either for the first time or from the cache.
        """
        DistributedFireworkShow.DistributedFireworkShow.generate(self)
        
    def announceGenerate(self):
        self.notify.debug("announceGenerate")
        self.accept(self.fireworksSphereEnterEvent,  self.__handleEnterSphere)
        
    def disable(self):
        self.notify.debug("disable")
        self.ignore(self.fireworksSphereEnterEvent)
        self.ignore(self.shootEvent)
        self.ignore(self.fireworksGuiDoneEvent)
        if self.fireworksGui:
            self.fireworksGui.destroy()
            self.fireworksGui = None
        DistributedFireworkShow.DistributedFireworkShow.disable(self)

    def delete(self):
        self.notify.debug("delete")
        self.geom.removeNode()
        DistributedFireworkShow.DistributedFireworkShow.delete(self)

    def load(self):
        self.geom = loader.loadModel("phase_5/models/props/trashcan_TT.bam")
        self.geom.reparentTo(base.cr.playGame.hood.loader.geom)
        self.geom.setScale(.5)
        
    def __handleEnterSphere(self, collEntry):
        self.notify.debug("handleEnterSphere()")
        # don't let other toons access the fireworks now
        self.ignore(self.fireworksSphereEnterEvent)
        self.sendUpdate("avatarEnter", [])
        
    def __handleFireworksDone(self):
        self.ignore(self.fireworksGuiDoneEvent)
        self.ignore(self.shootEvent)
        self.sendUpdate("avatarExit")
        self.fireworksGui.destroy()
        self.fireworksGui = None

    def freeAvatar(self):
        """
        This is a message from the AI used to free the avatar from movie mode
        """
        # If we are the local toon and we have simply taken too long,
        # just free us
        base.localAvatar.posCamera(0,0)
        base.cr.playGame.getPlace().setState("walk")
        # Start accepting the fireworks collision sphere event again
        self.accept(self.fireworksSphereEnterEvent, self.__handleEnterSphere)
        
        
    def setMovie(self, mode, avId, timestamp):
        """
        This is a message from the AI describing a movie between this fireworks
        cannon and a Toon that has approached us. 
        """
        timeStamp = globalClockDelta.localElapsedTime(timestamp)
        # See if this is the local toon
        isLocalToon = (avId == base.localAvatar.doId)

        if (mode == FIREWORKS_MOVIE_CLEAR):
            self.notify.debug("setMovie: clear")
            return
        elif (mode == FIREWORKS_MOVIE_GUI):
            self.notify.debug("setMovie: gui")
            if isLocalToon:
                self.fireworksGui = FireworksGui.FireworksGui(self.fireworksGuiDoneEvent, self.shootEvent)
                self.accept(self.fireworksGuiDoneEvent, self.__handleFireworksDone)
                self.accept(self.shootEvent, self.localShootFirework)
            return
        else:
            self.notify.warning("unknown mode in setMovie: %s" % (mode))
        
    def setPosition(self, x, y, z):
        self.pos = [x,y,z]
        self.geom.setPos(x,y,z)
        
    def localShootFirework(self, index):
        style = index
        col1,col2 = self.fireworksGui.getCurColor()
        amp = 30

        # attach a dummy node to the toon that always in front of him.
        # This is where the fireworks will shoot from.
        dummy = base.localAvatar.attachNewNode("dummy")
        dummy.setPos(0,100,60)
        pos = dummy.getPos(render)
        dummy.removeNode()
        
        print ("lauFirework: %s, col=%s" % (index,col1))
        self.d_requestFirework(pos[0],pos[1],pos[2],style,col1,col2)
        
