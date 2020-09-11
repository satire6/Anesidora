"""LawOfficeFloorSpecs.py: contains table of lawoffice floor specs"""

from direct.showbase.PythonUtil import invertDict
from toontown.toonbase import ToontownGlobals
from toontown.coghq import NullCogs
from toontown.coghq import LabotOfficeFloor_01a_Cogs
from toontown.coghq import LabotOfficeFloor_01b_Cogs


def getLawOfficeFloorSpecModule(floorId):
    return LawbotOfficeSpecModules[floorId]

def getCogSpecModule(floorId):
    floor = LawbotOfficeFloorId2FloorName[roomId]
    return CogSpecModules.get(floorId, NullCogs)

def getNumBattles(floorId):
    return floorId2numBattles[floorId]

# things that rooms need:
# r: reward (barrels, etc.)
# s: safe(s)
# x: adjust prop positions

LawbotOfficeFloorId2FloorName = {
     0: 'LabotOfficeFloor_01_a',
     1: 'LabotOfficeFloor_01_b',
    }
    
LawbotOfficeFloorName2FloorId = invertDict(LawbotOfficeFloorId2FloorName)

LawbotOfficeEntranceIDs   = (0,1)
LawbotOfficeFloorIDs = (0,1)

# dict of roomId to spec Python module
LawbotOfficeSpecModules = {}
for roomName, roomId in LawbotOfficeFloorName2FloorId.items():
    exec 'from toontown.coghq import %s' % roomName
    LawbotOfficeSpecModules[roomId] = eval(roomName)

## until cogs are entities...
CogSpecModules = {
    'CashbotMintBoilerRoom_Battle00' : LabotOfficeFloor_01a_Cogs,
    'CashbotMintBoilerRoom_Battle01' : LabotOfficeFloor_01b_Cogs,
    }

floorId2numBattles = {}
for roomName, roomId in LawbotOfficeFloorName2FloorId.items():
    if roomName not in CogSpecModules:
        floorId2numBattles[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        floorId2numBattles[roomId] = len(cogSpecModule.BattleCells)
