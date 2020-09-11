
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.hood import Place
from toontown.building import Elevator
from toontown.toonbase import ToontownGlobals
from pandac.PandaModules import *

class CogHQLobby(Place.Place):
    # create a notify category
    notify = DirectNotifyGlobal.directNotify.newCategory("CogHQLobby")
    
    # special methods
    def __init__(self, hood, parentFSM, doneEvent):
        assert(self.notify.debug("__init__()"))
        Place.Place.__init__(self, hood, doneEvent)
        self.parentFSM = parentFSM
        self.elevatorDoneEvent = "elevatorDone"
        self.fsm = ClassicFSM.ClassicFSM('CogHQLobby',
                           [State.State('start',
                                        self.enterStart,
                                        self.exitStart,
                                        ['walk', 'tunnelIn', 'teleportIn', 'doorIn',
                                         ]),
                            State.State('walk',
                                        self.enterWalk,
                                        self.exitWalk,
                                        ['elevator', 'DFA', 'doorOut', 'stopped',
                                         ]),
                            State.State('stopped',
                                        self.enterStopped,
                                        self.exitStopped,
                                        ['walk', 'teleportOut', 'elevator',
                                         ]),
                            State.State('doorIn',
                                        self.enterDoorIn,
                                        self.exitDoorIn,
                                        ['walk']),
                            State.State('doorOut',
                                        self.enterDoorOut,
                                        self.exitDoorOut,
                                        ['walk']),
                            State.State('teleportIn',
                                        self.enterTeleportIn,
                                        self.exitTeleportIn,
                                        ['walk',
                                         ]),
                            State.State('elevator',
                                        self.enterElevator,
                                        self.exitElevator,
                                        ['walk', 'stopped']),
                            # Download Force Acknowledge
                            State.State('DFA',
                                        self.enterDFA,
                                        self.exitDFA,
                                        ['DFAReject']),
                            State.State('DFAReject',
                                        self.enterDFAReject,
                                        self.exitDFAReject,
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

    def load(self):
        self.parentFSM.getStateNamed("cogHQLobby").addChild(self.fsm)
        Place.Place.load(self)

    def unload(self):
        self.parentFSM.getStateNamed("cogHQLobby").removeChild(self.fsm)
        Place.Place.unload(self)
        self.fsm = None

    def enter(self, requestStatus):
        self.zoneId = requestStatus["zoneId"]
        # This will call load()
        Place.Place.enter(self)
        self.fsm.enterInitialState()
        # Play music
        base.playMusic(self.loader.music, looping = 1, volume = 0.8)
        self.loader.geom.reparentTo(render)
        self.accept("doorDoneEvent", self.handleDoorDoneEvent)
        self.accept("DistributedDoor_doorTrigger", self.handleDoorTrigger)
        # Turn on the little red arrows.
        NametagGlobals.setMasterArrowsOn(1)
        how=requestStatus["how"]
        self.fsm.request(how, [requestStatus])

    def exit(self):
        # Stop music
        self.fsm.requestFinalState()        
        self.ignoreAll()
        self.loader.music.stop()
        # MPG - this was None when the boss elevator closed!
        if (self.loader.geom != None):
            self.loader.geom.reparentTo(hidden)
        Place.Place.exit(self)

    # walk state inherited from BattlePlace.py
    # Override to disable teleport access
    def enterWalk(self, teleportIn=0):
        Place.Place.enterWalk(self, teleportIn)
        self.ignore('teleportQuery')
        base.localAvatar.setTeleportAvailable(0)

    # elevator state
    # (For boarding a building elevator)
    def enterElevator(self, distElevator, skipDFABoard = 0):
        assert(self.notify.debug("enterElevator()"))
        
        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed("elevator"),
                                          self.elevatorDoneEvent,
                                          distElevator)
        if skipDFABoard:
            self.elevator.skipDFABoard = 1
        #We've placed a reference to the elevator on the DistributedElevator Itself
        distElevator.elevatorFSM=self.elevator
        self.elevator.load()
        self.elevator.enter()

    def exitElevator(self):
        assert(self.notify.debug("exitElevator()"))
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()
        del self.elevator

    def detectedElevatorCollision(self, distElevator):
        assert(self.notify.debug("detectedElevatorCollision()"))
        self.fsm.request("elevator", [distElevator])

    def handleElevatorDone(self, doneStatus):
        assert(self.notify.debug("handleElevatorDone()"))
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
        elif (where == 'cogHQBossBattle'):
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error("Unknown mode: " + where +
                              " in handleElevatorDone")

    def enterTeleportIn(self, requestStatus):
        base.localAvatar.setPosHpr(render, 0,0,0,0,0,0)
        Place.Place.enterTeleportIn(self, requestStatus)

