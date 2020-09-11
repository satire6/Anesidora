from otp.switchboard.sbNode import sbNode
from otp.switchboard.xd.ChannelManager import *
import sys
import getopt

try:
    opts,args = getopt.getopt(sys.argv[1:], "",
                              ['name=',
                               'nodeport=',
                               'nshost=',
                               'nsport=',
                               'clhost=',
                               'clport=',
                               'dshost=',
                               'dsport=',
                               'dislurl='
                               ])
except getopt.GetoptError:
    print "Please pass a node name with --name=."
    sys.exit(1)

#defaults
nodename = ""
nodeport = None
nshost = None
nsport = None
clhost = None
clport = None
dshost = None
dsport = None
dislurl = None

for o,a in opts:
    if o == "--name":
        nodename = a
    elif o == "--nodeport":
        nodeport = int(a)
    elif o == "--nshost":
        nshost = a
    elif o == "--nsport":
        nsport = int(a)
    elif o == "--clhost":
        clhost = a
    elif o == "--clport":
        clport = int(a)
    elif o == "--dshost":
        dshost = a
    elif o == "--dsport":
        dsport = int(a)
    elif o == "--dislurl":
        dislurl = a
    else:
        print "Error: Illegal option: " + o
        sys.exit(1)        

if nodename == "":
    print "Please pass a node name with --name=."
    sys.exit(2)
    
cm = ChannelManager()
ncm = NetChannelMessenger(nodename,cm,dshost,dsport,1,1000000)

myNode = sbNode(nodeName=nodename,nsHost=nshost,nsPort=nsport,listenPort=nodeport,clHost=clhost,clPort=clport,chanMgr=cm,dislURL=dislurl)

sys.stdout.flush()

try:
    while 1:
        myNode.pyroDaemon.handleRequests(0)
        ncm.pump()
        if ncm.checkReconnect():
            cm.addPromiscuousListener(ncm)
            myNode.joinChannels()
        time.sleep(0.01)
finally:
    #try:
    #    myNode.pyroDaemon.shutdown(True)
    #except: pass
    sys.stdout.flush()
