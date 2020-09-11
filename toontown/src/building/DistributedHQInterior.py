from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *

import random
from direct.task.Task import Task
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
import ToonInteriorColors
import cPickle
from toontown.toonbase import TTLocalizer

class DistributedHQInterior(DistributedObject.DistributedObject):
    if __debug__:
        notify = DirectNotifyGlobal.directNotify.newCategory(
            'DistributedHQInterior')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.dnaStore=cr.playGame.dnaStore
        # These are stored in sorted order, highest score first
        self.leaderAvIds = []
        self.leaderNames = []
        self.leaderScores = []
        self.numLeaders = 10
        self.tutorial = 0

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.interior = loader.loadModel('phase_3.5/models/modules/HQ_interior')
        self.interior.reparentTo(render)
        # hide these props until we intergrate them fully
        self.interior.find("**/cream").hide()
        self.interior.find("**/crashed_piano").hide()
        self.buildLeaderBoard()

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setupDoors()
        # Flatten everything
        self.interior.flattenMedium()
        # Then put the leaderboard under
        # We do not want the leaderboard flattened because we need to update it
        # Also, throw a decal transition on
        emptyBoard = self.interior.find("**/empty_board")
        # emptyBoard.getChild(0).node().setEffect(DecalEffect.make())
        self.leaderBoard.reparentTo(emptyBoard.getChild(0))

    def setTutorial(self, flag):
        if self.tutorial == flag:
            return
        else:
            self.tutorial = flag
        if self.tutorial:
            # don't show the scope in the tutorial building for viz
            self.interior.find("**/periscope").hide()
            self.interior.find("**/speakers").hide()
        else:
            # show the scope in the tutorial building for viz
            self.interior.find("**/periscope").show()
            self.interior.find("**/speakers").show()
        
    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def buildLeaderBoard(self):
        # Create the models and layout the elements to create
        # the leaderboard. This gets called once on load
        # TODO: do we want avatar dna / faces here?
        self.leaderBoard = hidden.attachNewNode('leaderBoard')
        # Away from the wall by 0.1 since the decal does not seem to be working
        self.leaderBoard.setPosHprScale(0.1,0,4.5,90,0,0,0.9,0.9,0.9)
        z = 0
        row = self.buildTitleRow()
        row.reparentTo(self.leaderBoard)
        row.setPos(0,0,z)
        z -= 1
        # Store the text nodes so we can setText() them later with
        # score updates
        self.nameTextNodes = []
        self.scoreTextNodes = []
        # Store the trophy stars next to each name because they need
        # to change with score updates too
        self.trophyStars = []

        # Create blank entries for each row in the leaderboard
        for i in range(self.numLeaders):
            row, nameText, scoreText, trophyStar = self.buildLeaderRow()
            self.nameTextNodes.append(nameText)
            self.scoreTextNodes.append(scoreText)
            self.trophyStars.append(trophyStar)
            row.reparentTo(self.leaderBoard)
            row.setPos(0,0,z)
            z -= 1
            
    def updateLeaderBoard(self):
        # Refresh the data and graphics on the leaderboard with our new information
        # Kill any existing star tasks
        taskMgr.remove(self.uniqueName("starSpinHQ"))
        # Fill in the names, scores, and stars we have
        # We may not have the max number of leaderNames
        for i in range(len(self.leaderNames)):
            name = self.leaderNames[i]
            score = self.leaderScores[i]
            self.nameTextNodes[i].setText(name)
            self.scoreTextNodes[i].setText(str(score))
            self.updateTrophyStar(self.trophyStars[i], score)
        # Fill in the rest with empty looking strings and hide the stars
        for i in range(len(self.leaderNames), self.numLeaders):
            self.nameTextNodes[i].setText("-")
            self.scoreTextNodes[i].setText("-")
            self.trophyStars[i].hide()

    def buildTitleRow(self):
        # Build the title row on the leaderboard
        row = hidden.attachNewNode("leaderRow")        
        nameText = TextNode("titleRow")
        nameText.setFont(ToontownGlobals.getSignFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0.5, 0.75, 0.7, 1)
        nameText.setText(TTLocalizer.LeaderboardTitle)
        namePath = row.attachNewNode(nameText)
        # Centered
        namePath.setPos(0,0,0)
        return row

    def buildLeaderRow(self):
        # Build a single row on the leaderboard
        row = hidden.attachNewNode("leaderRow")
        
        # Text node for the toon name
        nameText = TextNode("nameText")
        nameText.setFont(ToontownGlobals.getToonFont())
        nameText.setAlign(TextNode.ALeft)
        nameText.setTextColor(1, 1, 1, 0.7)
        nameText.setText("-")
        namePath = row.attachNewNode(nameText)
        namePath.setPos(*TTLocalizer.DHtoonNamePos)
        namePath.setScale(TTLocalizer.DHtoonName)

        # Text node for the score
        scoreText = TextNode("scoreText")
        scoreText.setFont(ToontownGlobals.getToonFont())
        scoreText.setAlign(TextNode.ARight)
        scoreText.setTextColor(1, 1, 0.1, 0.7)
        scoreText.setText("-")
        scorePath = row.attachNewNode(scoreText)
        scorePath.setPos(*TTLocalizer.DHscorePos)

        # Put a star on the row, just like over the Toon heads
        trophyStar = self.buildTrophyStar()
        trophyStar.reparentTo(row)

        return row, nameText, scoreText, trophyStar

    def setLeaderBoard(self, leaderData):
        # This message is sent from the AI when the leaderboard is updated
        # We assume that because we got this message, something must have changed,
        # or we are in our generate
        avIds, names, scores = cPickle.loads(leaderData)
        # Note, these lists are in order, highest score first
        self.notify.debug("setLeaderBoard: avIds: %s, names: %s, scores: %s" % (avIds, names, scores))
        self.leaderAvIds = avIds
        self.leaderNames = names
        self.leaderScores = scores
        # Refresh the display
        self.updateLeaderBoard()

    def chooseDoor(self):
        # I copy/pasted this door string choosing code from
        # DistributedToonInterior.
        # Door:
        doorModelName="door_double_round_ul" # hack  zzzzzzz
        # Switch leaning of the door:
        if doorModelName[-1:] == "r":
            doorModelName=doorModelName[:-1]+"l"
        else:
            doorModelName=doorModelName[:-1]+"r"
        door=self.dnaStore.findNode(doorModelName)
        return door

    def setupDoors(self):
        # Set up random generator
        self.randomGenerator = random.Random()
        self.randomGenerator.seed(self.zoneId)

        # Pick a color list. For now, I've picked ToontownCentral.
        # Maybe there will be a special color scheme for HQ interiors
        self.colors = ToonInteriorColors.colors[ToontownCentral]

        # Pick a door model
        door = self.chooseDoor()
        # Find the door origins
        doorOrigins = render.findAllMatches("**/door_origin*")
        numDoorOrigins = doorOrigins.getNumPaths()
        for npIndex in range(numDoorOrigins):
            doorOrigin = doorOrigins[npIndex]
            doorOriginNPName = doorOrigin.getName()
            doorOriginIndexStr = doorOriginNPName[len("door_origin_"):]
            newNode = ModelNode("door_" + doorOriginIndexStr)
            newNodePath = NodePath(newNode)
            newNodePath.reparentTo(self.interior)
            doorNP = door.copyTo(newNodePath)
            assert(not doorNP.isEmpty())
            assert(not doorOrigin.isEmpty())
            doorOrigin.setScale(0.8, 0.8, 0.8)
            doorOrigin.setPos(doorOrigin, 0, -0.025, 0)
            doorColor = self.randomGenerator.choice(self.colors["TI_door"])
            triggerId = str(self.block) + "_" + doorOriginIndexStr
            DNADoor.setupDoor(doorNP,
                              newNodePath, doorOrigin,
                              self.dnaStore, triggerId,
                              doorColor)
            doorFrame = doorNP.find("door_*_flat")
            #doorFrame.wrtReparentTo(self.interior)
            doorFrame.setColor(doorColor)

        del self.dnaStore
        del self.randomGenerator
                                      
    def disable(self):
        self.leaderBoard.removeNode()
        del self.leaderBoard
        self.interior.removeNode()
        del self.interior
        del self.nameTextNodes
        del self.scoreTextNodes
        del self.trophyStars
        taskMgr.remove(self.uniqueName("starSpinHQ"))
        DistributedObject.DistributedObject.disable(self)

    # TODO: perhaps the star code should be abstracted out and shared
    # between the leaderboard and the Toons.

    def buildTrophyStar(self):
        trophyStar = loader.loadModel('phase_3.5/models/gui/name_star')
        trophyStar.hide()
        trophyStar.setPos(*TTLocalizer.DHtrophyPos)
        return trophyStar

    def updateTrophyStar(self, trophyStar, score):
        # Customize the star just like the ones over Toon's heads
        scale = 0.8
        if score >= ToontownGlobals.TrophyStarLevels[4]:
            # A gold star!
            trophyStar.show()
            trophyStar.setScale(scale)
            trophyStar.setColor(ToontownGlobals.TrophyStarColors[4])
            if score >= ToontownGlobals.TrophyStarLevels[5]:
                # Spinning!
                task = taskMgr.add(self.__starSpin, self.uniqueName("starSpinHQ"))
                task.trophyStarSpeed = 15
                task.trophyStar = trophyStar

        elif score >= ToontownGlobals.TrophyStarLevels[2]:
            # A silver star!
            trophyStar.show()
            trophyStar.setScale(0.75 * scale)
            trophyStar.setColor(ToontownGlobals.TrophyStarColors[2])
            # Spinning!
            if score >= ToontownGlobals.TrophyStarLevels[3]:
                task = taskMgr.add(self.__starSpin, self.uniqueName("starSpinHQ"))
                task.trophyStarSpeed = 10
                task.trophyStar = trophyStar

        elif score >= ToontownGlobals.TrophyStarLevels[0]:
            # A bronze star.
            trophyStar.show()
            trophyStar.setScale(0.75 * scale)
            trophyStar.setColor(ToontownGlobals.TrophyStarColors[0])
            # Spinning!
            if score >= ToontownGlobals.TrophyStarLevels[1]:
                task = taskMgr.add(self.__starSpin, self.uniqueName("starSpinHQ"))
                task.trophyStarSpeed = 8
                task.trophyStar = trophyStar

        else:
            trophyStar.hide()

    def __starSpin(self, task):
        # The little star spin task
        now = globalClock.getFrameTime()
        r = now * task.trophyStarSpeed % 360.0
        task.trophyStar.setR(r)
        return Task.cont
        
"""
from toontown.makeatoon import NameGenerator
ng = NameGenerator.NameGenerator()
data = [[0,1,2,3,4,5,6,7,8,9],[ng.randomName(), ng.randomName(), ng.randomName(), ng.randomName(), ng.randomName(), ng.randomName(), ng.randomName(), ng.randomName(), ng.randomName(), ng.randomName()], [35,26,18,15,14,10,6,4,3,2]]
hq.setLeaderBoard(cPickle.dumps(data))
"""
