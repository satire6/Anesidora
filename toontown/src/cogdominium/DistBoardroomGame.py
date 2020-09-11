from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.cogdominium.DistCogdoGame import DistCogdoGame
from toontown.toonbase import ToontownTimer
from toontown.toonbase import TTLocalizer as TTL

class DistBoardroomGame(DistCogdoGame):
    notify = directNotify.newCategory("DistBoardroomGame")

    def __init__(self, cr):
        DistCogdoGame.__init__(self, cr)

    def getTitle(self):
        return TTL.BoardroomGameTitle

    def getInstructions(self):
        return TTL.BoardroomGameInstructions

    def announceGenerate(self):
        DistCogdoGame.announceGenerate(self)
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.stash()

    def disable(self):
        self.timer.destroy()
        self.timer = None
        DistCogdoGame.disable(self)
        
    def enterGame(self):
        DistCogdoGame.enterGame(self)
        #self.timer.posInTopRightCorner()
        timeLeft = 15. - (globalClock.getRealTime() - self.getStartTime())
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    def enterFinish(self):
        DistCogdoGame.enterFinish(self)
        timeLeft = 10 - (globalClock.getRealTime() - self.getFinishTime())
        self.timer.setTime(timeLeft)
        self.timer.countdown(timeLeft, self.timerExpired)
        self.timer.unstash()

    def timerExpired(self):
        pass
