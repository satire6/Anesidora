from direct.distributed import DistributedObjectAI
from direct.fsm import FSM
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import FoodBeltBase

class DistributedFoodBeltAI(DistributedObjectAI.DistributedObjectAI, FSM.FSM, FoodBeltBase.FoodBeltBase):
    """ This class represents an AI side conveyer belt bringing cog food out.
    The DistributedLawbotBoss creates 2 of these for the CEO
    battle scene. """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFoodBeltAI')

    def __init__(self, air, boss, index):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        FSM.FSM.__init__(self, 'DistributedFoodBeltAI')
        self.boss = boss # the CEO himself
        self.index = index # 0-left side belt, 1-right side belt

    def delete(self):
        """Delete ourself."""
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def getBossCogId(self):
        """Return the doId of the associated CEO."""
        return self.boss.doId

    def getIndex(self):
        """Return our index which identifies our side."""
        return self.index

    def setState(self, state):
        self.request(state)
    
    def d_setState(self, state):
        newState = state
        if state == 'On':
            newState = 'N'
        elif state == 'Off':
            newState = 'F'
        elif state == 'Inactive':
            newState = 'I'
        elif state == 'Toonup':
            newState = 'T'                
        else:
            assert(self.notify.error("Unknown state %s", state))
        
        self.sendUpdate('setState', [newState])

    def b_setState(self, state):
        self.request(state)
        self.d_setState( state) 

    def turnOn(self):
        #we've entered battle two so start move
        self.b_setState('On')

    def goInactive(self):
        """Force us into the inactive state."""
        self.b_setState('Inactive')

    def goToonup(self):
        """Force us into the inactive state."""
        self.b_setState('Toonup')           

    ### FSM States ###
    def enterOn(self):
        """Handle entering the on state."""
        pass

    def exitOn(slef):
        """Handle exiting the on state."""
        pass

    def enterOff(self):
        """Handle entering the off state."""
        pass

    def exitOff(self):
        """Handle exiting the off state."""
        pass

    def enterInactive(self):
        """Handle entering the inactive state."""
        pass

    def exitInactive(slef):
        """Handle exiting the inactive state."""
        pass        
