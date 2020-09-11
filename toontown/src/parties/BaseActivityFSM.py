#-------------------------------------------------------------------------------
# Contact: Rob Gordon
# Created: Oct 2008
#
# Purpose: Provides base functionality that all ActivityFSMs use.
#-------------------------------------------------------------------------------

"""
Individual ActivityFSMs are expected to subclass from BaseActivityFSM and from
appropriate state mixins found in the activityGameFSMMixins module.
"""

from direct.fsm.FSM import FSM
from direct.directnotify import DirectNotifyGlobal

class BaseActivityFSM( FSM ):
    notify = DirectNotifyGlobal.directNotify.newCategory( "BaseActivityFSM" )

    def __init__( self, activity ):
        FSM.__init__( self, self.__class__.__name__ )
        self.activity = activity

        # Subclasses should modify this dictionary
        self.defaultTransitions = None