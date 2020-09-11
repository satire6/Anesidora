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
    # HEALBARREL
    10015: {
        'type': 'healBarrel',
        'name': 'heal',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(16.9929084778,7.15916633606,0.0),
        'hpr': Vec3(107.078933716,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'rewardPerGrab': 6,
        'rewardPerGrabMax': 0,
        }, # end entity 10015
    # MINTSHELF
    10004: {
        'type': 'mintShelf',
        'name': '<unnamed>',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(41.5774269104,-16.0394973755,0.0),
        'hpr': Vec3(270.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12500,
        }, # end entity 10004
    10005: {
        'type': 'mintShelf',
        'name': 'copy of <unnamed>',
        'comment': '',
        'parentEntId': 10003,
        'pos': Point3(41.5774269104,15.5885248184,0.0),
        'hpr': Vec3(270.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        'mintId': 12700,
        }, # end entity 10005
    # MODEL
    10009: {
        'type': 'model',
        'name': 'crateColl0',
        'comment': '',
        'parentEntId': 10010,
        'pos': Point3(-21.0479602814,-8.71147918701,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.6654573679,4.67459440231,4.99637460709),
        'collisionsOnly': 1,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/CBMetalCrate.bam',
        }, # end entity 10009
    10013: {
        'type': 'model',
        'name': 'crate0',
        'comment': '',
        'parentEntId': 10010,
        'pos': Point3(-21.0,0.735621452332,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.60000002384,1.60000002384,1.60000002384),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam',
        }, # end entity 10013
    10016: {
        'type': 'model',
        'name': 'copy of crate0',
        'comment': '',
        'parentEntId': 10010,
        'pos': Point3(-21.0,-8.74976444244,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.60000002384,1.60000002384,1.60000002384),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam',
        }, # end entity 10016
    10017: {
        'type': 'model',
        'name': 'copy of crate0 (2)',
        'comment': '',
        'parentEntId': 10010,
        'pos': Point3(-21.0,-18.1307086945,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.60000002384,1.60000002384,1.60000002384),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam',
        }, # end entity 10017
    10019: {
        'type': 'model',
        'name': 'copy of crate0',
        'comment': '',
        'parentEntId': 10018,
        'pos': Point3(-21.0,-8.74976444244,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(1.60000002384,1.60000002384,1.60000002384),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam',
        }, # end entity 10019
    10020: {
        'type': 'model',
        'name': 'crateColl0',
        'comment': '',
        'parentEntId': 10018,
        'pos': Point3(-21.0479602814,-8.71147918701,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.69406318665,4.75488471985,5.08219003677),
        'collisionsOnly': 1,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cashbotHQ/CBMetalCrate.bam',
        }, # end entity 10020
    10021: {
        'type': 'model',
        'name': 'crate0',
        'comment': '',
        'parentEntId': 10018,
        'pos': Point3(-21.0,0.735621452332,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.60000002384,1.60000002384,1.60000002384),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam',
        }, # end entity 10021
    10022: {
        'type': 'model',
        'name': 'copy of crate0 (2)',
        'comment': '',
        'parentEntId': 10018,
        'pos': Point3(-21.0,-18.1307086945,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.60000002384,1.60000002384,1.60000002384),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam',
        }, # end entity 10022
    10024: {
        'type': 'model',
        'name': 'hider',
        'comment': '',
        'parentEntId': 10023,
        'pos': Point3(17.0452461243,-0.882949709892,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.54636645317,1.54636645317,1.54636645317),
        'collisionsOnly': 0,
        'flattenType': 'light',
        'loadType': 'loadModelCopy',
        'modelPath': 'phase_10/models/cogHQ/CBMetalCrate2.bam',
        }, # end entity 10024
    # NODEPATH
    10003: {
        'type': 'nodepath',
        'name': 'props',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10003
    10010: {
        'type': 'nodepath',
        'name': 'crates0',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(1.2899544239,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10010
    10018: {
        'type': 'nodepath',
        'name': 'crates1',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-13.2792396545,0.0,0.0),
        'hpr': Vec3(180.0,0.0,0.0),
        'scale': Vec3(1.0,1.0,1.0),
        }, # end entity 10018
    10023: {
        'type': 'nodepath',
        'name': 'heal',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(0.0,0.0,0.0),
        'hpr': Vec3(0.0,0.0,0.0),
        'scale': 1,
        }, # end entity 10023
    # STOMPER
    10000: {
        'type': 'stomper',
        'name': 'stomper0',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-23.0840358734,13.8124275208,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(8.0,8.0,8.0),
        'crushCellId': None,
        'damage': 8,
        'headScale': Vec3(1.0,1.0,1.0),
        'modelPath': 0,
        'motion': 3,
        'period': 3.0,
        'phaseShift': 0.0,
        'range': 1.6000000000000001,
        'shaftScale': Point3(1.0,5.0,1.0),
        'soundLen': 0,
        'soundOn': 1,
        'soundPath': 0,
        'style': 'vertical',
        'switchId': 0,
        'wantShadow': 1,
        'wantSmoke': 1,
        'zOffset': 0,
        }, # end entity 10000
    10001: {
        'type': 'stomper',
        'name': 'stomper1',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(-5.92516326904,-0.618411839008,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(8.0,8.0,8.0),
        'crushCellId': None,
        'damage': 8,
        'headScale': Vec3(1.0,1.0,1.0),
        'modelPath': 0,
        'motion': 3,
        'period': 3.0,
        'phaseShift': 0.33000000000000002,
        'range': 1.6000000000000001,
        'shaftScale': Point3(1.0,5.0,1.0),
        'soundLen': 0,
        'soundOn': 1,
        'soundPath': 0,
        'style': 'vertical',
        'switchId': 0,
        'wantShadow': 1,
        'wantSmoke': 1,
        'zOffset': 0,
        }, # end entity 10001
    10002: {
        'type': 'stomper',
        'name': 'stomper2',
        'comment': '',
        'parentEntId': 0,
        'pos': Point3(11.6394100189,-14.1471977234,0.0),
        'hpr': Point3(0.0,0.0,0.0),
        'scale': Vec3(8.0,8.0,8.0),
        'crushCellId': None,
        'damage': 8,
        'headScale': Vec3(1.0,1.0,1.0),
        'modelPath': 0,
        'motion': 3,
        'period': 3.0,
        'phaseShift': 0.66000000000000003,
        'range': 1.6000000000000001,
        'shaftScale': Point3(1.0,5.0,1.0),
        'soundLen': 0,
        'soundOn': 1,
        'soundPath': 0,
        'style': 'vertical',
        'switchId': 0,
        'wantShadow': 1,
        'wantSmoke': 1,
        'zOffset': 0,
        }, # end entity 10002
    }

Scenario0 = {
    }

levelSpec = {
    'globalEntities': GlobalEntities,
    'scenarios': [
        Scenario0,
        ],
    }
