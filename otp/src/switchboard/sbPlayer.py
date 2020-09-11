import Pyro.core


class sbPlayer(Pyro.core.ObjBase):
    def __init__(self,myNode,playerId):
        Pyro.core.ObjBase.__init__(self)
        self.node = myNode
        self.playerId = playerId

    def exit(self):
        self.node.exitPlayer(self.playerId)

    def recvWhisper(self,senderId,msgText):
        #CHECK FRIENDSHIP
        self.node.recvWhisper(self.playerId,senderId,msgText)

    def recvWhisperSC(self,senderId,msgIndex):
        self.node.recvWhisperSC(self.playerId,senderId,msgText)
    
    def mul(s, arg1, arg2): return arg1*arg2
    def add(s, arg1, arg2): return arg1+arg2
    def sub(s, arg1, arg2): return arg1-arg2
    def div(s, arg1, arg2): return arg1/arg2
