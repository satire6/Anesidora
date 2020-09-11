import MySQLdb
import _mysql_exceptions

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.uberdog.DBKeepAlive import DBKeepAlive
from otp.uberdog.DBInterface import DBInterface

class StatusDatabaseUD(DistributedObjectGlobalUD,DBInterface):
    """
    StatusDatabase is a lightweight DB wrapper for status information about avatars.
    This initial version only stores last online times by recording timestamps each
    time an avatar comes online or goes offline.
    
    Currently, he client must pull all desired information using requestOfflineAvatarStatus.
    This can easily change to a push interface later on, if desired.
    """

    notify = directNotify.newCategory('StatusDatabaseUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.avatarId2LastOnline = {}

        self.DBuser = uber.config.GetString("mysql-user", "ud_rw")
        self.DBpasswd = uber.config.GetString("mysql-passwd", "r3adwr1te")

        self.DBhost = "localhost"
        self.DBport = 3306
        self.DBname = self.processDBName("status")

        self.db = MySQLdb.connect(host=self.DBhost,
                                  port=self.DBport,
                                  user=self.DBuser,
                                  passwd=self.DBpasswd)

        self.notify.info("Connected to MySQL server at %s:%d."%(self.DBhost,self.DBport))

        cursor = self.db.cursor()

        try:
            cursor.execute("CREATE DATABASE `%s`"%self.DBname)
            self.notify.info("Database '%s' did not exist, created a new one!"%self.DBname)
        except _mysql_exceptions.ProgrammingError,e:
            pass

        cursor.execute("USE `%s`"%self.DBname)
        self.notify.debug("Using database '%s'"%self.DBname)

        try:
            cursor.execute("""
            CREATE TABLE `offlineAvatarStatus` (
            `avatarId` int(32) UNSIGNED NOT NULL,
            `lastOnlineTime` TIMESTAMP NOT NULL,
            PRIMARY KEY (`avatarId`)
            ) ENGINE=InnoDB
            """)
            self.notify.info("Table offlineAvatarStatus did not exist, created a new one!")
        except _mysql_exceptions.OperationalError,e:
            pass

        if __dev__:
            self.dbkeep = DBKeepAlive(self.db)

        taskMgr.doMethodLater(1.0,self._lazyCommit,'lazyCommit')

    
    def announceGenerate(self):
        self.accept("avatarOnline", self.avatarOnline, [])
        self.accept("avatarOffline", self.avatarOffline, [])
        DistributedObjectGlobalUD.announceGenerate(self)

    def delete(self):
        self.ignoreAll()
        DistributedObjectGlobalUD.delete(self)


    def avatarOnline(self, avatarId, avatarType):
        self._updateLastOnlineTime(avatarId)

    def avatarOffline(self, avatarId):
        self._updateLastOnlineTime(avatarId)


    # CL -> UD
    def requestOfflineAvatarStatus(self, avatarIds):
        """
        CL->UD message to request details for a list of offline avatars.
        Results in a set of UD->CL recvOfflineAvatarStatus messages, one for each avatar.
        """
        if not avatarIds: #return if empty
            return
        
        senderId = self.air.getAvatarIdFromSender()

        if len(avatarIds) > 1000:
            self.notify.warning("Ignoring huge avatarIds list sent to requestOfflineAvatarStatus from sender %s: %s" % (senderId,avatarIds))
            return
        
        onlineTimes = self._getLastOnlineTimes(avatarIds)

        for (avId,onlineTime) in onlineTimes:
            self.sendUpdateToAvatarId(senderId,
                                      "recvOfflineAvatarStatus",
                                      [avId, onlineTime])

        
    # ----- Handy internal functions -----


    def _lazyCommit(self,task):
        self.db.commit()
        return task.again
    

    def _valueList(self, numVals):
        assert numVals > -1
        if numVals == 0:
            return "()"
        else:
            return "(" + ("%s," * (numVals-1)) + "%s)"


    def _getLastOnlineTimes(self, avatarIds):
        """
        Returns a list of pairs of (avatarId,lastOnlineTime) for the given avatarIds.
        If we have no data for an avatarId, (avatarId,0) is returned.
        """
        if len(avatarIds) < 1:
            return

        missing = []

        # Determine who we don't have cached in RAM
        for id in avatarIds:
            if (not id in self.avatarId2LastOnline) and (id > 0):
                missing.append(id)

        # Get the missing people from the DB into RAM
        if len(missing) > 0:
            cursor = self.db.cursor()
            cursor.execute("SELECT avatarId,UNIX_TIMESTAMP(lastOnlineTime) from offlineAvatarStatus WHERE avatarId in " + self._valueList(len(missing)), missing)
            while cursor.rownumber < cursor.rowcount:
                id,lastOnline = cursor.fetchone()
                self.avatarId2LastOnline[id] = lastOnline

        result = []

        # Return results from RAM
        for id in avatarIds:
            lastOnline = self.avatarId2LastOnline.get(id,0)

            result.append((id,lastOnline))

        return result


    def _updateLastOnlineTime(self,avatarId):
        """
        Sets the last online time for the specified avatar to NOW (UTC).
        Value is updated in MySQL and in our in-memory cache.
        """
        assert avatarId > 0

        cursor = self.db.cursor()

        # Update in DB, also read back the timestamp that SQL just recorded so we can cache it
        cursor.execute("""
            INSERT INTO offlineAvatarStatus (avatarId,lastOnlineTime) VALUES (%s,UTC_TIMESTAMP)
            ON DUPLICATE KEY UPDATE lastOnlineTime=UTC_TIMESTAMP;
            SELECT UNIX_TIMESTAMP(lastOnlineTime) from offlineAvatarStatus WHERE avatarId = %s
            """, [avatarId, avatarId])

        # Skip empty result set from INSERT/UPDATE
        cursor.nextset()

        # Get the timestamp our SELECT retrieved and store it in RAM
        assert cursor.rowcount == 1

        lastOnline = cursor.fetchone()[0]
        self.avatarId2LastOnline[avatarId] = lastOnline

        # For 10x performance improvement: Do not commit here!
        # lazyCommit will be called in 1 second or less and flush our changes to disk then.
