from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from otp.ai.Barrier import Barrier

class SadCallbackToken:
    pass

class DistCogdoGameAI(DistributedObjectAI):
    notify = directNotify.newCategory("DistCogdoGameAI")

    MaxPlayers = 4

    def __init__(self, air, interior):
        DistributedObjectAI.__init__(self, air)
        self._interior = interior

        self.loadFSM = ClassicFSM.ClassicFSM(
            'DistCogdoGameAI.loaded',
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
            'DistCogdoGameAI',
            [State.State('Intro',
                         self.enterIntro,
                         self.exitIntro,
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

    def generate(self):
        DistributedObjectAI.generate(self)
        self._sadToken2callback = {}
        self._interior.addGameFSM(self.fsm)

    def getInteriorId(self):
        return self._interior.doId

    def getToonIds(self):
        toonIds = []
        for toonId in self._interior.getToons()[0]:
            if toonId:
                toonIds.append(toonId)
        return toonIds

    def getNumPlayers(self):
        return len(self.getToonIds())

    def requestDelete(self):
        self.fsm.requestFinalState()
        self.loadFSM.requestFinalState()
        self._sadToken2callback = None
        DistributedObjectAI.requestDelete(self)

    def delete(self):
        self._interior.removeGameFSM(self.fsm)
        self._interior = None
        self.fsm = None
        self.loadFSM = None
        DistributedObjectAI.delete(self)

    def start(self):
        self.loadFSM.enterInitialState()
        self.fsm.enterInitialState()

        self.loadFSM.request('Loaded')
        self.fsm.request('Intro')

    def markStartTime(self):
        self._startTime = globalClock.getRealTime()

    def getStartTime(self):
        return self._startTime

    def markFinishTime(self):
        self._finishTime = globalClock.getRealTime()

    def getFinishTime(self):
        return self._finishTime

    ########################

    # game class must override these methods if anything needs to be done when a toon
    # leaves the game. game class should call down

    def handleToonDisconnected(self, toonId):
        self.notify.debug('handleToonDisconnected: %s' % toonId)

    def handleToonWentSad(self, toonId):
        self.notify.debug('handleToonWentSad: %s' % toonId)
        callbacks = self._sadToken2callback.values()
        for callback in callbacks:
            callback(toonId)

    ########################

    # use these methods to get notification when a toon goes sad
    def _registerSadCallback(self, callback):
        token = SadCallbackToken()
        self._sadToken2callback[token] = callback
        return token

    def _unregisterSadCallback(self, token):
        self._sadToken2callback.pop(token)


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

    def enterSetup(self):
        pass
    def exitSetup(self):
        pass

    def enterIntro(self):
        self.sendUpdate('setIntroStart', [])
        self._introBarrier = Barrier('intro', uniqueName('intro'), self.getToonIds(), 1<<20,
                                     doneFunc=self._handleIntroBarrierDone)
        self._sadToken = self._registerSadCallback(self._handleSadToonDuringIntro)
    def exitIntro(self):
        self._unregisterSadCallback(self._sadToken)
        self._sadToken = None
        self._introBarrier.cleanup()
        self._introBarrier = None

    def _handleSadToonDuringIntro(self, toonId):
        # shouldn't be possible unless someone hacks their client or we add some
        # sort of DOT
        self._introBarrier.clear(toonId)

    def setAvatarReady(self):
        senderId = self.air.getAvatarIdFromSender()
        if senderId not in self.getToonIds():
            self.air.writeServerEvent('suspicious', senderId, 'CogdoGameAI.setAvatarReady: unknown avatar')
            return
        if self._introBarrier:
            self._introBarrier.clear(senderId)

    def _handleIntroBarrierDone(self, avIds):
        self.fsm.request('Game')

    def enterGame(self):
        self.markStartTime()
        self.sendUpdate('setGameStart', [
            globalClockDelta.localToNetworkTime(self.getStartTime())])
    def exitGame(self):
        pass

    def _handleGameFinished(self):
        # call this from subclass when Game state is completed
        self.fsm.request('Finish')
        
    def enterFinish(self):
        self.markFinishTime()
        self.sendUpdate('setGameFinish', [
            globalClockDelta.localToNetworkTime(self.getFinishTime())])
    def exitFinish(self):
        pass

    def announceGameDone(self):
        # call this from subclass when Finish state is completed
        self._interior._gameDone()
