from toontown.building.DistributedElevatorExt import DistributedElevatorExt

class DistributedCogdoElevatorExt(DistributedElevatorExt):
    def getElevatorModel(self):
        return self.bldg.getCogdoElevatorNodePath()

    def getBldgDoorOrigin(self):
        return self.bldg.getCogdoDoorOrigin()

    def _getDoorsClosedInfo(self):
        return 'cogdoInterior', 'cogdoInterior'
