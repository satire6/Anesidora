from toontown.coghq.SpecImports import *
import random

GlobalEntities = {
    # LEVELMGR
    1000: {
        'type': 'levelMgr',
        'name': 'LevelMgr',
        'comment': '',
        'parentEntId': 0,
        'cogLevel': 0,
        'farPlaneDistance': 1500,
        'modelFilename': 'phase_11/models/lawbotHQ/LB_Zone22a',
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
    100030: {
        'type': 'battleBlocker',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-0.942754, -16.0554, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'cellId': 0,
        'radius': 20.0,
        }, # end entity 100030
    # MODEL
    100001: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-0.345429, -31.6315, 0),
        'hpr': Point3(180, 0, 0),
        'scale': Point3(2.65, 2.55, 3.2),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfB',
        }, # end entity 100001
    100002: {
        'type': 'model',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(0, -31.6418, 20.1296),
        'hpr': Point3(180, 0, 0),
        'scale': Point3(2.65, 2.52, 3.2),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfB',
        }, # end entity 100002
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(180, 0, 0),
        'scale': 1,
        }, # end entity 10000
    100000: {
        'type': 'nodepath',
        'name': 'extra cases',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 100000
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [Scenario0,],
    'titleString' : ("MemTag: LawbotOfficeOilRoom_Battle01 %s" % (random.random()))    
    }
