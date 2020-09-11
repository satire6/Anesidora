from pandac.PandaModules import *

CRATE_CLEAR   = 0
CRATE_POWERUP = 1
CRATE_PUSH    = 2

CrateNormals = [Vec3(1,0,0),
                Vec3(-1,0,0),
                Vec3(0,1,0),
                Vec3(0,-1,0)]
CrateHprs = [Vec3(90,0,0),
             Vec3(270,0,0),
             Vec3(180,0,0),
             Vec3(0,0,0)]

T_PUSH = 1.5
T_PAUSE = .1

TorsoToOffset = {"ss" : .17,
                 "ms" : .18,
                 "ls" : .75,
                 "sd" : .17,
                 "md" : .18,
                 "ld" : .75,
                 "s" : .17,
                 "m" : .18,
                 "l" : .75,
                 }
                 
