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
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE15a',
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
    # LOCATOR
    10001: {
        'type': 'locator',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 0,
        'searchPath': '**/EXIT',
        }, # end entity 10001
    # MINTPRODUCT
    10009: {
        'type': 'mintProduct',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(37.843006134,8.74360656738,0.0),
        'hpr': Point3(-90.0,0.0,0.0),
        'scale': Point3(1.0,1.0,1.0),
        'mintId': 12500,
        }, # end entity 10009
    10010: {
        'type': 'mintProduct',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(36.8768577576,-10.2692861557,0.0),
        'hpr': Point3(-90.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12500,
        }, # end entity 10010
    10011: {
        'type': 'mintProduct',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(26.2384986877,-16.2085189819,0.0),
        'hpr': Point3(90.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12500,
        }, # end entity 10011
    10012: {
        'type': 'mintProduct',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(38.4032859802,-3.16089892387,0.0),
        'hpr': Point3(90.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12500,
        }, # end entity 10012
    # MODEL
    10002: {
        'type': 'model',
        'name': 'vaultDoor',
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
    10004: {
        'type': 'model',
        'name': 'backRight',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(42.1358146667,-20.2375278473,0.275439172983),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/crates_A.bam',
        }, # end entity 10004
    10005: {
        'type': 'model',
        'name': 'backLeft',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(38.4724159241,18.6007175446,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.44939172268,1.44939172268,1.44939172268),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/crates_F1.bam',
        }, # end entity 10005
    10006: {
        'type': 'model',
        'name': 'frontRight',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(-42.3298530579,-20.0590000153,0.0695294439793),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.40563333035,1.40563333035,1.40563333035),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/crates_D.bam',
        }, # end entity 10006
    10007: {
        'type': 'model',
        'name': 'frontLeft',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(-42.3731651306,18.05443573,0.0688875243068),
        'hpr': Vec3(270.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/crates_G1.bam',
        }, # end entity 10007
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Point3(270.0,0.0,0.0),
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
    10008: {
        'type': 'nodepath',
        'name': 'product',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10008
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
