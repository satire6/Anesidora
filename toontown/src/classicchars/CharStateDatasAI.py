"""CharStateDatasAI module: contains the server variation of the various
state datas available to the classic character NPC's found in safezones"""
#from PandaModules import *
from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *

from direct.fsm import StateData
from direct.directnotify import DirectNotifyGlobal
import random
from direct.task import Task
from toontown.toonbase import ToontownGlobals

import CCharChatter
import CCharPaths

class CharLonelyStateAI(StateData.StateData):
    """
    ////////////////////////////////////////////////////////////////////
    //
    // CharLonelyStateAI:  available to a character that might get lonely
    //                     once in a while and just stand by his or her
    //                     self for a little while, responding to toons
    //                     that pass by.
    //
    ////////////////////////////////////////////////////////////////////
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("CharLonelyStateAI")

    def __init__(self, doneEvent, character):
        StateData.StateData.__init__(self, doneEvent)
        self.__doneEvent = doneEvent
        self.character = character

    def enter(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the character enters the lonely state
        //             create a doLater to wait a random amount of time
        //             before deciding what to do next (such as walk to a
        //             new area).
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # so lonely... oh, so lonely...
        if hasattr( self.character, "name" ):
            name = self.character.getName()
        else:
            name = "character"
        self.notify.debug("Lonely " + self.character.getName() + "...")

        # pick a random amount of time in which to stay in lonely state
        # before deciding what to do next
        #
        StateData.StateData.enter(self)
        duration = random.randint(3,15)
        taskMgr.doMethodLater( duration,
                               self.__doneHandler,
                               self.character.taskName("startWalking") )

    def exit(self):
        StateData.StateData.exit(self)
        taskMgr.remove(self.character.taskName("startWalking"))

    def __doneHandler(self, task):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   done being lonely, send a message to notify the
        //             character and it will decide which state to go to
        //             next
        // Parameters: task, the task that called this function
        // Changes:    none
        // Returns:    task done status
        ////////////////////////////////////////////////////////////////////
        """
        doneStatus = {}
        doneStatus['state'] = 'lonely'
        doneStatus['status'] = 'done'
        messenger.send(self.__doneEvent, [doneStatus])
        return Task.done


class CharChattyStateAI(StateData.StateData):
    """
    ////////////////////////////////////////////////////////////////////
    //
    // CharChattyStateAI:  available to a character that is able to
    //                     talk to players when they get close enough
    //
    ////////////////////////////////////////////////////////////////////
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("CharChattyStateAI")

    def __init__(self, doneEvent, character):
        StateData.StateData.__init__(self, doneEvent)
        self.__doneEvent = doneEvent
        self.character = character

        self.__chatTaskName = "characterChat-" + str(character)

        # this is set to the id of the toon that this character last
        # spoke to
        self.lastChatTarget = 0
        # Character should not talk until we reach this time
        self.nextChatTime = 0
        # this is the last thing character said
        self.lastMessage = [-1, -1] # category, message index

    def enter(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the character enters the lonely state
        //             create a doLater to wait a random amount of time
        //             before deciding what to do next (such as walk to a
        //             new area).
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # so lonely... oh, so lonely...
        if hasattr( self.character, "name" ):
            name = self.character.getName()
        else:
            name = "character"
        self.notify.debug("Chatty " + self.character.getName() + "...")

        # if the last person we talked to leaves the chat
        # sphere and re-enters, don't greet them again
        #self.lastChatTarget = 0
        
        self.chatter = CCharChatter.getChatter(self.character.getName(),
                                               self.character.getCCChatter())

        # only spawn the chat task if this is a talking char
        if self.chatter != None:
            # remove any old
            taskMgr.remove(self.__chatTaskName)
            # spawn the new task
            taskMgr.add(self.blather, self.__chatTaskName)

        StateData.StateData.enter(self)

    # pick a random message
    def pickMsg(self, category):    
        self.getLatestChatter()
        if self.chatter:
            return random.randint(0, len(self.chatter[category])-1)
        else:
            return None
            
    def getLatestChatter(self):
        self.chatter = CCharChatter.getChatter(self.character.getName(),
                                               self.character.getCCChatter())

    def setCorrectChatter(self):
        """Forces an update on self.chatter, possibly affected by holidays."""
        self.chatter = CCharChatter.getChatter(self.character.getName(),
                                               self.character.getCCChatter())

    def blather(self, task):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   say something if it is time to
        // Parameters: task, task which calls this function repeatedly
        // Changes:
        // Returns:    task status
        ////////////////////////////////////////////////////////////////////
        """
        now = globalClock.getFrameTime()
        if now < self.nextChatTime:
            return Task.cont
            
        self.getLatestChatter()

        if self.character.lostInterest():
            # character is bored.
            self.leave()
            return Task.done 
            
        if not self.chatter:
            self.notify.debug("I do not want to talk")
            return Task.done        

        if not self.character.getNearbyAvatars():
            return Task.cont

        target = self.character.getNearbyAvatars()[0]

        # say something profound
        if self.lastChatTarget != target:
            self.lastChatTarget = target
            category = CCharChatter.GREETING
        else:
            category = CCharChatter.COMMENT            

        # avoid an index out of range crash
        self.setCorrectChatter()

        # if the category is the same as the last message,
        # and there's more than one message, pick a different
        # message
        if (            
            category == self.lastMessage[0] and
            len(self.chatter[category]) > 1
            ):
            # make sure character doesn't say the same thing twice
            msg = self.lastMessage[1]
            #while (msg == self.lastMessage[1]):
            # look at actual msg - not index
            lastMsgIndex = self.lastMessage[1]
            if (lastMsgIndex < len(self.chatter[category])) and (lastMsgIndex >= 0) :
                while (self.chatter[category][msg] == self.chatter[category][lastMsgIndex]):
                    msg = self.pickMsg(category)
                    if not msg:
                        break
            else:
                # our last message index was invalid, we probably switched from holiday chatter
                # to regular chatter or vice versa
                # very small chance we repeat, but it's better than crashing
                msg = self.pickMsg(category)
        else:
            msg = self.pickMsg(category)
        
        if msg == None:
            self.notify.debug("I do not want to talk")
            return Task.done
            
        self.character.sendUpdate("setChat", [category, msg, target])

        self.lastMessage = [category, msg] # category, message index

        self.nextChatTime = now + 8.0 + (random.random() * 4.0)

        return Task.cont

    def leave(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the character decides to leave and has
        //             more important things to do than being friendly
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # if we talk, say goodbye.
        if self.chatter != None:
            category = CCharChatter.GOODBYE
            msg = random.randint(0,
                                   len(self.chatter[CCharChatter.GOODBYE])-1)
            target = self.character.getNearbyAvatars()[0]
            self.character.sendUpdate("setChat", [category, msg, target])

        # set up a doLater to make character walk away
        taskMgr.doMethodLater( 1, self.doneHandler,
                               self.character.taskName("waitToFinish") )

    def exit(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   leave the chatty state, clean up dangling tasks
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        StateData.StateData.exit(self)
        taskMgr.remove(self.__chatTaskName)

    def doneHandler(self, task):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   done being lonely, send a message to notify the
        //             character and it will decide which state to go to
        //             next
        // Parameters: task, the task that called this function
        // Changes:    none
        // Returns:    task done status
        ////////////////////////////////////////////////////////////////////
        """
        doneStatus = {}
        doneStatus['state'] = 'chatty'
        doneStatus['status'] = 'done'
        messenger.send(self.__doneEvent, [doneStatus])
        return Task.done


class CharWalkStateAI(StateData.StateData):
    """
    ////////////////////////////////////////////////////////////////////
    //
    // CharWalkStateAI:  available to a character that is able to
    //                   walk around a predetermined set of waypoints
    //
    ////////////////////////////////////////////////////////////////////
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("CharWalkStateAI")

    def __init__(self, doneEvent, character, diffPath = None):
        StateData.StateData.__init__(self, doneEvent)
        self.__doneEvent = doneEvent
        self.character = character
        if diffPath == None:
            self.paths = CCharPaths.getPaths(character.getName(),
                                         character.getCCLocation())
        else:
            self.paths = CCharPaths.getPaths(diffPath, character.getCCLocation())
        self.speed = character.walkSpeed()

        # this is the last node that the character was at
        self.__lastWalkNode = CCharPaths.startNode
        self.__curWalkNode = CCharPaths.startNode

    def enter(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the character enters the walk state
        //             create a doLater to wait a specific amount of time
        //             while character gets to the destination on all client
        //             machines.
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # choose a destination
        # choose a new destination node, different from last
        destNode = self.__lastWalkNode
        choices = CCharPaths.getAdjacentNodes(self.__curWalkNode, self.paths)
        if len(choices) == 1:
            destNode = choices[0]
        else:
            while destNode == self.__lastWalkNode:
                destNode = random.choice(
                    CCharPaths.getAdjacentNodes(self.__curWalkNode, self.paths))

        self.notify.debug("Walking " +
                          self.character.getName() +
                          "... from " + \
                          str(self.__curWalkNode) + "(" +
                          str(CCharPaths.getNodePos(self.__curWalkNode,
                                                    self.paths))
                          + ") to " + \
                          str(destNode) + "(" +
                          str(CCharPaths.getNodePos(destNode,self.paths)) +
                          ")")

        # broadcast the walk
        self.character.sendUpdate("setWalk", [self.__curWalkNode, destNode, globalClockDelta.getRealNetworkTime()])

        # set up a doLater to fire when character is done walking
        duration = CCharPaths.getWalkDuration(self.__curWalkNode,
                                              destNode,
                                              self.speed,
                                              self.paths)
        t = taskMgr.doMethodLater(
            duration,
            self.doneHandler,
            self.character.taskName(self.character.getName() +
                                    "DoneWalking") )
        t.newWalkNode = destNode

        # keep track of the destination since dale needs to know about
        self.destNode = destNode

    def exit(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   leave the walk state, clean up dangling tasks
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        StateData.StateData.exit(self)
        taskMgr.remove(self.character.taskName( self.character.getName() +
                                                "DoneWalking"))

    def getDestNode(self):
        """Return the destination node he's walking to."""
        # if the node hasn't been created, retunr the first node
        if hasattr(self,"destNode") and self.destNode:
            return self.destNode
        else:
            return self.__curWalkNode

    def setCurNode(self, curWalkNode):
        self.__curWalkNode = curWalkNode

    def doneHandler(self, task):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   done walking, send a message to notify the
        //             character and it will decide which state to go to
        //             next
        // Parameters: task, the task that called this function
        // Changes:    none
        // Returns:    task done status
        ////////////////////////////////////////////////////////////////////
        """
        # this is called after the walk duration expires
        # transition back to lonely or chatty, depending
        # on the number of nearby avatars

        # set the new walk node position
        self.__lastWalkNode = self.__curWalkNode
        self.__curWalkNode = task.newWalkNode

        # Send an update that indicates the character is definitely at
        # its node now.
        self.character.sendUpdate("setWalk", [self.__curWalkNode, self.__curWalkNode, globalClockDelta.getRealNetworkTime()])

        doneStatus = {}
        doneStatus['state'] = 'walk'
        doneStatus['status'] = 'done'
        messenger.send(self.__doneEvent, [doneStatus])
        return Task.done


class CharFollowChipStateAI(StateData.StateData):
    """
    ////////////////////////////////////////////////////////////////////
    //
    // CharWalkStateAI:  available to a character that is able to
    //                   buzz around around another classic char
    //
    ////////////////////////////////////////////////////////////////////
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("CharFollowChipStateAI")

    def __init__(self, doneEvent, character, followedChar):
        StateData.StateData.__init__(self, doneEvent)
        self.__doneEvent = doneEvent
        self.character = character
        self.followedChar = followedChar
        self.paths = CCharPaths.getPaths( character.getName(),
                                          character.getCCLocation() )
        self.speed = character.walkSpeed()

        # this is the last node that the character was at
        self.__lastWalkNode = CCharPaths.startNode
        self.__curWalkNode = CCharPaths.startNode

    def enter(self, chipDestNode):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the character enters the walk state
        //             create a doLater to wait a specific amount of time
        //             while character gets to the destination on all client
        //             machines.
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # choose a destination
        # choose a new destination node, different from last
        #import pdb; pdb.set_trace()
        destNode = self.__lastWalkNode
        choices = CCharPaths.getAdjacentNodes(self.__curWalkNode, self.paths)
        if len(choices) == 1:
            destNode = choices[0]
        else:
            while destNode == self.__lastWalkNode:
                destNode = random.choice(
                    CCharPaths.getAdjacentNodes(self.__curWalkNode, self.paths))

        destNode = chipDestNode
        self.notify.debug("Walking " +
                          self.character.getName() +
                          "... from " + \
                          str(self.__curWalkNode) + "(" +
                          str(CCharPaths.getNodePos(self.__curWalkNode,
                                                    self.paths))
                          + ") to " + \
                          str(destNode) + "(" +
                          str(CCharPaths.getNodePos(destNode,self.paths)) +
                          ")")
        # calculate an offset
        self.offsetDistance = ToontownGlobals.DaleOrbitDistance
        angle = random.randint(0,359)
        self.offsetX = math.cos(deg2Rad(angle))* self.offsetDistance
        self.offsetY = math.sin(deg2Rad(angle))* self.offsetDistance

        # broadcast the walk
        self.character.sendUpdate("setFollowChip", [self.__curWalkNode, destNode, globalClockDelta.getRealNetworkTime(), self.offsetX, self.offsetY])

        # set up a doLater to fire when character is done walking
        duration = CCharPaths.getWalkDuration(self.__curWalkNode,
                                              destNode,
                                              self.speed,
                                              self.paths)
        t = taskMgr.doMethodLater(
            duration,
            self.__doneHandler,
            self.character.taskName(self.character.getName() +
                                    "DoneWalking") )
        t.newWalkNode = destNode

    def exit(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   leave the walk state, clean up dangling tasks
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        StateData.StateData.exit(self)
        taskMgr.remove(self.character.taskName( self.character.getName() +
                                                "DoneWalking"))

    def __doneHandler(self, task):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   done walking, send a message to notify the
        //             character and it will decide which state to go to
        //             next
        // Parameters: task, the task that called this function
        // Changes:    none
        // Returns:    task done status
        ////////////////////////////////////////////////////////////////////
        """
        # this is called after the walk duration expires
        # transition back to lonely or chatty, depending
        # on the number of nearby avatars

        # set the new walk node position
        self.__lastWalkNode = self.__curWalkNode
        self.__curWalkNode = task.newWalkNode

        # Send an update that indicates the character is definitely at
        # its node now.
        self.character.sendUpdate("setFollowChip", [self.__curWalkNode, self.__curWalkNode, globalClockDelta.getRealNetworkTime(), self.offsetX, self.offsetY])

        doneStatus = {}
        doneStatus['state'] = 'walk'
        doneStatus['status'] = 'done'
        messenger.send(self.__doneEvent, [doneStatus])
        return Task.done


class ChipChattyStateAI(CharChattyStateAI):

    notify = DirectNotifyGlobal.directNotify.newCategory("ChipChattyStateAI")

    def setDaleId(self, daleId):
        """Set the dale id, so chip knows aout him."""
        self.daleId = daleId
        self.dale = simbase.air.doId2do.get(self.daleId)

    def blather(self, task):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   say something if it is time to
        // Parameters: task, task which calls this function repeatedly
        // Changes:
        // Returns:    task status
        ////////////////////////////////////////////////////////////////////
        """
        now = globalClock.getFrameTime()
        if now < self.nextChatTime:
            return Task.cont

        self.getLatestChatter()

        if self.character.lostInterest():
            # character is bored.
            self.leave()
            return Task.done 
            
        if not self.chatter:
            self.notify.debug("I do not want to talk")
            return Task.done        

        if not self.character.getNearbyAvatars():
            return Task.cont

        target = self.character.getNearbyAvatars()[0]

        # say something profound
        if self.lastChatTarget != target:
            self.lastChatTarget = target
            category = CCharChatter.GREETING
        else:
            category = CCharChatter.COMMENT

        # if the category is the same as the last message,
        # and there's more than one message, pick a different
        # message
        if (
            category == self.lastMessage[0] and
            len(self.chatter[category]) > 1
            ):
            # make sure character doesn't say the same thing twice
            msg = self.lastMessage[1]
            #while (msg == self.lastMessage[1]):
            # look at actual msg - not index
            lastMsgIndex = self.lastMessage[1]
            if (lastMsgIndex < len(self.chatter[category])) and (lastMsgIndex >= 0) :
                while (self.chatter[category][msg] == self.chatter[category][lastMsgIndex]):
                    msg = self.pickMsg(category)
                    if not msg:
                        break
            else:
                msg = self.pickMsg(category)
                #import pdb; pdb.set_trace()
        else:
            msg = self.pickMsg(category)
            
        if msg == None:
            self.notify.debug("I do not want to talk")
            return Task.done

        self.character.sendUpdate("setChat", [category, msg, target])

        # inform dale what we're saying
        if hasattr(self, 'dale') and self.dale:
            self.dale.sendUpdate("setChat", [category, msg, target])

        self.lastMessage = [category, msg] # category, message index

        self.nextChatTime = now + 8.0 + (random.random() * 4.0)

        return Task.cont

    def leave(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:   called when the character decides to leave and has
        //             more important things to do than being friendly
        // Parameters: none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        # if we talk, say goodbye.
        if self.chatter != None:
            category = CCharChatter.GOODBYE
            msg = random.randint(0,
                                   len(self.chatter[CCharChatter.GOODBYE])-1)
            target = self.character.getNearbyAvatars()[0]
            self.character.sendUpdate("setChat", [category, msg, target])
            if hasattr(self,'dale') and self.dale:
                self.dale.sendUpdate("setChat", [category, msg, target])


        # set up a doLater to make character walk away
        taskMgr.doMethodLater( 1, self.doneHandler,
                               self.character.taskName("waitToFinish") )

# history
#
# 01Oct01    jlbutler    created.
#
