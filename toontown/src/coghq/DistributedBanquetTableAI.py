import random
from direct.distributed import DistributedObjectAI
from direct.fsm import FSM
from direct.directnotify import DirectNotifyGlobal
from toontown.coghq import BanquetTableBase
from toontown.toonbase import ToontownGlobals

class DistributedBanquetTableAI(DistributedObjectAI.DistributedObjectAI, FSM.FSM,
                                BanquetTableBase.BanquetTableBase):
    """ This class represents an AI banquet table and the associated chairs,
    The DistributedBossbotBoss creates several of these for the CEO
    battle scene. """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBanquetTableAI')

    def __init__(self, air, boss, index, numDiners, dinerLevel):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        FSM.FSM.__init__(self, 'DistributedBanquetTableAI')
        self.boss = boss # the CEO himself
        self.index = index # distinguishes us from the 13 tables in the scene
        self.numDiners = numDiners
        self.numChairs = 8
        self.dinerStatus = {} # is the dinner dead, hungry,  eating
        self.dinerInfo = {} # keep track how long they stay in hungry and eating states
        for i in xrange(self.numDiners):
            self.dinerStatus[i] = self.INACTIVE
            diffSettings = ToontownGlobals.BossbotBossDifficultySettings[self.boss.battleDifficulty]
            hungryDuration = diffSettings[4]
            eatingDuration = diffSettings[5]
            hungryDuration += random.uniform(-5,5)
            eatingDuration += random.uniform(-5,5)
            level = 12
            if type(dinerLevel) == type(0):
                level = dinerLevel
            else:
                level = random.choice(dinerLevel)
                
            self.dinerInfo[i] = (hungryDuration, eatingDuration, level)
            # (hungryDuration, eatingDuration, dinerLevel)
            #self.dinerInfo[i] = (20, 30, self.dinerLevel)
        self.transitionTasks = {}
        self.numFoodEaten = {}
        self.avId = 0 # which toon is controlling us

    def delete(self):
        """Delete ourself."""
        DistributedObjectAI.DistributedObjectAI.delete(self)
        
    def getBossCogId(self):
        """Return the doId of the associated CEO."""
        return self.boss.doId

    def getIndex(self):
        """Return our index which identifies our side."""
        return self.index

    def getNumDiners(self):
        """Return how many diners we have."""
        return self.numDiners

    def getDinerStatus(self, chairIndex):
        """Return the staus of a diner in a chair."""
        retval = self.DEAD
        if chairIndex in self.dinerStatus:
            retval = self.dinerStatus[chairIndex]
        return retval

    def setDinerStatus(self, chairIndex, newStatus):
        """Set the staus of a diner in a chair."""
        self.dinerStatus[chairIndex] = newStatus

    def getDinerInfo(self):
        """Return an array of our hungry and eating durations."""
        hungryDurations = []
        eatingDurations = []
        dinerLevels = []
        for i in xrange(self.numDiners):
            hungryDurations.append(self.dinerInfo[i][0])
            eatingDurations.append(self.dinerInfo[i][1])
            dinerLevels.append(self.dinerInfo[i][2])
        return hungryDurations, eatingDurations, dinerLevels
                                   

    def d_setDinerStatus(self, chairIndex, newStatus):
        """Send the new diner status."""
        self.sendUpdate('setDinerStatus', [chairIndex, newStatus])

    def b_setDinerStatus(self, chairIndex, newStatus):
        """Set the diner status on the ai and the client."""
        self.setDinerStatus(chairIndex, newStatus)
        self.d_setDinerStatus(chairIndex, newStatus)

    def setState(self, state):
        self.request(state)
    
    def d_setState(self, state, avId=0, extraInfo=0):
        newState = state
        if state == 'On':
            newState = 'N'
        elif state == 'Off':
            newState = 'F'
        elif state == 'Inactive':
            newState = 'I'
        elif state == 'Free':
            newState = 'R'
        elif state == 'Controlled':
            newState = 'C'
        elif state == 'Flat':
            newState = 'L'
        else:
            assert(self.notify.error("Unknown state %s", state))
        
        self.sendUpdate('setState', [newState, avId, extraInfo])
 
    def b_setState(self, state, avId =0, extraInfo = 0):
        if state == 'Controlled' or state == 'Flat':
            self.request(state, avId)
        else:
            self.request(state)
        self.d_setState( state, avId, extraInfo) 

    def turnOn(self):
        """Force us and clients to the On state."""
        self.b_setState('On')

    def turnOff(self):
        """Force us and clients to the Off state."""
        # happens when we are going to the reward state in the CEO battle
        self.b_setState('Off')        

    def foodServed(self, chairIndex):
        """Handle a player succesfully serving food on a diner."""
        self.b_setDinerStatus(chairIndex, self.EATING)
        eatingDur = self.dinerInfo[chairIndex][1]
        if chairIndex in self.transitionTasks:
            self.removeTask(self.transitionTasks[chairIndex])
        taskName = self.uniqueName('transition-%d' % chairIndex)
        newTask = self.doMethodLater(eatingDur, self.finishedEating, taskName, extraArgs = [chairIndex])
        self.transitionTasks[chairIndex] = newTask

    def finishedEating(self, chairIndex):
        """Handle a diner finishing eating."""
        if chairIndex in self.transitionTasks:
            self.removeTask(self.transitionTasks[chairIndex])
        self.incrementFoodEaten(chairIndex)
        if self.numFoodEaten[chairIndex] >= ToontownGlobals.BossbotNumFoodToExplode:
            self.b_setDinerStatus(chairIndex, self.DEAD)
            self.boss.incrementDinersExploded()
        else:
            self.b_setDinerStatus(chairIndex, self.HUNGRY)
            taskName = self.uniqueName('transition-%d' % chairIndex)
            hungryDur = self.dinerInfo[chairIndex][0]
            newTask = self.doMethodLater(hungryDur, self.finishedHungry, taskName, extraArgs = [chairIndex])
            self.transitionTasks[chairIndex] = newTask
            
    def incrementFoodEaten(self, chairIndex):
        """Increase the number of food eaten for a diner."""
        numFood = 0
        if chairIndex in self.numFoodEaten:
            numFood = self.numFoodEaten[chairIndex]
        self.numFoodEaten[chairIndex] = numFood +1

    def finishedHungry(self, chairIndex):
        """Handle a diner getting fed up in Hungry and going to Angry."""
        self.b_setDinerStatus(chairIndex, self.ANGRY)
        self.numFoodEaten[chairIndex] = 0
        if chairIndex in self.transitionTasks:
            self.removeTask(self.transitionTasks[chairIndex])

    def goInactive(self):
        """Force a transition to go inactive."""
        self.b_setState('Inactive')

    def goFree(self):
        """Force a transition to go to free."""
        self.b_setState('Free')        

    def goFlat(self):
        """Force a transition to go to free."""
        self.b_setState('Flat', self.avId)        


    def getNotDeadInfo(self):
        """Return a list of (<table index>, <chair Index>, <suit level>) suits that are not dead."""
        notDeadList  = []
        for i in xrange(self.numDiners):
            if self.dinerStatus[i] != self.DEAD:
                notDeadList.append( (self.index, i, self.dinerInfo[i][2]))
        return notDeadList
        
    def requestControl(self):
        """Handle request from client to control the pitcher."""
        assert self.notify.debugStateCall(self)        
        # A client wants to start controlling the pitcher.
        avId = self.air.getAvatarIdFromSender()
        
        if avId in self.boss.involvedToons and self.avId == 0 and self.state == 'Free':
            # Also make sure the client isn't controlling some other
            # table.
            tableId = self.__getTableId(avId)
            if tableId == 0:
                # one last check, make sure the toon is roaming
                grantRequest = True
                if self.boss and not self.boss.isToonRoaming(avId):
                    grantRequest = False
                if grantRequest:
                    self.b_setState('Controlled', avId)

    def forceControl(self, avId):
        """Force the table into the controlled state."""
        self.notify.debug('forceContrl  tableIndex=%d avId=%d' % (self.index, avId))
        tableId = self.__getTableId(avId)
        if tableId == self.doId:
            if self.state == 'Flat':
                self.b_setState('Controlled', avId)
            else:
                self.notify.warning('invalid forceControl from state %s' % self.state)
        else:
            self.notify.warning('tableId %d  != self.doId %d ' %(tableId, self.doId))
        

    def requestFree(self, gotHitByBoss):
        """Handle request from client to exit the pitcher."""
        # The client is done controlling the Pitcher.
        avId = self.air.getAvatarIdFromSender()
        if avId == self.avId:
            if self.state == 'Controlled':
                self.b_setState('Free', extraInfo = gotHitByBoss)
                if self.boss:
                    self.boss.toonLeftTable(self.index)
            else:
                self.notify.debug('requestFree denied in state %s' % self.state)          

    def __getTableId(self, avId):
        # Returns the craneId for the crane that the indicated avatar
        # is controlling, or 0 if none.

        if self.boss and self.boss.tables != None:
            for table in self.boss.tables:
                if table.avId == avId:
                    return table.doId

        return 0                

    ### FSM States ###
    def enterOn(self):
        for i in xrange(self.numDiners):
            self.b_setDinerStatus(i, self.HUNGRY)
        """Handle entering the on state."""
        pass

    def exitOn(slef):
        """Handle exiting the off state."""
        pass

    def enterOff(self):
        """Handle entering the off state."""
        pass

    def exitOff(self):
        """Handle exiting the off state."""
        pass

    def enterInactive(self):
        """Handle going to the inactive state."""
        for task in self.transitionTasks.values():
            self.removeTask(task)
        self.transitionTasks = {}

    def exitInactive(self):
        """Handle going out of the inactive state."""
        pass

    def enterFree(self):
        """Handle going to the water state. Water shoots out at the boss"""
        self.notify.debug('enterFree tableIndex=%d' % self.index)
        self.avId = 0
        pass

    def exitFree(self):
        """Handle going to the inactive state."""
        pass

    def enterControlled(self, avId):
        """Handle going to the controlled state by the given toon."""
        self.notify.debug('enterControlled tableIndex=%d' % self.index)  
        self.avId = avId
        #self.d_setState('C', avId)

    def exitControlled(self):
              
        """Handle exiting to the controlled state by the given toon."""        
        pass

    def enterFlat(self, avId):
        """Handle going to the controlled state by the given toon."""
        self.notify.debug('enterFlat tableIndex=%d' % self.index)        
        #self.avId = avId
        #self.avId = 0
        pass

    def exitFlat(self):
        """Handle exiting to the controlled state by the given toon."""        
        pass
