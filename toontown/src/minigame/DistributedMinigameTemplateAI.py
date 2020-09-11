"""DistributedMinigameTemplateAI module: contains the DistributedMinigameTemplateAI class"""

from DistributedMinigameAI import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State

class DistributedMinigameTemplateAI(DistributedMinigameAI):

    def __init__(self, air, minigameId):
        try:
            self.DistributedMinigameTemplateAI_initialized
        except:
            self.DistributedMinigameTemplateAI_initialized = 1
            DistributedMinigameAI.__init__(self, air, minigameId)

            self.gameFSM = ClassicFSM.ClassicFSM('DistributedMinigameTemplateAI',
                                   [
                                    State.State('inactive',
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

    def generate(self):
        self.notify.debug("generate")
        DistributedMinigameAI.generate(self)

    # Disable is never called on the AI so we do not define one

    def delete(self):
        self.notify.debug("delete")
        del self.gameFSM
        DistributedMinigameAI.delete(self)

    # override some network message handlers
    def setGameReady(self):
        self.notify.debug("setGameReady")
        DistributedMinigameAI.setGameReady(self)
        # all of the players have checked in
        # they will now be shown the rules

    def setGameStart(self, timestamp):
        self.notify.debug("setGameStart")
        # base class will cause gameFSM to enter initial state
        DistributedMinigameAI.setGameStart(self, timestamp)
        # all of the players are ready to start playing the game
        # transition to the appropriate ClassicFSM state
        self.gameFSM.request('play')

    def setGameAbort(self):
        self.notify.debug("setGameAbort")
        # this is called when the minigame is unexpectedly
        # ended (a player got disconnected, etc.)
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

        # when the game is done, call gameOver()
        self.gameOver()

    def exitPlay(self):
        pass

    def enterCleanup(self):
        self.notify.debug("enterCleanup")
        self.gameFSM.request('inactive')

    def exitCleanup(self):
        pass
