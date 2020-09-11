import math
from pandac.PandaModules import Point3
from toontown.toonbase import ToontownGlobals

# in seconds, how many seconds do we wait for them to decide
InputTimeout = 15

# in secons, how many seconds do we wait for the tire movie to finish
TireMovieTimeout = 120

MinWall = (-20.0, -15.0) # lower left corner of fence
MaxWall = (20.0, 15.0) # upper right corner of fence

TireRadius = 1.5 # in feet

WallMargin = 1 + TireRadius
StartingPositions = ( Point3(MinWall[0] + WallMargin, # bottomLeft
                             MinWall[1] + WallMargin,
                             TireRadius),
                      Point3(MaxWall[0] - WallMargin, # topRight
                             MaxWall[1] - WallMargin,
                             TireRadius),
                      Point3(MinWall[0] + WallMargin, # topLeft
                             MaxWall[1] - WallMargin,
                             TireRadius),
                      Point3(MaxWall[0] - WallMargin, # bottomRight
                             MinWall[1] + WallMargin,
                             TireRadius),
                      )
                          
NumMatches = 3 # how many matches for the whole game
NumRounds = 2 # how many rounds per match

# how many points do you get when you're at dead center,
# key is number of players
PointsDeadCenter = {
    0: 5,
    1: 5,
    2: 5,
    3: 4,
    4: 3,
    }
PointsInCorner = 1 # how many points do you get when you're as far as you can be
FarthestLength = math.sqrt( ((MaxWall[0]-TireRadius) * (MaxWall[0]-TireRadius)) + ((MaxWall[1]-TireRadius)*(MaxWall[1]-TireRadius)))
BonusPointsForPlace = (3, 2, 1, 0) # Bonus points awarded for 1st, 2nd, 3rd, 4th

ExpandFeetPerSec = 5 # how fast does the scoring circle expand
#ScoreIncreaseDuration = 3 # how long does a players score increase

ScoreCountUpRate  = 0.15 # in seconds how long does increasint a point take

ShowScoresDuration = 4. # in seconds, how long to display the player's score

# for each safezone, how many treasures do we put
NumTreasures = {
     ToontownGlobals.ToontownCentral : 2,
     ToontownGlobals.DonaldsDock : 2,
     ToontownGlobals.DaisyGardens : 2, 
     ToontownGlobals.MinniesMelodyland: 2,
     ToontownGlobals.TheBrrrgh: 1,
     ToontownGlobals.DonaldsDreamland: 1,
     }

# for each safezone, how many penalties do we put
NumPenalties = {
     ToontownGlobals.ToontownCentral : 0,
     ToontownGlobals.DonaldsDock : 1,
     ToontownGlobals.DaisyGardens : 1, 
     ToontownGlobals.MinniesMelodyland: 1,
     ToontownGlobals.TheBrrrgh: 2,
     ToontownGlobals.DonaldsDreamland: 2,
     }

# for each safezone, where the obstacles go
Obstacles = {
     ToontownGlobals.ToontownCentral : (),
     ToontownGlobals.DonaldsDock : ((0,0),),
     ToontownGlobals.DaisyGardens : ((MinWall[0]/2,0), (MaxWall[0]/2,0)), 
     ToontownGlobals.MinniesMelodyland: ((0,MinWall[1]/2), (0, MaxWall[1]/2)), 
     ToontownGlobals.TheBrrrgh: ((MinWall[0]/2,0),
                                 (MaxWall[0]/2 , 0),
                                 (0,MinWall[1]/2),
                                 (0,MaxWall[1]/2) ), 
     ToontownGlobals.DonaldsDreamland: ( ( MinWall[0]/2, MinWall[1]/2),
                                         ( MinWall[0]/2, MaxWall[1]/2),
                                         ( MaxWall[0]/2, MinWall[1]/2),
                                         ( MaxWall[0]/2, MaxWall[1]/2),
                                         ),
     }

# for each safezone, if we use cubic obstacles (false means cylindrical)
ObstacleShapes = {
     ToontownGlobals.ToontownCentral : True ,
     ToontownGlobals.DonaldsDock : True ,
     ToontownGlobals.DaisyGardens : True, 
     ToontownGlobals.MinniesMelodyland: True, 
     ToontownGlobals.TheBrrrgh: False, 
     ToontownGlobals.DonaldsDreamland: False ,
     }
    
