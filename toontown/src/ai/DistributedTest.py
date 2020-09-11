from direct.distributed import DistributedObject

class DistributedTest(DistributedObject.DistributedObject):
    def __init__(self, air):
        try:
            self.DistributedTest_initialized
        except:
            self.DistributedTest_initialized = 1
            DistributedObject.DistributedObject.__init__(self, air)
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

    def d_setB(self, b):
        self.sendUpdate("setB", [b])
        return None

    def b_setB(self, b):
        self.setB(b)
        self.d_setB(b)
        return None

    def getB(self):
        return(self.b)

    def d_setC(self, c):
        self.sendUpdate("setC", [c])
        return None

    def setC(self, c):
        self.c = c
        
