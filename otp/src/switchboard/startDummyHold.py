from sbNode import sbNode
from sbWedge import sbWedge
import sys
import socket  
import select

#myWedge = sbWedge("dummy")

#myWedge.node._setOneway(["enterPlayer","exitPlayer","sendWhisper"])

#myWedge.node.enterPlayer(1234)

def log(message):
    print message
    sys.stdout.flush()


listensock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listensock.bind(('',8990))
listensock.listen(500)
log("Listening for clients.")

clisock = None
s = ""

while True:
    try:
        #socks = myWedge.pyroDaemon.getServerSockets()
        #socks.append(listensock)
        socks = [listensock]
        if clisock is not None:
            socks.append(clisock)

        ins,outs,exs=select.select(socks,[],[])

        if listensock in ins:
            if clisock is not None:
                clisock.close()
            (clisock,addr) = listensock.accept()
            log("Client connected!")
            clisock.sendall("HELLO\n")
            s = ""

        #for sock in myWedge.pyroDaemon.getServerSockets():
        #    if sock in ins:
        #        myWedge.pyroDaemon.handleRequests()
        #        break
            
        if clisock in ins:
            data = clisock.recv(1)            
            if data == "\n":
                try:
                    (dest,src,action,msg) = s.split(None,3)
                    if action == "SEND":
                        log("%d -> %d: %s" % (int(src),int(dest),msg))
                        clisock.sendall("%s %s SEND Hey I got your whisper.\n" % (src,dest))
                        #myWedge.node.sendWhisper(1234,1234,msg)
                    else:
                        log("Invalid message: %s" % s)
                        clisock.sendall("Blargh invalid message\n")
                except:
                    log("Invalid message: %s" % s)
                    clisock.sendall("Blargh invalid message\n")
                s = ""
            else:
                s = s + data


    except Exception,e:
        log("Caught error:")
        log(e)
        try:
            clisock.close()
            clisock = None
        except:
            pass
        

