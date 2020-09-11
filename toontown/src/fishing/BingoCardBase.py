#################################################################
# class: BingoCardBase.py
# Purpose: Provide a base layout of the bingo card which can
#          be used in a variety of games. 
#################################################################

#################################################################
# Direct Specific Modules
#################################################################
from direct.directnotify import DirectNotifyGlobal

#################################################################
# Toontown Specific Modules
#################################################################
from toontown.fishing import FishGlobals
from toontown.fishing import BingoGlobals
from direct.showbase import RandomNumGen

#################################################################
# Python Specific Modules
#################################################################
from math import ceil, pow

class BingoCardBase:
    notify = DirectNotifyGlobal.directNotify.newCategory('BingoCardBase')
    #################################################################
    # Method: __init__
    # Purpose: This method provides initial construction of the Card.
    #          It determines if the card is of a valid size, and
    #          that it is square. Checking of a non-square card is
    #          impossible for diagonal cases. 
    # Input: cardSize - The size of the card rowSize x colSize.
    #        rowSize - The number of rows in the card.
    #        colSize - The number of cols in the card.
    #        **kw - OptionDefs for the DirectFrame
    # Output: None
    #################################################################
    def __init__( self, cardSize=BingoGlobals.CARD_SIZE,
                  rowSize=BingoGlobals.CARD_ROWS, colSize=BingoGlobals.CARD_COLS ):
        
        self.rowSize = rowSize
        self.colSize = colSize
        self.cardSize = cardSize
        
        self.cellList = []
        self.gameType = None
        self.gameState = 1<<self.cardSize/2

    #################################################################
    # Method: destroy
    # Purpose: This method cleans up the Card.
    # Input: None
    # Output: None
    #################################################################
    def destroy(self):
        del self.cellList

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
        rng = RandomNumGen.RandomNumGen(tileSeed)

        # Retrieve a list of Fish based on the Genus Type. Each Genus
        # found in the pond will be represented on the board.
        fishList = FishGlobals.getPondGeneraList(zoneId)

        # Determine the number of cells left to fill.
        emptyCells = (self.cardSize-1) - len(fishList)

        rodId = 0
        for i in xrange(emptyCells):
            fish = FishGlobals.getRandomFishVitals(zoneId, rodId, rng)
            while( not fish[0] ):
                fish = FishGlobals.getRandomFishVitals(zoneId, rodId, rng)
            fishList.append( (fish[1], fish[2]) )
            rodId += 1

            if rodId > 4: rodId = 0

        # Now, fill up the the card by randomly placing the fish in a cell.
        for index in xrange(self.cardSize):
            if index != self.cardSize/2:
                choice = rng.randrange(0,len(fishList))
                self.cellList.append( fishList.pop(choice) )
            else:
                self.cellList.append( (None, None) )

    #################################################################
    # Method: getGameType
    # Purpose: This method retrieves the game type of the Bingo
    #          card.
    # Input: None
    # Output: Returns the type of the Bingo Card.
    #################################################################
    def getGameType(self):
        return self.gameType

    #################################################################
    # Method: getGameState
    # Purpose: This method retrieves the game state of the current Bingo
    #          card.
    # Input: None
    # Output: Returns the current state of the Bingo Card.
    #################################################################
    def getGameState(self):
        return self.gameState

    #################################################################
    # Method: getCardSize
    # Purpose: This method retrieves the card size of the current
    #          Bingo Card.
    # Input: None
    # Output: Returns the card size of the Bingo Card.
    #################################################################
    def getCardSize(self):
        return self.cardSize

    #################################################################
    # Method: getRowSize
    # Purpose: This method retrieves the row size of the current
    #          Bingo Card.
    # Input: None
    # Output: Returns the row size of the Bingo Card.
    #################################################################
    def getRowSize(self):
        return self.rowSize

    #################################################################
    # Method: getColSize
    # Purpose: This method retrieves the col size of the current
    #          Bingo Card.
    # Input: None
    # Output: Returns the col size of the Bingo Card.
    #################################################################
    def getColSize(self):
        return self.colSize

    #################################################################
    # Method: setGameState
    # Purpose: This method sets the game state of the current Bingo
    #          card.
    # Input: state - New State of the Card.
    # Output: None
    #################################################################
    def setGameState(self, state):
        self.gameState = state
                                      
    #################################################################
    # Method: clearCellList
    # Purpose: This method clears the list of cells corresponding
    #          to this card.
    # Input: None
    # Output: None
    ################################################################# 
    def clearCellList(self):
        del self.cellList
        self.cellList = [] 

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

        # Determine if the id of the cell is within the
        # proper range so that we do not receive and invalid
        # index from a client. Possible hack attempt.
        if id >= self.cardSize:
            self.notify.warning('cellUpdateCheck: Invalid Cell Id %s. Id greater than Card Size.')
            return
        elif id < 0:
            self.notify.warning('cellUpdateCheck: Invalid Cell Id %s. Id less than zero.')
            return
            
        fishTuple = (genus, species)
        if (self.cellList[id][0] == genus) or (fishTuple == FishGlobals.BingoBoot):
            self.gameState = self.gameState | (1<<id)
            if self.checkForWin(id):
                return BingoGlobals.WIN
            return BingoGlobals.UPDATE
        return BingoGlobals.NO_UPDATE

    #################################################################
    # Method: checkForWin
    # Purpose: This method is really just here as a base class
    #          method. It would be equivalent to a virtual class
    #          in C++.
    # Input: id - Cell ID to check against.
    # Output: None
    ################################################################# 
    def checkForWin(self, id):
        pass
                 
    #################################################################
    # Method: rowCheck
    # Purpose: This method checks to determine if there there is
    #          a win in a particular row.
    # Input: rowId - The Id Number of the Row to Check.
    # Output: None
    ################################################################# 
    def rowCheck(self, rowId):
        for colId in xrange(self.colSize):
            if not (self.gameState & (1 << (self.rowSize*rowId+colId) )):
                return 0
        return 1

    #################################################################
    # Method: colCheck
    # Purpose: This method checks to determine if a particular
    #          column has been filled out. Not a part of traditional
    #          bingo, but may be used for bonuses or such.
    # Input: rowId - The Id Number of the Column to Check.
    # Output: None
    ################################################################# 
    def colCheck(self, colId):
        for rowId in xrange(self.rowSize):
            if not (self.gameState & (1 << (self.rowSize*rowId+colId) )):
                return 0
        return 1

    #################################################################
    # Method: fDiagCheck
    # Purpose: This method checks along the forward diagonal of the
    #          Bingo Card square to determine if there was a win. The
    #          forward diagonal consists of ids from 0 to (cardSize-1)
    # Input: cellId - The ID Number of the Cell to check.
    # Output: None
    ################################################################# 
    def fDiagCheck(self, id):
        checkNum = self.rowSize+1
        if not (id % checkNum):
            for i in xrange(self.rowSize):
                if not (self.gameState & (1 << i*checkNum)):
                    return 0
            return 1
        else:
            return 0

    #################################################################
    # Method: bDiagCheck
    # Purpose: This method checks along the backward diagonal of the
    #          Bingo Card square to determine if there was a win. The
    #          forward diagonal consists of ids from 4 to
    #          (cardSize-rowSize)
    # Input: cellId - The ID Number of the Cell to check.
    # Output: None
    ################################################################# 
    def bDiagCheck(self, id):
        checkNum = self.rowSize-1
        if not(id % checkNum) and (not(id==(self.cardSize-1))):
            for i in xrange(self.rowSize):
                if not (self.gameState & (1 << (i*checkNum+checkNum))):
                    return 0
            return 1
        return 0

#####################################################################
# Utility Methods
#####################################################################
    # Method: cellCheck
    # Purpose: Determines whether a cell is occupied or not. It is
    #          called w
    # Input: id - The ID Number of the Cell to check.
    # Output: returns 1 or 0 based on whether the cell is occupied.
    ################################################################# 
    def cellCheck(self, id):
        if (self.gameState & (1 << id)):
            return 1
        return 0

    #################################################################
    # Method: onRow
    # Purpose: Determines whether a cell is located on a specific
    #          row in the card.
    # Input: row - column to check against
    #        id - The ID Number of the Cell to check.
    # Output: returns 1 or 0 whether cell is on the specified row.
    ################################################################# 
    def onRow(self, row, id):
        if int( id / self.rowSize ) == row:
            return 1
        return 0


    #################################################################
    # Method: onCol
    # Purpose: Determines whether a cell is located on a specific
    #          column in the card.
    # Input: col - column to check against
    #        id - The ID Number of the Cell to check.
    # Output: returns 1 or 0 whether cell is on the specified column.
    ################################################################# 
    def onCol(self, col, id):
        if (id % BingoGlobals.CARD_COLS) == col:
            return 1
        return 0

    #################################################################
    # Method: onFDiag
    # Purpose: Determines whether a cell is located on the forward
    #          diagonal of the card.
    # Input: id - The ID Number of the Cell to check.
    # Output: returns 1 or 0 whether cell is on the Forward Diagonal
    ################################################################# 
    def onFDiag(self, id):
        checkNum = self.rowSize + 1
        if not (id % checkNum):
            return 1
        return 0

    #################################################################
    # Method: onBDiag
    # Purpose: Determines whether a cell is located on the backwards
    #          diagonal of the card.
    # Input: id - The ID Number of the Cell to check.
    # Output: returns 1 or 0 whether cell is on the backward Diagonal
    ################################################################# 
    def onBDiag(self, id):
        checkNum = self.rowSize - 1
        if not (id % checkNum):
            return 1
        return 0
