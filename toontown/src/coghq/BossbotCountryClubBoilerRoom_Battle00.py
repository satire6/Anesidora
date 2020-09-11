from toontown.coghq.SpecImports import *

GlobalEntities = {
    # LEVELMGR
    1000: {
        'type': 'levelMgr',
        'name': 'LevelMgr',
        'comment': '',
        'parentEntId': 0,
        'cogLevel': 0,
        'farPlaneDistance': 1500,
        'modelFilename': 'phase_12/models/bossbotHQ/BossbotKartBoardingRm',
        'wantDoors': 1,
        }, # end entity 1000
    # EDITMGR
    1001: {
        'type': 'editMgr',
        'name': 'EditMgr',
        'parentEntId': 0,
        'insertEntity': None,
        'removeEntity': None,
        'requestNewEntity': None,
        'requestSave': None,
        }, # end entity 1001
    # ZONE
    0: {
        'type': 'zone',
        'name': 'UberZone',
        'comment': '',
        'parentEntId': 0,
        'scale': 1,
        'description': '',
        'visibility': [],
        }, # end entity 0
    # BATTLEBLOCKER
    10001: {
        'type': 'battleBlocker',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(-1.02925205231,87.0907745361,11.8959827423),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'cellId': 0,
        'radius': 10.0,
        }, # end entity 10001
    10006: {
        'type': 'battleBlocker',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(-60.9065246582,-3.26905798912,0.117109239101),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'cellId': 1,
        'radius': 15.0,
        }, # end entity 10006
    10047: {
        'type': 'battleBlocker',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10013,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Point3(1.0,0.20000000298,1.0),
        'cellId': 2,
        'radius': 20.0,
        }, # end entity 10047
    # GAGBARREL
    10041: {
        'type': 'gagBarrel',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10033,
        'pos': Point3(5.40611028671,0.0,0.0),
        'hpr': Vec3(199.440032959,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'gagLevel': 5,
        'gagLevelMax': 0,
        'gagTrack': 'random',
        'rewardPerGrab': 4,
        'rewardPerGrabMax': 6,
        }, # end entity 10041
    # HEALBARREL
    10034: {
        'type': 'healBarrel',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10033,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(163.300750732,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'rewardPerGrab': 7,
        'rewardPerGrabMax': 9,
        }, # end entity 10034
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(0.0,66.1200027466,10.1833248138),
        'hpr': Point3(270.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10000
    10002: {
        'type': 'nodepath',
        'name': 'battle',
        'comment': '',
        'parentEntId': 10000,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Point3(90.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10002
    10003: {
        'type': 'nodepath',
        'name': 'cogs2',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(-53.9246749878,-22.7616195679,0.0),
        'hpr': Point3(45.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10003
    10005: {
        'type': 'nodepath',
        'name': 'battle',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10005
    10007: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10007
    10008: {
        'type': 'nodepath',
        'name': 'topWall',
        'comment': '',
        'parentEntId': 10007,
        'pos': Point3(0.0,48.0299987793,10.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10008
    10011: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10011
    10013: {
        'type': 'nodepath',
        'name': 'frontCogs',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(25.3957309723,-12.3005743027,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10013
    10014: {
        'type': 'nodepath',
        'name': 'frontPalletWall',
        'comment': '',
        'parentEntId': 10007,
        'pos': Point3(45.5494384766,38.2237281799,0.0),
        'hpr': Point3(180.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10014
    10021: {
        'type': 'nodepath',
        'name': 'middlePalletWallLeft',
        'comment': '',
        'parentEntId': 10046,
        'pos': Point3(6.0,-37.9928665161,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10021
    10023: {
        'type': 'nodepath',
        'name': 'crateIsland',
        'comment': '',
        'parentEntId': 10007,
        'pos': Point3(-23.1813278198,7.08758449554,0.00999999977648),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(2.0,2.0,2.0),
        }, # end entity 10023
    10028: {
        'type': 'nodepath',
        'name': 'rewardCulDeSac',
        'comment': '',
        'parentEntId': 10045,
        'pos': Point3(-8.26172065735,38.377407074,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10028
    10033: {
        'type': 'nodepath',
        'name': 'barrels',
        'comment': '',
        'parentEntId': 10028,
        'pos': Point3(-4.75077962875,34.1425209045,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10033
    10035: {
        'type': 'nodepath',
        'name': 'backPalletWall',
        'comment': '',
        'parentEntId': 10007,
        'pos': Point3(-47.6501731873,40.006893158,0.0),
        'hpr': Point3(180.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10035
    10040: {
        'type': 'nodepath',
        'name': 'centerCogs',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(-23.9375743866,28.353269577,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10040
    10045: {
        'type': 'nodepath',
        'name': 'middlePalletWallRight',
        'comment': '',
        'parentEntId': 10046,
        'pos': Point3(17.4200000763,-38.2999992371,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10045
    10046: {
        'type': 'nodepath',
        'name': 'middlePalletWall',
        'comment': '',
        'parentEntId': 10007,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10046
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
