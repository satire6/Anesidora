import urllib
import socket
import datetime
import os
import pytz
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.http.WebRequest import WebRequestDispatcher
from otp.distributed import OtpDoGlobals
from otp.ai import BanManagerAI
from toontown.toonbase import ToontownGlobals
from toontown.uberdog import InGameNewsResponses
from toontown.ai.ToontownAIMsgTypes import IN_GAME_NEWS_MANAGER_UD_TO_ALL_AI


class DistributedCpuInfoMgrUD(DistributedObjectGlobalUD):
    """
    Uberdog object is more properly called the Security / Ban Manager

    Called Cpu Info for obfuscation as it is in toon.dc
    """
    notify = directNotify.newCategory('DistributedCpuInfoMgrUD')
    serverDataFolder = simbase.config.GetString('server-data-folder', "")

    # WARNING this is a global OTP object
    # InGameNewsMgrAI is NOT!
    # Hence the use of sendUpdateToDoId when sending back to AI

    securityBanMgrFailureXML = """
    <securityBanMgrResponse>
    <success>false</success>
    <error>%s</error>
    </securityBanMgrResponse>
    \r\n"""

    securityBanMgrAddFingerprintXML = """
    <securityBanMgrAddResponse>
    <success>true</success>
    <fingerprint>%s</fingerprint>
    </securityBanMgrAddResponse>
    \r\n"""    

    securityBanMgrRemoveFingerprintXML = """
    <securityBanMgrRemoveResponse>
    <success>true</success>
    <fingerprint>%s</fingerprint>
    </securityBanMgrRemoveResponse>
    \r\n"""    

     

    def __init__(self, air):
        """Construct ourselves, set up web dispatcher."""
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)
        self.HTTPListenPort = uber.cpuInfoMgrHTTPListenPort

        self.webDispatcher = WebRequestDispatcher()
        self.webDispatcher.landingPage.setTitle("SecurityBanMgr")
        self.webDispatcher.landingPage.setDescription("SecurityBanMgr for now handles banning my mac address.")
        self.webDispatcher.registerGETHandler('securityBanMgr', self.securityBanMgr)
        self.webDispatcher.registerGETHandler('securityBanMgrAddFingerprint', self.addFingerprint)
        self.webDispatcher.registerGETHandler('securityBanMgrRemoveFingerprint', self.removeFingerprint)
        self.webDispatcher.registerGETHandler('securityBanMgrListFingerprints', self.listFingerprints)
        self.webDispatcher.listenOnPort(self.HTTPListenPort)
        self.webDispatcher.landingPage.addTab("SecurityBanMgr","/securityBanMgr")

        self.air.setConnectionName("SecurityBanMgr")
        self.air.setConnectionURL("http://%s:%s/" % (socket.gethostbyname(socket.gethostname()),self.HTTPListenPort))

        self.filename = self.getFilename()

        self.bannedFingerprints = set()
        self.bannedFingerprints = self.loadRecords()
        self.banMgr = BanManagerAI.BanManagerAI()


    def setCpuInfoToUd(self, avId, dislId, cpuInfo, cacheStatus):
        """AI telling us a client just logged in."""
        if cacheStatus in self.bannedFingerprints:
            self.notify.info("got a banned fingerprint %s for avId=%s dislId=%s" % (cacheStatus, avId, dislId))
            self.banMgr.ban(avId, dislId, "banned macId, fingerprint is  %s" % cacheStatus)
            pass        
       
    def announceGenerate(self):
        """Start accepting http requests."""
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        self.webDispatcher.startCheckingIncomingHTTP()

    def securityBanMgr(self, replyTo, **kw):
        """Handle all calls to web requests awardMgr."""
        assert self.notify.debugCall()
        
        # If no arguments are passed, assume that the main menu should
        # be displayed

        if not kw:
            function = None
            id = None
        else:
            function = "doAward"

        header = body = help = footer = ""
        if not function:
            header,body,footer,help= self.getMainMenu()
        else:
            self.notify.debug("%s" % str(kw))
            header,body,footer,help= self.getMainMenu()
            body = """<BODY><div id="contents"><center><P>got these arguments """
            body += str(kw)
            
        #self.notify.info("%s" % header + body + help + footer)
        replyTo.respond(header + body + help + footer)


    def getMainMenu(self):
        """Create the main menu with forms for input."""
        header = """<HTML><HEAD><TITLE>Main Menu: In Game News Mgr</TITLE><link rel="stylesheet" type="text/css" href="/default.css">
        </HEAD>"""

        body = """<BODY><div id="contents"><center><P>"""

        body += """
            <br>
            <form name="addFingerprintForm" action="securityBanMgrAddFingerprint">
            <input type="text" name="fingerprintToAdd" value="">
            <input type="submit" value="Add Fingerprint" />
            </form>
            """

        body += """
            <br>
            <form name="removeFingerprintForm" action="securityBanMgrRemoveFingerprint">
            <input type="text" name="fingerprintToRemove" value="">
            <input type="submit" value="Remove Fingerprint" />
            </form>
            """

        body += """
            <br>
            <form name="listFingerprintsForm" action="securityBanMgrListFingerprints">
            <input type="submit" value="List Fingerprints" />
            </form>            
            """            
            
        footer = """</tbody></table></P></center></div><div id="footer">Security Ban Mgr</div></BODY></HTML>"""
        help = """<table height = "15%"></table><P><table width = "60%"><caption>Note</caption><tr><th scope=col>- Use add to add ONE fingerpint that's autobanned. Use remove to take ONE fingerprint out. And use list to see them all.</th></tr></table></P>"""
        return (header,body,footer,help)


    def updateRecordFile(self):
        """Update current track record in this shard's record file"""
        # notify the leader boards that there has been an update
        try:
            backup = self.filename + '.bu'
            if os.path.exists(self.filename):
                os.rename(self.filename, backup)
            file = open(self.filename, 'w')
            file.seek(0)
            for fingerprint in self.bannedFingerprints:
                file.write(fingerprint + '\n')
            file.close()
            if os.path.exists(backup):
                os.remove(backup)
        except EnvironmentError:
            self.notify.warning(str(sys.exc_info()[1]))
        
    def getFilename(self):
        """Compose the track record filename"""
        result = "%s.bannedFingerprints" % (self.serverDataFolder)
        return result

    def getDefaultLatestIssueTime(self):
        """Hmmm what the heck do we give. Lets use the current time."""
        result = self.air.toontownTimeManager.getCurServerDateTime()
        return result

    def loadRecords(self):
        """Load track record data from default location"""
        try:
            # Try to open the backup file:
            file = open(self.filename + '.bu', 'r')
            # Remove the (assumed) broken file:
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except IOError:
            # OK, there's no backup file, good.
            try:
                # Open the real file:
                file = open(self.filename, 'r')
            except IOError:
                # OK, there's no file.  Grab the default empty set.
                return set()
        file.seek(0)
        result = self.loadFrom(file)
        file.close()

        return result 

    def loadFrom(self, file):
        """Load banned fingerprint record data from specified file"""        
        result = set()
        try:
            for oneFingerprint in file:
                oneFingerprint = oneFingerprint.strip()
                if oneFingerprint:
                    result.add(oneFingerprint)
        except EOFError:
            pass
        return result

    def setLatestIssueStr(self, issueStr):
        self.notify.debugStateCall(self)

  
    def setLatestIssue(self, latestIssue):
        self.latestIssue = latestIssue

    def b_setLatestIssue(self, latestIssue):
        self.setLatestIssue(latestIssue)
        self.d_setLatestIssue(latestIssue)
        
    def d_setLatestIssue(self, latestIssue):
        pass
        #self.sendUpdateToAllAis('newIssueUDtoAI', [ self.getLatestIssueUtcStr()])

    def sendUpdateToAllAis(self, message, args):
        dg = self.dclass.aiFormatUpdateMsgType(
                message, self.doId, self.doId, self.air.ourChannel, IN_GAME_NEWS_MANAGER_UD_TO_ALL_AI, args)
        self.air.send(dg)

    def inGameNewsMgrAIStartingUp(self,  doId,  shardId):
        """Tell the new AI that just started up what the latest issue is."""
        self.air.sendUpdateToDoId(
                "DistributedInGameNewsMgr",
                'newIssueUDtoAI',
                doId ,
                [self.getLatestIssueStr()]
            )


    def addFingerprint(self, replyTo, **kw):
        """Add a new fingerprint to auto ban."""
        try:
            fingerprint = urllib.unquote(kw['fingerprintToAdd'])
            self.bannedFingerprints.add(fingerprint)
            self.updateRecordFile()
            header,body,footer,help= self.getMainMenu()
            replyTo.respondXML(self.securityBanMgrAddFingerprintXML %
                               ("%s" % fingerprint))
            
        except Exception, e:
            replyTo.respondXML(self.securityBanMgrFailureXML %
                               ("Catastrophic failure add fingerprint %s" % str(e)))
            self.notify.warning("Got exception %s" % str(e))


    def removeFingerprint(self, replyTo, **kw):
        """Remove a fingerprint to auto ban."""
        try:
            fingerprint = urllib.unquote(kw['fingerprintToRemove'])
            if fingerprint in self.bannedFingerprints:
                self.bannedFingerprints.remove(fingerprint)
                self.updateRecordFile()
                header,body,footer,help= self.getMainMenu()
                replyTo.respondXML(self.securityBanMgrRemoveFingerprintXML %
                                   ("%s" % fingerprint))
            else:
                replyTo.respondXML(self.securityBanMgrFailureXML % ("%s not a banned fingerprint" % fingerprint))
        except Exception, e:
            replyTo.respondXML(self.securityBanMgrFailureXML %
                               ("Catastrophic failure add fingerprint %s" % str(e)))
            self.notify.warning("Got exception %s" % str(e))  

    def listFingerprints(self, replyTo, **kw): 
        """List all banned fingerprints."""
        try:
            header,body,footer,help= self.getMainMenu()
            body = """<BODY><div id="contents"><center><P>"""
            body += """<h4>Banned Fingerprints:</h4>
            <table border="1">
            """
            for fingerprint in self.bannedFingerprints:
                body += "<tr><td>" + str(fingerprint) +  "</td>"+"</tr>\n"
            body += """
            </table>
            """        
            replyTo.respond(header +body+ help+footer)
        except Exception, e:
            replyTo.respondXML(self.securityBanMgrFailureXML % ("Catastrophic failure listing fingerprints %s" % str(e)))
            self.notify.warning("Got exception %s" % str(e))

        
        
