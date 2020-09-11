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
        'modelFilename': 'phase_11/models/lawbotHQ/LB_Zone13a',
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
        'pos': Point3(140, -2, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        'cellId': 0,
        'radius': 15.0,
        }, # end entity 10001
    # COLLISIONSOLID
    10002: {
        'type': 'collisionSolid',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-96.7274, 20.5323, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'length': 10.0,
        'radius': 6.0,
        'showSolid': 0,
        'solidType': 'tube',
        }, # end entity 10002
    10003: {
        'type': 'collisionSolid',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-96.7274, -23.0117, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'length': 10.0,
        'radius': 6.0,
        'showSolid': 0,
        'solidType': 'tube',
        }, # end entity 10003
    # MODEL
    100001: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-4.75302, 55.148, 0),
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
        'pos': Point3(-4.75302, -55.15, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB',
        }, # end entity 100002
    100003: {
        'type': 'model',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-24.8072, -17.6762, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB',
        }, # end entity 100003
    100004: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-24.8072, 17.68, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_torch_lampB',
        }, # end entity 100004
    100005: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-93.6953, 17.68, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA',
        }, # end entity 100005
    100006: {
        'type': 'model',
        'name': 'copy of <unnamed> (5)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-99.5488, 17.68, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA',
        }, # end entity 100006
    100007: {
        'type': 'model',
        'name': 'copy of <unnamed> (6)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-99.5488, -20.5, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA',
        }, # end entity 100007
    100008: {
        'type': 'model',
        'name': 'copy of <unnamed> (5)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(-93.6953, -20.5, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(8, 8, 8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_pottedplantA',
        }, # end entity 100008
    100009: {
        'type': 'model',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(13.2635, -58.812, 0),
        'hpr': Vec3(211.701, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA',
        }, # end entity 100009
    100010: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(32.4825, -48.4216, 0),
        'hpr': Vec3(211.701, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA',
        }, # end entity 100010
    100011: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(53.5274, -37.2339, 0),
        'hpr': Vec3(204.775, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA',
        }, # end entity 100011
    100012: {
        'type': 'model',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(14.898, 55.5914, 0),
        'hpr': Vec3(336.371, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA',
        }, # end entity 100012
    100013: {
        'type': 'model',
        'name': 'copy of <unnamed> (4)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(37.3381, 45.4534, 0),
        'hpr': Vec3(335.225, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA',
        }, # end entity 100013
    100014: {
        'type': 'model',
        'name': 'copy of <unnamed> (5)',
        'comment': '',
        'parentEntId': 100000,
        'pos': Point3(60.4494, 34.2323, 0),
        'hpr': Vec3(334.011, 0, 0),
        'scale': Vec3(1.8, 1.8, 1.8),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_11/models/lawbotHQ/LB_bookshelfA',
        }, # end entity 100014
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(100, 0, 0),
        'hpr': Point3(270, 0, 0),
        'scale': Vec3(1, 1, 1),
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
    100015: {
        'type': 'nodepath',
        'name': 'lights',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 0, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': 1,
        }, # end entity 100015
    100017: {
        'type': 'nodepath',
        'name': 'cameratarget1',
        'comment': '',
        'parentEntId': 100015,
        'pos': Point3(-67.0138, 21.058, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 100017
    100018: {
        'type': 'nodepath',
        'name': 'copy of cameratarget1',
        'comment': '',
        'parentEntId': 100015,
        'pos': Point3(-3.89516, 39.263, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 100018
    100019: {
        'type': 'nodepath',
        'name': 'copy of cameratarget1 (2)',
        'comment': '',
        'parentEntId': 100015,
        'pos': Point3(-23.9228, 20.3744, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 100019
    100020: {
        'type': 'nodepath',
        'name': 'lights2',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0, 4.9793, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 100020
    100022: {
        'type': 'nodepath',
        'name': 'camtar1',
        'comment': '',
        'parentEntId': 100020,
        'pos': Point3(16.2876, -35.7071, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 100022
    100023: {
        'type': 'nodepath',
        'name': 'copy of camtar1',
        'comment': '',
        'parentEntId': 100020,
        'pos': Point3(-52.2915, -8.50529, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 100023
    100024: {
        'type': 'nodepath',
        'name': 'copy of camtar1 (2)',
        'comment': '',
        'parentEntId': 100020,
        'pos': Point3(-52.2915, -37.5322, 0),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        }, # end entity 100024
    # SECURITYCAMERA
    100016: {
        'type': 'securityCamera',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100015,
        'pos': Point3(-45.8708, 39.2215, 0.05),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'accel': 5.0,
        'damPow': 8,
        'hideModel': 0,
        'maxVel': 12.0,
        'modelPath': 0,
        'projector': Point3(6, 6, 25),
        'radius': 5,
        'switchId': 0,
        'trackTarget1': 100017,
        'trackTarget2': 100018,
        'trackTarget3': 100019,
        }, # end entity 100016
    100021: {
        'type': 'securityCamera',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 100020,
        'pos': Point3(-45.2862, -55.4163, 0.05),
        'hpr': Vec3(0, 0, 0),
        'scale': Vec3(1, 1, 1),
        'accel': 5.0,
        'damPow': 8,
        'hideModel': 0,
        'maxVel': 12.0,
        'modelPath': 0,
        'projector': Point3(6, 6, 25),
        'radius': 5,
        'switchId': 0,
        'trackTarget1': 100022,
        'trackTarget2': 100023,
        'trackTarget3': 100024,
        }, # end entity 100021
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
