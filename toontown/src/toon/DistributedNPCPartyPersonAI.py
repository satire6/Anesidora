#-------------------------------------------------------------------------------
# Contact: Shawn Patton
# Created: Sep 2008
#
# Purpose: AI side of a party person, an NPC who stands near the party hat
#          and can send you to the party grounds to plan your party
#-------------------------------------------------------------------------------

from DistributedNPCToonBaseAI import DistributedNPCToonBaseAI
from toontown.toonbase import TTLocalizer
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from toontown.toon import NPCToons
from direct.distributed import ClockDelta
from toontown.parties import PartyGlobals

class DistributedNPCPartyPersonAI(DistributedNPCToonBaseAI):
    def __init__(self, air, npcId):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)
        # Party planners are not in the business of giving out quests
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
        
        if not self.air.doId2do.has_key(avId):
            self.notify.warning("Avatar: %s not found" % (avId))
            return

        if self.isBusy():
            self.freeAvatar(avId)
            return

        av = self.air.doId2do[avId]
        self.busy = avId

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])

        parties = av.hostedParties
        if not self.air.partyManager.canBuyParties():
            # people can't buy parties yet
            flag = NPCToons.PARTY_MOVIE_COMINGSOON
            self.d_setMovie(avId, flag)
            # Immediately send the clear movie - we are done with this Toon
            self.sendClearMovie(None)
        elif av.getTotalMoney() < PartyGlobals.MinimumPartyCost:
            flag = NPCToons.PARTY_MOVIE_MINCOST
            self.d_setMovie(avId, flag)
            # Immediately send the clear movie - we are done with this Toon
            self.sendClearMovie(None)            
        elif av.canPlanParty():
            # If you're not planning a party, maybe you want to?  Ask them!
            flag = NPCToons.PARTY_MOVIE_START
            self.d_setMovie(avId, flag)
            taskMgr.doMethodLater(30.0, self.sendTimeoutMovie, self.uniqueName("clearMovie"))
        else:
            # If you have a party planned already, you can't plan another
            flag = NPCToons.PARTY_MOVIE_ALREADYHOSTING
            self.d_setMovie(avId, flag)
            # Immediately send the clear movie - we are done with this Toon
            self.sendClearMovie(None)

        DistributedNPCToonBaseAI.avatarEnter(self)

    def rejectAvatar(self, avId):
        self.notify.warning("rejectAvatar: should not be called by a party person!")
        return

    def d_setMovie(self, avId, flag, extraArgs=[]):
        # tell the client what to do
        self.sendUpdate("setMovie", [flag, self.npcId, avId, extraArgs, ClockDelta.globalClockDelta.getRealNetworkTime()])
        
    def sendTimeoutMovie(self, task):
        assert self.notify.debug('sendTimeoutMovie()')
        # The timeout has expired.
        self.d_setMovie(self.busy, NPCToons.PARTY_MOVIE_TIMEOUT)
        self.sendClearMovie(None)
        return Task.done

    def sendClearMovie(self, task):
        assert self.notify.debug('sendClearMovie()')
        # Ignore unexpected exits on whoever I was busy with
        self.ignore(self.air.getAvatarExitEvent(self.busy))
        taskMgr.remove(self.uniqueName("clearMovie"))
        self.busy = 0
        self.d_setMovie(0, NPCToons.PARTY_MOVIE_CLEAR)
        return Task.done

    def answer(self, wantsToPlan):
        assert self.notify.debug('answer()')
        avId = self.air.getAvatarIdFromSender()

        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCPartyPersonAI.answer busy with %s' % (self.busy))
            self.notify.warning("somebody called setMovieDone that I was not busy with! avId: %s" % avId)
            return
            
        if wantsToPlan:
            av = simbase.air.doId2do.get(avId)
            if av:
                if av.getGameAccess() != ToontownGlobals.AccessFull:
                    # It can only come here if the client is hacked.
                    self.air.writeServerEvent('suspicious', avId, 'DistributedNPCPartyPersonAI.free player tried to host party.')
                    # If you are a trialer you can't buy a party
                    flag = NPCToons.PARTY_MOVIE_ONLYPAID
                    self.d_setMovie(avId, flag)
                else:
                    # this function sends the toon to the party grounds to start planning!
                    zoneId = self.air.allocateZone()
                    # hoodId determines the loader that gets used
                    hoodId = ToontownGlobals.PartyHood
                    # Send a movie to reward the avatar
                    self.d_setMovie(avId, NPCToons.PARTY_MOVIE_COMPLETE, [hoodId, zoneId])
            else:
                # perhaps the avatar got disconnected, just ignore him...
                pass
        else:
            av = simbase.air.doId2do.get(avId)
            if av:
                # Send a movie to say goodbye
                self.d_setMovie(avId, NPCToons.PARTY_MOVIE_MAYBENEXTTIME)
        self.sendClearMovie(None)
        return

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        taskMgr.remove(self.uniqueName("clearMovie"))
        self.sendClearMovie(None)

