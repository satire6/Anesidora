from otp.ai.AIBase import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
import DistributedCrusherEntityAI
import StomperGlobals
from direct.distributed import ClockDelta

class DistributedStomperAI(DistributedCrusherEntityAI.DistributedCrusherEntityAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStomperAI")
    def __init__(self, level, entId, pairId=-1):
        DistributedCrusherEntityAI.DistributedCrusherEntityAI.__init__(self,
                                                                       level, entId)
        self.pairId = pairId
        
    def generate(self):
        DistributedCrusherEntityAI.DistributedCrusherEntityAI.generate(self)

        # if we are attached to a switch, listen for on/off events
        if self.switchId != 0:
            self.accept(self.getOutputEventName(self.switchId),
                        self.reactToSwitch)
        
        # start the stomper on the clients
        self.d_startStomper()
        
    def delete(self):
        del self.pos
        self.ignoreAll()
        DistributedCrusherEntityAI.DistributedCrusherEntityAI.delete(self)
        
    def d_startStomper(self):
        self.sendUpdate("setMovie", [StomperGlobals.STOMPER_START,
                                     ClockDelta.globalClockDelta.getRealNetworkTime(),
                                     []])
    
    def reactToSwitch(self, on):
        if on:
            # switch has been stepped on, make the stomper stomp
            crushedList = []
            if self.crushCell:
                # check if anything is in this crush cell first
                self.crushCell.updateCrushables()
        
                # make a list of things to be crushed by this stomper
                for id in self.crushCell.occupantIds:
                    if id in self.crushCell.crushables:
                        crushedList.append(id)

                # calling sendCrushMsg calls doCrush on the crusherCellAI
                # which in turn calls doCrush on all the crushableEntitys
                # contained in that cell
                self.sendCrushMsg()
                
            self.sendUpdate("setMovie", [StomperGlobals.STOMPER_STOMP,
                                         ClockDelta.globalClockDelta.getRealNetworkTime(),
                                         crushedList])
        else:
            # make the stomper rise
            self.sendUpdate("setMovie", [StomperGlobals.STOMPER_RISE,
                                         ClockDelta.globalClockDelta.getRealNetworkTime(),
                                         []])
        
