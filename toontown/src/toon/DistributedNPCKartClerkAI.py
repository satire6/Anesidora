##########################################################################
# Module: DistributedNPCKartClerkAI.py
#   (Based on Distributed NPCPetclerkAI.py)
# Date: 4/24/05
# Author: shaskell
##########################################################################

from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *
from DistributedNPCToonBaseAI import *
from toontown.toonbase import TTLocalizer
from direct.task import Task     
from toontown.racing.KartShopGlobals import *
from toontown.racing.KartDNA import *

class DistributedNPCKartClerkAI(DistributedNPCToonBaseAI):
    def __init__(self, air, npcId):
        DistributedNPCToonBaseAI.__init__(self, air, npcId)
        # should kart clerks give out quests? not for now...
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

        self.transactionType = ""
        
        av = self.air.doId2do[avId]
        self.busy = avId

        # Handle unexpected exit
        self.acceptOnce(self.air.getAvatarExitEvent(avId),
                        self.__handleUnexpectedExit, extraArgs=[avId])

        #TODO: does this need to change?
        flag = NPCToons.SELL_MOVIE_START
        self.d_setMovie(avId, flag)
        taskMgr.doMethodLater(KartShopGlobals.KARTCLERK_TIMER, self.sendTimeoutMovie, self.uniqueName("clearMovie"))

        DistributedNPCToonBaseAI.avatarEnter(self)

    def rejectAvatar(self, avId):
        self.notify.warning("rejectAvatar: should not be called by a kart clerk!")
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

    def buyKart(self, whichKart):
        assert self.notify.debug('buyKart()')
        avId = self.air.getAvatarIdFromSender()

        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCKartClerkAI.buyKart busy with %s' % (self.busy))
            self.notify.warning("somebody called buyKart that I was not busy with! avId: %s" % avId)
            return    
        av = simbase.air.doId2do.get(avId)
                
        if av:
            movieType = NPCToons.SELL_MOVIE_COMPLETE
            extraArgs = []
            #deduct the tickets from the toon's account
            cost = getKartCost(whichKart)
            if cost == "key error":
                self.air.writeServerEvent('suspicious', avId, 'Player trying to buy non-existant kart %s' % (whichKart))
                self.notify.warning("somebody is trying to buy non-existant kart%s! avId: %s" % (whichKart, avId))
                return
            elif cost > av.getTickets():
                #how is THIS possible?
                self.air.writeServerEvent('suspicious', avId, "DistributedNPCKartClerkAI.buyKart and toon doesn't have enough tickets!")
                self.notify.warning("somebody called buyKart and didn't have enough tickets to purchase! avId: %s" % avId)
                return
            av.b_setTickets(av.getTickets() - cost)
            # Write to the server log
            self.air.writeServerEvent("kartingTicketsSpent", avId, "%s" % (cost))

            av.b_setKartBodyType(whichKart)
            # Write to the server log
            self.air.writeServerEvent("kartingKartPurchased", avId, "%s" % (whichKart))

            # Send a movie to reward the avatar
            #self.d_setMovie(avId, movieType, extraArgs)

        #TODO: do we want this?
        #self.transactionType = "fish"

        else:
            # perhaps the avatar got disconnected
            pass
        #self.sendClearMovie(None)
        
    def buyAccessory(self, whichAcc):
        assert self.notify.debug('buyAccessory()')
            
        avId = self.air.getAvatarIdFromSender()
        av = simbase.air.doId2do.get(avId)
        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCKartClerkAI.buyAccessory busy with %s' % (self.busy))
            self.notify.warning("somebody called buyAccessory that I was not busy with! avId: %s" % avId)
            return
        #check if this toon already has maximum number of accessories
        if len(av.getKartAccessoriesOwned()) >= KartShopGlobals.MAX_KART_ACC:
            #how is THIS possible?
            self.air.writeServerEvent('suspicious', avId, "DistributedNPCKartClerkAI.buyAcc and toon already has max number of accessories!")
            self.notify.warning("somebody called buyAcc and already has maximum allowed accessories! avId: %s" % avId)
            return

            
        av = simbase.air.doId2do.get(avId)
        if av:
            movieType = NPCToons.SELL_MOVIE_COMPLETE
            extraArgs = []
            #deduct the tickets from the toon's account
            cost = getAccCost(whichAcc)
            if cost > av.getTickets():
                #how is THIS possible?
                self.air.writeServerEvent('suspicious', avId, "DistributedNPCKartClerkAI.buyAcc and toon doesn't have enough tickets!")
                self.notify.warning("somebody called buyAcc and didn't have enough tickets to purchase! avId: %s" % avId)
                return
            av.b_setTickets(av.getTickets() - cost)
            # Write to the server log
            self.air.writeServerEvent("kartingTicketsSpent", avId, "%s" % (cost))

            #add this accessory to list of owned accessories
            av.addOwnedAccessory( whichAcc ) 

            # Write to the server log
            self.air.writeServerEvent("kartingAccessoryPurchased", avId, "%s" % (whichAcc))

            #automagically put on this accessory
            av.updateKartDNAField( getAccessoryType(whichAcc), whichAcc)               
 
            # Send a movie to reward the avatar
            #self.d_setMovie(avId, movieType, extraArgs)

        #TODO: do we want this?
        #self.transactionType = "fish"

        else:
            # perhaps the avatar got disconnected
            pass
        #self.sendClearMovie(None)


    #TODO: do we need this?
    def transactionDone(self):
        avId = self.air.getAvatarIdFromSender()

        if self.busy != avId:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCKartClerkAI.transactionDone busy with %s' % (self.busy))
            self.notify.warning("somebody called transactionDone that I was not busy with! avId: %s" % avId)
            return

        av = simbase.air.doId2do.get(avId)
        if av:
        
            # Send a movie to say goodbye
            movieType = NPCToons.SELL_MOVIE_COMPLETE
            extraArgs = []
            self.d_setMovie(avId, movieType, extraArgs)
            #elif self.transactionType == "return":
            #    self.d_setMovie(avId, NPCToons.SELL_MOVIE_PETRETURNED)

            #TODO: movie for kart clerk? we're not exiting with every transaction
            #so do we need more than one?
            #self.d_setMovie(avId, NPCToons.SELL_MOVIE_PETCANCELED)
            

        self.sendClearMovie(None)
        return


    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        taskMgr.remove(self.uniqueName("clearMovie"))
        self.sendClearMovie(None)

