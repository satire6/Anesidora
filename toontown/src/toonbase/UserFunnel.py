"""UserFunnel.py: Contains functions to report data back to hitbox and our own data collection servers""" 

import os, sys, socket, random
from urllib import quote_plus

from pandac.PandaModules import HTTPClient
from pandac.PandaModules import HTTPCookie
from pandac.PandaModules import URLSpec
from pandac.PandaModules import Ramfile
from pandac.PandaModules import Ostream
from pandac.PandaModules import HTTPDate
from pandac.PandaModules import DocumentSpec
from direct.task.Task import Task

from direct.directnotify.DirectNotifyGlobal import directNotify
notify = directNotify.newCategory("UserFunnel")

# The easy way to use this with hitbox is to import the UserFunnel module.
# Then execute UserFunnel.logSubmit(1,'STRING')
# Where STRING is the logging string (page name) to send to hitbox.
# You can use it with the internal data collector too, just use 0 instead of 1

class UserFunnel:
    
    def __init__(self):
        
        # Variables required for acct service access
        # HitBox Account Number.
        # DOL test account = DM510925KJWE
        # Pirates Account = DM560804E8WD
        # ToonTown Account = DM53030620EW

        self.hitboxAcct = 'DM53030620EW'
        # self.hitboxAcct = 'DM510925KJWE'
        # Language Used; example: English (US) = en-us

        self.language = 'en-us'

        # Content Group

        self.cgRoot = 'ToonTown_Online'

        # Content Sub-Groups
        # For now, I've hardcoded the cgLocation to US. In the future
        # we'll need to change this by hand or via a function, to reflect
        # the geolocation that this is being built for.

        self.cgBeta = 'Beta'
        self.cgRelease = 'Release'
        self.cgLocation = 'US'

        # Campaign ID for hitbox
        # Again, this ID has yet to be provided

        self.campaignID = ''

        # Cookie CallBack for HBX, but can be used for others if needed

        # self.cfCookie = cookielib.MozillaCookieJar('cf.txt')
        self.cfCookieFile = 'cf.txt'

        # Host Listing. Access hostnames and paths will be listed here
        # Each item has an int that goes along with it.

        self.dynamicVRFunnel = 'http://download.toontown.com/'
        # self.dynamicVRFunnel = 'http://build64:3120/logging/collector.php'

        self.hostDict = {0:'Internal Disney PHP Collector Site',
                         1:'ehg-dig.hitbox.com/HG?',
                         2:'ehg-dig.hitbox.com/HG?',
                         3:'build64.online.disney.com:5020/index.php?'}

        # The current host variable will be an int value that points to an
        # entry in the hostDict. It is used at URL generation time to insert
        # the correct hostname and path into the URL

        self.CurrentHost = ''

        # URLtoSend is the actual URL that will be accessed when run() is called
        self.URLtoSend = ''

        # System Variables to report on. Currently, they are not all being used.
        # Some variables have been put in place for future use.

        # GameName is the name of the game being reported on

        self.gameName = 'ToonTown'

        # BrowserName for ID

        self.browserName = 'Panda3D%20(' + self.gameName + ';%20' + sys.platform + ')'
        # HTTPUserHeader to be transmitted once the http connection is established. This is not part of the URL that is sent. It is part of the header.

        self.HTTPUserHeader = [('User-agent', 'Panda3D')]

        # OS Major Version: Example MS-WinXP = 5, MacOSX Tiger = 10

        self.osMajorver = ''

        # OS Minor Version: Example MS-WinXP = 1, OSX Tiger = 4

        self.osMinorver = ''

        # OS Rev Version: Example OSX Tiger = 1...9

        self.osRevver = ''

        # OS Build Number: Example MS-WinXP = 2600

        self.osBuild = ''

        # OS Type. Example: int value that goes along with the msWinTypeDict

        self.osType = ''

        # The getwindowsversion command returns comments. An example would the a comment about the currently installed service pack

        self.osComments = ''

        # Dict of int to string pairs for self.osType

        self.msWinTypeDict = {0:'Win32s on Windows 3.1',
                              1:'Windows 95/98/ME',
                              2:'Windows NT/2000/XP',
                              3:'Windows CE'}

        self.milestoneDict = {0:'New User',
                              1:'Create Account',
                              2:'View EULA',
                              3:'Accept EULA',
                              4:'Download Start',
                              5:'Download End',
                              6:'Installer Run',
                              7:'Launcher Start',
                              8:'Launcher Login',
                              9:'Client Opens',
                              10:'Create Pirate Loads',
                              11:'Create Pirate Exit',
                              12:'Cutscene One Start',
                              13:'Cutscene One Ends',
                              14:'Cutscene Two Start',
                              15:'Cutscene Thee Start',
                              16:'Cutscene Three Ends',
                              17:'Access Cannon',
                              18:'Cutscene Four Starts',
                              19:'Cutscene Four Ends',
                              20:'Dock - Start Game'}

        self.macTypeDict = {2:'Jaguar',
                            1:'Puma',
                            3:'Panther',
                            4:'Tiger',
                            5:'Lepard'}

        # Milestone string var. Used to hold the funnel location string. This used to be an int (as per the dict above), but later is was decided that it would be a string value; ie. START_GAME or BUILD_PIRATE_START. I have left the milestoneDict in place for reference purposes.

        self.milestone = ''

        # The next three lists hold the cookie vars for the three hitbox based
        # variable / value pairs requred for hitbox.
        # [DOMAIN, /, VARIABLE, VALUE]

        self.pandaHTTPClientVarWSS = []
        self.pandaHTTPClientVarCTG = []
        self.pandaHTTPClientVarDM = []

        # In an effort to determine if this is the first time the client has
        # been executed on the system, we will check for the existance of the
        # cf.txt file. If the file does not exist, we will set the firstRun()
        # to True.

        self.checkForCFfile()

        # Instance an HTTPClient session

        self.httpSession = HTTPClient()

        # Run the whatOSver command at the end of the constructor.
        self.whatOSver()


    def checkForCFfile(self):
        # Check for the existance of the cf.txt file. If it does not exist,
        # then set the firstRun() to True. If it does exist, do nothing.

        if firstRun() == True:
            pass
        else:
            if(os.path.isfile(self.cfCookieFile) == False):
                firstRun('write', True)
                

    # Populate the osMajor, osMinor, osBuild, osType, osComments, and osRevver vars
    def whatOSver(self):
        if (sys.platform == 'win32'):
            self.osMajorver = str(sys.getwindowsversion()[0])
            self.osMinorver = str(sys.getwindowsversion()[1])
            self.osBuild = str(sys.getwindowsversion()[2])
            self.osType = str(sys.getwindowsversion()[3])
            self.osComments = str(sys.getwindowsversion()[4])
            return

        if (sys.platform == 'darwin'):
            self.osMajorver = '10'
            osxcmd = '/usr/sbin/system_profiler SPSoftwareDataType |/usr/bin/grep "System Version"'
            infopipe = os.popen(osxcmd, 'r')
            parseLine = infopipe.read()
            infopipe.close()
            del infopipe
            notify.info("parseLine = %s" % str(parseLine))
            versionStringStart = parseLine.find('10.')
            notify.info("versionStringStart = %s" % str(versionStringStart))
            testPlist = False
            try:
                # I placed this segment into the try/except pair due to an
                # exception that pops up at most once a day, where these
                # assignments return an out of range error
                # RAU exception always happen in 10.6
                
                self.osMinorver = parseLine[versionStringStart+3]
                self.osRevver = parseLine[versionStringStart+5:versionStringStart+7].strip(' ')
                self.osBuild = parseLine[int(parseLine.find('('))+1:parseLine.find(')')]
            except:
                # This should catch this rare case. It's probably happening
                # due to a corrupt OS install on the client. 
                # In this case, we'll just manually assign values
                # RAU so 10.6 will always report as 10.0
                notify.info("couldn't parse the system_profiler output, using zeros")
                self.osMinorver = '0'
                self.osRevver = '0'
                self.osBuild = '0000'
                testPlist = True
            del versionStringStart
            del parseLine
            del osxcmd

            if testPlist:
                try:
                    import plistlib
                    pl = plistlib.readPlist("/System/Library/CoreServices/SystemVersion.plist")
                    notify.info("pl=%s" % str(pl))
                    parseLine = pl['ProductVersion']
                    numbers = parseLine.split('.')
                    notify.info("parseline =%s numbers =%s" % (parseLine, numbers))
                    self.osMinorver = numbers[1]
                    self.osRevver = numbers[2]
                    self.osBuild = pl["ProductBuildVersion"]
                except:
                    notify.info("tried plist but still got exception")
                    self.osMinorver = '0'
                    self.osRevver = '0'
                    self.osBuild = '0000'
            return

    def setmilestone(self,ms):
        if firstRun() == False:
            self.milestone = ms
        else:
            self.milestone = '%s_INITIAL' % (ms)

    def setgamename(self, gamename):
        self.gameName = gamename

    def printosComments(self):
        return self.osComments

    def setHost(self, hostID):
        assert hostID < len(self.hostDict), "Error: hostID passed in UserTracker.setHost not valid, value to high"
        assert hostID > -1, "Error: hostID must be 0 or positive int"
        self.CurrentHost = hostID

    # This will go out to the download server and get the current Disney Funnel logging URL

    def getFunnelURL(self):
        # print 'VRS URL: ' + self.dynamicVRFunnel
        if (patcherVer() == ['OFFLINE']):
            # print "Funnel System Offline"
            return
        if (patcherVer() == []):
            # print "Funnel URL not set. Setting now"
            patcherHTTP = HTTPClient()
            if checkParamFile() == None:
                patcherDoc = patcherHTTP.getDocument(URLSpec('http://download.toontown.com/english/currentVersion/content/patcher.ver'))
                # Now set vcon (Content Group) to the Release string
                vconGroup('w', self.cgRelease)
            else:
                patcherDoc = patcherHTTP.getDocument(URLSpec(checkParamFile()))
                # Set vcon (Content Group) to the Beta string
                vconGroup('w', self.cgBeta)
            # patcherDoc = patcherHTTP.getDocument(URLSpec('http://build64:3120/english/currentVersion/dev/content/patcher.ver'))
            rf = Ramfile()
            patcherDoc.downloadToRam(rf)
            self.patcherURL = rf.getData()
            if self.patcherURL.find('FUNNEL_LOG') == -1:
                # The file did not download, need to set
                # the patcherVer to offline
                patcherVer('w','OFFLINE')
                # print 'Patcher system could not be reached'
                return
            self.patcherURL = self.patcherURL.split('\n')
            del rf, patcherDoc, patcherHTTP
            while self.patcherURL:
                self.confLine = self.patcherURL.pop()
                if (self.confLine.find('FUNNEL_LOG=') != -1 and self.confLine.find('#FUNNEL_LOG=') == -1 ):
                    self.dynamicVRFunnel =  self.confLine[11:].strip('\n')
                    patcherVer('w',self.confLine[11:].strip('\n'))
        else:
            self.dynamicVRFunnel = patcherVer()[0]

    def isVarSet(self, varInQuestion):
        try:
            tempvar = type(varInQuestion)
            return 1
        except NameError:
            return 0

    def buildURL(self):

        # A recent Hitbox Addition. We need to generate a variable/value pair.
        # The variable name depends on the OS. If the OS is win32, then the
        # variable name is c3. If the OS is darwin, then the variable name
        # is c4. The value to be passed to c3 and c4 is the same:
        # str(self.osMajorver) + '_' + str(self.osMinorver) + '_' + str(self.osRevver) + '_' + str(self.osBuild)

        if sys.platform == 'win32':
            hitboxOSType = 'c3'
        else:
            hitboxOSType = 'c4'

        # This will take all of the required variables and generate
        # A URL to be transmitted to the currently selected service
        # Host 1 is the hitbox URL config

        if (self.CurrentHost == 1):
            self.URLtoSend = 'http://' + self.hostDict[self.CurrentHost] + 'hb=' + str(self.hitboxAcct) + '&n=' + str(self.milestone) + '&ln=' + self.language + '&gp=STARTGAME&fnl=TOONTOWN_FUNNEL&vcon=/' + self.cgRoot + '/' + self.cgLocation + '/' + str(vconGroup()) + '&c1=' + str(sys.platform) + '&' + str(hitboxOSType) + '=' + str(self.osMajorver) + '_' + str(self.osMinorver) + '_' + str(self.osRevver) + '_' + str(self.osBuild)
            # print self.URLtoSend

        # Host 2 is for the Hitbox, with no funnel

        if (self.CurrentHost == 2):
            self.URLtoSend = 'http://' + self.hostDict[self.CurrentHost] + 'hb=' + str(self.hitboxAcct) + '&n=' + str(self.milestone) + '&ln=' + self.language + '&vcon=/' + self.cgRoot + '/' + self.cgLocation + '/' + str(vconGroup()) + '&c1=' + str(sys.platform) + '&' + str(hitboxOSType) + '=' + str(self.osMajorver) + '_' + str(self.osMinorver) + '_' + str(self.osRevver) + '_' + str(self.osBuild)
        # Host 3 is the disney logging server config.

        # if (self.CurrentHost == 3):
            # self.URLtoSend = 'http://' + self.hostDict[self.CurrentHost] + 'some_var_name=' + self.gameName

            #Need to add a bunch more. Just not sure of the variable names yet
        # This host is for the internal server

        if (self.CurrentHost == 0):
            localMAC = str(getMAC())
            self.URLtoSend = str(self.dynamicVRFunnel) + '?funnel=' + str(self.milestone) + '&platform=' + str(sys.platform) + '&sysver=' + str(self.osMajorver) + '_' + str(self.osMinorver) + '_' + str(self.osRevver) + '_' + str(self.osBuild) + '&mac=' + localMAC + '&username=' + str(loggingSubID()) + '&id=' + str(loggingAvID())


    def readInPandaCookie(self):
        # This function is designed to read in the cookie format that
        # the panda HTTPClient uses.
        # The format is as follows:
        # DOMAINAME<TAB>/<TAB>VARIABLE<TAB>VALUE<\n>
        # EXAMPLE:
        # .hitbox.com     /     CTG     1181271609

        thefile = open(self.cfCookieFile, 'r')
        thedata = thefile.read().split('\n')
        thefile.close()
        del thefile
        # Before we go any further, lets check to see if the file is using
        # the old Netscape HTTP format the python's MozillaCookie Jar
        # supports. If so, lets delete the file and re-populate with
        # a new cookie from the server
        if (thedata[0].find('Netscape HTTP Cookie File') != -1):
            return
        # Pop off last element; it's blank
        thedata.pop()
        try:
            while thedata:
                temp = thedata.pop()
                # if temp.find('.hitbox.com') != -1 or temp.find('ehg-dig.hitbox.com') != -1:
                temp = temp.split('\t')
                domain = temp[0]
                loc = temp[1]
                variable = temp[2]
                value = temp[3]

                if (variable == 'CTG'):
                    self.pandaHTTPClientVarCTG = [domain, loc, variable, value]
                    self.setTheHTTPCookie(self.pandaHTTPClientVarCTG)
                if (variable == self.hitboxAcct + 'V6'):
                    self.pandaHTTPClientVarDM = [domain, loc, variable, value]
                    self.setTheHTTPCookie(self.pandaHTTPClientVarDM)
                if (variable == 'WSS_GW'):
                    self.pandaHTTPClientVarWSS = [domain, loc, variable, value]
                    self.setTheHTTPCookie(self.pandaHTTPClientVarWSS)
        except IndexError:
            print "UserFunnel(Warning): Cookie Data file bad"

        del thedata

    def updateInstanceCookieValues(self):
        a = self.httpSession.getCookie(HTTPCookie('WSS_GW', '/', '.hitbox.com'))
        if a.getName():
            self.pandaHTTPClientVarWSS = ['.hitbox.com', '/', 'WSS_GW', a.getValue()]
        else:
            # print 'WSS_GW Cookie Value not set'
            pass

        b = self.httpSession.getCookie(HTTPCookie('CTG', '/', '.hitbox.com'))
        if b.getName():
            self.pandaHTTPClientVarCTG = ['.hitbox.com', '/', 'CTG', b.getValue()]
        else:
            # print 'CTG Cookie Value not set'
            pass

        c = self.httpSession.getCookie(HTTPCookie(self.hitboxAcct + 'V6', '/', 'ehg-dig.hitbox.com'))
        if c.getName():
            self.pandaHTTPClientVarDM = ['ehg-dig.hitbox.com', '/', self.hitboxAcct + 'V6', c.getValue()]
        else:
            #print self.hitboxAcct + 'V6 Cookie Value not set'
            pass

        del a, b, c

    def setTheHTTPCookie(self, cookieParams):
        c = HTTPCookie(cookieParams[2], cookieParams[1], cookieParams[0])
        c.setValue(cookieParams[3])
        self.httpSession.setCookie(c)

    def writeOutPandaCookie(self):
        # This is designed to write out a cookie file in the format that
        # the panda HTTPClient uses.
        # Please see the readInPandaCookie comments for format.

        try:
            thefile = open(self.cfCookieFile, 'w')
            if len(self.pandaHTTPClientVarWSS) == 4:
                thefile.write(self.pandaHTTPClientVarWSS[0] + '\t' + self.pandaHTTPClientVarWSS[1] + '\t' + self.pandaHTTPClientVarWSS[2] + '\t' + self.pandaHTTPClientVarWSS[3] + '\n')
            if len(self.pandaHTTPClientVarCTG) == 4:
                thefile.write(self.pandaHTTPClientVarCTG[0] + '\t' + self.pandaHTTPClientVarCTG[1] + '\t' + self.pandaHTTPClientVarCTG[2] + '\t' + self.pandaHTTPClientVarCTG[3] + '\n')
            if len(self.pandaHTTPClientVarDM) == 4:
                thefile.write(self.pandaHTTPClientVarDM[0] + '\t' + self.pandaHTTPClientVarDM[1] + '\t' + self.pandaHTTPClientVarDM[2] + '\t' + self.pandaHTTPClientVarDM[3] + '\n')
            thefile.close()
        except IOError:
            return

    # The next function spawns another thread and executed the network
    # transaction; i.e. host resolve, open connection, send, close, etc.
    # Update, the threading has been disbaled for the time being.

    def prerun(self):

        # print "Begin Hitbox Thread"
        # Use start() method to execute this run() function in second thread

        # Commented out the next line (if statement) on 9-10-07,
        # and moved the indent on self.getFunnelURL to the left.
        # It looks like due to changes in the function that gets the
        # patcher.ver, it is no longer necessary to only check the FunnelURL
        # status when the CurrentHost is 0. The getFunnelURL() should be
        # called no mater what the CurrentHost is set to. I think that it was
        # only checking when CurrentHost == 0, due to some URLs being
        # hardcoded in previous versions of the logging module. But that
        # is no longer the case for the VRS collector.
        
        # if (self.CurrentHost == 0):
        self.getFunnelURL()

        # print "build url"
        self.buildURL()
        if(os.path.isfile(self.cfCookieFile) == True):
            # print "load preexisting cookie"
            # self.cfCookie.load()
            if self.CurrentHost == 1 or self.CurrentHost == 2:
                self.readInPandaCookie()
        # print "Cookies before transaction"
        # self.httpSession.writeCookies(ostream)
        # print "Cookie Header Line"
        # self.httpSession.sendCookies(ostream, URLSpec(self.URLtoSend))

    def run(self):

        # Here is where the new Panda based HTTP code starts

        # But before we hit the URL, let make sure we need to.
        # Lets check to see if the VRS Collector is OFFLINE and
        # host type 0 was selected. If that is the case, we can just
        # return here; nothing needs to be done.

        if self.CurrentHost == 0 and patcherVer() == ['OFFLINE']:
            return

        # Hit the URL
        # The next line uses the Panda HTTP lib (blocking)
        # doc = self.httpSession.getDocument(URLSpec(self.URLtoSend))

        # Next line uses non-blocking

        self.nonBlock = self.httpSession.makeChannel(False)
        # nonBlock.setHttpTimeout(1)
        # nonBlock.setConnectTimeout(.5)
        # nonBlock.setBlockingConnect(False)
        # doc = nonBlock.getDocument(DocumentSpec(self.URLtoSend))
        self.nonBlock.beginGetDocument(DocumentSpec(self.URLtoSend))

        instanceMarker = str(random.randint(1,1000))

        instanceMarker = 'FunnelLoggingRequest-%s' % instanceMarker

        self.startCheckingAsyncRequest(instanceMarker)
        
        # That's it. The server should have recorded the hit
        # delete the object
        # del doc

        # print "The Funnel URL could not be accessed"
        # if (self.CurrentHost == 0):
        #    patcherVer('w','OFFLINE')
        # For testing, write out all cookies in memory
        # print "Cookies after Transaction"
        # self.httpSession.writeCookies(ostream)

        # Commented out the following, moved it to the taskMgr call
        # if self.CurrentHost == 1 or self.CurrentHost == 2:
            # self.updateInstanceCookieValues()
            # self.writeOutPandaCookie()
            
        # Now lets do a check to see if the string LEAK is in the milestone
        # If LEAK is present, then we will also call the memory leak report
        # function to submit a report.

        # if self.milestone.find('LEAK') != -1:
           # reportMemoryLeaks()

    def startCheckingAsyncRequest(self, name):
        taskMgr.remove(name)
        # print "Starting Checking Async Request"
        taskMgr.doMethodLater(0.5, self.pollFunnelTask, name)

    def stopCheckingFunnelTask(self, name):
        taskMgr.remove('pollFunnelTask')

    def pollFunnelTask(self, task):
        # print "Polling....."
        result = self.nonBlock.run()
        if result == 0:
            # print "Result = 0, Done"
            # Funnel request complete
            self.stopCheckingFunnelTask(task)
            if self.CurrentHost == 1 or self.CurrentHost == 2:
                self.updateInstanceCookieValues()
                self.writeOutPandaCookie()
        else:
            return Task.again

def logSubmit(setHostID, setMileStone):

    # Autopilot. Just run logSubmit passing it the service ID and the milestone id. It will do the rest
    if __dev__:
         # print "UserFunnel: Game running in Dev Mode. Not logging to Hitbox or VRS Collector."
        assert notify.debug('UserFunnel: Game running in Dev Mode. Not logging to Hitbox or VRS Collector.')
        return
    if __debug__:
        # print "UserFunnel: Game running in Debug Mode. Not logging to Hitbox or VRS Collector"
        assert notify.debug('UserFunnel: Game running in Debug Mode. Not logging to Hitbox or VRS Collector.')
        return

    trackItem = UserFunnel()
    trackItem.setmilestone(quote_plus(setMileStone))
    trackItem.setHost(setHostID)
    trackItem.prerun()
    # trackItem.start()
    trackItem.run()
    # del trackItem
    # print 'Hitbox logging executed: ' + setMileStone

def getVRSFunnelURL():
    # Autopilot to get the funnel URL
    a = UserFunnel()
    a.getFunnelURL()

class HitBoxCookie:
    def __init__(self):
        # print 'UserFunnel: Created New HitBoxCookie Object'
        # Cookie file path and cookie file names
        self.ieCookieDir = os.getenv('USERPROFILE') + '\\Cookies'
        self.pythonCookieFile = 'cf.txt'
        self.hitboxCookieFile = None
        self.ehgdigCookieFile = None

        # HitBox Account Numbers
        # DOL test account = DM510925KJWE
        # Pirates Account = DM560804E8WD
        # ToonTown Account = DM53030620EW

        self.hitboxAcct = 'DM53030620EW'

        # Data for the hitbox cookies.
        # Once extracted each item will be a list of three items.

        self.ctg = None
        self.wss_gw = None
        #self.dm560804E8WD = None
        self.dmAcct = None

        # Header for Python Cookie files
        self.pythonCookieHeader = '    # Netscape HTTP Cookie File\n    # http://www.netscape.com/newsref/std/cookie_spec.html\n    # This is a generated file!  Do not edit.\n\n'

    def returnIECookieDir(self):
        return self.ieCookieDir

    def findIECookieFiles(self):
        try:
            sdir = os.listdir(self.ieCookieDir)
        except WindowsError:
            print 'Dir does not exist, do nothing'
            return
            
        while sdir:
            temp = sdir.pop()
            if (temp.find('@hitbox[') != -1):
                self.hitboxCookieFile = temp
            if (temp.find('@ehg-dig.hitbox[') != -1):
                self.ehgdigCookieFile = temp
        if (self.hitboxCookieFile != None and self.ehgdigCookieFile != None):
            # print 'UserFunnel: Both Files Have been located'
            return 1
        if (self.hitboxCookieFile == None and self.ehgdigCookieFile == None):
            # print 'UserFunnel: Error, neither file was located'
            return 0
        else:
            # print 'UserFunnel: At least one cookie file was located'
            return -1

    def openHitboxFile(self, filename, type = 'python'):
        # If the type passed is 'ie', then the opener assumes that it should
        # prefix the filename with the cookie dir path
        if (type == 'ie'):
            fullfile = self.ieCookieDir + '\\' + filename
        else:
            fullfile = filename
        # print 'Opening ' + fullfile
        cf = open(fullfile, 'r')
        data = cf.read()
        cf.close()
        return data

    def splitIECookie(self,filestream):
        # Break up the cookie, by placing each domain entry into a different list item
        return filestream.split('*\n')

    def sortIECookie(self,filestreamListElement):
        return [filestreamListElement.split('\n')[2],filestreamListElement.split('\n')[0],filestreamListElement.split('\n')[1]]

    def sortPythonCookie(self,filestreamListElement):
        return [filestreamListElement.split('\t')[0], filestreamListElement.split('\t')[5], filestreamListElement.split('\t')[6]]

    # Writing to the IE CookieJar will require the preservation of other hitbox related entries.

    def writeIEHitBoxCookies(self):
        if ( self.ctg == None or self.wss_gw == None or self.dmAcct ==None):
            # print 'UserFunnel: Error: CTG, WSS, or DM vars are not populated'
            return
        if (sys.platform != 'win32'):
            # print 'Not Windows'
            return
        # First we need to get the path to the cookiejar
        # In case it hasn't been executed already, we'll run it again to
        # location the two hitbox related cookie files we need to work with.
        self.findIECookieFiles()
        # First, we'll start with the ehg-dig file.
        # This file has the dm560804E8WD entry
        iecData = self.openHitboxFile(self.ehgdigCookieFile, 'ie')
        iecData = iecData.split('*\n')
        x = 0
        while (x < len(iecData)):
            if iecData[x].find(self.hitboxAcct) != -1:
                # We've located the entry we need to modify
                # print 'DM Found'
                iecData.pop(x)
                print 'Removed it from the list'
                break
            x += 1
        # Now we need to write the list back out to file.
        iecWrite = open(self.ieCookieDir + '\\' + self.ehgdigCookieFile, 'w')
        while iecData:
             # iecWrite.write(iecData.pop() + '*\n')
             iecBuffer = (iecData.pop() + '*\n')
             iecBuffer = iecBuffer.strip('/')
             if (iecBuffer[0] == '.'):
                 iecBuffer = iecBuffer[1:]
             iecWrite.write(iecBuffer)
        tempDMBUFFER = self.dmAcct[0]
        if tempDMBUFFER[0].find('.') == 0:
            tempDMBUFFER = tempDMBUFFER[1:]
        iecWrite.write(self.dmAcct[1] + '\n' + self.dmAcct[2] + '\n' + tempDMBUFFER + '/\n*\n')
        iecWrite.close()

        # Now on to the other file. From what I can tell self.hitboxCookieFile is safe to overwrite completly with the CTG and WSS_GW values.

        del iecData
        del iecWrite
        del iecBuffer
        iecWrite = open(self.ieCookieDir + '\\' + self.hitboxCookieFile, 'w')
        iecBuffer = self.ctg[0]
        if (iecBuffer[0] == '.'):
            iecBuffer = iecBuffer[1:]
        if (iecBuffer.find('/') == -1):
            iecBuffer = iecBuffer + '/'
        iecWrite.write(self.ctg[1] + '\n' + self.ctg[2] + '\n' + iecBuffer + '\n*\n')
        iecWrite.write(self.wss_gw[1] + '\n' + self.wss_gw[2] + '\n' + iecBuffer + '\n*\n')
        iecWrite.close()
        
        

    # This will write a python cookie file. Unless specified when called, the file will be called cf.txt. This is the old function, based on the netscape HTTP cokie format. 

    def OLDwritePythonHitBoxCookies(self, filename = 'cf.txt'):
        if ( self.ctg == None or self.wss_gw == None or self.dmAcct ==None):
            # print 'UserFunnel: Error: CTG, WSS, or DM vars are not populated'
            return
        outputfile = open(filename,'w')
        # First we can write out the header
        
        outputfile.write(self.pythonCookieHeader)
        
        # Next the domain, for the first entry. Note: the IE cookie files have a '/' after the domain name, while the python (Netscape HTTP format) does not. We need to check for the slash and strip it out before writing to the file

        outputfile.write('.' + self.dmAcct[0].strip('/') + '\tTRUE\t/\tFALSE\t9999999999\t' + self.dmAcct[1] + '\t' + self.dmAcct[2] + '\n')
        # Now the second
        outputfile.write('.' + self.ctg[0].strip('/') + '\tTRUE\t/\tFALSE\t9999999999\t' + self.ctg[1] + '\t' + self.ctg[2] + '\n')
        # And the third
        outputfile.write('.' + self.wss_gw[0].strip('/') + '\tTRUE\t/\tFALSE\t9999999999\t' + self.wss_gw[1] + '\t' + self.wss_gw[2] + '\n')
        outputfile.close()
        
    def writePythonHitBoxCookies(self, filename = 'cf.txt'):
        if ( self.ctg == None or self.wss_gw == None or self.dmAcct ==None):
            # print 'UserFunnel: Error: CTG, WSS, or DM vars are not populated'
            return
        outputfile = open(filename,'w')
        # First we can write out the header
        
        # outputfile.write(self.pythonCookieHeader)
        
        # Next the domain, for the first entry. Note: the IE cookie files have a '/' after the domain name, while the python (Netscape HTTP format) does not. We need to check for the slash and strip it out before writing to the file

        outputfile.write('.' + self.dmAcct[0].strip('/') + '\t/\t' + self.dmAcct[1] + '\t' + self.dmAcct[2] + '\n')
        # Now the second
        outputfile.write('.' + self.ctg[0].strip('/') + '\t/\t' + self.ctg[1] + '\t' + self.ctg[2] + '\n')
        # And the third
        outputfile.write('.' + self.wss_gw[0].strip('/') + '\t/\t' + self.wss_gw[1] + '\t' + self.wss_gw[2] + '\n')
        outputfile.close()

        


    # This will load the python cookies

    def loadPythonHitBoxCookies(self):
        if (os.path.isfile(self.pythonCookieFile) != 1):
            # print 'The python cookie file does not exist.'
            return
        pythonStandard = self.openHitboxFile(self.pythonCookieFile, 'python')
        # print pythonStandard
        # Now split the file at the \n\n, and pop off the second element. This will remove the header
        pythonStandard = pythonStandard.split('\n\n').pop(1)
        # Now split the second element into lines; each line is a cookie entry
        pythonStandard = pythonStandard.split('\n')
        # Now, we will locate the line with the DM, CTG, and WSS var
        for x in pythonStandard:
            if (x.find('\t' + self.hitboxAcct) != -1):
                # print self.hitboxAcct
                self.dmAcct = self.sortPythonCookie(x)
            if (x.find('\tCTG\t') != -1):
                # print 'CTG Found'
                self.ctg = self.sortPythonCookie(x)
            if (x.find('\tWSS_GW\t') != -1):
                # print 'WSS_GW Found'
                self.wss_gw = self.sortPythonCookie(x)

    # This function will locate the IE hitbox cookies (relating to Pirates), and place them in the proper list variable
    
    def loadIEHitBoxCookies(self):
        if (self.findIECookieFiles() != 1):
            # print 'UserFunnel: Error! One or both of the IE cookie files could not be loaded.'
            return
        
        if (sys.platform != 'win32'):
            # print 'Not Windows'
            return
        
        hitboxStandard = self.openHitboxFile(self.hitboxCookieFile, 'ie')
        hitboxDIG = self.openHitboxFile(self.ehgdigCookieFile, 'ie')

        hitboxStandard = self.splitIECookie(hitboxStandard)
        hitboxDIG = self.splitIECookie(hitboxDIG)

        # Now we need to locate the CTG and WSS_GW variable
        ctg = None
        wss = None
        for x in hitboxStandard:
            if (x.find('CTG\n') != -1):
                # print 'CTG Found'
                ctg = x
            if (x.find('WSS_GW\n') != -1):
                # print 'WSS_GW Found'
                wss = x
        if (ctg == None or wss == None):
            # print 'Both Cookie Values in hitbox could not be found'
            return

        # Now locate the pirates account number in ehg-dig.hitbox file
        DM = None
        for x in hitboxDIG:
            if (x.find(self.hitboxAcct) != -1):
                # print 'DM560804E8WD account found in cookie'
                DM = x
        if (DM == None):
            # print 'DM Cookie Value in ehg-dig.hitbox could not be found'
            return

        # Now split the streams into 3 elements of a list

        self.ctg = self.sortIECookie(ctg)
        self.wss_gw = self.sortIECookie(wss)
        self.dm560804E8WD = self.sortIECookie(DM)

        
        

# This should convert HitBox cookies generated by MS-IE (AKA the ActiveX and Launcher on Win32 systems), to the Netscape/Mozilla format that python needs

def convertHitBoxIEtoPython():
    if (sys.platform != 'win32'):
        print "Cookie Converter: Warning: System is not MS-Windows. I have not been setup to work with other systems yet. Sorry " + sys.platform + " user. The game client will create a cookie."
        return
    if __dev__:
        return
    if __debug__:
        return
    # There are two IE cookie files that we need to extract from
    # username@ehg-dig.hitbox[n].txt and username@hitbox[n].txt
    # Once we have the data from each, we need to merge them into cf.txt

    a = HitBoxCookie()
    a.loadIEHitBoxCookies()
    a.writePythonHitBoxCookies()
    del a

# This will convert back the other way. Python to IE

def convertHitBoxPythontoIE():
    if (sys.platform != 'win32'):
        print "System is not MS-Windows. I have not been setup to work with other systems yet. Sorry " + sys.platform + " user."
        return

    # Next, if the cookiefile already exists, then we don't have to convert it from IE to python.

    if(os.path.isfile('cf.txt') == True):
        return

    a = HitBoxCookie()
    a.loadPythonHitBoxCookies()
    a.writeIEHitBoxCookies()
    del a

def getreg(regVar):
    if (sys.platform != 'win32'):
        print "System is not MS-Windows. I haven't been setup yet to work with systems other than MS-Win using MS-Internet Explorer Cookies"
        return ''
    # Site to scan for cookie from

    siteName = 'toontown.online.disney'

    # Next, get the USERPROFILE dir

    cookiedir = os.getenv('USERPROFILE') + '\\Cookies'

    # make sdir a list of file in the cookiedir

    sdir = os.listdir(cookiedir)
    wholeCookie = None
    while sdir:
        temp = sdir.pop()
        if (temp.find(siteName) != -1):
            wholeCookie = temp
            break
    if (wholeCookie == None):
        print "Cookie not found for site name: " + siteName
        return ''
    CompleteCookiePath = cookiedir + '\\' + wholeCookie
    cf = open(CompleteCookiePath, 'r')

    # data will contain the complete contents of the cookie file

    data = cf.read()

    # Close the file

    cf.close()

    # Delete reference

    del cf

    # Change a few chars
    
    data = data.replace('%3D','=')
    data = data.replace('%26','&')

    # Attempt to locate the variable

    regNameStart = data.find(regVar)
    if (regNameStart == -1):
        return ''
    regVarStart = data.find('=',regNameStart + 1)
    regVarEnd = data.find('&',regNameStart + 1)
    return data[regVarStart+1: regVarEnd]

# getMAC() should allow for the MAC and IP address to be extracted from the NIC
# This should be a unique identifier. Function currently returns the MAC
# For MS-Windows, we attempt to locate the first Local Area Connection, then return that MAC.
# For OSX, we take the first MAC address listed in the system profiler.

def getMAC(staticMAC = [None]):
    
   if staticMAC[0] == None:
    if (sys.platform == 'win32'):
        correctSection = 0
        # curr_ip = socket.gethostbyname(socket.gethostname())
        try:
            ipconfdata = os.popen('/WINDOWS/SYSTEM32/ipconfig /all').readlines()
        except:
            # Could not get MAC address due to lack of execute permissions
            # on the ipconfig program. (Most likely a Vista issue)
            # print "MAC ADDRESS Recovery Problm"
            staticMAC[0] = 'NO_MAC'
            return staticMAC[0]
            
        for line in ipconfdata:
            if line.find('Local Area Connection') >= 0:
                correctSection = 1
            if line.find('Physical Address') >= 0 and correctSection == 1:
                pa = line.split(':')[-1].strip()
                correctSection = 0
                staticMAC[0] = pa
                return pa


    if (sys.platform == 'darwin'):
        # curr_ip = socket.gethostbyname(socket.gethostname())        
        macconfdata = os.popen('/usr/sbin/system_profiler SPNetworkDataType |/usr/bin/grep MAC').readlines()
        result = '-1'
        if macconfdata:
            if (macconfdata[0].find('MAC Address') != -1):
                pa = macconfdata[0][macconfdata[0].find(':') + 2 : macconfdata[0].find(':') + 22].strip('\n')
                staticMAC[0] = pa.replace(':','-')
                result = staticMAC[0]
        return result
                

    if (sys.platform != 'darwin' and sys.platform != 'win32'):
        print "System is not running OSX or MS-Windows."
        return '-2'

   else:

       return staticMAC[0]

def firstRun(operation = 'read', newPlayer = None, newPlayerBool = [False]):
    if (operation != 'read'):
        if (len(newPlayerBool) != 0):
            newPlayerBool.pop()
        newPlayerBool.append(newPlayer)
    return newPlayerBool[0]

def patcherVer(operation = 'read', url = None,  patchfile=[]):
    if (operation != 'read'):
        if (len(patchfile) != 0):
            patchfile.pop()
        patchfile.append(url)
    return patchfile

def loggingAvID(operation = 'read', newId = None, localAvId = [None]):
    if operation == 'write':
        localAvId[0] = newId
    else:
        return localAvId[0]

def loggingSubID(operation = 'read', newId = None, localSubId = [None]):
    if operation == 'write':
        localSubId[0] = newId
    else:
        return localSubId[0]

def vconGroup(operation = 'read', group = None, staticStore=[]):
    if (operation != 'read'):
        if (len(staticStore) != 0):
            staticStore.pop()
        staticStore.append(group)
    try:
        return staticStore[0]
    except IndexError:
        return None

def printUnreachableLen():
  # check memory on memory leaks
  import gc
  gc.set_debug(gc.DEBUG_SAVEALL)
  gc.collect()
  unreachableL = []
  for it in gc.garbage:
    unreachableL.append(it)
  return len(str(unreachableL))

def printUnreachableNum():
    # Check memory and return number of unreachable objects
    import gc
    gc.set_debug(gc.DEBUG_SAVEALL)
    gc.collect()
    return len(gc.garbage)

    
def reportMemoryLeaks():
    # First check to make sure we are leaking, if number of leaks = 0, we can return
    if printUnreachableNum() == 0:
        return


    # If we made it this far, then some sort of leaking has happened.
    # For this, we will need the bz2(compression), gc(access to garbage list) modules

    import bz2, gc
    # import httplib

    gc.set_debug(gc.DEBUG_SAVEALL)
    gc.collect()
    uncompressedReport = ''
    for s in gc.garbage:
        try:
            uncompressedReport += str(s) + '&'
        except TypeError:
            # __repr__ is probably trying to return a non-string
            pass
    reportdata = bz2.compress(uncompressedReport, 9)
    
    headers = {"Content-type": "application/x-bzip2", "Accept": "text/plain"}
    # Need to split patcherVer()[0] to just get the base url and port
    try:
        baseURL = patcherVer()[0].split('/lo')[0]
    except IndexError:
        print 'Base URL not available for leak submit'
        return
    basePort = 80
    if baseURL.count(':') == 2:
        basePort = baseURL[-4:]
        baseURL = baseURL[:-5]
    baseURL = baseURL[7:]

    if basePort != 80:
        finalURL = 'http://' + baseURL + ':' + str(basePort) + '/logging/memory_leak.php?leakcount=' + str(printUnreachableNum())
    else:
        finalURL = 'http://' + baseURL + '/logging/memory_leak.php?leakcount=' + str(printUnreachableNum())
    reporthttp = HTTPClient()
    reporthttp.postForm(URLSpec(finalURL), reportdata)

    return

def checkParamFile():
# checkParamFile will check to see if the parameters.txt file exists
# If it does, then the file is read in. If the 'PATCHER_BASE_URL' is found
# then the value after the =, is returned. If the file does not exist or the
# file does not contain the PATCHER_BASE_URL, then None is returned.
 if os.path.exists('parameters.txt') == 1:
    paramfile = open('parameters.txt', 'r')
    contents = paramfile.read()
    paramfile.close()
    del paramfile
    contents = contents.split('\n')
    newURL = ''
    while contents:
        checkLine = contents.pop()
        if checkLine.find('PATCHER_BASE_URL=') != -1 and checkLine[0] == 'P':
            newURL = checkLine.split('=')[1]
            # Just in case a space exists after the =, we should remove whitespace from the element
            newURL = newURL.replace(' ','')
            break
    if newURL == '':
        #print 'Parameters.txt did not contain a new PATCHER_BASE_URL'
        return
    else:
        #print 'Parameters.txt does have a new base url'
        return newURL + 'patcher.ver'
 # parameters.txt file not found
 return
