import socket
import datetime
import os
import pytz
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.http.WebRequest import WebRequestDispatcher
from otp.distributed import OtpDoGlobals
from toontown.toonbase import ToontownGlobals
from toontown.uberdog import InGameNewsResponses
from toontown.ai.ToontownAIMsgTypes import IN_GAME_NEWS_MANAGER_UD_TO_ALL_AI 

class DistributedInGameNewsMgrUD(DistributedObjectGlobalUD):
    """
    Uberdog object that keeps track of the last time in game news has been updated
    """
    notify = directNotify.newCategory('DistributedInGameNewsMgrUD')
    serverDataFolder = simbase.config.GetString('server-data-folder', "")

    # WARNING this is a global OTP object
    # InGameNewsMgrAI is NOT!
    # Hence the use of sendUpdateToDoId when sending back to AI
     

    def __init__(self, air):
        """Construct ourselves, set up web dispatcher."""
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.__init__(self, air)
        self.HTTPListenPort = uber.inGameNewsMgrHTTPListenPort

        self.webDispatcher = WebRequestDispatcher()
        self.webDispatcher.landingPage.setTitle("InGameNewsMgr")
        self.webDispatcher.landingPage.setDescription("InGameNews is update when a new issue of in-game-news is out.")
        self.webDispatcher.registerGETHandler('inGameNewsMgr', self.inGameNewsMgr)
        self.webDispatcher.registerGETHandler('inGameNewsNewIssue', self.inGameNewsNewIssue)
        self.webDispatcher.listenOnPort(self.HTTPListenPort)
        self.webDispatcher.landingPage.addTab("InGameNewsMgr","/inGameNewsMgr")

        self.air.setConnectionName("InGameNewsMgr")
        self.air.setConnectionURL("http://%s:%s/" % (socket.gethostbyname(socket.gethostname()),self.HTTPListenPort))

        self.filename = self.getFilename()
        self.latestIssue = datetime.datetime.now()
        self.latestIssue = self.loadRecords()

    def getLatestIssueStr(self):
        self.notify.debugStateCall(self)
        return self.latestIssue.strftime(self.air.toontownTimeManager.formatStr)

    def getLatestIssueUtcStr(self):
        self.notify.debugStateCall(self)
        datetimeInUtc = self.latestIssue.astimezone(pytz.utc)
        result = datetimeInUtc.strftime(self.air.toontownTimeManager.formatStr)
        return result
        
    def announceGenerate(self):
        """Start accepting http requests."""
        assert self.notify.debugCall()
        DistributedObjectGlobalUD.announceGenerate(self)
        self.b_setLatestIssue(self.latestIssue)
        self.webDispatcher.startCheckingIncomingHTTP()

    def inGameNewsMgr(self, replyTo, **kw):
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

    def inGameNewsNewIssue(self, replyTo, **kw):
        try:
            newIssue = self.air.toontownTimeManager.getCurServerDateTime()                        
            self.b_setLatestIssue(newIssue)
            self.updateRecordFile()
            replyTo.respondXML(InGameNewsResponses.setLatestIssueSuccessXML % (self.getLatestIssueStr()))
            
            pass
        except Exception,e:
            replyTo.respondXML(InGameNewsResponses.setLatestIssueFailureXML  % ("Catastrophic failure setting latest issue %s" % str(e)))
            pass


    def getMainMenu(self):
        """Create the main menu with forms for input."""
        header = """<HTML><HEAD><TITLE>Main Menu: In Game News Mgr</TITLE><link rel="stylesheet" type="text/css" href="/default.css">
        </HEAD>"""

        body = """<BODY><div id="contents"><center><P>"""
        body += """
            Latest Issue = """
        body += self.getLatestIssueStr()
        body += """
            <br>
            <form name="myform" action="inGameNewsNewIssue">
            <input type="submit" value="New Issue Released" />
            </form>            
            """
            
        footer = """</tbody></table></P></center></div><div id="footer">Toontown In Game News</div></BODY></HTML>"""
        help = """<table height = "15%"></table><P><table width = "60%"><caption>Note</caption><tr><th scope=col>- Click on the button when a new issue of in game news has been released.</th></tr></table></P>"""
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
            file.write(self.getLatestIssueStr())
            file.close()
            if os.path.exists(backup):
                os.remove(backup)
        except EnvironmentError:
            self.notify.warning(str(sys.exc_info()[1]))
        
    def getFilename(self):
        """Compose the track record filename"""
        return "%s.latestissue" % (self.serverDataFolder)

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
                # OK, there's no file.  Grab the default times.
                return self.getDefaultLatestIssueTime()
        file.seek(0)
        result = self.loadFrom(file)
        file.close()

        return result 

    def loadFrom(self, file):
        """Load track record data from specified file"""
        result = self.air.toontownTimeManager.getCurServerDateTime()        
        try:
            latestIssueStr = file.readline()
            result = self.air.toontownTimeManager.convertStrToToontownTime(latestIssueStr)
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
        self.sendUpdateToAllAis('newIssueUDtoAI', [ self.getLatestIssueUtcStr()])

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
    
