# dummy SB

from sbNode import sbNode
from sbWedge import sbWedge
import Queue
import sys
import socket  
import select

q = Queue.Queue()

class dumWedge(sbWedge):
    def __init__(self,wedgeName,qq):
        sbWedge.__init__(self,wedgeName)
        self.q = qq
    def recvWhisper(self,recipientId,senderId,msgText):
        self.log("**Whisper from %d received for %d: %s"%(senderId,recipientId,msgText))
        self.q.put((recipientId,senderId,msgText))
    def shutdown(self):
        self.q.put((-1,-1,-1))
        sbWedge.shutdown()
        
myWedge = dumWedge("dummy",q)

myWedge.node._setOneway(["enterPlayer","exitPlayer","sendWhisper"])

#myWedge.node.enterPlayer(1234)

def log(message):
    print message
    sys.stdout.flush()


listensock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listensock.bind(('',8989))
listensock.listen(500)
log("Listening for clients.")

clisock = None
s = ""

while True:
    try:
        socks = myWedge.pyroDaemon.getServerSockets()
        socks.append(listensock)
        if clisock is not None:
            socks.append(clisock)

        ins = []

        while not len(ins):
            ins,outs,exs=select.select(socks,[],[],1)
            try:
                (recipient,sender,msg) = q.get_nowait()
                if recipient == -1:
                    log(":sb.wedge.dummy: Shutting down cleanly.")
                    try:
                        clisock.close()
                        listensock.close()
                    except: pass
                    sys.exit(0)
                log("ping")
                sendstr = "%d %d SEND %s\n" % (recipient,sender,msg)
                log(sendstr)
                clisock.sendall(sendstr)
            except Queue.Empty: pass      

        if listensock in ins:
            if clisock is not None:
                clisock.close()
            (clisock,addr) = listensock.accept()
            log("Client connected!")
            clisock.sendall("HELLO\n")
            s = ""

        for sock in myWedge.pyroDaemon.getServerSockets():
            if sock in ins:
                myWedge.pyroDaemon.handleRequests()
                break
            
        if clisock in ins:
            data = clisock.recv(1)            
            if data == "\n":
                try:
                    (dest,src,action,msg) = s.split(None,3)
                    if action == "SEND":
                        log("%d -> %d: %s" % (int(src),int(dest),msg))
                        myWedge.sendWhisper(int(dest),int(src),"michael@GEM: %s"%msg)
                    else:
                        log("Invalid message: %s" % s)
                        clisock.sendall("Blargh invalid message\n")
                except Exception,e:
                    log(e)
                    log("Problematic message: %s" % s)
                    clisock.sendall("Blargh invalid message\n")
                s = ""
            else:
                s = s + data


    except Queue.Empty,e:
        log("Caught error:")
        log(e)
        try:
            clisock.close()
            clisock = None
        except:
            pass
        

