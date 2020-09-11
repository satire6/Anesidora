#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Sep 2008
#
# Purpose: DistributedParty controls message passing to the AI for parties.
#
#-------------------------------------------------------------------------------
import random
import time
import datetime

from pandac.PandaModules import Vec4, TextNode, CardMaker, NodePath

from direct.distributed import DistributedObject
from direct.task.Task import Task
from direct.gui.DirectGui import DirectLabel
from direct.gui import OnscreenText

from toontown.toonbase import ToontownGlobals
from toontown.parties.PartyInfo import PartyInfo
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from toontown.toon import GMUtils
from toontown.parties import PartyGlobals
from toontown.parties.Decoration import Decoration
import PartyUtils

class DistributedParty(DistributedObject.DistributedObject):
    notify = directNotify.newCategory("DistributedParty")

    def __init__(self,cr):
        assert(self.notify.debug("__init__"))
        DistributedObject.DistributedObject.__init__(self,cr)
        self.partyDoneEvent = "partyDone"
        self.load()
        self.avIdsAtParty = [] #list of toon ids in this party
        # Needed by Party.py
        base.distributedParty = self
        self.titleText = "" 
        
        self.isPartyEnding = False       

    def setPartyState(self, partyState):
        self.isPartyEnding = partyState 
        messenger.send("partyStateChanged", [partyState])       
                
    def getPartyState(self):    
        return self.isPartyEnding

    def setPartyClockInfo(self, x, y, h):
        x = PartyUtils.convertDistanceFromPartyGrid(x, 0)
        y = PartyUtils.convertDistanceFromPartyGrid(y, 1)
        h = PartyUtils.convertDegreesFromPartyGrid(h)
        self.partyClockInfo = (x, y, h)
        self.loadPartyCountdownTimer()

    def setInviteeIds(self, inviteeIds):
        self.inviteeIds = inviteeIds

    def setPartyInfoTuple(self, partyInfoTuple):
        self.partyInfo = PartyInfo(*partyInfoTuple)
        self.loadDecorations()
        allActIds = [x.activityId for x in self.partyInfo.activityList]
        base.partyHasJukebox = (PartyGlobals.ActivityIds.PartyJukebox) in allActIds  \
                               or (PartyGlobals.ActivityIds.PartyJukebox40) in allActIds 
        
        # Fill in a grid showing if a square has an activity or decoration on it
        # Note : This grid is the reverse y of the PartyEditorGrid
        # The difference might be down to where the origin makes the most sense in screen-space vs. world-space.
        self.grid = [[False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, False, False, False],
                     [False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, False, False, False],
                     [False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False],
                     [False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False],
                     [False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False],
                     [False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                     [False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False],
                     [False, False, False, False, True, True, True, True, True, True, True, True, True, False, False, False, False, False],
                     [False, False, False, False, False, True, True, True, True, True, True, True, False, False, False, False, False, False],
                     [False, False, False, False, False, False, True, True, True, True, True, False, False, False, False, False, False, False],
                    ]

        # This uses essentially the same functionality as computeGridYRange and computeGridXRange.
        def fillGrid(x, y, size):
            for i in range(-size[1]/2+1, size[1]/2+1):
                for j in range(-size[0]/2+1, size[0]/2+1):
                    self.grid[i+y][j+x] = False
        
        for activityBase in self.partyInfo.activityList:
            fillGrid(activityBase.x, activityBase.y, PartyGlobals.ActivityInformationDict[activityBase.activityId]["gridsize"])
            
        for decorBase in self.partyInfo.decors:
            fillGrid(decorBase.x, decorBase.y, PartyGlobals.DecorationInformationDict[decorBase.decorId]["gridsize"])
            
        self.loadGrass()

    def setPartyStartedTime(self, startedTime):
        stime = time.strptime(startedTime, "%Y-%m-%d %H:%M:%S")
        self.partyStartedTime = datetime.datetime(
            year=stime.tm_year,
            month=stime.tm_mon,
            day=stime.tm_mday,
            hour=stime.tm_hour,
            minute=stime.tm_min,
            second=stime.tm_sec,
            tzinfo=base.cr.toontownTimeManager.getCurServerDateTime().tzinfo,
        )

    def disable(self):
        self.notify.debug("disable")
        DistributedObject.DistributedObject.disable(self)
        base.localAvatar.chatMgr.chatInputSpeedChat.removeInsidePartiesMenu()

    def delete(self):
        self.notify.debug("delete")
        self.unload()
        if hasattr(base, "distributedParty"):
            del base.distributedParty
        DistributedObject.DistributedObject.delete(self)

    def load(self):
        assert(self.notify.debug("load"))
        Toon.loadMinigameAnims()

        # Load a sign for the activities to copy and use
        self.defaultSignModel = loader.loadModel("phase_13/models/parties/eventSign")
        
        # Load activity icons
        self.activityIconsModel = loader.loadModel("phase_4/models/parties/eventSignIcons")

        # Load party hat for host
        model = loader.loadModel("phase_4/models/parties/partyStickerbook")
        self.partyHat = model.find('**/Stickerbook_PartyIcon')
        self.partyHat.setPos(0.0, 0.1, 2.5)
        self.partyHat.setHpr(0.0, 0.0, -50.0)
        self.partyHat.setScale(4.0)
        self.partyHat.setBillboardAxis()
        self.partyHat.reparentTo(hidden)
        model.removeNode()

        # Load a lever for the activities to copy and use
        self.defaultLeverModel = loader.loadModel('phase_13/models/parties/partyLeverBase')
        self.defaultStickModel = loader.loadModel('phase_13/models/parties/partyLeverStick')

    def loadGrass(self):
        self.grassRoot = NodePath("GrassRoot")
        self.grassRoot.reparentTo(base.cr.playGame.hood.loader.geom)
        grass = loader.loadModel("phase_13/models/parties/grass")
        
        clearPositions = self.getClearSquarePositions()
        
        # Create up to 3 tufts of grass per clear square (avg) or up to PartyGlobals.TuftsOfGrass.
        numTufts = min(len(clearPositions) * 3, PartyGlobals.TuftsOfGrass)
        
        for i in range(numTufts):
            g = grass.copyTo(self.grassRoot)
            pos = random.choice(clearPositions)
            g.setPos(pos[0]+random.randint(-8,8), pos[1]+random.randint(-8,8), 0.0)

    def loadDecorations(self):
        self.decorationsList = []
        for decorBase in self.partyInfo.decors:
            self.decorationsList.append(Decoration(
                PartyGlobals.DecorationIds.getString(decorBase.decorId),
                PartyUtils.convertDistanceFromPartyGrid(decorBase.x, 0),
                PartyUtils.convertDistanceFromPartyGrid(decorBase.y, 1),
                PartyUtils.convertDegreesFromPartyGrid(decorBase.h),
            ))
                
    def unload(self):
        assert(self.notify.debug("unload"))
        if hasattr(self, "decorationsList") and self.decorationsList:
            for decor in self.decorationsList:
                decor.unload()

            del self.decorationsList
        
        self.stopPartyClock()
        self.grassRoot.removeNode()
        del self.grassRoot

        # Only exists with show-debug-party-grid 1.
        if hasattr(self, 'testGrid'):
            self.testGrid.removeNode()
            del self.testGrid
        
        # Ignore all events we might have accepted
        self.ignoreAll()
        
        Toon.unloadMinigameAnims()
        self.partyHat.removeNode()
        del self.partyHat
        if hasattr(base, "partyHasJukebox"):
            del base.partyHasJukebox

    def announceGenerate(self):
        assert(self.notify.debug("announceGenerate()"))
        DistributedObject.DistributedObject.announceGenerate(self)
        self.sendUpdate("avIdEnteredParty", [base.localAvatar.doId])
        # we probably just spent a lot of time loading, so
        # tell globalClock to update the frame timestamp
        globalClock.syncFrameTime()
        self.startPartyClock()
        base.localAvatar.chatMgr.chatInputSpeedChat.addInsidePartiesMenu()
        self.spawnTitleText()
        if config.GetBool('show-debug-party-grid', 0):
            # Debug grid
            self.testGrid = NodePath("test_grid")
            self.testGrid.reparentTo(base.cr.playGame.hood.loader.geom)
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    cm = CardMaker("gridsquare")
                    np = NodePath(cm.generate())
                    np.setScale(12)
                    np.setP(-90.0)
                    np.setPos(PartyUtils.convertDistanceFromPartyGrid(j,0)-6.0, PartyUtils.convertDistanceFromPartyGrid(i,1)-6.0, 0.1)
                    np.reparentTo(self.testGrid)
                    if self.grid[i][j]:
                        np.setColorScale(0.0, 1.0, 0.0, 1.0)
                    else:
                        np.setColorScale(1.0, 0.0, 0.0, 1.0)

    def getClearSquarePos(self):
        """
        Return a tuple of x,y,z of the center of a clear square in the party. Raises an exception
        if there are no clear squares.
        """
        clearPositions = self.getClearSquarePositions()
        
        # A party with no clear squares shouldn't be able to make it through validation. If you get
        # this exception, take a look at DistributedPartyManagerAI.validatePartyAndReturnCost().
        if len(clearPositions) == 0:
            raise StandardError, "Party %s has no empty grid squares." % self.doId
        
        return random.choice(clearPositions)
        
    def getClearSquarePositions(self):
        """
        Return a list of (x,y,z) positions at the center of a clear square in the party.
        """
        clearPositions = []
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x]:
                    pos = (PartyUtils.convertDistanceFromPartyGrid(x,0), PartyUtils.convertDistanceFromPartyGrid(y,1), 0.1)
                    clearPositions.append(pos)
        
        return clearPositions
    
    def startPartyClock(self):
        self.partyClockModel.reparentTo(base.cr.playGame.hood.loader.geom)
        curServerTime = base.cr.toontownTimeManager.getCurServerDateTime()
        # if we are of by even a tiny bit on server time, we could return a negative number
        # and a timedelta(seconds = -1) when normalized gives us a day of -1 and ridiculously large seconds
        timePartyWillEnd = self.partyStartedTime + datetime.timedelta(hours = PartyGlobals.DefaultPartyDuration)
        timeLeftInParty = timePartyWillEnd - curServerTime
        if curServerTime < timePartyWillEnd:
            self.secondsLeftInParty = timeLeftInParty.seconds
        else:
            self.secondsLeftInParty = 0
        taskMgr.doMethodLater(0.5, self.partyClockTask, "UpdatePartyClock")
        self.partyClockSignFront = self.partyClockModel.find("**/signFrontText_locator")
        self.partyClockSignBack = self.partyClockModel.find("**/signBackText_locator")
        self.attachHostNameToSign(self.partyClockSignFront)
        self.attachHostNameToSign(self.partyClockSignBack)

    def attachHostNameToSign(self, locator):
        if (self.hostName == ""):
            # don't bother putting an empty string up
            return
        nameText = TextNode('nameText')
        nameText.setCardAsMargin(0.1, 0.1, 0.1, 0.1)
        nameText.setCardDecal(True)
        nameText.setCardColor(1.0, 1.0, 1.0, 0.0)

        r = 232.0 /255.0 #self.randomGenerator.random()
        g = 169.0 / 255.0  #self.randomGenerator.random()
        b = 23.0 / 255.0 #self.randomGenerator.random()
        nameText.setTextColor(r,g,b,1)
        nameText.setAlign(nameText.ACenter)
        nameText.setFont(ToontownGlobals.getBuildingNametagFont())
        nameText.setShadowColor(0, 0, 0, 1)
        nameText.setBin('fixed')
        if TTLocalizer.BuildingNametagShadow:
            nameText.setShadow(*TTLocalizer.BuildingNametagShadow)
        nameWordWrap = 11.0
        nameText.setWordwrap(nameWordWrap)
        scaleMult = 0.48
        #xScale = 1.0 * scaleMult
        #numLines = 0
        
        houseName = self.hostName

        nameText.setText(houseName)
        #self.nameText = nameText

        # Since the text is wordwrapped, it may flow over more
        # than one line.  Try to adjust the scale and position of
        # the sign accordingly.
        #textHeight = nameText.getHeight() - 2
        textWidth = nameText.getWidth()
        xScale = 1.0 * scaleMult
        if textWidth > nameWordWrap:
            xScale = nameWordWrap / textWidth * scaleMult

        sign_origin = locator # self.house.find("**/sign_origin")
        #pos = sign_origin.getPos()
        #sign_origin.setPosHpr(pos[0],pos[1],pos[2]+.15*textHeight,90,0,0)
        namePlate = sign_origin.attachNewNode(nameText)
        namePlate.setDepthWrite(0)
        namePlate.setPos(0,0,0)
        namePlate.setScale(xScale)

    def stopPartyClock(self):
        self.partyClockModel.removeNode()
        taskMgr.remove("UpdatePartyClock")
        
    def partyClockTask(self, task):
        self.secondsLeftInParty -= 0.5
        if self.secondsLeftInParty < 0:
            self.frontTimer["minute"]["text"] = "--"
            self.backTimer["minute"]["text"] = "--"
            self.frontTimer["second"]["text"] = "--"
            self.backTimer["second"]["text"] = "--"            
            return
        if self.frontTimer["colon"].isStashed():
            self.frontTimer["colon"].unstash()
            self.backTimer["colon"].unstash()
        else:
            self.frontTimer["colon"].stash()
            self.backTimer["colon"].stash()

        minutesLeft = int(int(self.secondsLeftInParty/60)%60)
        if minutesLeft < 10:
            minutesLeft = "0%d"%minutesLeft
        else:
            minutesLeft = "%d"%minutesLeft
        secondsLeft = int(self.secondsLeftInParty%60)
        if secondsLeft < 10:
            secondsLeft = "0%d"%secondsLeft
        else:
            secondsLeft = "%d"%secondsLeft
        self.frontTimer["minute"]["text"] = minutesLeft
        self.backTimer["minute"]["text"] = minutesLeft
        self.frontTimer["second"]["text"] = secondsLeft
        self.backTimer["second"]["text"] = secondsLeft
        taskMgr.doMethodLater(0.5, self.partyClockTask, "UpdatePartyClock")
        if self.secondsLeftInParty != int(self.secondsLeftInParty):
            self.partyClockModel.find("**/middleRotateFront_grp").setR(-6.0*(self.secondsLeftInParty%60))
            self.partyClockModel.find("**/middleRotateBack_grp").setR(6.0*(self.secondsLeftInParty%60))

    def getAvIdsAtParty(self):
        return self.avIdsAtParty
        
    def setAvIdsAtParty(self, avIdsAtParty):
        assert(self.notify.debug("setAvIdsAtParty : avIdsAtParty = %s" % avIdsAtParty))
        self.avIdsAtParty = avIdsAtParty

    def loadPartyCountdownTimer(self):
        self.partyClockModel = loader.loadModel('phase_13/models/parties/partyClock')
        self.partyClockModel.setPos(self.partyClockInfo[0], self.partyClockInfo[1], 0.0)
        self.partyClockModel.setH(self.partyClockInfo[2])
        self.partyClockModel.reparentTo(base.cr.playGame.hood.loader.geom)
        #self.partyClockModel.find("**/frontText_locator").setPos(0.0, -1.1, 13.7)
        #self.partyClockModel.find("**/backText_locator").setPos(0.0, 0.633, 13.7)
        self.partyClockModel.find("**/frontText_locator").setY(-1.1)
        self.partyClockModel.find("**/backText_locator").setY(0.633)
        self.frontTimer = self.getTimer(self.partyClockModel.find("**/frontText_locator"))
        base.frontTimerLoc = self.partyClockModel.find("**/frontText_locator")
        base.backTimerLoc = self.partyClockModel.find("**/backText_locator")
        self.backTimer = self.getTimer(self.partyClockModel.find("**/backText_locator"))
        self.partyClockModel.stash()

    def getTimer(self, parent):
        timeFont = ToontownGlobals.getMinnieFont()
        timer = {}
        timer["minute"] = DirectLabel(
            parent = parent,
            pos = (-1.2, TTLocalizer.DPpartyCountdownClockMinutesPosY, 0.0),
            relief = None,
            text = '59',
            text_align = TextNode.ACenter,
            text_font = timeFont,
            text_fg = (0.7, 0.3, 0.3, 1.0),
            scale = TTLocalizer.DPpartyCountdownClockMinutesScale,
        )
        timer["colon"] = DirectLabel(
            parent = parent,
            pos = (0, TTLocalizer.DPpartyCountdownClockColonPosY, 0.0),
            relief = None,
            text = ':',
            text_align = TextNode.ACenter,
            text_font = timeFont,
            text_fg = (0.7, 0.3, 0.3, 1.0),
            scale = TTLocalizer.DPpartyCountdownClockColonScale,
        )
        timer["second"] = DirectLabel(
            parent = parent,
            relief = None,
            pos = (1.2, TTLocalizer.DPpartyCountdownClockSecondPosY, 0.0),
            text = '14',
            text_align = TextNode.ACenter,
            text_font = timeFont,
            text_fg = (0.7, 0.3, 0.3, 1.0),
            scale = TTLocalizer.DPpartyCountdownClockSecondScale,
        )
        timer["textLabel"] = DirectLabel(
            parent = parent,
            relief = None,
            pos = (0.0, 0.0, 1.15),
            text = TTLocalizer.PartyCountdownClockText,
            text_font = timeFont,
            text_fg = (0.7, 0.3, 0.3, 1.0),
            scale = TTLocalizer.DPpartyCountdownClockTextScale,
        )
        return timer

    def setHostName(self, hostName):
        """Handle AI telling us the hostname."""
        self.hostName = hostName
        
        if GMUtils.testGMIdentity(self.hostName):
            self.hostName = GMUtils.handleGMName(self.hostName)
            
        # it is possible to get here initially without the model being loaded yet,
        # hence the hasattr self
        if hasattr(self, "partyClockSignFront"):
            self.attachHostNameToSign(self.partyClockSignFront)
        if hasattr(self, "partyClockSignBack"):
            self.attachHostNameToSign(self.partyClockSignBack)

    def spawnTitleText(self):
        """Spawn the title text."""
        if not self.hostName:
            # potentially we don't have the host name yet
            return
        
        partyText = TTLocalizer.PartyTitleText % TTLocalizer.GetPossesive(self.hostName)
        self.doSpawnTitleText(partyText)

    def doSpawnTitleText(self, text):
        self.titleColor = (1.0, 0.5, 0.4, 1.0)
        self.titleText = OnscreenText.OnscreenText(
            text,
            fg = self.titleColor,
            font = ToontownGlobals.getSignFont(),
            pos = (0,-0.5),
            scale = 0.16,
            drawOrder = 0,
            mayChange = 1,
            wordwrap = 16
            )        
        
        self.titleText.setText(text)
        self.titleText.show()
        self.titleText.setColor(Vec4(*self.titleColor))
        self.titleText.clearColorScale()
        self.titleText.setFg(self.titleColor)
        seq = Task.sequence(
            # HACK! Let a pause go by to cover the loading pause
            # This tricks the taskMgr
            Task.pause(0.1),
            Task.pause(6.0),
            self.titleText.lerpColorScale(
            Vec4(1.0, 1.0, 1.0, 1.0),
            Vec4(1.0, 1.0, 1.0, 0.0),
            0.5),
            Task(self.hideTitleTextTask))
        taskMgr.add(seq, "titleText")

    def hideTitleTextTask(self, task):
        assert(self.notify.debug("hideTitleTextTask()"))
        self.titleText.hide()
        return Task.done

    def hideTitleText(self):
        """
        This gets called from the town and safe zone to cleanup
        the title text if we leave walk mode for instance
        """
        assert(self.notify.debug("hideTitleText()"))
        if self.titleText:
            self.titleText.hide()
