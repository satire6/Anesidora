"""
Start the Toontown UberDog (Uber Distributed Object Globals server).
"""
import __builtin__
from direct.task.Task import Task

class game:
    name = "uberDog"
    process = "server"
__builtin__.game = game()

import time
import os
import sys
import getopt

# Initialize ihooks importer On the production servers, we run genPyCode -n
# meaning no squeeze, so nobody else does this. When we squeeze, the
# unpacker does this for us and it does not hurt to do in either case.
import ihooks
ihooks.install()

if os.getenv('TTMODELS'):
    from pandac.PandaModules import getModelPath, Filename
    # In the publish environment, TTMODELS won't be on the model
    # path by default, so we always add it there.  In the dev
    # environment, it'll be on the model path already, but it
    # doesn't hurt to add it again.
    getModelPath().appendDirectory(Filename.expandFrom("$TTMODELS"))

from direct.directnotify import RotatingLog
from otp.uberdog.UberDogGlobal import *

# Get the options
try:
    opts, pargs = getopt.getopt(sys.argv[1:], '',
                                ['mdip=',
                                 'mdport=',
                                 'esip=',
                                 'esport=',
                                 'logpath=',
                                 'ssid=',
                                 'minChan=',
                                 'maxChan=',
                                 'sbNSHost=',
                                 'sbNSPort=',
                                 'sbListenPort=',
                                 'sbCLHost=',
                                 'sbCLPort=',
                                 'bwDictPath=',
                                 'mysqlhost=',
                                 'crDbName=',
                                 ])
except Exception, e:
    print e
    print helpString
    sys.exit(1)

# Only four of the items are required
if len(opts) < 4:
    print helpString
    sys.exit(1)

# Default values
uber.mdip = "localhost"
uber.mdport = 6666
uber.esip = "localhost"
uber.esport = 4343
logpath = ""
stateServerId = None
minChannel = None
maxChannel = None
sbNSHost = ""
sbNSPort = 6053
sbListenPort = 6053
sbCLHost = ""
sbCLPort = 6060

homedir = os.getenv("HOME", "")
language = os.getenv("LANGUAGE", "")
if language in ['castillian', 'japanese', 'german', 'portuguese', 'french'] :
   bwDictPath = homedir + "/support/"
else :
   bwDictPath = "/home/toonpub/support/"
uber.RATManagerHTTPListenPort = 8080
uber.awardManagerHTTPListenPort = 8888
uber.inGameNewsMgrHTTPListenPort = 8889
mysqlhost = "localhost"

# example values
#minChannel = 20400000
#maxChannel = 20449999
#stateServerId = 20100000
dcFileNames = ['otp.dc', 'toon.dc']
#uber.bwDictPath = ""

for opt in opts:
    flag, value = opt
    if (flag == '--logpath'):
        logpath = value
    elif (flag == '--ssid'):
        stateServerId = int(value)
    elif (flag == '--minChan'):
        minChannel = int(value)
    elif (flag == '--maxChan'):
        maxChannel = int(value)
    elif (flag == '--mdip'):
        uber.mdip = value
    elif (flag == '--mdport'):
        uber.mdport = int(value)
    elif (flag == '--esip'):
        uber.esip = value
    elif (flag == '--esport'):
        uber.esport = int(value)
    elif (flag == '--sbNSHost'):
        sbNSHost = value
    elif (flag == '--sbNSPort'):
        sbNSPort = int(value)
    elif (flag == '--sbCLHost'):
        sbCLHost = value
    elif (flag == '--sbCLPort'):
        sbCLPort = int(value)
    elif (flag == '--sbListenPort'):
        sbListenPort = int(value)
    elif (flag == '--bwDictPath'):
        bwDictPath = value
    elif (flag == '--mysqlhost'):
        mysqlhost = value    
    elif (flag == '--crDbName'):
        crDbName = value    
    else:
        print "Error: Illegal option: " + flag
        print helpString
        sys.exit(1)

# date_hour_sequence.log will be added to the logfile name by RotatingLog():
logfile = logpath + 'aidistrict_uberdog'

# Redirect Python output and err to the same file
class LogAndOutput:
    def __init__(self, orig, log):
        self.orig = orig
        self.log = log
    def write(self, str):
        self.log.write(str)
        self.log.flush()
        self.orig.write(str)
        self.orig.flush()
    def flush(self):
        self.log.flush()
        self.orig.flush()

log = RotatingLog.RotatingLog(logfile, hourInterval=24, megabyteLimit=1024)
logOut = LogAndOutput(sys.__stdout__, log)
logErr = LogAndOutput(sys.__stderr__, log)
sys.stdout = logOut
sys.stderr = logErr

from pandac.PandaModules import *

# Give Panda the same log we use
nout = MultiplexStream()
Notify.ptr().setOstreamPtr(nout, 0)
nout.addFile(Filename(logfile))
nout.addStandardOutput()
nout.addSystemDebug()

# We prefer writing the date on the same line as the starting message,
# so we can more easily grep for a restart on a particular date in the
# log files.
print "\n\nStarting Uberdog on %s port %s. %s %s" % \
      (uber.mdip, uber.mdport, time.asctime(time.localtime(time.time())), time.tzname[0])

print "Initializing the Toontown UberDog (Uber Distributed Object Globals server)..."

from toontown.uberdog.ToontownUberDog import ToontownUberDog
from direct.showbase.PythonUtil import *

uber.objectNames = set(os.getenv("uberdog_objects", "").split())

uber.sbNSHost = sbNSHost
uber.sbNSPort = sbNSPort
uber.sbListenPort = sbListenPort
uber.clHost = sbCLHost
uber.clPort = sbCLPort
uber.allowUnfilteredChat = 0
uber.bwDictPath = bwDictPath

uber.RATManagerHTTPListenPort = int(os.getenv("RAT_PORT","8080"))
uber.awardManagerHTTPListenPort = int(os.getenv("AWARD_MANAGER_PORT","8888"))
uber.inGameNewsMgrHTTPListenPort = int(os.getenv("IN_GAME_NEWS_PORT","8889"))
uber.mysqlhost = mysqlhost

uber.codeRedemptionMgrHTTPListenPort = int(os.getenv("CODE_REDEMPTION_PORT","8998"))
uber.crDbName = crDbName

uber.cpuInfoMgrHTTPListenPort = int(os.getenv("SECURITY_BAN_MGR_PORT",8892))

uber.air = ToontownUberDog(
        uber.mdip, uber.mdport,
        uber.esip, uber.esport,
        dcFileNames,
        stateServerId,
        minChannel,
        maxChannel)

# We let the world know that we are running as a service
uber.aiService = 1

uber.wantEmbeddedOtpServer = 0

try:
    run()
except:
    info = describeException()
    #uber.air.writeServerEvent('uberdog-exception', districtNumber, info)
    raise

