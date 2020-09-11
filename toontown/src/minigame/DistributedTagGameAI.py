
from DistributedMinigameAI import *
from TagTreasurePlannerAI import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import random
import TagGameGlobals

class DistributedTagGameAI(DistributedMinigameAI):

    DURATION = TagGameGlobals.DURATION

    def __init__(self, air, minigameId):
        try:
            self.DistributedTagGameAI_initialized
        except:
            self.DistributedTagGameAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedTagGameAI',
                                   [State.State('inactive',
                                                self.enterInactive,
                                                self.exitInactive,
                                                ['play']),
                                    State.State('play',
                                                self.enterPlay,
                                                self.exitPlay,
                                                ['cleanup']),
                                    State.State('cleanup',
                                                self.enterCleanup,
                                                self.exitCleanup,
                                                ['inactive']),
                                    ],
                                   # Initial State
                                   'inactive',
                                   # Final State
                                   'inactive',
                                   )

            # Add our game ClassicFSM to the framework ClassicFSM
            self.addChildGameFSM(self.gameFSM)

            self.treasureScores = {}

            # This is the pointer to the avId that is currently "it"
            self.itAvId = None

            # Flag to prevent immediate tag backs
            self.tagBack = 1

    # Generate is never called on the AI so we do not define one
    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.setGameReady(self)
        for avId in self.avIdList:
            self.treasureScores[avId] = 0

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        self.gameFSM.request('play')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)

        # transitioning to 'cleanup' will cause the distributed
        # treasures to be deleted
        # base class calls this func before sending 'gameAbort' msg
        # NOTE: this doesn't really have the desired effect; the intent
        # was to ensure that the treasures are deleted before the client
        # gets the gameAbort msg, but the DO destroy msgs come from a
        # different server; there's no guarantee of the msg ordering.
        # the right solution is probably to leave the zone after each
        # minigame.
        if self.gameFSM.getCurrentState():
            self.gameFSM.request('cleanup')

        DistributedMinigameAI.setGameAbort(self)

    def gameOver(self):
        self.notify.debug("gameOver")
        # call this when the game is done
        # clean things up in this class
        self.gameFSM.request('cleanup')
        # tell the base class to wrap things up
        DistributedMinigameAI.gameOver(self)

    def enterInactive(self):
        self.notify.debug("enterInactive")

    def exitInactive(self):
        pass

    def enterPlay(self):
        self.notify.debug("enterPlay")

        # Make some poor player IT
        self.b_setIt(random.choice(self.avIdList))

        # Start the game timer
        taskMgr.doMethodLater(self.DURATION,
                              self.timerExpired,
                              self.taskName("gameTimer"))

        # Start spawning treasure
        self.tagTreasurePlanner = TagTreasurePlannerAI(self.zoneId,
                                                       self.treasureGrabCallback)
        # Prime the treasure pump a little
        self.tagTreasurePlanner.placeRandomTreasure()
        self.tagTreasurePlanner.placeRandomTreasure()
        self.tagTreasurePlanner.placeRandomTreasure()
        self.tagTreasurePlanner.placeRandomTreasure()
        # Start the treasure planner up
        self.tagTreasurePlanner.start()

    def timerExpired(self, task):
        # Show's over folks
        self.notify.debug("timer expired")
        self.gameOver()
        return Task.done

    def exitPlay(self):
        taskMgr.remove(self.taskName("gameTimer"))
        taskMgr.remove(self.taskName("tagBack"))
        taskMgr.remove(self.taskName("clearTagBack"))
        # Stop spawning treasure
        self.tagTreasurePlanner.stop()
        self.tagTreasurePlanner.deleteAllTreasuresNow()
        del self.tagTreasurePlanner

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass

    def treasureGrabCallback(self, avId):
        if avId not in self.avIdList:
            self.air.writeServerEvent('suspicious', avId, 'TagGameAI.treasureGrabCallback non-player avId')
            return
        # Add one to this avIds treasure score
        self.treasureScores[avId] += 2
        self.notify.debug("treasureGrabCallback: " + str(avId) +
                            " grabbed a treasure, new score: " +
                            str(self.treasureScores[avId]))

        # Count the treasure towards the real purchasing score
        self.scoreDict[avId] = self.treasureScores[avId]

        # Broadcast the new score to all the clients so they can
        # update their scoreboards
        treasureScoreParams = []
        # we need to make sure the list is in the proper order
        # iterate through avIdList to get correct order
        for avId in self.avIdList:
            treasureScoreParams.append(self.treasureScores[avId])
        self.sendUpdate("setTreasureScore", [treasureScoreParams])

    def clearTagBack(self, task):
        self.tagBack = 1
        return Task.done

    def tag(self, taggedAvId):
        """
        This is a dist update from the client saying he tagged somebody
        """
        taggedAvatar = simbase.air.doId2do.get(taggedAvId)
        if taggedAvatar == None:
            self.air.writeServerEvent('suspicious', taggedAvId, 'TagGameAI.tag invalid taggedAvId')
            return
        
        itAvId = self.air.getAvatarIdFromSender()
        if self.tagBack:
            self.notify.debug("tag: " + str(itAvId) +
                                " tagged: " + str(taggedAvId))
            # double check to see if itAvId was it before
            if (self.itAvId == itAvId):
                self.b_setIt(taggedAvId)
            else:
                self.notify.warning("Got tag message from avatar that is not IT")
                # Hmmm, now what should I do?
                return None
            
            # No tag backs until the doLater is finished
            self.tagBack = 0
            taskMgr.doMethodLater(2.0, self.clearTagBack,
                                  self.taskName("clearTagBack"))

    def b_setIt(self, avId):
        self.d_setIt(avId)
        self.setIt(avId)

    def d_setIt(self, avId):
        self.sendUpdate("setIt", [avId])

    def setIt(self, avId):
        self.itAvId = avId
