from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.fsm import FSM
from direct.distributed import DistributedObject
from direct.showutil import Rope
from direct.showbase import PythonUtil
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPGlobals
from direct.actor import Actor

class DistributedLawbotBossGavel(DistributedObject.DistributedObject, FSM.FSM):
    """ This class represents a crane holding a magnet on a cable.
    The DistributedCashbotBoss creates four of these for the CFO
    battle scene. """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLawbotBossGavel')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedLawbotBossGavel')

        self.boss = None
        self.index = None
        self.avId = 0
        
        #self.modelPath = "phase_11/models/lawbotHQ/lawbot_gavel"
        self.modelPath = "phase_11/models/lawbotHQ/LB_gavel"
        self.modelFindString = None

        self.nodePath = None

        self.ival = None
        self.origHpr = Point3(0,0,0)
        self.downTime = 0.5 #how long to stomp down
        self.upTime = 5 #how long to go up

        self.gavelSfx = None

    def announceGenerate(self):
        self.notify.debug("announceGenerate: %s" % self.doId)
        DistributedObject.DistributedObject.announceGenerate(self)
        self.name = 'gavel-%s' % (self.doId)
        #self.setName(self.name)

  

        # Load the model, (using loadModelOnce), and child it to the nodepath
        self.loadModel(self.modelPath, self.modelFindString)
        # animate if necessary
        #self.startAnimation()
        # Put this thing in the world
        self.nodePath.wrtReparentTo(render)

        self.gavelSfx = loader.loadSfx('phase_11/audio/sfx/LB_gavel.mp3')
        
        tempTuple = ToontownGlobals.LawbotBossGavelPosHprs[self.index]
        self.nodePath.setPosHpr(*tempTuple)
        self.origHpr = Point3( tempTuple[3], tempTuple[4], tempTuple[5])
        self.downTime = ToontownGlobals.LawbotBossGavelTimes[self.index][0]
        self.upTime = ToontownGlobals.LawbotBossGavelTimes[self.index][1]
        self.stayDownTime = ToontownGlobals.LawbotBossGavelTimes[self.index][2]


        
        assert(not self.boss.gavels.has_key(self.index))
        self.boss.gavels[self.index] = self

    def delete(self):
        # Call up the chain
        DistributedObject.DistributedObject.delete(self)

        # Really, we don't want to unloadModel on this, until we're
        # leaving the safezone.  Calling unloadModel will force the
        # next treasure of this type to reload from disk.
        loader.unloadModel(self.modelPath)
        
        self.nodePath.removeNode()


    def loadModel(self, modelPath, modelFindString = None):
        if self.nodePath == None:
            self.makeNodePath()
        else:
            self.gavel.getChildren().detach()

        # Load the gavel model and put it under our root node.
        model = loader.loadModel(modelPath)
        if modelFindString != None:
            modTel = model.find("**/" + modelFindString)
            assert model != None

        parts = model.findAllMatches("**/gavel*")
        #color it dark brown
        #parts.setColor(139,37,12)
        #parts.setColor(0.402,0.06640625,0.02734375)

        gavelTop = model.find("**/top*")
        gavelHandle = model.find("**/handle*")
        #import pdb; pdb.set_trace()
            
        model.instanceTo(self.gavel)

        self.attachColTube()

        self.scale = 3.0        
        self.nodePath.setScale(self.scale)


    def attachColTube(self):

        gavelTop = self.nodePath.find("**/top*")
        self.gavelTop = gavelTop
        gavelHandle = self.nodePath.find("**/handle*")

        collNode = CollisionNode(self.uniqueName("headSphere"))
        #collNode.setIntoCollideMask(WallBitmask)
        #collNode.addSolid(collSphere)

        topBounds = gavelTop.getBounds()
        center = topBounds.getCenter()
        radius = topBounds.getRadius()

        tube1 = CollisionTube(0, -1, center.getZ(), 0, 1, center.getZ(), 1)
        tube1.setTangible(0)        
        collNode.addSolid(tube1)
        collNode.setTag('attackCode', str(ToontownGlobals.BossCogGavelStomp))        
        collNode.setName('GavelZap')

        
        self.collNodePath = self.nodePath.attachNewNode(collNode)
        #self.collNodePath.stash()

        handleBounds = gavelHandle.getBounds()
        handleCenter = handleBounds.getCenter()
        handleRadius = handleBounds.getRadius()


        tube2 = CollisionTube(0, 0, handleCenter.getZ() + handleRadius, 0, 0, handleCenter.getZ() - handleRadius, 0.25)
        tube2.setTangible(0)
        handleCollNode = CollisionNode(self.uniqueName("gavelHandle"))
        handleCollNode.addSolid(tube2)
        handleCollNode.setTag('attackCode', str(ToontownGlobals.BossCogGavelHandle))
        handleCollNode.setName('GavelHandleZap')
        self.handleCollNodePath = self.nodePath.attachNewNode(handleCollNode)
        
        

    def makeNodePath(self):
        self.nodePath = Actor.Actor() #NodePath(self.uniqueName("gavelNodePath"))        

 

        

        self.gavel = self.nodePath.attachNewNode('myGavel')

        # Make a sphere, name it uniqueName("headSphere"), and child it
        # to the nodepath.
        #collSphere = CollisionSphere(0, 0, 0, 1)
        # Make the sphere intangible
        #collSphere.setTangible(0)
        #collSphere.setTangible(1)




        #self.scale = 5.0

        
    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        assert(self.boss.gavels.get(self.index) == self)
        self.nodePath.detachNode()
        if (self.ival):        
            self.ival.finish();
            self.ival = None

        self.ignoreAll()
        del self.boss.gavels[self.index]
        self.cleanup()

    def cleanup(self):
        #if self.state != 'Off':
        #    self.demand('Off')
        self.boss = None



    ##### Messages To/From The Server #####

    def setBossCogId(self, bossCogId):
        self.bossCogId = bossCogId

        # This would be risky if we had toons entering the zone during
        # a battle--but since all the toons are always there from the
        # beginning, we can be confident that the BossCog has already
        # been generated by the time we receive the generate for its
        # associated battles.
        self.boss = base.cr.doId2do[bossCogId]

    def setIndex(self, index):
        self.index = index

    def setState(self, state):
        avId = 0
        if state == 'C':
            self.demand('Controlled', avId)
        elif state == 'F':
            self.demand('Free')
        elif state == 'N':
            self.demand('On')
        else:
            self.notify.error("Invalid state from AI: %s" % (state))


    ### FSM States ###

    def enterOn(self):
        #do whatever we need to start the big gavels stomping
        self.notify.debug("enterOn for gavel %d" % self.index)

        myHeadings = ToontownGlobals.LawbotBossGavelHeadings[self.index]

        seqName = "LawbotBossGavel-%s" % self.doId
        self.ival = Sequence(name = seqName)
        downAngle = -80

        for index in range(len(myHeadings)):
            nextIndex = index +1;
            if (nextIndex == len(myHeadings)):
                nextIndex = 0
                
            goingDown = self.nodePath.hprInterval(self.downTime,
                                                  Point3(myHeadings[index] + self.origHpr[0],
                                                  downAngle,
                                                  self.origHpr[2]),
                                                  startHpr = Point3(myHeadings[index] + self.origHpr[0] ,0,self.origHpr[2]))
            self.ival.append(goingDown)
            self.ival.append(SoundInterval(self.gavelSfx, node = self.gavelTop))
            self.ival.append(Wait(self.stayDownTime))
            
            goingUp = self.nodePath.hprInterval(self.upTime,
                                                Point3(myHeadings[nextIndex] + self.origHpr[0],
                                                0,
                                                self.origHpr[2]),
                                                startHpr = Point3(myHeadings[index] + self.origHpr[0], downAngle, self.origHpr[2]))
            self.ival.append(goingUp)
            

        self.ival.loop() #globalClock.getFrameTime());
        self.accept('enterGavelZap', self.__touchedGavel)
        self.accept('enterGavelHandleZap', self.__touchedGavelHandle)

    def enterOff(self):
        if self.ival:
            self.ival.finish()

        tempTuple = ToontownGlobals.LawbotBossGavelPosHprs[self.index]
        self.nodePath.setPosHpr(*tempTuple)

    def __touchedGavel(self,entry):
        self.notify.debug("__touchedGavel")
        self.notify.debug("self=%s entry=%s" % (self,entry))

        self.boss.touchedGavel(self, entry)

    def __touchedGavelHandle(self, entry):
        self.notify.debug("__touchedGavelHandle")

        self.boss.touchedGavelHandle(self, entry)

