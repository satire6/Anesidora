from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.fsm import StateData
from toontown.toontowngui import TTDialog
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class Trolley(StateData.StateData):
    def __init__(self, safeZone, parentFSM, doneEvent):

        StateData.StateData.__init__(self, doneEvent)

        self.fsm = ClassicFSM.ClassicFSM('Trolley',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['requestBoard',
                                         'trolleyHFA',
                                         'trolleyTFA']),
                            State.State('trolleyHFA',
                                        self.enterTrolleyHFA,
                                        self.exitTrolleyHFA,
                                        ['final',
                                         ]),
                            State.State('trolleyTFA',
                                        self.enterTrolleyTFA,
                                        self.exitTrolleyTFA,
                                        ['final',
                                         ]),
                            State.State('requestBoard',
                                        self.enterRequestBoard,
                                        self.exitRequestBoard,
                                        ['boarding']),
                            State.State('boarding',
                                        self.enterBoarding,
                                        self.exitBoarding,
                                        ['boarded']),
                            State.State('boarded',
                                        self.enterBoarded,
                                        self.exitBoarded,
                                        ['requestExit',
                                         'trolleyLeaving',
                                         'final']),
                            State.State('requestExit',
                                        self.enterRequestExit,
                                        self.exitRequestExit,
                                        ['exiting', 'trolleyLeaving']),
                            State.State('trolleyLeaving',
                                        self.enterTrolleyLeaving,
                                        self.exitTrolleyLeaving,
                                        ['final']),
                            State.State('exiting',
                                        self.enterExiting,
                                        self.exitExiting,
                                        ['final']),
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

        return None

    def load(self):
        self.parentFSM.getStateNamed("trolley").addChild(self.fsm)
        self.buttonModels = loader.loadModel("phase_3.5/models/gui/inventory_gui")
        self.upButton = self.buttonModels.find("**//InventoryButtonUp")
        self.downButton = self.buttonModels.find("**/InventoryButtonDown")
        self.rolloverButton = self.buttonModels.find(
            "**/InventoryButtonRollover")
        return
    
    def unload(self):
        self.parentFSM.getStateNamed("trolley").removeChild(self.fsm)
        del self.fsm
        del self.parentFSM
        self.buttonModels.removeNode()
        del self.buttonModels
        del self.upButton
        del self.downButton
        del self.rolloverButton
        return
        
    def enter(self):
        """enter(self)
        """
        self.fsm.enterInitialState()
        if base.localAvatar.hp > 0:
            # let the distributed trolley know it is
            # ok for us to enter the trolley
            messenger.send('enterTrolleyOK')
            self.fsm.request("requestBoard")
        else:
            # can't board if we are 'sad'
            self.fsm.request("trolleyHFA")
        return None

    def exit(self):
        self.ignoreAll()
        return None

    def enterStart(self):
        return None

    def exitStart(self):
        return None

    def enterTrolleyHFA(self):
        self.noTrolleyBox = TTDialog.TTGlobalDialog(
            message = TTLocalizer.TrolleyHFAMessage,
            doneEvent = "noTrolleyAck",
            style = TTDialog.Acknowledge)
        self.noTrolleyBox.show()
        base.localAvatar.b_setAnimState("neutral", 1)
        self.accept("noTrolleyAck", self.__handleNoTrolleyAck)
        return

    def exitTrolleyHFA(self):
        self.ignore("noTrolleyAck")
        self.noTrolleyBox.cleanup()
        del self.noTrolleyBox
        return

    def enterTrolleyTFA(self):
        self.noTrolleyBox = TTDialog.TTGlobalDialog(
            message = TTLocalizer.TrolleyTFAMessage,
            doneEvent = "noTrolleyAck",
            style = TTDialog.Acknowledge)
        self.noTrolleyBox.show()
        base.localAvatar.b_setAnimState("neutral", 1)
        self.accept("noTrolleyAck", self.__handleNoTrolleyAck)
        return

    def exitTrolleyTFA(self):
        self.ignore("noTrolleyAck")
        self.noTrolleyBox.cleanup()
        del self.noTrolleyBox
        return

    def __handleNoTrolleyAck(self):
        ntbDoneStatus = self.noTrolleyBox.doneStatus
        if ntbDoneStatus == "ok":
            doneStatus = {}
            doneStatus["mode"] = "reject"
            messenger.send(self.doneEvent, [doneStatus])
        else:
            self.notify.error("Unrecognized doneStatus: " + str(ntbDoneStatus))
        return

    def enterRequestBoard(self):
        return None

    def handleRejectBoard(self):
        doneStatus = {}
        doneStatus["mode"] = "reject"
        messenger.send(self.doneEvent, [doneStatus])

    def exitRequestBoard(self):
        return None

    def enterBoarding(self, nodePath):
        camera.wrtReparentTo(nodePath)
        self.cameraBoardTrack = LerpPosHprInterval(camera, 1.5,
                                                   Point3(-35, 0, 8),
                                                   Point3(-90, 0, 0))
        
        self.cameraBoardTrack.start()
        return None

    def exitBoarding(self):
        self.ignore("boardedTrolley")
        return None

    def enterBoarded(self):
        self.enableExitButton()
        return None

    def exitBoarded(self):
        # Remove the boarding task... You might think this should be
        # removed in exitBoarding, but we want the camera move to continue
        # into the boarded state. Since boarding only goes directly into
        # boarded state, it's okay. Probably boarding and boarded should
        # be the same state.
        self.cameraBoardTrack.finish()
        self.disableExitButton()
        return None

    def enableExitButton(self):
        self.exitButton = DirectButton(
            relief = None,
            text = TTLocalizer.TrolleyHopOff,
            text_fg = (1, 1, 0.65, 1),
            text_pos = (0, -0.23),
            text_scale = TTLocalizer.TtrolleyHopOff,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (1, 0, 0, 1),
            image_scale = (20, 1, 11),
            pos = (0, 0, 0.8),
            scale = 0.15,
            command = lambda self=self: self.fsm.request("requestExit"),
            )
        return

    def disableExitButton(self):
        self.exitButton.destroy()
        return

    def enterRequestExit(self):
        messenger.send("trolleyExitButton")
        return None

    def exitRequestExit(self):
        return None

    def enterTrolleyLeaving(self):
        # A camera move
        camera.lerpPosHprXYZHPR(0, 18.55, 3.75, -180, 0, 0, 3,
                                blendType = "easeInOut", task="leavingCamera")
        self.acceptOnce("playMinigame", self.handlePlayMinigame)
        return None

    def handlePlayMinigame(self, zoneId, minigameId):
        base.localAvatar.b_setParent(ToontownGlobals.SPHidden)
        doneStatus = {}
        doneStatus["mode"] = "minigame"
        doneStatus["zoneId"] = zoneId
        doneStatus["minigameId"] = minigameId
        messenger.send(self.doneEvent, [doneStatus])

    def exitTrolleyLeaving(self):
        self.ignore("playMinigame")
        taskMgr.remove("leavingCamera")
        return None

    def enterExiting(self):
        return None

    def handleOffTrolley(self):
        doneStatus = {}
        doneStatus["mode"] = "exit"
        messenger.send(self.doneEvent, [doneStatus])
        return None

    def exitExiting(self):
        return None

    def enterFinal(self):
        return None

    def exitFinal(self):
        return None

