
import Street

class DDStreet(Street.Street):
    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)

    def enter(self, requestStatus):
        # We need to do our own code here first because the act
        # of entering can actually cause a complete exit/unload
        # sequence in the case that we are teleporting to a friend
        # that is not here
        self.loader.hood.setWhiteFog()        
        Street.Street.enter(self, requestStatus)

    def exit(self):
        self.loader.hood.setNoFog()
        Street.Street.exit(self)

