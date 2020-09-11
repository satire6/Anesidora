from pandac.PandaModules import NodePath
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from toontown.estate import DistributedStatuary
from toontown.estate import GardenGlobals

class DistributedChangingStatuary(DistributedStatuary.DistributedStatuary):
    """
    Regular statues and toon statues don't change once planted.
    This class does, initially created for the melting snowman
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChangingStatuary')

    def __init__(self, cr):
        """Construct for our changing statuary."""
        self.notify.debug('constructing DistributedChangingStatuary')
        DistributedStatuary.DistributedStatuary.__init__(self, cr)

    def loadModel(self):
        """Load the assets, hide the other parts that don't match our growth level."""
        self.rotateNode = self.plantPath.attachNewNode('rotate')
        self.model = loader.loadModel(self.modelPath)
        #import pdb; pdb.set_trace()
        colNode = self.model.find("**/+CollisionNode")
        if not colNode.isEmpty():
            score, multiplier = ToontownGlobals.PinballScoring[ToontownGlobals.PinballStatuary]
            if self.pinballScore:
                score = self.pinballScore[0]
                multiplier = self.pinballScore[1]
            scoreNodePath = NodePath("statuary-%d-%d" % (score, multiplier))
            colNode.setName('statuaryCol')
            scoreNodePath.reparentTo( colNode.getParent())
            colNode.reparentTo(scoreNodePath)
        self.model.setScale(self.worldScale)
        self.model.reparentTo(self.rotateNode)

        self.hideParts()
        self.stick2Ground()

    def hideParts(self):
        """Hide the other parts of the statue that doesn't match our growth level."""
        stage = -1
        attrib = GardenGlobals.PlantAttributes[self.typeIndex]
        growthThresholds = attrib['growthThresholds']
        # figure out which stage model we should use
        for index, threshold in enumerate(growthThresholds):
            if self.growthLevel < threshold:
                stage = index
                break
        if stage == -1:
            stage = len(growthThresholds)
        self.notify.debug('growth Stage=%d' % stage)
        # we know the right stage, hide the others
        for index in xrange(len(growthThresholds) +1):
            if index != stage:
                partName = '**/growthStage_%d' % index
                self.notify.debug('trying to remove %s' % partName)
                hideThis = self.model.find(partName)
                if not hideThis.isEmpty():
                    hideThis.removeNode()
                
    def setupShadow(self):
        # set up the shadow
        DistributedStatuary.DistributedStatuary.setupShadow(self)
        # hide the shadow as it looks wrong on the snowman
        self.hideShadow()

    def setGrowthLevel(self, growthLevel):
        """Handle AI telling us our growth level."""
        # it starts at 0 then goes all the way up to the max 127
        assert self.notify.debug( "growth %d" % growthLevel)

        self.growthLevel = growthLevel
        if self.model:
            # check to see if there is a model-change
            # reload the model
            self.model.removeNode()
            self.loadModel()
