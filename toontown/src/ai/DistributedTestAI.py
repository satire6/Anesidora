from direct.distributed import DistributedObjectAI

class DistributedTestAI(DistributedObjectAI.DistributedObjectAI):
    def __init__(self, air):
        try:
            self.DistributedTestAI_initialized
        except:
            self.DistributedTestAI_initialized = 1
            DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        return None

    def setA(self, a):
        self.a = a
        return None

    def d_setA(self, a):
        self.sendUpdate("setA", [a])
        return None

    def b_setA(self, a):
        self.setA(a)
        self.d_setA(a)
        return None
        
    def getA(self):
        return(self.a)
    
    def setB(self, b):
        self.b = b
        return None

    def d_setB(self, b):
        self.sendUpdate("setB", [b])
        return None

    def b_setB(self, b):
        self.setB(b)
        self.d_setB(b)
        return None

    def getB(self):
        return(self.b)

    def setC(self, c):
        self.c = c
        
