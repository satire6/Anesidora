#from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
#from pandac.PandaModules import Vec4
import random

MAX_PLAYERS_PER_HOLE = 4
GOLF_BALL_RADIUS = 0.25 # the radius in feet of our golf ball
GOLF_BALL_VOLUME = 4.0 / 3.0 * 3.14159 * (GOLF_BALL_RADIUS)**3 # in cubic feet
GOLF_BALL_MASS = 0.5 # in pounds
GOLF_BALL_DENSITY = GOLF_BALL_MASS / GOLF_BALL_VOLUME

# surface type constants
GRASS_SURFACE = 0 # the default if you don't specify anyting
BALL_SURFACE = 1 # the golf ball
HARD_SURFACE = 2 # the barriers and blockers
HOLE_SURFACE = 3 # the hole
SLICK_SURFACE = 4 # low friction

# collide id constants
OOB_RAY_COLLIDE_ID = -1 # out of bounds ray
GRASS_COLLIDE_ID = 2
HARD_COLLIDE_ID = 3
TOON_RAY_COLLIDE_ID = 4
MOVER_COLLIDE_ID = 7
WINDMILL_BASE_COLLIDE_ID = 8
CAMERA_RAY_COLLIDE_ID = 10
BALL_COLLIDE_ID = 42
HOLE_CUP_COLLIDE_ID = 64
SKY_RAY_COLLIDE_ID = 78
SLICK_COLLIDE_ID = 13

#animations constants
BALL_CONTACT_FRAME = 9 # what frame does the swing anim hit the ball
BALL_CONTACT_TIME = (BALL_CONTACT_FRAME +1) / 24.0 # in seconds

# timing constants
AIM_DURATION = 60 # in seconds, amount of time for them to aim
TEE_DURATION = 15 # in seconds, amount of time for them to choose their tee spot

RANDOM_HOLES = True

# disconnect constants
KICKOUT_SWINGS = 2 # if reaches this number of swings without pressing control, kick him out

TIME_TIE_BREAKER = True # if true, total aim time is used to break ties


# This describes each course,
# name = a toony name to describe the course
# holeIds = which holes are valid for this course if its just an int
#   then it's assumed to have a weight of 1.  If it's a tuple
#   the first number is the holeId, the second number will be the weight of choosing
#   that holeId
# if len(holeIds) < numHoles, we recycle starting at the first holeId, if not randomized
# if len(holeIds) > numHoles, we don't use all of the holes
CourseInfo = {
         # no volcano, no windmills, little if any blockers/movers
    0: { 'name' : '', #TTLocalizer.GolfCourseNames[0],
         'numHoles' : 3,
         'holeIds' : (2,3,4,5,6,7,8,12,13,15,16),
         },
    1: { 'name' : '', #TTLocalizer.GolfCourseNames[1],
         'numHoles' : 6,
         'holeIds' : ( (0,5), (1,5),
                      2, 3, 4, 5, 6, 7, 8, 9, 10, (11,5), 12, 13, (14,5), 15,  16, 
                      (17,5), (20,5), (21,5), (22,5), (23,5), (24,5), (25,5), (26,5),
                      (28,5), (30,5), (31,5),(33,5), (34,5),
                      ),
       },
    2: { 'name' : '', #TTLocalizer.GolfCourseNames[2],
         'numHoles' : 9,
         'holeIds' :( (1,5), 4, 5, 6, 7,  8, 9, 10, 11, 12, 13, (14,5), 15,
                     (17,5), (18,20), (19,20), (20,20), (21,5), (22,5),
                     (23,20), (24,20), (25,20),(26,20), (27,20), (28,20), (29,20),
                     (30,5), (31,20), (32,20), (33,5), (34,20), (35,20)
                     ),
         # don't delete to quickly test all the holes
         # 'holeIds' : (0,1,2,3,4,5,6,7,8),
         # 'holeIds' : (9,10,11,12,13,14,15,16,17),
       },    
}

# This describes each hole
# name = a toony name to describe the hole
# par = what is the par for this hole
# maxSwing = if he can't sink the ball after enough tries, give him this score
# holePos = xyz position of the actual hole, may be more than 1, WARNING no longer used
# terrainModel = model to load and reparent to render, includes background scenery
# physicsData = actual node used under terrainModel used for physics
# blockers = which blockers to enable, 1 based
# optionalMovers = which optionalMovers to enable, 1 based
# add 18 to the holeId and you get the more difficult version of that hole
HoleInfo = {
    0: { 'name' : '', 
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole18.bam',
         'physicsData' : 'golfGreen18',
         'blockers' : (),
         'optionalMovers' : ()
         },
    1: { 'name' : '', 
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole1.bam',
         'physicsData' : 'golfGreen1',
         'blockers' : (),
         },
    2: { 'name' : '', 
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole2.bam',
         'physicsData' : 'golfGreen2',
         'blockers' : (),
         },
    3: { 'name' : '', 
         'par' : 2,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole3.bam',
         'physicsData' : 'golfGreen3',
         'blockers' : (),
         },    
    4: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole4.bam',
         'physicsData' : 'golfGreen4',
         'blockers' : (),
         },
    5: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' :  'phase_6/models/golf/hole5.bam',
         'physicsData' : 'golfGreen2',           
         'blockers' : (),
         },
    6: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' :'phase_6/models/golf/hole6.bam',
         'physicsData' : 'golfGreen6',           
         'blockers' : (),
         },
     7: { 'name' : '', 
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole7.bam',
         'physicsData' : 'golfGreen7',           
         'blockers' : (),
         },
    8: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole8.bam',
         'physicsData' : 'golfGreen8',           
         'blockers' : (),
         },
    9: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' :  'phase_6/models/golf/hole9.bam',
         'physicsData' : 'golfGreen9',           
         'blockers' : (2),
         },
    10: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' :  'phase_6/models/golf/hole10.bam',
         'physicsData' : 'golfGreen10',           
         'blockers' : (),
         },
    11: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole11.bam',
         'physicsData' : 'golfGreen11',           
         'blockers' : (),
         },
    12: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole12.bam',
         'physicsData' : 'golfGreen12',           
         'blockers' : (),
         },
    13: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole13.bam',
         'physicsData' : 'golfGreen13',           
         'blockers' : (),
         },
    14: { 'name' : '', # this has a windmill
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole14.bam',
         'physicsData' : 'golfGreen14',           
         'blockers' : (),
         },
    15: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole15.bam',
         'physicsData' : 'golfGreen15',             
         'blockers' : (),
         },
    16: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole16.bam',
         'physicsData' : 'golfGreen16',           
         'blockers' : (),
         },
    17: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole17.bam',
         'physicsData' : 'golfGreen17',               
         'blockers' : (),
         },
    18: { 'name' : '', 
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole18.bam',
         'physicsData' : 'golfGreen18',
         'blockers' : (1,2),
         'optionalMovers' : (1)
         },    
    19: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole1.bam',
         'physicsData' : 'golfGreen1',
         'blockers' : (2,5),
         },
    20: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole2.bam',
         'physicsData' : 'golfGreen2',
         'blockers' : (1,3),
         },
    21: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole3.bam',
         'physicsData' : 'golfGreen3',
         'blockers' : (1,2,3),
         },
    22: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole4.bam',
         'physicsData' : 'golfGreen4',
         'blockers' : (2),
         },
    23: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole5.bam',
         'physicsData' : 'golfGreen5',
         'blockers' : (3,4),
          'optionalMovers' : (1),
         },
    24: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole6.bam',
         'physicsData' : 'golfGreen6',
         'blockers' : (1),
          'optionalMovers' : (1),
         },
    25: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole7.bam',
         'physicsData' : 'golfGreen7',
         'blockers' : (3),
          'optionalMovers' : (1),
         },
    26: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole8.bam',
         'physicsData' : 'golfGreen8',
         'blockers' : (),
          'optionalMovers' : (1),
         },
    27: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole9.bam',
         'physicsData' : 'golfGreen9',
         'blockers' : (),
         'optionalMovers' : (1,2),
         },
    28: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole10.bam',
         'physicsData' : 'golfGreen10',
         'blockers' : (),
         'optionalMovers' : (1,2),
         },
    29: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole11.bam',
         'physicsData' : 'golfGreen11',
         'blockers' : (),
         'optionalMovers' : (1),
         },
    30: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole12.bam',
         'physicsData' : 'golfGreen12',
         'blockers' : (1,2,3,),
         },
    31: { 'name' : '',
         'par' : 4,
         'maxSwing' : 7,
         'terrainModel' : 'phase_6/models/golf/hole13.bam',
         'physicsData' : 'golfGreen13',
         'blockers' : (3,4),
         'optionalMovers' : (1),
         },
    32: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole14.bam',
         'physicsData' : 'golfGreen14',
         'blockers' : (1),
         'optionalMovers' : (1),
         },
    33: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole15.bam',
         'physicsData' : 'golfGreen15',
         'blockers' : (1,2,3),
         'optionalMovers' : (1,2),          
         },
    34: { 'name' : '',
         'par' : 3,
         'maxSwing' : 6,
         'terrainModel' : 'phase_6/models/golf/hole16.bam',
         'physicsData' : 'golfGreen16',
         'blockers' : (1,2,5,6),
         'optionalMovers' : (1),          
         },
    35: { 'name' : '',
         'par' : 4,
         'maxSwing' : 7,
         'terrainModel' : 'phase_6/models/golf/hole17.bam',
         'physicsData' : 'golfGreen17',
         'blockers' : (3,4,5),
         },    
}

# fixup blockers, optionalMovers, make sure they are tuple
for holeId in HoleInfo:
   if type(HoleInfo[holeId]['blockers']) == type(0):
      blockerNum = HoleInfo[holeId]['blockers']
      HoleInfo[holeId]['blockers'] = (blockerNum,)
   if HoleInfo[holeId].has_key('optionalMovers'):
      if type(HoleInfo[holeId]['optionalMovers']) == type(0):
         blockerNum = HoleInfo[holeId]['optionalMovers']
         HoleInfo[holeId]['optionalMovers'] = (blockerNum,)      
   
   

# TODO once we have real hole geometry this can be reduced from 5
DistanceToBeInHole = 0.75 # how many feet from the hole bottom center to be considered inside the hole

# Golf History  indices   # amount needed to get a new trophy
CoursesCompleted = 0
CoursesUnderPar = 1
HoleInOneShots = 2
EagleOrBetterShots= 3
BirdieOrBetterShots = 4
ParOrBetterShots = 5
MultiPlayerCoursesCompleted = 6  
CourseZeroWins = 7     
CourseOneWins = 8    
CourseTwoWins = 9

TwoPlayerWins = 10  
ThreePlayerWins = 11
FourPlayerWins = 12

MaxHistoryIndex = 9
NumHistory = MaxHistoryIndex + 1

# Display other people's hole and course bests when achieved
CalcOtherHoleBest = False
CalcOtherCourseBest = False

# Trophies can be computed from the history, so no need to store it in the db

TrophyRequirements = {
    CoursesCompleted :   (4, 40, 400),
    CoursesUnderPar :    (1, 10, 100),
    HoleInOneShots :     (1, 10, 100),
    EagleOrBetterShots : (2, 20, 200),    
    BirdieOrBetterShots :(3, 30, 300),
    ParOrBetterShots :   (4, 40, 400),    
    MultiPlayerCoursesCompleted :    (6, 60, 600),
    CourseZeroWins :     (1, 10, 100),
    CourseOneWins :      (1, 10, 100),
    CourseTwoWins :      (1, 10, 100),
    #TwoPlayerWins :    (1, 10, 100),
    #ThreePlayerWins :    (1, 10, 100),
    #FourPlayerWins :     (1, 10, 100),    

}

# Colors taken from the avatar choice panel
# Affects toon panel and golf ball color
PlayerColors = [
   (0.925, 0.168, 0.168, 1),
   (0.13, 0.59, 0.973, 1),
   (0.973, 0.809, 0.129, 1),
   (0.598, 0.402, 0.875, 1),
   ]

# Kart colors stored in r,g,b (the horizontal array) for easy, medium, and hard courses (the vertical array)
KartColors = [
   [ [0, 50], [90, 255], [0, 85] ],
   [ [160, 255], [-15, 15], [0,120] ],
   [ [160, 255], [0, 110], [0, 110] ],
   ]

NumTrophies = 0
for key in TrophyRequirements:
   NumTrophies += len(TrophyRequirements[key])
NumCups = 3
TrophiesPerCup = NumTrophies / NumCups
               
def calcTrophyListFromHistory( history):
   """Return a list of booleans, with True meaning he has trophy.

   The first item (index 0) is for 4 courses completed.
   Last item is for 100 course two wins."""
   retval = []
   historyIndex = 0
   for trophyIndex in xrange(NumHistory):
       requirements = TrophyRequirements[trophyIndex]
       for amountNeeded in requirements:
           if history[historyIndex] >= amountNeeded:
               retval.append(True)
           else:
               retval.append(False)
       historyIndex += 1
   return retval
           

def calcCupListFromHistory( history):
   """Return a list of booleans, with True meaning he has the cup.

   The first item (index 0)is for 10 trophies won. next is 20 trophies won.
   Last item is for 30 trophies won."""
   retval = [False] * NumCups
   trophyList = calcTrophyListFromHistory(history)
   numTrophiesWon = 0
   for gotTrophy in trophyList:
      if gotTrophy:
         numTrophiesWon += 1
   for cupIndex in xrange(len(retval)):
      threshold = (cupIndex + 1) * TrophiesPerCup
      if threshold <= numTrophiesWon:
         retval[cupIndex] = True
   return retval
   
def getCourseName(courseId):
   """Return the name of the course."""
   from toontown.toonbase import TTLocalizer
   if courseId in CourseInfo:
      if not CourseInfo[courseId]['name']:
         CourseInfo[courseId]['name'] = TTLocalizer.GolfCourseNames[courseId]
      return CourseInfo[courseId]['name']
   else:
      return ''

   
def getHoleName(holeId):
   """Return the name of the hole."""
   from toontown.toonbase import TTLocalizer
   if holeId in HoleInfo :
      if not HoleInfo[holeId]['name']:
         HoleInfo[holeId]['name'] = TTLocalizer.GolfHoleNames[holeId]
      return HoleInfo[holeId]['name']
   else:
      return ''

def getHistoryIndexForTrophy(trophyIndex):
   """Returns the corresponding history the trophy is based on. -1 on error."""
   retval = -1
   # this shortcut will work since each trophy requirement has a 3 tuple
   # definitely change this if we have varying tuple lengths
   divBy3 = int(trophyIndex / 3)
   if divBy3 < NumHistory:
      retval = divBy3
   return retval

def packGolfHoleBest(holeBest):
   """Returns a packed version of the holeBest uint8 list."""
   retval = []
   shiftLeft = False
   for hole in holeBest:      
      hole &= 0xF
      if shiftLeft:
         retval[-1] |= (hole <<4)
         shiftLeft = False
      else:
         retval.append(hole)
         shiftLeft = True         
   return retval

def unpackGolfHoleBest(packedHoleBest):
   """Returns an unpacked version of the holeBest uint8 list."""
   retval = []
   for packedHole in packedHoleBest:
      lowbitHole = packedHole & 0xF
      retval.append(lowbitHole)
      highBitHole = (packedHole &0xF0) >> 4
      retval.append(highBitHole)
   return retval
