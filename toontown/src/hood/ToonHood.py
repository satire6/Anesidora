
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.distributed.ToontownMsgTypes import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.minigame import Purchase
from otp.avatar import DistributedAvatar
import Hood
from toontown.building import SuitInterior
from toontown.cogdominium import CogdoInterior

class ToonHood(Hood.Hood):
    """
    The base class for toon neighborhoods
    Every neighborhood should have a ToonHood subclass to implement
    neighborhood specific things like fog

    To subclass from hood, you need to define a Town, a SafeZone, a storage
    DNA file, a sky model file, and an id.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory("ToonHood")

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        assert(self.notify.debug("__init__(parentFSM="+str(parentFSM)
                +", doneEvent="+str(doneEvent)
                +", dnaStore="+str(dnaStore)+")"))
        Hood.Hood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)

        # The event for suitInterior done
        self.suitInteriorDoneEvent = "suitInteriorDone"
        # The event for minigame done
        self.minigameDoneEvent = "minigameDone"
        self.safeZoneLoaderClass = None
        self.townLoaderClass = None

        self.fsm = ClassicFSM.ClassicFSM('Hood',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['townLoader', 'safeZoneLoader']),
                            State.State('townLoader',
                                        self.enterTownLoader,
                                        self.exitTownLoader,
                                        ['quietZone',
                                         'safeZoneLoader', 'suitInterior', 'cogdoInterior']),
                            State.State('safeZoneLoader',
                                        self.enterSafeZoneLoader,
                                        self.exitSafeZoneLoader,
                                        ['quietZone',
                                         'suitInterior', 'cogdoInterior', 'townLoader', 
                                         'minigame',
                                         #'tutorial',
                                         ]),
                            State.State('purchase',
                                        self.enterPurchase,
                                        self.exitPurchase,
                                        ['quietZone',
                                         'minigame', 'safeZoneLoader']),
                            State.State('suitInterior',
                                        self.enterSuitInterior,
                                        self.exitSuitInterior,
                                        ['quietZone',
                                        'townLoader', 'safeZoneLoader']),
                            State.State('cogdoInterior',
                                        self.enterCogdoInterior,
                                        self.exitCogdoInterior,
                                        ['quietZone',
                                        'townLoader', 'safeZoneLoader']),
                            State.State('minigame',
                                        self.enterMinigame,
                                        self.exitMinigame,
                                        ['purchase']),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['safeZoneLoader', 'townLoader', 
                                        'suitInterior', 'cogdoInterior', 'minigame']),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        [])
                            ],
                           'start',
                           'final',
                           )
        self.fsm.enterInitialState()
        
    def load(self):
        Hood.Hood.load(self)

    def unload(self):
        del self.safeZoneLoaderClass
        del self.townLoaderClass
        Hood.Hood.unload(self)

    def loadLoader(self, requestStatus):
        assert(self.notify.debug("loadLoader(requestStatus="
                                 +str(requestStatus)+")"))
        loaderName = requestStatus["loader"]
        if loaderName=="safeZoneLoader":
            self.loader = self.safeZoneLoaderClass(self, 
                    self.fsm.getStateNamed("safeZoneLoader"), 
                    self.loaderDoneEvent)
            self.loader.load()
        elif loaderName=="townLoader":
            self.loader = self.townLoaderClass(self, 
                    self.fsm.getStateNamed("townLoader"), 
                    self.loaderDoneEvent)
            self.loader.load(requestStatus["zoneId"])
        else:
            assert(self.notify.debug("  unknown loaderName: "+str(loaderName)))

    # TownLoader state
    
    def enterTownLoader(self, requestStatus):
        """enterTownLoader(self)
        """
        assert(self.notify.debug("enterTownLoader(requestStatus="+str(requestStatus)+")"))
        self.accept(self.loaderDoneEvent, self.handleTownLoaderDone)
        self.loader.enter(requestStatus)
        self.spawnTitleText(requestStatus['zoneId'])

    def exitTownLoader(self):
        """exitTownLoader(self)
        """
        assert(self.notify.debug("exitTownLoader()"))
        taskMgr.remove("titleText")
        self.hideTitleText()
        self.ignore(self.loaderDoneEvent)
        self.loader.exit()
        self.loader.unload()
        del self.loader        

    def handleTownLoaderDone(self):
        """
        We will get this callback when the town state data throws
        its done event. Now we have to figure out why we exited from
        the town. This is done by querying the TownLoader StateData done status.
        """
        assert(self.notify.debug("handleTownLoaderDone()"))
        doneStatus = self.loader.getDoneStatus()
        if self.isSameHood(doneStatus):
            self.fsm.request("quietZone", [doneStatus])
        else:
            # ...we're leaving the hood.
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)

    # Purchase state

    def enterPurchase(self, pointsAwarded, playerMoney, playerIds, playerStates, remain, metagameRound=-1, votesArray=None):
        """enterPurchase(self, pointsAwarded)
        """
        assert(self.notify.debug("enterPurchase()"))
        # Healing should take place during purchasing, so tell the
        # safezone manager we are in a safezone.
        messenger.send("enterSafeZone")
        # Turn off laff numbers
        DistributedAvatar.DistributedAvatar.HpTextEnabled = 0
        # Turn on laff meter
        base.localAvatar.laffMeter.start()

        # this should be a set via a query to the minigame
        self.purchaseDoneEvent = "purchaseDone"
        self.accept(self.purchaseDoneEvent, self.handlePurchaseDone)
        self.purchase = Purchase.Purchase(base.localAvatar,
                pointsAwarded, playerMoney, playerIds, playerStates, remain,
                self.purchaseDoneEvent, metagameRound, votesArray)

        self.purchase.load()
        self.purchase.enter()

    def exitPurchase(self):
        """exitPurchase(self)
        """
        assert(self.notify.debug("exitPurchase()"))
        # No more healing when you leave, please.
        messenger.send("exitSafeZone")
        # Turn laff numbers back on
        DistributedAvatar.DistributedAvatar.HpTextEnabled = 1
        # Turn off laff meter
        base.localAvatar.laffMeter.stop()        
        
        self.ignore(self.purchaseDoneEvent)
        self.purchase.exit()
        self.purchase.unload()
        del self.purchase

    def handlePurchaseDone(self):
        assert(self.notify.debug("handlePurchaseDone()"))
        doneStatus = self.purchase.getDoneStatus()
        if (doneStatus["where"] == "playground"):
            self.fsm.request("quietZone",
                             [{"loader": "safeZoneLoader",
                               "where":  "playground",
                               "how":    "teleportIn",
                               "hoodId": self.hoodId,
                               "zoneId": self.hoodId,
                               "shardId": None,
                               "avId":   -1}])
        elif (doneStatus["loader"] == "minigame"):
            self.fsm.request("minigame")
        else:
            self.notify.error("handlePurchaseDone: unknown mode")

    # suitInterior state

    def enterSuitInterior(self, requestStatus=None):
        """enterSuitInterior(self)
        """
        assert(self.notify.debug("enterSuitInterior"))
        self.placeDoneEvent = 'suit-interior-done'
        self.acceptOnce(self.placeDoneEvent, self.handleSuitInteriorDone)
        self.place = SuitInterior.SuitInterior(self, self.fsm, 
                                                        self.placeDoneEvent)
        self.place.load()
        self.place.enter(requestStatus)
        base.cr.playGame.setPlace(self.place)
        
    def exitSuitInterior(self):
        """exitSuitInterior(self)
        """
        assert(self.notify.debug("exitSuitInterior()"))
        self.ignore(self.placeDoneEvent)
        del self.placeDoneEvent
        self.place.exit()
        self.place.unload()
        self.place=None
        base.cr.playGame.setPlace(self.place)
    
    def handleSuitInteriorDone(self):
        assert(self.notify.debug("handleSuitInteriorDone()"))
        doneStatus = self.place.getDoneStatus()
        if self.isSameHood(doneStatus):
            self.fsm.request("quietZone", [doneStatus])
        else:
            # ...we're leaving the hood.
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)

    # cogdoInterior state

    def enterCogdoInterior(self, requestStatus=None):
        """enterCogdoInterior(self)
        """
        assert(self.notify.debug("enterCogdoInterior"))
        self.placeDoneEvent = 'cogdo-interior-done'
        self.acceptOnce(self.placeDoneEvent, self.handleCogdoInteriorDone)
        self.place = CogdoInterior.CogdoInterior(self, self.fsm, 
                                                        self.placeDoneEvent)
        self.place.load()
        self.place.enter(requestStatus)
        base.cr.playGame.setPlace(self.place)
        
    def exitCogdoInterior(self):
        """exitCogdoInterior(self)
        """
        assert(self.notify.debug("exitCogdoInterior()"))
        self.ignore(self.placeDoneEvent)
        del self.placeDoneEvent
        self.place.exit()
        self.place.unload()
        self.place=None
        base.cr.playGame.setPlace(self.place)
    
    def handleCogdoInteriorDone(self):
        assert(self.notify.debug("handleCogdoInteriorDone()"))
        doneStatus = self.place.getDoneStatus()
        if self.isSameHood(doneStatus):
            self.fsm.request("quietZone", [doneStatus])
        else:
            # ...we're leaving the hood.
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)

    # Minigame state

    def enterMinigame(self, ignoredParameter=None):
        """enterMinigame(self)
        This state is just a puppet state while the DistributedMinigame
        actually does all the work. The DistributedMinigame will actually
        make his state machine a child of this state.
        """
        # Healing should take place during minigames, so tell the
        # safezone manager we are in a safezone.
        messenger.send("enterSafeZone")
        # Turn off laff numbers
        DistributedAvatar.DistributedAvatar.HpTextEnabled = 0
        # Turn on laff meter
        base.localAvatar.laffMeter.start()
        # Cheesy rendering effects are not allowed in minigames.
        base.cr.forbidCheesyEffects(1)
        
        # Wait for the real minigame to say it is done
        self.acceptOnce(self.minigameDoneEvent, self.handleMinigameDone)
        return None

    def exitMinigame(self):
        """exitMinigame(self)
        """
        # Exit minigame, exit healing zone.
        messenger.send("exitSafeZone")
        # Turn laff numbers back on
        DistributedAvatar.DistributedAvatar.HpTextEnabled = 1
        # Turn off laff meter
        base.localAvatar.laffMeter.stop()
        # Restore cheesy rendering effects.
        base.cr.forbidCheesyEffects(0)
        
        self.ignore(self.minigameDoneEvent)
        # Remove the minigame child state machine if it has not been already
        minigameState = self.fsm.getStateNamed("minigame")
        for childFSM in minigameState.getChildren():
            minigameState.removeChild(childFSM)

    def handleMinigameDone(self):
        """
        Ok, games are over, time to shop
        """
        # PurchaseManager will make the transition. Minigame can just sit
        # here peacefully.
        return None

    # final state
    # Defined in Hood.py

    # quietZone state
    # Defined in Hood.py

