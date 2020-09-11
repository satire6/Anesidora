from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import BitMask32

NumVines = 20 # how many vines in the game
GameDuration = 70 # in seconds how long does the game last
ShowScoresDuration = 4. # in seconds, how long to display the player's score
VineStartingT = 0.25 # when game starts where are they in vine 0
VineFellDownT = 0.1 # when they fall, where to place them on the last vine
EndlessGame = False # continue even whe timer expires        

BonusPerSecondLeft = 0.4 # for each second left how many more points to give
JumpTimeBuffer = 0.5 # how soon to check collision on the vine we came from
SpiderBitmask = ToontownGlobals.CatchGameBitmask # bitmask for the spider and bat
TreasureBitmask = ToontownGlobals.PieBitmask # bitmask for the banana treasure
VineXIncrement = 30 # in feet how far apart are they spaced
VineHeight = 30 # how high is the vine
BatMaxHeight = 28 # maximum height bat flies
BatMinHeight = 10 # minimum height bat flies
RadarCameraBitmask = BitMask32.bit(3) # bitmask for the radar camera
    

# each course section will cover 5 vines,
# the harder difficulties will use the later sections
# the first and last vine must always be able to connect to each other
# spiders must not be next to each other
# each vine tuple specifies the length, angle, vinePeriod and spider period, 0 if no spider
# the harder sections should be towards the end
CourseSections = (
    # easiest, long vines and big angles
    ((20, 30, 4, 0), (19, 39, 3.1, 0), (18, 41, 4, 0), (19,38,3.2,0), (20,30,6,0)),
    # shorter angles
    ((20, 30, 3, 0), (18, 40, 4.1, 0), (19, 31, 5.1, 0), (18,41,4.2,0), (20,30,5,0)),
    # first challenge, shorter vines
    ((20, 30, 3, 0), (15, 39, 4.1, 0), (19, 29, 5, 0), (16,38,4.2,0), (20,30,5,0)),
    # first occurrence of spider
    ((20, 30, 3, 0), (18, 36, 4.1, 0), (19, 30, 5, 9), (18,38,4.2,0), (20,30,5,0)),
    # small angles now
    ((20, 30, 3, 0), (18, 15, 4.1, 0), (19, 30, 5, 11), (18,16,4.2,0), (20,30,5,0)),
    # two small angles in a row
    ((20, 30, 3, 0), (18, 11, 4.1, 0), (15, 12, 5, 0), (18,16,4.2,0), (20,30,5,0)),
    # spider on a short vine
    ((20, 30, 3, 0), (15, 39, 4.1, 13), (19, 29, 5, 0), (16,38,4.2,0), (20,30,5,0)),
    # 2 spiders
    ((20, 30, 3, 0), (18, 26, 4.1, 9), (19, 30, 5, 0), (18,28,4.2,12), (20,30,5,0)),
    # 2 spiders on short vines
    ((20, 30, 3, 0), (15, 26, 4.1, 9), (19, 30, 5, 0), (15,28,4.2,12), (20,30,5,0)),

    # test only
    ((15, 50, 4, 0), (15, 40, 4.1, 0), (19, 40, 5, 0), (19,28,4.2,0), (20,30,5,0)),
    )

# each tuple references a course section, and how many times that can be chosen
# recommended but not required that they add up to 100
CourseWeights = {
    ToontownGlobals.ToontownCentral : ( (0,25), (1,25), (2,25), (3,25) ),
    ToontownGlobals.DonaldsDock : ( (1,25), (2,25), (3,25), (4,25) ),
    ToontownGlobals.DaisyGardens :  ( (2,25), (3,25), (4,25), (5,25) ), 
    ToontownGlobals.MinniesMelodyland:  ( (3,25), (4,25), (5,25), (6,25) ),
    ToontownGlobals.TheBrrrgh: ( (4,25), (5,25), (6,25), (7,25) ),
    ToontownGlobals.DonaldsDreamland: ( (4,20), (5,20), (6,20), (7,20), (8,20) ),
    }

 # extra points to award when they reach end vine
BaseBonusOnEndVine = {
    ToontownGlobals.ToontownCentral : 4,
    ToontownGlobals.DonaldsDock : 5,
    ToontownGlobals.DaisyGardens : 6, 
    ToontownGlobals.MinniesMelodyland: 7,
    ToontownGlobals.TheBrrrgh: 8,
    ToontownGlobals.DonaldsDreamland: 9,
    }

# first number is how many seconds it takes for the bat to traverse entire field
# second number is how many seconds to wait before it starts
# third number, if any, is where in the field it starts 0..1, 1 meaning it starts at the end
BatInfo = {
    ToontownGlobals.ToontownCentral : ( (60, 0, 0.35),),
    ToontownGlobals.DonaldsDock : ( (60, 0, 0.25), (30,30)),
    ToontownGlobals.DaisyGardens :  ( (60, 0, 0.25), (15,30) ), 
    ToontownGlobals.MinniesMelodyland:  (  (60, 0, 0.25), (10,25)  ),
    ToontownGlobals.TheBrrrgh: ((60, 0, 0.25), (30,30), (30, 20) ),
    ToontownGlobals.DonaldsDreamland: ( (60, 0, 0.25), (30,30), (10, 20)),
}

# for each difficulty, what is the maximum number of spiders, the course
# can have less than the maximum numbre of spiders
SpiderLimits = {
    ToontownGlobals.ToontownCentral : 1,
    ToontownGlobals.DonaldsDock : 2,
    ToontownGlobals.DaisyGardens : 2,
    ToontownGlobals.MinniesMelodyland:  3,
    ToontownGlobals.TheBrrrgh: 3,
    ToontownGlobals.DonaldsDreamland: 4
}
    
   
def getNumSpidersInSection( sectionIndex):
    if sectionIndex <0 or sectionIndex >= len(CourseSections):
        return 0
    numSpiders = 0
    for vine in CourseSections[sectionIndex]:
        if vine[3]:
            numSpiders += 1
    return numSpiders
    
