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
        'modelFilename': 'phase_10/models/cashbotHQ/ZONE13a',
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
    10020: {
        'type': 'mintProduct',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10019,
        'pos': Point3(6.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12600,
        }, # end entity 10020
    10021: {
        'type': 'mintProduct',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10019,
        'pos': Point3(13.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12600,
        }, # end entity 10021
    10022: {
        'type': 'mintProduct',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 10019,
        'pos': Point3(-6.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12600,
        }, # end entity 10022
    10023: {
        'type': 'mintProduct',
        'name': 'copy of <unnamed> (3)',
        'comment': '',
        'parentEntId': 10019,
        'pos': Point3(-13.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12600,
        }, # end entity 10023
    # MINTSHELF
    10025: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10027,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12600,
        }, # end entity 10025
    10029: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10027,
        'pos': Point3(13.4300003052,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12600,
        }, # end entity 10029
    10030: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10028,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12600,
        }, # end entity 10030
    10031: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed> (2)',
        'comment': '',
        'parentEntId': 10028,
        'pos': Point3(-13.4300003052,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12600,
        }, # end entity 10031
    10033: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10032,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12500,
        }, # end entity 10033
    10034: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10032,
        'pos': Point3(29.7916145325,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12500,
        }, # end entity 10034
    10036: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10035,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        'mintId': 12500,
        }, # end entity 10036
    10037: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10035,
        'pos': Point3(-37.7522773743,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12500,
        }, # end entity 10037
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
    10009: {
        'type': 'model',
        'name': 'backPillar',
        'comment': '',
        'parentEntId': 10005,
        'pos': Point3(41.4432792664,0.0,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10009
    10010: {
        'type': 'model',
        'name': 'frontPillar',
        'comment': '',
        'parentEntId': 10005,
        'pos': Point3(-41.0848464966,0.0,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10010
    10011: {
        'type': 'model',
        'name': 'rightPillar',
        'comment': '',
        'parentEntId': 10005,
        'pos': Point3(0.0,-22.3441867828,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10011
    10012: {
        'type': 'model',
        'name': 'leftPillar',
        'comment': '',
        'parentEntId': 10005,
        'pos': Point3(0.0,21.9451503754,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10012
    10013: {
        'type': 'model',
        'name': 'frontRightPillar',
        'comment': '',
        'parentEntId': 10006,
        'pos': Point3(0.0,-22.5711078644,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10013
    10014: {
        'type': 'model',
        'name': 'frontLeftPillar',
        'comment': '',
        'parentEntId': 10006,
        'pos': Point3(0.0,22.1686630249,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10014
    10015: {
        'type': 'model',
        'name': 'frontRightPillar',
        'comment': '',
        'parentEntId': 10007,
        'pos': Point3(0.0,-22.5711078644,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10015
    10016: {
        'type': 'model',
        'name': 'frontLeftPillar',
        'comment': '',
        'parentEntId': 10007,
        'pos': Point3(0.0,22.1686630249,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10016
    10017: {
        'type': 'model',
        'name': 'leftPillar',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(0.0,67.0966033936,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10017
    10018: {
        'type': 'model',
        'name': 'rightPillar',
        'comment': '',
        'parentEntId': 10008,
        'pos': Point3(0.0,-66.8615875244,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/pipes_A1',
        }, # end entity 10018
    10039: {
        'type': 'model',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10038,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(90.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/crates_E.bam',
        }, # end entity 10039
    # NODEPATH
    10000: {
        'type': 'nodepath',
        'name': 'cogs',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(107.260322571,0.0,0.0),
        'hpr': Vec3(270.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10000
    10003: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,-1.79999995232,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10003
    10004: {
        'type': 'nodepath',
        'name': 'pillars',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10004
    10005: {
        'type': 'nodepath',
        'name': 'centerPillars',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10005
    10006: {
        'type': 'nodepath',
        'name': 'frontPillars',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(-89.9665527344,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10006
    10007: {
        'type': 'nodepath',
        'name': 'backPillars',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(89.9700012207,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10007
    10008: {
        'type': 'nodepath',
        'name': 'outerPillars',
        'comment': '',
        'parentEntId': 10004,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10008
    10019: {
        'type': 'nodepath',
        'name': 'byVaultDoor',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(127.898963928,0.0,0.0),
        'hpr': Vec3(90.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10019
    10024: {
        'type': 'nodepath',
        'name': 'shelves',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10024
    10026: {
        'type': 'nodepath',
        'name': 'nearVault',
        'comment': '',
        'parentEntId': 10024,
        'pos': Point3(101.76008606,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10026
    10027: {
        'type': 'nodepath',
        'name': 'left',
        'comment': '',
        'parentEntId': 10026,
        'pos': Point3(0.0,19.3625793457,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10027
    10028: {
        'type': 'nodepath',
        'name': 'right',
        'comment': '',
        'parentEntId': 10026,
        'pos': Point3(0.0,-19.3600006104,0.0),
        'hpr': Point3(180.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10028
    10032: {
        'type': 'nodepath',
        'name': 'rightNear',
        'comment': '',
        'parentEntId': 10024,
        'pos': Point3(-15.3249912262,-55.9873504639,0.0),
        'hpr': Vec3(152.447189331,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10032
    10035: {
        'type': 'nodepath',
        'name': 'leftNear',
        'comment': '',
        'parentEntId': 10024,
        'pos': Point3(-17.6631221771,55.3191757202,0.0),
        'hpr': Vec3(26.3582077026,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10035
    10038: {
        'type': 'nodepath',
        'name': 'nearEntrance',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(-107.089996338,-1.71000003815,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10038
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
