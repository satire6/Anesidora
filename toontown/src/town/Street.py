"""Street module: contains the Street class"""

from pandac.PandaModules import *
from toontown.battle.BattleProps import *
from toontown.battle.BattleSounds import *
from toontown.distributed.ToontownMsgTypes import *
from direct.gui.DirectGui import cleanupDialog
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from toontown.battle import BattlePlace
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.task import Task
from toontown.battle import BattleParticles
from toontown.building import Elevator
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.estate import HouseGlobals
from toontown.toonbase import TTLocalizer
from direct.interval.IntervalGlobal import *


visualizeZones = base.config.GetBool("visualize-zones", 0)

class Street(BattlePlace.BattlePlace):
    """
    Street class
    """

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("Street")
    
    # special methods

    def __init__(self, loader, parentFSM, doneEvent):
        """
        Street constructor: create a play game ClassicFSM
        """
        assert self.notify.debug("__init__()")
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.fsm = ClassicFSM.ClassicFSM('Street',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['walk', 'tunnelIn', 
                                         'doorIn', 'teleportIn',
                                         'elevatorIn']),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['push', 'sit', 'stickerBook', 
                                         'WaitForBattle', 'battle', 
                                         'DFA', 'trialerFA',
                                         'doorOut', 'elevator',
                                         'tunnelIn', 'tunnelOut', 
                                         'teleportOut', 'quest',
                                         'stopped', 'fishing', 'purchase',
                                         'died']),
                            State.State('sit',
                                        self.enterSit,
                                        self.exitSit,
                                        ['walk',]),
                            State.State('push',
                                        self.enterPush,
                                        self.exitPush,
                                        ['walk',]),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'push', 'sit', 'battle',
                                         'DFA', 'trialerFA',
                                         'doorOut', 'elevator',
                                         'tunnelIn', 'tunnelOut', 
                                         'WaitForBattle', 'teleportOut', 'quest',
                                         'stopped', 'fishing', 'purchase',
                                         ]),
                            State.State('WaitForBattle',
                                        self.enterWaitForBattle,
                                        self.exitWaitForBattle,
                                        ['battle', 'walk']),
                            State.State('battle',
                                        self.enterBattle,
                                        self.exitBattle,
                                        ['walk', 'teleportOut', 'died']),
                            State.State('doorIn',
                                        self.enterDoorIn,
                                        self.exitDoorIn,
                                        ['walk']),
                            State.State('doorOut',
                                        self.enterDoorOut,
                                        self.exitDoorOut,
                                        ['walk']),
                            State.State('elevatorIn',
                                        self.enterElevatorIn,
                                        self.exitElevatorIn,
                                        ['walk']),
                            State.State('elevator',
                                        self.enterElevator,
                                        self.exitElevator,
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
                            # Download Force Acknowlege:
                            State.State('DFA',
                                        self.enterDFA,
                                        self.exitDFA,
                                        ['DFAReject', 'teleportOut', 'tunnelOut']),
                            State.State('DFAReject',
                                        self.enterDFAReject,
                                        self.exitDFAReject,
                                        ['walk']),
                            State.State('teleportIn',
                                        self.enterTeleportIn,
                                        self.exitTeleportIn,
                                        ['walk', 'teleportOut', 'quietZone',
                                         'WaitForBattle', 'battle']),
                            State.State('teleportOut',
                                        self.enterTeleportOut,
                                        self.exitTeleportOut,
                                        ['teleportIn', 'quietZone',
                                         'WaitForBattle']),
                            State.State('died',
                                        self.enterDied,
                                        self.exitDied,
                                        ['quietZone']),
                            State.State('tunnelIn',
                                        self.enterTunnelIn,
                                        self.exitTunnelIn,
                                        ['walk']),
                            State.State('tunnelOut',
                                        self.enterTunnelOut,
                                        self.exitTunnelOut,
                                        ['final']),
                            State.State('quietZone',
                                        self.enterQuietZone,
                                        self.exitQuietZone,
                                        ['teleportIn']),
                            State.State('quest',
                                        self.enterQuest,
                                        self.exitQuest,
                                        ['walk','stopped']),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk']),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk']),
                            State.State('fishing',
                                        self.enterFishing,
                                        self.exitFishing,
                                        ['walk']),
                            State.State('purchase',
                                        self.enterPurchase,
                                        self.exitPurchase,
                                        ['walk']),
                            State.State('final',
                                        self.enterFinal,
                                        self.exitFinal,
                                        ['start'])],
                          
                           # Initial State
                           'start',
                           # Final State
                           'final',
                           )
        self.parentFSM = parentFSM
        self.tunnelOriginList = []
        self.elevatorDoneEvent = "elevatorDone"
        
        # For Halloween
        self.halloweenLights = []

    def enter(self, requestStatus, visibilityFlag=1, arrowsOn=1):
        # Note: The visibilityFlag was added for the tutorial, which
        # doesn't want visibility. TutorialStreet overrides this function,
        # calling it with visibilityFlag=0. 
        assert self.notify.debug("enter(requestStatus="+str(requestStatus)
                                 +")")
        self.fsm.enterInitialState()
        # Play music
        base.playMusic(self.loader.music, looping = 1, volume = 0.8)
        self.loader.geom.reparentTo(render)
        if visibilityFlag:
            self.visibilityOn()

        ## give the camera a nodepath to the geometry
        #base.localAvatar.camera.setGeom(self.geom)
        base.localAvatar.setGeom(self.loader.geom)
        ## tell the camera that we're in a level area
        #base.localAvatar.camera.onLevelGround(1)
        base.localAvatar.setOnLevelGround(1)

        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(arrowsOn)

        # Turn the sky on
        # For halloween
        def __lightDecorationOn__():
            geom = base.cr.playGame.getPlace().loader.geom
            self.halloweenLights  = geom.findAllMatches("**/*light*")
            self.halloweenLights += geom.findAllMatches("**/*lamp*")
            self.halloweenLights += geom.findAllMatches("**/prop_snow_tree*")
            
            for light in self.halloweenLights:
                #light.reparentTo(render)
                light.setColorScaleOff(1)

        newsManager = base.cr.newsManager

        if newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            if (ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds) and self.loader.hood.spookySkyFile:

                lightsOff = Sequence(LerpColorScaleInterval(
                    base.cr.playGame.hood.loader.geom,
                    0.1,
                    Vec4(0.55, 0.55, 0.65, 1)),
                    Func(self.loader.hood.startSpookySky),
                    # Func(__lightDecorationOn__),
                    )

                lightsOff.start()
            else:
                # Turn the sky on
                self.loader.hood.startSky()
                lightsOn = LerpColorScaleInterval(
                    base.cr.playGame.hood.loader.geom,
                    0.1,
                    Vec4(1, 1, 1, 1))
                lightsOn.start()
        else:
            # Turn the sky on
            self.loader.hood.startSky()
            lightsOn = LerpColorScaleInterval(
                base.cr.playGame.hood.loader.geom,
                0.1,
                Vec4(1, 1, 1, 1))
            lightsOn.start()

        self.accept("doorDoneEvent", self.handleDoorDoneEvent)
        self.accept("DistributedDoor_doorTrigger", self.handleDoorTrigger)

        self.enterZone(requestStatus["zoneId"])

        # Add hooks for the linktunnels
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, 
                self.loader.nodeList, self.zoneId)

        # Note that the following fsm request *could* result in an
        # immediate request to teleportOut, which will call exit() and
        # unload() before it returns!  This will happen in the case in
        # which we are teleporting to visit a particular toon, who is
        # no longer in this zone by the time we get there (which
        # requires immediately teleporting back to the safezone).
        self.fsm.request(requestStatus["how"], [requestStatus])
        
    def exit(self, visibilityFlag=1):
        # See note on "enter" function about visibilityFlag.
        assert self.notify.debug("exit()")

        if visibilityFlag:
            self.visibilityOff()
        self.loader.geom.reparentTo(hidden)
        
        # For halloween
        def __lightDecorationOff__():
            for light in self.halloweenLights:
                light.reparentTo(hidden)

        newsManager = base.cr.newsManager

##        if newsManager:
##            holidayIds = base.cr.newsManager.getDecorationHolidayId()
##            if (ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds) and self.loader.hood.spookySkyFile:
##                __lightDecorationOff__()
        
##        for node in self.tunnelOriginList:
##            node.removeNode()
##        del self.tunnelOriginList

        # Turn off the little red arrows.
        NametagGlobals.setMasterArrowsOn(0)

        # Turn the sky off
        self.loader.hood.stopSky()

        # Stop music
        self.loader.music.stop()

        ## reset the camera to collide against everything and anything
        #base.localAvatar.camera.setGeom(render)
        base.localAvatar.setGeom(render)
        ## tell the camera we're leaving an area with level ground
        #base.localAvatar.camera.onLevelGround(0)
        base.localAvatar.setOnLevelGround(0)


    def load(self):
        assert self.notify.debug("load()")
        # Call up the chain
        BattlePlace.BattlePlace.load(self)
        # Prepare the state machine
        self.parentFSM.getStateNamed("street").addChild(self.fsm)
    
    def unload(self):
        assert self.notify.debug("unload()")
        self.parentFSM.getStateNamed("street").removeChild(self.fsm)
        del self.parentFSM
        del self.fsm
        self.enterZone(None)

        # remove any dfa dialogs
        cleanupDialog("globalDialog")
        self.ignoreAll()
        # Call up the chain
        BattlePlace.BattlePlace.unload(self)        

    # walk state inherited from BattlePlace.py

    # sticker book state inherited from Place.py
        
    # battle state inherited from BattlePlace.py

    # elevatorIn state
    # (for coming off of an elevator for a victory dance)
    def enterElevatorIn(self, requestStatus):
        assert self.notify.debug("enterElevatorIn()")
        # Whew! Where did bldgDoId get set?
        # Look in DistributedSuitInterior.py, in the enterReward state.
        # Hey! That's funny... We don't even seem to need this, unless
        # we want to use it to place ourselves inside the elevator while
        # we wait for the building to start the movie...
        bldg = base.cr.doId2do.get(requestStatus['bldgDoId'])
        # TODO: Place us in the elevator while we wait for the building
        # to start the movie.

        # We throw this event to tell the building that we are ready
        # to exit the building now.
        messenger.send("insideVictorElevator")
        assert bldg

    def exitElevatorIn(self):
        assert self.notify.debug("exitElevatorIn()")
        

    # elevator state
    # (For boarding a building elevator)
    def enterElevator(self, distElevator):
        assert self.notify.debug("enterElevator()")

        # Disable leave to pay / set parent password
        base.localAvatar.cantLeaveGame = 1

        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed("elevator"),
                                          self.elevatorDoneEvent,
                                          distElevator)
        self.elevator.load()
        self.elevator.enter()
        return

    def exitElevator(self):
        assert self.notify.debug("exitElevator()")
        base.localAvatar.cantLeaveGame = 0
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()
        del self.elevator
        return

    def detectedElevatorCollision(self, distElevator):
        assert self.notify.debug("detectedElevatorCollision()")
        self.fsm.request("elevator", [distElevator])
        return None

    def handleElevatorDone(self, doneStatus):
        assert self.notify.debug("handleElevatorDone()")
        self.notify.debug("handling elevator done event")
        where = doneStatus['where']
        if (where == 'reject'):
            # If there has been a reject the Elevator should show an 
            # elevatorNotifier message and put the toon in the stopped state.
            # Don't request the walk state here. Let the the toon be stuck in the
            # stopped state till the player removes that message from his screen.
            # Removing the message will automatically put him in the walk state there.
            # Put the player in the walk state only if there is no elevator message.
            if hasattr(base.localAvatar, "elevatorNotifier") and base.localAvatar.elevatorNotifier.isNotifierOpen():
                pass
            else:
                self.fsm.request("walk")
        elif (where == 'exit'):
            self.fsm.request("walk")
        elif (where in ('suitInterior', 'cogdoInterior')):
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error("Unknown mode: " + where +
                              " in handleElevatorDone")

    # tunnel in state partly inherited from Place.py

    def enterTunnelIn(self, requestStatus):
        """
        If we are entering a street, we need to show the tunnel
        because the collisions are not turned on until we start
        walking which means we will not get the onfloor event until
        we finish walking through the tunnel which means the tunnel
        will be hidden because of visibility
        
        SO... we explicitly set you into the zone you're headed
        towards, which both reveals the tunnel and indicates the
        correct zone ID as your current zone, in case anyone needs
        to know your zone ID in the next few milliseconds.
        """
        assert self.notify.debug("enterTunnelIn(requestStatus="+str(requestStatus)+")")
        self.enterZone(requestStatus["zoneId"])
        BattlePlace.BattlePlace.enterTunnelIn(self, requestStatus)

    # tunnel out state inherited from Place.py

    # teleportIn state partly inherited from Place.py

    def enterTeleportIn(self, requestStatus):
        assert self.notify.debug("enterTeleportIn(requestStatus="+str(requestStatus)+")")
        avId = requestStatus["avId"]
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        
        if avId != -1:
            if not base.cr.doId2do.has_key(avId):
                # We're trying to teleport to a toon who isn't here
                # any more.  Forget it, and bail to the safezone.
                handle = base.cr.identifyFriend(avId)
                requestStatus = {"how" : "teleportIn",
                                 "hoodId" : hoodId,
                                 "zoneId" : hoodId,
                                 "shardId" : None,
                                 "loader" : "safeZoneLoader",
                                 "where" : "playground",
                                 "avId" : avId}

                # We don't actually want to switch to the teleportOut
                # state, because that will play the jump-in-the-hole
                # animation and everything.  Instead, we'll switch to
                # the final state, and just directly execute the code
                # that takes us out of here.

                # Note that switching states like this in the middle
                # of the enterTeleportIn call can potentially confuse
                # our parent state objects that didn't expect to
                # suddenly switch out of their own state just as they
                # were finishing up teleporting in.  We will have to
                # be careful in coding the parent state objects so
                # that they can handle this.
                self.fsm.request('final')
                self.__teleportOutDone(requestStatus)
                return

        # In the normal case, if we're not going directly to an avatar
        # (or the avatar we're going to is still in sight), then set
        # our zone and go there.
        self.enterZone(zoneId)
        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)

    # teleport out state

    def enterTeleportOut(self, requestStatus):
        assert self.notify.debug("enterTeleportOut(requestStatus="+str(requestStatus)+")")
        # If the request comes from a battle, let the battle handle
        # the teleport animation sequence, otherwise use the distributed
        # toon version
        if (requestStatus.has_key('battle')):
            self.__teleportOutDone(requestStatus)
        else:
            BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus,
                    self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        assert self.notify.debug("__teleportOutDone(requestStatus="+str(requestStatus)+")")
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        shardId = requestStatus["shardId"]
        if (hoodId == self.loader.hood.id and shardId == None):
            # We are in the same hood
            if (zoneId == self.zoneId):
                # We are teleporting to somebody in the same zone,
                # just do it
                self.fsm.request("teleportIn", [requestStatus])
            elif (requestStatus["where"]=="street"
                  and ZoneUtil.getBranchZone(zoneId)
                  ==self.loader.branchZone):
                # If you are teleporting to somebody in this branch.
                # In this case, we don't need to leave the town or
                # anything, but we do need to be careful with the set
                # zone.  We can't just send the set-zone message and
                # go, since we need to be sure we'll have been told
                # about the toon by the time we get there, so we must
                # wait for the set-zone message to be completed.
                self.fsm.request("quietZone", [requestStatus])
            else:
                # Somebody in the same town, different branch, or safe
                # zone we have to leave the town mode and come back in
                self.doneStatus = requestStatus
                messenger.send(self.doneEvent)
        else:
            # Different hood, we have to leave the town
            if (hoodId == ToontownGlobals.MyEstate):
                self.getEstateZoneAndGoHome(requestStatus)
            else:
                self.doneStatus = requestStatus
                messenger.send(self.doneEvent)

    def exitTeleportOut(self):
        assert self.notify.debug("exitTeleportOut()")
        BattlePlace.BattlePlace.exitTeleportOut(self)

    def goHomeFailed(self, task):
        # it took too long to hear back from the server,
        # or we tried going to a non-friends house
        self.notifyUserGoHomeFailed()
        #  ignore the setLocalEstateZone message
        self.ignore("setLocalEstateZone")
        self.doneStatus["avId"] =  -1
        self.doneStatus["zoneId"] =  self.getZoneId()
        self.fsm.request("teleportIn", [self.doneStatus])
        return Task.done

    # Quietzone is in Place.py

    def renameFloorPolys(self, nodeList):
        assert self.notify.debug("renameFloorPolys()")
        for i in nodeList:
            # Get all the collision nodes in the vis group
            collNodePaths = i.findAllMatches("**/+CollisionNode")
            numCollNodePaths = collNodePaths.getNumPaths()
            visGroupName = i.node().getName()
            for j in range(numCollNodePaths):
                collNodePath = collNodePaths.getPath(j)
                bitMask = collNodePath.node().getIntoCollideMask()
                if bitMask.getBit(1):
                    # Bit 1 is the floor collision bit. This renames
                    # all floor collision polys to the same name as their
                    # visgroup.
                    collNodePath.node().setName(visGroupName)

    def hideAllVisibles(self):
        assert self.notify.debug("hideAllVisibles()")
        for i in self.loader.nodeList:
            i.stash()

    def showAllVisibles(self):
        assert self.notify.debug("showAllVisibles()")
        for i in self.loader.nodeList:
            i.unstash()

    def visibilityOn(self):
        assert self.notify.debug("visibilityOn()")
        self.hideAllVisibles()
        self.accept("on-floor", self.enterZone)

    def visibilityOff(self):
        assert self.notify.debug("visibilityOff()")
        self.ignore("on-floor")
        self.showAllVisibles()

    def doEnterZone(self, newZoneId):
        # Ensure we are in a hood
        assert self.loader.nodeDict and self.loader.hood

        # Hide the old zone (if there is one)
        if self.zoneId != None:
            for i in self.loader.nodeDict[self.zoneId]:
                if newZoneId:
                    if (i not in self.loader.nodeDict[newZoneId]):
                        self.loader.fadeOutDict[i].start()
                        self.loader.exitAnimatedProps(i)
                else:
                    i.stash()
                    self.loader.exitAnimatedProps(i)

        # Show the new zone
        if newZoneId != None:

            for i in self.loader.nodeDict[newZoneId]:
                # self.notify.debug(str(newZoneId)+" Visgroup: "+ i.getIntoNode().getName())
                if self.zoneId:
                    if (i not in self.loader.nodeDict[self.zoneId]):
                        self.loader.fadeInDict[i].start()
                        self.loader.enterAnimatedProps(i)
                else:
                    # Finish any fade out tracks if they are playing
                    # otherwise you could teleport to a zone that is fading out
                    if self.loader.fadeOutDict[i].isPlaying():
                        self.loader.fadeOutDict[i].finish()
                    # Same with fade in
                    if self.loader.fadeInDict[i].isPlaying():
                        self.loader.fadeInDict[i].finish()
                    self.loader.enterAnimatedProps(i)
                    i.unstash()
                    
        # Make sure we changed zones
        if newZoneId != self.zoneId:
            if visualizeZones:
                # Set a color override on our zone to make it obvious what
                # zone we're in.
                if self.zoneId != None:
                    self.loader.zoneDict[self.zoneId].clearColor()
                if newZoneId != None:
                    self.loader.zoneDict[newZoneId].setColor(0, 0, 1, 1, 100)
            
            # Tell the server that we changed zones
            if newZoneId != None:
                base.cr.sendSetZoneMsg(newZoneId)
                self.notify.debug("Entering Zone %d" % (newZoneId))
                
            # The new zone is now old
            self.zoneId = newZoneId
        assert self.notify.debug("  newZoneId="+str(newZoneId))
        
        geom = base.cr.playGame.getPlace().loader.geom
        self.halloweenLights  = geom.findAllMatches("**/*light*")
        self.halloweenLights += geom.findAllMatches("**/*lamp*")
        self.halloweenLights += geom.findAllMatches("**/prop_snow_tree*")

        for light in self.halloweenLights:
            #light.reparentTo(render)
            light.setColorScaleOff(1)
