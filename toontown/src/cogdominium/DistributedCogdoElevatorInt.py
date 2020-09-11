from toontown.building.DistributedElevatorInt import DistributedElevatorInt

class DistributedCogdoElevatorInt(DistributedElevatorInt):
    def _getDoorsClosedInfo(self):
        # return loader, where strings
        return 'cogdoInterior', 'cogdoInterior'
    
