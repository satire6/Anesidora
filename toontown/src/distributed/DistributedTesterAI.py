from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObjectAI
import random
from direct.task import Task

"""
import DistributedTesterAI
d = DistributedTesterAI.DistributedTesterAI(simbase.air)
d.generateWithRequired(2000) # Toontown Central safe zone
d.sendMovieLoop(None)
"""

class DistributedTesterAI(DistributedObjectAI.DistributedObjectAI):

    def getRanUint8(self):
        return int((1<<8) * random.random())

    def getRanUint16(self):
        return int((1<<16) * random.random())

    def getRanUint32(self):
        # Can only go up to 30 here
        return int((1<<30) * random.random())

    def getRanInt8(self):
        return int((1<<8)/2 - (1<<8) * random.random())

    def getRanInt16(self):
        return int((1<<16)/2 - (1<<16) * random.random())

    def getRanInt32(self):
        # Can only go up to 30 here
        return int((1<<30)/2 - (1 << 30) * random.random())

    def getRanUint32array(self):
        return [self.getRanUint32(), self.getRanUint32(), self.getRanUint32(), self.getRanUint32()]

    def getRanInt16array(self):
        return [self.getRanInt16(), self.getRanInt16(), self.getRanInt16(), self.getRanInt16()]

    def getMsg(self):
        msg = [self.getRanInt8(), # active
               self.getRanUint32array(), # toons
               self.getRanUint32array(), # suits
               
               self.getRanInt8(), # id0
               self.getRanInt8(), # tr0
               self.getRanInt8(), # le0 
               self.getRanUint32(), # tg0
               self.getRanInt16array(), # hp0 
               self.getRanInt16(),  # ac0
               self.getRanInt16(), # hpb0
               self.getRanInt16array(), # kbb0
               self.getRanInt8(), # died0

               self.getRanInt8(), # id1
               self.getRanInt8(), # tr1
               self.getRanInt8(), # le1 
               self.getRanUint32(), # tg1
               self.getRanInt16array(), # hp1
               self.getRanInt16(),  # ac1
               self.getRanInt16(), # hpb1
               self.getRanInt16array(), # kbb1
               self.getRanInt8(), # died1

               self.getRanInt8(), # id2
               self.getRanInt8(), # tr2
               self.getRanInt8(), # le2 
               self.getRanUint32(), # tg2
               self.getRanInt16array(), # hp2
               self.getRanInt16(),  # ac2
               self.getRanInt16(), # hpb2
               self.getRanInt16array(), # kbb2
               self.getRanInt8(), # died2
               
               self.getRanInt8(), # id3
               self.getRanInt8(), # tr3
               self.getRanInt8(), # le3 
               self.getRanUint32(), # tg3
               self.getRanInt16array(), # hp3
               self.getRanInt16(),  # ac3
               self.getRanInt16(), # hpb3
               self.getRanInt16array(), # kbb3
               self.getRanInt8(), # died3

               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt16array(),
               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt8(),

               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt16array(),
               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt8(),

               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt16array(),
               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt8(),

               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt16array(),
               self.getRanInt8(),
               self.getRanInt8(),
               self.getRanInt8(),
               ]
        return msg

    def getState(self):
        return ['PlayMovie', globalClockDelta.getRealNetworkTime()]

    def getMovie(self):
        msg = self.getMsg()
        print "get movie", msg
        return msg

    def badMovie(self):
        return [-126, [955899898, 509065983, 960926492, 81065606], [680133635, 605541213, 292096447, 796580728], -26, -108, 62, 923747760, [-25682, -29341, -7593, 30016], -12694, 5591, [22660, -16418, -5502, 2241], -26, -101, 13, 52, 645424651, [-7770, -5732, 9321, -15618], 14005, 11185, [17463, -13305, -17446, 3621], 32, 13, 100, 35, 988348921, [-32722, -9363, -18511, 29851], 29093, 6620, [17046, -29729, -26187, -31586], 42, -10, -49, -2, 487248998, [29940, 6573, -30864, 2953], -8914, -9981, [-952, -20232, 16826, -834], 123, -45, -90, 12, [-28659, 27866, -24647, 23687], -29, 96, 0, 50, -127, -104, [31348, 30517, 24694, 24052], 64, -104, 18, -46, 42, 17, [5558, -896, -30330, -18004], 118, -121, -11, -122, 51, 6, [23869, 14629, -3689, 5496], 19, -122, -106]

    def d_setMovie(self):
        print "about to send setMovie"
        msg = self.getMovie()
        # msg = self.badMovie()
        print "movie message: ", msg
        self.sendUpdate('setMovie', msg)
        stime = globalClock.getRealTime() + 2.0
        self.sendUpdate('setState', ['PlayMovie', globalClockDelta.localToNetworkTime(stime)])
        print "sent setMovie"

    def sendMovieLoop(self, task):
        self.d_setMovie()
        taskMgr.doMethodLater(0.5, self.sendMovieLoop, 'sendMovieLoop')
        return Task.done
        
