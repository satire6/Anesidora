"""
This class was for testing the so-called 0-timer bug.
It can be resurrected to test future bugs.
You need to uncomment it from toon.dc to use it.
"""

from direct.distributed import DistributedObject

class DistributedTester(DistributedObject.DistributedObject):

    """
    def setMovie(self, active, toons, suits,
                 id0, tr0, le0, tg0, hp0, ac0, hpb0, kbb0, died0,
                 id1, tr1, le1, tg1, hp1, ac1, hpb1, kbb1, died1,
                 id2, tr2, le2, tg2, hp2, ac2, hpb2, kbb2, died2,
                 id3, tr3, le3, tg3, hp3, ac3, hpb3, kbb3, died3,
                 sid0, at0, stg0, dm0, sd0, sb0, st0,
                 sid1, at1, stg1, dm1, sd1, sb1, st1,
                 sid2, at2, stg2, dm2, sd2, sb2, st2,
                 sid3, at3, stg3, dm3, sd3, sb3, st3):
    """

    def __init__(self, cr):
        print "DistributedTester: __init__"
        DistributedObject.DistributedObject.__init__(self, cr)

    def disable(self):
        print "DistributedTester: disable"
        DistributedObject.DistributedObject.disable(self)

    def generate(self):
        print "DistributedTester: generate"
        DistributedObject.DistributedObject.generate(self)

    def generateInit(self):
        print "DistributedTester: generateInit"
        DistributedObject.DistributedObject.generateInit(self)

    def delete(self):
        print "DistributedTester: delete"
        DistributedObject.DistributedObject.delete(self)

    def setMovie(self, *args):
        print "DistributedTester setMovie: doId: ", self.doId

    def setState(self, *args):
        print "DistributedTester setState: doId: ", self.doId


