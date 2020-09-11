"""
PlayGame module: contains the PlayGame class
"""

from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task.Task import Task
from ToontownMsgTypes import *
from toontown.toonbase import ToontownGlobals
from toontown.hood import TTHood
from toontown.hood import DDHood
from toontown.hood import MMHood
from toontown.hood import BRHood
from toontown.hood import DGHood
from toontown.hood import DLHood
from toontown.hood import GSHood
from toontown.hood import OZHood
from toontown.hood import GZHood
from toontown.hood import SellbotHQ, CashbotHQ, LawbotHQ, BossbotHQ
from toontown.hood import TutorialHood
from direct.task import TaskManagerGlobal
from toontown.hood import QuietZoneState
from toontown.hood import ZoneUtil
from toontown.hood import EstateHood
from toontown.hood import PartyHood
from toontown.toonbase import TTLocalizer
from toontown.parties.PartyGlobals import GoToPartyStatus

class PlayGame(StateData.StateData):
    """PlayGame class"""

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("PlayGame")

    Hood2ClassDict = {
        ToontownGlobals.ToontownCentral: TTHood.TTHood,
        ToontownGlobals.DonaldsDock: DDHood.DDHood,
        ToontownGlobals.TheBrrrgh: BRHood.BRHood,
        ToontownGlobals.MinniesMelodyland: MMHood.MMHood,
        ToontownGlobals.DaisyGardens: DGHood.DGHood,
        ToontownGlobals.DonaldsDreamland: DLHood.DLHood,
        ToontownGlobals.GoofySpeedway: GSHood.GSHood,
        ToontownGlobals.OutdoorZone: OZHood.OZHood,
        ToontownGlobals.Tutorial: TutorialHood.TutorialHood,
        ToontownGlobals.MyEstate: EstateHood.EstateHood,
        ToontownGlobals.BossbotHQ: BossbotHQ.BossbotHQ, # Not implemented yet
        ToontownGlobals.SellbotHQ: SellbotHQ.SellbotHQ,
        ToontownGlobals.CashbotHQ: CashbotHQ.CashbotHQ, 
        ToontownGlobals.LawbotHQ: LawbotHQ.LawbotHQ,
        ToontownGlobals.GolfZone: GZHood.GZHood,
        ToontownGlobals.PartyHood: PartyHood.PartyHood,
        }

    Hood2StateDict = {
        ToontownGlobals.ToontownCentral: "TTHood",
        ToontownGlobals.DonaldsDock: "DDHood",
        ToontownGlobals.TheBrrrgh: "BRHood",
        ToontownGlobals.MinniesMelodyland: "MMHood",
        ToontownGlobals.DaisyGardens: "DGHood",
        ToontownGlobals.DonaldsDreamland: "DLHood",
        ToontownGlobals.GoofySpeedway: "GSHood",
        ToontownGlobals.OutdoorZone: "OZHood",        
        ToontownGlobals.Tutorial: "TutorialHood",
        ToontownGlobals.MyEstate: "EstateHood",
        ToontownGlobals.BossbotHQ: "BossbotHQ",
        ToontownGlobals.SellbotHQ: "SellbotHQ",
        ToontownGlobals.CashbotHQ: "CashbotHQ",
        ToontownGlobals.LawbotHQ: "LawbotHQ",
        ToontownGlobals.GolfZone: "GZHood",
        ToontownGlobals.PartyHood: "PartyHood",
        }
    
    # special methods

    def __init__(self, parentFSM, doneEvent):
        """__init__(self, ClassicFSM, string)
        PlayGame constructor: create a play game ClassicFSM
        """
        StateData.StateData.__init__(self, doneEvent)
        self.place = None
        self.fsm = ClassicFSM.ClassicFSM('PlayGame',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['quietZone']),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['TTHood', 'DDHood', 
                                         'BRHood', 'MMHood', 
                                         'DGHood', 'DLHood',
                                         'GSHood', 'OZHood',
                                         'GZHood',
                                         'SellbotHQ', 'CashbotHQ', 'LawbotHQ',
                                         'BossbotHQ', 'TutorialHood', 
                                         'EstateHood',
                                         'PartyHood']),
                            State.State('TTHood',
                                        self.enterTTHood,
                                        self.exitTTHood,
                                        ['quietZone']),
                            State.State('DDHood',
                                        self.enterDDHood,
                                        self.exitDDHood,
                                        ['quietZone']),
                            State.State('BRHood',
                                        self.enterBRHood,
                                        self.exitBRHood,
                                        ['quietZone']),
                            State.State('MMHood',
                                        self.enterMMHood,
                                        self.exitMMHood,
                                        ['quietZone']),
                            State.State('DGHood',
                                        self.enterDGHood,
                                        self.exitDGHood,
                                        ['quietZone']),
                            State.State('DLHood',
                                        self.enterDLHood,
                                        self.exitDLHood,
                                        ['quietZone']),
                            State.State('GSHood',
                                        self.enterGSHood,
                                        self.exitGSHood,
                                        ['quietZone']),
                            State.State('OZHood',
                                        self.enterOZHood,
                                        self.exitOZHood,
                                        ['quietZone']),
                            State.State('GZHood',
                                        self.enterGZHood,
                                        self.exitGZHood,
                                        ['quietZone']),
                            State.State('BossbotHQ',
                                        self.enterBossbotHQ,
                                        self.exitBossbotHQ,
                                        ['quietZone']),
                            State.State('SellbotHQ',
                                        self.enterSellbotHQ,
                                        self.exitSellbotHQ,
                                        ['quietZone']),
                            State.State('CashbotHQ',
                                        self.enterCashbotHQ,
                                        self.exitCashbotHQ,
                                        ['quietZone']),
                            State.State('LawbotHQ',
                                        self.enterLawbotHQ,
                                        self.exitLawbotHQ,
                                        ['quietZone']),
                            State.State('TutorialHood',
                                        self.enterTutorialHood,
                                        self.exitTutorialHood,
                                        ['quietZone']),
                            State.State('EstateHood',
                                        self.enterEstateHood,
                                        self.exitEstateHood,
                                        ['quietZone']),
                            State.State('PartyHood',
                                        self.enterPartyHood,
                                        self.exitPartyHood,
                                        ['quietZone']),
                            ],
                           # Initial State
                           'start',
                           # Final State
                           'start',
                           )

        self.fsm.enterInitialState()

        self.parentFSM = parentFSM
        # Add this state machine to the parent fsm playGame state
        self.parentFSM.getStateNamed("playGame").addChild(self.fsm)
        # Create the state datas for each hood
        self.hoodDoneEvent = "hoodDone"
        self.hood = None

    def enter(self, hoodId, zoneId, avId):
        """enter(self)
        You will only get this case if you came from outside this shard
        This means login, or switching shards
        avId is the avatar to teleport to, or -1 to put you at the
        safezone.
        """
        if hoodId == ToontownGlobals.Tutorial:
            loaderName = "townLoader"
            whereName = "toonInterior"
        elif hoodId == ToontownGlobals.MyEstate:
            # we just switched shards.  The zoneId we have right now is the zoneId
            # we will be going to.  But we still need to call
            # getEstateZone on the AI again, so the AI can do it's bookkeeping
            # on the estate.
            self.getEstateZoneAndGoHome(avId, zoneId)
            return
        elif hoodId == ToontownGlobals.PartyHood:
            # We just switched to the Party shard. We need to check if the party
            # exists and create it if necessary through getPartyZoneAndGoToParty:
            self.getPartyZoneAndGoToParty(avId, zoneId)
            return
        else:
            loaderName = ZoneUtil.getLoaderName(zoneId)
            whereName = ZoneUtil.getToonWhereName(zoneId)
            
        
        self.fsm.request("quietZone",
                         [{"loader": loaderName,
                           "where": whereName,
                           "how": "teleportIn",
                           "hoodId": hoodId,
                           "zoneId": zoneId,
                           "shardId": None,
                           "avId": avId}])
        
    def exit(self):
        """exit(self)
        """
        pass
            
    def load(self):
        """load(self)
        """
        pass

    def loadDnaStoreTutorial(self):
        # The tutorial has special storage to separate the phases more optimally
        # Create a DNA Store
        self.dnaStore = DNAStorage()
        # Fill up that DNA Store
        loader.loadDNAFile(self.dnaStore, "phase_3.5/dna/storage_tutorial.dna")
        loader.loadDNAFile(self.dnaStore, "phase_3.5/dna/storage_interior.dna")

    def loadDnaStore(self):
        if not hasattr(self, "dnaStore"):
            # Create a DNA Store
            self.dnaStore = DNAStorage()
            # Fill up that DNA Store
            loader.loadDNAFile(self.dnaStore, "phase_4/dna/storage.dna")

            # We'd rather share the font models where possible, so
            # we'll replace some of the fonts the dna store loaded
            # with the corresponding fonts we already have in memory.
            self.dnaStore.storeFont("humanist", ToontownGlobals.getInterfaceFont())
            self.dnaStore.storeFont("mickey", ToontownGlobals.getSignFont())
            self.dnaStore.storeFont("suit", ToontownGlobals.getSuitFont())
            
            # Also load the interior models
            # Perhaps these should be loaded elsewhere? It is a memory vs load
            # time tradeoff
            loader.loadDNAFile(self.dnaStore, "phase_3.5/dna/storage_interior.dna")

    def unloadDnaStore(self):
        if hasattr(self, "dnaStore"):
            self.dnaStore.resetNodes()
            self.dnaStore.resetTextures()
            del self.dnaStore
            ModelPool.garbageCollect()
            TexturePool.garbageCollect()
        
    def unload(self):
        """unload(self)
        """
        self.unloadDnaStore()

        # The hood should have been cleaned up by the appropriate
        # exit*Hood state transition, but because we actually load
        # these before we enter those states, it's possible we never
        # even got there, so it might still be hanging around.  If so,
        # clean it up now.
        if self.hood:
            self.notify.info("Aggressively cleaning up hood: %s" % (self.hood))
            self.hood.exit()
            self.hood.unload()
            self.hood = None
        

    def enterStart(self):
        """enterStart(self)
        """
        pass
        
    def exitStart(self):
        """exitStart(self)
        """
        pass

    def handleHoodDone(self):
        doneStatus = self.hood.getDoneStatus()
        shardId = doneStatus["shardId"]
        if shardId != None:
            # If we're switching shards, we need to back out one more
            # level.
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
            # blank the screen so we don't see distributed objects
            # with no ground
            base.transitions.fadeOut(0)
            return
        
        if doneStatus["where"] == "party":
            self.getPartyZoneAndGoToParty(doneStatus["avId"], doneStatus["zoneId"])
            return
        
        how = doneStatus["how"]
        if how in ["tunnelIn", "teleportIn", "doorIn", "elevatorIn"]:
            self.fsm.request("quietZone", [doneStatus])
        else:
            self.notify.error("Exited hood with unexpected mode %s" % (how))

    def _destroyHood(self):
        # every hood exit handler should call _destroyHood()
        self.ignore(self.hoodDoneEvent)
        self.hood.exit()
        self.hood.unload()
        self.hood = None
        base.cr.cache.flush()

    def enterQuietZone(self, requestStatus):
        assert(self.notify.debug("enterQuietZone()"))
        self.quietZoneDoneEvent = "quietZoneDone"
        self.acceptOnce(self.quietZoneDoneEvent, self.handleQuietZoneDone)
        self.acceptOnce("enterWaitForSetZoneResponse", self.handleWaitForSetZoneResponse)
        self.quietZoneStateData = QuietZoneState.QuietZoneState(
            self.quietZoneDoneEvent)
        self.quietZoneStateData.load()
        self.quietZoneStateData.enter(requestStatus)
        
    def exitQuietZone(self):
        assert(self.notify.debug("exitQuietZone()"))
        self.ignore(self.quietZoneDoneEvent)
        self.ignore("enterWaitForSetZoneResponse")
        del self.quietZoneDoneEvent
        self.quietZoneStateData.exit()
        self.quietZoneStateData.unload()
        self.quietZoneStateData=None

    def handleWaitForSetZoneResponse(self, requestStatus):
        assert(self.notify.debug("handleWaitForSetZoneResponse(requestStatus="
                +str(requestStatus)+")"))

        hoodId = requestStatus["hoodId"]
        canonicalHoodId = ZoneUtil.getCanonicalZoneId(hoodId)
        toHoodPhrase = ToontownGlobals.hoodNameMap[canonicalHoodId][0]
        hoodName = ToontownGlobals.hoodNameMap[canonicalHoodId][-1]
        zoneId = requestStatus["zoneId"]
        loaderName = requestStatus["loader"]
        avId = requestStatus.get("avId", -1)          # Better be conservative; some senders don't set this.
        ownerId = requestStatus.get("ownerId", avId)  # ditto
        
        # Get the loading bar count
        count = ToontownGlobals.hoodCountMap[canonicalHoodId]
        if loaderName=="safeZoneLoader":
            count += ToontownGlobals.safeZoneCountMap[canonicalHoodId]
        elif loaderName=="townLoader":
            count += ToontownGlobals.townCountMap[canonicalHoodId]
        else:
            assert(self.notify.debug("  unknown loaderName="+loaderName))

        if not loader.inBulkBlock:
            if hoodId == ToontownGlobals.MyEstate:
                if avId == -1:
                    # we are going to our own estate
                    loader.beginBulkLoad("hood", TTLocalizer.HeadingToYourEstate, count,
                                         1, TTLocalizer.TIP_ESTATE)
                else:
                    # we are going to someone elses estate, find owners name
                    owner = base.cr.identifyAvatar(ownerId)
                    if (owner == None):
                        # we aren't friends with the owner, get name of avId we are visiting
                        friend = base.cr.identifyAvatar(avId)
                        if friend != None:
                            avName = friend.getName()
                            loader.beginBulkLoad("hood", (TTLocalizer.HeadingToFriend % avName), count,
                                                 1, TTLocalizer.TIP_ESTATE)
                        else:
                            self.notify.warning("we can't perform this teleport")
                            return
                    else:
                        avName = owner.getName()
                        loader.beginBulkLoad("hood", (TTLocalizer.HeadingToEstate % avName), count,
                                             1, TTLocalizer.TIP_ESTATE)
            elif ZoneUtil.isCogHQZone(zoneId):
                loader.beginBulkLoad("hood", (TTLocalizer.HeadingToHood % {'to':toHoodPhrase,'hood':hoodName}), count,
                                     1, TTLocalizer.TIP_COGHQ)
            elif ZoneUtil.isGoofySpeedwayZone(zoneId):
                loader.beginBulkLoad("hood", (TTLocalizer.HeadingToHood % {'to':toHoodPhrase,'hood':hoodName}), count,
                                     1, TTLocalizer.TIP_KARTING)
            else:
                loader.beginBulkLoad("hood", (TTLocalizer.HeadingToHood % {'to':toHoodPhrase,'hood':hoodName}), count,
                                     1, TTLocalizer.TIP_GENERAL)

        if hoodId == ToontownGlobals.Tutorial:
            self.loadDnaStoreTutorial()
        else:
            self.loadDnaStore()
        
        hoodClass = self.getHoodClassByNumber(canonicalHoodId)

        self.hood = hoodClass(self.fsm, self.hoodDoneEvent, self.dnaStore,
                              hoodId)
        self.hood.load()
        self.hood.loadLoader(requestStatus)
        
        loader.endBulkLoad("hood")

    def handleQuietZoneDone(self):
        assert(self.notify.debug("handleQuietZoneDone()"))
        status = self.quietZoneStateData.getRequestStatus()
        hoodId = ZoneUtil.getCanonicalZoneId(status["hoodId"])
        hoodState = self.getHoodStateByNumber(hoodId)
        self.fsm.request(hoodState, [status])

    def enterTTHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitTTHood(self):
        self._destroyHood()

    def enterDDHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitDDHood(self):
        self._destroyHood()

    def enterMMHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitMMHood(self):
        self._destroyHood()

    def enterBRHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitBRHood(self):
        self._destroyHood()

    def enterDGHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitDGHood(self):
        self._destroyHood()

    def enterDLHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitDLHood(self):
        self._destroyHood()

    def enterGSHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitGSHood(self):
        self._destroyHood()

    def enterOZHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitOZHood(self):
        self._destroyHood()

    def enterGZHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitGZHood(self):
        self._destroyHood()        

    def enterSellbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitSellbotHQ(self):
        self._destroyHood()

    def enterCashbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitCashbotHQ(self):
        self._destroyHood()

    def enterLawbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitLawbotHQ(self):
        self._destroyHood()

    def enterBossbotHQ(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitBossbotHQ(self):
        self._destroyHood()        

    def enterTutorialHood(self, requestStatus):
        # Notify that we are now in the tutorial zone
        messenger.send("toonArrivedTutorial")
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        # The book is obscured until you are awarded it by the HQ
        base.localAvatar.book.obscureButton(1)
        base.localAvatar.book.setSafeMode(1)
        # Hide the laff meter until awarded by Tutorial Tom
        base.localAvatar.laffMeter.obscure(1)
        # Hide the chat buttons and friends list
        base.localAvatar.chatMgr.obscure(1, 1)
        base.localAvatar.obscureFriendsListButton(1)
        # Replace teleport in with tutorial mode
        requestStatus["how"] = "tutorial"
        # Lower volume for japanese version so you can hear voice
        if base.config.GetString("language", "english") == "japanese":
            musicVolume = base.config.GetFloat("tutorial-music-volume", 0.5)
            requestStatus['musicVolume'] = musicVolume
        self.hood.enter(requestStatus)        

    def exitTutorialHood(self):
        self.unloadDnaStore()
        self._destroyHood()
        base.localAvatar.book.obscureButton(0)
        base.localAvatar.book.setSafeMode(0)
        base.localAvatar.laffMeter.obscure(0)
        base.localAvatar.chatMgr.obscure(0, 0)
        base.localAvatar.obscureFriendsListButton(-1)

    def enterEstateHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        self.hood.enter(requestStatus)

    def exitEstateHood(self):
        assert(self.notify.debug("exitEstateHood"))
        self._destroyHood()

    def getEstateZoneAndGoHome(self, avId, zoneId):
        self.doneStatus = {"avId":   avId, 
                           "zoneId": zoneId,
                           "hoodId": ToontownGlobals.MyEstate,
                           "loader": "safeZoneLoader",
                           "how":    "teleportIn",
                           "shardId": None,
                           }
        
        self.acceptOnce("setLocalEstateZone", self.goHome)
        if avId > 0:
            # we are teleporting to another toons estate
            base.cr.estateMgr.getLocalEstateZone(avId)
        else:
            # we are teleporting to our own estate
            base.cr.estateMgr.getLocalEstateZone(base.localAvatar.getDoId())

    def goHome(self, ownerId, zoneId):
        self.notify.debug("goHome ownerId = %s" % ownerId)
        # Disallow transitive visits, i.e. teleporting to a friend who is
        # currently at a non-friends estate
        if (ownerId > 0 and ownerId != base.localAvatar.doId and \
            not base.cr.isFriend(ownerId)):
            self.doneStatus["failed"] = 1
            taskMgr.remove("goHomeFailed")
            taskMgr.add(self.goHomeFailed, "goHomeFailed")
            return

        if (ownerId == 0 and zoneId == 0):
            # we are trying to teleport to a friend who isn't around anymore
            self.doneStatus["failed"] = 1
            self.goHomeFailed(None)
            return

        # If the zoneId returned by the AI is different than
        # the one we got in the teleport query, it means we
        # are teleporting directly into a house
        if self.doneStatus["zoneId"] != zoneId:
            # we are teleporting to a house
            self.doneStatus["where"] = "house"
        else:
            self.doneStatus["where"] = "estate"
            

        # for certain functions, we need to know who is the owner of the estate
        self.doneStatus["ownerId"] = ownerId
        #self.doneStatus["zoneId"] = zoneId
        self.fsm.request("quietZone", [self.doneStatus])


    def goHomeFailed(self, task):
        self.notify.debug("goHomeFailed")
        failedToVisitAvId = self.doneStatus.get("avId")

        # disallow transitive friends
        if failedToVisitAvId > 0:
            message = TTLocalizer.EstateTeleportFailedNotFriends % base.cr.identifyAvatar(failedToVisitAvId).getName()
        else:
            message = TTLocalizer.EstateTeleportFailed
        self.notify.debug("goHomeFailed, why =: %s" % message)
        #  ignore the setLocalEstateZone message
        self.ignore("setLocalEstateZone")
        zoneId = base.localAvatar.lastHood
        loaderName = ZoneUtil.getLoaderName(zoneId)
        whereName = ZoneUtil.getToonWhereName(zoneId)
        
        base.localAvatar.setSystemMessage(0, message)
        self.fsm.request("quietZone",
                         [{"loader": loaderName,
                           "where": whereName,
                           "how": "teleportIn",
                           "hoodId": zoneId,
                           "zoneId": zoneId,
                           "shardId": None}])
        return Task.done
        
#===============================================================================
# PARTIES
#===============================================================================

    def enterPartyHood(self, requestStatus):
        self.accept(self.hoodDoneEvent, self.handleHoodDone)
        requestStatus['where'] = "party"
        self.hood.enter(requestStatus)

    def exitPartyHood(self):
        assert(self.notify.debug("exitPartyHood"))
        self._destroyHood()

    def getPartyZoneAndGoToParty(self, avId, zoneId):
        self.doneStatus = {"avId":   avId, 
                           "zoneId": zoneId,
                           "hoodId": ToontownGlobals.PartyHood,
                           "loader": "safeZoneLoader",
                           "how":    "teleportIn",
                           "shardId": None,
                           }
        
        # Avatar id could be host, someone at a party, or us starting a new party
        if avId < 0:
            avId = base.localAvatar.getDoId()
            
        base.cr.partyManager.requestPartyZone(avId, zoneId, callback = self.goToParty)

    def goToParty(self, ownerId, partyId, zoneId):
        assert(self.notify.debug("goToParty ownerId = %s" % ownerId))
        # TODO-parties: Disallow transitive visits, i.e. Teleporting to a friend who is
        # currently at a private party and you're not invited

        if ownerId == 0 and partyId == 0 and zoneId == 0:
            # Something went wrong, back to the playground!
            self.doneStatus["where"] = "playground"
        else:
            # We're going to a party, of course!
            self.doneStatus["where"] = "party"
        self.doneStatus["ownerId"] = ownerId
        self.doneStatus["partyId"] = partyId
        self.doneStatus["zoneId"] = zoneId
        
        self.fsm.request("quietZone", [self.doneStatus])

    def goToPartyFailed(self, reason):
        self.notify.debug("goToPartyFailed")
        failedToVisitAvId = self.doneStatus.get("avId")

        message = base.cr.partyManager.getGoToPartyFailedMessage(reason)

        self.notify.debug("goToPartyFailed, why =: %s" % message)
        #  ignore the gotLocalPartyZone message
        # Isn't this redudant? it's only doing an acceptOnce
        self.ignore("gotLocalPartyZone")
        
        # TODO-parties: If we came here from a party, then make sure to send me back to that party.
        zoneId = base.localAvatar.lastHood
        loaderName = ZoneUtil.getLoaderName(zoneId)
        whereName = ZoneUtil.getToonWhereName(zoneId)
        
        base.localAvatar.setSystemMessage(0, message)
        self.fsm.request("quietZone",
                         [{"loader": loaderName,
                           "where": whereName,
                           "how": "teleportIn",
                           "hoodId": zoneId,
                           "zoneId": zoneId,
                           "shardId": None}])
        return Task.done
    
#===============================================================================

    def getCatalogCodes(self, category):
        numCodes = self.dnaStore.getNumCatalogCodes(category)
        codes = []
        for i in range(numCodes):
            codes.append(self.dnaStore.getCatalogCode(category, i))
        return codes
    
    def getNodePathList(self, catalogGroup):
        result=[]
        codes=self.getCatalogCodes(catalogGroup)
        for code in codes:
            np = self.dnaStore.findNode(code)
            result.append(np)
        return result
    
    def getNodePathDict(self, catalogGroup):
        result={}
        codes=self.getCatalogCodes(catalogGroup)
        for code in codes:
            np = self.dnaStore.findNode(code)
            result[code]=np
        return result

    def getHoodClassByNumber(self, hoodNumber):
        return self.Hood2ClassDict[hoodNumber]

    def getHoodStateByNumber(self, hoodNumber):
        return self.Hood2StateDict[hoodNumber]

    def setPlace(self, place):
        self.place = place
        if self.place:
            # RAU DistributedBattle.calcInteractiveProp listens to this
            # used to get a handle on the actual physical prop
            messenger.send("playGameSetPlace")

    def getPlace(self):
        return self.place

    def getPlaceId(self):
        if self.hood:
            return self.hood.hoodId
        else:
            return None
