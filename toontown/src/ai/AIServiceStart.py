#!python -S

class game:
    name = "toontown"
    process = "ai"
__builtins__.game = game()

import time
import os
import sys
import string
import getopt

# Initialize ihooks importer On the production servers, we run genPyCode -n
# meaning no squeeze, so nobody else does this. When we squeeze, the
# unpacker does this for us and it does not hurt to do in either case.
import ihooks
ihooks.install()

from direct.directnotify import RotatingLog

# Define a usage string
helpString ="""
python AIServiceStart.py [--mdip=<msgdirector ip/name>] [--mdport=<msgdirector port>] [--esip=<eventserver ip/name>] [--esport=<eventserver port>] [--logpath=<logpath>] --district_number=<number> --district_name=<name> --ssid=<id> --min_objid=<id> --max_objid=<id>

Starts an ai district. Default message director is localhost.  Default
port is 6666. In the district name, underbars will be converted into
spaces.

Example:

python AIServiceStart.py --mdip=localhost --mdport=6665 --logpath=D:\toonlog\ --district_number=200000000 --district_name="Kooky_Summit" --ssid=20100000 --min_objid=30000000 --max_objid=39999999
"""

# Get the options
try:
    opts, pargs = getopt.getopt(sys.argv[1:], '', [
        'mdip=',
        'mdport=',
        'esip=',
        'esport=',
        'logpath=',
        'district_number=',
        'district_name=',
        'ssid=',
        'min_objid=',
        'max_objid=',
        'dcfile=',
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
mdip = "localhost"
mdport = 6666
esip = "localhost"
esport = 4343
logpath = ""
dcFileNames = []
districtType = 0

for opt in opts:
    flag, value = opt
    if (flag == '--district_number'):
        districtNumber = int(value)
    elif (flag == '--district_name'):
        # Convert underbars to spaces
        origDistrictName = value
        districtName = string.replace(value, "_", " ")
    elif (flag == '--logpath'):
        logpath = value
    elif (flag == '--ssid'):
        ssId = int(value)
    elif (flag == '--min_objid'):
        minObjId = int(value)
    elif (flag == '--max_objid'):
        maxObjId = int(value)
    elif (flag == '--mdip'):
        mdip = value
    elif (flag == '--mdport'):
        mdport = int(value)
    elif (flag == '--esip'):
        esip = value
    elif (flag == '--esport'):
        esport = int(value)
    elif (flag == '--dcfile'):
        dcFileNames.append(value)
    else:
        print "Error: Illegal option: " + flag
        print helpString
        sys.exit(1)

if not dcFileNames:
    dcFileNames = ['otp.dc', 'toon.dc']
    
# Setup the log files
# We want C++ and Python to both go to the same log so they
# will be interlaced properly.

# date_hour_sequence.log will be added to the logfile name by RotatingLog():
logfile = logpath + 'aidistrict_' + origDistrictName + "_" +str(districtNumber)

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
print "\n\nStarting %s (number: %s) on %s port %s. %s %s" % (
    districtName, districtNumber, mdip, mdport, 
    time.asctime(time.localtime(time.time())), time.tzname[0])

print "Initializing..."

from otp.ai.AIBaseGlobal import *
from toontown.ai import ToontownAIRepository
from direct.showbase import PythonUtil

simbase.air = ToontownAIRepository.ToontownAIRepository(
    mdip, mdport,
    esip, esport,
    dcFileNames,
    districtNumber,
    districtName,
    districtType,
    ssId,
    minObjId,
    maxObjId)

# How we let the world know we are running a service
simbase.aiService = 1

try:
    run()
except:
    info = PythonUtil.describeException()
    simbase.air.writeServerEvent('ai-exception', districtNumber, info)
    raise
