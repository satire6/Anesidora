import random
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import os
from direct.showbase import AppRunnerGlobal
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *

class PetNameGenerator:

    notify = DirectNotifyGlobal.directNotify.newCategory("PetNameGenerator")

    boyFirsts = []
    girlFirsts = []
    neutralFirsts = []

    def __init__(self):
        self.generateLists()
        return

    def generateLists(self):
        """ This method looks in a text file specified in the localizer and loads
            in all the names into the 8 lists as well as populating self.nameDictionary
            which has uniqueIDs mapped to a tuple of category and name
            """
        self.boyFirsts = []
        self.girlFirsts = []
        self.neutralFirsts = []
        self.nameDictionary = {}

        # Look for the name master file and read it in.
        searchPath = DSearchPath()
        if AppRunnerGlobal.appRunner:
            # In the web-publish runtime, it will always be here:
            searchPath.appendDirectory(Filename.expandFrom('$TT_3_ROOT/phase_3/etc'))
        else:
            # In other environments, including the dev environment, look here:
            searchPath.appendDirectory(Filename('phase_3/etc'))
            if os.path.expandvars('$TOONTOWN') != '':
                searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$TOONTOWN/src/configfiles')))
            else:
                searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('toontown/src/configfiles')))
            # RobotToonManager needs to look for file in current directory
            searchPath.appendDirectory(Filename('.'))

        filename = Filename(TTLocalizer.PetNameMaster)
        found = vfs.resolveFilename(filename, searchPath)

        if not found:
            self.notify.error("PetNameGenerator: Error opening name list text file.")

        input = StreamReader(vfs.openReadFile(filename, 1), 1)

        currentLine = input.readline()
        while currentLine:
            if currentLine.lstrip()[0:1] != '#':
                a1 = currentLine.find('*')
                a2 = currentLine.find('*', a1+1)
                self.nameDictionary[int(currentLine[0:a1])]=(int(currentLine[a1+1:a2]),
                                                             currentLine[a2+1:len(currentLine)-1].strip())
            currentLine = input.readline()

        masterList = [self.boyFirsts, self.girlFirsts, self.neutralFirsts]
        for tu in self.nameDictionary.values():
            masterList[tu[0]].append(tu[1])
        return 1

    def getName(self, uniqueID):
        return self.nameDictionary[uniqueID][1]
    
    def returnUniqueID(self, name):
        """
        If successful it returns the uniqueID, if not then -1
        """
        newtu = [(),(),()]
        newtu[0] = (0, name)
        newtu[1] = (1, name)
        newtu[2] = (2, name)

        for tu in self.nameDictionary.items():
            for g in newtu:
                if tu[1] == g:
                    return tu[0]
        return -1

    def randomName(self, gender = None, seed = None):
        S = random.getstate()

        if seed is not None:
            random.seed(seed)

        if gender is None:
            # Randomly pick the name sex
            gender = random.choice([0, 1])

        retString = ""

        # Shallow copy, since we will be altering the list
        firstList = self.neutralFirsts[:]
        if gender == 0:
            firstList += self.boyFirsts
        elif gender == 1:
            firstList += self.girlFirsts
        else:
            self.error("Must be boy or girl.")

        retString += random.choice(firstList)

        random.setstate(S)

        return retString
