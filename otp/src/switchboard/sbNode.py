import Pyro.core
import Pyro.naming
import Pyro.errors
import sys
import time

from sbLog import sbLog
import sbConfig

from Pyro.errors import ConnectionClosedError
from Pyro.errors import ProtocolError

from otp.switchboard.xd.ChannelManager import ChannelListener
from otp.switchboard.xd.ChannelManager import ChannelMessage

if sbConfig.scrubMessages:
    import badwordpy
    badwordpy.init("","")

class sbNode(Pyro.core.SynchronizedObjBase,ChannelListener):
    def __init__(self,
                 nodeName,
                 wedgeName="",
                 nsHost=None,
                 nsPort=None,
                 listenPort=None,
                 clHost=None,
                 clPort=None,
                 chanMgr=None,
                 dislURL=None):
        
        ChannelListener.__init__(self,nodeName,chanMgr)

        Pyro.config.PYRO_MULTITHREADED = 0

        Pyro.core.SynchronizedObjBase.__init__(self)
        Pyro.core.initServer(banner=0)

        self.log = sbLog(":sb.node.%s"%nodeName,clHost,clPort)

        self.nodeName = nodeName
        if wedgeName == "":
            self.wedgeName = nodeName
        else:
            self.wedgeName = wedgeName

        self.wedge = None
        self.nodeList = []
        self.nodeProxy = {}

        self.id2Friends = {}

        self.log.info("Starting.")

        # DISL SOAP init (temporary)
        from PlayerFriendsDB import PlayerFriendsDB
        self.friendsDB = PlayerFriendsDB(self.log,dislURL)

        # DISL MD init
        self.channelList = [sbConfig.DISL2SBChannel,sbConfig.DISL2SBChannel+self.nodeName]
        self.joinChannels()
        
        # db init

        from LastSeenDB import LastSeenDB
        self.lastSeenDB = LastSeenDB(log=self.log,
                                     host=sbConfig.lastSeenDBhost,
                                     port=sbConfig.lastSeenDBport,
                                     user=sbConfig.lastSeenDBuser,
                                     passwd=sbConfig.lastSeenDBpasswd,
                                     dbname=sbConfig.lastSeenDBdb)

        from sbMaildb import sbMaildb
        self.mailDB = sbMaildb(log=self.log,
                               host=sbConfig.mailDBhost,
                               port=sbConfig.mailDBport,
                               user=sbConfig.mailDBuser,
                               passwd=sbConfig.mailDBpasswd,
                               db=sbConfig.mailDBdb)
                               
        # pyro init
        
        self.initPyro(nsHost,nsPort,listenPort)

        self.updateWedge()
        self.updateNodes()

        self.log.debug("Enter sendEnterNode")
        self.sendEnterNode()
        self.log.debug("Exit sendEnterNode")

        self.localPlayers = {}
        self.remotePlayerLoc = {}
        self.remotePlayerInfo = {}

        self.servedLogins = 0        
        self.servedChat = 0
        self.servedChatSC = 0
        self.servedMail = 0
        self.servedMailSC = 0

        self.log.info("-- sb.node.%s is ready. --" %self.nodeName)

    def joinChannels(self):
        self.log.debug("Joining channels: %s" % str(self.channelList))
        for channel in self.channelList:
            self.startChannelListen(channel)

    def shutdown(self):
        self.pyroDaemon.disconnect(self)
        self.sendExitNode()
        self.log.info("shutdown() called.  Shutting down cleanly.")
        self.pyroDaemon.shutdown(True)


    def initPyro(self,nsHost,nsPort,listenPort):
        if nsHost is None:
            self.log.warning("No NS host/port specified, trying location via broadcast.")
            self.nameServer = Pyro.naming.NameServerLocator().getNS()
        else:
            self.log.info("Connecting to NS at %s:%d." % (nsHost,nsPort))
            self.nameServer = Pyro.naming.NameServerLocator().getNS(host=nsHost,port=nsPort)

        if listenPort is not None:
            self.log.info("Accepting Pyro requests on port %d."%listenPort)
            Pyro.config.PYRO_PORT = listenPort
            Pyro.config.PYRO_PORT_RANGE = 1
            
        self.pyroDaemon = Pyro.core.Daemon()
        self.pyroDaemon.useNameServer(self.nameServer)
        try:
            self.nameServer.createGroup(":sb")
            self.nameServer.createGroup(":sb.node")
            self.nameServer.createGroup(":sb.player")
            self.nameServer.createGroup(":sb.wedge")
        except Pyro.errors.NamingError:
            pass
        try:
            self.pyroDaemon.connectPersistent(self,":sb.node.%s"%self.nodeName)
        except Pyro.errors.NamingError:
            self.log.debug(":sb.node.%s was already registered, overwriting old entry."%self.nodeName)
            self.nameServer.unregister(":sb.node.%s"%self.nodeName)
            self.pyroDaemon.connectPersistent(self,":sb.node.%s"%self.nodeName)



    # ---------------------------
    # | DISL <-> Node messages   |
    # ---------------------------

    def rcvMessage(self,message):
        """
        Receive and act on a single message from the DISL MD.
        Message will be passed to the appropriate handler function based on its functionCode.
        """
        #self.lastMsgTime = time.time()

        self.log.debug("Message from DISL:  %s %s %s %s" % (message.targetChannel,
                                                                      message.responseChannel,
                                                                      message.functionCode,
                                                                      message.otherData))

        if message.targetChannel == sbConfig.DISL2SBChannel:
            if message.functionCode == sbConfig.FC_DISLSendFriendAdd:
                self.handleDISLSendNewFriendship(message)
            elif message.functionCode == sbConfig.FC_DISLSendFriendRemove:
                self.handleDISLSendFriendRemove(message)
            else:
                # we should not be here!
                self.log.warning("Invalid FC received from DISL MD: %s" % message.functionCode)
                self.log.warning("Offending message:  %s %s %s %s" % (message.targetChannel,
                                                                      message.responseChannel,
                                                                      message.functionCode,
                                                                      message.otherData))
        elif message.targetChannel == (sbConfig.DISL2SBChannel + self.nodeName):
            if message.functionCode == sbConfig.FC_DISLSendFriendAdd:
                self.handleDISLSendFriendsList(message)
            else:
                # we should not be here!
                self.log.warning("Invalid FC received from DISL MD: %s" % message.functionCode)
                self.log.warning("Offending message:  %s %s %s %s" % (message.targetChannel,
                                                                      message.responseChannel,
                                                                      message.functionCode,
                                                                      message.otherData))
        else:
            # we should not be here!
            self.log.warning("Got an MD message with a weird target channel:" % message.targetChannel)
            self.log.warning("Offending message:  %s %s %s %s" % (message.targetChannel,
                                                                message.responseChannel,
                                                                message.functionCode,
                                                                message.otherData))

    def handleDISLSendFriendsList(self,message):
        """
        Handle a "here are your friends" message (DISL -> SB).
        Add the friendships to users' in-memory friends lists.
        Let users know about the friendships.
        """
        try:
            # parse the message
            tempVals = str(message.otherData).split('|')
            #self.log.debug(str(tempVals))
            friendOne = int(tempVals[0])

            friends = []

            for i in xrange(1,len(tempVals)-1,2):
                friends.append([int(tempVals[i]),int(tempVals[i+1])])
            #self.log.debug(str(friends))
        except Exception,e:
            self.parsingError(message)
            self.log.error(str(e))   
            return

        #self.log.debug("localPlayers: %s"%self.localPlayers)

        if self.localPlayers.has_key(friendOne):
            # add the new friendships
            for friend in friends:
                friendTwo = friend[0]
                if friend[1] == 1:
                    secret = True
                else:
                    secret = False

                self.id2Friends[friendOne][friendTwo] = secret

            # tell the other nodes I'm here (they probably need to know, but might already)
            self.sendEnterRemotePlayer(friendOne,self.localPlayers[friendOne],self.id2Friends[friendOne])

            # send me my friends, let local ones know I'm here
            self.sendLocalFriendsUpdate(friendOne,friends)


    def handleDISLSendNewFriendship(self,message):
        """
        Handle a "here are your friends" message (DISL -> SB).
        Add the friendships to users' in-memory friends lists.
        Let users know about the friendships.
        """
        #self.log.debug("handleDISLSendNewFriendship")
        try:
            # parse the message
            tempVals = str(message.otherData).split('|')
            #self.log.debug(str(tempVals))
            friendOne = int(tempVals[0])

            friends = []

            for i in xrange(1,len(tempVals)-1,2):
                friends.append([int(tempVals[i]),int(tempVals[i+1])])
            #self.log.debug(str(friends))
        except Exception,e:
            self.parsingError(message)
            self.log.error(str(e))
            return

        if not len(friends) == 1:
            self.log.error("len(friends) was %d in handleDISLSendNewFriendship!"%len(friends))
            return

        friendTwo = friends[0][0]
        if friends[0][1] == 1:
            secret = True
        else:
            secret = False

        if self.id2Friends.has_key(friendOne):
            self.id2Friends[friendOne][friendTwo] = secret
            self.sendLocalFriendsUpdate(friendOne,[[friendTwo,secret],])

        if self.id2Friends.has_key(friendTwo):
            self.id2Friends[friendTwo][friendOne] = secret
            self.sendLocalFriendsUpdate(friendTwo,[[friendOne,secret],])


    def handleDISLSendFriendRemove(self,message):
        """
        Handle a "no more friend" message (DISL -> SB).
        Remove the friendships from both users' in-memory friends lists.
        Let both users know.
        """
        try:
            # parse the message
            tempVals = str(message.otherData).split('|')
            friendOne = int(tempVals[0])
            friendTwo = int(tempVals[1])
        except:
            self.parsingError(message)
            return

        self.log.debug("Got a friend remove notice from disl: %d and %d"%(friendOne,friendTwo))

        #self.log.debug("Friends before removal: %s" % str(self.id2Friends))

        # update my in-memory lists
        if self.id2Friends.has_key(friendOne):
            self.id2Friends[friendOne].pop(friendTwo,None)

        if self.id2Friends.has_key(friendTwo):
            self.id2Friends[friendTwo].pop(friendOne,None)

        #self.log.debug("Friends after removal: %s" % str(self.id2Friends))

        # notify both friends
        if self.localPlayers.has_key(friendOne) or self.localPlayers.has_key(friendTwo):
            self.sendLocalFriendshipRemoved(friendOne,friendTwo)


    def parsingError(self,message):
        self.log.error("Couldn't parse MD message: %s %s %s %s" % (message.targetChannel,
                                                                   message.responseChannel,
                                                                   message.functionCode,
                                                                   message.otherData))        


    #---------------------------------
    # Node/Wedge Entry/Exit
    #---------------------------------

    def healthCheck(self):
        return True

    def statCheck(self):
        avgFriends = 0.0
        if len(self.id2Friends) > 0:
            for key in self.id2Friends:
                avgFriends += len(self.id2Friends[key])
            avgFriends /= len(self.id2Friends)
        return {'onlinePlayers':len(self.localPlayers),
                'avgFriends':avgFriends,
                'servedLogins':self.servedLogins,
                'servedChat':self.servedChat,
                'servedChatSC':self.servedChatSC,
                'servedMail':self.servedMail,
                'servedMailSC':self.servedMailSC}

    def sendEnterNode(self):
        if self.wedge:
            self.log.debug("poking wedge")
            try:
                self.wedge.recvEnterNode(self.nodeName)
            except Exception,e:
                self.log.info("Couldn't contact sb.wedge.%s, wedge is None." % self.nodeName)
                self.wedge = None

        for node in self.nodeList:
            self.log.debug("poking node %s" % node)
            try:
                proxy = self.nodeProxy[node]
                proxy.recvEnterNode(self.nodeName)
            except Exception,e:
                self.log.info("Couldn't contact sb.node.%s, removing from nodelist." % node)
                self.nodeList.remove(node)
                del self.nodeProxy[node]

    def sendExitNode(self):
        try:
            if self.wedge:
                self.wedge.recvExitNode(self.nodeName)

            for node in self.nodeList:
                proxy = self.nodeProxy[node]
                proxy._setOneway(["recvExitNode"])
                proxy.recvExitNode(self.nodeName)
        except:
            pass

    def recvEnterNode(self,nodeName):
        self.log.debug("Received enterNode(%s)"%nodeName)
        # clear all players present on the remote node
        self.updateNodes()

    def recvExitNode(self,nodeName):
        self.log.debug("Received exitNode(%s)"%nodeName)
        # clear all players present on the remote node
        self.updateNodes()

    def recvEnterWedge(self,wedgeName):
        self.log.debug("Received enterWedge(%s)."%wedgeName)
        self.wedgeName = wedgeName
        # clear all local players?
        self.updateWedge()

    def recvExitWedge(self,wedgeName):
        self.log.debug("Received exitWedge(%s)."%wedgeName)
        # clear all local players?
        self.updateWedge()
    
    def updateWedge(self):
        try:
            self.wedge = Pyro.core.getProxyForURI(self.nameServer.resolve(":sb.wedge.%s"%self.wedgeName))
            self.wedge._setOneway(["recvEnterNode",
                                   "recvExitNode",
                                   "recvEnterRemotePlayer",
                                   "recvExitRemotePlayer",
                                   "recvFriendsUpdate",
                                   "recvFriendshipRemoved",
                                   "recvWhisper",
                                   "recvSCWhisper",       
                                   "recvWhisperFailed",
                                   "recvSCWhisperFailed",
                                   "recvMailUpdate",
                                   "recvMail",
                                   "recvSecretGenerated",
                                   "recvSecretRequestError",
                                   "recvSecretRedeemError"])
            self.wedge._setTimeout(10)
            self.log.info("-- Connected to sb.wedge.%s. --" % self.wedgeName)
        except Pyro.errors.NamingError:
            self.wedge = None
            self.log.info("sb.wedge.%s not found on name server, wedge is None." % self.wedgeName)
        
    def updateNodes(self):
        nodelist = self.nameServer.list(":sb.node")
        self.nodeList = []
        self.nodeProxy = {}
        for node in nodelist:
            if node[0] != self.nodeName:
                self.log.debug("Getting proxy for node %s"%node[0])
                self.nodeList.append(node[0])
                self.nodeProxy[node[0]] = Pyro.core.getProxyForURI(self.nameServer.resolve(":sb.node.%s" % node[0]))

                self.nodeProxy[node[0]]._setOneway(["recvEnterNode",     
                                                    "recvExitNode",         
                                                    "recvEnterRemotePlayer",     
                                                    "recvExitRemotePlayer",     
                                                    "recvWhisper",
                                                    "recvSCWhisper",             
                                                    "recvMailUpdate"]) 
                self.nodeProxy[node[0]]._setTimeout(10)

        self.log.debug("Updated node list: %s"%str(self.nodeList))


    #---------------------------------------
    # Player Entry/Exit
    #---------------------------------------

    #wedge->node
    def recvEnterLocalPlayer(self,playerId,playerInfo):
        if self.localPlayers.has_key(playerId):
            self.log.warning("Warning: enterPlayer(%d) called, but I already have this player."%(playerId))

        self.log.debug("Player %d entered." % (playerId))
        self.servedLogins = self.servedLogins + 1

        #self.log.debug("PlayerInfo.onlineYesNo = %d" % playerInfo.onlineYesNo)

        self.localPlayers[playerId] = playerInfo
        self.id2Friends[playerId] = {}

        # get friends list asynchronously, DISL will send it back
        # and hit handleDISLSendFriendAdd
        try:
            self.log.debug("Sending msg to DISL: %s %s %s %s" % (sbConfig.SB2DISLChannel,
                                                                 sbConfig.DISL2SBChannel+self.nodeName,
                                                                 sbConfig.FC_DISLGetFriends,
                                                                 "%d"%playerId))
            self.broadcastMessage(ChannelMessage(sbConfig.SB2DISLChannel,
                                                 sbConfig.DISL2SBChannel+self.nodeName,
                                                 sbConfig.FC_DISLGetFriends,
                                                 "%d"%playerId))
        except Exception,e:
            self.log.error("Error sending friends request to DISL:")
            self.log.error(''.join(Pyro.util.getPyroTraceback(e)))

        if playerInfo:
            self.lastSeenDB.setInfo(playerId,playerInfo)
        

    #wedge->node
    def recvExitLocalPlayer(self,playerId,playerInfo=None):
        if not self.localPlayers.has_key(playerId):
            self.log.warning("Warning: exitPlayer(%d) called, but I don't have this one."%playerId)
        
        self.log.debug("Player %d exited." % playerId)

        if playerInfo:
            self.lastSeenDB.setInfo(playerId,playerInfo)

        self.localPlayers.pop(playerId,None)
        friends = self.id2Friends.pop(playerId,None)

        #announce exit to other nodes
        self.sendExitRemotePlayer(playerId,friends)


    #node->node
    def sendEnterRemotePlayer(self,playerId,playerInfo,friendsList):
        try:
            for node in self.nodeList:
                self.nodeProxy[node].recvEnterRemotePlayer(playerId,self.nodeName,playerInfo,friendsList)
        except ConnectionClosedError,e:
            self.log.error("ConnectionClosedError in sendEnterRemotePlayer.  Refreshing all nodes.")
            self.updateNodes()
        except ProtocolError,e:
            self.log.error("ProtocolError (%s) in sendEnterRemotePlayer.  Refreshing all nodes."%str(e))
            self.updateNodes()
        except Exception,e:
            self.log.error("Error sending enterRemotePlayer to sb.node.%s: %s" % (node,''.join(Pyro.util.getPyroTraceback(e))))
        

    #node->node
    def sendExitRemotePlayer(self,playerId,friendsList):
        try:
            for node in self.nodeList:
                self.nodeProxy[node].recvExitRemotePlayer(playerId,self.nodeName,friendsList)
        except ConnectionClosedError,e:
            self.log.error("ConnectionClosedError in sendExitRemotePlayer.  Refreshing all nodes.")
            self.updateNodes()
        except ProtocolError,e:
            self.log.error("ProtocolError (%s) in sendExitRemotePlayer.  Refreshing all nodes."%str(e))
            self.updateNodes()
        except Exception,e:
            self.log.error("Error sending exitRemotePlayer to sb.node.%s: %s" % (node,''.join(Pyro.util.getPyroTraceback(e))))


    #node->node
    def recvEnterRemotePlayer(self,playerId,nodeName,playerInfo,friendsList):
        if self.remotePlayerLoc.has_key(playerId):
            self.log.warning("Warning: enterRemotePlayer(%d) called, but I already see this player."%(playerId))
            
        self.log.debug("Saw player %d enter at :sb.node.%s."%(playerId,nodeName))

        self.remotePlayerLoc[playerId] = nodeName
        self.remotePlayerInfo[playerId] = playerInfo

        #self.log.debug("Current locations: %s" % str(self.remotePlayerLoc))

        if self.wedge is not None:
            try:
                self.wedge.recvEnterRemotePlayer(playerId,playerInfo,friendsList)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvEnterRemotePlayer.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvEnterRemotePlayer.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send player enter notice to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
                self.log.error("I sent: %s, %s, %s"%(str(playerId),str(playerInfo),str(friendsList)))
        else:
            self.log.warning("EnterRemotePlayer: No wedge connected!")

    #node->node
    def recvExitRemotePlayer(self,playerId,nodeName,friendsList):
        if not self.remotePlayerLoc.has_key(playerId):
            self.log.warning("Warning: exitRemotePlayer(%d) called, but I don't see this player.  Ignoring."%(playerId))
            return

        self.log.debug("Saw player %d exit."%playerId)

        self.remotePlayerLoc.pop(playerId,None)
        self.remotePlayerInfo.pop(playerId,None)

        #self.log.debug("Current locations: %s" % str(self.remotePlayerLoc))

        if self.wedge is not None:
            try:
                self.wedge.recvExitRemotePlayer(playerId,friendsList)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvExitRemotePlayer.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvExitRemotePlayer.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send player exit notice to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
        else:
            self.log.warning("ExitRemotePlayer: No wedge connected!")

    
    #---------------------------------------------
    # Friends
    #---------------------------------------------

    def addFriendship(self,playerId1,playerId2):
        err = None
        try:
            self.friendsDB.addFriendship(playerId1,playerId2)
        except Exception,e:
            try:                                           
                for d in e.fault.detail:
                    if d.nodeName.find("errcode") != -1:
                        err = d.childNodes[0].get_data()
            except Exception,ex:
                self.log.error("Unknown exception in removeFriendship: %s" % str(e))
        if err is not None:
            try:           
                self.wedge.recvAddFriendshipError(playerId,err)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvSecretRequestError.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvSecretRequestError.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send recvAddFriendshipError to my wedge")
        

    def removeFriendship(self,playerId1,playerId2):
        self.log.debug("Got removeFriendship request")
        try:
            self.friendsDB.removeFriendship(playerId1,playerId2)
        except Exception,e:           
            try:
                for d in e.fault.detail:
                    if d.nodeName.find("errcode") != -1:
                        err = d.childNodes[0].get_data()
            except Exception,ex:
                self.log.error("Unknown exception in removeFriendship: %s" % str(e))
            

    def recvSecretRequest(self,playerId,parentUsername,parentPassword):
        self.log.debug("Got recvSecretRequest!")
        info = self._getFriendInfo(playerId)
        err = None
        try:
            secret = self.friendsDB.getToken(playerId)
        except Exception,e:
            try:
                for d in e.fault.detail:
                    if d.nodeName.find("errcode") != -1:
                        err = d.childNodes[0].get_data()
            except Exception,e:
                self.log.error("Unknown exception in generateToken: %s" % str(e))

        if err is None:
            try:
                self.wedge.recvSecretGenerated(playerId,secret)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvSecretGenerated.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvSecretGenerated.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send recvSecretGenerated to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
        else:
            try:
                self.wedge.recvSecretRequestError(playerId,err)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvSecretRequestError.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvSecretRequestError.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send recvSecretRequestError to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
        
    def recvSecretRedeem(self,playerId,secret,parentUsername,parentPassword):
        info = self._getFriendInfo(playerId)
        err = None
        try:
            res = self.friendsDB.redeemToken(playerId,secret)
        except Exception,e:
            try:
                for d in e.fault.detail:
                    if d.nodeName.find("errcode") != -1:
                        err = d.childNodes[0]._get_data()
            except Exception,e:
                self.log.error("Unknown exception in redeemToken: %s" % str(e))

        if err is not None:
            try:
                self.wedge.recvSecretRedeemError(playerId,err)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvSecretRedeemError.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvSecretRedeemError.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send recvSecretRedeemError to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))

    def _getFriendInfo(self,playerId):
        if self.localPlayers.has_key(playerId):
            return self.localPlayers[playerId]
        elif self.remotePlayerInfo.has_key(playerId):
            return self.remotePlayerInfo[playerId]
        else:
            return self.lastSeenDB.getInfo(playerId)

    def _getFriendView(self,viewerId,friendId):
        info = self._getFriendInfo(friendId)
        assert self.id2Friends.has_key(viewerId)
        if self.id2Friends[viewerId][friendId] is True:
            info.openChatFriendshipYesNo = 1
        else:
            info.openChatFriendshipYesNo = 0

        info.understandableYesNo = info.openChatFriendshipYesNo

        return info
        
    
    def sendLocalFriendsUpdate(self,friendOne,friends):
        #self.log.debug("sendLocalFriendsUpdate %d: %s"%(friendOne,str(friends)))
        if self.wedge is not None:
            for friend in friends:
                friend[1] = self._getFriendView(friendOne,friend[0])
            try:
                self.wedge.recvFriendsUpdate(friendOne,friends)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in sendLocalFriendsUpdate.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError (%s) in sendLocalFriendsUpdate.  Reconnecting to wedge."%str(e))
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't sendLocalFriendsUpdate to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
                self.log.error("I sent: %d, %s"%(friendOne,friends))
        else:
            self.log.warning("sendFriendshipUpdated: No wedge connected!")

    def sendLocalFriendshipRemoved(self,friendOne,friendTwo):
        self.log.debug("sendLocalFriendshipRemoved on %d,%d"%(friendOne,friendTwo))
        if self.wedge is not None:
            try:
                self.wedge.recvFriendshipRemoved(friendOne,friendTwo)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in sendFriendshipRemoved.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in sendLocalFriendshipRemoved.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't sendFriendshipRemoved to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
                self.log.error("I sent: %d, %d"%(friendOne,friendTwo))
        else:
            self.log.warning("sendFriendshipRemoved: No wedge connected!")



    #---------------------------------------------
    # Whispers
    #---------------------------------------------
        

    def sendWhisper(self,recipientId,senderId,msgText):
        if sbConfig.scrubMessages:
            msgText = badwordpy.scrub(msgText)
        #if self.localPlayers.has_key(recipientId):
        #    self.log("Warning: I own %d.  Ignoring whisper." % (recipientId))
        #    self.wedge.recvWhisperFailed(recipientId,senderId,msgText)
        if not self.remotePlayerLoc.has_key(recipientId):
            self.log.warning("I don't see %d anywhere!  Whisper not delivered."%recipientId)
            return
        #CHECK FRIENDSHIP, permissions, ignore list, etc?
        # wedge is doing this right now, not worrying about it
        loc = self.remotePlayerLoc[recipientId]
        self.log.debug("Delivering whisper to :sb.node.%s."%loc)
        #self.nodeProxy[loc]._setOneway(["recvWhisper"])
        try:
            self.servedChat = self.servedChat + 1
            self.nodeProxy[loc].recvWhisper(recipientId,senderId,msgText)
        except ConnectionClosedError,e:
            self.log.error("ConnectionClosedError in sendWhisper.  Reconnecting to nodes.")
            self.updateNodes()
        except ProtocolError,e:
            self.log.error("ProtocolError in sendWhisper.  Reconnecting to nodes.")
            self.updateNodes()
        except Exception,e:
            self.log.error("Couldn't send whisper to sb.node.%s, had an error: %s"%(loc,''.join(Pyro.util.getPyroTraceback(e))))

    def recvWhisper(self,recipientId,senderId,msgText):
        #msgText = badwordpy.scrub(msgText)
        self.log.debug("WHISPER %d to %d: %s"%(senderId,recipientId,msgText))
        #self.wedge._setOneway(["recvWhisper"])
        if self.wedge is not None:
            try:
                self.wedge.recvWhisper(recipientId,senderId,msgText)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvWhisper.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvWhisper.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send whisper to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
                self.log.error("I sent: %d, %d, %s"%(recipientId,senderId,msgText))
        else:
            self.log.warning("recvWhisper: No wedge connected!")


    def sendSCWhisper(self,recipientId,senderId,msgText):
        self.log.debug("sbNode.sendSCWHISPER %d to %d: %s" % (senderId,recipientId,msgText))
        #if self.localPlayers.has_key(recipientId):
        #    self.log("Warning: I own %d.  Ignoring whisper." % (recipientId))
        #    self.wedge.recvWhisperFailed(recipientId,senderId,msgText)
        if not self.remotePlayerLoc.has_key(recipientId):
            self.log.warning("I don't see %d anywhere!  Whisper not delivered."%recipientId)
            #self.wedge.recvSCWhisperFailed(recipientId,senderId,msgText)
            return
        self.log.debug("Found recipient %d." % recipientId)
        #CHECK FRIENDSHIP, permissions, ignore list, etc?
        loc = self.remotePlayerLoc[recipientId]
        self.log.debug("Delivering SCwhisper to :sb.node.%s."%loc)
        #self.nodeProxy[loc]._setOneway(["recvWhisper"])
        try:
            self.servedSC = self.servedSC + 1
            self.nodeProxy[loc].recvSCWhisper(recipientId,senderId,msgText)
        except ConnectionClosedError,e:
            self.log.error("ConnectionClosedError in sendSCWhisper.  Reconnecting to nodes.")
            self.updateNodes()
        except ProtocolError,e:
            self.log.error("ProtocolError in sendSCWhisper.  Reconnecting to nodes.")
            self.updateNodes()
        except Exception,e:
            self.log.error("Couldn't send SCwhisper to sb.node.%s, had an error: %s"%(loc,''.join(Pyro.util.getPyroTraceback(e))))

    def recvSCWhisper(self,recipientId,senderId,msgText):
        self.log.debug("sbNode.recvSCWHISPER %d to %d: %s"%(senderId,recipientId,msgText))
        if self.wedge is not None:
            try:
                self.wedge.recvWhisper(recipientId,senderId,msgText)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvSCWhisper.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvSCWhisper.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send whisper to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
                self.log.error("I sent: %d, %d, %s"%(recipientId,senderId,msgText))
        else:
            self.log.debug("No wedge connected!")

    #---------------------------------------------
    # Mail
    #---------------------------------------------
    
    def sendMail(self,recipientId,senderId,msgText):
        self.log.debug("sbNode.sendMail %d to %d: %s" % (senderId,recipientId,msgText))
        self.servedMail = self.servedMail + 1
        self.mailDB.putMail(recipientId,senderId,msgText)

        #if self.remotePlayerLoc.has_key(recipientId):
        #    loc = self.remotePlayerLoc[recipientId]
        #    self.log.debug("Sending mail update to :sb.node.%s."%loc)
        #    self.nodeProxy[loc].recvMailUpdate(recipientId,senderId,msgText)

    def sendSCMail(self,recipientId,senderId,msgText):
        self.log.debug("sbNode.sendSCMAIL %d to %d: %s" % (senderId,recipientId,msgText))
        self.servedMailSC = self.servedMailSC + 1
        self.mailDB.putMail(recipientId,senderId,msgText)

    def recvMailUpdate(self,recipientId,senderId,msgText):
        if self.wedge is not None:
            try:
                self.wedge.recvMailUpdate(recipientId,senderId,msgText)
            except ConnectionClosedError,e:
                self.log.error("ConnectionClosedError in recvMailUpdate.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:
                self.log.error("ProtocolError in recvMailUpdate.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send mail update to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
                self.log.error("I sent: %d, %d, %s"%(recipientId,senderId,msgText))
        else:
            self.log.debug("Tried to receive mail update, but no wedge connected!")
            
    def getMail(self,recipientId):
        #self.log.debug("Getting mail for %d"%recipientId)
        mail = self.mailDB.getMail(recipientId)
        for msg in mail:
            senderInfo = self._getFriendInfo(msg['senderId'])
            msg['senderName'] = senderInfo.playerName

        if self.wedge is not None:
            try:
                self.wedge.recvMail(recipientId,mail)
                self.log.debug("Sent mail to %d: %s" % (recipientId,mail))
            except ConnectionClosedError,e:       
                self.log.error("ConnectionClosedError in recvMail.  Reconnecting to wedge.")
                self.updateWedge()
            except ProtocolError,e:       
                self.log.error("ProtocolError in recvMail.  Reconnecting to wedge.")
                self.updateWedge()
            except Exception,e:
                self.log.error("Couldn't send mail to my wedge, had an error: %s"%''.join(Pyro.util.getPyroTraceback(e)))
                self.log.error("I sent: %d, %s"%(recipientId,mail))
        else:
            self.log.debug("Tried to receive mail, but no wedge connected!")


    def deleteMail(self,accountId,messageId):
        self.log.debug("User %d deleting message %d"%(accountId,messageId))
        self.mailDB.deleteMail(accountId,messageId)


    def getLogTail(self,numLines=None):
        if numLines is None:
            return self.log.getMemLog()
        else:
            return "numLInes!=NOne!"
