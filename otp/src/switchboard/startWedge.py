from sbWedge import sbWedge
import sys
import getopt

try:
    opts,args = getopt.getopt(sys.argv[1:], "",
                              ['name=',
                               'wedgeport=',
                               'nshost=',
                               'nsport=',
                               'clhost=',
                               'clport=',
                               'bwdictpath='
                               ])
except getopt.GetoptError:
    print "Please pass a wedge name with --name=."
    sys.exit(1)

#defaults
wedgename = ""
wedgeport = None
nshost = None
nsport = None
clhost = None
clport = None
bwdictpath = ""

for o,a in opts:
    if o == "--name":
        wedgename = a
    elif o == "--wedgeport":
        wedgeport = int(a)
    elif o == "--nshost":
        nshost = a
    elif o == "--nsport":
        nsport = int(a)
    elif o == "--clhost":
        clhost = a
    elif o == "--clport":
        clport = int(a)
    elif o == "--bwdictpath":
        bwdictpath = a
    else:
        print "Error: Illegal option: " + o
        sys.exit(1)        

if wedgename == "":
    print "Please pass a wedge name with --name=."
    sys.exit(2)
    

myWedge = sbWedge(wedgeName=wedgename,
                  nsHost=nshost,
                  nsPort=nsport,
                  listenPort=wedgeport,
                  clHost=clhost,
                  clPort=clport,
                  bwDictPath=bwdictpath)

sys.stdout.flush()

try:
    myWedge.pyroDaemon.requestLoop()
finally:
    myWedge.pyroDaemon.shutdown(True)
