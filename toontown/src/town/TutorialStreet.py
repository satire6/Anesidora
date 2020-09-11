
import TTStreet

class TutorialStreet(TTStreet.TTStreet):

    # This is where the meat of the tutorial hookup code is going to go.
    # In fact, the whole state machine should probably go here.

    def enter(self, requestStatus):
        # No visibility in the tutorial, please.
        # turn arrows off, the one to flippy on the other side of HQ just confuses the user.
        # the position of the Flunky is fairly obvious
        TTStreet.TTStreet.enter(self, requestStatus, visibilityFlag=0, arrowsOn=0)

    def exit(self):
        # No visibility in the tutorial, please.
        TTStreet.TTStreet.exit(self, visibilityFlag=0)
    
    def enterTeleportIn(self, requestStatus):
        TTStreet.TTStreet.enterTeleportIn(self, requestStatus)
        # This is how the tutorial knows that the toon has arrived.
        #messenger.send("toonEntersTutorial")
        return

    def enterTownBattle(self, event):
        # Here, we explicitly do not pay attention to the invasion status
        # Let's just keep it simple and have creditMultiplier be 1.0
        # so the tutorial panels do not have to change to explain this 
        self.loader.townBattle.enter(event, self.fsm.getStateNamed("battle"),
                                     tutorialFlag=1)

    def handleEnterTunnel(self, requestStatus, collEntry):
        """
        This is an override of the version in Place.py, because
        this is how we announce we are leaving the tutorial.
        """
        messenger.send("stopTutorial")
        TTStreet.TTStreet.handleEnterTunnel(self, requestStatus, collEntry)
        return

    def exitDoorIn(self):
        """
        This is an override of the version in Place.py, because
        we want to leave arrows off
        """
        base.localAvatar.obscureMoveFurnitureButton(-1)
        
    

    
