"""
FlatBuilding object
"""

import random, string
from ToonTownObj import *

class FlatBuildingObj(ToonTownObj):
    def __init__(self, editor, buildingType, dna=None, nodePath=None):
        hoodId = buildingType[:2]
        self.editor = editor
        self.buildingType = buildingType[3:]
        self.editor.setEditMode(hoodId)
        ToonTownObj.__init__(self, editor, dna, nodePath)

    def initDNA(self):
        # Create new building
        dnaNode = DNAFlatBuilding()
        self.setRandomBuildingStyle(dnaNode,
                                    name = 'tb0:'+ self.buildingType + '_DNARoot')
        # Now place new building in the world
        return dnaNode

    def getRandomHeightList(self, buildingHeight):
        # Select a list of wall heights
        heightLists = self.getList(`buildingHeight` + '_ft_wall_heights')
        l = len(heightLists)
        if l > 0:
            # If a list exists for this building height, pick randomly
            return heightLists[random.randint(0, l - 1)]
        else:
            # No height lists exists for this building height, generate
            chance = random.randint(0, 100)
            if buildingHeight <= 10:
                return [buildingHeight]
            elif buildingHeight <= 14:
                return [4, 10]
            elif buildingHeight <= 20:
                if chance <= 30:
                    return [20]
                elif chance <= 80:
                    return [10, 10]
                else:
                    return [12, 8]
            elif buildingHeight <= 24:
                if chance <= 50:
                    return [4, 10, 10]
                else:
                    return [4, 20]
            elif buildingHeight <= 25:
                if chance <= 25:
                    return [3, 22]
                elif chance <= 50:
                    return [4, 21]
                elif chance <= 75:
                    return [3, 13, 9]
                else:
                    return [4, 13, 8]
            else:
                if chance <= 20:
                    return [10, 20]
                elif chance <= 35:
                    return [20, 10]
                elif chance <= 75:
                    return [10, 10, 10]
                else:
                    return [13, 9, 8]

    def getRandomWallWidth(self):
        chance = random.randint(0, 100)
        if chance <= 15:
            return 5.0
        elif chance <= 30:
            return 10.0
        elif chance <= 65:
            return 15.0
        elif chance <= 85:
            return 20.0
        else:
            return 25.0

    def getRandomDictionaryEntry(self, dict):
        numKeys = len(dict)
        if numKeys > 0:
            keys = dict.keys()
            key = keys[random.randint(0, numKeys - 1)]
            return dict[key]
        else:
            return None

    def getRandomWindowCount(self):
        if ((self.lastWall != None) and (self.lastBuilding != None)):
            h = ROUND_INT(self.lastWall.getHeight())
            w = ROUND_INT(self.lastBuilding.getWidth())
            # Otherwise....
            if w == 5:
                # 5 ft walls can have 1 window
                return 1
            elif h == 10:
                # All other 10 ft high bldgs can have 1 or 2
                return random.randint(1, 2)
            else:
                # All others can have 1 - 4
                return random.randint(1, 4)
        else:
            return 1

    def getList(self, attribute):
        """ Return neighborhood's List for specified attribute """
        return self.getAttribute(attribute).getList()

    def getDict(self, attribute):
        """ Return neighborhood's Dictionary for specified attribute """
        return self.getAttribute(attribute).getDict()

    def getAttribute(self, attribute):
        """ Return specified attribute for current neighborhood """
        return self.styleManager.getAttribute(attribute)

    def setRandomBuildingStyle(self, dnaNode, name = 'building'):
        """ Initialize a new DNA Flat building to a random building style """
        # What is the current building type?
        buildingType = self.buildingType
        # If random
        if 'random' in buildingType:
            # Generate height list based on current building height
            buildingHeight = int(buildingType[6:])
            heightList = self.getRandomHeightList(buildingHeight)
            # Convert height list to building type
            buildingType = createHeightCode(heightList)
        else:
            # Use specified height list
            heightList = map(string.atof, string.split(buildingType, '_'))
            height = calcHeight(heightList)
            # Is this a never before seen height list?  If so, record it.
            try:
                attr = self.getAttribute(`height` + '_ft_wall_heights')
                if heightList not in attr.getList():
                    print 'Adding new height list entry'
                    attr.add(heightList)
            except KeyError:
                print 'Non standard height building'

        # See if this building type corresponds to existing style dict
        try:
            dict = self.getDict(buildingType + '_styles')
        except KeyError:
            # Nope
            dict = {}

        # No specific dict or empty dict, try to pick a dict
        # based on number of walls
        if not dict:
            # How many walls?
            numWalls = len(heightList)
            # Get the building_style attribute dictionary for
            # this number of walls
            dict = self.getDict(`numWalls` + '_wall_styles')

        if not dict:
            # Still no dict, create new random style using height list
            styleList = []
            # Build up wall styles
            for height in heightList:
                wallStyle = self.getRandomDictionaryEntry(
                    self.getDict('wall_style'))
                styleList.append((wallStyle, height))
            # Create new random flat building style
            style = DNAFlatBuildingStyle(styleList = styleList)
        else:
            # Pick a style
            style = self.getRandomDictionaryEntry(dict)

        # Set style....finally
        self.styleManager.setDNAFlatBuildingStyle(
            dnaNode, style, width = self.getRandomWallWidth(),
            heightList = heightList, name = name)

    def computeWallNum(self):
        heightList, offsetList = DNAGetWallHeights(self.dna)
        return heightList, offsetList

    # GET/SET
    # DNA Object elements
    def getWall(self, wallNum):
        wallCount = 0
        for i in range(self.dna.getNumChildren()):
            child = self.dna.at(i)
            if DNAClassEqual(child, DNA_WALL):
                if wallCount == wallNum:
                    return child
                wallCount = wallCount + 1
        # Not found
        return None
