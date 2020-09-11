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
        'modelFilename': 'phase_11/models/lawbotHQ/LB_Zone7a',
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
        'parentEntId': 0,
        'pos': Point3(8.03298, 23.7306, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'cellId': 0,
        'radius': 15.0,
        }, # end entity 10001
    # MODEL
    100001: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(15.6666, -22.49, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB',
        }, # end entity 100001
    100002: {
        'type': 'model',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-8.21365, 18.3459, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox',
        }, # end entity 100002
    100003: {
        'type': 'model',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-17.6094, 17.5472, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox',
        }, # end entity 100003
    100004: {
        'type': 'model',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(51.1181, -21.6279, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB',
        }, # end entity 100004
    100005: {
        'type': 'model',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(39.917, -25.2425, 0),
        'hpr': Vec3(180, 0, 0),
        'scale': Vec3(1.5, 1.5, 1.5),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_filing_cabB',
        }, # end entity 100005
    100006: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(36.8762, -25.0662, 0),
        'hpr': Vec3(180, 0, 0),
        'scale': Vec3(1.5, 1.5, 1.5),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_filing_cabA',
        }, # end entity 100006
    100007: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(42.9283, -25.1704, 0),
        'hpr': Vec3(180, 0, 0),
        'scale': Vec3(1.5, 1.5, 1.5),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_filing_cabA',
        }, # end entity 100007
    100008: {
        'type': 'model',
        'name': 'copy of <unnamed> (5)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(55.8945, -14.0806, 0.05),
        'hpr': Vec3(90, 0, 0),
        'scale': Vec3(1.5, 1.5, 1.5),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_deskA',
        }, # end entity 100008
    100009: {
        'type': 'model',
        'name': 'copy of <unnamed> (6)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(55.8945, 5.46793, 0),
        'hpr': Vec3(90, 0, 0),
        'scale': Vec3(1.5, 1.5, 1.5),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_deskA',
        }, # end entity 100009
    100010: {
        'type': 'model',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(51.1181, -2.86719, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB',
        }, # end entity 100010
    100011: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(49.0929, 21.7054, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA',
        }, # end entity 100011
    100012: {
        'type': 'model',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-8.21365, -63.6967, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox',
        }, # end entity 100012
    100013: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-8.21365, -57.4073, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox',
        }, # end entity 100013
    100014: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-15.1195, -63.5076, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox',
        }, # end entity 100014
    100015: {
        'type': 'model',
        'name': 'copy of <unnamed> (5)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-0.987966, -63.5446, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox',
        }, # end entity 100015
    100016: {
        'type': 'model',
        'name': 'copy of <unnamed> (6)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(6.21987, -63.5446, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox',
        }, # end entity 100016
    100017: {
        'type': 'model',
        'name': 'copy of <unnamed> (7)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(6.21987, -63.5446, 5.45351),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_CardBoardBox',
        }, # end entity 100017
    100018: {
        'type': 'model',
        'name': 'copy of <unnamed> (7)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-38.1114, -20.025, 0),
        'hpr': Vec3(175.135, 0, 0),
        'scale': Vec3(1.81307, 1.81307, 1.81307),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA',
        }, # end entity 100018
    100019: {
        'type': 'model',
        'name': 'copy of <unnamed> (8)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-38.1114, 16.2551, 0),
        'hpr': Vec3(3.01279, 0, 0),
        'scale': Vec3(1.44025, 1.44025, 1.44025),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_chairA',
        }, # end entity 100019
    100020: {
        'type': 'model',
        'name': 'copy of <unnamed> (9)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-55.9616, 16.2551, 0),
        'hpr': Vec3(3.01279, 0, 0),
        'scale': Vec3(1.44025, 1.44025, 1.44025),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_chairA',
        }, # end entity 100020
    100021: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-45.4842, 16.387, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA',
        }, # end entity 100021
    100022: {
        'type': 'model',
        'name': 'copy of <unnamed> (8)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(12.856, -33.9782, 0),
        'hpr': Vec3(270, 0, 0),
        'scale': Vec3(1.81307, 1.81307, 1.81307),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA',
        }, # end entity 100022
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Point3(270, 0, 0),
        'scale': 1,
        }, # end entity 10000
    100000: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0.05),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 100000
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
