from pandac.PandaModules import *
from toontown.toon import Toon
from toontown.hood import Place

class BattlePlace(Place.Place):
    def __init__(self, loader, doneEvent):
        assert(self.notify.debug("__init__()"))
        Place.Place.__init__(self, loader, doneEvent)

    def load(self):
        Place.Place.load(self)
        # load Toon battle anims and props
        Toon.loadBattleAnims()

    def setState(self, state, battleEvent=None):
        assert(self.notify.debug("setState(state="+str(state)
                +", battleEvent="+str(battleEvent)+")"))
        if (battleEvent):
            if not self.fsm.request(state, [battleEvent]):
                self.notify.warning("fsm.request('%s') returned 0 (zone id %s, avatar pos %s)." 
                    % (state, self.zoneId, base.localAvatar.getPos(render)))
        else:
            if not self.fsm.request(state):
                self.notify.warning("fsm.request('%s') returned 0 (zone id %s, avatar pos %s)." 
                    % (state, self.zoneId, base.localAvatar.getPos(render)))

    def enterWalk(self, flag=0):
        assert(self.notify.debug("enterWalk()"))
        Place.Place.enterWalk(self, flag)
        # handlers
        self.accept("enterBattle", self.handleBattleEntry)
        
    def exitWalk(self):
        assert(self.notify.debug("exitWalk()"))
        Place.Place.exitWalk(self)
        self.ignore("enterBattle")

    def enterWaitForBattle(self):
        assert(self.notify.debug("enterWaitForBattle()"))
        base.localAvatar.b_setAnimState('neutral', 1)

    def exitWaitForBattle(self):
        assert(self.notify.debug("exitWaitForBattle()"))

    def enterBattle(self, event):
        assert(self.notify.debug("enterBattle()"))
        self.loader.music.stop()
        base.playMusic(self.loader.battleMusic, looping=1, volume=0.9)
        self.enterTownBattle(event)

        # Make sure the toon's anim state gets reset
        base.localAvatar.b_setAnimState('off', 1)
        # A query for a teleport location might come along while we're
        # in battle, which is acceptable.  We should handle it, so
        # friends can teleport to us to help us out.
        # We can't put this handler in the TownBattle object, because
        # it doesn't know what zone or hood we're in.
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)
        # Disable leave to pay / set parent password
        base.localAvatar.cantLeaveGame = 1

    def enterTownBattle(self, event):
        self.loader.townBattle.enter(event, self.fsm.getStateNamed("battle"))
        
    def exitBattle(self):
        assert(self.notify.debug("exitBattle()"))
        self.loader.townBattle.exit()
        self.loader.battleMusic.stop()
        base.playMusic(self.loader.music, looping=1, volume=0.8)
        base.localAvatar.cantLeaveGame = 0
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")

    def handleBattleEntry(self):
        assert(self.notify.debug("handleBattleEntry()"))
        self.fsm.request("battle")
    
    def enterFallDown(self, extraArgs=[]):
        assert(self.notify.debug("enterFallDown()"))
        # exitWalk hides the laffmeter, so start it here
        base.localAvatar.laffMeter.start()
         # Play the 'slip backwards' animation
        base.localAvatar.b_setAnimState('FallDown',
                                        callback=self.handleFallDownDone,
                                        extraArgs=extraArgs)

    def handleFallDownDone(self):
        # put place back in walk state after squish is done
        base.cr.playGame.getPlace().setState("walk")
        
    def exitFallDown(self):
        assert(self.notify.debug("exitFallDown"))
        base.localAvatar.laffMeter.stop()
    
    def enterSquished(self):
        assert(self.notify.debug("enterSquished()"))
        # exitWalk hides the laffmeter, so start it here
        base.localAvatar.laffMeter.start()
        # Play the 'squish' animation
        base.localAvatar.b_setAnimState('Squish')
        # Put toon back in walk state after a couple seconds
        taskMgr.doMethodLater(2.0,
                              self.handleSquishDone,
                              base.localAvatar.uniqueName("finishSquishTask"))
        
    def handleSquishDone(self, extraArgs=[]):
        # put place back in walk state after squish is done
        base.cr.playGame.getPlace().setState("walk")
        #self.fsm.request("walk")
        
    def exitSquished(self):
        assert(self.notify.debug("exitSquished()"))
        taskMgr.remove(base.localAvatar.uniqueName("finishSquishTask"))
        base.localAvatar.laffMeter.stop()
    
    def enterZone(self, newZone):
        """
        Puts the toon in the indicated zone.  newZone may either be a
        CollisionEntry object as determined by a floor polygon, or an
        integer zone id.  It may also be None, to indicate no zone.
        """
        assert(self.notify.debug("enterZone(newZone=%s)"%(newZone,)))
        if isinstance(newZone, CollisionEntry):
            # Get the name of the collide node
            try:
                newZoneId = int(newZone.getIntoNode().getName())
            except:
                self.notify.warning("Invalid floor collision node in street: %s" % (newZone.getIntoNode().getName()))
                return
        else:
            newZoneId = newZone

        self.doEnterZone(newZoneId)

    def doEnterZone(self, newZoneId):
        """
        Puts the Toon in the indicated zone, which is an integer
        number.  This is overridden in Street.py to implement
        zone-based visibility of geometry.
        """
        if newZoneId != self.zoneId:
            # Tell the server that we changed zones
            if newZoneId != None:
                base.cr.sendSetZoneMsg(newZoneId)
                self.notify.debug("Entering Zone %d" % (newZoneId))
                
            # The new zone is now old
            self.zoneId = newZoneId
        assert(self.notify.debug("  newZoneId="+str(newZoneId)))
