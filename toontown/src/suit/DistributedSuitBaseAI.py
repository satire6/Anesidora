from otp.ai.AIBaseGlobal import *

from otp.avatar import DistributedAvatarAI
import SuitPlannerBase
import SuitBase
import SuitDNA
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import SuitBattleGlobals

class DistributedSuitBaseAI(DistributedAvatarAI.DistributedAvatarAI,
                         SuitBase.SuitBase):

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSuitBaseAI')

    def __init__(self, air, suitPlanner):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
        SuitBase.SuitBase.__init__(self)

        self.sp = suitPlanner

        # the current health of this suit
        # for now use some default values, these are pulled
        # from a table once the suit's level is determined
        #
        self.maxHP = 10
        self.currHP = 10
        self.zoneId = 0
        self.dna = None
        self.virtual = 0 #the red glowing effect
        
        self.skeleRevives = 0 #number of times to reanimate into a skeleCog
        self.maxSkeleRevives = 0 #keep track of how many times we have reanimated
        self.reviveFlag = 0

        # This is filled in only if the suit is trying to take over a
        # building of a particular height.
        self.buildingHeight = None

    def generate(self):
        DistributedAvatarAI.DistributedAvatarAI.generate(self)

    def delete(self):
        self.sp = None
        del self.dna
        DistributedAvatarAI.DistributedAvatarAI.delete(self)

    def requestRemoval(self):
        """
        Suggest that this suit is done with its duties and should be removed.
        """
        if (self.sp != None):
            # If we have a SuitPlanner, it should do the removing.
            self.sp.removeSuit(self)
        else:
            # Otherwise, remove ourselves.
            self.requestDelete()

    def setLevel(self, lvl=None):
        """
        Function:    randomly choose a level for this suit based on the
                     type of the suit (such as yesman, flunky, etc) or
                     set the level to be the one specified
        Parameters:  lvl, level the suit should be
        """
        attributes = SuitBattleGlobals.SuitAttributes[ self.dna.name ]
        if lvl:
            self.level = lvl - attributes[ 'level' ] - 1
        else:
            self.level = SuitBattleGlobals.pickFromFreqList(
                attributes[ 'freq' ])
        self.notify.debug("Assigning level " + str(lvl))
        if hasattr(self, "doId"):
            self.d_setLevelDist(self.level)

        # be sure to set the hp to proper values based on the suit's
        # new level
        #
        hp = attributes['hp'][self.level]
        self.maxHP = hp
        self.currHP = hp
        assert self.notify.debug("Assigning hp " + str(self.currHP))

    def getLevelDist(self):
        """
        Function:    the distributed function to be called when the
                     server side suit changes level
        Parameters:  level, the new level of the suit
        """
        return self.getLevel()

    def d_setLevelDist(self, level):
        """
        Function:    the distributed function to be called when the
                     server side suit changes level
        Parameters:  level, the new level of the suit
        """
        self.sendUpdate('setLevelDist', [level])

    def setupSuitDNA(self, level, type, track):
        """
        setupSuitDNA(self, int level, int type, char track)

        Creates the suit DNA, according to the indicated level (1..9),
        type (1..8), and track ("c", "l", "m", "s").
        """
        dna = SuitDNA.SuitDNA()
        dna.newSuitRandom(type, track)
        self.dna = dna
        self.track = track
        self.setLevel(level)

        return None

    def getDNAString(self):
        """
        Function:    retrieve the dna information from this suit, called
                     whenever a client needs to create this suit
        Parameters:  none
        Returns:     netString representation of this suit's dna
        """
        if self.dna:
            return self.dna.makeNetString()
        else:
            self.notify.debug('No dna has been created for suit %d!' % \
                self.getDoId())
            return ""

    # setBrushOff
    def b_setBrushOff(self, index):
        # Local
        self.setBrushOff(index)
        # Distributed
        self.d_setBrushOff(index)
        return None

    def d_setBrushOff(self, index):
        self.sendUpdate("setBrushOff", [index])

    def setBrushOff(self, index):
        # I guess on the AI side there is nothing to do here
        pass

    def d_denyBattle(self, toonId):
        self.sendUpdateToAvatarId(toonId, 'denyBattle', [])
        
    def b_setSkeleRevives(self, num):
        if num == None:
            num = 0
        self.setSkeleRevives(num)
        self.d_setSkeleRevives(self.getSkeleRevives())
        
    def d_setSkeleRevives(self, num):
        self.sendUpdate("setSkeleRevives" , [num])
        
    def getSkeleRevives(self):
        return self.skeleRevives
        
    def setSkeleRevives(self, num):
        if num == None:
            num = 0
        self.skeleRevives = num
        if num > self.maxSkeleRevives:
            self.maxSkeleRevives = num
            
    def getMaxSkeleRevives(self):
        return self.maxSkeleRevives

    def useSkeleRevive(self):
        self.skeleRevives -= 1
        self.currHP = self.maxHP
        self.reviveFlag = 1
        
    def reviveCheckAndClear(self):
        returnValue = 0
        if self.reviveFlag == 1:
            returnValue = 1
            self.reviveFlag = 0
        return returnValue

    def getHP(self):
        return self.currHP

    def setHP(self, hp):
        """
        Function:    set the current health of this suit, this can
                     be called during battle and at initialization
        Parameters:  hp, value to set health to
        """
        if hp > self.maxHP:
            self.currHP = self.maxHP
        else:
            self.currHP = hp
        return None

    def b_setHP(self, hp):
        self.setHP(hp)
        self.d_setHP(hp)

    def d_setHP(self, hp):
        self.sendUpdate("setHP", [hp])
        
    def releaseControl(self):
        # Do whatever needs to be done to turn control of the suit over to
        # another party (e.g. a battle) - should be redefined by child if
        # any behavior is required
        return None

    def getDeathEvent(self):
        return 'cogDead-%s' % self.doId

    def resume(self):
        self.notify.debug('resume, hp=%s' % self.currHP)

        # Do whatever needs to be done to restore control of the suit from 
        # another party (e.g. a battle) - should be redefined by child if
        # any additional behavior is required
        if (self.currHP <= 0):
            messenger.send(self.getDeathEvent())
            # Clean up dead suits
            self.requestRemoval()
        return None

    def prepareToJoinBattle(self):
        """
        do whatever is appropriate when the suit is about to join
        a battle; most likely, stop doing anything and let the battle
        puppeteer
        """
        pass

    def b_setSkelecog(self, flag):
        self.setSkelecog(flag)
        self.d_setSkelecog(flag)

    def setSkelecog(self, flag):
        SuitBase.SuitBase.setSkelecog(self, flag)
        
    def d_setSkelecog(self, flag):
        # send update
        self.sendUpdate("setSkelecog", [flag])

    def isForeman(self):
        """is this a factory foreman?"""
        return 0
    
    def isSupervisor(self):
        """is this a mint floor supervisor?"""
        return 0

    def setVirtual(self, virtual):
        pass
        
    def getVirtual(self):
        return 0

    # just for consistencies sake
    def isVirtual(self):
        """is this a virtual laser cog?"""
        return self.getVirtual()

    
