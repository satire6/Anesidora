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
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE11a',
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
    # MINTPRODUCT
    10024: {
        'type': 'mintProduct',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(-4.0706076622,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12500,
        }, # end entity 10024
    # MINTSHELF
    10003: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12600,
        }, # end entity 10003
    10005: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10006,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12600,
        }, # end entity 10005
    10007: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 10006,
        'pos': Point3(13.4306573868,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12600,
        }, # end entity 10007
    10009: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(-13.4300003052,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12600,
        }, # end entity 10009
    10013: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(-13.4300003052,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12600,
        }, # end entity 10013
    10014: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10011,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12600,
        }, # end entity 10014
    10015: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10012,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12600,
        }, # end entity 10015
    10016: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 10012,
        'pos': Point3(13.4306573868,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12600,
        }, # end entity 10016
    # MODEL
    10001: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,22.2368240356,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/VaultDoorCover.bam',
        }, # end entity 10001
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10000
    10002: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10002
    10004: {
        'type': 'nodepath',
        'name': 'backWall',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(0.0,19.0782051086,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10004
    10006: {
        'type': 'nodepath',
        'name': 'rightShelves',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(17.2106304169,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10006
    10008: {
        'type': 'nodepath',
        'name': 'leftShelves',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(-17.4771251678,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10008
    10010: {
        'type': 'nodepath',
        'name': 'frontWall',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(0.0,-19.1254119873,0.0),
        'hpr': Point3(180.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10010
    10011: {
        'type': 'nodepath',
        'name': 'leftShelves',
        'comment': '',
        'parentEntId': 10010,
        'pos': Point3(-17.4771251678,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10011
    10012: {
        'type': 'nodepath',
        'name': 'rightShelves',
        'comment': '',
        'parentEntId': 10010,
        'pos': Point3(17.2106304169,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10012
    10023: {
        'type': 'nodepath',
        'name': 'byVaultDoor',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(0.0,16.0373382568,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10023
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
