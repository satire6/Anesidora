#################################################################
# class: FourCornerBingo.py
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

class FourCornerBingo(BingoCardBase.BingoCardBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('FourCornerBingo')

    corners = [ 0, (BingoGlobals.CARD_ROWS-1),
                (BingoGlobals.CARD_COLS*(BingoGlobals.CARD_ROWS-1)),
                ((BingoGlobals.CARD_COLS*BingoGlobals.CARD_ROWS)-1)]
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

        self.gameType = BingoGlobals.FOURCORNER_CARD
        
    #################################################################
    # Method: checkForWin
    # Purpose: This method checks if there was a win after the last
    #          cell update. It calls all of the game logic methods
    #          which are required to determine a win.
    # Input: id - The ID Number of the cell to Check.
    # Output: None
    ################################################################# 
    def checkForWin(self, id):
        corners = self.corners
        if (self.cellCheck(corners[0]) and
            self.cellCheck(corners[1]) and
            self.cellCheck(corners[2]) and
            self.cellCheck(corners[3])):
            return BingoGlobals.WIN
        return BingoGlobals.NO_UPDATE

    #################################################################
    # Method: checkForColor
    # Purpose: This method determines if a specified cell ID should
    #          be a particular color.
    # Input: id - The ID Number of the cell to Check.
    # Output: returns 1 if on a corner, 0 if it is not
    ################################################################# 
    def checkForColor(self, id):
        topLeft, topRight, bottomLeft, bottomRight = 0, 0, 0, 0        
        if id == self.corners[0]:
            topLeft = 1
        elif id == self.corners[1]:
            topRight = 1
        elif id == self.corners[2]:
            bottomLeft = 1
        elif id == self.corners[3]:
            bottomRight = 1
        else:
            pass
        
        return (topLeft or topRight or bottomLeft or bottomRight)

    #################################################################
    # Method: checkForBingo
    # Purpose: This method checks if there was a win after the last
    #          cell update. It calls all of the game logic methods
    #          which are required to determine a win.
    # Input: id - The ID Number of the cell to Check.
    # Output: returns BingoGlobals.WIN(2) or BingoGlobals.NO_UPDATE(0)
    ################################################################# 
    def checkForBingo(self):
        return self.checkForWin(0)

