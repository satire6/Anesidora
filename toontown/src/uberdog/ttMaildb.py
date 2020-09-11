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

from otp.switchboard import sbConfig

SERVER_GONE_ERROR = MySQLdb.constants.CR.SERVER_GONE_ERROR
SERVER_LOST = MySQLdb.constants.CR.SERVER_LOST

class ttMaildb:
    """Based on sbMaildb.py in $OTP/src/switchboard."""

    notify = DirectNotifyGlobal.directNotify.newCategory("ttMaildb")
    
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
            self.notify.warning("Failed to connect to MySQL db=%s at %s:%d.  ttMaildb DB is disabled."%(db,host,port))
            self.notify.warning("Error detail: %s"%str(e))
            self.sqlAvailable = False
            return

        self.notify.info("Connected to maildb=%s at %s:%d."%(db,host,port))

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
            cursor.execute("""
            CREATE TABLE ttrecipientmail (
              messageId             BIGINT     NOT NULL AUTO_INCREMENT UNIQUE,
              recipientId           BIGINT     NOT NULL,
              senderId              BIGINT     NOT NULL,
              message               TEXT       NOT NULL,
              lastupdate            TIMESTAMP  NOT NULL 
                                     DEFAULT   CURRENT_TIMESTAMP
                                     ON UPDATE CURRENT_TIMESTAMP,
              dateSent		        TIMESTAMP  NOT NULL default '0000-00-00 00:00:00',
              readFlag					BOOLEAN    DEFAULT FALSE,
              PRIMARY KEY  (messageId),
              INDEX idx_recipientId (recipientId)
            ) 
            ENGINE=InnoDB 
            DEFAULT CHARSET=utf8;            

            """)
            if __debug__:
                self.notify.info("Table ttrecipientmail did not exist, created a new one!")
        except _mysql_exceptions.OperationalError,e:
            pass            

        try:
            cursor = self.db.cursor()
            cursor.execute("USE `%s`"%self.dbname)
            self.notify.debug("Using database '%s'"%self.dbname)
        except:
            self.notify.debug("%s database not found, maildb not active."%self.dbname)
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

    def getMail(self,recipientId,isRetry=False):
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getMail")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.getMailSELECT,(recipientId,))
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttMaildb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error on getMail retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getMail(recipientId,True)
            else:
                self.notify.warning("Unknown error in getMail, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getMail(recipientId,True)
        except Exception,e:
            self.notify.warning("Unknown error in getMail, giving up:\n%s" % str(e))
            return ()


    def putMail(self,recipientId,senderId,message,isRetry=False):
        if not self.sqlAvailable:
            return

        countcursor = self.db.cursor()

        try:
            countcursor.execute("USE `%s`"%self.dbname)
            countcursor.execute(ttSQL.getMailSELECT,(recipientId,))
            if countcursor.rowcount >= sbConfig.mailStoreMessageLimit:
                self.notify.debug("%d's mailbox is full!  Can't fit message from %d." %(recipientId,senderId))
                return     

            cursor = MySQLdb.cursors.DictCursor(self.db)

            cursor.execute(ttSQL.putMailINSERT,
                           (recipientId,senderId,message))
            self.db.commit()

        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error on putMail retry, giving up:\n%s" % str(e))
                return
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                self.putMail(recipientId,senderId,message,True)
            else:
                self.notify.warning("Unknown error in putMail, retrying:\n%s" % str(e))
                self.reconnect()
                self.putMail(recipientId,senderId,message,True)
        except Exception,e:
            self.notify.warning("Unknown error in putMail, giving up:\n%s" % str(e))
            return


    def deleteMail(self,accountId,messageId,isRetry=False):
        if not self.sqlAvailable:
            return

        cursor = MySQLdb.cursors.DictCursor(self.db)

        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.deleteMailDELETE,(messageId,accountId))

            if cursor.rowcount < 1:
                self.notify.warning("%d tried to delete message %d which didn't exist or wasn't his!" % (accountId,messageId))

            self.db.commit()
                
        except _mysql_exceptions.OperationalError,e:
            if isRetry == True:
                self.notify.warning("Error in deleteMail retry, giving up:\n%s" % str(e))
                return
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                self.deleteMail(accountId,messageId,True)
            else:
                self.notify.warning("Unnown error in deleteMail, retrying:\n%s" % str(e))
                self.reconnect()
                self.deleteMail(accountId,messageId,True)
        except Exception,e:
            self.notify.warning("Unknown error in deleteMail, giving up:\n%s" % str(e))
            return            


    def dumpMailTable(self):
        cursor = MySQLdb.cursors.DictCursor(self.db)
        cursor.execute("USE `%s`"%self.dbname)
        cursor.execute("SELECT * FROM recipientmail")
        return cursor.fetchall()


        
