from pandac.PandaModules import *

from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from toontown.distributed.DelayDeletable import DelayDeletable
import DistributedSuitBase

class DistributedTutorialSuit(DistributedSuitBase.DistributedSuitBase, DelayDeletable):

    notify = DirectNotifyGlobal.directNotify.newCategory(
                                        'DistributedTutorialSuit')

    def __init__(self, cr):
        """__init__(cr)"""
        try:
            self.DistributedSuit_initialized
        except:
            self.DistributedSuit_initialized = 1
            DistributedSuitBase.DistributedSuitBase.__init__(self, cr)

            # Set up the DistributedSuit state machine
            self.fsm = ClassicFSM.ClassicFSM(
                'DistributedSuit',
                [State.State('Off',
                             self.enterOff,
                             self.exitOff,
                             ['Walk',
                              'Battle']),
                 State.State('Walk',
                             self.enterWalk,
                             self.exitWalk,
                             ['WaitForBattle',
                              'Battle']
                             ),
                 State.State('Battle',
                             self.enterBattle,
                             self.exitBattle,
                             []),
                 State.State('WaitForBattle',
                             self.enterWaitForBattle,
                             self.exitWaitForBattle,
                             ['Battle']),
                 ],
                        # Initial state
                        'Off',
                        # Final state
                        'Off',
                       )

            self.fsm.enterInitialState()

        return None

    def generate(self):
        DistributedSuitBase.DistributedSuitBase.generate(self)

    def announceGenerate(self):
        DistributedSuitBase.DistributedSuitBase.announceGenerate(self)
        self.setState('Walk')

    def disable(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    This method is called when the DistributedObject
        //              is removed from active duty and stored in a cache.
        // Parameters:
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.notify.debug("DistributedSuit %d: disabling" % self.getDoId())
        self.setState('Off')
        DistributedSuitBase.DistributedSuitBase.disable(self)
        return

    def delete(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    This method is called when the DistributedObject is
        //              permanently removed from the world and deleted from
        //              the cache.
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        try:
            self.DistributedSuit_deleted
        except:
            self.DistributedSuit_deleted = 1
            self.notify.debug("DistributedSuit %d: deleting" % self.getDoId())

            del self.fsm
            DistributedSuitBase.DistributedSuitBase.delete(self)
        return

    def d_requestBattle(self, pos, hpr):
        """d_requestBattle(toonId)
        """
        # Make sure the local toon can't continue to run around (and
        # potentially start battles with other suits!)
        self.cr.playGame.getPlace().setState('WaitForBattle')
        self.sendUpdate('requestBattle', [pos[0], pos[1], pos[2],
                                          hpr[0], hpr[1], hpr[2]])
        return None

    def __handleToonCollision(self, collEntry):
        """
        /////////////////////////////////////////////////////////////
        // Function:    This function is the callback for any
        //              collision events that the collision sphere
        //              for this bad guy might receive
        // Parameters:  collEntry, the collision entry object
        // Changes:     None
        /////////////////////////////////////////////////////////////
        """

        toonId = base.localAvatar.getDoId()
        self.notify.debug('Distributed suit: requesting a Battle with ' +
                           'toon: %d' % toonId)
        self.d_requestBattle(self.getPos(), self.getHpr())

        # the suit on this machine only will go into wait for battle while it
        # is waiting for word back from the server about our battle request
        #
        self.setState('WaitForBattle')

        return None


    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### Off state #####

    # Defined in DistributedSuitBase.py

    ##### Walk state #####

    def enterWalk(self):
        self.enableBattleDetect('walk', self.__handleToonCollision)
        # Just stand here waiting for a toon to approach.
        self.loop('walk', 0)
        # This is the path that the tutorial suit walks along.
        # There is a path in the tutorial DNA file that is not used so make sure
        # the path gets changed here.
        pathPoints = [Vec3(55, 15, -0.5),
                      Vec3(55, 25, -0.5),
                      Vec3(25, 25, -0.5),
                      Vec3(25, 15, -0.5),
                      Vec3(55, 15, -0.5),
                      ]
        self.tutWalkTrack = self.makePathTrack(self, pathPoints,
                                               4.5, "tutFlunkyWalk")
        self.tutWalkTrack.loop()

    def exitWalk(self):
        self.disableBattleDetect()
        self.tutWalkTrack.pause()
        self.tutWalkTrack = None
        return

    ##### Battle state #####

    # Defined in DistributedSuitBase.py

    ##### WaitForBattle state #####

    # Defined in DistributedSuitBase.py
