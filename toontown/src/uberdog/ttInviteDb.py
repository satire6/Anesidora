#import Pyro.core
#import Pyro.naming
#import Pyro.errors
import sys
import datetime
import MySQLdb
import MySQLdb.constants.CR
import _mysql_exceptions
from direct.directnotify import DirectNotifyGlobal
from toontown.uberdog import ttSQL
from toontown.parties import PartyGlobals

SERVER_GONE_ERROR = MySQLdb.constants.CR.SERVER_GONE_ERROR
SERVER_LOST = MySQLdb.constants.CR.SERVER_LOST

class ttInviteDb:
    """Based on sbMaildb.py in $OTP/src/switchboard."""

    notify = DirectNotifyGlobal.directNotify.newCategory("ttInviteDb")
    
    def __init__(self,host,port,user,passwd,db):
        self.sqlAvailable = True
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = db

        try:
            self.db = MySQLdb.connect(host=host,
                                      port=port,
                                      user=user,
                                      passwd=passwd,
                                      )
        except _mysql_exceptions.OperationalError,e:
            self.notify.warning("Failed to connect to MySQL db=%s at %s:%d.  ttInvitedb DB is disabled."%(db,host,port))
            self.notify.warning("Error detail: %s"%str(e))
            self.sqlAvailable = False
            return

        self.notify.info("Connected to invitedb=%s at %s:%d."%(db,host,port))

        #temp hack for initial dev, create DB structure if it doesn't exist already
        cursor = self.db.cursor()
        try:
            cursor.execute("CREATE DATABASE `%s`"%self.dbname)
            if __debug__:
                self.notify.info("Database '%s' did not exist, created a new one!"%self.dbname)
        except _mysql_exceptions.ProgrammingError, e:
            # self.notify.info('%s' % str(e))
            pass
        except _mysql_exceptions.OperationalError, e:
            self.notify.info('%s' % str(e))            
            pass

        cursor.execute("USE `%s`"%self.dbname)
        if __debug__:
            self.notify.debug("Using database '%s'"%self.dbname)
        try:
            # well if we're creating the party table again,
            # might as well create the party status lookup table for the benefit of database reporting
            cursor.execute("Show tables like 'ttInviteStatus';")
            if not cursor.rowcount:
                # we know the ttInviteStatus table doesn't exist, create it again
                cursor.execute("""
                DROP TABLE IF EXISTS ttInviteStatus;
                """)

                cursor.execute("""
                CREATE TABLE ttInviteStatus(
                  statusId      TINYINT NOT NULL,
                  description   VARCHAR(20) NOT NULL,
                  lastupdate    TIMESTAMP  NOT NULL 
                                      DEFAULT   CURRENT_TIMESTAMP
                                      ON UPDATE CURRENT_TIMESTAMP,
                  PRIMARY KEY (statusId),
                  UNIQUE INDEX uidx_desc(description)
                )
                ENGINE=Innodb
                DEFAULT CHARSET=utf8;
                """)
                # this ensure that the table values come directly from PartyGlobals.InviteStatus
                for index in xrange(len(PartyGlobals.InviteStatus)):
                    cursor.execute(\
                        "INSERT INTO ttInviteStatus(statusId, description) VALUES (%d, '%s')" %
                    (index, PartyGlobals.InviteStatus.getString(index)))
                    
            # TODO is it better to do a show tables than to do a try create Table except block?        
            cursor.execute("""
            CREATE TABLE ttInvite (
              inviteId           BIGINT     NOT NULL AUTO_INCREMENT,            
              partyId            BIGINT     NOT NULL,
              guestId            BIGINT     NOT NULL,
              statusId           TINYINT    NOT NULL DEFAULT 0,
              lastupdate         TIMESTAMP  NOT NULL 
                                 DEFAULT   CURRENT_TIMESTAMP
                                 ON UPDATE CURRENT_TIMESTAMP,

              PRIMARY KEY  (inviteId),
              INDEX idx_guestId (guestId),
              INDEX idx_partyId(partyId),
              FOREIGN KEY (partyId) REFERENCES ttParty(partyId) ON DELETE CASCADE
            ) 
            ENGINE=InnoDB 
            DEFAULT CHARSET=utf8;            
            """)
            if __debug__:
                self.notify.info("Table ttInvite did not exist, created a new one!")
        except _mysql_exceptions.OperationalError,e:
            pass            

        try:
            cursor = self.db.cursor()
            cursor.execute("USE `%s`"%self.dbname)
            self.notify.debug("Using database '%s'"%self.dbname)
        except:
            self.notify.debug("%s database not found, ttInvite not active."%self.dbname)
            self.sqlAvailable = False


    def reconnect(self):
        self.notify.debug("MySQL server was missing, attempting to reconnect.")
        try: self.db.close()
        except: pass
        self.db = MySQLdb.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd)
        cursor = self.db.cursor()
        cursor.execute("USE `%s`"%self.dbname)
        self.notify.debug("Reconnected to MySQL server at %s:%d."%(self.host,self.port))

    def disconnect(self):
        if not self.sqlAvailable:
            return
        self.db.close()
        self.db = None

    def getInvites(self, avatarId,isRetry=False):
        """
        Returns a tuple, which could be empty.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getInvites")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.getInvitesSELECT,(avatarId,))
            res = cursor.fetchall()
            self.notify.debug("Select was successful in ttInvitedb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error on getInvites retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getInvites(avatarId,True)
            else:
                self.notify.warning("Unknown error in getInvites, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getInvites(avatarId,True)
        except Exception,e:
            self.notify.warning("Unknown error in getInvites, giving up:\n%s" % str(e))
            return ()


    def putInvite(self, partyId, inviteeId,isRetry=False):
        if not self.sqlAvailable:
            return

        countcursor = self.db.cursor()

        try:
            cursor = MySQLdb.cursors.DictCursor(self.db)

            cursor.execute(ttSQL.putInviteINSERT,
                           (partyId, inviteeId))
            self.db.commit() 

        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error on putInvite retry, giving up:\n%s" % str(e))
                return
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                self.putInvite(partyId, inviteeId,True)
            else:
                self.notify.warning("Unknown error in putInvite, retrying:\n%s" % str(e))
                self.reconnect()
                self.putInvite(partyId, inviteeId,True)
        except Exception,e:
            self.notify.warning("Unknown error in putInvite, giving up:\n%s" % str(e))
            return


    def deleteInviteByParty(self,partyId,isRetry=False):
        if not self.sqlAvailable:
            return

        cursor = MySQLdb.cursors.DictCursor(self.db)

        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.deleteInviteByPartyDELETE,( partyId))

            if cursor.rowcount < 1:
                self.notify.warning("%d tried to delete party %d which didn't exist or wasn't his!" % (accountId,messageId))

            self.db.commit()
                
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error in deleteInviteByParty retry, giving up:\n%s" % str(e))
                return
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                self.deleteMail(accountId,messageId,True)
            else:
                self.notify.warning("Unnown error in deleteInviteByParty, retrying:\n%s" % str(e))
                self.reconnect()
                self.deleteMail(accountId,messageId,True)
        except Exception,e:
            self.notify.warning("Unknown error in deleteInviteByParty, giving up:\n%s" % str(e))
            return            

    def getReplies(self,partyId,isRetry=False):
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getParty")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.getRepliesSELECT,(partyId,))
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttInvitedb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error on getReplies retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getReplies(partyId,True)
            else:
                self.notify.warning("Unknown error in getReplies, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getReplies(partyId,True)
        except Exception,e:
            self.notify.warning("Unknown error in getReplies, giving up:\n%s" % str(e))
            return ()


    def dumpInviteTable(self):
        cursor = MySQLdb.cursors.DictCursor(self.db)
        cursor.execute("USE `%s`"%self.dbname)
        cursor.execute("SELECT * FROM ttInviteDb")
        return cursor.fetchall()


    def getOneInvite(self, inviteKey, isRetry = False):
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getParty")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.getOneInviteSELECT,(inviteKey,))
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttInvitedb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error on getOneInvite retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getOneInvite(partyId,True)
            else:
                self.notify.warning("Unknown error in getOneInvite, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getOneInvite(partyId,True)
        except Exception,e:
            self.notify.warning("Unknown error in getOneInvite, giving up:\n%s" % str(e))
            return ()

    def updateInvite(self, inviteKey, newStatus, isRetry = False):
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getParty")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.inviteUPDATE,(newStatus, inviteKey))
            self.db.commit()
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttInvitedb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error on updateInvite retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.updateInvite( newStatus, inviteKey, True)
            else:
                self.notify.warning("Unknown error in updateInvite, retrying:\n%s" % str(e))
                self.reconnect()
                return self.updateInvite( newStatus, inviteKey, True)
        except Exception,e:
            self.notify.warning("Unknown error in updateInvite, giving up:\n%s" % str(e))
            return ()                
    

    def getInviteesOfParty(self, inviteKey, isRetry = False):
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getParty")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.getInviteesOfPartySELECT,(inviteKey,))
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttInvitedb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error on getInviteesOfParty retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getInviteesOfParty(partyId,True)
            else:
                self.notify.warning("Unknown error in getInviteesOfParty, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getInviteesOfParty(partyId,True)
        except Exception,e:
            self.notify.warning("Unknown error in getInviteesOfParty, giving up:\n%s" % str(e))
            return ()
