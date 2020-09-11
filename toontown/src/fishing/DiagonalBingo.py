#################################################################
# class: NormalBingo.py
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
from toontown.fishing import BingoGlobals
from toontown.fishing import BingoCardBase

class DiagonalBingo(BingoCardBase.BingoCardBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DiagonalBingo')
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
        BingoCardBase.BingoCardBase.__init__(self, cardSize, rowSize, colSize)

        self.gameType = BingoGlobals.DIAGONAL_CARD
        self.fDiagResult = 0
        self.bDiagResult = 0

    #################################################################
    # Method: checkForWin
    # Purpose: This method checks if there was a win after the last
    #          cell update. It calls all of the game logic methods
    #          which are required to determine a win.
    # Input: id - The ID Number of the cell to Check.
    # Output: None
    ################################################################# 
    def checkForWin(self, id):
        if self.fDiagCheck(id):
            self.fDiagResult = 1
        if self.bDiagCheck(id):
            self.bDiagResult = 1
            
        if self.fDiagResult and self.bDiagResult:
            return BingoGlobals.WIN
        return BingoGlobals.NO_UPDATE

    #################################################################
    # Method: checkForColor
    # Purpose: This method determines if a specified cell ID should
    #          be a particular color.
    # Input: id - The ID Number of the cell to Check.
    # Output: returns 1 if on a diagonal, 0 if it is not
    ################################################################# 
    def checkForColor(self, id):
        return (self.onFDiag(id) | self.onBDiag(id))

    #################################################################
    # Method: checkForBingo
    # Purpose: This method checks if there was a win after the last
    #          cell update. It calls all of the game logic methods
    #          which are required to determine a win.
    # Input: id - The ID Number of the cell to Check.
    # Output: returns BingoGlobals.WIN(2) or BingoGlobals.NO_UPDATE(0)
    ################################################################# 
    def checkForBingo(self):
        id = self.cardSize/2
        if self.checkForWin(id):
            return BingoGlobals.WIN
        return BingoGlobals.NO_UPDATE

        
            
        
