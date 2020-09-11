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
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE19a',
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
    10005: {
        'type': 'attribModifier',
        'name': 'sinkDuration',
        'comment': '',
        'parentEntId': 10002,
        'attribName': 'sinkDuration',
        'recursive': 1,
        'typeName': 'sinkingPlatform',
        'value': '2.0',
        }, # end entity 10005
    10006: {
        'type': 'attribModifier',
        'name': 'riseDuration',
        'comment': '',
        'parentEntId': 10002,
        'attribName': 'riseDuration',
        'recursive': 1,
        'typeName': 'sinkingPlatform',
        'value': '2.0',
        }, # end entity 10006
    # HEALBARREL
    10004: {
        'type': 'healBarrel',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-52.5099983215,-3.81641983986,4.99661874771),
        'hpr': Vec3(100.165977478,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'rewardPerGrab': 8,
        'rewardPerGrabMax': 0,
        }, # end entity 10004
    # MODEL
    10008: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10007,
        'pos': Point3(-24.928899765,-4.86700963974,-1.70696532726),
        'hpr': Vec3(270.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'loadType': 'loadModel',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A5.bam',
        }, # end entity 10008
    # NODEPATH
    10002: {
        'type': 'nodepath',
        'name': 'sinkingPlatforms',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(2.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(0.864239275455,0.864239275455,0.864239275455),
        }, # end entity 10002
    10007: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10007
    # SINKINGPLATFORM
    10000: {
        'type': 'sinkingPlatform',
        'name': 'plat1',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'pauseBeforeRise': 1,
        'riseDuration': 2.0,
        'sinkDuration': 2.0,
        'verticalRange': 3.0,
        }, # end entity 10000
    10001: {
        'type': 'sinkingPlatform',
        'name': 'plat0',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(20.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'pauseBeforeRise': 1,
        'riseDuration': 2.0,
        'sinkDuration': 2.0,
        'verticalRange': 3.0,
        }, # end entity 10001
    10003: {
        'type': 'sinkingPlatform',
        'name': 'plat2',
        'comment': '',
        'parentEntId': 10002,
        'pos': Point3(-20.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'pauseBeforeRise': 1,
        'riseDuration': 2.0,
        'sinkDuration': 2.0,
        'verticalRange': 3.0,
        }, # end entity 10003
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
