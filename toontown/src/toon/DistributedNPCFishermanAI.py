
from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.fishing import FishGlobals
from toontown.toonbase import TTLocalizer
from toontown.fishing import FishGlobals
from direct.task import Task

class DistributedNPCFishermanAI(DistributedNPCToonBaseAI):
    def __init__(self, air, npcId):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)
        # Fishermen are not in the business of giving out quests
        self.givesQuests = 0
        self.busy = 0
        
    def delete(self):
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.ignoreAll()
        DistributedNPCToonBaseAI.delete(self)

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        # this avatar has come within range
        assert self.notify.debug("avatar enter " + str(avId))
        
        if (not self.air.doId2do.has_key(avId)):
            self.notify.warning("Avatar: %s not found" % (avId))
            return

        if (self.isBusy()):
            self.freeAvatar(avId)
            return

        av = self.air.doId2do[avId]
        self.busy = avId

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])

        value = av.fishTank.getTotalValue()
        if value > 0:
            # If you have some fish, let the client popup a gui to sell them
            flag = NPCToons.SELL_MOVIE_START
            self.d_setMovie(avId, flag)
            taskMgr.doMethodLater(30.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        else:
            # If you have no fish, send this instructional movie
            flag = NPCToons.SELL_MOVIE_NOFISH
            self.d_setMovie(avId, flag)
            # Immediately send the clear movie - we are done with this Toon
            self.sendClearMovie(None)        
        DistributedNPCToonBaseAI.avatarEnter(self)

    def rejectAvatar(self, avId):
        self.notify.warning("rejectAvatar: should not be called by a fisherman!")
        return

    def d_setMovie(self, avId, flag, extraArgs=[]):
        # tell the client to popup it's sell/adopt interface
        self.sendUpdate("setMovie",
                        [flag,
                         self.npcId, avId, extraArgs,
                         ClockDelta.globalClockDelta.getRealNetworkTime()])
        
    def sendTimeoutMovie(self, task):
        assert self.notify.debug('sendTimeoutMovie()')
        # The timeout has expired.
        self.d_setMovie(self.busy, NPCToons.SELL_MOVIE_TIMEOUT)
        self.sendClearMovie(None)
        return Task.done

    def sendClearMovie(self, task):
        assert self.notify.debug('sendClearMovie()')
        # Ignore unexpected exits on whoever I was busy with
        self.ignore(self.air.getAvatarExitEvent(self.busy))
        taskMgr.remove(self.uniqueName("clearMovie"))
        self.busy = 0
        self.d_setMovie(0, NPCToons.SELL_MOVIE_CLEAR)
        return Task.done

    def completeSale(self, sell):
        assert self.notify.debug('completeSale()')
        avId = self.air.getAvatarIdFromSender()

        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCFishermanAI.completeSale busy with %s' % (self.busy))
            self.notify.warning("somebody called setMovieDone that I was not busy with! avId: %s" % avId)
            return
            
        if sell:
            av = simbase.air.doId2do.get(avId)
            if av:
                # this function sells the fish, clears the tank, and
                # updates the collection, trophies, and maxhp. One stop shopping!
                trophyResult = self.air.fishManager.creditFishTank(av)
                
                if trophyResult:
                    movieType = NPCToons.SELL_MOVIE_TROPHY
                    extraArgs = [len(av.fishCollection), FishGlobals.getTotalNumFish()]
                else:
                    movieType = NPCToons.SELL_MOVIE_COMPLETE
                    extraArgs = []

                # Send a movie to reward the avatar
                self.d_setMovie(avId, movieType, extraArgs)
            else:
                # perhaps the avatar got disconnected, just leave the fish
                # in his tank and let him resell them next time
                pass
        else:
            av = simbase.air.doId2do.get(avId)
            if av:
                # Send a movie to say goodbye
                self.d_setMovie(avId, NPCToons.SELL_MOVIE_NOFISH)
        self.sendClearMovie(None)
        return

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        taskMgr.remove(self.uniqueName("clearMovie"))
        self.sendClearMovie(None)

