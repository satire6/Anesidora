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
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE10a',
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
    # HEALBARREL
    10009: {
        'type': 'healBarrel',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(63.9741363525,-10.9343223572,9.97696113586),
        'hpr': Vec3(270.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'rewardPerGrab': 8,
        'rewardPerGrabMax': 0,
        }, # end entity 10009
    10010: {
        'type': 'healBarrel',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10009,
        'pos': Point3(0.0,0.0,4.13999986649),
        'hpr': Vec3(349.358764648,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'rewardPerGrab': 8,
        'rewardPerGrabMax': 0,
        }, # end entity 10010
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': 'mixers',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-19.2397289276,0.0,5.53999996185),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(0.758001744747,0.758001744747,0.758001744747),
        }, # end entity 10000
    # PAINTMIXER
    10004: {
        'type': 'paintMixer',
        'name': 'mixer0',
        'comment': '',
        'parentEntId': 10000,
        'pos': Point3(0.0,10.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'floorName': 'PaintMixerFloorCollision',
        'modelPath': 'phase_9/models/cogHQ/PaintMixer',
        'modelScale': Vec3(1.0,1.0,1.0),
        'motion': 'easeInOut',
        'offset': Point3(20.0,20.0,0.0),
        'period': 8.0,
        'phaseShift': 0.0,
        'shaftScale': 1,
        'waitPercent': 0.10000000000000001,
        }, # end entity 10004
    10005: {
        'type': 'paintMixer',
        'name': 'mixer1',
        'comment': '',
        'parentEntId': 10000,
        'pos': Point3(29.0,10.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'floorName': 'PaintMixerFloorCollision',
        'modelPath': 'phase_9/models/cogHQ/PaintMixer',
        'modelScale': Vec3(1.0,1.0,1.0),
        'motion': 'easeInOut',
        'offset': Point3(0.0,-20.0,0.0),
        'period': 8.0,
        'phaseShift': 0.5,
        'shaftScale': 1,
        'waitPercent': 0.10000000000000001,
        }, # end entity 10005
    10006: {
        'type': 'paintMixer',
        'name': 'mixer2',
        'comment': '',
        'parentEntId': 10000,
        'pos': Point3(58.0,-8.94072246552,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'floorName': 'PaintMixerFloorCollision',
        'modelPath': 'phase_9/models/cogHQ/PaintMixer',
        'modelScale': Vec3(1.0,1.0,1.0),
        'motion': 'easeInOut',
        'offset': Point3(-20.0,-20.0,0.0),
        'period': 8.0,
        'phaseShift': 0.5,
        'shaftScale': 1,
        'waitPercent': 0.10000000000000001,
        }, # end entity 10006
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
