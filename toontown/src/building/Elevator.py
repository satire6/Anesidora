from pandac.PandaModules import *
from toontown.toonbase.ToonBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.fsm import StateData
from toontown.launcher import DownloadForceAcknowledge
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil

class Elevator(StateData.StateData):
    def __init__(self, elevatorState, doneEvent, distElevator):

        StateData.StateData.__init__(self, doneEvent)

        self.fsm = ClassicFSM.ClassicFSM('Elevator',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['elevatorDFA',
                                         ]),
                            State.State('elevatorDFA',
                                        self.enterElevatorDFA,
                                        self.exitElevatorDFA,
                                        ['requestBoard',
                                         'final'
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
                                         'elevatorClosing',
                                         'final']),
                            State.State('requestExit',
                                        self.enterRequestExit,
                                        self.exitRequestExit,
                                        ['exiting', 'elevatorClosing']),
                            State.State('elevatorClosing',
                                        self.enterElevatorClosing,
                                        self.exitElevatorClosing,
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

        self.dfaDoneEvent = "elevatorDfaDoneEvent"
        self.elevatorState = elevatorState
        self.distElevator = distElevator
        distElevator.elevatorFSM=self
        self.reverseBoardingCamera = False
        self.skipDFABoard = 0

    def load(self):
        self.elevatorState.addChild(self.fsm)
        self.buttonModels = loader.loadModel("phase_3.5/models/gui/inventory_gui")
        self.upButton = self.buttonModels.find("**//InventoryButtonUp")
        self.downButton = self.buttonModels.find("**/InventoryButtonDown")
        self.rolloverButton = self.buttonModels.find(
            "**/InventoryButtonRollover")
    
    def unload(self):
        self.elevatorState.removeChild(self.fsm)
        self.distElevator.elevatorFSM = None # kill the loop
        del self.distElevator
        del self.fsm
        del self.elevatorState
        self.buttonModels.removeNode()
        del self.buttonModels
        del self.upButton
        del self.downButton
        del self.rolloverButton
        
    def enter(self):
        self.fsm.enterInitialState()
        self.fsm.request("elevatorDFA")

    def exit(self):
        self.ignoreAll()

    def signalDone(self, doneStatus):
        messenger.send(self.doneEvent, [doneStatus])

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def enterElevatorDFA(self):
        self.acceptOnce(self.dfaDoneEvent, self.enterDFACallback)
        self.dfa = DownloadForceAcknowledge.DownloadForceAcknowledge(
            self.dfaDoneEvent)
        # The suit interiors are download phase 7
        self.dfa.enter(7)
        return

    def enterDFACallback(self, DFAdoneStatus):
        self.dfa.exit()
        del self.dfa

        if (DFAdoneStatus["mode"] == "complete"):
            if self.skipDFABoard:
                self.skipDFABoard = 0
            else:
                self.fsm.request("requestBoard")
        elif (DFAdoneStatus["mode"] == "incomplete"):
            elevatorDoneStatus = {}
            elevatorDoneStatus["where"] = "reject"
            # Let our parent fsm know that we are done.
            messenger.send(self.doneEvent, [elevatorDoneStatus])
        else:
            self.notify.error("Unrecognized doneStatus: " + str(DFAdoneStatus))

    def exitElevatorDFA(self):
        self.ignore(self.dfaDoneEvent)

    def enterRequestBoard(self):
        # Let the distributed elevator know that it can safely make
        # the request.
        messenger.send(self.distElevator.uniqueName("enterElevatorOK"))

    def exitRequestBoard(self):
        pass

    def enterBoarding(self, nodePath):
        camera.wrtReparentTo(nodePath)        
        if self.reverseBoardingCamera:
            heading = PythonUtil.fitDestAngle2Src( camera.getH( nodePath), 180 )        
            self.cameraBoardTrack = LerpPosHprInterval(camera, 1.5,
                                                       Point3(0, 18, 8),
                                                       Point3(heading, -10, 0))
        else:
            self.cameraBoardTrack = LerpPosHprInterval(
                camera, 1.5, Point3(0, -16, 5.5), Point3(0, 0, 0))
        
        self.cameraBoardTrack.start()

    def exitBoarding(self):
        self.ignore("boardedElevator")

    def enterBoarded(self):
        self.enableExitButton()

    def exitBoarded(self):
        # Remove the boarding task... You might think this should be
        # removed in exitBoarding, but we want the camera move to continue
        # into the boarded state. Since boarding only goes directly into
        # boarded state, it's okay. Probably boarding and boarded should
        # be the same state.
        self.cameraBoardTrack.finish()
        self.disableExitButton()

    def enableExitButton(self):

        self.exitButton = DirectButton(
            relief = None,
            text = TTLocalizer.ElevatorHopOff,
            text_fg = (0.9, 0.9, 0.9, 1),
            text_pos = (0, -0.23),
            text_scale = TTLocalizer.EelevatorHopOff,
            image = (self.upButton, self.downButton, self.rolloverButton),
            image_color = (0.5, 0.5, 0.5, 1),
            image_scale = (20, 1, 11),
            pos = (0, 0, 0.8),
            scale = 0.15,
            command = lambda self=self: self.fsm.request("requestExit"),
            )
            
        if hasattr(localAvatar, "boardingParty") and \
           localAvatar.boardingParty and \
           localAvatar.boardingParty.getGroupLeader(localAvatar.doId) and \
           localAvatar.boardingParty.getGroupLeader(localAvatar.doId) != localAvatar.doId:
           
            self.exitButton['command'] = None
            self.exitButton.hide()
            
##            self.hopWarning = DirectLabel(
##                parent = self.exitButton,
##                relief = None,
##                pos = Vec3(0, 0, 0.0),
##                text = TTLocalizer.ElevatorLeaderOff,
##                text_fg = (0.9, 0.9, 0.9, 1),
##                text_pos = (0, -1.1),
##                text_scale = 0.6,
##            )
##            self.hopWarning.reparentTo(self.exitButton.stateNodePath[2])
            
        if self.distElevator.antiShuffle:
            self.hopWarning = DirectLabel(
                parent = self.exitButton,
                relief = None,
                pos = Vec3(0, 0, 0.0),
                text = TTLocalizer.ElevatorStayOff,
                text_fg = (0.9, 0.9, 0.9, 1),
                text_pos = (0, -1.1),
                text_scale = 0.6,
            )
            self.hopWarning.reparentTo(self.exitButton.stateNodePath[2])

        else:
            self.hopWarning = None 

    def disableExitButton(self):
        if self.hopWarning:
            self.hopWarning.destroy()
        self.exitButton.destroy()

    def enterRequestExit(self):
        messenger.send("elevatorExitButton")

    def exitRequestExit(self):
        pass

    def enterElevatorClosing(self):
        # A camera move
        #camera.lerpPosHprXYZHPR(0, 18.55, 3.75, -180, 0, 0, 3,
        #                       blendType = "easeInOut", task="closingCamera")
        
        # TODO: Actually go inside the building... Set doneStatus to
        # whatever is necessary to enter the building, and call the
        # done event.
        assert(self.notify.debug('enterElevatorClosing()'))

    def exitElevatorClosing(self):
        #taskMgr.remove("closingCamera")
        pass

    def enterExiting(self):
        pass

    def exitExiting(self):
        pass

    def enterFinal(self):
        assert(self.notify.debug('enterFinal()'))

    def exitFinal(self):
        pass

    def setReverseBoardingCamera(self, newVal):
        """Set the flag if True, we reverse the boarding camera."""
        self.reverseBoardingCamera = newVal
