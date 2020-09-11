import MySQLdb
import MySQLdb.constants.CR
import MySQLdb.constants.ER
import _mysql_exceptions

from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.uberdog.DBInterface import DBInterface
notify = directNotify.newCategory('SubscriptionToAvatars')


class MySQLAccountAvatarsDB(DBInterface):
    notify = notify
        
    def __init__(self, host, port, user, passwd, dbname):
        #self.sqlAvailable = uber.sqlAvailable
        #if not self.sqlAvailable:
        #    self.notify.warning("SQL not available")
        #    return

        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = self.processDBName(dbname)

        if __debug__:
            self.notify.info("About to open connection to MySQL server at "
                             "%s:%d." % (host, port))
        cursor = self.connect()

        try:
            cursor.execute("CREATE DATABASE %s" % self.dbname)
            if __debug__:
                self.notify.info("MySQL database '%s' did not exist, "
                                 "created a new one." % self.dbname)
        except _mysql_exceptions.ProgrammingError, e:
            pass

        cursor.execute("USE %s" % self.dbname)
        if __debug__:
            self.notify.info("Using MySQL database '%s'." % self.dbname)

        try:
            cursor.execute("""
                CREATE TABLE account_to_avatars
                (avatar_id INT UNSIGNED NOT NULL PRIMARY KEY,
                 creator_id INT UNSIGNED NOT NULL,
                 subscription_id INT UNSIGNED NOT NULL,
                 shared_with_family INT UNSIGNED NOT NULL,
                 birthdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                 last_played TIMESTAMP NULL,
                 datemadeinactive TIMESTAMP NULL);
                 """)
            cursor.execute("""
                CREATE UNIQUE INDEX account_to_avatars_1 
                ON account_to_avatars(subscription_id, avatar_id);
                """)
            if __debug__:
                self.notify.info("Table 'account_to_avatars' did not exist, "
                                 "created a new one.")
        except _mysql_exceptions.OperationalError, e:
            pass

    def connect(self):
        # NOTE 1: The default storage engine is InnoDB and we always want to
        #           ensure that InnoDB is selected.
        # NOTE 2: InnoDB provides MySQL with a transaction-safe storage engine
        #           that has commit, rollback, and crash recovery capabilities.
        # NOTE 3: By default, MySQL runs with autocommit mode enabled,
        #           although MySQLdb follows PEP-249 in the Connection class
        #           constructor by disabling autocommit mode.
        # NOTE 4: The default isolation level of InnoDB is REPEATABLE READ.
        #
        # ISSUE: The affect of disabling autocommit mode and having
        #           isolation level set to REPEATABLE READ is that INSERT and
        #           UPDATE transactions performed on a table that uses the
        #           InnoDB storage engine must be explicitly committed, but
        #           query results do not reflect updates made outside the
        #           context of this connection.
        #
        # RESOLUTION: Either of the following will resolve the issue
        #               described above.
        #   OPTION A: After the database connection is established by
        #               MySQLdb, autocommit can be disabled as follows:
        #
        #                   self.db.autocommit(True)
        #
        #               And the calls to commit can be removed:
        #
        #                   self.db.commit()
        #
        #       PROS: A second round trip to the database is eliminated.
        #       CONS: Multi-step transactions are not possible.
        #
        #   OPTION B: After the database connection is established by
        #               MySQLdb, the isolation level can be updated to READ
        #               COMMITTED at the session level.  A statement such as
        #               the following will accomplish this task:
        #
        #       cursor.execute(
        #           "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
        #
        #       PROS: Multi-step transactions are possible.
        #       CONS: A second round trip to the database is required in
        #               order to perform a commit after each change to the
        #               database is executed.
        #
        self.db = MySQLdb.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd)
        # Enable autocommit mode (all explicit calls to commit have been
        # deleted - see NOTES, ISSUE, and RESOLUTION above)
        self.db.autocommit(True)
        # Return the default cursor associated with this connection
        return self.db.cursor()

    def reconnect(self):
        if __debug__:
            self.notify.warning("MySQL server was missing, "
                                "attempting to reconnect.")
        try:
            self.db.close()
        except:
            pass

        cursor = self.connect()
        cursor.execute("USE %s" % self.dbname)
        if __debug__:
            self.notify.debug("Reconnected to MySQL server at %s:%d." %
                              (self.host, self.port))

    def disconnect(self):
        if not self.sqlAvailable:
            return

        try:
            self.db.close()
        except:
            pass

        self.db = None

    def setSharedFlag(self, avatar, subscription, shared):
        command = """
            UPDATE account_to_avatars 
            SET shared_with_family = %s 
            WHERE avatar_id = %s and subscription_id = %s
            """ % (shared, avatar, subscription)
        try:
            cursor = MySQLdb.cursors.DictCursor(self.db)
            cursor.execute(command)
        except _mysql_exceptions.OperationalError, e:
            if (e[0] == MySQLdb.constants.CR.SERVER_GONE_ERROR) or \
               (e[0] == MySQLdb.constants.CR.SERVER_LOST):
                self.reconnect()
                cursor = MySQLdb.cursors.DictCursor(self.db)
                cursor.execute(command)
            else:
                raise e

    def addAvatarToSubscription(self, avatar, creator, subscription, shared):
        command = """
            INSERT INTO account_to_avatars(
            avatar_id, creator_id, subscription_id, shared_with_family) 
            VALUES (%s, %s, %s, %s)
            """ % (avatar, creator, subscription, shared)
        try:
            cursor = MySQLdb.cursors.DictCursor(self.db)
            cursor.execute(command)
        except _mysql_exceptions.OperationalError, e:
            if (e[0] == MySQLdb.constants.CR.SERVER_GONE_ERROR) or \
               (e[0] == MySQLdb.constants.CR.SERVER_LOST):
                self.reconnect()
                cursor = MySQLdb.cursors.DictCursor(self.db)
                cursor.execute(command)
            else:
                raise e

    def removeAvatarFromSubscription(self, avatar, subscription):
        command = """
            UPDATE account_to_avatars 
            SET datemadeinactive = CURRENT_TIMESTAMP 
            WHERE avatar_id = %s and subscription_id = %s
            """ % (avatar, subscription)
        try:
            cursor = MySQLdb.cursors.DictCursor(self.db)
            cursor.execute(command)
        except _mysql_exceptions.OperationalError, e:
            if (e[0] == MySQLdb.constants.CR.SERVER_GONE_ERROR) or \
               (e[0] == MySQLdb.constants.CR.SERVER_LOST):
                self.reconnect()
                cursor = MySQLdb.cursors.DictCursor(self.db)
                cursor.execute(command)
            else:
                raise e

    def deleteIncompleteAvatarFromDB(self, avatar):
        # Only call this when deleting an avatar we don't ever need to restore
        # CAUTION: THIS WILL REMOVE IT COMPLETELY FROM THE SQL DATABASE
        command = """
            DELETE FROM account_to_avatars 
            WHERE avatar_id = %s
            """ % (avatar)
        try:
            cursor = MySQLdb.cursors.DictCursor(self.db)
            cursor.execute(command)
        except _mysql_exceptions.OperationalError, e:
            if (e[0] == MySQLdb.constants.CR.SERVER_GONE_ERROR) or \
               (e[0] == MySQLdb.constants.CR.SERVER_LOST):
                self.reconnect()
                cursor = MySQLdb.cursors.DictCursor(self.db)
                cursor.execute(command)
            else:
                raise e

    def getAvatarIdsForSubscription(self, subscription):
        command = """
            SELECT avatar_id, creator_id, subscription_id, shared_with_family 
            FROM account_to_avatars 
            WHERE subscription_id = %s AND datemadeinactive IS NULL 
            ORDER BY birthdate
            """ % (subscription)
        try:
            cursor = MySQLdb.cursors.Cursor(self.db)
            cursor.execute(command)
            return cursor.fetchall()
        except _mysql_exceptions.OperationalError, e:
            if (e[0] == MySQLdb.constants.CR.SERVER_GONE_ERROR) or \
               (e[0] == MySQLdb.constants.CR.SERVER_LOST):
                self.reconnect()
                cursor = MySQLdb.cursors.Cursor(self.db)
                cursor.execute(command)
                return cursor.fetchall()
            else:
                raise e

    def lastPlayed(self, avatar, subscription):
        command = """
            UPDATE account_to_avatars 
            SET last_played = CURRENT_TIMESTAMP 
            WHERE avatar_id = %s and subscription_id = %s
            """ % (avatar, subscription)
        try:
            cursor = MySQLdb.cursors.Cursor(self.db)
            cursor.execute(command)
        except _mysql_exceptions.OperationalError, e:
            if (e[0] == MySQLdb.constants.CR.SERVER_GONE_ERROR) or \
               (e[0] == MySQLdb.constants.CR.SERVER_LOST):
                self.reconnect()
                cursor = MySQLdb.cursors.Cursor(self.db)
                cursor.execute(command)
            else:
                raise e

# if __name__ == "__main__":
    # # Create 10 avatar id's for each of 1,000,000 subscription id's
    # fdb = MySQLAccountAvatarsDB("127.0.0.1", 3306, "root", "root", "a")
    # subscriptionBase = 712104
    # for subscriptionId in range(subscriptionBase, 1000001):
    #     if 0 == (subscriptionId % 10):
    #         print "subscriptionId=%d" % subscriptionId
    #     for i in xrange(10):
    #         fdb.addAvatarToSubscription((subscriptionId * 10) + i, 1234, subscriptionId, 1)
    #
    # # Unit test logic
    # fdb = MySQLAccountAvatarsDB("127.0.0.1", 3306, "root", "root", "avatars")
    # fdb.addAvatarToSubscription(3300000002, 1234, 1023, 1)
    # t = fdb.getAvatarIdsForSubscription(1023)
    # print t
    # fdb.addAvatarToSubscription(3300000005, 1234, 1023, 1)
    # t = fdb.getAvatarIdsForSubscription(1023)
    # print t
    # fdb.removeAvatarFromSubscription(3300000005, 1023)
    # t = fdb.getAvatarIdsForSubscription(1023)
    # print t
    # fdb.setSharedFlag(3300000002, 1023, 1)
    # t = fdb.getAvatarIdsForSubscription(1023)
    # print t
    # print "break and execute: UPDATE account_to_avatars SET datemadeinactive = NULL WHERE avatar_id = 3300000005"
    # t = fdb.getAvatarIdsForSubscription(1023)
    # print t
