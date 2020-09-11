#-------------------------------------------------------------------------------
# Contact: Rob Gordon
# Created: Oct 2008
#
# Purpose: This module provides mixin classes (mostly individual states) for
#          use with ActivityFSM.
#-------------------------------------------------------------------------------

"""
This module provides mixin classes (mostly individual states) for use with
ActivityFSM.  Functionality is provided in this manner to avoid massive code
duplication that would occur otherwise.
"""

# parties imports
from BaseActivityFSM import BaseActivityFSM

#--------------------------------------------------------------------------
# Idle State
#--------------------------------------------------------------------------
class IdleMixin:
    def enterIdle( self, *args ):
        BaseActivityFSM.notify.info( "enterIdle: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startIdle( *args )
        else:
            self.activity.startIdle()

    def filterIdle( self, request, args ):
        BaseActivityFSM.notify.debug( "filterIdle( '%s', '%s' )" % (request, args) )
        if request == "Idle":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitIdle( self ):
        BaseActivityFSM.notify.debug( "exitIdle: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishIdle()

#--------------------------------------------------------------------------
# Active State
#--------------------------------------------------------------------------
class ActiveMixin:
    def enterActive( self, *args ):
        BaseActivityFSM.notify.info( "enterActive: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startActive( *args )
        else:
            self.activity.startActive()

    def filterActive( self, request, args ):
        BaseActivityFSM.notify.debug( "filterActive( '%s', '%s' )" % (request, args) )
        if request == "Active":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitActive( self ):
        BaseActivityFSM.notify.debug( "exitActive: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishActive()

#--------------------------------------------------------------------------
# Disabled State
#--------------------------------------------------------------------------
class DisabledMixin:
    def enterDisabled( self, *args ):
        BaseActivityFSM.notify.info( "enterDisabled: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startDisabled( *args )
        else:
            self.activity.startDisabled()

    def filterDisabled( self, request, args ):
        BaseActivityFSM.notify.debug( "filterDisabled( '%s', '%s' )" % (request, args) )
        if request == "Disabled":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitDisabled( self ):
        BaseActivityFSM.notify.debug( "exitDisabled: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishDisabled()


#--------------------------------------------------------------------------
# Rules State
#--------------------------------------------------------------------------
class RulesMixin:
    def enterRules( self, *args ):
        BaseActivityFSM.notify.info( "enterRules: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startRules( *args )
        else:
            self.activity.startRules()
        
    def filterRules( self, request, args ):
        BaseActivityFSM.notify.debug( "filterRules( '%s', '%s' )" % (request, args) )
        if request == "Rules":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitRules( self ):
        BaseActivityFSM.notify.debug( "exitRules: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishRules()


#--------------------------------------------------------------------------
# WaitForEnough State
#--------------------------------------------------------------------------
class WaitForEnoughMixin:
    def enterWaitForEnough( self, *args ):
        BaseActivityFSM.notify.info( "enterWaitForEnough: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startWaitForEnough( *args )
        else:
            self.activity.startWaitForEnough()

    def filterWaitForEnough( self, request, args ):
        BaseActivityFSM.notify.debug( "filterWaitForEnough( '%s', '%s' )" % (request, args) )
        if request == "WaitForEnough":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitWaitForEnough( self ):
        BaseActivityFSM.notify.debug( "exitWaitForEnough: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishWaitForEnough()


#--------------------------------------------------------------------------
# WaitToStart State
#--------------------------------------------------------------------------
class WaitToStartMixin:
    def enterWaitToStart( self, *args ):
        BaseActivityFSM.notify.info( "enterWaitToStart: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startWaitToStart( *args )
        else:
            self.activity.startWaitToStart()

    def filterWaitToStart( self, request, args ):
        BaseActivityFSM.notify.debug( "filterWaitToStart( '%s', '%s' )" % (request, args) )
        if request == "WaitToStart":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitWaitToStart( self ):
        BaseActivityFSM.notify.debug( "exitWaitToStart: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishWaitToStart()


#--------------------------------------------------------------------------
# WaitClientsReady State
#--------------------------------------------------------------------------
class WaitClientsReadyMixin:
    def enterWaitClientsReady( self, *args ):
        BaseActivityFSM.notify.info( "enterWaitClientsReady: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startWaitClientsReady( *args )
        else:
            self.activity.startWaitClientsReady()

    def filterWaitClientsReady( self, request, args ):
        BaseActivityFSM.notify.debug( "filterWaitClientsReady( '%s', '%s' )" % (request, args) )
        if request == "WaitClientsReady":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitWaitClientsReady( self ):
        BaseActivityFSM.notify.debug( "exitWaitClientsReady: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishWaitClientsReady()

#--------------------------------------------------------------------------
# WaitForServer State
#--------------------------------------------------------------------------
class WaitForServerMixin:
    def enterWaitForServer( self, *args ):
        BaseActivityFSM.notify.info( "enterWaitForServer: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startWaitForServer( *args )
        else:
            self.activity.startWaitForServer()

    def filterWaitForServer( self, request, args ):
        BaseActivityFSM.notify.debug( "filterWaitForServer( '%s', '%s' )" % (request, args) )
        if request == "WaitForServer":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitWaitForServer( self ):
        BaseActivityFSM.notify.debug( "exitWaitForServer: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishWaitForServer()


#--------------------------------------------------------------------------
# Conclusion State
#--------------------------------------------------------------------------
class ConclusionMixin:
    def enterConclusion( self, *args ):
        BaseActivityFSM.notify.info( "enterConclusion: '%s' -> '%s'" % (self.oldState, self.newState) )
        if len(args) > 0:
            self.activity.startConclusion( *args )
        else:
            self.activity.startConclusion()

    def filterConclusion( self, request, args ):
        BaseActivityFSM.notify.debug( "filterConclusion( '%s', '%s' )" % (request, args) )
        if request == "Conclusion":
            return None
        else:
            return self.defaultFilter( request, args )

    def exitConclusion( self ):
        BaseActivityFSM.notify.debug( "exitConclusion: '%s' -> '%s'" % (self.oldState, self.newState) )
        self.activity.finishConclusion()

