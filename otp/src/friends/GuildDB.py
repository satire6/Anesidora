import MySQLdb
import _mysql_exceptions
import time
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from otp.distributed import OtpDoGlobals
from otp.uberdog.DBInterface import DBInterface
import random, string

NOACTION_FLAG=0
REVIEW_FLAG=1
DENY_FLAG=2
APPROVE_FLAG=3
ALLDONE_FLAG=4

# During off-line guild token generation, we'll use the badwordpy module to
# check our alpha strings.

try:
    import badwordpy
except ImportError:
    class BadwordDummy:
        def __init__(self, *args):
            pass
        def test(self, word):
            return False
        def scrub(self, str):
            return str
    badwordpy = BadwordDummy()

class GuildDB(DBInterface):
    """
    DB wrapper class for guilds!  All SQL code for guilds should be in here.
    """
    notify = directNotify.newCategory('GuildDB')
        
    def __init__(self,host,port,user,passwd,dbname):
        self.sqlAvailable = uber.sqlAvailable
        if not self.sqlAvailable:
            return

        # Now set the bwDictPath. Used during token generation to make sure
        # we're not giving out any strings that contain bad words
        
        self.bwDictPath = uber.bwDictPath

        # If Path string is empty, flag the dict as being offline

        if self.bwDictPath == "":
            self.bwDictOnline = False
            self.notify.info("Badword filtering for Guild Tokens not online. Dict path not provided")
        else:
            self.bwDictOnline = True
            # Now that the module has loaded, try to init the lib with the
            # bwDictPath provided
            badwordpy.init(self.bwDictPath,"")
            # If the path provided is good, the next if statement should return 1
            if not badwordpy.test("shit"):
                self.notify.info("Bad Word Filtering not online for token guild generation. Dict test failed")
                self.bwDistOnline = False

        # Place startCleanUpExpiredTokens into TaskMgr. It will clean up the
        # expired guild membership tokens every 5 minutes.

        self.startCleanUpExpiredTokens()

        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = self.processDBName(dbname)

        if __debug__:
            self.notify.info("About to connect to %s MySQL db at %s:%d." % (self.dbname, host, port))
        self.db = MySQLdb.connect(host=host,
                                  port=port,
                                  user=user,
                                  passwd=passwd)

        if __debug__:
            self.notify.info("Connected to %s MySQL db at %s:%d." % (self.dbname, host, port))

        #temp hack for initial dev, create DB structure if it doesn't exist already
        cursor = self.db.cursor()
        try:
            cursor.execute("CREATE DATABASE `%s`" % self.dbname)
            if __debug__:
                self.notify.debug("Database '%s' did not exist, created a new one!" % self.dbname)
        except _mysql_exceptions.ProgrammingError,e:
            pass

        cursor.execute("USE `%s`" % self.dbname)
        if __debug__:
            self.notify.debug("Using database '%s'" % self.dbname)
        
        try:
            cursor.execute("CREATE TABLE `guildinfo` (`gid` INT(32) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, `name` VARCHAR(21), `wantname` VARCHAR(21), `namestatus` INT(8), `create_date` DATETIME)")
            if __debug__:
                self.notify.debug("Table guildinfo did not exist, created a new one!")
        except _mysql_exceptions.OperationalError,e:
            pass

        try:
            cursor.execute("CREATE TABLE `member` (`gid` INT(32) UNSIGNED NOT NULL, `avid` INT(32) UNSIGNED NOT NULL PRIMARY KEY, `rank` INT(8) NOT NULL, FOREIGN KEY (`gid`) REFERENCES `guildinfo` (`gid`))")
            if __debug__:
                self.notify.debug("Table member did not exist, created a new one!")
        except _mysql_exceptions.OperationalError,e:
            pass

        try:
            cursor.execute("CREATE TABLE `guildtokens` (`tokenid` VARCHAR(8) NOT NULL PRIMARY KEY, `createtime` DATETIME, `ttl` INT(8) UNSIGNED NOT NULL, `gid` INT(32) UNSIGNED, `avid` INT(32) UNSIGNED, `rcount` INT(8), FOREIGN KEY (`gid`) REFERENCES `guildinfo` (`gid`), FOREIGN KEY (`avid`) REFERENCES `member` (`avid`))")
            # An index should also be added to the avid col
            cursor.execute("CREATE INDEX `avatarid` on guildtokens (avid)")
            if __debug__:
                self.notify.debug("Table guildtokens did not exist, created a new one!")
        except _mysql_exceptions.OperationalError,e:
            pass

# Commented out next table create function for the time being.
# Waiting for "STAF" access.

##         try:
##             cursor.execute("CREATE TABLE `email_notify` (`avid` INT(32) UNSIGNED NOT NULL PRIMARY KEY, `notify` INT(8) NOT NULL, `emailaddress` VARCHAR(75))")
##             if __debug__:
##                 self.notify.debug("Table email_notify did not exist, created a new one!")

##         except _mysql_exceptions.OperationalError,e:
##             pass

    def reconnect(self):
        if __debug__:
            self.notify.debug("MySQL server was missing, attempting to reconnect.")
        try: self.db.close()
        except: pass
        self.db = MySQLdb.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd)
        cursor = self.db.cursor()
        cursor.execute("USE `%s`"%self.dbname)
        if __debug__:
            self.notify.debug("Reconnected to MySQL server at %s:%d."%(self.host,self.port))

    def disconnect(self):
        if not self.sqlAvailable:
            return
        self.db.close()
        self.db = None

    def createGuild(self, avId, isRetry=False):
        if not self.sqlAvailable:
            return
        
        # Enter a new Guild into the guildinfo table, and a new member into the member table
        try:
            # By giving a guild Id of 0, it will auto-increment to the desired id
            # Name fields are left blank
            cursor = self.db.cursor()
            # construct datetime string
            foo = time.localtime()
            date_time = "%d-%d-%d %d:%d:%d" % (foo[0], foo[1], foo[2], foo[3], foo[4], foo[5])
            cursor.execute("INSERT INTO `guildinfo` VALUES (%s, %s, %s, %s, %s)" , (0, 0, 0, 0, date_time))
            cursor.execute("SELECT LAST_INSERT_ID()")
            guildId = cursor.fetchall()[0][0]
            self.addMember(guildId, avId, 3)
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            if isRetry:
                raise e
            else:
                self.reconnect()
                self.createGuild(avId,True)
        except _mysql_exceptions.IntegrityError,e:
            self.notify.warning("IntegrityError creating new guild for avId %s: %s.  Rolling back." % (avId,e))
            from direct.showbase import PythonUtil
            self.notify.warning(str(PythonUtil.StackTrace()))
            self.db.rollback()

    def memberCount(self, guildId):
        if not self.sqlAvailable:
            print "Guild DB Unavailable"
            return 99999

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM `member` where `gid` = %s" , guildId)
            stuff = cursor.fetchall()
            return len(stuff)
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            return self.memberCount(guildId)

        print "Guild DB failed member Count for ", guildId
        return 9999

    def verifyGuild(self, guildId):
        if not self.sqlAvailable:
            print "Guild DB Unavailable"
            return False

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM `guildinfo` where `gid` = %s" , guildId)
            stuff = cursor.fetchall()
            if (len(stuff)):
                return True
            else:
                return False
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            return self.verifyGuild(guildId)


    def queryStatus(self, avatarId):
        if not self.sqlAvailable:
            print "Guild DB Unavailable"
            return 0, "DB Unavailable", 0

        try:
            # Return guildid, name, and rank for the avatarid in question
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM `member` where `avid` = %s" , avatarId)
            # This will return a single row of gid, avid, rank
            stuff = cursor.fetchall()
            if (len(stuff) == 0):
                # We aren't currently in a guild
                guildId = 0
                rank = 0
                name = "Null"
                change = 0
            else:
                guildId = stuff[0][0]
                rank = stuff[0][2]

                cursor.execute("SELECT * FROM `guildinfo` where `gid` = %s" , guildId)
                # This will be a single row with gid, name, wantname
                stuff = cursor.fetchall()
                name = stuff[0][1]
                gstatus = stuff[0][3]
                if (gstatus == 2):
                    change = 2
                elif (gstatus == 3):
                    change = 3
                else:
                    change = 0
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            return self.queryStatus(avatarId)

        return guildId, name, rank, change
        

    def getName(self, guildId):
        if not self.sqlAvailable:
            return "DB Unavailable"

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM `guildinfo` where `gid` = %s" , guildId)
            stuff = cursor.fetchall()
            return stuff[0][1]
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.getName(guildId)


    def tryWantName(self, guildId, wantname):
        if not self.sqlAvailable:
            return

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM `guildinfo` where `wantname` = %s" , wantname)
            stuff = cursor.fetchall()
            count = len(stuff)
            cursor.execute("SELECT * FROM `guildinfo` where `name` = %s" , wantname)
            stuff = cursor.fetchall()
            count += len(stuff)
        except:
            self.reconnect()
            self.setWantName(guildId, wantname)
        
    def setWantName(self, guildId, wantname):
        if not self.sqlAvailable:
            return 0

        # Insert name into want name field for this guild
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM `guildinfo` where `wantname` = %s" , wantname)
            stuff = cursor.fetchall()
            count = len(stuff)
            cursor.execute("SELECT * FROM `guildinfo` where `name` = %s" , wantname)
            stuff = cursor.fetchall()
            count += len(stuff)
            if (count == 0):
                cursor.execute("UPDATE `guildinfo` SET `wantname` = %s WHERE `gid` = %s" , (wantname, guildId))
                cursor.execute("UPDATE `guildinfo` SET `namestatus` = %s WHERE `gid` = %s" , (REVIEW_FLAG, guildId))
                success = 1
            else:
                # No longer actually process the name request, just deny it up front
                # cursor.execute("UPDATE `guildinfo` SET `namestatus` = %s WHERE `gid` = %s" , (DENY_FLAG, guildId))
                success = 2

            self.db.commit()
            return success
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            return self.setWantName(guildId, wantname)

    def getWantName(self, guildId):
        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        # Get currently selected want-name for this guild
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM `guildinfo` where `gid` = %s" , guildId)
            stuff = cursor.fetchall()
            return stuff[0][2]
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.getWantName(guildId)
    
    def approveName(self, guildId):
        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        # Set the official Guildname
        # This will only be called by a customer support application
        cursor = self.db.cursor()
        try:
            wantname = self.getWantName(guildId)
            if (wantname == "0"):
                return
            cursor.execute("UPDATE `guildinfo` SET `wantname` = '0' WHERE `gid` = %s" , (guildId))
            cursor.execute("UPDATE `guildinfo` SET `name` = %s WHERE `gid` = %s" , (wantname, guildId))
            cursor.execute("UPDATE `guildinfo` SET `namestatus` = %s WHERE `gid` = %s" , (APPROVE_FLAG, guildId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.approveName(guildId)

    def rejectName(self, guildId):
        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        # Decline the existing wantname and clear it out
        cursor = self.db.cursor()
        try:
            wantname = self.getWantName(guildId)
            if (wantname == "0"):
                return
            cursor.execute("UPDATE `guildinfo` SET `wantname` = 'Rejected' WHERE `gid` = %s" , (guildId))
            cursor.execute("UPDATE `guildinfo` SET `namestatus` = %s WHERE `gid` = %s" , (DENY_FLAG, guildId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.rejectName(guildId)

    def nameProcessed(self, guildId, newval):
        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        # Decline the existing wantname and clear it out
        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE `guildinfo` SET `namestatus` = %s WHERE `gid` = %s" , (newval, guildId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.nameProcessed(guildId, newval)
        
    def addMember(self, guildId, avId, rank):
        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        if (not self.verifyGuild(guildId)):
            return 0

        # Insert new member into list
        try:
            # All new members start at rank 1
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO `member` VALUES (%s, %s, %s)" , (guildId, avId, rank))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "GuildDB::addMember - reconnect"
            self.addMember(guildId, avId, rank)
            return
        except _mysql_exceptions.IntegrityError,e:
            self.notify.warning("IntegrityError adding avId %s to guild %s: %s.  Rolling back." % (avId,guildId,e))
            from direct.showbase import PythonUtil
            self.notify.warning(str(PythonUtil.StackTrace()))
            self.db.rollback()

    def removeMember(self, avId, guildId, guildRank):
        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        # Remove member from guild
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM `guildtokens` WHERE `avid` = %s", avId)
            cursor.execute("DELETE FROM `member` WHERE `avId` = %s" , avId)
            if (guildRank == 3):
                # Removing guild leader, remove all pending name requests as well
                cursor.execute("UPDATE `guildinfo` SET `wantname` = %s WHERE `gid` = %s" , (0, guildId))
                cursor.execute("UPDATE `guildinfo` SET `namestatus` = %s WHERE `gid` = %s" , (NOACTION_FLAG, guildId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.removeMember(avId)
            return

        if (guildId and self.memberCount(guildId) < 1):
            self.removeGuild(guildId)

    # Only used to remove an empty guild.  Do not do this to a guild with members
    def removeGuild(self, guildId):
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM `guildtokens` WHERE `gid` = %s" , guildId)
            cursor.execute("DELETE FROM `guildinfo` WHERE `gid` = %s", guildId)
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.removeGuild(guildId)
            return

    def changeRank(self, avId, rank):
        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        # Change rank of existing guild member
        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE `member` SET `rank` = %s WHERE `avId` = %s" , (rank, avId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.changeRank(avId, rank)
    
        
    def getMembers(self, guildId):
        if not self.sqlAvailable:
            return []

        # cursor = MySQLdb.cursors.DictCursor(self.db)
        cursor = self.db.cursor()
        
        try:
            cursor.execute("SELECT * FROM `member` where `gid` = %s" , guildId)
            members = cursor.fetchall()
            return members
        except _mysql_exceptions.OperationalError,e:            
            self.reconnect()
            print "DEBUG - Operational Error"
            return self.getMembers(guildId)

    def genToken(self):
        # alpha = string.letters.upper()
        alpha = 'ABCDEFHKLMNPRSTUVWXYZ'
        # num = string.digits
        num = '23456789'
        ranNumber = ''
        ranAlpha = ''
        for i in range(4):
            ranNumber = ranNumber + random.choice(num)
        for i in range(4):
            ranAlpha = ranAlpha + random.choice(alpha)
        token = "%s%s" % (ranAlpha, ranNumber)
        return token

    def isTokenUnique(self, token):
        # Verify that the passed token is unique in the guildToken table
        if not self.sqlAvailable:
            return "Error: DB not online"

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM `guildtokens` where `tokenid` = %s" , token)
            entries = cursor.fetchall()
            if len(entries) == 0:
                return 1
            else:
                return 0
        except _mysql_exceptions.OperationalError,e:            
            self.reconnect()
            print "DEBUG - Operational Error"
            return self.isTokenUnique(token)

    def redeemToken(self, token, avId):
        # Redeem a token, by adding the avid to the guild in the guildtokens DB
        if not self.sqlAvailable:
            return "Error: DB not online"

        # Lets first check to make sure the entry is in the guildtokens table
        cursor = self.db.cursor()
        try:
            # print 'Executing Query for %s' % token
            cursor.execute("SELECT * FROM `guildtokens` where `tokenid` = %s", token)
            entries = cursor.fetchall()
            # print len(entries)
            if len(entries) == 1:
                pass
            else:
                raise Exception("INVALID_TOKEN")
        except _mysql_exceptions.OperationalError,e:            
            self.reconnect()
            print "DEBUG - Operational Error"
            return self.redeemToken(token, avId)


        # Since the entry is there, lets add the avid to the gid
        guildToken = entries[0][0]
        gNameId = entries[0][3]
        creatorAvId = entries[0][4]
        # rCount indicates the code type / redeeem rules, i.e. onetime use,
        # multi-use, unlimited use.
        rCount = entries[0][5]
        # print guildToken, gNameId
        rank = 1

        # Make sure we don't have too many members in the guild
        from otp.friends import GuildManagerUD
        count = self.memberCount(gNameId)
        if (count >= GuildManagerUD.MAX_MEMBERS):
            raise Exception("GUILD_FULL")

        self.addMember(gNameId, avId, rank)

        # Now delete the entry from the guildToken table
        # If rCount is (NULL) None or 1, delete

        if rCount == None or rCount == 1:
            self.deleteFriendToken(guildToken)

        # If rCount >= 2, then we need to decrement the rcount in the rec by 1

        if rCount >= 2:
            self.decRCountInDB(token, creatorAvId, rCount - 1)

        # Return the Guild Name

        return [gNameId, creatorAvId]
        
    def deleteFriendToken(self, token):
        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM `guildtokens` WHERE `tokenid` = %s" , token)
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.deleteFriendToken(token)
            return

    def checkForTooManyTokens(self, avId):
        # Check the guildToken table to make sure the the passed avId does not
        # have too many off-line guild join requests pending.
        # If returns True = Too many entries in table pending. They either have
        # to be redeemed or wait until they expire; the ttl.
        # If returns False = The user does not have too many.
        # Currently the max number of entries is 20. It is set locally in this
        # function

        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM `guildtokens` WHERE `avid` = %s", avId)
            entries = cursor.fetchall()
            if len(entries) >= 20:
                return True
            else:
                return False

        except _mysql_exceptions.OperationalError,e:            
            self.reconnect()
            print "DEBUG - Operational Error - Checking for Too Many Tokens from AVID"
            return self.checkForTooManyTokens(avId)

    def getFriendToken(self, guildId, avId, ttl = 10):
        # Generate a friend token for the membership to the guildId passed
        # Step .5: Verify that the user does not have too many tokens pending
        # Step One: Generate a token (self.genToken)
        # Step Two: Verify that the token does not collide with an existing one
        #           and if self.bwDictOnline == True, check for bad words
        # Step Three: Insert entry into the DB
        # Step Four: Return token string

        # Note: The TTL is in days

        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        # Step .5:

        tooManyTokens = self.checkForTooManyTokens(avId)
        if tooManyTokens == True:
            # Too many tokens pending
            # Return string 'TOO_MANY_TOKENS'
            return 'TOO_MANY_TOKENS'

        from otp.friends import GuildManagerUD
        count = self.memberCount(guildId)
        if (count >= GuildManagerUD.MAX_MEMBERS):
            # Too many people in the guild, refuse to issue a token
            return 'GUILD FULL'

        # Step One:

        ourToken = self.genToken()
        # print 'Token Generated %s.' % ourToken
        # Step Two:

        if self.bwDictPath:
            while not self.isTokenUnique(ourToken) or badwordpy.test(ourToken):
                self.notify.info('Token is not unique or contains a bad word: %s' % ourToken)
                ourToken = self.genToken()

        else:
            while self.isTokenUnique(ourToken) == 0:
                self.notify.info('Token is not unique: %s' % ourToken)
                ourToken = self.genToken()

        # Step Three:

        foo = time.localtime()
        date_time = "%d-%d-%d %d:%d:%d" % (foo[0], foo[1], foo[2], foo[3], foo[4], foo[5])

        try:
            cursor = self.db.cursor()
            cursor.execute("INSERT INTO `guildtokens` VALUES (%s, %s, %s, %s, %s, NULL)", (ourToken, date_time, ttl, guildId, avId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "GuildDB::getFriendToken Error "
            self.getFriendToken(guildId, avId, ttl)

        # Step Four:

        return ourToken

    def changeTokenRValue(self, avatarId, tokenString, rValue):
        # Change the rValue for the token (tokenString)
        # avatarId is passed to allow us to verify that the token being passed
        # is associated with this requesting avId

        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE `guildtokens` SET `rcount` = %s WHERE `avid` = %s AND `tokenid` = %s", (rValue, avatarId, tokenString))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.changeTokenRValue(avatarId, tokenString, rValue)
        self.notify.debug('Guild Token (%s) rValue (%s) Updated for %s' % (tokenString, rValue, avatarId))

    def decRCountInDB(self, token, avId, newRCount):
        # This will decrement the rcount value in the guildtokens table by one
        # Normally, this will get called when we have a multi-use code that
        # has to have its record updated.
        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE `guildtokens` SET `rcount` = %s WHERE `tokenid` = %s AND `avid` = %s", (newRCount, token, avId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            self.decRCountInDB(token, avId, newRCount)
        

    def startCleanUpExpiredTokens(self):
        taskMgr.remove('cleanUpTokensTask')
        taskMgr.doMethodLater(300, self.tokenDeleteSQLCall, 'cleanUpTokensTask')

    def stopCleanUpExpiredTokens(self):
        taskMgr.remove('cleanUpTokensTask')

    def tokenDeleteSQLCall(self, task):
        if not self.sqlAvailable:
            return "DB Unavailable"

        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM `guildtokens` WHERE(`createtime` + INTERVAL `ttl` DAY) < NOW() AND `rcount` = NULL ORDER BY `createtime` LIMIT 100")
            self.db.commit()
            self.notify.debug('Executing expired token cleanup in DB. Deleting up to 100 expired/old tokens')
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "GuildDB::tokenDeleteSQLCall Error "
            self.tokenDeleteSQLCall(task)
        return Task.again

    def checkForUnlimitedUseToken(self, avId):
        # Check the DB to see if avId, currently has a unlimited use token;
        # then token can be active or inactive
        # If unlimited token exists, the tokenId is returned.
        # If unlimited token does not exist, return None
        if not self.sqlAvailable:
            return "DB Unavailable"

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT `tokenid` FROM `guildtokens` WHERE avid = %s AND `rcount` = -1", (avId))
            entries = cursor.fetchall()
            if len(entries) == 0:
                return None
            else:
                return entries[0][0]

        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "DEBUG - Operational Error - checkForUnlimitedUseToken"
            return self.checkForUnlimitedUseToken(avId)

    def returnLimitedUseTokens(self, avId):
        # Returns an int value, corrisponding to the number of limited
        # use tokens in the DB for the avId provided.
        # Limited use tokens count as "one time use" and "limited multi use".
        # If nothing is in the DB, 0 is returned

        if not self.sqlAvailable:
            return "DB Unavailable"

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT `tokenid` FROM `guildtokens` WHERE avid = %s AND (`rcount` != -1 OR `rcount` IS NULL)", (avId))
            entries = cursor.fetchall()
            recCount = len(entries)
            return recCount
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "DEBUG - Operational Error - returnLimitedUseTokens"
            return self.returnLimitedUseTokens(avId)

    def clearLimitedUseTokens(self, avId):
        # Deletes all "Limited Use" tokens for the provided avId from the DB

        if not self.sqlAvailable:
            return "DB Unavailable"

        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM `guildtokens` WHERE `avid` = %s AND (`rcount` != -1 OR `rcount` IS NULL)", (avId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "DEBUG - Error in clearLimitedUseTokens - reconnecting to DB"
            self.clearLimitedUseTokens(avId)
            return

    def clearPermUseTokens(self, avId):
        # Deletes all "Perm Use" tokens for the provided avId from the DB

        if not self.sqlAvailable:
            return "DB Unavailable"

        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM `guildtokens` WHERE `avid` = %s AND `rcount` = -1", (avId))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "DEBUG - Error in clearPermUseTokens - reconnecting to DB"
            self.clearPermUseTokens(avId)
            return

    def suspendToken(self, avId, token):
        # Suspend a perm use token
        # This is done by changing the rcount value for the row to -2

        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE `guildtokens` SET `rcount` = -2 WHERE `avid` = %s AND `tokenid` = %s", (avId, token))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "DEBUG - reconnecting to DB in suspendToken"
            self.suspendToken(avId, token)
            return

    def reEnableToken(self, avId, token):
        # Re-enable a perm use token
        # This is done by changing the rcount value for the row to -1

        if not self.sqlAvailable:
            return "Guild DB Unavailable"

        cursor = self.db.cursor()
        try:
            cursor.execute("UPDATE `guildtokens` SET `rcount` = -1 WHERE `avid` = %s AND `tokenid` = %s", (avId, token))
            self.db.commit()
        except _mysql_exceptions.OperationalError,e:
            self.reconnect()
            print "DEBUG - reconnecting to DB in reEnableToken"
            self.reEnableToken(avId, token)
            return

# Commented out next several functions, waiting for "STAF" access for email. Will uncomment once
# "STAF" Interface is worked out.

##     def getEmailNotificationPref(self, avId):
##         # Get the email notification preferences from the DB for the avid passed in
##         # If no rec exists, create a default entry and return it
##         # Note: Default config is notify = 0 (no), email set to NULL
##         # Returns a list: [notify, emailAddress]

##         if not self.sqlAvailable:
##             return "Guild DB Unavailable"

##         cursor = self.db.cursor()
##         try:
##             cursor.execute("SELECT notify, emailaddress FROM `email_notify` WHERE `avid` = %s" , avId)
##             entry = cursor.fetchall()
##             if len(entry) == 1:
##                 return [entry[0][0], entry[0][1]]
##             else:
##                 self.setEmailNotificationPref(avId, 0, None)
##                 return [0, None]
            
##         except _mysql_exceptions.OperationalError,e:
##             self.reconnect()
##             return getEmailNotificationPref(avId)

##     def setEmailNotificationPref(self, avId, notify, emailAddress):
##         # Set the Email Notification Preferences for an avId
##         # Notify = 0 : Do not notify
##         # Notify = 1 : Notify

##         try:
##             cursor = self.db.cursor()
##             if emailAddress:
##                 cursor.execute("INSERT INTO `email_notify` VALUES (%s, %s, %s)" , (avId, notify, emailAddress))
##             else:
##                 cursor.execute("INSERT INTO `email_notify` (`avid`, `notify`) VALUES (%s, %s)" , (avId, notify))
##             self.db.commit()
##         except _mysql_exceptions.OperationalError,e:
##             self.reconnect()
##             print "GuildDB::setEmailNotificationPref - reconnect"
##             self.setEmailNotificationPref(avId, notify, emailAddress)
##             return
##         except _mysql_exceptions.IntegrityError,e:
##             print "DEBUG - error is ", e

##     def updateNotificationPref(self, avId, notify, emailAddress):
##         # Update the notification rec in the DB

##         try:
##             cursor = self.db.cursor()
##             cursor.execute("UPDATE email_notify SET notify = %s,  emailaddress = %s WHERE avid = %s", (notify, emailAddress, avId))
##             self.db.commit()
##         except  _mysql_exceptions.OperationalError,e:
##             self.reconnect()
##             self.updateNotificationPref(avId, notify, emailAddress)

    #for debugging only
    def dumpGuildTable(self):
        assert self.db,"Tried to call dumpGuildTable when DB was closed."
        cursor = MySQLdb.cursors.DictCursor(self.db)
        cursor.execute("SELECT * FROM guilds")
        return cursor.fetchallDict()

    #for debugging only
    def clearGuildTable(self):
        assert self.db,"Tried to call clearGuildTable when DB was closed."
        cursor = MySQLdb.cursors.DictCursor(self.db)
        cursor.execute("TRUNCATE TABLE guilds")
        self.db.commit()

 
