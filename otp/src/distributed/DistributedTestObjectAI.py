from direct.distributed import DistributedObjectAI

class DistributedTestObjectAI(DistributedObjectAI.DistributedObjectAI):
    def getRequiredField(self):
        return 88
