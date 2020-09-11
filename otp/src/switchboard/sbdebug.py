#!/home/igraham/player/wintools/sdk/python/Python-2.4.1/PCbuild/python


import Pyro.util
import Pyro.core
import Pyro.naming
import sys
import getopt

try:
    opts,args = getopt.getopt(sys.argv[1:], "h:n:p:u:exw:m:sci")
except getopt.GetoptError:
    print "Switchboard Debugger Options:"
    print "-h hostname - Specify NS hostname"
    print "-p port - specify NS port"
    print "-n wedgename - Connect to wedge, required to issue any command"
    print "-u usernumber - Specify user to perform action"
    print "-e - Enter Player"
    print "-x - Exit Player"
    print "-w recipient -m message - Whisper to recipient with message"
    print "-c checkSocket"
    print "-i interactive"
    print "-s - Shutdown this node"
    sys.exit(2)

NShost = "localhost"
NSport = 6060

wedgename = ""
playernumber = 0

action = ""

recipient = ""
message = ""

for o,a in opts:
    if o == "-n":
        wedgename = a
    elif o == "-h":
        NShost = a
    elif o == "-p":
        NSport = int(a)
    elif o == "-u":
        playernumber = int(a)
    elif o == "-e":
        action = "enterPlayer"
    elif o == "-x":
        action = "exitPlayer"
    elif o == "-w":
        action = "whisper"
        recipient = int(a)
    elif o == "-m":
        message = a
    elif o == "-s":
        action = "shutdown"
    elif o == "-c":
        action = "checkSocket"
    elif o == "-i":
        action = "interactive"
        


if wedgename == "":
    print "Please pass a node name with -n."
    sys.exit(2)
if action == "":
    print "No action specified!  Doing nothing."
    sys.exit(0)



Pyro.core.initClient(banner=0)
ns = Pyro.naming.NameServerLocator().getNS(host=NShost,port=NSport)

try:
    if action == "shutdown":
        try:
            node = Pyro.core.getProxyForURI(ns.resolve(":sb.node.%s"%wedgename))
            node.shutdown()
        except:
            pass
        try:
            wedge = Pyro.core.getProxyForURI(ns.resolve(":sb.wedge.%s"%wedgename))
            wedge.shutdown()
        except:
            pass

    elif action == "interactive":
        wedge = Pyro.core.getProxyForURI(ns.resolve(":sb.wedge.%s"%wedgename))
        print wedge
        import pdb
        pdb.set_trace()

    elif action == "enterPlayer":
        info = 0
        wedge = Pyro.core.getProxyForURI(ns.resolve(":sb.wedge.%s"%wedgename))
        wedge.enterPlayer(playernumber,info)
    elif action == "exitPlayer":
        wedge = Pyro.core.getProxyForURI(ns.resolve(":sb.wedge.%s"%wedgename))
        wedge.exitPlayer(playernumber)
    elif action == "whisper":
        wedge = Pyro.core.getProxyForURI(ns.resolve(":sb.wedge.%s"%wedgename))
        wedge.sendWhisper(recipient,playernumber,message)
    elif action == "checkSocket":
        wedge = Pyro.core.getProxyForURI(ns.resolve(":sb.wedge.%s"%wedgename))
        wedge.checkSocket()
except Exception, x:
    print ''.join(Pyro.util.getPyroTraceback(x))
    sys.stdout.flush()
