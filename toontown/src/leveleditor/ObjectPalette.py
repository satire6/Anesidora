"""
ToonTown Object Palette will be automatically generated while loading storage DNA files
"""
import __builtin__, os, glob
from pandac.PandaModules import *
from direct.leveleditor.ObjectPaletteBase import *

class ObjectSuitPoint(ObjectBase):
    def __init__(self, *args, **kw):
        kw['name'] = 'SuitPath Point'
        kw['createFunction'] = ('.createSuitPathPoint', {})
        ObjectBase.__init__(self, *args, **kw)

        self.properties['index'] = [OG.PROP_UI_BLIND,
                                    OG.PROP_INT,
                                    ('.updateSuitPointIndex',
                                     {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                    0,
                                    None]

        self.properties['lbIndex'] = [OG.PROP_UI_BLIND,
                                    OG.PROP_INT,
                                    ('.updateSuitPointLbIndex',
                                     {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                    -1,
                                    None]

        self.properties['pointType'] = [OG.PROP_UI_RADIO,
                                    OG.PROP_STR,
                                    ('.updateSuitPointType',
                                     {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                    'STREETPOINT',
                                    ['STREETPOINT',
                                     'FRONTDOORPOINT',
                                     'SIDEDOORPOINT',
                                     'COGHQINPOINT',
                                     'COGHQOUTPOINT']]
                                    
class ObjectToon(ObjectBase):
    def __init__(self, *args, **kw):
        if kw.get('hood'):
            self.hood = kw['hood']
            del kw['hood']
        else:
            self.hood = 'Generic'

        ObjectBase.__init__(self, *args, **kw)

        self.properties['_subDna'] = [OG.PROP_UI_BLIND,
                                     OG.PROP_BLIND,
                                     None,
                                     [],
                                     None]
        self.dnaProperties = {}

class ObjectVisGroup(ObjectToon):
    def __init__(self, *args, **kw):
        kw['name'] = '__vis_group__'
        kw['createFunction'] = ('.createVisGroup', {'name':OG.ARG_NAME})
        kw['movable'] = False
        kw['named'] = True
        ObjectToon.__init__(self, *args, **kw)

        self.properties['_visList'] = [OG.PROP_UI_BLIND,
                                     OG.PROP_BLIND,
                                     None,
                                     [],
                                     None]

        self.properties['_battleCellList'] = [OG.PROP_UI_BLIND,
                                     OG.PROP_BLIND,
                                     None,
                                     [],
                                     None]

        self.properties['_suitEdgeList'] = [OG.PROP_UI_BLIND,
                                     OG.PROP_BLIND,
                                     None,
                                     [],
                                     None]        
class ObjectProp(ObjectToon):
    def __init__(self, *args, **kw):
        kw['createFunction'] = ('.createProp', {'propType': kw['name'], 'name':OG.ARG_NAME})
        kw['named'] = True
        ObjectToon.__init__(self, *args, **kw)

class ObjectStreet(ObjectToon):
    def __init__(self, *args, **kw):
        kw['createFunction'] = ('.createStreet', {'streetType': kw['name']})
        ObjectToon.__init__(self, *args, **kw)

class ObjectLandmark(ObjectToon):
    def __init__(self, *args, **kw):
        kw['createFunction'] = ('.createLandmark', {'landmarkType': kw['name']})
        ObjectToon.__init__(self, *args, **kw)
        self.properties['Special Type'] = [OG.PROP_UI_RADIO,
                                           OG.PROP_STR,
                                           ('.updateSpecialBuildingType',
                                           {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                           '',
                                           ['', 'hq', 'gagshop', 'clotheshop','petshop', 'kartshop']]
        self.properties['Title'] = [OG.PROP_UI_ENTRY,
                                    OG.PROP_STR,
                                    ('.updateTitle',
                                     {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),
                                    '',
                                    None]

        self.dnaProperties['Special Type'] = 'getBuildingType'
        self.dnaProperties['Title'] = 'getTitle'

class ObjectFlatBuilding(ObjectToon):
    def __init__(self, *args, **kw):
        kw['createFunction'] = ('.createFlatBuilding', {'buildingType': kw['name']})
        ObjectToon.__init__(self, *args, **kw)
        self.properties['Building Width'] = [OG.PROP_UI_RADIO,
                                             OG.PROP_STR,
                                             ('.updateFlatBuildingWidth',
                                              {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ, 'no_loading':OG.ARG_NOLOADING}),
                                             '10',
                                             ['5', '10', '15', '15.6', '20', '20.7', '25']]
        self.dnaProperties['Building Width'] = 'getWidth'

BUILDING_TYPES = ['10_10', '20', '10_20', '20_10', '10_10_10',
                  '4_21', '3_22', '4_13_8', '3_13_9', '10',
                  '12_8', '13_9_8', '4_10_10',  '4_10', '4_20',
                  ]

class ObjectAnimBase(ObjectToon):
    def __init__(self, *args, **kw):
        ObjectToon.__init__(self, *args, **kw)

        # [gjeon] try to find proper animations
        code = kw['name']
        modelName = DNASTORE.findNode(code).getAncestors()[-1].getName()
        tokens =  modelName.split('.')[0].split('_r_')

        if isinstance(self, ObjectInteractiveProp):
            pathStr = code[len('interactive_prop_'):].split('__')[0]
        elif isinstance(self, ObjectAnimBuilding):
            pathStr = code[len('animated_building_'):].split('__')[0]            
        elif code.startswith('animated_prop_generic_'):
            pathStr = code[len('animated_prop_generic_'):].split('__')[0]
        elif code.startswith('animated_prop_'):
            # we expect generic to be replaced with the class name
            tempStr = code[len('animated_prop_'):]
            nextUnderscore = tempStr.find('_')
            finalStr = tempStr[nextUnderscore+1:]                           
            pathStr = finalStr.split('__')[0]

        phaseDelimeter = len('phase_') + pathStr[len('phase_'):].find('_')
        phaseStr = pathStr[:phaseDelimeter]
        pathTokens = pathStr[phaseDelimeter+1:].split('_')
        modelPathStr = phaseStr
        for path in pathTokens:
            modelPathStr += '/'
            modelPathStr += path

        modelPath = getModelPath().findFile(modelPathStr)
        animFileList = glob.glob('%s%s/%s_a_%s_*.bam'%(os.environ['PANDA_ROOT'], modelPath, tokens[0], tokens[1]))

        # [gjeon] define anim list menu for selection
        animNameList = []
        for animFile in animFileList:
            animName = os.path.basename(animFile[:animFile.rfind('.')])
            animNameList.append(animName)

        if len(animNameList) == 0:
            defaultAnimName = None
        else:
            defaultAnimName = animNameList[0]
        self.properties['anims'] = [OG.PROP_UI_COMBO,
                                  OG.PROP_STR,
                                  ('.updateAnimPropAnim',
                                   {'val':OG.ARG_VAL, 'obj':OG.ARG_OBJ}),                                    
                                  defaultAnimName,
                                  animNameList] 
        self.dnaProperties['anims'] = 'getAnim'

class ObjectAnimProp(ObjectAnimBase):
    def __init__(self, *args, **kw):
        kw['createFunction'] = ('.createAnimProp', {'animPropType': kw['name']})
        ObjectAnimBase.__init__(self, *args, **kw)

class ObjectInteractiveProp(ObjectAnimBase):
    def __init__(self, *args, **kw):
        kw['createFunction'] = ('.createInteractiveProp', {'interactivePropType': kw['name']})
        ObjectAnimBase.__init__(self, *args, **kw)

class ObjectAnimBuilding(ObjectAnimBase):
    def __init__(self, *args, **kw):
        kw['createFunction'] = ('.createAnimBuilding', {'animBuildingType': kw['name']})
        ObjectAnimBase.__init__(self, *args, **kw)

class ObjectPalette(ObjectPaletteBase):
    def __init__(self):
        self.dnaBuiltDirectory = Filename.expandFrom(base.config.GetString("dna-built-directory", "$TTMODELS/built"))
        self.hoodDict = {}
        ObjectPaletteBase.__init__(self)

    def loadStorageFile(self, pandaPath):
        path = Filename(pandaPath)
        filePath = self.dnaBuiltDirectory.toOsSpecific() + '\\' + path.toOsSpecific()
        if os.path.exists(filePath):
            loadDNAFile(DNASTORE, pandaPath, CSDefault, 1)

    def getCatalogCode(self, category, i):
        return DNASTORE.getCatalogCode(category, i)

    def getCatalogCodes(self, category):
        numCodes = DNASTORE.getNumCatalogCodes(category)
        codes = []
        for i in range(numCodes):
            codes.append(DNASTORE.getCatalogCode(category, i))
        return codes

    def populateHood(self, hoodName):
        self.hoodDict[hoodName] = {}
        codes = (self.getCatalogCodes('prop') + self.getCatalogCodes('holiday_prop'))
        codes.sort()
        self.populateTree(hoodName, 'Props', codes, ObjectProp)

        codes = self.getCatalogCodes('toon_landmark')
        codes.sort()
        self.populateTree(hoodName, 'Landmarks', codes, ObjectLandmark)

        codes = self.getCatalogCodes('anim_building')
        codes.sort()
        self.populateTree(hoodName, 'Anim Buildings', codes, ObjectAnimBuilding)

        codes = self.getCatalogCodes('anim_prop')
        codes.sort()
        self.populateTree(hoodName, 'Anim Props', codes, ObjectAnimProp)

        codes = self.getCatalogCodes('interactive_prop')
        codes.sort()
        self.populateTree(hoodName, 'Interactive Props', codes, ObjectInteractiveProp)

        if hoodName != 'Generic':
            codes = BUILDING_TYPES
            codes.extend(map(lambda x: 'random%s'%x, ['10', '14', '20', '24', '25', '30']))
            codes = map(lambda x:'%s_%s'%(hoodName, x), codes)
            codes.sort()
            self.populateTree(hoodName, 'Flat Buildings', codes, ObjectFlatBuilding)

            codes = map(lambda s: s[7:],
                      self.getCatalogCodes('street'))

            for pond in ['BR', 'DD', 'DG', 'DL', 'MM', 'TT']:
                if '%s_pond'%pond in codes:
                    codes.remove('%s_pond'%pond)

            if hoodName in ['BR', 'DD', 'DG', 'DL', 'MM', 'TT']:
                codes.append('pond')
            codes = map(lambda x:'%s_%s'%(hoodName, x), codes)

            codes.sort()
            self.populateTree(hoodName, 'Streets', codes, ObjectStreet)

    def populateTree(self, hoodName, groupName, codeList, objClass):
        registeredList = []
        for key in self.hoodDict.keys():
            if self.hoodDict[key].get(groupName):
                registeredList.extend(self.hoodDict[key][groupName])
        newList = []
        for code in codeList:
            if code not in registeredList:
               newList.append(code)
        if len(newList) > 0:
            self.add("%s %s"%(hoodName, groupName), groupName)
            self.hoodDict[hoodName][groupName] = []
            for code in newList:
                self.add(objClass(name=code,hood=hoodName), "%s %s"%(hoodName, groupName))
                self.hoodDict[hoodName][groupName].append(code)

    def populate(self):
        __builtin__.DNASTORE = DNASTORE = DNAStorage()
        # adding some hidden object type
        self.data['__sys__'] = ObjectBase('__sys__', createFunction=('.createSys', {}))
        self.data['__group__'] = ObjectToon('__group__', createFunction=('.createGroup', {'name':OG.ARG_NAME}), movable=False, named=True)
        self.data['__vis_group__'] = ObjectVisGroup()
        self.data['__node__'] = ObjectToon('__node__', createFunction=('.createNode', {'name':OG.ARG_NAME}), movable=True, named=True)
        self.data['DCS'] = ObjectProp(name='DCS',hood='Generic')
        
        # adding system object types
        self.add(ObjectSuitPoint())

        self.add('Props')
        self.add('Streets')
        self.add('Landmarks')
        self.add('Flat Buildings')
        self.add('Anim Buildings')
        self.add('Anim Props')
        self.add('Interactive Props')

        # Load the generic storage files
        self.loadStorageFile('dna/storage.dna')
        self.loadStorageFile('phase_4/dna/storage.dna')
        self.loadStorageFile('phase_5/dna/storage_town.dna')
        self.populateHood('Generic')

        # Load all the neighborhood specific storage files
        # TT
        self.loadStorageFile('phase_4/dna/storage_TT.dna')
        self.loadStorageFile('phase_4/dna/storage_TT_sz.dna')
        self.loadStorageFile('phase_5/dna/storage_TT_town.dna')
        self.populateHood('TT')

        # DD
        self.loadStorageFile('phase_6/dna/storage_DD.dna')
        self.loadStorageFile('phase_6/dna/storage_DD_sz.dna')
        self.loadStorageFile('phase_6/dna/storage_DD_town.dna')
        self.populateHood('DD')

        # MM
        self.loadStorageFile('phase_6/dna/storage_MM.dna')
        self.loadStorageFile('phase_6/dna/storage_MM_sz.dna')
        self.loadStorageFile('phase_6/dna/storage_MM_town.dna')
        self.populateHood('MM')

        # BR
        self.loadStorageFile('phase_8/dna/storage_BR.dna')
        self.loadStorageFile('phase_8/dna/storage_BR_sz.dna')
        self.loadStorageFile('phase_8/dna/storage_BR_town.dna')
        self.populateHood('BR')

        # DG
        self.loadStorageFile('phase_8/dna/storage_DG.dna')
        self.loadStorageFile('phase_8/dna/storage_DG_sz.dna')
        self.loadStorageFile('phase_8/dna/storage_DG_town.dna')
        self.populateHood('DG')

        # DL
        self.loadStorageFile('phase_8/dna/storage_DL.dna')
        self.loadStorageFile('phase_8/dna/storage_DL_sz.dna')
        self.loadStorageFile('phase_8/dna/storage_DL_town.dna')
        self.populateHood('DL')

        # CS
        self.loadStorageFile('phase_9/dna/storage_CS.dna')
        self.populateHood('CS')

        # GS
        self.loadStorageFile('phase_6/dna/storage_GS.dna')
        self.loadStorageFile('phase_6/dna/storage_GS_sz.dna')
        self.populateHood('GS')

        # OZ
        self.loadStorageFile('phase_6/dna/storage_OZ.dna')
        self.loadStorageFile('phase_6/dna/storage_OZ_sz.dna')
        self.populateHood('OZ')

        # GZ
        self.loadStorageFile('phase_6/dna/storage_GZ.dna')
        self.loadStorageFile('phase_6/dna/storage_GZ_sz.dna')
        self.populateHood('GZ')

        # CC
        self.loadStorageFile('phase_12/dna/storage_CC_sz.dna')
        self.populateHood('CC')

        # PA
        self.loadStorageFile('phase_13/dna/storage_party_sz.dna')
        self.populateHood('PA')
