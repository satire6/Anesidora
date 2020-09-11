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

class NormalBingo(BingoCardBase.BingoCardBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('NormalBingo')
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
        self.gameType = BingoGlobals.NORMAL_CARD

    #################################################################
    # Method: checkForWin
    # Purpose: This method checks if there was a win after the last
    #          cell update. It calls all of the game logic methods
    #          which are required to determine a win.
    # Input: id - The ID Number of the cell to Check.
    # Output: None
    ################################################################# 
    def checkForWin(self, id):
        rowId = int(id / BingoGlobals.CARD_ROWS)
        colId = id % BingoGlobals.CARD_COLS

        rowResult = self.rowCheck(rowId)
        colResult = self.colCheck(colId)
        fDiagResult = self.fDiagCheck(id)
        bDiagResult = self.bDiagCheck(id)

        if rowResult or colResult or fDiagResult or bDiagResult:
            return BingoGlobals.WIN
        return BingoGlobals.NO_UPDATE

    #################################################################
    # Method: checkForColor
    # Purpose: This method determines if a specified cell ID should
    #          be a particular color.
    # Input: id - The ID Number of the cell to Check.
    # Output: returns 1 since this is normal bingo.
    ################################################################# 
    def checkForColor(self, id):
        return 1

    #################################################################
    # Method: checkForBingo
    # Purpose: This method checks if there was a win after the last
    #          cell update. It calls all of the game logic methods
    #          which are required to determine a win.
    # Input: id - The ID Number of the cell to Check.
    # Output: None
    ################################################################# 
    def checkForBingo(self):
        # First Check the middle square to eliminate
        # diagonals and middle row & col
        id = self.cardSize/2
        if self.checkForWin(id):
            return BingoGlobals.WIN

        # Next check remaining rows and columns
        for i in xrange(BingoGlobals.CARD_ROWS):
            if i != (BingoGlobals.CARD_ROWS/2):
                rowResult = self.rowCheck(i)
                colResult = self.colCheck(i)
                if rowResult | colResult:
                    return BingoGlobals.WIN
        return BingoGlobals.NO_UPDATE
