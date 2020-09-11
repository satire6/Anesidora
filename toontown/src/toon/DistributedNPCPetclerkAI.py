from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.toonbase import TTLocalizer
from direct.task import Task
from toontown.fishing import FishGlobals
from toontown.pets import PetUtil, PetDNA, PetConstants

class DistributedNPCPetclerkAI(DistributedNPCToonBaseAI):
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

        self.petSeeds = simbase.air.petMgr.getAvailablePets(3, 2)
        # 'fix' pet seeds so there are two of each (female/male)
        numGenders = len(PetDNA.PetGenders)
        self.petSeeds *= numGenders
        self.petSeeds.sort()
        self.sendUpdateToAvatarId(avId, "setPetSeeds", [self.petSeeds])

        self.transactionType = ""
        
        av = self.air.doId2do[avId]
        self.busy = avId

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])

        # If you have some fish, let the client popup a gui to sell them
        flag = NPCToons.SELL_MOVIE_START
        self.d_setMovie(avId, flag)
        taskMgr.doMethodLater(PetConstants.PETCLERK_TIMER, self.sendTimeoutMovie, self.uniqueName("clearMovie"))

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

    def fishSold(self):
        assert self.notify.debug('fishSold()')
        avId = self.air.getAvatarIdFromSender()

        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCPetshopAI.fishSold busy with %s' % (self.busy))
            self.notify.warning("somebody called fishSold that I was not busy with! avId: %s" % avId)
            return
            
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
            self.transactionType = "fish"
        else:
            # perhaps the avatar got disconnected, just leave the fish
            # in his tank and let him resell them next time
            pass
        self.sendClearMovie(None)

    def petAdopted(self, petNum, nameIndex):
        assert self.notify.debug('petAdopted()')
        avId = self.air.getAvatarIdFromSender()

        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCPetshopAI.petAdopted busy with %s' % (self.busy))
            self.notify.warning("somebody called petAdopted that I was not busy with! avId: %s" % avId)
            return

        av = simbase.air.doId2do.get(avId)
        if av:
            from toontown.hood import ZoneUtil
            zoneId = ZoneUtil.getCanonicalSafeZoneId(self.zoneId)
            # make sure this isn't a suspicious request
            if not petNum in range(0, len(self.petSeeds)):
                # hacker?
                self.air.writeServerEvent('suspicious', avId, "DistributedNPCPetshopAI.petAdopted and no such pet!")
                self.notify.warning("somebody called petAdopted on a non-existent pet! avId: %s" % avId)
                return
            cost = PetUtil.getPetCostFromSeed(self.petSeeds[petNum], zoneId)
            if cost > av.getTotalMoney():
                #houston, we have a problem
                self.air.writeServerEvent('suspicious', avId, "DistributedNPCPetshopAI.petAdopted and toon doesn't have enough money!")
                self.notify.warning("somebody called petAdopted and didn't have enough money to adopt! avId: %s" % avId)
                return

            if av.petId != 0:
                # this function deletes the pet
                simbase.air.petMgr.deleteToonsPet(avId)

            #create new pet
            gender = petNum % len(PetDNA.PetGenders)
            simbase.air.petMgr.createNewPetFromSeed(avId, self.petSeeds[petNum], nameIndex = nameIndex, gender = gender, safeZoneId = zoneId)
            self.transactionType = "adopt"

            #deduct the money from the toon's account
            bankPrice = min(av.getBankMoney(), cost)
            walletPrice = cost - bankPrice
            av.b_setBankMoney(av.getBankMoney() - bankPrice)
            av.b_setMoney(av.getMoney() - walletPrice)
        else:
            # perhaps the avatar got disconnected, just leave the fish
            # in his tank and let him resell them next time
            pass

    def petReturned(self):
        assert self.notify.debug('petReturned()')
        avId = self.air.getAvatarIdFromSender()

        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCPetshopAI.petReturned busy with %s' % (self.busy))
            self.notify.warning("somebody called petReturned that I was not busy with! avId: %s" % avId)
            return
            
        av = simbase.air.doId2do.get(avId)
        if av:
            # this function deletes the pet
            simbase.air.petMgr.deleteToonsPet(avId)
            self.transactionType = "return"
        else:
            # perhaps the avatar got disconnected, just leave the fish
            # in his tank and let him resell them next time
            pass

    def transactionDone(self):
        avId = self.air.getAvatarIdFromSender()

        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCPetshopAI.transactionDone busy with %s' % (self.busy))
            self.notify.warning("somebody called transactionDone that I was not busy with! avId: %s" % avId)
            return

        av = simbase.air.doId2do.get(avId)
        if av:
            # Send a movie to say goodbye
            if self.transactionType == "adopt":
                self.d_setMovie(avId, NPCToons.SELL_MOVIE_PETADOPTED)
            elif self.transactionType == "return":
                self.d_setMovie(avId, NPCToons.SELL_MOVIE_PETRETURNED)
            elif self.transactionType == "":
                self.d_setMovie(avId, NPCToons.SELL_MOVIE_PETCANCELED)

        self.sendClearMovie(None)
        return

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        taskMgr.remove(self.uniqueName("clearMovie"))
        self.sendClearMovie(None)

