##########################################################################
# Module: DistributedLeaderBoard.py
# Purpose:
# Date: 6/24/05
# Author: sabrina (sabrina@schellgames.com)
##########################################################################

from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPTimer
from toontown.toonbase import TTLocalizer
from toontown.racing import KartShopGlobals

#added
from toontown.toonbase.ToonBaseGlobal import *
from pandac.PandaModules import *
from toontown.toonbase.ToontownGlobals import *
import random
import cPickle



class DistributedLeaderBoard(DistributedObject.DistributedObject):
    '''The leader board class handles the display of player rankings.

    Leader Board class was created to showcase race records in Toontown Kart racing
    '''


    notify = DirectNotifyGlobal.directNotify.newCategory('DisributedLeaderBoard')
    #notify.setInfo(True)
    #notify.setDebug(True)

    def __init__(self,  cr):
        '''
        Setup the Leader Board.
        '''
        self.notify.debug("__init__: initialization of local leaderboard")
        DistributedObject.DistributedObject.__init__(self, cr)
        self.corner = 0
        self.length = 0
        self.width = 0
        self.updateCount = 0
        self.board = None #basically the root node that takes on pos/hpr of leader board model
        self.surface = None #one under the root.. all text elements are parented to it

    def generateInit(self):
        DistributedObject.DistributedObject.generateInit(self)
        self.board = NodePath(self.uniqueName('LeaderBoard') )

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

        self.buildListParts()
        

    def announceGenerate(self):
        """
        """
        DistributedObject.DistributedObject.announceGenerate(self)
        self.board.reparentTo(render)
        
        self.accept("decorator-holiday-%d-ending" % ToontownGlobals.CRASHED_LEADERBOARD, self.showLists)
        self.accept("decorator-holiday-%d-starting" % ToontownGlobals.CRASHED_LEADERBOARD, self.hideLists)

        newsManager = base.cr.newsManager
        if newsManager:
            if ToontownGlobals.CRASHED_LEADERBOARD in newsManager.holidayIdList :
                self.hideLists()

    def showLists(self):
        """Show the top ten lists."""
        self.board.show()

    def hideLists(self):
        """Hide the top ten lists."""
        self.board.hide()


    def setPosHpr(self, x, y, z, h, p, r):
        """
        """
        assert self.notify.debugStateCall(self)
        self.surface.setPosHpr(x, y, z, h, p, r)

    def setDisplay(self, pData):
        # This message is sent from the AI when the leaderboard data should change
        # so the assumption is we should update the display afterwards
        self.notify.debug("setDisplay: changing leaderboard text on local side")
        trackName, recordTitle, scores = cPickle.loads(pData)
        self.display(trackName, recordTitle, scores)

    def buildListParts(self):

        self.surface = self.board.attachNewNode("surface")

        z = 7.7
        dz = .4
        x = -3.7#-3.8

        #build track title row
        row, trackName = self.buildTrackRow()
        self.trackNameNode = trackName
        row.reparentTo(self.surface)
        row.setPos(0, 1.6, z)
        #row.setH(-90)
        z = 7.3

        #build race title row
        row, self.titleTextNode = self.buildTitleRow()
        row.reparentTo(self.surface)
        row.setPos(0, 1.6, z)
        #row.setH(-90)

        zListTop = 6.9
        z = zListTop

        # Store the text nodes so we can setText() them later with
        # score updates
        self.nameTextNodes = []
        self.timeTextNodes = []

        # Create blank entries for each row in the leaderboard
        for i in range(10):

            row, nameText, timeText, placeText = self.buildLeaderRow()
            self.nameTextNodes.append(nameText)
            placeText.setText(str(len(self.nameTextNodes))+".")
            self.timeTextNodes.append(timeText)
            row.reparentTo(self.surface)

            #row.setH(-90)
            if len(self.nameTextNodes)== 6:
                        z = zListTop
                        x =  .35#.1

            row.setX(x)

            row.setZ(z)
            #ow.setY(1.4)
            row.setY(1.6)
            z -= dz

        # Now flatten out all of those transforms.
        self.surface.flattenLight()


    def display(self, pTrackTitle="Track Title", pPeriodTitle="Period Title", pLeaderList=[]):
        # Refresh the data and graphics on the leaderboard with our new information

        #update the race title
        self.titleTextNode.setText(pPeriodTitle)
        self.trackNameNode.setText(pTrackTitle)

        self.updateCount += 1

        # Fill in the names, scores
        # We may not have the max number of leaderNames
        for i in range(10):
            if i > len(pLeaderList):
                self.nameTextNodes[i].setText("-")
                self.timeTextNodes[i].setText("-")
            else:
                name = pLeaderList[i][1]
                time = pLeaderList[i][0]
                secs, hundredths = divmod(time, 1)
                min, sec = divmod(secs, 60)
                # trunc the name to 22 chars
                self.nameTextNodes[i].setText(name[: 22])
                self.timeTextNodes[i].setText("%02d:%02d:%02d" % (min, sec, hundredths * 100))


    def buildTitleRow(self):
        # Build the title row on the leaderboard
        row = hidden.attachNewNode("TitleRow")
        nameText = TextNode("titleRow")
        nameText.setFont(ToontownGlobals.getSignFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0.3, 0.75, 0.6, 1)
        nameText.setText("Score Title")
        #nameText.setGlyphScale(.4)
        namePath = row.attachNewNode(nameText)
        namePath.setScale(TTLocalizer.DLBtitleRowScale)
        namePath.setDepthWrite(0)

        return row, nameText

    def buildTrackRow(self):
        # Build the title row on the leaderboard
        row = hidden.attachNewNode("trackRow")
        nameText = TextNode("trackRow")
        nameText.setFont(ToontownGlobals.getSignFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0.5, 0.75, 0.7, 1)
        nameText.setText("Track Title")
        #nameText.setGlyphScale(.75)
        namePath = row.attachNewNode(nameText)
        namePath.setScale(.55)
        namePath.setDepthWrite(0)

        return row, nameText

    def buildLeaderRow(self):
        # Build a single row on the leaderboard
        row = hidden.attachNewNode("leaderRow")

        # Text node for the toon name
        nameText = TextNode("nameText")
        nameText.setFont(ToontownGlobals.getToonFont())
        nameText.setAlign(TextNode.ALeft)
        nameText.setTextColor(0.125, 0, 0.5, 1)
        #nameText.setGlyphScale(.23)
        nameText.setText("-")
        namePath = row.attachNewNode(nameText)
        namePath.setPos(1.1, 0, 0)
        namePath.setScale(.23)
        namePath.setDepthWrite(0)

        # Text node for the score
        timeText = TextNode("timeText")
        timeText.setFont(ToontownGlobals.getToonFont())
        timeText.setAlign(TextNode.ARight)
        timeText.setTextColor(0, 0, 0, 1)
        timeText.setText("-")
        #timeText.setGlyphScale(.23)
        timePath = row.attachNewNode(timeText)
        timePath.setPos(1.0, 0, 0)
        timePath.setScale(.23)
        timePath.setDepthWrite(0)

        #Text node for the place numbers
        placeText = TextNode("placeText")
        placeText.setFont(ToontownGlobals.getSignFont())
        placeText.setAlign(TextNode.ARight)
        placeText.setTextColor(1, 1, 0.1, 1)
        placeText.setText("-")
        #placeText.setGlyphScale(.23)
        placePath = row.attachNewNode(placeText)
        placePath.setPos(-0.1, 0, -0.05)
        #placePath.setScale(.23)
        placePath.setScale(.3)
        placePath.setDepthWrite(0)

        return row, nameText, timeText, placeText

    def delete(self):
        '''
        Clean up myself
        '''
        self.notify.debug("delete: deleting local leaderboard")
        self.ignoreAll()
        self.board.removeNode()
        DistributedObject.DistributedObject.delete(self)


