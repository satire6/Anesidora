"""
Base class for toontown objects
"""
import random
from pandac.PandaModules import *
from direct.leveleditor import ObjectGlobals as OG
from LevelStyleManager import *

DNA_TYPE_DICT = {
    'cornice': DNA_CORNICE,
    'door': DNA_FLAT_DOOR,
    'landmark_door' : DNA_DOOR,
    'windows' : DNA_WINDOWS,
    'sign' : DNA_SIGN,
    }

class ToonTownObjBase(NodePath):
    def __init__(self, editor, dna, nodePath):
        NodePath.__init__(self)
        self.editor = editor

        if dna:
            self.dna = dna
        else:
            self.dna = self.initDNA()
            self.editor.DNAParent.add(self.dna)
        if nodePath:
            np = nodePath
        else:
            np = self.dna.traverse(self.editor.NPParent, DNASTORE, 1)
        self.assign(np)    

    def initDNA(self):
        # You should implement this in subclass
        raise NotImplementedError('initDNA() must be implemented in subclasses')

    # overriding NodePath's wrtReparentTo
    def wrtReparentTo(self, parent):
        NodePath.wrtReparentTo(self, parent)
        oldParent = self.dna.getParent()
        if hasattr(parent, 'dna') and oldParent == parent.dna:
            return
        if oldParent:
            oldParent.remove(self.dna)
        if hasattr(parent, 'dna'):
            parent.dna.add(self.dna)

    # overriding NodePath's reparentTo
    def reparentTo(self, parent):
        NodePath.reparentTo(self, parent)
        oldParent = self.dna.getParent()
        if hasattr(parent, 'dna') and oldParent == parent.dna:
            return
        if oldParent:
            oldParent.remove(self.dna)
        if hasattr(parent, 'dna'):
            parent.dna.add(self.dna)

    def removeDNA(self):
        dnaParent = self.dna.getParent()
        dnaParent.remove(self.dna)

    def remove(self):
        self.removeDNA()
        NodePath.remove(self)

    def setName(self, newName):
        NodePath.setName(self, newName)
        self.dna.setName(newName)

class ToonTownObj(ToonTownObjBase):
    def __init__(self, editor, dna, nodePath):
        self.styleManager = editor.styleManager
        ToonTownObjBase.__init__(self, editor, dna, nodePath)

    # overriding NodePath's setMat
    def setMat(self, tMat):
        NodePath.setMat(self, tMat)
        self.dna.setPos(self.getPos())
        self.dna.setHpr(self.getHpr())
        self.dna.setScale(self.getScale())

    # overriding NodePath's setPos
    def setPos(self, newPos):
        NodePath.setPos(self, newPos)
        self.dna.setPos(newPos)

    # overriding NodePath's setHpr
    def setHpr(self, newHpr):
        NodePath.setHpr(self, newHpr)
        self.dna.setHpr(newHpr)

    # overriding NodePath's setScale
    def setScale(self, newScale):
        NodePath.setScale(self, newScale)
        self.dna.setScale(newScale)
        
    def getNextLandmarkBlock(self):
        self.editor.landmarkBlock=self.editor.landmarkBlock+1
        return str(self.editor.landmarkBlock)

    def createSign(self):
        defaultSignStyle = self.styleManager.attributeDictionary['sign_texture'].getList()[0]
        newDNASign = DNASign('sign')
        #newDNASign.setCode(self.getCurrent('sign_texture'))
        #newDNASign.setColor(self.getCurrent('sign_color'))

        baseline = DNASignBaseline('baseline')
        baseline.setCode("humanist")
        baseline.setColor(VBase4(0.0, 0.0, 0.0, 1.0))
        baseline.setScale(VBase3(0.7, 1.0, 0.7))
        newDNASign.add(baseline)

        DNASetBaselineString(baseline, "Toon Shop")

        return newDNASign

    def createDoor(self, doorType):
        if (doorType == 'landmark_door'):
            newDNADoor = DNADoor('door')
            doorStyles = self.styleManager.attributeDictionary['door_double_texture'].getList()[1:]
            newDNADoor.setCode(random.choice(doorStyles))
            #newDNADoor.setCode(self.getCurrent('door_double_texture'))
            #newDNADoor.setColor(self.getCurrent('door_color'))
        elif (doorType == 'door'):
            newDNADoor = DNAFlatDoor('door')
            doorStyles = self.styleManager.attributeDictionary['door_single_texture'].getList()[1:]
            newDNADoor.setCode(random.choice(doorStyles))
            #newDNADoor.setCode(self.getCurrent('door_single_texture'))
            #newDNADoor.setColor(self.getCurrent('door_color'))
        return newDNADoor

    def createWindows(self):
        newDNAWindows = DNAWindows()
        windowStyles = self.styleManager.attributeDictionary['window_texture'].getList()[1:]
        newDNAWindows.setCode(random.choice(windowStyles))
        #newDNAWindows.setCode(self.getCurrent('window_texture'))
        newDNAWindows.setWindowCount(1)
        #newDNAWindows.setColor(self.getCurrent('window_color'))
        return newDNAWindows

    def setDNATargetCode(self, dnaType, dnaTarget, dnaParent, code):
        if dnaType != 'wall':
            dnaTarget = DNAGetChildOfClass(dnaParent, DNA_TYPE_DICT[dnaType])
            
        if (dnaTarget != None) and (code != None):
            dnaTarget.setCode(code)
        elif (dnaTarget != None) and (code == None):
            # Delete object, record pertinant properties before
            # you delete the object so you can restore them later
            # Remove object
            if (dnaType == 'cornice'):
                DNARemoveChildOfClass(dnaParent, DNA_CORNICE)
            elif (dnaType == 'sign'):
                DNARemoveChildOfClass(dnaParent, DNA_SIGN)
            elif (dnaType == 'landmark_door'):
                # since landmark buildings should have doors
                return
                #DNARemoveChildOfClass(dnaParent, DNA_DOOR)
            elif (dnaType == 'door'):
                DNARemoveChildOfClass(dnaParent, DNA_FLAT_DOOR)
            elif (dnaType == 'windows'):
                DNARemoveChildOfClass(dnaParent, DNA_WINDOWS)
            # Clear out DNATarget
            dnaTarget = None
        elif (dnaTarget == None) and (code != None):
            # Add new object
            if (dnaType == 'cornice'):
                dnaTarget = DNACornice('cornice')
                dnaTarget.setCode(code)
            elif (dnaType == 'sign'):
                dnaTarget = self.createSign()
                dnaTarget.setCode(code)
            elif (dnaType == 'landmark_door'):
                dnaTarget = self.createDoor('landmark_door')
                dnaTarget.setCode(code)
            elif (dnaType == 'door'):
                dnaTarget = self.createDoor('door')
                dnaTarget.setCode(code)
            elif (dnaType == 'windows'):
                # Now create the windows
                dnaTarget = self.createWindows()
                dnaTarget.setCode(code)
            if dnaTarget:
                dnaParent.add(dnaTarget)
        self.editor.ui.buildContextMenu(self)
        # Update visible representation
        self.replace()

    def setDNATargetColor(self, dnaType,  dnaTarget, dnaParent, color):
        if dnaParent and dnaType != 'wall':
            dnaTarget = DNAGetChildOfClass(dnaParent, DNA_TYPE_DICT[dnaType])
        if dnaTarget:
            dnaTarget.setColor(color)
            self.replace()

    def setDNATargetOrientation(self, dnaType, dnaTarget, dnaParent, orientation):
        if dnaParent and dnaType != 'wall':
            dnaTarget = DNAGetChildOfClass(dnaParent, DNA_TYPE_DICT[dnaType])
        if (dnaTarget != None) and (orientation != None):
            oldCode = dnaTarget.getCode()[:-2]
            # Suit walls only have two orientations!
            if oldCode.find('wall_suit') >= 0:
                orientation = 'u' + orientation[1]
            dnaTarget.setCode(oldCode+orientation)
            self.replace()

    def setWindowCount(self, dnaTarget, dnaParent, count):
        if count == 0 or dnaTarget is None:
            # not allowing set windows count to 0
            # since they could remove windows from window texture menu
            return
        if (dnaTarget != None) and (count != 0):
            dnaTarget.setWindowCount(count)
        self.replace()

    def setWallStyle(self, dnaTarget, style):
        if (dnaTarget != None) and (style != None):
            self.styleManager.setDNAWallStyle(
                dnaTarget, style,
                dnaTarget.getHeight())
            self.replace()
        
    def replace(self, populateSubDna = True):
        parent = self.getParent()
        dnaParent = self.dna.getParent()
        dnaParent.remove(self.dna)
        if populateSubDna:
            DNASTORE.removeDNAGroup(self.dna)
        # Get rid of the old node path and remove its DNA and
        # node relations from the DNA Store
        #self.remove()
        oldNp = NodePath(self)
        obj = self.editor.objectMgr.findObjectByNodePath(oldNp)
        uid = obj[OG.OBJ_UID]
        oldMat = Mat4(oldNp.getMat())
        del self.editor.objectMgr.npIndex[NodePath(oldNp)]
        childrenBackup = []
        for child in oldNp.getChildren():
            if child.hasTag('OBJRoot'):
                childObj = self.editor.objectMgr.findObjectByNodePath(child)
                childObjNP = childObj[OG.OBJ_NP]
                childObjNP.reparentTo(hidden)
                childrenBackup.append(childObjNP)
        oldNp.removeNode()

        # Traverse the old (modified) dna to create the new node path
        np = self.dna.traverse(parent, DNASTORE, 1)
        np.setTag('OBJRoot','1')
        np.setMat(oldMat)
        self.assign(np)
        obj[OG.OBJ_NP] = self
        self.editor.objectMgr.npIndex[NodePath(self)] = uid

        for childObjNP in childrenBackup:
            childObjNP.reparentTo(self)

        # Add it back to the dna parent
        dnaParent.add(self.dna)

        if DNAClassEqual(self.dna, DNA_ANIM_BUILDING) or\
           DNAClassEqual(self.dna, DNA_ANIM_PROP) or\
           DNAClassEqual(self.dna, DNA_INTERACTIVE_PROP): 
            self.createAnimatedProp()

        if populateSubDna:
            # update _subDna property
            obj[OG.OBJ_PROP]['_subDna'] = self.editor.objectMgr.populateSubDna(self.dna)

