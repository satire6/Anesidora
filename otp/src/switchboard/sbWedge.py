import Pyro.core
import Pyro.naming
import Pyro.errors
import time
import sys

from Pyro.errors import ConnectionClosedError
from Pyro.errors import ProtocolError

from sbNode import sbNode
from sbLog import sbLog
import sbConfig

try:
    import badwordpy
    gotBadwordpy = True
except ImportError:
    gotBadwordpy = False
    class BadwordDummy:
        def __init__(self, *args):
            pass
        def test(self, word):
            return False
        def scrub(self, str):
            return str
    badwordpy = BadwordDummy()
        

class sbWedge(Pyro.core.SynchronizedObjBase):
    def __init__(self,wedgeName,
                 nodeName="",
                 nsHost=None,nsPort=None,
                 listenPort=None,
                 bcLocate=False,
                 clHost=None,clPort=None,
                 allowUnfilteredChat=0,
                 bwDictPath=""):
        Pyro.config.PYRO_MULTITHREADED = 0
        Pyro.config.PYRO_TRACELEVEL = 2

        Pyro.core.SynchronizedObjBase.__init__(self)
        Pyro.core.initServer(banner=0)

        self.log = sbLog(":sb.wedge.%s"%wedgeName,clHost,clPort)

        badwordpy.init(bwDictPath,"")

        if not badwordpy.test("fuck") and not allowUnfilteredChat:
            self.log.error("Dirty word filter not working, refusing to start.  Devs should add .prc setting 'allow-unfiltered-chat 1' to bypass.")
            raise Exception("No dirty word filter, aborting SB Wedge startup.  Devs should add .prc setting 'allow-unfiltered-chat 1' to bypass.")

        self.wedgeName = wedgeName
        if nodeName == "":
            self.nodeName = wedgeName
        else:
            self.nodeName = nodeName
            
        self.node = None

        self.log.info("Starting.")
        self.sbConnected = False

        self.nsHost = nsHost
        self.nsPort = nsPort
        
        try:
            self.initPyro(nsHost,nsPort,listenPort,bcLocate)

            self.updateNode()
            self.log.debug("Enter sendEnterWedge")
            self.sendEnterWedge()
            self.log.debug("Exit sendEnterWedge")
            self.sbConnected = True
        except Exception,e:
            self.log.warning("Failed to connect to Switchboard.  Player friends are being faked.")

        self.onlinePlayers = 0
        self.servedLogins = 0
        self.servedChat = 0           
        self.servedChatSC = 0
        self.servedMail = 0
        self.servedMailSC = 0
            
        self.log.info("-- sb.wedge.%s is ready. --" %self.wedgeName)

    def shutdown(self):
        self.sbConnected = False
        self.pyroDaemon.disconnect(self)
        self.log.info("shutdown() called.  Shutting down cleanly.")
        sys.stdout.flush()
        self.pyroDaemon.shutdown(True)
        
    #def log(self,message):
    #    #pass
    #    print ":sb.wedge.%s: %s" % (self.wedgeName,message)
    #    sys.stdout.flush()


    def initPyro(self,nsHost,nsPort,listenPort,bcLocate):
        if listenPort is not None:
            self.log.debug("Accepting requests on port %d."%listenPort)
            Pyro.config.PYRO_PORT = listenPort
            Pyro.config.PYRO_PORT_RANGE = 1

        self.pyroDaemon = Pyro.core.Daemon()
        
        if nsHost is None:
            if bcLocate is True:
                self.log.info("No NS host/port specified, trying location via broadcast.")
                self.nameServer = Pyro.naming.NameServerLocator().getNS()
            else:
                self.log.warning("No NS host/port specified and no broadcast enabled.  sbWedge not connecting to Switchboard.")
                return
        else:
            self.log.info("Connecting to NS at %s:%d." % (nsHost,nsPort))
            self.nameServer = Pyro.naming.NameServerLocator().getNS(host=nsHost,port=nsPort)
            
        self.pyroDaemon.useNameServer(self.nameServer)
        try:
            self.nameServer.createGroup(":sb")
            self.nameServer.createGroup(":sb.node")
            self.nameServer.createGroup(":sb.player")
            self.nameServer.createGroup(":sb.wedge")
        except Pyro.errors.NamingError:
            pass
        try:
            self.pyroDaemon.connectPersistent(self,":sb.wedge.%s"%self.wedgeName)
        except Pyro.errors.NamingError:
            self.log.debug(":sb.wedge.%s was already registered, overwriting old entry."%self.wedgeName)
            self.nameServer.unregister(":sb.wedge.%s"%self.wedgeName)
            self.pyroDaemon.connectPersistent(self,":sb.wedge.%s"%self.wedgeName)


    def handleRequests(self,timeout):
        if self.sbConnected:
            self.pyroDaemon.handleRequests(timeout)

    def requestLoop(self):
        if self.sbConnected:
            try:
                self.pyroDaemon.requestLoop()
            finally:
                self.pyroDaemon.shutdown(True)

    #---------------------------------
    # Node/Wedge Entry/Exit
    #---------------------------------

    def refreshNS(self):
        self.nameServer = Pyro.naming.NameServerLocator().getNS(host=self.nsHost,port=self.nsPort)
        self.pyroDaemon.useNameServer(self.nameServer)

    def sendEnterWedge(self):
        if self.node:
            try:
                self.node.recvEnterWedge(self.wedgeName)
            except Exception,e:
                self.log.warning("Error contacting my node (%s), node is None."%str(e))
                self.node = None

    def sendExitWedge(self):
        try:
            if self.node:
                self.node.recvExitWedge(self.wedgeName)
        except:
            pass
        
    def recvEnterNode(self,nodeName):
        self.log.debug("Received enterNode.")
        #send out players online etc
        self.nodeName = nodeName
        self.updateNode()

    def recvExitNode(self,nodeName):
        self.log.debug("Received exitNode.")
        self.nodeName = nodeName
        self.updateNode()

    def updateNode(self):
        self.log.debug("updateNode")
        try:
            self.refreshNS()
            self.node = Pyro.core.getProxyForURI(self.nameServer.resolve(":sb.node.%s"%self.nodeName))
            self.log.debug("gotProxyForNode")
            self.node._setOneway(["recvEnterWedge",
                                  "recvExitWedge",
                                  "recvEnterLocalPlayer",
                                  "recvExitLocalPlayer",
                                  "recvExitLocalAvatar",
                                  "addFriendship",
                                  "removeFriendship",
                                  "getToken",
                                  "redeemToken",
                                  "sendWhisper",
                                  "sendWLWhisper",
                                  "sendSCWhisper",
                                  "getMail",
                                  "sendMail",
                                  "sendWLMail",
                                  "sendSCMail",
                                  "deleteMail",
                                  "recvSecretRequest",
                                  "recvSecretRedeem",
                                  "recvOpenInvite",
                                  "recvDeclineInvite"])
            self.log.info("-- Connected to sb.node.%s. --" % self.nodeName)
            self.sbConnected = True
        except Exception,e:
            self.node = None
            self.sbConnected = False
            self.log.debug("Failed to locate sb.node.%s, node is None." % self.nodeName)
            self.log.debug(str(e))


    #---------------------------------------
    # Player Entry/Exit
    #---------------------------------------

    #app->wedge
    def enterPlayer(self,playerId,playerInfo):
        self.log.debug("Player %d entered." % (playerId))
        self.servedLogins += 1
        if self.node:
            try:
                self.node.recvEnterLocalPlayer(playerId,playerInfo)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in enterPlayer.  Refreshing node.")
                self.updateNode()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in enterPlayer.  Refreshing node."%str(e))
                self.updateNode()
            except Exception,e:
                self.log.error("Unknown error sending enterLocalPlayer to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))

    #app->wedge
    def exitPlayer(self,playerId):
        self.log.debug("Player %d exited." % (playerId))
        if self.node:
            try:
                self.node.recvExitLocalPlayer(playerId)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in exitPlayer.  Refreshing node.")
                self.updateNode()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in exitPlayer.  Refreshing node."%str(e))
                self.updateNode()
            except Exception,e:
                self.log.error("Error sending exitLocalPlayer to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))

    #app->wedge
    def exitAvatar(self,avatarId):
        self.log.debug("Avatar %d exited." % (avatarId))
        if self.node:
            try:
                self.node.recvExitLocalAvatar(avatarId)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in exitAvatar.  Refreshing node.")
                self.updateNode()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in exitAvatar.  Refreshing node."%str(e))
                self.updateNode()
            except Exception,e:
                self.log.error("Error sending exitLocalAvatar to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))


    #wedge->app, override
    def recvEnterRemotePlayer(self,playerId,playerInfo,friendsList):
        self.log.debug("Saw player %d enter."%(playerId))
        pass

    #wedge->app, override
    def recvExitRemotePlayer(self,playerId,friendsList):
        self.log.debug("Saw player %d exit."%(playerId))
        pass
        

    #---------------------------------------------
    # Friends
    #---------------------------------------------

    def addFriendship(self,playerId1,playerId2):
        if self.node:
            self.node.addFriendship(playerId1,playerId2)

    def removeFriendship(self,playerId1,playerId2):
        if self.node:
            self.node.removeFriendship(playerId1,playerId2)

    def sendOpenInvite(self,inviterId,inviteeId,secretYesNo=True):
        if self.node:
            self.log.debug("sendOpenInvite found node, sending request")
            self.node.recvOpenInvite(inviterId,inviteeId,secretYesNo)

    def sendDeclineInvite(self,senderId,otherId):
        if self.node:
            self.node.recvDeclineInvite(senderId,otherId)

    def sendSecretRequest(self,playerId,parentUsername=None,parentPassword=None):
        if self.node:
            try:
                self.node.recvSecretRequest(playerId,parentUsername,parentPassword)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in sendSecretRequest.  Refreshing node.")
                self.updateNode()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in sendSecretRequest.  Refreshing node.")
                self.updateNode()
            except Exception,e:
                self.log.error("Error sending secretRequest to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))

    def sendSecretRedeem(self,playerId,secret,parentUsername=None,parentPassword=None):
        if self.node:
            try:
                self.node.recvSecretRedeem(playerId,secret,parentUsername,parentPassword)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in sendSecretRedeem.  Refreshing node.")
                self.updateNode()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in sendSecretRedeem.  Refreshing node.")
                self.updateNode()
            except Exception,e:
                self.log.error("Error sending secretRedeem to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))

    #wedge->app, override
    def recvFriendsUpdate(self,playerId,friends):
        self.log.debug("Got friends update - OVERRIDE THIS!")
        pass

    def recvFriendshipRemoved(self,playerOne,playerTwo):
        self.log.debug("Got friendship removed - OVERRIDE THIS!")
        pass

    def recvAddFriendshipError(self,playerId,error):
        self.log.debug("Got friend add error back from SB - OVERRIDE THIS!")
        pass

    def recvSecretGenerated(self,playerId,secret):
        self.log.debug("Got secret token back from SB - OVERRIDE THIS!")
        pass

    def recvSecretRequestError(self,playerId,error):
        self.log.debug("Got secret error back from SB - OVERRIDE THIS!")
        pass

    def recvSecretRedeemError(self,playerId,error):
        self.log.debug("Got secret error back from SB - OVERRIDE THIS!")
        pass

    def recvInviteNotice(self,inviteeId,inviterId,inviterAvName):
        self.log.debug("Got recvInviteNotice from SB - OVERRIDE THIS!")
        pass

    def recvInviteRetracted(self,inviteeId,inviterId):
        self.log.debug("Got recvInviteRetracted from SB - OVERRIDE THIS!")
        pass

    def recvInviteRejected(self,inviterId,inviteeId,reason):
        self.log.debug("Got recvInviteRejected from SB - OVERRIDE THIS!")
        pass

    #---------------------------------------------
    # Whispers
    #---------------------------------------------

    #app->wedge
    def sendWhisper(self,recipientId,senderId,msgText):
        self.log.debug("sendWhisper %d->%d: %s" % (senderId,recipientId,msgText))
        if not self._validateChatMessage(recipientId,senderId,msgText):
            return

        if self.node:
            try:
                self.node.sendWhisper(recipientId,senderId,msgText)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in sendWhisper.  Refreshing node.")
                self.updateNode()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in sendWhisper.  Refreshing node."%str(e))
                self.updateNode()
            except Exception,e:
                self.log.error("Error sending whisper to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))

    #app->wedge
    def sendWLWhisper(self,recipientId,senderId,msgText):
        self.log.debug("sendWLWhisper %d->%d: %s" % (senderId,recipientId,msgText))
        if not self._validateChatMessage(recipientId,senderId,msgText):
            return

        if self.node:
            try:
                self.node.sendWLWhisper(recipientId,senderId,msgText)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in sendWLWhisper.  Refreshing node.")
                self.updateNode()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in sendWLWhisper.  Refreshing node."%str(e))
                self.updateNode()
            except Exception,e:
                self.log.error("Error sending WLwhisper to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))
            
    #app->wedge
    def sendSCWhisper(self,recipientId,senderId,msgText):
        self.log.debug("sendSCWhisper %d->%d: %s" % (senderId,recipientId,msgText))
        if not self._validateChatMessage(recipientId,senderId,msgText):
            return

        if self.node:
            try:
                self.node.sendSCWhisper(recipientId,senderId,msgText)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in sendSCWhisper.  Refreshing node.")
                self.updateNode()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in sendSCWhisper.  Refreshing node."%str(e))
                self.updateNode()
            except Exception,e:
                self.log.error("Error sending SCwhisper to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))
            
    #wedge->app, override
    def recvWhisper(self,recipientId,senderId,msgText):
        #msgText = badwordpy.scrub(msgText)
        self.log.debug("WHISPER %d to %d: %s"%(senderId,recipientId,msgText))
        pass

    #wedge->app, override
    def recvWLWhisper(self,recipientId,senderId,msgText):
        self.log.debug("sbWedge.recvWLWHISPER %d to %d: %s"%(senderId,recipientId,msgText))
        pass

    #wedge->app, override
    def recvSCWhisper(self,recipientId,senderId,msgText):
        self.log.debug("sbWedge.recvSCWHISPER %d to %d: %s"%(senderId,recipientId,msgText))
        pass

    #wedge->app, override
    def recvWhisperFailed(self,recipientId,senderId,msgText):
        self.log.debug("Received whisper fail notice for %d to %d: %s"%(senderId,recipientId,msgText))
        pass

    #wedge->app, override
    def recvSCWhisperFailed(self,recipientId,senderId,msgText):
        self.log.debug("Received SCwhisper fail notice for %d to %d: %s"%(senderId,recipientId,msgText))
        pass

    def _validateChatMessage(self,recipientId,senderId,msg):
        if len(msg) < 1 or len(msg) > sbConfig.chatMessageMaxChars:
            self.log.security("Invalid chat message length.  %d->%d: %s"%(recipientId,senderId,msg))
            return False

        return True


    #---------------------------------------------
    # Mail
    #---------------------------------------------
    
    def sendMail(self,recipientId,senderId,msgText):
        #CHECK FRIENDSHIP, permissions, ignore list, etc?
        try:
            self.servedMail += 1
            self.node.sendMail(recipientId,senderId,msgText)
        except Exception,e:
            self.log.error("Error sending mail to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))

    def sendWLMail(self,recipientId,senderId,msgText):
        self.log.debug("sbWedge.sendWLMAIL %d to %d: %s" % (senderId,recipientId,msgText))

        #CHECK FRIENDSHIP
        try:
            self.servedMail += 1
            self.node.sendSCMail(recipientId,senderId,msgText)
        except Exception,e:
            self.log.error("Error sending mail to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))

    def sendSCMail(self,recipientId,senderId,msgText):
        self.log.debug("sbWedge.sendSCMAIL %d to %d: %s" % (senderId,recipientId,msgText))

        #CHECK FRIENDSHIP
        try:
            self.servedMailSC += 1
            self.node.sendSCMail(recipientId,senderId,msgText)
        except Exception,e:
            self.log.error("Error sending mail to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))

    #wedge->app, override
    def recvMailUpdate(self,recipientId,senderId,msgText):
        self.log.debug("Received mail update for %d to %d: %s" % (senderId,recipientId,msgText))
        pass

    def recvMail(self,recipientId,mail):
        self.log.debug("Received mail for %d: %s" % (recipientId,mail))
        pass    

    def getMail(self,recipientId):
        self.log.debug("Requesting mail for %d"%recipientId)
        self.node.getMail(recipientId)

    def deleteMail(self,accountId,messageId):
        self.log.debug("User %d deleting message %d"%(accountId,messageId))

        try:
            self.node.deleteMail(accountId,messageId)
        except Exception,e:
            self.log.error("Error sending mail to my node: %s" % ''.join(Pyro.util.getPyroTraceback(e)))



    def healthCheck(self):
        return True

    def statCheck(self):     
        avgFriends = 0.0
        return {'onlinePlayers':self.onlinePlayers,
                'avgFriends':avgFriends,            
                'servedLogins':self.servedLogins,
                'servedChat':self.servedChat,
                'servedChatSC':self.servedChatSC,
                'servedMail':self.servedMail,
                'servedMailSC':self.servedMailSC}

    def getLogTail(self,numLines=None):
        if numLines is None:
            return self.log.getMemLog()                    
        else:
            return "numLInes!=NOne!"

