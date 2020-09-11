import Pyro.core
import Pyro.naming
import Pyro.errors
import time
import sys
import socket

from sbWedge import sbWedge

class dummySocketWedge(sbWedge):
    def __init__(self):
        sbWedge.__init__("dummy")

    def run(self):
        pass

#dsw = dummySocketWedge()
#dsw.run()

while True:
    try:
        print "Starting"
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(('',8989))
        sock.listen(5)

        (clisock,addr) = sock.accept()

        clisock.sendall("Hey you're connected.\n")

        s = ""

        while True:
            data = clisock.recv(1)
            s = s + data
            if data == "\n":
                print s,
                sys.stdout.flush()
                clisock.sendall(s)
                s = ""
            if not len(data):
                break            

        clisock.close()
        sock.close()
    except Exception,e:
        print e
