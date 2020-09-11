from pandac.PandaModules import VBase4
from direct.gui.DirectGui import DirectLabel
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm import ClassicFSM, State
from toontown.minigame.MinigameRulesPanel import MinigameRulesPanel
from toontown.toonbase import TTLocalizer as TTL

class DistCogdoGame(DistributedObject):
    notify = directNotify.newCategory("DistCogdoGame")

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self._waitingStartLabel = DirectLabel(
            text = TTL.MinigameWaitingForOtherPlayers,
            text_fg = VBase4(1,1,1,1),
            relief = None,
            pos = (-0.6, 0, -0.75),
            scale = 0.075)   
        self._waitingStartLabel.hide()

        self.loadFSM = ClassicFSM.ClassicFSM(
            'DistCogdoGame.loaded',
            [State.State('NotLoaded',
                         self.enterNotLoaded,
                         self.exitNotLoaded,
                         ['Loaded']),
             State.State('Loaded',
                         self.enterLoaded,
                         self.exitLoaded,
                         ['NotLoaded'])],
            # Initial state
            'NotLoaded',
            # Final state
            'NotLoaded')

        self.fsm = ClassicFSM.ClassicFSM(
            'DistCogdoGame',
            [State.State('Intro',
                         self.enterIntro,
                         self.exitIntro,
                         ['WaitServerStart']),
             State.State('WaitServerStart',
                         self.enterWaitServerStart,
                         self.exitWaitServerStart,
                         ['Game']),
             State.State('Game',
                         self.enterGame,
                         self.exitGame,
                         ['Finish']),
             State.State('Finish',
                         self.enterFinish,
                         self.exitFinish,
                         ['Off']),
             State.State('Off',
                         self.enterOff,
                         self.exitOff,
                         ['Intro'])],
            # Initial state
            'Off',
            # Final state
            'Off')
        self.fsm.enterInitialState()

    def getTitle(self):
        pass # override and return title

    def getInstructions(self):
        pass # override and return instructions

    def setInteriorId(self, interiorId):
        self._interiorId = interiorId

    def getInterior(self):
        return self.cr.getDo(self._interiorId)

    def getToonIds(self):
        toonIds = []
        interior = self.getInterior()
        for toonId in interior.getToons()[0]:
            if toonId:
                toonIds.append(toonId)
        return toonIds

    def getNumPlayers(self):
        return len(self.getToonIds())

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.loadFSM.request('Loaded')

    def disable(self):
        self.fsm.requestFinalState()
        self.loadFSM.requestFinalState()
        self.fsm = None
        self.loadFSM = None
        DistributedObject.disable(self)

    def delete(self):
        self._waitingStartLabel.destroy()
        self._waitingStartLabel = None
        DistributedObject.delete(self)


    def enterNotLoaded(self):
        pass
    def exitNotLoaded(self):
        pass

    def enterLoaded(self):
        pass
    def exitLoaded(self):
        pass


    def enterOff(self):
        pass
    def exitOff(self):
        pass

    def setIntroStart(self):
        self.fsm.request('Intro')

    def enterIntro(self):
        assert self.notify.debugCall()
        base.cr.playGame.getPlace().fsm.request('Game')
        self._rulesDoneEvent = uniqueName('cogdoGameRulesDone')
        self.accept(self._rulesDoneEvent, self._handleRulesDone)
        self._rulesPanel = MinigameRulesPanel(
            "MinigameRulesPanel",
            self.getTitle(),
            self.getInstructions(),
            self._rulesDoneEvent)
        self._rulesPanel.load()
        self._rulesPanel.enter()

    def exitIntro(self):
        self.ignore(self._rulesDoneEvent)
        if self._rulesPanel:
            self._rulesPanel.exit()
            self._rulesPanel.unload()
            self._rulesPanel = None

    def _handleRulesDone(self):
        self.ignore(self._rulesDoneEvent)
        self._rulesPanel.exit()
        self._rulesPanel.unload()
        self._rulesPanel = None
        self.sendUpdate('setAvatarReady', [])
        self.fsm.request('WaitServerStart')

    def enterWaitServerStart(self):
        numToons = 1
        interior = self.getInterior()
        if interior:
            numToons = len(interior.getToonIds())
        if numToons > 1:
            msg = TTL.MinigameWaitingForOtherPlayers
        else:
            msg = TTL.MinigamePleaseWait
        self._waitingStartLabel['text'] = msg
        self._waitingStartLabel.show()
    def exitWaitServerStart(self):
        self._waitingStartLabel.hide()

    def setGameStart(self, timestamp):
        self._startTime = globalClockDelta.networkToLocalTime(timestamp)
        self.fsm.request('Game')

    def getStartTime(self):
        return self._startTime

    def enterGame(self):
        assert self.notify.debugCall()
    def exitGame(self):
        pass

    def setGameFinish(self, timestamp):
        self._finishTime = globalClockDelta.networkToLocalTime(timestamp)
        self.fsm.request('Finish')

    def getFinishTime(self):
        return self._finishTime

    def enterFinish(self):
        assert self.notify.debugCall()
    def exitFinish(self):
        pass
