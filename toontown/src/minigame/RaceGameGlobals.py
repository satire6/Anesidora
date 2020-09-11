# RaceGameGlobals.py: info used by client and AI for the race game

from toontown.toonbase import TTLocalizer

# This stores the value of each choice.
# These are the only valid choices for a client to make. Any choice
# not in this array will be caught and handled here
ValidChoices = [0,1,2,3,4]

NumberToWin = 14
InputTimeout = 20

# repeated for probabilities sake
ChanceRewards = (
        # ((affect on us, affect on others), text string, extra-jellybeans)
        ((1, 0), TTLocalizer.RaceGameForwardOneSpace, 0),
        ((1, 0), TTLocalizer.RaceGameForwardOneSpace, 0),
        ((1, 0), TTLocalizer.RaceGameForwardOneSpace, 0),
        ((2, 0), TTLocalizer.RaceGameForwardTwoSpaces, 0),
        ((2, 0), TTLocalizer.RaceGameForwardTwoSpaces, 0),
        ((2, 0), TTLocalizer.RaceGameForwardTwoSpaces, 0),
        ((3, 0), TTLocalizer.RaceGameForwardThreeSpaces, 0),
        ((3, 0), TTLocalizer.RaceGameForwardThreeSpaces, 0),
        ((3, 0), TTLocalizer.RaceGameForwardThreeSpaces, 0),
        ((0, -3), TTLocalizer.RaceGameOthersBackThree, 0),
        ((0, -3), TTLocalizer.RaceGameOthersBackThree, 0),
        ((-1, 0), TTLocalizer.RaceGameBackOneSpace, 0),
        ((-1, 0), TTLocalizer.RaceGameBackOneSpace, 0),
        ((-2, 0), TTLocalizer.RaceGameBackTwoSpaces, 0),
        ((-2, 0), TTLocalizer.RaceGameBackTwoSpaces, 0),
        ((-3, 0), TTLocalizer.RaceGameBackThreeSpaces, 0),
        ((-3, 0), TTLocalizer.RaceGameBackThreeSpaces, 0),
        ((0, 3), TTLocalizer.RaceGameOthersForwardThree, 0),
        ((0, 3), TTLocalizer.RaceGameOthersForwardThree, 0),
        ((0, 0), TTLocalizer.RaceGameJellybeans2, 2),
        ((0, 0), TTLocalizer.RaceGameJellybeans2, 2),
        ((0, 0), TTLocalizer.RaceGameJellybeans2, 2),
        ((0, 0), TTLocalizer.RaceGameJellybeans2, 2),
        ((0, 0), TTLocalizer.RaceGameJellybeans4, 4),
        ((0, 0), TTLocalizer.RaceGameJellybeans4, 4),
        ((0, 0), TTLocalizer.RaceGameJellybeans4, 4),
        ((0, 0), TTLocalizer.RaceGameJellybeans4, 4),
        ((0, 0), TTLocalizer.RaceGameJellybeans10, 10),
        ((0, 0), -1, 0),   #  -1 tells showChanceCardText() to use TTLocalizer.RaceGameCardTextHi[x]
        ((NumberToWin, 0), TTLocalizer.RaceGameInstantWinner, 0),
        )



