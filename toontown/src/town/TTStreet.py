
import Street

class TTStreet(Street.Street):
    def __init__(self, loader, parentFSM, doneEvent):
        Street.Street.__init__(self, loader, parentFSM, doneEvent)

    def load(self):
        Street.Street.load(self)

    def unload(self):
        Street.Street.unload(self)

    def doRequestLeave(self, requestStatus):
        # when it's time to leave, check their trialer status first
        self.fsm.request('trialerFA', [requestStatus])
