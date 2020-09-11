from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from direct.distributed.ClockDelta import *
from toontown.hood import Place
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.task.Task import Task
from toontown.toonbase import TTLocalizer
import random
from direct.showbase import PythonUtil
from toontown.hood import Place
from toontown.hood import SkyUtil
from toontown.toon import GMUtils

from toontown.parties import PartyPlanner

class Party(Place.Place):
    """
    originally copied from Estate.py
    """
    notify = DirectNotifyGlobal.directNotify.newCategory("Party")

    def __init__(self, loader, avId, zoneId, parentFSMState, doneEvent):
        Place.Place.__init__(self, None, doneEvent)

        self.id = PartyHood
        self.avId = avId
        self.zoneId = zoneId
        self.loader = loader
        
        self.musicShouldPlay = False
        self.partyPlannerDoneEvent = "partyPlannerGuiDone"

        self.fsm = ClassicFSM.ClassicFSM(
            'Party',
            [State.State('init',
                         self.enterInit,
                         self.exitInit,
                         ['final', 'teleportIn', 'walk']),
             State.State('walk',
                         self.enterWalk,
                         self.exitWalk,
                         ['final', 'sit', 'stickerBook', 
                          'options', 'quest', 'fishing',
                          'stopped', 'DFA', 'trialerFA',
                          'push', 'activity',
                          ]),
            State.State('stopped',
                        self.enterStopped,
                        self.exitStopped,
                        ['walk', 'teleportOut',
                         ]),
             State.State('sit',
                         self.enterSit,
                         self.exitSit,
                         ['walk',]),
             State.State('push',
                         self.enterPush,
                         self.exitPush,
                         ['walk',]),
             State.State('partyPlanning',
                         self.enterPartyPlanning,
                         self.exitPartyPlanning,
                         ['DFA','teleportOut',
                          ]),
             State.State('stickerBook',
                         self.enterStickerBook,
                         self.exitStickerBook,
                         ['walk', 'sit',
                          'quest', 'fishing',
                          'stopped', 'activity',
                          'push',
                          'DFA', 'trialerFA',
                          ]),
             State.State('teleportIn',
                         self.enterTeleportIn,
                         self.exitTeleportIn,
                         ['walk', 'partyPlanning']),
             State.State('teleportOut',
                         self.enterTeleportOut,
                         self.exitTeleportOut,
                         ['teleportIn', 'walk', 'final']), # 'final'                         
             State.State('died', # Only for certain edge cases.
                         self.enterDied,
                         self.exitDied,
                         ['walk', 'final']),
             State.State('final',
                         self.enterFinal,
                         self.exitFinal,
                         ['teleportIn']),
             State.State('quest',
                         self.enterQuest,
                         self.exitQuest,
                         ['walk']),
             State.State('fishing',
                         self.enterFishing,
                         self.exitFishing,
                         ['walk', 'stopped']),
             State.State('activity',
                         self.enterActivity,
                         self.exitActivity,
                         ['walk', 'stopped']),                          
             State.State('stopped',
                         self.enterStopped,
                         self.exitStopped,
                         ['walk']),
             # Trialer Force Acknowledge:
             State.State('trialerFA',
                         self.enterTrialerFA,
                         self.exitTrialerFA,
                         ['trialerFAReject', 'DFA']),
             State.State('trialerFAReject',
                         self.enterTrialerFAReject,
                         self.exitTrialerFAReject,
                         ['walk']),
             # Download Force Acknowledge
             State.State('DFA',
                         self.enterDFA,
                         self.exitDFA,
                         ['DFAReject',
                          'teleportOut']),
             State.State('DFAReject',
                         self.enterDFAReject,
                         self.exitDFAReject,
                         ['walk']),
             ],
            # Initial state
            'init',
            # Final state
            'final',
            )
        
        self.fsm.enterInitialState()
        self.doneEvent = doneEvent
        self.parentFSMState = parentFSMState        
        self.isPartyEnding = False        
                
        self.accept("partyStateChanged", self.setPartyState)     
        
    def delete(self):
        assert(self.notify.debug("delete()"))
        self.unload()
        
    def load(self):
        assert(self.notify.debug("load()"))
        self.fog = Fog("PartyFog")
        # Call up the chain
        Place.Place.load(self)
        if hasattr(base.localAvatar, "aboutToPlanParty") and base.localAvatar.aboutToPlanParty:
            if not hasattr(self, "partyPlanner") or self.partyPlanner is None:
                self.partyPlanner = PartyPlanner.PartyPlanner(self.partyPlannerDoneEvent)

        self.parentFSMState.addChild(self.fsm)

    def unload(self):
        assert(self.notify.debug("unload()"))
        if hasattr(self,'partyPlanner'):
            # an AI reset can bring us to this point
            # we need to ignore the event as the handler also calls partyPlanner.close
            self.ignore( self.partyPlannerDoneEvent )
            self.partyPlanner.close()
            del self.partyPlanner
        if hasattr(base, "distributedParty"):
            if base.cr.doId2do.has_key(base.distributedParty.partyInfo.hostId):
                host = base.cr.doId2do[base.distributedParty.partyInfo.hostId]
                if hasattr(host, "gmIcon") and host.gmIcon:
                    host.removeGMIcon()
                    host.setGMIcon()
        self.fog = None
        self.ignoreAll()
        self.parentFSMState.removeChild(self.fsm)
        del self.fsm
        Place.Place.unload(self)

    def enter(self, requestStatus):
        """
        enter this party and start the state machine
        """
        assert(self.notify.debug("enter(requestStatus="+str(requestStatus)+")"))
        
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]

        # start the sky
        self.loader.hood.startSky()
        #self.loader.hood.sky.setFogOff()
        #self.__setFaintFog()
        # Turn on the animated props for the party
        for i in self.loader.nodeList:
            self.loader.enterAnimatedProps(i)
        self.loader.geom.reparentTo(render)        

        self.fsm.request(requestStatus["how"], [requestStatus])
        
        self.playMusic()
    
    def playMusic(self):
        """
        Only play the default music if the party doesn't have a jukebox.
        If the party has a jukebox, then the jukebox will take care of the music.
        partyHasJukebox flag is set by DistributedParty
        """
        if not hasattr(base, 'partyHasJukebox') or not base.partyHasJukebox:
            base.playMusic(self.loader.music, looping = 1, volume = 1)

    def exit(self):
        assert(self.notify.debug("exit"))
        base.localAvatar.stopChat()

        # Make sure our ClassicFSM goes into its final state
        # so the walkStateData cleans up its tasks
        if (hasattr(self, 'fsm')):
            self.fsm.requestFinalState()

        # hide the party terrain
        self.loader.geom.reparentTo(hidden)

        # Turn off the animated props once since there is only one zone
        for i in self.loader.nodeList:
            self.loader.exitAnimatedProps(i)

        # Turn the sky off
        self.loader.hood.stopSky()

        render.setFogOff()
        base.cr.cache.flush()
        
        self.loader.music.stop()        
                                
        self.notify.debug("exit")
        self.ignoreAll()
    
    def __setZoneId(self, zoneId):
        assert(self.notify.debug("setting our local zone ID from %d to %d" % (self.zoneId, zoneId)))
        self.zoneId = zoneId

    def doRequestLeave(self, requestStatus):
        # when it's time to leave, check their trialer status first
        self.fsm.request('trialerFA', [requestStatus])

    def enterInit(self):
        pass

    def exitInit(self):
        pass

    def enterPartyPlanning(self, requestStatus):
        assert(self.notify.debug("enterPartyPlanning()"))
        base.localAvatar.aboutToPlanParty = False
        self.accept(self.partyPlannerDoneEvent, self.handlePartyPlanningDone)

    def handlePartyPlanningDone(self):
        self.ignore( self.partyPlannerDoneEvent )
        self.partyPlanner.close()
        del self.partyPlanner
        # Start the process of freeing the planning zone
        messenger.send("deallocateZoneIdFromPlannedParty", [base.localAvatar.zoneId])
        # We're done planning, let's go back to the playground we came from!
        hoodId = base.localAvatar.lastHood
        self.fsm.request( "teleportOut", [ {
            'avId': -1,
            'zoneId': hoodId,
            'shardId': None,
            'how': 'teleportIn',
            'hoodId': hoodId,
            'loader': 'safeZoneLoader',
            'where': "playground",
        } ] )

    def exitPartyPlanning(self):
        assert(self.notify.debug("exitPartyPlanning()"))

    def enterTeleportIn(self, requestStatus):
        assert(self.notify.debug("enterTeleportIn()"))
        # This gets set by init of DistributedParty, it also gets cleaned up by
        # DistributedParty in delete.
        if hasattr(base, "distributedParty"):
            x,y,z = base.distributedParty.getClearSquarePos()
            if base.cr.doId2do.has_key(base.distributedParty.partyInfo.hostId):
                host = base.cr.doId2do[base.distributedParty.partyInfo.hostId]
                if hasattr(host, "gmIcon") and host.gmIcon:
                    host.removeGMIcon()
                    host.setGMPartyIcon()
                else:
                    base.distributedParty.partyHat.reparentTo(host.nametag.getNameIcon())
        else:
            x,y,z = (0.0, 0.0, 0.1)
        base.localAvatar.detachNode()
        base.localAvatar.setPos(render, x,y,z)
        base.localAvatar.lookAt(0.0, 0.0, 0.1)
        base.localAvatar.setScale(1,1,1)
        Place.Place.enterTeleportIn(self, requestStatus)        
                
        if hasattr(base, "distributedParty") and base.distributedParty:
            self.setPartyState(base.distributedParty.getPartyState())

        # If we're about to plan a party, set the next state to partyPlanning
        if hasattr(base.localAvatar, "aboutToPlanParty") and base.localAvatar.aboutToPlanParty:
            self.nextState = 'partyPlanning'

    def enterTeleportOut(self, requestStatus):
        assert(self.notify.debug("enterTeleportOut()"))
        Place.Place.enterTeleportOut(self, requestStatus, 
                self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        assert(self.notify.debug("__teleportOutDone()"))
        # If we're teleporting from a safezone, we need to set the
        # fsm to the final state
        if (hasattr(self, 'fsm')):
            self.fsm.requestFinalState()
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        avId = requestStatus["avId"]
        shardId = requestStatus["shardId"]
        
        # If we're at a party and we're going to the same party
        if ((hoodId == ToontownGlobals.PartyHood) and
            (zoneId == self.getZoneId()) and
            shardId == None):
            self.fsm.request("teleportIn", [requestStatus])
        # we are going to an estate
        elif hoodId == ToontownGlobals.MyEstate:
            self.doneStatus = requestStatus
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent, [self.doneStatus])

    def goHomeFailed(self, task):
        # it took to long to hear back from the server,
        # or we tried going to a non-friends house
        self.notifyUserGoHomeFailed()
        self.doneStatus["avId"] =  -1
        self.doneStatus["zoneId"] =  self.getZoneId()
        self.fsm.request("teleportIn", [self.doneStatus])
        return Task.done

    def exitTeleportOut(self):
        assert(self.notify.debug("exitTeleportOut()"))
        Place.Place.exitTeleportOut(self)

    def getZoneId(self):
        """
        Returns the current zone ID.  This is either the same as the
        hoodID for a Playground class, or the current zoneId for a Town
        class.
        """
        if self.zoneId:
            return self.zoneId
        else:
            self.notify.warning("no zone id available")
        
    """
    def __setFaintFog(self):
        if base.wantFog:
            self.fog.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
            self.fog.setLinearRange(0.1, 700.0)
            render.setFog(self.fog)
    """         
    def enterActivity(self, setAnimState=True):
        if setAnimState:
            base.localAvatar.b_setAnimState('neutral', 1)
        # People can still teleport to us 
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(False)
        base.localAvatar.laffMeter.start()

    def exitActivity(self):
        # Turn off what we turned on
        base.localAvatar.setTeleportAvailable(True)
        self.ignore("teleportQuery")
        base.localAvatar.laffMeter.stop()        
                
    def setPartyState(self, partyState):
        self.isPartyEnding = partyState             
                        
    def handleTeleportQuery(self, fromAvatar, toAvatar):
        """
        Called when another avatar somewhere in the world wants to
        teleport to us, and we're available to be teleported to.
        """        
        if self.isPartyEnding: 
            fromAvatar.d_teleportResponse(toAvatar.doId, 0, toAvatar.defaultShard,
                                      base.cr.playGame.getPlaceId(), self.getZoneId())                                      
        else:        
            fromAvatar.d_teleportResponse(toAvatar.doId, 1, toAvatar.defaultShard,
                                      base.cr.playGame.getPlaceId(), self.getZoneId())
