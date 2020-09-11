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
    # ATTRIBMODIFIER
    10055: {
        'type': 'attribModifier',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10001,
        'attribName': 'modelPath',
        'recursive': 1,
        'typeName': 'model',
        'value': '',
        }, # end entity 10055
 
    # NODEPATH
    10001: {
        'type': 'nodepath',
        'name': 'crates',
        'comment': '',
        'parentEntId': 10028,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1.3, 1.3, 1.64892),
        }, # end entity 10001
    10002: {
        'type': 'nodepath',
        'name': 'rewardBarrels',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-0.719734, 56.9691, 10.0021),
        'hpr': Vec3(61.6992, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 10002
    10003: {
        'type': 'nodepath',
        'name': 'upperWall',
        'comment': 'TODO: replace with lines of shelves',
        'parentEntId': 0,
        'pos': Point3(-20.3203, 52.6549, 9.90873),
        'hpr': Vec3(270, 0, 0),
        'scale': Vec3(1.1143, 1.1143, 1.1143),
        }, # end entity 10003
    10009: {
        'type': 'nodepath',
        'name': 'toGear0',
        'comment': '',
        'parentEntId': 10001,
        'pos': Point3(-26.5593, 31.856, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 10009
    10011: {
        'type': 'nodepath',
        'name': 'toGear1',
        'comment': '',
        'parentEntId': 10001,
        'pos': Point3(-25.884, 13.6749, 0),
        'hpr': Vec3(41.6335, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 10011
    10023: {
        'type': 'nodepath',
        'name': 'leftWall',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 10023
    10024: {
        'type': 'nodepath',
        'name': 'rightWall',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(-26.7112, 6.85982, 0),
        'hpr': Point3(180, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 10024
    10028: {
        'type': 'nodepath',
        'name': 'lowerPuzzle',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0.05),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 10028
    10029: {
        'type': 'nodepath',
        'name': 'entranceWall',
        'comment': '',
        'parentEntId': 10001,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 10029
    10032: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 10032
    10038: {
        'type': 'nodepath',
        'name': 'archStompers',
        'comment': '',
        'parentEntId': 10028,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 10038
    10040: {
        'type': 'nodepath',
        'name': 'backWall',
        'comment': '',
        'parentEntId': 10001,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 10040
    10044: {
        'type': 'nodepath',
        'name': 'gear',
        'comment': '',
        'parentEntId': 10028,
        'pos': Point3(11.85, -11.38, 12.528),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 10044
    10046: {
        'type': 'nodepath',
        'name': 'supportedCrateBackWall',
        'comment': '',
        'parentEntId': 10028,
        'pos': Point3(34.9045, -34.0589, -1.51687),
        'hpr': Vec3(63.4349, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 10046
    10051: {
        'type': 'nodepath',
        'name': 'supportedCrateEntrance',
        'comment': '',
        'parentEntId': 10028,
        'pos': Point3(48.5077, 7.75915, 0.357897),
        'hpr': Point3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 10051
    10059: {
        'type': 'nodepath',
        'name': 'largeStack',
        'comment': '',
        'parentEntId': 10029,
        'pos': Point3(47.98, -16.98, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 10059
    10061: {
        'type': 'nodepath',
        'name': 'lower',
        'comment': '',
        'parentEntId': 10059,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 10061
    100001: {
        'type': 'nodepath',
        'name': 'trap1 cog node',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 100001
    # PATH
    100003: {
        'type': 'path',
        'name': 'test goon path',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-50.4808, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'pathIndex': 0,
        'pathScale': 1.0,
        }, # end entity 100003
        
    }


Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
