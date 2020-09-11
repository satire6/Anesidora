#################################################################
# class: BingoCardGui.py
# Purpose: Provide a base layout of the bingo card GUI which can
#          be used in a variety of games.
#################################################################

#################################################################
# Direct Specific Modules
#################################################################
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task
import random

#################################################################
# Toontown Specific Modules
#################################################################
from toontown.fishing import BingoCardCell
from toontown.fishing import BingoGlobals
from toontown.fishing import FishBase
from toontown.fishing import FishGlobals
from direct.showbase import RandomNumGen
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownTimer
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TTDialog

#################################################################
# Globals and Constants
#################################################################
BG = BingoGlobals

class BingoCardGui(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('BingoCardGui')
    #notify.setDebug(True)

    #################################################################
    # Method: __init__
    # Purpose: This method provides initial construction of the Card.
    #          It determines if the card is of a valid size, and
    #          that it is square. Checking of a non-square card is
    #          impossible for diagonal cases. In addition, it
    #          initializes the DirectFrame and BingoCardBase classes
    #          from which it is derived.
    # Input: parent - The parent that the card.
    #        cardSize - The size of the card rowSize x colSize.
    #        rowSize - The number of rows in the card.
    #        colSize - The number of cols in the card.
    #        **kw - OptionDefs for the DirectFrame
    # Output: None
    #################################################################
    def __init__( self, parent=aspect2d, **kw):
        self.notify.debug("Bingo card initialized")
        self.model = loader.loadModel("phase_4/models/gui/FishBingo")
        optiondefs = (
            ('relief',                                    None, None),
            ('state',                                   DGG.NORMAL, None),
            ('image',                  self.model.find('**/g'), None),
            ('image_color',                     BG.getColor(0), None),
            ('image_scale',                  BG.CardImageScale, None),
            ('image_hpr',                     (0.0, 90.0, 0.0), None),
            ('pos',                            BG.CardPosition, None)
            )

        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(BingoCardGui)

        # Class Member Variable Definitions.
        self.game = None
        self.cellGuiList = []
        self.parent = parent

        self.load()
        self.hide()

        self.taskNameFlashFish = "flashMatchingFishTask"

    def show(self):
        DirectFrame.show(self)
        if self.game and self.game.checkForBingo():
            self.__indicateBingo(True)
            if self.game.getGameType() == BG.BLOCKOUT_CARD:
                self.showJackpot()

    def hide(self):
        self.hideTutorial()
        self.hideJackpot()
        DirectFrame.hide(self)

    #################################################################
    # Method: loadTimer
    # Purpose: This method instantiates a game timer, positions it
    #          and scales it according to the CardImageScale.
    # Input: None
    # Output: None
    #################################################################
    def loadGameTimer(self):
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self)
        self.timer.setScale(0.17)
        self.timer.setPos(0.24, 0, -0.18)

    #################################################################
    # Method: resetTimer
    # Purpose: This method reset the Game Timer to Zero.
    # Input: None
    # Output: None
    #################################################################
    def resetGameTimer(self):
        self.timer.reset()

    #################################################################
    # Method: startCountdown
    # Purpose: Starts the Countdown of the game timer.
    # Input: time - the amount of time to countdown from in secs
    # Output: None
    #################################################################
    def startGameCountdown(self, time):
        self.notify.debug("startGameCountdown: %s" % time)
        self.timer.countdown(time)

    #################################################################
    # Method: startNextGameCountdown
    # Purpose: Starts the Countdown of the intermission and
    #          timeout timer.
    # Input: time - the amount of time to countdown from in secs
    # Output: None
    #################################################################
    def startNextGameCountdown(self, time):
        self.nextGameTimer.countdown(time)

    #################################################################
    # Method: hideNextGameTimer
    # Purpose: This method hides the next game timer. It is called
    #          when the timer is no longer in use.
    # Input: None
    # Output: None
    #################################################################
    def hideNextGameTimer(self):
        self.nextGame['text'] = ''
        self.nextGame.hide()

    #################################################################
    # Method: showNextGameTimer
    # Purpose: This method shows the next game timer. It is called
    #          when the timer is needed once more.
    # Input: text - text to display with the timer.
    # Output: None
    #################################################################
    def showNextGameTimer(self, text):
        self.nextGame['text'] = text
        self.nextGame.show()

    #################################################################
    # Method: resetNextGameTimer
    # Purpose: This method resets the next game timer to zero.
    # Input: None
    # Output: None
    #################################################################
    def resetNextGameTimer(self):
        self.nextGameTimer.reset()

    #################################################################
    # Method: stopNextGameTimer
    # Purpose: This method stops the next game timer when it is no
    #          longer needed.
    # Input: None
    # Output: None
    #################################################################
    def stopNextGameTimer(self):
        self.nextGameTimer.stop()

    #################################################################
    # Method: setNextGameText
    # Purpose: This method sets the text to display for the
    #          intermission or timeout period.
    # Input: text - text to display with the timer.
    # Output: None
    #################################################################
    def setNextGameText(self, text):
        self.nextGame['text'] = text

    #################################################################
    # Method: setJackpotText
    # Purpose: This method sets the text to display for the
    #          jackpot.
    # Input: text - text to display with the timer.
    # Output: None
    #################################################################
    def setJackpotText(self, text):
        if text:
            str = TTLocalizer.FishBingoJackpotWin % text
        else:
            str = ""

        self.jpText['text'] = str

    #################################################################
    # Method: resetGameTypeText
    # Purpose: This method resets the Game Type text to ''.
    # Input: text - text to display with the timer.
    # Output: None
    #################################################################
    def resetGameTypeText(self):
        self.gameType['text'] = ''
        self.gameType.setFrameSize()
        self.gameType.hide()

    #################################################################
    # Method: loadNextGameTimer
    # Purpose: This method instantiates a game timer, hides the image
    #          of the timer, and positions it relative to the card
    #          so that when a timeout has occured, the countdown will
    #          be viewed on the card.
    # Input: None
    # Output: None
    #################################################################
    def loadNextGameTimer(self):
        self.nextGame = DirectLabel(parent= self,
                                    relief = None,
                                    text = '',
                                    text_font = ToontownGlobals.getSignFont(),
                                    text_scale = TTLocalizer.BCGnextGame*BG.CardImageScale[2],
                                    text_fg = (1.0, 1.0, 1.0, 1),
                                    pos = (BG.GridXOffset, 0, 4*BG.CardImageScale[2]))

        self.nextGameTimer = ToontownTimer.ToontownTimer()
        self.nextGameTimer.reparentTo(self.nextGame)
        self.nextGameTimer.setPos(0, 0, -5*BG.CardImageScale[2])
        self.nextGameTimer.setProp('image', None)
        self.nextGameTimer.setProp('text_font', ToontownGlobals.getSignFont())
        self.nextGameTimer.setProp('text_scale', 0.2*BG.CardImageScale[2])
        self.nextGameTimer.setFontColor(Vec4(1.0, 1.0, 1.0, 1))


    #################################################################
    # Method: setGameOver
    # Purpose: This method sets the gameOver text to the appropriate
    #          string.
    # Input: text - string of text that should be updated.
    # Output: None
    #################################################################
    def setGameOver(self, text):
        self.gameOver['text'] = text

    #################################################################
    # Method: load
    # Purpose: Loads the basic GUI of the card outside of the base
    #          image. For now, Labels for 'B'I'N'G'O' are generated
    #          and are scaled/positioned according to the image
    #          scale.
    # Input: None
    # Output: None
    #################################################################
    def load(self):
        assert self.notify.debugStateCall(self)
        self.notify.debug("Bingo card loading")

        # Create Timer
        self.loadGameTimer()
        self.loadNextGameTimer()

        textScale = 0.06 #0.125*BG.CardImageScale[2]
        textHeight = 0.38*BG.CardImageScale[2]

        guiButton = loader.loadModel("phase_3/models/gui/quit_button")
        self.bingo = DirectButton( parent = self,
                                   pos = (BG.GridXOffset, 0, 0.305),
                                   scale = (0.0343, 0.035, 0.035),
                                   relief = None,
                                   state = DGG.DISABLED,
                                   geom = self.model.find("**/BINGObutton"),
                                   geom_pos = (0, 0, 0),
                                   geom_hpr = (0, 90, 0),
                                   image = (self.model.find("**/Gold_TTButtUP"),
                                            self.model.find("**/goldTTButtDown"),
                                            self.model.find("**/RolloverBingoButton1")),
                                   image_pos = (0, 0, 0),
                                   image_hpr = (0, 90, 0),
                                   image_color = BG.getButtonColor(0),
                                   pressEffect = False,
                                   )
        guiButton.removeNode()

        arrowModel = loader.loadModel("phase_3.5/models/gui/speedChatGui")
        self.gameType = DirectButton( parent = self,
                                      pos = (BG.GridXOffset, 0, -8*BG.CardImageScale[2] - 0.01),
                                      relief = None,
                                      image = arrowModel.find("**/chatArrow"),
                                      image_scale = -0.05,
                                      image_pos = (-0.2, 0, 0.025),
                                      text="",
                                      text_scale = 0.045,
                                      text_fg = (1,1,1,1),
                                      text_font = ToontownGlobals.getSignFont(),
                                      text_wordwrap = 10.5,
                                      text_pos = (0.01,0.008),
                                      pressEffect = False,
                                      #frameSize = (-0.18,0.23,0.05,-0.003),
                                      )
        arrowModel.removeNode()

        self.gameType.bind(DGG.ENTER, self.onMouseEnter)
        self.gameType.bind(DGG.EXIT,  self.onMouseLeave)
        self.gameType.hide()

        """
        iScale = (0.3*BG.CardImageScale[0], 0.3*BG.CardImageScale[2])
        self.jackpot = DirectLabel( parent = self,
                                    pos = (.675*BG.CardImageScale[0], 0, -0.05*BG.CardImageScale[2]),
                                    relief = None,
                                    state = DGG.NORMAL,
                                    text = '0',
                                    text_scale = 0.0425,
                                    text_fg = (0, 0, 0, 1),
                                    #text_pos = (0, .30*iScale[1], 0),
                                    text_font = ToontownGlobals.getInterfaceFont(),
                                    text_wordwrap = 10.5,
                                    image = DGG.getDefaultDialogGeom(),
                                    image_scale = (iScale[0],0, iScale[1]))
        """
        self.jpText = DirectLabel( parent = self,
                                   pos = (BG.GridXOffset, 0, 0.22),
                                   relief = None,
                                   state = DGG.NORMAL,
                                   text = '',
                                   text_scale = TTLocalizer.BCGjpText,
                                   text_pos = (0,0,0),
                                   text_fg = (1, 1, 1, 1),
                                   text_shadow = (0, 0, 0, 1),
                                   text_font = ToontownGlobals.getInterfaceFont(),
                                   text_wordwrap = TTLocalizer.BCGjpTextWordwrap)

        self.gameOver = DirectLabel( parent = self,
                                     pos = (BG.GridXOffset, 0, 0),
                                     relief = None,
                                     state = DGG.NORMAL,
                                     text = '',
                                     text_scale = textScale,
                                     text_fg = (1, 1, 1, 1),
                                     text_font = ToontownGlobals.getSignFont())

        #jpsign is parented to self.parent so we can place it behind the main card
        self.jpSign = DirectFrame( parent = self.parent,
                                   relief = None,
                                   state = DGG.NORMAL,
                                   pos = BG.CardPosition,
                                   scale = (0.035, 0.035, 0.035),
                                   text = TTLocalizer.FishBingoJackpot,
                                   text_scale = 2,
                                   text_pos = (-1.5, 18.6),
                                   text_fg = (1,1,1,1),
                                   image = self.model.find("**/jackpot"),
                                   image_pos = (0, 0, 0),
                                   image_hpr = (0, 90, 0),
                                   sortOrder = DGG.BACKGROUND_SORT_INDEX,
                                   )

        self.makeJackpotLights(self.jpSign)
        self.hideJackpot()

        self.makeTutorial()

    #################################################################
    # Method: destroy
    # Purpose: This method cleans up the Card so that there are no
    #          persisting memory leaks. Each cell within the card
    #          is destroyed as well as each letter label.
    # Input: None
    # Output: None
    #################################################################
    def destroy(self):
        self.cleanTutorial()

        self.removeGame()
        del self.cellGuiList

        self.gameOver.destroy()
        self.destroyJackpotLights()
        self.jpSign.destroy()
        self.nextGameTimer.destroy()
        self.nextGame.destroy()
        self.timer.destroy()
        self.bingo.destroy()
        self.gameType.destroy()
        DirectFrame.destroy(self)
        self.notify.debug("Bingo card destroyed")

    #################################################################
    # Method: loadCard
    # Purpose: This method generates the necessary logos for each
    #          cell within the card. It then attempts to show those
    #          logos based-on the current game state. If a cell is
    #          not occupied by a "Bingo Marker", ie a 0 in the
    #          gameState bit-string, then its logo will be shown.
    #          The free cell logo is always shown.
    # Input: None
    # Output: None
    #################################################################
    def loadCard(self):
        cardSize = self.game.getCardSize()
        for index in xrange(cardSize):
            self.cellGuiList[index].generateLogo()
            if index == cardSize/2:
                self.cellGuiList[index].generateMarkedLogo()
            elif (self.game.getGameState() & (1 << index)):
                self.cellGuiList[index].disable()

    #################################################################
    # Method: disableCard
    # Purpose: This method disables each cell within the card so that
    #          the button can no longer trigger an invalid play
    #          attempt.
    # Input: None
    # Output: None
    #################################################################
    def disableCard(self):
        self.stopCellBlinking()
        for index in xrange(self.game.getCardSize()):
            self.cellGuiList[index].disable()

    #################################################################
    # Method: enablesCard
    # Purpose: This method enables each cell within the card so that
    #          when a button is pressed, it triggers the appropriate
    #          callback routine. The Free Cell is never enabled.
    # Input: callback - A callback routine to handle a button press.
    # Output: None
    #################################################################
    def enableCard(self, callback=None):
        self.notify.info("enable Bingo card")
        self.stopCellBlinking()
        for index in xrange(len(self.cellGuiList)):
            if index != self.game.getCardSize()/2:
                self.cellGuiList[index].enable(callback)

    #################################################################
    # Method: generateCard
    # Purpose: This method generates the actual card, and is based-on
    #          the tileSeed that is provided by the AI and the zoneId
    #          which is obtained from the pond.
    # Input: tileSeed - Seed for the RNG to generate the same fish
    #                   as those found on the AI Card.
    #        zoneId - Needed to choose the appropriate fish for the
    #                 pond that the card instance is associated with.
    # Output: None
    #################################################################
    def generateCard(self, tileSeed, zoneId):
        assert( self.game != None )

        rng = RandomNumGen.RandomNumGen(tileSeed)
        rowSize = self.game.getRowSize()

        # Retrieve a list of Fish based on the Genus Type. Each Genus
        # found in the pond will be represented on the board.
        fishList = FishGlobals.getPondGeneraList(zoneId)

        # Go through the fish list and generate actual fish.
        # NOTE: This should likely be removed when the fish logos come into play.
        # There is no need to generate a Fish object. Tuples (genus, species)
        # can effectively be used to identify the type of fish for a specific
        # BingoCardCell.
        for i in xrange(len(fishList)):
            fishTuple = fishList.pop(0)
            weight = FishGlobals.getRandomWeight(fishTuple[0], fishTuple[1])
            fish = FishBase.FishBase(fishTuple[0], fishTuple[1], weight)
            fishList.append(fish)

        # Determine the number of cells left to fill.
        emptyCells = (self.game.getCardSize()-1) - len(fishList)

        # Fill up the empty cells with randomly generated fish. In order to
        # maintain fairness, iterate through the rods as well.
        rodId = 0
        for i in xrange(emptyCells):
            fishVitals = FishGlobals.getRandomFishVitals(zoneId, rodId, rng)
            while( not fishVitals[0] ):
                fishVitals = FishGlobals.getRandomFishVitals(zoneId, rodId, rng)

            fish = FishBase.FishBase(fishVitals[1], fishVitals[2], fishVitals[3])
            fishList.append( fish )
            rodId +=1
            if rodId > 4: rodId = 0

        # Now that we have generated all of the fish that will make up the card,
        # it is time to actually generate a BingoCardCell for every fish. This
        # cell will be parented to the GUI instance and its position and scale
        # are based on the CardImageScale. (See base positions above)
        for i in xrange(rowSize):
            for j in xrange(self.game.getColSize()):
                color = self.getCellColor(i*rowSize+j)
                if i*rowSize+j == self.game.getCardSize()/2:
                    tmpFish = 'Free'
                else:
                    choice = rng.randrange(0, len(fishList))
                    tmpFish = fishList.pop(choice)

                xPos = BG.CellImageScale * (j-2) + BG.GridXOffset
                yPos = BG.CellImageScale * (i-2) - 0.015
                cellGui = BingoCardCell.BingoCardCell(i*rowSize+j,
                                                      tmpFish,
                                                      self.model,
                                                      color,
                                                      self,
                                                      image_scale=BG.CellImageScale,
                                                      pos=(xPos,0,yPos),
                                                      )
                self.cellGuiList.append(cellGui)

    #################################################################
    # Method: cellUpdateCheck
    # Purpose: This method checks to see if there was a successful
    #          update on a cell. If so, that cell should now become
    #          disabled and the checkForWin method is called in
    #          order to determine if the client has won.
    # Input: id - Cell ID to check against.
    #        Genus - Genus of the fish to check against.
    #        Species - Species of the fish to check against.
    # Output: None
    #################################################################
    def cellUpdateCheck(self, id, genus, species):
        # For now, only check against genus. Perhaps
        # we shall move to species later if it is too easy.
        fishTuple = (genus, species)
        if (self.cellGuiList[id].getFishGenus() == genus) or (fishTuple == FishGlobals.BingoBoot):
            self.notify.debug("Square found!  Cell disabled: %s" % id)
            self.stopCellBlinking()
            self.cellGuiList[id].disable()
            self.game.setGameState( self.game.getGameState() | 1<<id )
            if self.game.checkForBingo():
                return BG.WIN
            return BG.UPDATE
        return BG.NO_UPDATE

    #################################################################
    # Method: cellUpdate
    # Purpose: This method updates a particular cell. Essentially,
    #          it disables this cell so that a player can no longer
    #          click the button and generate further checks against
    #          it.
    # Input: cellId - The Id of the Cell to update.
    # Output: None
    #################################################################
    def cellUpdate(self, cellId):
        assert( 0 <= cellId < BG.CARD_SIZE )
        self.cellGuiList[cellId].disable()

    #################################################################
    # Method: addGame
    # Input: game instance
    # Output: None
    #################################################################
    def addGame(self, game):
        self.game = game

        # setup Jackpot
        type = game.getGameType()
        self.gameType.setProp('text', BG.getGameName(type))
        self.gameType.setFrameSize()
        self.gameType.show()


    #################################################################
    # Method: getGame
    # Purpose: Accessor method that retrieves the current game which
    #          is associated with the GUI instance.
    # Input: None
    # Output: returns the current bingo game
    #################################################################
    def getGame(self):
        return self.game

    #################################################################
    # Method: removeGame
    # Purpose: This method removes the current game from the bingo
    #          gui. This occurs after a game has been completed and
    #          a new game will be instantiated in the next round. It
    #          will also occur the CardGui is destroyed.
    # Input: None
    # Output: None
    #################################################################
    def removeGame(self):
        self.stopCellBlinking()
        if self.game:
            self.game.destroy()
            self.game = None

        self.setJackpotText(None)
        self.resetGameTypeText()
        for cell in self.cellGuiList:
            cell.destroy()
        self.cellGuiList = []

    #################################################################
    # Method: getUnmarkedMatches
    # Purpose: returns a list of cells that match
    #          a particular fish
    #################################################################
    def getUnmarkedMatches(self, fish):
        if self.game is None:
            return []

        matches = []
        for cell in self.cellGuiList:
            if cell['state'] == DGG.NORMAL:
                if (cell.getFishGenus() == fish[0]) or (fish == FishGlobals.BingoBoot):
                    matches.append(cell)

        return matches

    #################################################################
    # Method: getCellColor
    # Purpose: This method determines what color a cell on the bingo
    #          card should be. This is useful for representing
    #          patterns such as Diagonals or Four Corner, etc.
    # Input: id - the Cell Id to return this color
    # Output: returns specific color or base color of a cell
    #################################################################
    def getCellColor(self, id):
        if self.game.checkForColor(id):
            return BG.CellColorActive
        return BG.CellColorInactive

    #################################################################
    # Method: resetCellColors
    #################################################################
    def resetCellColors(self):
        for cell in self.cellGuiList:
            c = self.getCellColor(cell.cellId)
            cell['image'].setColor(c[0], c[1], c[2], c[3])
            cell.setImage()

    #################################################################
    # Method: stopCellBlinking
    #################################################################
    def stopCellBlinking(self):
        self.hideTutorial()
        self.resetCellColors()
        taskMgr.remove(self.taskNameFlashFish)

    #################################################################
    # Method: __inidicateMatches
    #################################################################
    def __indicateMatches(self, bFlipFlop, fish):
        unmarkedMatches = self.getUnmarkedMatches(fish)
        if len(unmarkedMatches) is 0:
            return Task.done

        if bFlipFlop:
            #mark the cells
            for cell in unmarkedMatches:
                cell['image'].setColor(1,0,0,1)
                cell.setImage()
        else:
            #unmark the cells
            self.resetCellColors()

        taskMgr.doMethodLater(0.5, self.__indicateMatches, self.taskNameFlashFish, extraArgs = (not bFlipFlop, fish))
        return Task.done

    #################################################################
    # Method: fishCaught
    # Purpose: This method is called when a fish has been caught.
    #          It then indicates which squares match.
    # Input: fish - the caught fish
    # Output: None
    #################################################################
    def fishCaught(self, fish):
        self.stopCellBlinking()
        self.__indicateMatches(True, fish)

    #################################################################
    # Method: setBingo
    # Purpose: This method updates the current state of the bingo
    #          button that is used to "call" out bingo.
    # Input: state - DGG.NORMAL or DGG.DISABLED.
    #        command - a callback function to check for bingo
    #                  when a user clicks the button.
    # Output: Returns BG.WIN(2) or BG.NO_UPDATE(0)
    # Note: We may decide to DISABLE the button until there is a winner
    #       or more appropriately, make it flash a few times when
    #       bingo is first detected.
    #################################################################
    def setBingo(self, state=DGG.DISABLED, callback=None):
        self.notify.debug("setBingo: %s %s" % (state, callback))
        if self.bingo['state'] == state:
            #duplicate message... ignore
            return

        if not self.game:
            #race condition
            return

        if state == DGG.NORMAL:
            self.__indicateBingo(True)
            if self.game.getGameType() == BG.BLOCKOUT_CARD:
                self.showJackpot()
        else:
            taskMgr.remove("bingoFlash")
            c = BG.getButtonColor(self.game.getGameType())
            self.bingo['image_color'] = Vec4(c[0], c[1], c[2], c[3])
            self.hideJackpot()

        self.bingo['state'] = state
        self.bingo['command'] = callback

    #################################################################
    # Method: checkForBingo
    # Purpose: This method checks for bingo of the current game
    #          and returns if there was a win.
    # Input: None
    # Output: Returns BG.WIN(2) or BG.NO_UPDATE(0)
    #################################################################
    def checkForBingo(self):
        return self.game.checkForBingo()

    #################################################################
    # Method: __inidicateBingo
    #################################################################
    def __indicateBingo(self, bFlipFlop):
        if not self.game:
            #user has left, stop doing this task
            return Task.done

        if bFlipFlop:
            gameType = self.game.getGameType()
            if gameType == BG.DIAGONAL_CARD:
                color = Vec4(1,1,1,1)
            else:
                color = Vec4(1,0,0,1)
            self.bingo['image_color'] = color
        else:
            c = BG.getButtonColor(self.game.getGameType())
            self.bingo['image_color'] = Vec4(c[0], c[1], c[2], c[3])

        taskMgr.doMethodLater(0.5, self.__indicateBingo, "bingoFlash", extraArgs = (not bFlipFlop,))
        return Task.done

    ###########################################################################
    # These methods handle the jackpot lights.
    ###########################################################################

    NumLights = 32
    Off = False
    On = True
    def showJackpot(self):
        self.jpSign.show()
        for light in self.jpLights:
            light.show()
        self.flashJackpotLights(random.randrange(3))
    def hideJackpot(self):
        self.jpSign.hide()
        for light in self.jpLights:
            light.hide()
        taskMgr.remove("jackpotLightFlash")

    def getLightName(self, lightIndex, bOn):
        lightIndex += 1
        if bOn == self.On:
            return "**/LightOn_0%02d" % lightIndex
        else:
            return "**/LightOff_0%02d" % lightIndex

    def makeJackpotLights(self, parent):
        self.jpLights = []
        for nLight in range(self.NumLights):
            lightName = self.getLightName(nLight, self.Off)
            light = DirectFrame( parent = parent,
                                 relief = None,
                                 image = self.model.find(lightName),
                                 image_hpr = (0,90,0),
                                 )
            self.jpLights.append(light)

    def destroyJackpotLights(self):
        taskMgr.remove("jackpotLightFlash")
        for light in self.jpLights:
            light.destroy()

    def lightSwitch(self, bOn, lightIndex = -1):
        if lightIndex == -1:
            #turn them all on
            for nLight in range(self.NumLights):
                self.lightSwitch(bOn, nLight)
        else:
            lightIndex %= self.NumLights
            light = self.jpLights[lightIndex-1]
            light['image'] = self.model.find(self.getLightName(lightIndex, bOn))
            light['image_hpr'] = (0,90,0)

    def flashJackpotLights(self, flashMode, nTimeIndex = 0):
        if flashMode == 2:
            #cool chasing lights
            self.lightSwitch(self.Off)
            self.lightSwitch(self.On, nTimeIndex)
            self.lightSwitch(self.On, self.NumLights-nTimeIndex)
            self.lightSwitch(self.On, self.NumLights/2 + nTimeIndex)
            self.lightSwitch(self.On, self.NumLights/2 - nTimeIndex)

            nTimeIndex = (nTimeIndex + 1) % (self.NumLights/2)
            delay = 0.05
        elif flashMode == 1:
            #simple blink
            if nTimeIndex:
                self.lightSwitch(self.On)
            else:
                self.lightSwitch(self.Off)
            nTimeIndex = not nTimeIndex
            delay = 0.5
        elif flashMode == 0:
            #every third light... rotating
            for nLight in range(self.NumLights):
                if nLight % 2 == nTimeIndex:
                    self.lightSwitch(self.On, nLight)
                else:
                    self.lightSwitch(self.Off, nLight)

            nTimeIndex = (nTimeIndex + 1) % 2
            delay = 0.2

        taskMgr.doMethodLater(delay, self.flashJackpotLights, "jackpotLightFlash", extraArgs = (flashMode,nTimeIndex))
        return Task.done

    #################################################################
    # stuff for the FishBingo tutorial
    #################################################################
    def makeTutorial(self):
        self.tutorial = TTDialog.TTDialog(
            fadeScreen = 0,
            pad = (0.05,0.05),
            midPad = 0,
            topPad = 0,
            sidePad = 0,
            text = TTLocalizer.FishBingoHelpBlockout,  #use this one to set the size of the dialog sonce it's the longest string
            style = TTDialog.NoButtons,
            pos = BG.TutorialPosition,
            scale = BG.TutorialScale,
            )
        self.tutorial.hide()

    def cleanTutorial(self):
        self.tutorial.cleanup()
        self.tutorial = None

    def showTutorial(self, messageType):
        # Tells the user how to play bingo
        if messageType == BG.TutorialIntro:
            self.tutorial['text'] = TTLocalizer.FishBingoHelpMain
        elif messageType == BG.TutorialMark:
            self.tutorial['text'] = TTLocalizer.FishBingoHelpFlash
        elif messageType == BG.TutorialCard:
            if self.game:
                gameType = self.game.getGameType()
                self.tutorial['text'] = BG.getHelpString(gameType)
        elif messageType == BG.TutorialBingo:
            self.tutorial['text'] = TTLocalizer.FishBingoHelpBingo

        self.tutorial.show()

    def hideTutorial(self, event=None):
        if self.tutorial:
            self.tutorial.hide()

    def onMouseEnter(self, event):
        """ the mouse has just entered this entity """
        if self.gameType['text'] is not "":
            self.showTutorial(BG.TutorialCard)

    def onMouseLeave(self, event):
        """ the mouse has just left this entity """
        self.hideTutorial()

    def castingStarted(self):
        if taskMgr.hasTaskNamed(self.taskNameFlashFish):
            if not base.localAvatar.bFishBingoMarkTutorialDone:
                self.showTutorial(BG.TutorialMark)
                base.localAvatar.b_setFishBingoMarkTutorialDone(True)
