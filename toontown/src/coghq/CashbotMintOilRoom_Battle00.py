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
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE22a',
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
    # MODEL
    10001: {
        'type': 'model',
        'name': 'vaultDoor',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(7.2503657341,-35.8064537048,0.0),
        'hpr': Point3(180.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
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
        'hpr': Vec3(180.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10000
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
