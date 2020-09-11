#if not specified, how many votes do we start out with
DefaultStartingVotes = 5

# how far do we go on the travel game and minigame cycle
FinalMetagameRoundIndex = 5

# base beans formula for bonus currently goes
# BaseBeans x num of unique paths x metagame round (1,2 or 3) x num players / 4
BaseBeans = 10

# what percent of votes left are converted to beans
# key is the number of players
PercentOfVotesConverted = {
    1: 50,
    2: 33,
    3: 66,
    4: 100,
    }

# in seconds, how many seconds do we wait for them to decide
InputTimeout = 15

# what is the maximum number of directions we can go from each switch
MaxDirections = 2

# reasons we are going to a certain direction
ReasonVote = 0 # one direction had the most votes
ReasonPlaceDecider = 1 # a tie, and 1st place in last minigame breaks it
ReasonRandom = 2 # a tie, multiple 1st place in diff directions, so just make it random

DisplayVotesTimePerPlayer = 2 # how long do we display the votes per player
MoveTrolleyTime = 5 # in seconds, how long does this state last
FudgeTime = 0 # in seconds a small buffer to account for lag

SpoofFour = False # debug variable to spoof 4 players on vote results panel
ReverseWin = False # debug variable to switch sound effects

# Our Tree Structure
# First number is our id,
# links is a list of other nodes we connect to,
# pos is our x,y,z on the board in render coords
# for kicks we could potentially do a different board layout
# in between rounds, or a different one for each safe zone
# our initial layout, change as necessary
#         10
#       6 
#     3   11
#   1   7
# 0   4   12
#   2   8
#     5   13
#       9
#         14 
# baseBonus is calculated from the inverse of the number of unique paths
# it takes to get to that leaf

xInc = 60
yInc = 15
BoardLayout4VotingRounds = {
    0 : { 
          'links' : (1,2),
          'pos' : (0,0,0),
          },
    1 : {
          'links' : (3,4),
          'pos' : (xInc,yInc,0),    
          },
    2 : { 
          'links' : (4,5),
          'pos' : (xInc,-yInc,0),
          },
    3 : {
          'links' : (6,7),
          'pos' : (2*xInc,2*yInc,0),    
          },
    4 : { 
          'links' : (7,8),
          'pos' : (2*xInc,0,0),
          },
    5 : {
          'links' : (8,9),
          'pos' : (2*xInc,-2 * yInc,0),    
          },
    6 : { 
          'links' : (10,11),
          'pos' : (3 * xInc, 3*yInc,0),
          },
    7 : {
          'links' : (11,12),
          'pos' : (3*xInc , yInc,0),    
          },
    8 : { 
          'links' : (12,13),
          'pos' : (3*xInc, -yInc,0),
          },
    9 : {
          'links' : (13,14),
          'pos' : (3*xInc, -3*yInc,0),    
          },
    10 : { 
          'links' : (),
          'pos' : (4*xInc, 4*yInc,0),
          'baseBonus' : 3,
          },
    11 : {
          'links' : (),
          'pos' : (4*xInc, 2*yInc,0),
          'baseBonus' : 2 
          },
    12 : { 
          'links' : (),
          'pos' : (4*xInc,0,0),
          'baseBonus' : 1
          },
    13 : {
          'links' : (),
          'pos' : (4*xInc, -2 * yInc,0),
          'baseBonus' : 2
          },
    14 : { 
          'links' : (),
          'pos' : (4*xInc, -4*yInc,0),
          'baseBonus' : 3
          },
}

#       6
#      /
#     3
#    / \7
#   1
#  / \ /8
# 0   4\
#  \ /  9
#   2 	 
#    \  10
#     5/  
#      \
#       11 
BoardLayout0 = {
    0 : { 
          'links' : (1,2),
          'pos' : (0,0,0),
          },
    1 : {
          'links' : (3,4),
          'pos' : (xInc,2*yInc,0),    
          },
    2 : { 
          'links' : (4,5),
          'pos' : (xInc,-2*yInc,0),
          },
    3 : {
          'links' : (6,7),
          'pos' : (2*xInc,4*yInc,0),    
          },
    4 : { 
          'links' : (8,9),
          'pos' : (2*xInc,0,0),
          },
    5 : {
          'links' : (10,11),
          'pos' : (2*xInc,-4 * yInc,0),    
          },
    6 : { 
          'links' : (),
          'pos' : (3 * xInc, 5*yInc,0),
          'baseBonus' : 2,
          },
    7 : {
          'links' : (),
          'pos' : (3*xInc , 3 * yInc,0),
          'baseBonus' : 2,
          },
    8 : { 
          'links' : (),
          'pos' : (3*xInc, 1 *yInc,0),
          'baseBonus' : 1,
          },
    9 : {
          'links' : (),
          'pos' : (3*xInc, -1*yInc,0),
          'baseBonus' : 1,
          },
    10 : { 
          'links' : (),
          'pos' : (3*xInc, -3*yInc,0),
          'baseBonus' : 2,
          },
    11 : {
          'links' : (),
          'pos' : (3*xInc, -5*yInc,0),
          'baseBonus' : 2 
          },
}

#       7
#      /
#     3
#    / \
#   1   8
#  / \ /
# 0   4-9
#  \
#   2-5-10
#    \  \
#     6- 11
#      \
#       12
BoardLayout1 = {
    0 : { 
          'links' : (1,2),
          'pos' : (0,0,0),
          },
    1 : {
          'links' : (3,4),
          'pos' : (xInc,3*yInc,0),    
          },
    2 : { 
          'links' : (5,6),
          'pos' : (xInc,-3*yInc,0),
          },
    3 : {
          'links' : (7,8),
          'pos' : (2*xInc,4*yInc,0),    
          },
    4 : { 
          'links' : (8,9),
          'pos' : (2*xInc,2*yInc,0),
          },
    5 : {
          'links' : (10,11),
          'pos' : (2*xInc,-2 * yInc,0),    
          },
    6 : { 
          'links' : (11,12),
          'pos' : (2 * xInc, -4*yInc,0),
          },
    7 : {
          'links' : (),
          'pos' : (3*xInc , 5 * yInc,0),
          'baseBonus' : 2,
          },
    8 : { 
          'links' : (),
          'pos' : (3*xInc, 3 *yInc,0),
          'baseBonus' : 1,
          },
    9 : {
          'links' : (),
          'pos' : (3*xInc, 1*yInc,0),
          'baseBonus' : 2,
          },
    10 : { 
          'links' : (),
          'pos' : (3*xInc, -1*yInc,0),
          'baseBonus' : 2,
          },
    11 : {
          'links' : (),
          'pos' : (3*xInc, -3*yInc,0),
          'baseBonus' : 1 
          },
    12 : {
          'links' : (),
          'pos' : (3*xInc, -5*yInc,0),
          'baseBonus' : 2 
          },    
}

#       7
#      /
#     3
#    / \
#   1   8
#  / \ /
# 0   4-9
#  \   /
#   2-5-10
#    \  
#     6-11
#      \
#       12
BoardLayout2 = {
    0 : { 
          'links' : (1,2),
          'pos' : (0,0,0),
          },
    1 : {
          'links' : (3,4),
          'pos' : (xInc,3*yInc,0),    
          },
    2 : { 
          'links' : (5,6),
          'pos' : (xInc,-3*yInc,0),
          },
    3 : {
          'links' : (7,8),
          'pos' : (2*xInc,4*yInc,0),    
          },
    4 : { 
          'links' : (8,9),
          'pos' : (2*xInc,2*yInc,0),
          },
    5 : {
          'links' : (9,10),
          'pos' : (2*xInc, 0 * yInc,0),    
          },
    6 : { 
          'links' : (11,12),
          'pos' : (2 * xInc, -4*yInc,0),
          },
    7 : {
          'links' : (),
          'pos' : (3*xInc , 5 * yInc,0),
          'baseBonus' : 2,
          },
    8 : { 
          'links' : (),
          'pos' : (3*xInc, 3 *yInc,0),
          'baseBonus' : 1,
          },
    9 : {
          'links' : (),
          'pos' : (3*xInc, 1*yInc,0),
          'baseBonus' : 1,
          },
    10 : { 
          'links' : (),
          'pos' : (3*xInc, -1*yInc,0),
          'baseBonus' : 2,
          },
    11 : {
          'links' : (),
          'pos' : (3*xInc, -3*yInc,0),
          'baseBonus' : 2 
          },
    12 : {
          'links' : (),
          'pos' : (3*xInc, -5*yInc,0),
          'baseBonus' : 2 
          },    
}

#       7
#      /
#     3
#    / \
#   1   8
#  / \ 
# 0   4-9
#  \   \
#   2-5-10
#    \ \ 
#     6-11
#      \
#       12
BoardLayout3 = {
    0 : { 
          'links' : (1,2),
          'pos' : (0,0,0),
          },
    1 : {
          'links' : (3,4),
          'pos' : (xInc,2*yInc,0),    
          },
    2 : { 
          'links' : (5,6),
          'pos' : (xInc,-3*yInc,0),
          },
    3 : {
          'links' : (7,8),
          'pos' : (2*xInc,4*yInc,0),    
          },
    4 : { 
          'links' : (9,10),
          'pos' : (2*xInc,0*yInc,0),
          },
    5 : {
          'links' : (10,11),
          'pos' : (2*xInc,-2 * yInc,0),    
          },
    6 : { 
          'links' : (11,12),
          'pos' : (2 * xInc, -4*yInc,0),
          },
    7 : {
          'links' : (),
          'pos' : (3*xInc , 5 * yInc,0),
          'baseBonus' : 2,
          },
    8 : { 
          'links' : (),
          'pos' : (3*xInc, 3 *yInc,0),
          'baseBonus' : 2,
          },
    9 : {
          'links' : (),
          'pos' : (3*xInc, 1*yInc,0),
          'baseBonus' : 2,
          },
    10 : { 
          'links' : (),
          'pos' : (3*xInc, -1*yInc,0),
          'baseBonus' : 1,
          },
    11 : {
          'links' : (),
          'pos' : (3*xInc, -3*yInc,0),
          'baseBonus' : 1 
          },
    12 : {
          'links' : (),
          'pos' : (3*xInc, -5*yInc,0),
          'baseBonus' : 2 
          },    
}

BoardLayouts = (BoardLayout0,BoardLayout1,BoardLayout2,BoardLayout3)
