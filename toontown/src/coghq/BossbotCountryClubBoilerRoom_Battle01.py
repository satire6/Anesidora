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
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE08a',
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
    # GAGBARREL
    10006: {
        'type': 'gagBarrel',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10005,
        'pos': Point3(-23.8955783844,-29.8914642334,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'gagLevel': 5,
        'gagLevelMax': 0,
        'gagTrack': 'random',
        'rewardPerGrab': 5,
        'rewardPerGrabMax': 7,
        }, # end entity 10006
    # HEALBARREL
    10007: {
        'type': 'healBarrel',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10005,
        'pos': Point3(-7.71000003815,6.03817367554,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'rewardPerGrab': 5,
        'rewardPerGrabMax': 8,
        }, # end entity 10007
    # LOCATOR
    10001: {
        'type': 'locator',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'searchPath': '**/EXIT',
        }, # end entity 10001
    # MODEL
    10002: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10001,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/VaultDoorCover.bam',
        }, # end entity 10002
    10011: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(34.3037414551,6.2506942749,0.0),
        'hpr': Vec3(306.869903564,0.0,0.0),
        'scale': Vec3(1.22879016399,1.22879016399,1.22879016399),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/boiler_A2.bam',
        }, # end entity 10011
    10012: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(-37.5963821411,0.68013381958,0.0),
        'hpr': Vec3(45.0,0.0,0.0),
        'scale': Vec3(0.761251866817,0.761251866817,0.761251866817),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_D1.bam',
        }, # end entity 10012
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,68.932258606,9.97146701813),
        'hpr': Vec3(270.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10000
    10003: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10003
    10004: {
        'type': 'nodepath',
        'name': 'lower',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10004
    10005: {
        'type': 'nodepath',
        'name': 'barrels',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10005
    10008: {
        'type': 'nodepath',
        'name': 'upperLevel',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,65.4967575073,9.99451065063),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10008
    10013: {
        'type': 'nodepath',
        'name': 'product',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(0.0,17.8199996948,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10013
    10023: {
        'type': 'nodepath',
        'name': 'shelves',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(0.0,1.89410364628,0.0),
        'hpr': Point3(90.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10023
    10027: {
        'type': 'nodepath',
        'name': 'row1',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(0.0,-32.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10027
    10032: {
        'type': 'nodepath',
        'name': 'row2',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(0.0,-14.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10032
    10039: {
        'type': 'nodepath',
        'name': 'row3',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(0.0,4.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10039
    10048: {
        'type': 'nodepath',
        'name': 'row4',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(0.0,22.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10048
    10055: {
        'type': 'nodepath',
        'name': 'row5',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(0.0,40.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10055
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
