"""StageRoomSpecs.py: contains table of stage room specs"""

from direct.showbase.PythonUtil import invertDict
from toontown.toonbase import ToontownGlobals
from toontown.coghq import NullCogs
from toontown.coghq import LawbotOfficeOilRoom_Battle00_Cogs
from toontown.coghq import LawbotOfficeOilRoom_Battle01_Cogs
from toontown.coghq import LawbotOfficeBoilerRoom_Battle00_Cogs
from toontown.coghq import LawbotOfficeBoilerRoom_Trap00_Cogs
from toontown.coghq import LawbotOfficeLobby_Trap00_Cogs
from toontown.coghq import LawbotOfficeDiamondRoom_Trap00_Cogs
from toontown.coghq import LawbotOfficeDiamondRoom_Battle00_Cogs
from toontown.coghq import LawbotOfficeGearRoom_Battle00_Cogs

def getStageRoomSpecModule(roomId):
    return CashbotStageSpecModules[roomId]

def getCogSpecModule(roomId):
    roomName = CashbotStageRoomId2RoomName[roomId]
    return CogSpecModules.get(roomName, NullCogs)

def getNumBattles(roomId):
    return roomId2numBattles[roomId]

# things that rooms need:
# r: reward (barrels, etc.)
# s: safe(s)
# x: adjust prop positions

CashbotStageRoomId2RoomName = {
     0: 'LawbotOfficeEntrance_Action00', # entrance
     1: 'LawbotOfficeOilRoom_Battle00', # oil room (final)
     2: 'LawbotOfficeOilRoom_Battle01', # oil room (final)
     3: 'LawbotOfficeBoilerRoom_Security00',
     4: 'LawbotOfficeBoilerRoom_Battle00',
     5: 'LawbotOfficeGearRoom_Action00',
     6: 'LawbotOfficeLobby_Action00',
     7: 'LawbotOfficeGearRoom_Security00', # plus-room library with lights
     8: 'LawbotOfficeLobby_Trap00', # two laser puzzles
     9: 'LawbotOfficeDiamondRoom_Security00',
     10: 'LawbotOfficeDiamondRoom_Trap00', # diamond with laser grids
     11: 'LawbotOfficeGearRoom_Platform00', # crate stack with lifter/stompers
     12: 'LawbotOfficeLobby_Lights00', # barrels surrounded by lights
     100: 'LawbotOfficeBoilerRoom_Action01', # large room with many big goons
     101: 'LawbotOfficeDiamondRoom_Action00', # stompers and lights
     102: 'LawbotOfficeDiamondRoom_Action01', # filing cabinet wall, big goons
     103: 'LawbotOfficeLobby_Action01', # lights around central pillar, library maze
     104: 'LawbotOfficeDiamondRoom_Battle00',
     105: 'LawbotOfficeGearRoom_Battle00',
    }
CashbotStageRoomName2RoomId = invertDict(CashbotStageRoomId2RoomName)

CashbotStageEntranceIDs   = (0,)
CashbotStageMiddleRoomIDs = (1,)
CashbotStageFinalRoomIDs  = (2,)

#CashbotStageConnectorRooms = ('phase_10/models/cashbotHQ/connector_7cubeL2',
#                             'phase_10/models/cashbotHQ/connector_7cubeR2')
                             
CashbotStageConnectorRooms = ('phase_11/models/lawbotHQ/LB_connector_7cubeL2',
                             'phase_11/models/lawbotHQ/LB_connector_7cubeLR')

# dict of roomId to spec Python module
CashbotStageSpecModules = {}
for roomName, roomId in CashbotStageRoomName2RoomId.items():
    exec 'from toontown.coghq import %s' % roomName
    CashbotStageSpecModules[roomId] = eval(roomName)

## until cogs are entities...
CogSpecModules = {
    'LawbotOfficeOilRoom_Battle00' : LawbotOfficeOilRoom_Battle00_Cogs,
    'LawbotOfficeOilRoom_Battle01' : LawbotOfficeOilRoom_Battle01_Cogs,
    'LawbotOfficeBoilerRoom_Battle00' : LawbotOfficeBoilerRoom_Battle00_Cogs,
    'LawbotOfficeBoilerRoom_Trap00' : LawbotOfficeBoilerRoom_Trap00_Cogs,
    'LawbotOfficeLobby_Trap00' : LawbotOfficeLobby_Trap00_Cogs,
    'LawbotOfficeDiamondRoom_Trap00' : LawbotOfficeDiamondRoom_Trap00_Cogs,
    'LawbotOfficeDiamondRoom_Battle00' : LawbotOfficeDiamondRoom_Battle00_Cogs,
    'LawbotOfficeGearRoom_Battle00' : LawbotOfficeGearRoom_Battle00_Cogs,
    }

roomId2numBattles = {}
for roomName, roomId in CashbotStageRoomName2RoomId.items():
    if roomName not in CogSpecModules:
        roomId2numBattles[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        roomId2numBattles[roomId] = len(cogSpecModule.BattleCells)

roomId2numCogs = {}
for roomName, roomId in CashbotStageRoomName2RoomId.items():
    if roomName not in CogSpecModules:
        roomId2numCogs[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        roomId2numCogs[roomId] = len(cogSpecModule.CogData)

roomId2numCogLevels = {}
for roomName, roomId in CashbotStageRoomName2RoomId.items():
    if roomName not in CogSpecModules:
        roomId2numCogLevels[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        levels = 0
        for cogData in cogSpecModule.CogData:
            levels += cogData['level']
        roomId2numCogLevels[roomId] = levels

roomId2numMeritCogLevels = {}
for roomName, roomId in CashbotStageRoomName2RoomId.items():
    if roomName not in CogSpecModules or roomId in (8, 10): # HACK 8,10!
        roomId2numMeritCogLevels[roomId] = 0
    else:
        cogSpecModule = CogSpecModules[roomName]
        levels = 0
        for cogData in cogSpecModule.CogData:
            levels += cogData['level']
        roomId2numMeritCogLevels[roomId] = levels

# override # of battles for some rooms that don't have battle blockers for
# some battles
#name2id = CashbotStageRoomName2RoomId
#roomId2numBattles[name2id['CashbotStageBoilerRoom_Battle00']] = 3
#roomId2numBattles[name2id['CashbotStagePipeRoom_Battle00']] = 2
#del name2id

# make a table of middle rooms specifically, so StageLayout can easily pick
# and choose battle rooms to meet its battle quota
middleRoomId2numBattles = {}
for roomId in CashbotStageMiddleRoomIDs:
    middleRoomId2numBattles[roomId] = roomId2numBattles[roomId]
