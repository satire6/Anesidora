
class PlayerBase:
    # player code shared by AI & client

    def __init__(self):
        self.gmState = False
        pass
    
    def atLocation(self, locationId):
        return True

    def getLocation(self):
        # return a list of locationIds, starting from general location
        # (i.e. 'Pirates') down to specific location (i.e. jungle ID)
        return []

    def setAsGM(self, state):
        """ Toggle GM privilages """
        self.gmState = state
        
    def isGM(self):
        return self.gmState
    
