"""Playground module: contains the Playground class"""

from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import Place
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from toontown.toon import DeathForceAcknowledge
from toontown.toon import HealthForceAcknowledge
from toontown.tutorial import TutorialForceAcknowledge
from toontown.toon import NPCForceAcknowledge
from toontown.trolley import Trolley
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from direct.gui import DirectLabel
from toontown.quest import Quests

class Playground(Place.Place):
    """Playground class"""

    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("Playground")

    # special methods

    def __init__(self, loader, parentFSM, doneEvent):
        """
        Playground constructor: create a play game ClassicFSM
        """
        assert(self.notify.debug("__init__()"))
        Place.Place.__init__(self, loader, doneEvent)

        self.tfaDoneEvent = "tfaDoneEvent"
        # shared state
        self.fsm = ClassicFSM.ClassicFSM('Playground',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['walk', 'deathAck', 
                                        'doorIn', 'tunnelIn']),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['drive', 'sit', 'stickerBook',
                                         'TFA', 'DFA', 'trialerFA',
                                         'trolley', 'final',
                                         'doorOut', 'options', 'quest',
                                         'purchase', 'stopped', 'fishing']),
                            State.State('stickerBook',
                                        self.enterStickerBook,
                                        self.exitStickerBook,
                                        ['walk', 'DFA', 'TFA',
                                         # You can get to all of these by jumping over 
                                         # the trigger then opening your book
                                         'trolley', 'final',
                                         'doorOut', 'quest',
                                         'purchase', 'stopped',
                                         'fishing', 'trialerFA',
                                         ]),
                            State.State('sit',
                                        self.enterSit,
                                        self.exitSit,
                                        ['walk',
                                         'DFA', # So you can teleport to a friend
                                         'trialerFA',
                                         ]),
                            State.State('drive',
                                        self.enterDrive,
                                        self.exitDrive,
                                        ['walk',
                                         'DFA', # So you can teleport to a friend
                                         'trialerFA',
                                         ]),
                            State.State('trolley',
                                        self.enterTrolley,
                                        self.exitTrolley,
                                        ['walk']),
                            State.State('doorIn',
                                        self.enterDoorIn,
                                        self.exitDoorIn,
                                        ['walk']),
                            State.State('doorOut',
                                        self.enterDoorOut,
                                        self.exitDoorOut,
                                        ['walk']), # 'final'
                            # Tutorial Force Acknowledge:
                            State.State('TFA',
                                        self.enterTFA,
                                        self.exitTFA,
                                        ['TFAReject', 'DFA']),
                            State.State('TFAReject',
                                        self.enterTFAReject,
                                        self.exitTFAReject,
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
                                        ['DFAReject', 'NPCFA', 'HFA']),
                            State.State('DFAReject',
                                        self.enterDFAReject,
                                        self.exitDFAReject,
                                        ['walk']),
                            # NPC Force Acknowledge:
                            State.State('NPCFA',
                                        self.enterNPCFA,
                                        self.exitNPCFA,
                                        ['NPCFAReject', 'HFA']),
                            State.State('NPCFAReject',
                                        self.enterNPCFAReject,
                                        self.exitNPCFAReject,
                                        ['walk']),
                            # Health Force Acknowledge
                            State.State('HFA',
                                        self.enterHFA,
                                        self.exitHFA,
                                        ['HFAReject', 'teleportOut', 'tunnelOut']),
                            State.State('HFAReject',
                                        self.enterHFAReject,
                                        self.exitHFAReject,
                                        ['walk']),
                            State.State('deathAck',
                                        self.enterDeathAck,
                                        self.exitDeathAck,
                                        ['teleportIn']),
                            State.State('teleportIn',
                                        self.enterTeleportIn,
                                        self.exitTeleportIn,
                                        ['walk', 'popup']),
                            State.State('popup',
                                        self.enterPopup,
                                        self.exitPopup,
                                        ['walk']),
                            State.State('teleportOut',
                                        self.enterTeleportOut,
                                        self.exitTeleportOut,
                                        ['deathAck', 'teleportIn']), # 'final'
                            State.State('died', # No transitions to "died" in the playground.
                                        self.enterDied,
                                        self.exitDied,
                                        ['final']),
                            State.State('tunnelIn',
                                        self.enterTunnelIn,
                                        self.exitTunnelIn,
                                        ['walk']),
                            State.State('tunnelOut',
                                        self.enterTunnelOut,
                                        self.exitTunnelOut,
                                        ['final']),
                            State.State('quest',
                                        self.enterQuest,
                                        self.exitQuest,
                                        ['walk']),
                            State.State('purchase',
                                        self.enterPurchase,
                                        self.exitPurchase,
                                        ['walk']),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk']),
                            State.State('fishing',
                                        self.enterFishing,
                                        self.exitFishing,
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
        self.trolleyDoneEvent = "trolleyDone"
        self.hfaDoneEvent = "hfaDoneEvent"
        self.npcfaDoneEvent = "npcfaDoneEvent"
        self.dialog = None
        self.deathAckBox = None
        
    def enter(self, requestStatus):
        assert(self.notify.debug("enter(requestStatus="+str(requestStatus)+")"))
        self.fsm.enterInitialState()
        # Let the safe zone manager know that we are here.
        messenger.send("enterPlayground")
        self.accept("doorDoneEvent", self.handleDoorDoneEvent)
        self.accept("DistributedDoor_doorTrigger", self.handleDoorTrigger)
        # Play music
        base.playMusic(self.loader.music, looping = 1, volume = 0.8)

        self.loader.geom.reparentTo(render)

        # Turn on the animated props once since there is only one zone
        for i in self.loader.nodeList:
            self.loader.enterAnimatedProps(i)

        # For halloween
        def __lightDecorationOn__():
            geom = base.cr.playGame.hood.loader.geom
            self.loader.hood.halloweenLights  = geom.findAllMatches("**/*light*")
            self.loader.hood.halloweenLights += geom.findAllMatches("**/*lamp*")
            self.loader.hood.halloweenLights += geom.findAllMatches("**/prop_snow_tree*")

            for light in self.loader.hood.halloweenLights:
                #light.reparentTo(render)
                light.setColorScaleOff(0)

        newsManager = base.cr.newsManager
        
        if newsManager:
            holidayIds = base.cr.newsManager.getDecorationHolidayId()
            if (ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds) and self.loader.hood.spookySkyFile:
                
                lightsOff = Sequence(LerpColorScaleInterval(
                    base.cr.playGame.hood.loader.geom,
                    0.1,
                    Vec4(0.55, 0.55, 0.65, 1)),
                    Func(self.loader.hood.startSpookySky),
                    Func(__lightDecorationOn__),
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

        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(1)

        self.zoneId = requestStatus["zoneId"]

        # Add hooks for the linktunnels
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.loader.nodeList, self.zoneId)

        how=requestStatus["how"]
        if how=="teleportIn":
            how="deathAck"
        self.fsm.request(how, [requestStatus])

    def exit(self):
        assert(self.notify.debug("exit()"))
        self.ignoreAll()
        # Let the safe zone manager know that we are leaving
        messenger.send("exitPlayground")
        
        for node in self.tunnelOriginList:
            node.removeNode()
        del self.tunnelOriginList

        # remove the healing task
        # taskName = base.localAvatar.taskName("healToon")
        # taskMgr.remove(taskName)
        self.loader.geom.reparentTo(hidden)
        
        # For halloween
        def __lightDecorationOff__():
            for light in self.loader.hood.halloweenLights:
                light.reparentTo(hidden)
        
        newsManager = base.cr.newsManager
##        if newsManager:
##            holidayIds = base.cr.newsManager.getDecorationHolidayId()
##            if (ToontownGlobals.HALLOWEEN_COSTUMES in holidayIds) and self.loader.hood.spookySkyFile:
##                __lightDecorationOff__()

##        # If the lights had been reparented to render then delete them
##        for light in self.loader.hood.halloweenLights:
##            light.removeNode()
##            del light

        # Turn off the little red arrows.
        NametagGlobals.setMasterArrowsOn(0)

        # Turn off the animated props once since there is only one zone
        for i in self.loader.nodeList:
            self.loader.exitAnimatedProps(i)

        # Turn the sky off
        self.loader.hood.stopSky()
        # Stop music
        self.loader.music.stop()

    def load(self):
        assert(self.notify.debug("load()"))
        # Call up the chain
        Place.Place.load(self)
        self.parentFSM.getStateNamed("playground").addChild(self.fsm)

    def unload(self):
        assert(self.notify.debug("unload()"))

        self.parentFSM.getStateNamed("playground").removeChild(self.fsm)
        del self.parentFSM
        del self.fsm

        # remove any dfa dialogs
        if self.dialog:
            self.dialog.cleanup()
            self.dialog = None
        if self.deathAckBox:
            self.deathAckBox.cleanup()
            self.deathAckBox = None
        TTDialog.cleanupDialog("globalDialog")
        self.ignoreAll()

        # Call up the chain
        Place.Place.unload(self)

    if 0:
        def handleDoorTrigger(self):
            assert(self.notify.debug("handleDoorTrigger()"))
            self.requestLeave({
                "how":"doorIn",
                #"hoodId":self.hoodId,
                #"zoneId":self.zoenId,
                })

    def showTreasurePoints(self, points):
        # Reveals all the treasure points in the given point list (a
        # list of 3-tuples) by putting a big number there.  This is a
        # handy tool for debugging the treasure points set up in
        # *TreasurePlannerAI.py.
        self.hideDebugPointText()
        for i in range(len(points)):
            p = points[i]
            self.showDebugPointText(str(i), p)

    def showDropPoints(self, points):
        # Reveals all of the drop points (where a toon enters the
        # safezone) in the given point list (a list of 6-tuples,
        # defined in HoodMgr.py).
        self.hideDebugPointText()
        for i in range(len(points)):
            p = points[i]
            self.showDebugPointText(str(i), p)

    def showPaths(self):
        # To be overridden by derived classes to fill in the correct
        # parameters for showPathPoints().
        pass

    def hidePaths(self):
        # Undoes a previous call to showPaths().
        self.hideDebugPointText()

    def showPathPoints(self, paths, waypoints = None):
        # Reveals all of the char path points (where the neighborhood
        # char walks around the safezone) in the given paths and
        # waypoints lists (defined in CCharPaths.py).
        
        self.hideDebugPointText()
        lines = LineSegs()
        lines.setColor(1, 0, 0, 1)

        from toontown.classicchars import CCharPaths

        for name, pointDef in paths.items():
            self.showDebugPointText(name, pointDef[0])

            # Also draw the connecting lines.
            for connectTo in pointDef[1]:
                toDef = paths[connectTo]
                fromP = pointDef[0]
                toP = toDef[0]
                lines.moveTo(fromP[0], fromP[1], fromP[2] + 2.0)

                wpList = CCharPaths.getWayPoints(name, connectTo, paths, waypoints)
                for wp in wpList:
                    lines.drawTo(wp[0], wp[1], wp[2] + 2.0)
                    self.showDebugPointText('*', wp)

                lines.drawTo(toP[0], toP[1], toP[2] + 2.0)

        self.debugText.attachNewNode(lines.create())

    def hideDebugPointText(self):
        # Hides all text previously created by showDebugPointText().
        if hasattr(self, "debugText"):
            children = self.debugText.getChildren()
            for i in range(children.getNumPaths()):
                children[i].removeNode()

    def showDebugPointText(self, text, point):
        # Puts a little text object at the indicated point (defined by
        # a 3-tuple) in the safezone, for debugging drop points,
        # treasure points, char path points, etc.
        if not hasattr(self, "debugText"):
            self.debugText = self.loader.geom.attachNewNode('debugText')
            self.debugTextNode = TextNode('debugTextNode')
            self.debugTextNode.setTextColor(1, 0, 0, 1)
            self.debugTextNode.setAlign(TextNode.ACenter)
            self.debugTextNode.setFont(ToontownGlobals.getSignFont())

        self.debugTextNode.setText(text)
        np = self.debugText.attachNewNode(self.debugTextNode.generate())
        np.setPos(point[0], point[1], point[2])
        np.setScale(4.0)
        np.setBillboardPointEye()
        
    # walk state inherited from Place.py

    # sticker book state inherited from Place.py

    # sit state inherited from Place.py
    
    # drive state inherited from Place.py

    # Trolley state
    def enterTrolley(self):
        assert(self.notify.debug("enterTrolley()"))
        # Turn on the laff meter
        base.localAvatar.laffMeter.start()

        # clear the anim state
        base.localAvatar.b_setAnimState("off", 1)

        # Disable leave to pay / set parent password
        base.localAvatar.cantLeaveGame = 1

        self.accept(self.trolleyDoneEvent, self.handleTrolleyDone)
        self.trolley = Trolley.Trolley(self, self.fsm, self.trolleyDoneEvent)
        self.trolley.load()
        self.trolley.enter()

    def exitTrolley(self):
        assert(self.notify.debug("exitTrolley()"))

        # Turn off the laff meter
        base.localAvatar.laffMeter.stop()        
        base.localAvatar.cantLeaveGame = 0
        
        self.ignore(self.trolleyDoneEvent)
        self.trolley.unload()
        self.trolley.exit()
        del self.trolley

    def detectedTrolleyCollision(self):
        assert(self.notify.debug("detectedTrolleyCollision()"))
        self.fsm.request("trolley")

    def handleTrolleyDone(self, doneStatus):
        assert(self.notify.debug("handleTrolleyDone()"))
        self.notify.debug("handling trolley done event")
        mode = doneStatus["mode"]
        if mode == "reject":
            self.fsm.request("walk")
        elif mode == "exit":
            self.fsm.request("walk")
        elif mode == "minigame":
            self.doneStatus = {"loader" : "minigame",
                               "where" : "minigame",
                               "hoodId" : self.loader.hood.id,
                               "zoneId" : doneStatus["zoneId"],
                               "shardId" : None,
                               "minigameId" : doneStatus["minigameId"]
                               }
            messenger.send(self.doneEvent)
        else:
            self.notify.error("Unknown mode: " + mode + " in handleTrolleyDone")

    # this is a debug function for starting up a minigame
    # see MinigameDebug.py
    def debugStartMinigame(self, zoneId, minigameId):
        assert(self.notify.debug("debugStartMinigame()"))
        self.doneStatus = {"loader" : "minigame",
                           "where" : "minigame",
                           "hoodId" : self.loader.hood.id,
                           "zoneId" : zoneId,
                           "shardId" : None,
                           "minigameId" : minigameId}
        messenger.send(self.doneEvent)

    # tunnel dfa state functions inherited from Place.py
    # tunnel dfa reject state inherited from Place.py

    def enterTFACallback(self, requestStatus, doneStatus):
        assert(self.notify.debug("enterTFACallback()"))
        self.tfa.exit()
        del self.tfa
        doneStatusMode = doneStatus["mode"]
        if (doneStatusMode == "complete"):
            self.requestLeave(requestStatus)
        elif (doneStatusMode == "incomplete"):
            self.fsm.request("TFAReject")
        else:
            self.notify.error("Unknown mode: %s" % doneStatusMode)
        return
        
    def enterDFACallback(self, requestStatus, doneStatus):
        """
        Download Force Acknowledge
        This function overrides Place.py because from the safe zone we need to
        check your health before letting you into the tunnel. So if the download
        force acknowledge says we can go, request the HFA state next.
        """
        assert(self.notify.debug("enterDFACallback()"))
        self.dfa.exit()
        del self.dfa
        # Check the status from the dfa
        # If the download force acknowledge tells us the download is complete, then
        # we can enter the tunnel, otherwise for now we just stand there
        ds = doneStatus['mode']
        if (ds == 'complete'):
            # Allowed, check your quests
            # We no longer need the NPCFA with the new tutorial
            self.fsm.request("NPCFA", [requestStatus])
            # Skip straight to the HFA
            #self.fsm.request("HFA", [requestStatus])
        # Rejected
        elif (ds == 'incomplete'):
            self.fsm.request("DFAReject")
        else:
            # Some return code that is not handled
            self.notify.error("Unknown done status for DownloadForceAcknowledge: "
                              + `doneStatus`)
        
    # door state inherited from Place.py
        
    # HFA state

    def enterHFA(self, requestStatus):
        """Hit Point Force Acknowledge"""
        assert(self.notify.debug("enterHFA()"))
        self.acceptOnce(self.hfaDoneEvent, self.enterHFACallback, [requestStatus])
        # Make sure we have enough HP to leave the safe zone
        # This enforces the so-called time out penalty
        self.hfa = HealthForceAcknowledge.HealthForceAcknowledge(self.hfaDoneEvent)
        self.hfa.enter(1)
        
    def exitHFA(self):
        assert(self.notify.debug("exitHFA()"))
        self.ignore(self.hfaDoneEvent)
            
    def enterHFACallback(self, requestStatus, doneStatus):
        assert(self.notify.debug("enterHFACallback()"))
        self.hfa.exit()
        del self.hfa
        # Check the status from the hfa
        # If the health force acknowledge tells us we're healthy, then
        # we can enter the tunnel, otherwise for now we just stand there
        if (doneStatus["mode"] == "complete"):
            # Allowed, do the tunnel transition
            # Check to see if this is a partyHat transition.  You enter a party
            # hat tunnel but you teleport in to the party grounds
            if requestStatus.get( "partyHat", 0 ):
                outHow = {"teleportIn":"tunnelOut" }
            else:
                outHow={"teleportIn":"teleportOut", "tunnelIn":"tunnelOut", "doorIn":"doorOut"}
            self.fsm.request(outHow[requestStatus["how"]], [requestStatus])
        # Rejected
        elif (doneStatus["mode"] == 'incomplete'):
            self.fsm.request("HFAReject")
        else:
            # Some return code that is not handled
            self.notify.error("Unknown done status for HealthForceAcknowledge: "
                              + `doneStatus`)

    # hfa reject state

    def enterHFAReject(self):
        assert(self.notify.debug("enterHFAReject()"))
        # TODO: reject movie, turn toon around
        self.fsm.request("walk")
    
    def exitHFAReject(self):
        assert(self.notify.debug("exitHFAReject()"))


    # NPCFA state

    def enterNPCFA(self, requestStatus):
        """NPC Force Acknowledge"""
        assert(self.notify.debug("enterNPCFA()"))

        self.acceptOnce(self.npcfaDoneEvent, self.enterNPCFACallback, [requestStatus])
        # Make sure we have enough HP to leave the safe zone
        # This enforces the so-called time out penalty
        self.npcfa = NPCForceAcknowledge.NPCForceAcknowledge(self.npcfaDoneEvent)
        self.npcfa.enter()
        
    def exitNPCFA(self):
        assert(self.notify.debug("exitNPCFA()"))
        self.ignore(self.npcfaDoneEvent)
            
    def enterNPCFACallback(self, requestStatus, doneStatus):
        assert(self.notify.debug("enterNPCFACallback()"))
        self.npcfa.exit()
        del self.npcfa
        # Check the status from the fda
        # If the download force acknowledge tells us the download is complete, then
        # we can enter the tunnel, otherwise for now we just stand there
        # Allowed, do the tunnel transition
        if (doneStatus["mode"] == "complete"):
            # Allowed, check your health
            self.fsm.request("HFA", [requestStatus])
        # Rejected
        elif (doneStatus["mode"] == 'incomplete'):
            self.fsm.request("NPCFAReject")
        else:
            # Some return code that is not handled
            self.notify.error("Unknown done status for NPCForceAcknowledge: "
                              + `doneStatus`)

    # npca reject state

    def enterNPCFAReject(self):
        assert(self.notify.debug("enterNPCFAReject()"))
        # TODO: reject movie, turn toon around
        self.fsm.request("walk")
    
    def exitNPCFAReject(self):
        assert(self.notify.debug("exitNPCFAReject()"))


    def enterWalk(self, teleportIn=0):
        if self.deathAckBox:
            self.ignore("deathAck")
            self.deathAckBox.cleanup()
            self.deathAckBox = None

        Place.Place.enterWalk(self, teleportIn)

    # deathAck state

    def enterDeathAck(self, requestStatus):
        assert(self.notify.debug("enterDeathAck()"))
        self.deathAckBox = None
        # If you are dead, let the player know.
        #if base.localAvatar.hp < 1:
        #    self.accept("deathAck", self.__handleDeathAck,
        #                extraArgs=[requestStatus])
        #    self.deathAckBox = DeathForceAcknowledge.DeathForceAcknowledge(
        #        doneEvent = "deathAck")
        #else:
        #    self.fsm.request("teleportIn", [requestStatus])
        self.fsm.request("teleportIn", [requestStatus])

    #def __handleDeathAck(self, requestStatus):
    #    assert(self.notify.debug("__handleDeathAck()"))
    #    self.fsm.request("teleportIn", [requestStatus])

    def exitDeathAck(self):
        assert(self.notify.debug("exitDeathAck()"))
        if self.deathAckBox:
            self.ignore("deathAck")
            self.deathAckBox.cleanup()
            self.deathAckBox = None

    # teleport in state

    def enterTeleportIn(self, requestStatus):
        assert(self.notify.debug("enterTeleportIn()"))
        imgScale = 0.25

        # see if someone else is already showing a dialog
        if self.dialog:
            x,y,z,h,p,r = base.cr.hoodMgr.getPlaygroundCenterFromId(self.loader.hood.id)

        # See if we're sad
        elif (base.localAvatar.hp < 1):
            requestStatus['nextState'] = 'popup'
            x,y,z,h,p,r = base.cr.hoodMgr.getPlaygroundCenterFromId(self.loader.hood.id)
            self.accept("deathAck", self.__handleDeathAck, extraArgs=[requestStatus])
            self.deathAckBox = DeathForceAcknowledge.DeathForceAcknowledge(doneEvent = "deathAck")
            
        # Check to see if the toon has a tier zero quest
        elif ((base.localAvatar.hp > 0) and
            ((Quests.avatarHasTrolleyQuest(base.localAvatar)) or
            (Quests.avatarHasFirstCogQuest(base.localAvatar)) or
            (Quests.avatarHasFriendQuest(base.localAvatar)) or
            ((Quests.avatarHasPhoneQuest(base.localAvatar)) and
             (Quests.avatarHasCompletedPhoneQuest(base.localAvatar)))) and
            (self.loader.hood.id == ToontownGlobals.ToontownCentral)):
            requestStatus['nextState'] = 'popup'
            imageModel = loader.loadModel("phase_4/models/gui/tfa_images")
            # trolley quest
            if (base.localAvatar.quests[0][0] == Quests.TROLLEY_QUEST_ID):
                if not Quests.avatarHasCompletedTrolleyQuest(base.localAvatar):
                    x,y,z,h,p,r = base.cr.hoodMgr.getDropPoint(
                        base.cr.hoodMgr.ToontownCentralInitialDropPoints)
                    msg = TTLocalizer.NPCForceAcknowledgeMessage3
                    imgNodePath = imageModel.find("**/trolley-dialog-image")
                    imgPos = (0, 0, 0.04)
                    imgScale = 0.5
                else:
                    x,y,z,h,p,r = base.cr.hoodMgr.getDropPoint(
                        base.cr.hoodMgr.ToontownCentralHQDropPoints) 
                    msg = TTLocalizer.NPCForceAcknowledgeMessage4
                    imgNodePath = imageModel.find("**/hq-dialog-image")
                    imgPos = (0, 0, -0.02)
                    imgScale = 0.5
            # first cog quest
            elif (base.localAvatar.quests[0][0] == Quests.FIRST_COG_QUEST_ID):
                if not Quests.avatarHasCompletedFirstCogQuest(base.localAvatar):
                    x,y,z,h,p,r = base.cr.hoodMgr.getDropPoint(
                        base.cr.hoodMgr.ToontownCentralTunnelDropPoints)
                    msg = TTLocalizer.NPCForceAcknowledgeMessage5
                    imgNodePath = imageModel.find("**/tunnelSignA")
                    imgPos = (0, 0, 0.04)
                    imgScale = 0.5
                else:
                    x,y,z,h,p,r = base.cr.hoodMgr.getDropPoint(
                        base.cr.hoodMgr.ToontownCentralHQDropPoints) 
                    msg = TTLocalizer.NPCForceAcknowledgeMessage6
                    imgNodePath = imageModel.find("**/hq-dialog-image")
                    imgPos = (0, 0, 0.05)
                    imgScale = 0.5
            # make a friend quest                    
            elif (base.localAvatar.quests[0][0] == Quests.FRIEND_QUEST_ID):
                if not Quests.avatarHasCompletedFriendQuest(base.localAvatar):
                    x,y,z,h,p,r = base.cr.hoodMgr.getDropPoint(
                        base.cr.hoodMgr.ToontownCentralInitialDropPoints)
                    msg = TTLocalizer.NPCForceAcknowledgeMessage7
                    gui = loader.loadModel("phase_3.5/models/gui/friendslist_gui")
                    imgNodePath = gui.find("**/FriendsBox_Closed")
                    imgPos = (0, 0, 0.04)
                    imgScale = 1.0
                    gui.removeNode()
                else:
                    x,y,z,h,p,r = base.cr.hoodMgr.getDropPoint(
                        base.cr.hoodMgr.ToontownCentralHQDropPoints) 
                    msg = TTLocalizer.NPCForceAcknowledgeMessage8
                    imgNodePath = imageModel.find("**/hq-dialog-image")
                    imgPos = (0, 0, 0.05)
                    imgScale = 0.5
            # phone quest
            elif (base.localAvatar.quests[0][0] == Quests.PHONE_QUEST_ID):
                if Quests.avatarHasCompletedPhoneQuest(base.localAvatar):
                    x,y,z,h,p,r = base.cr.hoodMgr.getDropPoint(
                        base.cr.hoodMgr.ToontownCentralHQDropPoints) 
                    msg = TTLocalizer.NPCForceAcknowledgeMessage9
                    imgNodePath = imageModel.find("**/hq-dialog-image")
                    imgPos = (0, 0, 0.05)
                    imgScale = 0.5
            
            self.dialog = TTDialog.TTDialog(
                text = msg,
                command = self.__cleanupDialog,
                style = TTDialog.Acknowledge)
            imgLabel = DirectLabel.DirectLabel(
                parent = self.dialog,
                relief = None,
                pos = imgPos,
                scale = TTLocalizer.PimgLabel,
                image = imgNodePath,
                image_scale = imgScale)
            imageModel.removeNode()
        else:
            # ...this toon has completed their trolley quest.
            # Choose a random location within the safezone to drop you.
            # We do this even if we plan to be teleporting to a toon,
            # because the gotoToon option may fail if the toon has moved
            # on.
            requestStatus['nextState'] = 'walk'
            x,y,z,h,p,r = base.cr.hoodMgr.getPlaygroundCenterFromId(
                self.loader.hood.id)

        # toon may not be parented to hidden at this point, if say the boat or piano
        # on-floor event has detected an intersection (which seems to occur when Toon
        # who lost a connection in battle re-enters in melodyland).  In that case,
        # it would be parented to the moving platform, and for that case the coords below
        # are wrong, so before doing a setPos, reparent to hidden.
        base.localAvatar.detachNode()
        base.localAvatar.setPosHpr(render, x,y,z,h,p,r)

        Place.Place.enterTeleportIn(self, requestStatus)

    def __cleanupDialog(self, value):
        if (self.dialog):
            self.dialog.cleanup()
            self.dialog = None
        if hasattr(self, "fsm"):
            self.fsm.request('walk', [1])

    def __handleDeathAck(self, requestStatus):
        assert(self.notify.debug("__handleDeathAck()"))
        if self.deathAckBox:
            self.ignore("deathAck")
            self.deathAckBox.cleanup()
            self.deathAckBox = None
        self.fsm.request('walk', [1])

    # popup state

    def enterPopup(self, teleportIn=0):
        if (base.localAvatar.hp < 1):
            base.localAvatar.b_setAnimState("Sad", 1)
        else:
            base.localAvatar.b_setAnimState("neutral", 1.0)
        self.accept("teleportQuery", self.handleTeleportQuery)
        base.localAvatar.setTeleportAvailable(1)

        # Spawn the task that checks to see if toon has fallen asleep
        base.localAvatar.startSleepWatch(self.__handleFallingAsleepPopup)

    def exitPopup(self):
        base.localAvatar.stopSleepWatch()
        base.localAvatar.setTeleportAvailable(0)
        self.ignore("teleportQuery")

    def __handleFallingAsleepPopup(self, task):
        # Go to walk mode if we fall asleep with a popup up.
        if hasattr(self, "fsm"):
            self.fsm.request("walk")
            base.localAvatar.forceGotoSleep()
        return Task.done

    # teleport out state

    def enterTeleportOut(self, requestStatus):
        assert(self.notify.debug("enterTeleportOut()"))
        Place.Place.enterTeleportOut(self, requestStatus, 
                self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        assert(self.notify.debug("__teleportOutDone()"))
        # If we're teleporting from a safezone, we need to set the
        # activityFsm to the final state
        if (hasattr(self, 'activityFsm')):
            self.activityFsm.requestFinalState()
        hoodId = requestStatus["hoodId"]
        zoneId = requestStatus["zoneId"]
        avId = requestStatus["avId"]
        shardId = requestStatus["shardId"]
        if ((hoodId == self.loader.hood.hoodId) and (zoneId == self.loader.hood.hoodId) and (shardId == None)):
            # If you are teleporting to somebody in this safezone
            # We do not even need to set our zone because it is the same
            self.fsm.request("deathAck", [requestStatus])
        elif (hoodId == ToontownGlobals.MyEstate):
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            # Different hood or zone, exit the safe zone
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)

    def exitTeleportOut(self):
        assert(self.notify.debug("exitTeleportOut()"))
        Place.Place.exitTeleportOut(self)


    # tunnel in state inherited from Place.py
    # tunnel out state inherited from Place.py


    def createPlayground(self, dnaFile):
        assert(self.notify.debug("createPlayground()"))
        # Load the safe zone specific models and textures
        loader.loadDNAFile(self.loader.dnaStore, self.safeZoneStorageDNAFile)
        # Load the actual safe zone dna
        node = loader.loadDNAFile(self.loader.dnaStore, dnaFile)

        if node.getNumParents() == 1:
            # If the node already has a parent arc when it's loaded, we must
            # be using the level editor and we want to preserve that arc.
            self.geom = NodePath(node.getParent(0))
            self.geom.reparentTo(hidden)
        else:
            # Otherwise, we should create a new arc for the node.
            self.geom = hidden.attachNewNode(node)
        # Make the vis dictionaries
        self.makeDictionaries(self.loader.dnaStore)
        # Add hooks for the linktunnels
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.nodeList, self.zoneId)
        # Flatten the safe zone
        self.geom.flattenMedium()
        # Preload all textures in neighborhood
        gsg = base.win.getGsg()
        if gsg:
            self.geom.prepareScene(gsg)

    def makeDictionaries(self, dnaStore):
        assert(self.notify.debug("makeDictionaries()"))
        # A list of all visible nodes
        self.nodeList = []
        # There should only be one vis group
        for i in range(dnaStore.getNumDNAVisGroups()):
            groupFullName = dnaStore.getDNAVisGroupName(i)
            groupName = base.cr.hoodMgr.extractGroupName(groupFullName)
            groupNode = self.geom.find("**/" + groupFullName)
            if groupNode.isEmpty():
                self.notify.error("Could not find visgroup")
            self.nodeList.append(groupNode)
        self.removeLandmarkBlockNodes()
        # Now that we have extracted the vis groups we do not need
        # the dnaStore to keep them around
        # Remove all references to the safezone specific models and textures
        self.loader.dnaStore.resetPlaceNodes()
        self.loader.dnaStore.resetDNAGroups()
        self.loader.dnaStore.resetDNAVisGroups()
        self.loader.dnaStore.resetDNAVisGroupsAI()

    def removeLandmarkBlockNodes(self):
        """
        Since we are in the safe zone we do not need the suit_building_origins
        """
        assert(self.notify.debug("removeLandmarkBlockNodes()"))
        npc = self.geom.findAllMatches("**/suit_building_origin")
        for i in range(npc.getNumPaths()):
            npc.getPath(i).removeNode()

    def enterTFA(self, requestStatus):
        assert(self.notify.debug("enterTFA()"))
        self.acceptOnce(self.tfaDoneEvent, self.enterTFACallback,
                        [requestStatus])
        self.tfa = TutorialForceAcknowledge.TutorialForceAcknowledge(
            self.tfaDoneEvent)
        self.tfa.enter()
            
    def exitTFA(self):
        assert(self.notify.debug("exitTFA()"))
        self.ignore(self.tfaDoneEvent)

    def enterTFAReject(self):
        assert(self.notify.debug("enterTFAReject()"))
        self.fsm.request("walk")

    def exitTFAReject(self):
        assert(self.notify.debug("exitTFAReject()"))


