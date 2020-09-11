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
from toontown.parties.PartyGlobals import PartyStatus,InviteTheme

SERVER_GONE_ERROR = MySQLdb.constants.CR.SERVER_GONE_ERROR
SERVER_LOST = MySQLdb.constants.CR.SERVER_LOST

class ttPartyDb:
    """Based on sbMaildb.py in $OTP/src/switchboard."""

    notify = DirectNotifyGlobal.directNotify.newCategory("ttPartyDb")
    
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
                ttPartyDb.notify.info("Database '%s' did not exist, created a new one!"%self.dbname)
        except _mysql_exceptions.ProgrammingError, e:
            # ttPartyDb.notify.info('%s' % str(e))
            pass
        except _mysql_exceptions.OperationalError, e:
            ttPartyDb.notify.info('%s' % str(e))            
            pass

        cursor.execute("USE `%s`"%self.dbname)
        if __debug__:
            ttPartyDb.notify.debug("Using database '%s'"%self.dbname)
        try:
            # well if we're creating the party table again,
            # might as well create the party status lookup table for the benefit of database reporting
            cursor.execute("Show tables like 'ttPartyStatus';")
            if not cursor.rowcount:
                # we know the ttPartyStatus table doesn't exist, create it again
                cursor.execute("""
                DROP TABLE IF EXISTS ttPartyStatus;
                """)

                cursor.execute("""
                CREATE TABLE ttPartyStatus(
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
                # this ensure that the table values come directly from PartyGlobals.PartyStatus
                for index in xrange(len(PartyGlobals.PartyStatus)):
                    cursor.execute(\
                        "INSERT INTO ttPartyStatus(statusId, description) VALUES (%d, '%s')" %
                    (index, PartyGlobals.PartyStatus.getString(index)))

            # TODO is it better to do a show tables than to do a try create Table except block?
            cursor.execute("""
            CREATE TABLE ttParty (
              partyId             BIGINT     NOT NULL AUTO_INCREMENT,
              hostId              BIGINT     NOT NULL,
              startTime           TIMESTAMP     NOT NULL  default '0000-00-00 00:00:00',
              endTime             TIMESTAMP     NOT NULL  default '0000-00-00 00:00:00',
              isPrivate             BOOL       default False,
              inviteTheme         TINYINT,
              activities           VARBINARY(252),
              decorations         VARBINARY(252),
              statusId              TINYINT default 0,
              creationTime          TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
              lastupdate          TIMESTAMP  NOT NULL 
                                  DEFAULT   CURRENT_TIMESTAMP
                                  ON UPDATE CURRENT_TIMESTAMP,

              PRIMARY KEY  (partyId),
              INDEX idx_hostId (hostId),
              INDEX idx_statusId(statusId)
            ) 
            ENGINE=InnoDB 
            DEFAULT CHARSET=utf8;            

            """)

            # size calculations
            # partyId  8 bytes
            # hostId   8 bytes
            # startTime 4 bytes
            # endTime   4 bytes
            # isPrivate 1 byte
            # inviteTheme 1 byte
            # activites 252 bytes
            # decorations 252 bytes
            # statys 1 byte
            # creationTime 4 bytes
            # lastupdate 4 bytes
            # TOTAL = 539 bytes
            if __debug__:
                ttPartyDb.notify.info("Table ttParty did not exist, created a new one!")
        except _mysql_exceptions.OperationalError,e:
            pass            

        try:
            cursor = self.db.cursor()
            cursor.execute("USE `%s`"%self.dbname)
            self.notify.debug("Using database '%s'"%self.dbname)
        except:
            self.notify.debug("%s database not found, ttPartydb not active."%self.dbname)
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

    def getParty(self, partyId, isRetry=False):
        """
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getParty")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.getPartySELECT,(partyId,))
            res = cursor.fetchall()
            self.notify.debug("Select was successful in ttMaildb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on getParty retry. Giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getParty(partyId,True)
            else:
                self.notify.warning("Unknown error in getParty, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getParty(partyId,True)
        except Exception,e:
            self.notify.warning("Unknown error in getParty, giving up:\n%s" % str(e))
            return ()


    def putParty(self, hostId, startTime, endTime, isPrivate, inviteTheme, activities, decorations, status, isRetry=False):
        """
        Returns False if the operation failed for any reason.
        
        isRetry indicates whether this attempt is a retry or not.
        """
        self.notify.debug("putParty( hostId=%s, startTime=%s, endTime=%s, isPrivate=%s, inviteTheme=%s, ... status=%s, isRetry=%s )" %(hostId, startTime, endTime, isPrivate, InviteTheme.getString(inviteTheme), PartyStatus.getString(status), isRetry) )
        if not self.sqlAvailable:
            self.notify.warning("sqlAvailable is False in putParty call.")
            return False

        # we need to parse activites and decorations
        activityStr = ""
        for activity in activities:
            for field in activity:
                activityStr += chr(field)

        decorStr = ""
        for decor in decorations:
            for field in decor:
                decorStr += chr(field)

        countcursor = self.db.cursor()

        try:
            countcursor.execute("USE `%s`"%self.dbname)
            countcursor.execute(ttSQL.getPartyOfHostMatchingStatusSELECT,(hostId,PartyStatus.Pending))
            if countcursor.rowcount >= PartyGlobals.MaxHostedPartiesPerToon:
                self.notify.debug("%d can't host another party, over the limit " %(hostId))
                return False

            cursor = MySQLdb.cursors.DictCursor(self.db)

            cursor.execute(ttSQL.putPartyINSERT,
                           (hostId, startTime, endTime, isPrivate, inviteTheme, activityStr, decorStr, status))
            self.db.commit() 
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("putParty failed with error '%s' on retry. Giving up." % str(e))
                return False
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.putParty(hostId, startTime, endTime, isPrivate, inviteTheme, activityStr, decorStr, status, True)
            else:
                self.notify.warning("putParty failed with error '%s'. Retrying." % str(e))
                self.reconnect()
                return self.putParty(hostId, startTime, endTime, isPrivate, inviteTheme, activityStr, decorStr, status, True)
        except Exception,e:
            self.notify.warning("putParty failed with error '%s'. Giving up." % str(e))
            return False
        else:
            return True # if we got this far without an exception, we're good

    def deleteParty(self,partyId,isRetry=False):
        """
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            return

        cursor = MySQLdb.cursors.DictCursor(self.db)

        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.deletePartyDELETE,(messageId, partyId))

            if cursor.rowcount < 1:
                self.notify.warning("%d tried to delete party %d which didn't exist or wasn't his!" % (accountId,messageId))

            self.db.commit()
                
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error in deleteParty retry, giving up:\n%s" % str(e))
                return
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                self.deleteParty(partyId,True)
            else:
                self.notify.warning("Unnown error in deleteParty, retrying:\n%s" % str(e))
                self.reconnect()
                self.deleteParty(partyId,True)
        except Exception,e:
            self.notify.warning("Unknown error in deleteParty, giving up:\n%s" % str(e))
            return            


    def dumpPartyTable(self):
        cursor = MySQLdb.cursors.DictCursor(self.db)
        cursor.execute("USE `%s`"%self.dbname)
        cursor.execute("SELECT * FROM ttPartyDb")
        return cursor.fetchall()

    def getPartiesAvailableToStart(self, currentTime, isRetry=False):
        """
        Returns a list of tuples of partyId and hostId of all parties allowed to
        start.  A party is allowed to start if its status is Pending and server
        time is past it's start time.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getPartiesAvailableToStart")
            return ()

        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.getPartiesAvailableToStart,(currentTime, PartyGlobals.PartyStatus.Pending))
            res = cursor.fetchall()
            # Ok, these parties can start, go ahead and set their status to CanStart
            self._setPartyStatusToCanStart(res)
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on getPartiesAvailableToStart retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getPartiesAvailableToStart(currentTime, True)
            else:
                self.notify.warning("Unknown error in getPartiesAvailableToStart, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getPartiesAvailableToStart(currentTime,True)
        except Exception,e:
            self.notify.warning("Unknown error in getPartiesAvailableToStart, giving up:\n%s" % str(e))
            return ()


    def _setPartyStatusToCanStart(self, tupleOfResultDictionaries):
        """ Set the status on the following parties to CanStart """
        for resDict in tupleOfResultDictionaries:
            self.changePartyStatus(resDict['partyId'], PartyGlobals.PartyStatus.CanStart)

    def getPartiesOfHost(self, hostId, sortedByStartTime = False, isRetry=False):
        """
        Returns a tuple, which could be empty.
        
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getPartiesOfHost")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)            
            if sortedByStartTime:
                cursor.execute(ttSQL.getPartyOfHostSortedSELECT,(hostId,))                
            else:
                cursor.execute(ttSQL.getPartyOfHostSELECT,(hostId,))
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttMaildb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on getPartiesOfHost retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getPartiesOfHost(hostId, sortedByStartTime, True)
            else:
                self.notify.warning("Unknown error in getPartiesOfHost, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getPartiesOfHost(hostId, sortedByStartTime, True)
        except Exception,e:
            self.notify.warning("Unknown error in getPartiesOfHost, giving up:\n%s" % str(e))
            return ()

    def getPartiesOfHostThatCanStart(self, hostId, isRetry=False):
        """
        Returns a tuple, which could be empty.
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getPartiesOfHostThatCanStart")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)            
            cursor.execute(ttSQL.getPartyOfHostMatchingStatusSELECT,(hostId,PartyGlobals.PartyStatus.CanStart))
            res = cursor.fetchall()
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on getPartiesOfHostThatCanStart retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getPartiesOfHostThatCanStart(hostId, True)
            else:
                self.notify.warning("Unknown error in getPartiesOfHostThatCanStart, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getPartiesOfHostThatCanStart(hostId, True)
        except Exception,e:
            self.notify.warning("Unknown error in getPartiesOfHostThatCanStart, giving up:\n%s" % str(e))
            return ()

    def changePrivate(self, partyId, newPrivateStatus, isRetry=False):
        """
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling changePrivate")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.partyPrivateUPDATE,( newPrivateStatus, partyId))
            self.db.commit()
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttMaildb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on changePrivate retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.changePrivate(newPrivateStatus, partyId, True)
            else:
                self.notify.warning("Unknown error in changePrivate, retrying:\n%s" % str(e))
                self.reconnect()
                return self.changePrivate( newPrivateStatus, partyId, True)
        except Exception,e:
            self.notify.warning("Unknown error in changePrivate, giving up:\n%s" % str(e))
            return ()                


    def changePartyStatus(self, partyId, newPartyStatus, isRetry=False):
        """
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling changePartyStatus")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.partyStatusUPDATE,( newPartyStatus, partyId))
            self.db.commit()
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttMaildb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on changePartyStatus retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.changePartyStatus(newPartyStatus, partyId, True)
            else:
                self.notify.warning("Unknown error in changePartyStatus, retrying:\n%s" % str(e))
                self.reconnect()
                return self.changePartyStatus( newPartyStatus, partyId, True)
        except Exception,e:
            self.notify.warning("Unknown error in changePartyStatus, giving up:\n%s" % str(e))
            return ()

    def convertListToSQLString(self, partyIds):
        """Convert a list of integers to a string sql recognizes."""
        # string version of partyIds is so close to what we need, but it adds the L
        inClause = "("
        for index in xrange(len(partyIds)):                
            inClause += "%d" % partyIds[index]
            if index < len(partyIds) - 1:
                inClause += ","
        inClause += ")"
        return inClause

    def getMultipleParties(self, partyIds, sortByStartTime = False, isRetry=False):
        """
        Return all the partyInfo matching the partyIds list,
        It may return nothing if there are no matches.
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getMultipleParties")
            return ()

        if not partyIds:
            self.notify.debug("empty list in partyIds for getMultipleParties")
            return()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            inClause = self.convertListToSQLString(partyIds)
            
            if sortByStartTime:
                cursor.execute(ttSQL.getMultiplePartiesSortedSELECT % inClause)
            else:
                cursor.execute(ttSQL.getMultiplePartiesSELECT % inClause)
            res = cursor.fetchall()
            self.notify.debug("Select was successful in getMultipleParties, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on getMultipleParties retry. Giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getMultipleParties(partyIds, sortByStartTime, True)
            else:
                self.notify.warning("Unknown error in getMultipleParties, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getMultipleParties(partyIds,sortByStartTime, True)
        except Exception,e:
            self.notify.warning("Unknown error in getMultipleParties, giving up:\n%s" % str(e))
            return ()



    def getPrioritizedParties(self, partyIds, thresholdTime, limit, future, cancelled, isRetry=False):
        """Return parties from the database using the criteria specified in future and cancelled."""
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getCancelledFutureParties")
            return ()

        if not partyIds:
            self.notify.debug("empty list in partyIds for getCancelledFutureParties")
            return()
        
        sqlString = ""
        if future and cancelled:
            sqlString = ttSQL.getCancelledFuturePartiesSELECT
        elif future and not cancelled:
            sqlString = ttSQL.getNonCancelledFuturePartiesSELECT
        elif not future and cancelled:
            sqlString = ttSQL.getCancelledPastPartiesSELECT
        else:
            sqlString = ttSQL.getNonCancelledPastPartiesSELECT
            
        cursor = MySQLdb.cursors.DictCursor(self.db)

        try:
            cursor.execute("USE `%s`"%self.dbname)
            inClause = self.convertListToSQLString(partyIds)
            
            parameters = (inClause, thresholdTime,  str(limit))
            execStr = sqlString % parameters
            cursor.execute(execStr)
             
            res = cursor.fetchall()
            self.notify.debug("Select was successful in getPrioritizedParties, returning %s" % str(res))
            return res        
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on getPrioritizedParties retry. Giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getPrioritizedParties( partyIds, thresholdTime, limit, future, cancelled, isRetry=True)
            else:
                self.notify.warning("Unknown error in getPrioritizedParties getCancelledFutureParties, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getPrioritizedParties( partyIds, thresholdTime, limit, future, cancelled, isRetry=True)
        except Exception,e:
            self.notify.warning("Unknown error in getPrioritizedParties getCancelledFutureParties, giving up:\n%s" % str(e))
            return ()
        

    def getHostPrioritizedParties(self, hostId, thresholdTime, limit, future, cancelled, isRetry=False):
        """Return parties from the database using the criteria specified in future and cancelled."""
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling getCancelledFutureParties")
            return ()

        if not hostId:
            self.notify.debug("empty list in hostId for getCancelledFutureParties")
            return()
        
        sqlString = ""
        if future and cancelled:
            sqlString = ttSQL.getHostCancelledFuturePartiesSELECT
        elif future and not cancelled:
            sqlString = ttSQL.getHostNonCancelledFuturePartiesSELECT
        elif not future and cancelled:
            sqlString = ttSQL.getHostCancelledPastPartiesSELECT
        else:
            sqlString = ttSQL.getHostNonCancelledPastPartiesSELECT
            
        cursor = MySQLdb.cursors.DictCursor(self.db)

        try:
            cursor.execute("USE `%s`"%self.dbname)
            parameters = (hostId, thresholdTime,  str(limit))
            execStr = sqlString % parameters
            cursor.execute(execStr)
             
            res = cursor.fetchall()
            self.notify.debug("Select was successful in getHostPrioritizedParties, returning %s" % str(res))
            return res        
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on getHostPrioritizedParties retry. Giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.getHostPrioritizedParties( hostId, thresholdTime, limit, future, cancelled, isRetry=True)
            else:
                self.notify.warning("Unknown error in getHostPrioritizedParties getCancelledFutureParties, retrying:\n%s" % str(e))
                self.reconnect()
                return self.getHostPrioritizedParties( hostId, thresholdTime, limit, future, cancelled, isRetry=True)
        except Exception,e:
            self.notify.warning("Unknown error in getHostPrioritizedParties getCancelledFutureParties, giving up:\n%s" % str(e))
            return ()
        
    def forceFinishForStarted(self, thresholdTime, isRetry=False):
        """
        isRetry indicates whether this attempt is a retry or not.
        Returns a list of (partyId,hostId) for the ones that were forced to finished
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling forceFinishForStarted")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.partyGetPartiesGoingToFinishedSELECT,(thresholdTime,))
            res = cursor.fetchall()
            cursor.execute(ttSQL.partyForceFinishForStartedUPDATE,(thresholdTime,))
            self.db.commit()
            
            #self.notify.debug("Select was successful in ttMaildb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on forceFinishForStarted retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.forceFinishForStarted(thresholdTime, True)
            else:
                self.notify.warning("Unknown error in forceFinishForStarted, retrying:\n%s" % str(e))
                self.reconnect()
                return self.forceFinishForStarted( thresholdTime, True)
        except Exception,e:
            self.notify.warning("Unknown error in forceFinishForStarted, giving up:\n%s" % str(e))
            return ()

    def forceNeverStartedForCanStart(self, thresholdTime, isRetry=False):
        """
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling forceNeverStartedForCanStart")
            return ()
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            cursor.execute(ttSQL.partyGetPartiesGoingToNeverStartedSELECT,(thresholdTime,))
            res = cursor.fetchall()
            cursor.execute(ttSQL.partyForceNeverStartedForCanStartUPDATE ,(thresholdTime,))
            self.db.commit()
            
            #self.notify.debug("Select was successful in ttMaildb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on forceNeverStartedForCanStart retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.forceNeverStartedForCanStart(thresholdTime, True)
            else:
                self.notify.warning("Unknown error in forceNeverStartedForCanStart, retrying:\n%s" % str(e))
                self.reconnect()
                return self.forceNeverStartedForCanStart( thresholdTime, True)
        except Exception,e:
            self.notify.warning("Unknown error in forceNeverStartedForCanStart, giving up:\n%s" % str(e))
            return ()


    def changeMultiplePartiesStatus(self, partyIds, newPartyStatus, isRetry=False):
        """
        isRetry indicates whether this attempt is a retry or not.
        """
        if not self.sqlAvailable:
            self.notify.debug("sqlAvailable was false when calling changeMultiplePartiesStatus")
            return ()

        if not partyIds:
            self.notify.debug("empty list in partyIds for changeMultiplePartiesStatus")
            return()        
        
        cursor = MySQLdb.cursors.DictCursor(self.db)
        try:
            cursor.execute("USE `%s`"%self.dbname)
            inClause = self.convertListToSQLString(partyIds)
            sqlString = ttSQL.partyMultipleStatusUPDATE
            parameters = ( newPartyStatus, inClause)
            execStr = sqlString % parameters
            cursor.execute(execStr)
            self.db.commit()
            res = cursor.fetchall()
            #self.notify.debug("Select was successful in ttMaildb, returning %s" % str(res))
            return res
        
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                self.notify.warning("Error on changeMultiplePartiesStatus retry, giving up:\n%s" % str(e))
                return ()
            elif e[0] == SERVER_GONE_ERROR or e[0] == SERVER_LOST:
                self.reconnect()
                return self.changeMultiplePartiesStatus(partyIds, newPartyStatus,  True)
            else:
                self.notify.warning("Unknown error in changeMultiplePartiesStatus, retrying:\n%s" % str(e))
                self.reconnect()
                return self.changeMultiplePartiesStatus( partyIds, newPartyStatus,  True)
        except Exception,e:
            self.notify.warning("Unknown error in changeMultiplePartiesStatus, giving up:\n%s" % str(e))
            return ()
