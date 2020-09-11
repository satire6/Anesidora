import MySQLdb
import _mysql_exceptions
import MySQLdb.constants.CR
import datetime
from otp.friends.FriendInfo import FriendInfo
import otp.switchboard.sbSQL as sbSQL

SERVER_GONE_ERROR = MySQLdb.constants.CR.SERVER_GONE_ERROR
SERVER_LOST = MySQLdb.constants.CR.SERVER_LOST

class LastSeenDB:
    """
    DB wrapper class for last seen info!  All SQL and SOAP code for last seen info should be in here.
    """
    def __init__(self,log,host,port,user,passwd,dbname):
        self.sqlAvailable = True
        if not self.sqlAvailable:
            return

        self.log = log
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        try:
            self.db = MySQLdb.connect(host=host,
                                      port=port,
                                      user=user,
                                      passwd=passwd)
        except _mysql_exceptions.OperationalError,e:
            self.log.warning("Failed to connect to MySQL at %s:%d.  LastSeenDB is disabled."%(host,port))
            self.sqlAvailable = 0
            return

        self.log.info("Connected to lastseen MySQL db at %s:%d."%(host,port))

        
        try:
            cursor = self.db.cursor()
            cursor.execute("USE `%s`"%self.dbname)
            self.log.debug("Using database '%s'"%self.dbname)
        except:
            self.log.debug("%s database not found, lastseen not active." %self.dbname)
            self.sqlAvailable = False

    def reconnect(self):
        self.log.debug("MySQL server was missing, attempting to reconnect.")
        try: self.db.close()
        except: pass
        self.db = MySQLdb.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd)
        cursor = self.db.cursor()
        cursor.execute("USE `%s`"%self.dbname)
        self.log.debug("Reconnected to MySQL server at %s:%d."%(self.host,self.port))

    def disconnect(self):
        if not self.sqlAvailable:
            return
        self.db.close()
        self.db = None

    def getInfo(self,playerId,isRetry=False):
        if not self.sqlAvailable:
            return FriendInfo(playerName="NotFound")

        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(sbSQL.getInfoSELECT,(playerId))
            info = cursor.fetchone()

            if info is None:
                return FriendInfo(playerName="NotFound")
            else:
                return FriendInfo(avatarName = info['avatarName'],
                                  playerName = info['playerName'],
                                  openChatEnabledYesNo = info['openChatEnabledYesNo'],
                                  location = info['location'],
                                  sublocation = info['sublocation'],
                                  timestamp = info['lastupdate'])
            
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.log.error("Error on getInfo retry, giving up:\n%s" % str(e))
                return FriendInfo(playerName="NotFound")
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getInfo(playerId,True)
            else:
                self.log.error("Unknown error on getInfo, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getInfo(playerId,True)
        except Exception,e:
            self.log.error("Unknown error on getInfo, giving up:\n%s" % str(e))
            return FriendInfo(playerName="NotFound")


    def setInfo(self,playerId,info,isRetry=False):
        if not self.sqlAvailable:
            return
        cursor = MySQLdb.cursors.DictCursor(self.db)
        rows = 0
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(sbSQL.setInfoREPLACE,
                           (playerId,
                            info.avatarName,
                            info.playerName,
                            info.openChatEnabledYesNo,
                            info.location,
                            info.sublocation))

            self.db.commit()
            
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.log.error("Error on setInfo retry, giving up:\n" % str(e))
                return
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                self.setInfo(playerId,info,True)
                return
            else:
                self.log.error("Unknown error on setInfo, retrying:\n%s" % str(e))
                self.reconnect()
                self.setInfo(playerId,info,True)
                return
        except Exception,e:
            self.log.error("Unknown error on setInfo, giving up:\n%s" % str(e))
            return
                           

    def getTableStatus(self,isRetry=False):
        if not self.sqlAvailable:
            return None

        cursor = MySQLdb.cursors.DictCursor(self.db)
        rows = 0
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute("show table status")
            return cursor.fetchallDict()
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.log.error("Error on getTableStatus retry, giving up:\n" % str(e))
                return None
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getTableStatus(True)
            else:
                self.log.error("Unknown error on getTableStatus, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getTableStatus(True)
        except Exception,e:
            self.log.error("Unknown error on getTableStatus, giving up:\n%s" % str(e))
            return None
