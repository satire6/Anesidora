if __name__ == '__main__':
    # running as a MySQL communication subprocess

    # redirect any output during module init to stderr
    import sys
    stdOut = sys.stdout
    sys.stdout = sys.stderr
    print 'code redemption subprocess starting...'

    import direct
    from pandac.PandaModules import *
    from direct.showbase.ShowBase import ShowBase
    #showbase = ShowBase(fStartDirect=False, windowType='none')
    config = getConfigShowbase()

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.FSM import FSM
from direct.fsm.StatePush import StateVar, FunctionCall
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.showbase.Job import Job
from direct.stdpy import threading # MySQLdb blocks on locked table access
from otp.uberdog.DBInterface import DBInterface
from toontown.coderedemption.TTCodeDict import TTCodeDict
from toontown.coderedemption import TTCodeRedemptionConsts
from direct.directutil import DirectMySQLdb
import _mysql_exceptions
import random
import datetime
import MySQLdb
import os
import subprocess
import time

class MySQLErrors:
    DbAlreadyExists = 1007
    TableAlreadyExists = 1050
    ServerShuttingDown = 1053
    ServerGoneAway = 2006
    
class TryAgainLater(Exception):
    def __init__(self, mysqlException, address):
        self._exception = mysqlException
        self._address = address
    def getMySQLException(self):
        return self._exception
    def __str__(self):
        return 'problem using MySQL DB at %s, try again later (%s)' % (self._address, self._exception)

class TTDBCursorBase:
    ConnectionProblems = set([MySQLErrors.ServerShuttingDown,
                              MySQLErrors.ServerGoneAway,
                              ])
    def _setConnection(self, connection):
        self._connection = connection
        
    def _doExecute(self, cursorBase, *args, **kArgs):
        if self.notify.getDebug():
            self.notify.debug('execute:\n%s' % u2ascii(args[0]))
        try:
            cursorBase.execute(self, *args, **kArgs)
        except _mysql_exceptions.OperationalError, e:
            if self._connection.getErrorCode(e) in TTDBCursorBase.ConnectionProblems:
                # force a reconnect
                TTCRDBConnection.db = None
                raise TryAgainLater(e, '%s:%s' % (self._connection._host, self._connection._port))
            else:
                raise

class TTDBCursor(MySQLdb.cursors.Cursor, TTDBCursorBase):
    notify = directNotify.newCategory('TTCodeRedemptionDB')

    def execute(self, *args, **kArgs):
        self._doExecute(MySQLdb.cursors.Cursor, *args, **kArgs)

class TTDBDictCursor(MySQLdb.cursors.DictCursor, TTDBCursorBase):
    notify = directNotify.newCategory('TTCodeRedemptionDB')

    def execute(self, *args, **kArgs):
        self._doExecute(MySQLdb.cursors.DictCursor, *args, **kArgs)

class TTCRDBConnection(DBInterface):
    notify = directNotify.newCategory('TTCodeRedemptionDB')

    RetryPeriod = 5.
    TableLockRetryPeriod = 1.

    Connecting = 'Connecting'
    Initializing = 'Initializing'
    Locking = 'Locking'
    Connected = 'Connected'
    Released = 'Released'
    WaitForRetry = 'WaitForRetry'
    WaitForRetryLocking = 'WaitForRetryLocking'

    StartCodeLength = 4

    READ = 'READ'
    WRITE = 'WRITE'

    LoggedConnectionInfo = False
    ConnectedEvent = 'TTCRDBConnectionMgr-Connected-%s'

    WantTableLocking = config.GetBool('want-code-redemption-db-locking', 0)

    db = None

    LastFailedConnectTime = None
    ConnectRetryTimeout = 3.

    def __init__(self, connectInfo, tableLocks={}):
        # tableLocks: table name -> READ||WRITE
        self._host = connectInfo.host
        self._port = connectInfo.port
        self._user = connectInfo.user
        self._passwd = connectInfo.passwd
        self._tableLocks = tableLocks
        self._dbName = connectInfo.dbname
        self._retryDoLater = None
        self._retryLockingDoLater = None
        self._curState = 'Off'
        self.request(self.Connecting)

    # hack FSM to allow request in enter methods
    def request(self, state):
        exitFuncName = 'exit%s' % self._curState
        if hasattr(self, exitFuncName):
            getattr(self, exitFuncName)()
        enterFuncName = 'enter%s' % state
        self._curState = state
        if hasattr(self, enterFuncName):
            getattr(self, enterFuncName)()

    def getState(self):
        return self._curState

    def destroy(self):
        self.release()
        self.request('Off')

    def getConnectedEvent(self):
        return self.ConnectedEvent % id(self)

    def isConnected(self):
        return self._curState == self.Connected

    def getDb(self):
        # returns valid MySQLdb when in Connected state
        return self.__class__.db

    def getCursor(self):
        cursor = TTDBCursor(self.__class__.db)
        cursor._setConnection(self)
        return cursor

    def getDictCursor(self):
        cursor = TTDBDictCursor(self.__class__.db)
        cursor._setConnection(self)
        return cursor

    def commit(self):
        self.__class__.db.commit()

    def release(self):
        self.request('Released')

    def enterConnecting(self):
        if self.__class__.LastFailedConnectTime is not None:
            if (globalClock.getRealTime() - self.__class__.LastFailedConnectTime) < self.ConnectRetryTimeout:
                raise TryAgainLater(None, '%s:%s' % (self._host, self._port))
                
        if not self.__class__.db:
            try:
                self.__class__.db = DirectMySQLdb.connect(host=self._host,
                                                          port=self._port,
                                                          user=self._user,
                                                          passwd=self._passwd)
            except _mysql_exceptions.OperationalError,e:
                """
                self.notify.warning("Failed to connect to MySQL at %s:%d. Retrying in %s seconds."%(
                    self._host,self._port,self.RetryPeriod))
                self.request(self.WaitForRetry)
                """
                self.notify.warning(str(e))
                self.__class__.LastFailedConnectTime  = globalClock.getRealTime()
                raise TryAgainLater(e, '%s:%s' % (self._host, self._port))
            else:
                self.__class__.db.set_character_set('utf8')

                # spammy
                if not self.__class__.LoggedConnectionInfo:
                    self.notify.debug("Connected to MySQL at %s:%d."%(self._host,self._port))
                    self.__class__.LoggedConnectionInfo = True
                self.request(self.Initializing)
        else:
            # no DB initialization required since we're already connected
            self.request(self.Locking)

    def _createTable(self, command):
        cursor = self.getCursor()
        try:
            cursor.execute(command)
        except _mysql_exceptions.OperationalError, e:
            if self.getErrorCode(e) == MySQLErrors.TableAlreadyExists:
                # table already exists
                pass
            else:
                raise

    def enterInitializing(self):
        # create database
        cursor = self.getCursor()
        initDb = config.GetBool('want-code-redemption-init-db', __dev__)
        if initDb:
            try:
                cursor.execute("CREATE DATABASE %s" % self._dbName)
                self.notify.info("database %s did not exist, created new one" % self._dbName)
            except _mysql_exceptions.ProgrammingError, e:
                if self.getErrorCode(e) == MySQLErrors.DbAlreadyExists:
                    # db already exists
                    pass
                else:
                    raise

        cursor.execute("USE %s" % self._dbName)

        if initDb:
            # create tables
            self._createTable(
                """
                CREATE TABLE code_space (
                code_length int(32) unsigned NOT NULL,
                next_code_value bigint(64) unsigned NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                """
                )
            self._createTable(
                """
                CREATE TABLE lot (
                lot_id int(32) unsigned NOT NULL auto_increment,
                name text NOT NULL,
                manual enum('F','T') NOT NULL,
                %(rewardType)s int(32) unsigned NOT NULL,
                %(rewardItemId)s int(32) unsigned NOT NULL,
                size bigint(64) NOT NULL,
                creation DATETIME,
                expiration DATETIME,
                PRIMARY KEY (lot_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                """ % {'rewardType': TTCodeRedemptionDB.RewardTypeFieldName,
                       'rewardItemId': TTCodeRedemptionDB.RewardItemIdFieldName,
                       }
                )

        cursor = self.getDictCursor()

        while 1:
            cursor.execute(
                """
                SELECT code_length, next_code_value FROM code_space;
                """
                )
            rows = cursor.fetchall()
            if len(rows) == 0:
                if self.WantTableLocking:
                    cursor.execute(
                        """
                        LOCK TABLES code_space WRITE;
                        """
                        )
                cursor.execute(
                    """
                    INSERT INTO code_space (code_length, next_code_value) VALUES(%s, 0);
                    """ % (self.StartCodeLength)
                    )
                if self.WantTableLocking:
                    cursor.execute(
                        """
                        UNLOCK TABLES;
                        """
                        )
                self.commit()
                continue
            else:
                assert len(rows) == 1
                break

        self.request(self.Locking)

    def enterLocking(self):
        try:
            if self.WantTableLocking:
                if len(self._tableLocks):
                    cmd = 'LOCK TABLES '
                    for table, lock in self._tableLocks.iteritems():
                        cmd += '%s %s, ' % (table, lock)
                    cmd = cmd[:-2] + ';'
                    self.getCursor().execute(cmd)
        except TryAgainLater,e:
            self.notify.warning('failed to acquire table lock(s), retrying in %s seconds') % (
                self.TableLockRetryPeriod, )
            self.request(self.WaitForRetryLocking)
        else:
            # spammy
            #self.notify.info("tables locked")
            self.request(self.Connected)

    def enterConnected(self):
        messenger.send(self.getConnectedEvent())

    def enterDisconnected(self):
        pass
    def exitDisconnected(self):
        pass

    def enterWaitForRetry(self):
        if self._retryDoLater:
            taskMgr.remove(self._retryDoLater)
        self._retryDoLater = taskMgr.doMethodLater(self.RetryPeriod, self._retryConnect, 'TTCRDBConnectionMgr-retryConnect-%s' % id(self))

    def _retryConnect(self, task=None):
        self.request(self.Connecting)
        return Task.done

    def exitWaitForRetry(self):
        if self._retryDoLater:
            taskMgr.remove(self._retryDoLater)
            self._retryDoLater = None

    def enterWaitForRetryLocking(self):
        if self._retryLockingDoLater:
            taskMgr.remove(self._retryLockingDoLater)
        self._retryLockingDoLater = taskMgr.doMethodLater(self.RetryLockingPeriod, self._retryLocking,
                                                          'TTCRDBConnectionMgr-retryLocking-%s' % id(self))

    def _retryLockingDoLater(self, task=None):
        self.request(self.Locking)
        return Task.done

    def exitWaitForRetryLocking(self):
        if self._retryLockingDoLater:
            taskMgr.remove(self._retryLockingDoLater)
            self._retryLockingDoLater = None

    def enterReleased(self):
        if self.WantTableLocking:
            if len(self._tableLocks):
                self.getCursor().execute('UNLOCK TABLES;')

class TTCodeRedemptionDBTester(Job):
    notify = directNotify.newCategory('TTCodeRedemptionDBTester')

    TestLotName = 'temp_auto_test_lot_'

    class TestRewarder:
        FakeAvId = 2847
        def _giveReward(self, avId, rewardTypeId, rewardItemId, callback):
            callback(0)

    def __init__(self, db):
        self._db = db
        Job.__init__(self, 'TTCodeRedemptionDBTester-%s' % serialNum())

    def getRandomSamples(self, callback, numSamples):
        samples = []
        for i in xrange(numSamples):
            samples.append(int(random.random() * ((1L<<32)-1)))
        callback(samples)

    @classmethod
    def isLotNameValid(cls, lotName):
        # make sure a user doesn't create a lot that matches the test lot naming convention
        return (cls.TestLotName not in lotName)

    @classmethod
    def cleanup(cls, db):
        # remove any leftover data from previous tests
        db._testing = True
        lotNames = db.getLotNames()
        for lotName in lotNames:
            if cls.TestLotName in lotName:
                db.deleteLot(lotName)
        db._testing = False

    def _handleRedeemResult(self, result, awardMgrResult):
        self._redeemResult.append(result)
        self._redeemResult.append(awardMgrResult)

    def _getUnusedLotName(self):
        lotNames = self._db.getLotNames()
        while 1:
            lotName = '%s%s' % (self.TestLotName, int(random.random() * ((1L<<32)-1)))
            if lotName not in lotNames:
                break
        return lotName

    def _getUnusedManualCode(self):
        while 1:
            code = ''
            length = random.randrange(4, 16)
            manualCharIndex = random.randrange(length)
            for i in xrange(length):
                if i == manualCharIndex:
                    charSet = TTCodeDict.ManualOnlyCharacters
                else:
                    charSet = TTCodeDict.ManualCharacters
                char = random.choice(charSet)
                if char in TTCodeDict.IgnoredManualCharacters:
                    i -= 1
                code = code + char
            if not self._db.codeExists(code):
                break
        return code

    def _getUnusedUtf8ManualCode(self):
        chars = u'\u65e5\u672c\u8a9e'
        code = unicode('', 'utf-8')
        while 1:
            code += random.choice(chars)
            if not self._db.codeExists(code):
                break
        return code

    def run(self):
        self.notify.info('testing started')

        retryStartT = None
        retryDelay = 5

        while 1:
            try:
                db = self._db
                db._testing = True

                lotName = self._getUnusedLotName()

                # make sure there are at least one manual and one auto lot throughout the tests
                phLots = []
                phLots.append(self._getUnusedLotName())
                for i in self._db.createLot(self.getRandomSamples, phLots[-1], 1, 0, 0):
                    db._testing = False
                    yield None
                    db._testing = True
                phLots.append(self._getUnusedLotName())
                code = self._getUnusedManualCode()
                self._db.createManualLot(phLots[-1], code, 0, 0)
                db._testing = False
                yield None
                db._testing = True

                # lot creation
                NumCodes = 3
                RewardType = 0
                RewardItemId = 0
                ExpirationDate = '9999-04-01'
                for i in self._db.createLot(self.getRandomSamples, lotName, NumCodes,
                                            RewardType, RewardItemId, ExpirationDate):
                    db._testing = False
                    yield None
                    db._testing = True

                lotNames = self._db.getLotNames()
                if lotName not in lotNames:
                    self.notify.error('could not create code redemption lot \'%s\'' % lotName)
                db._testing = False
                yield None
                db._testing = True

                autoLotNames = self._db.getAutoLotNames()
                if lotName not in autoLotNames:
                    self.notify.error('auto lot \'%s\' not found in getAutoLotNames()' % lotName)
                db._testing = False
                yield None
                db._testing = True

                manualLotNames = self._db.getManualLotNames()
                if lotName in manualLotNames:
                    self.notify.error('auto lot \'%s\' found in getAutoLotNames()' % lotName)
                db._testing = False
                yield None
                db._testing = True

                # get codes in lot
                codes = self._db.getCodesInLot(lotName)
                if len(codes) != NumCodes:
                    self.notify.error('incorrect number of codes from getCodesInLot (%s)' % len(codes))
                db._testing = False
                yield None
                db._testing = True

                # code existance query
                exists = self._db.codeExists(codes[0])
                if not exists:
                    self.notify.error('codeExists returned false for code %s' % codes[0])
                db._testing = False
                yield None
                db._testing = True

                # number of redemptions (not yet redeemed)
                redemptions = self._db.getRedemptions(codes[0])
                if redemptions != 0:
                    self.notify.error(
                        'incorrect number of redemptions (%s) for not-yet-redeemed code %s' % (
                        redemptions, codes[0], ))
                db._testing = False
                yield None
                db._testing = True

                # get lot name from code
                ln = self._db.getLotNameFromCode(codes[0])
                if ln != lotName:
                    self.notify.error('incorrect lot name (%s) from code (%s)' % (ln, codes[0]))
                db._testing = False
                yield None
                db._testing = True

                # get reward from code
                rt, rid = self._db.getRewardFromCode(codes[0])
                if rt != RewardType or rid != RewardItemId:
                    self.notify.error('incorrect reward (%s, %s) from code %s' % (rt, rid))
                db._testing = False
                yield None
                db._testing = True

                # redeem code
                self._redeemResult = []
                self._db.redeemCode(codes[0], self.TestRewarder.FakeAvId, self.TestRewarder(),
                                    self._handleRedeemResult)
                if self._redeemResult[0] or self._redeemResult[1]:
                    self.notify.error('error redeeming code %s for fake avatar %s: %s' % (
                        codes[0], self.TestRewarder.FakeAvId, self._redeemResult))
                db._testing = False
                yield None
                db._testing = True

                # number of redemptions (redeemed)
                redemptions = self._db.getRedemptions(codes[0])
                if redemptions != 1:
                    self.notify.error(
                        'incorrect number of redemptions (%s) for already-redeemed code %s' % (
                        redemptions, codes[0], ))
                db._testing = False
                yield None
                db._testing = True

                # redeem code that has already been redeemed
                self._redeemResult = []
                self._db.redeemCode(codes[0], self.TestRewarder.FakeAvId, self.TestRewarder(),
                                    self._handleRedeemResult)
                if self._redeemResult[0] != TTCodeRedemptionConsts.RedeemErrors.CodeAlreadyRedeemed:
                    self.notify.error('able to redeem code %s twice' % (codes[0]))
                db._testing = False
                yield None
                db._testing = True

                # number of redemptions (redeemed)
                redemptions = self._db.getRedemptions(codes[0])
                if redemptions != 1:
                    self.notify.error(
                        'incorrect number of redemptions (%s) for already-redeemed code %s' % (
                        redemptions, codes[0], ))
                db._testing = False
                yield None
                db._testing = True

                # lookup codes redeemed by avId
                c = self._db.lookupCodesRedeemedByAvId(self.TestRewarder.FakeAvId)
                if len(c) != 1:
                    self.notify.error('lookupCodesRedeemedByAvId returned wrong number of codes: %s' % c)
                if c[0] != codes[0]:
                    self.notify.error('lookupCodesRedeemedByAvId returned wrong code: %s' % c[0])
                db._testing = False
                yield None
                db._testing = True

                # get code details
                details = self._db.getCodeDetails(codes[0])
                if details['code'] != codes[0]:
                    self.notify.error('incorrect code (%s) returned by getCodeDetails(%s)' % (details['code'],
                                                                                              codes[0]))
                if details['av_id'] != self.TestRewarder.FakeAvId:
                    self.notify.error('incorrect av_id (%s) returned by getCodeDetails(%s)' % (details['av_id'],
                                                                                               codes[0]))
                if details[TTCodeRedemptionDB.RewardTypeFieldName] != RewardType:
                    self.notify.error('incorrect av_id (%s) returned by getCodeDetails(%s)' % (
                        details[TTCodeRedemptionDB.RewardTypeFieldName], codes[0]))
                if details[TTCodeRedemptionDB.RewardItemIdFieldName] != RewardItemId:
                    self.notify.error('incorrect av_id (%s) returned by getCodeDetails(%s)' % (
                        details[TTCodeRedemptionDB.RewardItemIdFieldName], codes[0]))
                db._testing = False
                yield None
                db._testing = True

                # get expiration date
                exp = self._db.getExpiration(lotName)
                if exp != ExpirationDate:
                    self.notify.error('incorrect expiration date: %s' % exp)
                db._testing = False
                yield None
                db._testing = True

                # change expiration date
                y = 1111
                m = 4
                d = 1
                NewExp = '%s-%02d-%02d' % (y, m, d)
                assert datetime.datetime.fromtimestamp(time.time()) > datetime.datetime(y, m, d)

                # make sure it doesn't change the expiration date of all lots
                controlLotName = self._getUnusedLotName()
                controlCode = self._getUnusedManualCode()
                controlExp = '%s-%02d-%02d' % (y, m, d+1)
                self._db.createManualLot(controlLotName, controlCode, RewardType, RewardItemId,
                                         expirationDate=controlExp)
                db._testing = False
                yield None
                db._testing = True

                self._db.setExpiration(lotName, NewExp)
                db._testing = False
                yield None
                db._testing = True
                exp = self._db.getExpiration(lotName)
                if (exp != NewExp):
                    self.notify.error('could not change expiration date for lot %s' % lotName)
                db._testing = False
                yield None
                db._testing = True

                cExp = self._db.getExpiration(controlLotName)
                if (cExp != controlExp):
                    self.notify.error('setExpiration changed control lot expiration!')
                db._testing = False
                yield None
                db._testing = True

                self._db.deleteLot(controlLotName)
                db._testing = False
                yield None
                db._testing = True

                # redeem code that is expired
                self._redeemResult = []
                self._db.redeemCode(codes[1], self.TestRewarder.FakeAvId, self.TestRewarder(),
                                    self._handleRedeemResult)
                if self._redeemResult[0] != TTCodeRedemptionConsts.RedeemErrors.CodeIsExpired:
                    self.notify.error('expired code %s was not flagged upon redeem' % (codes[1]))
                db._testing = False
                yield None
                db._testing = True

                # lot deletion
                self._db.deleteLot(lotName)
                db._testing = False
                yield None
                db._testing = True

                codes = (
                    self._getUnusedManualCode(),
                    self._getUnusedUtf8ManualCode(),
                    )
                for code in codes:
                    # manual code lot
                    lotName = self._getUnusedLotName()
                    self.notify.info('manual code: %s' % u2ascii(code))
                    self._db.createManualLot(lotName, code, RewardType, RewardItemId)
                    if not self._db.lotExists(lotName):
                        self.notify.error('could not create manual lot %s' % lotName)
                    if not self._db.codeExists(code):
                        self.notify.error('could not create manual code %s' % code)
                    db._testing = False
                    yield None
                    db._testing = True

                    autoLotNames = self._db.getAutoLotNames()
                    if lotName in autoLotNames:
                        self.notify.error('manual lot \'%s\' found in getAutoLotNames()' % lotName)
                    db._testing = False
                    yield None
                    db._testing = True

                    manualLotNames = self._db.getManualLotNames()
                    if lotName not in manualLotNames:
                        self.notify.error('manual lot \'%s\' not found in getAutoLotNames()' % lotName)
                    db._testing = False
                    yield None
                    db._testing = True

                    # number of redemptions (not-yet-redeemed)
                    redemptions = self._db.getRedemptions(code)
                    if redemptions != 0:
                        self.notify.error(
                            'incorrect number of redemptions (%s) for not-yet-redeemed code %s' % (
                            redemptions, code, ))
                    db._testing = False
                    yield None
                    db._testing = True

                    # redeem manually-created code
                    self._redeemResult = []
                    self._db.redeemCode(code, self.TestRewarder.FakeAvId, self.TestRewarder(),
                                        self._handleRedeemResult)
                    if self._redeemResult[0] or self._redeemResult[1]:
                        self.notify.error('error redeeming code %s for fake avatar %s: %s' % (
                            code, self.TestRewarder.FakeAvId, self._redeemResult))
                    db._testing = False
                    yield None
                    db._testing = True

                    # number of redemptions (not-yet-redeemed)
                    self._db.commitOutstandingRedemptions()
                    redemptions = self._db.getRedemptions(code)
                    if redemptions != 1:
                        self.notify.error(
                            'incorrect number of redemptions (%s) for redeemed code %s' % (
                            redemptions, code, ))
                    db._testing = False
                    yield None
                    db._testing = True

                    # redeem manually-created code again
                    self._redeemResult = []
                    self._db.redeemCode(code, self.TestRewarder.FakeAvId, self.TestRewarder(),
                                        self._handleRedeemResult)
                    if self._redeemResult[0] or self._redeemResult[1]:
                        self.notify.error('error redeeming code %s again for fake avatar %s: %s' % (
                            code, self.TestRewarder.FakeAvId, self._redeemResult))
                    db._testing = False
                    yield None
                    db._testing = True

                    # number of redemptions (not-yet-redeemed)
                    self._db.commitOutstandingRedemptions()
                    redemptions = self._db.getRedemptions(code)
                    if redemptions != 2:
                        self.notify.error(
                            'incorrect number of redemptions (%s) for twice-redeemed code %s' % (
                            redemptions, code, ))
                    db._testing = False
                    yield None
                    db._testing = True

                    self._db.deleteLot(lotName)
                    db._testing = False
                    yield None
                    db._testing = True

                    lotNames = self._db.getLotNames()
                    if lotName in lotNames:
                        self.notify.error('could not delete code redemption lot \'%s\'' % lotName)
                    db._testing = False
                    yield None
                    db._testing = True

                # remove placeholder lots
                for lotName in phLots:
                    self._db.deleteLot(lotName)
                    db._testing = False
                    yield None
                    db._testing = True

                break

            except TryAgainLater, e:
                self.notify.warning('caught TryAgainLater exception during self-test, retrying')
                retryStartT = globalClock.getRealTime()
                while globalClock.getRealTime() < (retryStartT + retryDelay):
                    yield None
                retryDelay *= 2

        self.notify.info('testing done')
        db._testing = False
        yield Job.Done

class NotFound:
    pass

class InfoCache:
    NotFound = NotFound
    
    def __init__(self):
        self._cache = {}

    def clear(self):
        self._cache = {}

    def cacheInfo(self, key, info):
        self._cache[key] = info

    def hasInfo(self, key):
        return key in self._cache

    def getInfo(self, key):
        return self._cache.get(key, NotFound)

class TTCodeRedemptionDB(DBInterface, DirectObject):
    notify = directNotify.newCategory('TTCodeRedemptionDB')

    TryAgainLater = TryAgainLater

    READ = TTCRDBConnection.READ
    WRITE = TTCRDBConnection.WRITE

    RewardTypeFieldName = 'reward_type'
    RewardItemIdFieldName = 'reward_item_id'

    DoSelfTest = config.GetBool('code-redemption-self-test', 1)

    # optimization that reads in all codes and maps them to their lot
    # if the code set gets too large this might use up too much RAM
    # you can disable the optimization by turning this config off
    CacheAllCodes = config.GetBool('code-redemption-cache-all-codes', 1)

    class LotFilter:
        All = 'all'
        Redeemable = 'redeemable'
        NonRedeemable = 'nonRedeemable'
        Redeemed = 'redeemed'
        Expired = 'expired'

    def __init__(self,air,host,port,user,passwd,dbname):
        self.air = air
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = self.processDBName(dbname)

        # lot name cache
        self._code2lotNameCache = InfoCache()
        self._lotName2manualCache = InfoCache()
        self._code2rewardCache = InfoCache()
        self.doMethodLater(5 * 60, self._cacheClearTask, uniqueName('clearLotNameCache'))

        self._manualCode2outstandingRedemptions = {}
        self.doMethodLater(1 * 60, self._updateRedemptionsTask, uniqueName('updateRedemptions'))

        self._code2lotName = {}

        # set to true while doing internal tests
        self._testing = False
        self._initializedSV = StateVar(False)
        self._startTime = globalClock.getRealTime()
        self._doingCleanup = False
        self._dbInitRetryTimeout = 5
        self._doInitialCleanup()

        if config.GetBool('code-redemption-subprocess-test', 0):
            self._testSubProc()

        self._refreshCode2lotName()

    def _doInitialCleanup(self, task=None):
        if not self._initializedSV.get():
            self._doCleanup()
        if not self._initializedSV.get():
            self.doMethodLater(self._dbInitRetryTimeout, self._doInitialCleanup,
                               uniqueName('codeRedemptionInitialCleanup'))
            self._dbInitRetryTimeout *= 2
            self.notify.warning('could not initialize MySQL db, trying again later...')
        return Task.done

    def _doCleanup(self):
        if self._doingCleanup:
            return

        self._doingCleanup = True

        if not self._initializedSV.get():
            try:
                TTCodeRedemptionDBTester.cleanup(self)
            except TryAgainLater, e:
                pass
            else:
                self._initializedSV.set(True)

        self._doingCleanup = False

    def _randFuncCallback(self, randList, randSamplesOnOrder, samples):
        randSamplesOnOrder[0] -= len(samples)
        randList.extend(samples)

    def _refreshCode2lotName(self):
        if not self.CacheAllCodes:
            return
        # update the dict of code -> lotName for all codes
        self._code2lotName = {}
        lotNames = self.getLotNames()
        for lotName in lotNames:
            codes = self.getCodesInLot(lotName)
            for code in codes:
                self._code2lotName[code] = lotName

    @staticmethod
    def _getExpirationString(expiration):
        """
        formats expiration date for MySQL
        """
        return '\'%s 23:59:59\'' % str(expiration)

    @staticmethod
    def _getNowString():
        nowStr = str(datetime.datetime.fromtimestamp(time.time()))
        # leave off the fractional seconds
        if '.' in nowStr:
            nowStr = nowStr[:nowStr.index('.')]
        return nowStr

    def createManualLot(self, name, code, rewardType, rewardItemId, expirationDate=None):
        self.notify.info('creating manual code lot \'%s\', code=%s' % (name, u2ascii(code), ))
        self._doCleanup()

        code = TTCodeDict.getFromReadableCode(code)

        if self.lotExists(name):
            self.notify.error('tried to create lot %s that already exists' % name)

        if self.codeExists(code):
            self.notify.error('tried to create code %s that already exists' % u2ascii(code))

        conn = TTCRDBConnection(self)
        conn._createTable(
            """
            CREATE TABLE code_set_%s (
            code text NOT NULL,
            lot_id int(32) unsigned NOT NULL,
            redemptions bigint(64) NOT NULL,
            FOREIGN KEY (lot_id) REFERENCES lot (lot_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """ % (name, )
            )
        conn.destroy()

        conn = TTCRDBConnection(self, {'lot': self.WRITE,
                                       'code_set_%s' % name: self.WRITE,
                                       })
        cursor = conn.getDictCursor()

        cursor.execute(
            """
            INSERT INTO lot (name, manual, %s, %s, size, creation%s)
            VALUES('%s', 'T', %s, %s, 1, '%s'%s);
            """ % (self.RewardTypeFieldName,
                   self.RewardItemIdFieldName,
                   choice(expirationDate is None, '', ', expiration'),
                   name, rewardType, rewardItemId, self._getNowString(),
                   choice(expirationDate is None, '', ', %s' % self._getExpirationString(expirationDate)),
                   )
            )

        cursor.execute(
            """
            SELECT lot_id FROM lot WHERE name='%s';
            """ % (name)
            )
        rows = cursor.fetchall()
        lotId = int(rows[0]['lot_id'])

        cursor.execute(
            """
            INSERT INTO code_set_%s (code, lot_id, redemptions)
            VALUES('%s', %s, 0);
            """ % (name, code, lotId)
            )

        conn.release()
        conn.commit()
        conn.destroy()

        self._refreshCode2lotName()

        self.notify.info('done')

    def createLot(self, randFunc, name, numCodes, rewardType, rewardItemId, expirationDate=None):
        """
        generator, yields None while working, yields True when finished
        randFunc must take a callback and a number of random samples, and must call the callback
        with a list of random 32-bit values of length equal to that specified in the call to randFunc
        the random values must be truly random and non-repeatable (see NonRepeatableRandomSource)
        """
        self.notify.info('creating code lot \'%s\', %s codes' % (name, numCodes, ))
        self._doCleanup()

        if self.lotExists(name):
            self.notify.error('tried to create lot %s that already exists' % name)

        randSampleRequestSize = config.GetInt('code-redemption-rand-request-size', 50)
        randSampleRequestThreshold = 2 * randSampleRequestSize
        randSamples = []
        randSamplesOnOrder = [0, ]

        requestSize = min(numCodes, randSampleRequestSize)
        randSamplesOnOrder[0] += requestSize
        randFunc(Functor(self._randFuncCallback, randSamples, randSamplesOnOrder), requestSize)

        conn = TTCRDBConnection(self)
        conn._createTable(
            """
            CREATE TABLE code_set_%s (
            code text NOT NULL,
            lot_id int(32) unsigned NOT NULL,
            redemptions bigint(64) NOT NULL,
            av_id int(32) unsigned,
            FOREIGN KEY (lot_id) REFERENCES lot (lot_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """ % (name, )
            )
        conn.destroy()

        conn = TTCRDBConnection(self, {'code_space': self.WRITE,
                                       'lot': self.WRITE,
                                       'code_set_%s' % name: self.WRITE,
                                       })
        cursor = conn.getDictCursor()

        # grab the next serial number range
        cursor.execute(
            """
            SELECT code_length, next_code_value FROM code_space;
            """
            )
        rows = cursor.fetchall()
        assert len(rows) == 1
        codeLength = int(rows[0]['code_length'])
        nextCodeValue = int(rows[0]['next_code_value'])

        startSerialNum = nextCodeValue

        cursor.execute(
            """
            INSERT INTO lot (name, manual, %s, %s, size, creation%s)
            VALUES('%s', 'F', %s, %s, %s, '%s'%s);
            """ % (self.RewardTypeFieldName,
                   self.RewardItemIdFieldName,
                   choice(expirationDate is None, '', ', expiration'),
                   name, rewardType, rewardItemId, numCodes, self._getNowString(),
                   choice(expirationDate is None, '', ', %s' % self._getExpirationString(expirationDate)),
                   )
            )

        cursor.execute(
            """
            SELECT lot_id FROM lot WHERE name='%s';
            """ % (name)
            )
        rows = cursor.fetchall()
        lotId = int(rows[0]['lot_id'])

        codesLeft = numCodes
        curSerialNum = startSerialNum
        numCodeValues = TTCodeDict.getNumUsableValuesInCodeSpace(codeLength)
        n = 0
        while codesLeft:
            #print codesLeft, len(randSamples), randSamplesOnOrder[0]
            numCodesRequested = (len(randSamples) + randSamplesOnOrder[0])
            if numCodesRequested < codesLeft:
                if numCodesRequested < randSampleRequestThreshold:
                    requestSize = min(codesLeft, randSampleRequestSize)
                    randSamplesOnOrder[0] += requestSize
                    randFunc(Functor(self._randFuncCallback, randSamples, randSamplesOnOrder), requestSize)

            if len(randSamples) == 0:
                yield None
                continue
                
            # r in [0,1) but truly random (non-repeatable)
            r = randSamples.pop(0) / float(1L<<32)
            assert 0. <= r < 1.
            # this produces the 1 in N chance of guessing a correct code
            # each code is given a chunk of code space, of size N, and the actual value of the
            # code is chosen from that section of code space using a true random source
            # that means there's no way to guess a valid code based on observation of other codes
            randScatter = int(r * TTCodeDict.BruteForceFactor)
            assert 0 <= randScatter < TTCodeDict.BruteForceFactor
            value = (curSerialNum * TTCodeDict.BruteForceFactor) + randScatter
            obfValue = TTCodeDict.getObfuscatedCodeValue(value, codeLength)
            code = TTCodeDict.getCodeFromValue(obfValue, codeLength)
            cursor.execute(
                """
                INSERT INTO code_set_%s (code, lot_id, redemptions)
                VALUES('%s', %s, 0);
                """ % (name, code, lotId)
                )

            codesLeft -= 1
            curSerialNum += 1
            if curSerialNum >= numCodeValues:
                curSerialNum = 0
                codeLength += 1
                numCodeValues = TTCodeDict.getNumUsableValuesInCodeSpace(codeLength)

            n = n + 1
            if (n % 100) == 0:
                yield None

        # update the code_space tracking variables
        cursor.execute(
            """
            UPDATE code_space SET code_length=%s, next_code_value=%s;
            """ % (codeLength, curSerialNum)
            )

        conn.release()
        conn.commit()
        conn.destroy()

        self._refreshCode2lotName()

        self.notify.info('done')
        yield True

    def deleteLot(self, lotName):
        self.notify.info('deleting code lot \'%s\'' % (lotName, ))
        self._doCleanup()

        self._clearCaches()
        
        conn = TTCRDBConnection(self)
        cursor = conn.getDictCursor()

        cursor.execute(
            """
            DROP TABLE IF EXISTS code_set_%s;
            """ % lotName
            )

        if conn.WantTableLocking:
            cursor.execute(
                """
                LOCK TABLES lot WRITE;
                """
                )

        cursor.execute(
            """
            DELETE FROM lot WHERE name='%s';
            """ % lotName
            )

        if conn.WantTableLocking:
            cursor.execute(
                """
                UNLOCK TABLES;
                """
                )

        conn.commit()
        conn.destroy()

        self._refreshCode2lotName()

    def getLotNames(self):
        assert self.notify.debugCall()
        self._doCleanup()
        lotNames = []
        conn = TTCRDBConnection(self, {'lot': self.READ, })
        cursor = conn.getDictCursor()
        cursor.execute(
            """
            SELECT name FROM lot;
            """
            )
        rows = cursor.fetchall()
        conn.destroy()
        for row in rows:
            lotName = row['name']
            if not self._testing:
                if TTCodeRedemptionDBTester.TestLotName in lotName:
                    continue
            lotNames.append(lotName)
        return lotNames

    def getAutoLotNames(self):
        """
        returns names of all code lots that were automatically generated
        """
        assert self.notify.debugCall()
        self._doCleanup()
        autoLotNames = []
        conn = TTCRDBConnection(self, {'lot': self.READ, })
        cursor = conn.getDictCursor()
        cursor.execute(
            """
            SELECT name FROM lot WHERE manual='F';
            """
            )
        rows = cursor.fetchall()
        conn.destroy()
        for row in rows:
            lotName = row['name']
            if not self._testing:
                if TTCodeRedemptionDBTester.TestLotName in lotName:
                    continue
            autoLotNames.append(lotName)
        return autoLotNames

    def getManualLotNames(self):
        """
        returns names of all code lots that were manually generated
        """
        assert self.notify.debugCall()
        self._doCleanup()
        manualLotNames = []
        conn = TTCRDBConnection(self, {'lot': self.READ, })
        cursor = conn.getDictCursor()
        cursor.execute(
            """
            SELECT name FROM lot WHERE manual='T';
            """
            )
        rows = cursor.fetchall()
        conn.destroy()
        for row in rows:
            lotName = row['name']
            if not self._testing:
                if TTCodeRedemptionDBTester.TestLotName in lotName:
                    continue
            manualLotNames.append(lotName)
        return manualLotNames

    def getExpirationLotNames(self):
        """
        returns names of all code lots that have expiration dates
        """
        assert self.notify.debugCall()
        self._doCleanup()
        lotNames = []
        conn = TTCRDBConnection(self, {'lot': self.READ, })
        cursor = conn.getDictCursor()
        cursor.execute(
            """
            SELECT name FROM lot WHERE expiration IS NOT NULL;
            """
            )
        rows = cursor.fetchall()
        conn.destroy()
        for row in rows:
            lotName = row['name']
            if not self._testing:
                if TTCodeRedemptionDBTester.TestLotName in lotName:
                    continue
            lotNames.append(lotName)
        return lotNames

    def getCodesInLot(self, lotName, justCode=True, filter=None):
        # if justCode, returns list of codes
        # if not justCode, returns list of dict of field->value
        assert self.notify.debugCall()
        self._doCleanup()
        if filter is None:
            filter = self.LotFilter.All

        conn = TTCRDBConnection(self, {'code_set_%s' % lotName: self.READ,
                                       'lot': self.READ, })
        cursor = conn.getDictCursor()

        if filter == self.LotFilter.All:
            condition = ''
        elif filter == self.LotFilter.Redeemable:
            condition = ('((manual=\'T\' or redemptions=0) and '
                         '((expiration IS NULL) or (CURDATE()<=expiration)))')
        elif filter == self.LotFilter.NonRedeemable:
            condition = ('((manual=\'F\' and redemptions>0) or '
                         '((expiration IS NOT NULL) and (CURDATE()>expiration)))')
        elif filter == self.LotFilter.Redeemed:
            condition = '(redemptions>0)'
        elif filter == self.LotFilter.Expired:
            condition = '((expiration is NOT NULL) and (CURDATE()>expiration))'

        cursor.execute(
            """
            SELECT %s FROM code_set_%s INNER JOIN lot WHERE code_set_%s.lot_id=lot.lot_id%s%s;
            """ % (choice(justCode, 'code', '*'), lotName, lotName,
                   choice(filter==self.LotFilter.All, '', ' AND '), condition)
            )
        rows = cursor.fetchall()
        conn.destroy()

        if justCode:
            codes = []
            for row in rows:
                code = unicode(row['code'], 'utf-8')
                codes.append(code)
            result = codes
        else:
            for row in rows:
                row['code'] = unicode(row['code'], 'utf-8')
            result = rows
        return result

    def _clearCaches(self):
        self._code2lotNameCache.clear()
        self._lotName2manualCache.clear()
        self._code2rewardCache.clear()

    def _cacheClearTask(self, task):
        self._clearCaches()
        return Task.again

    def commitOutstandingRedemptions(self):
        if len(self._manualCode2outstandingRedemptions):
            self.notify.info('committing cached manual code redemption counts to DB')
        conn = TTCRDBConnection(self)
        cursor = conn.getDictCursor()
        for key in self._manualCode2outstandingRedemptions.iterkeys():
            code, lotName = key
            count = self._manualCode2outstandingRedemptions[key]
            self._updateRedemptionCount(cursor, code, True, None, lotName, count)
        self._manualCode2outstandingRedemptions = {}
        conn.destroy()

    def _updateRedemptionsTask(self, task):
        try:
            self.commitOutstandingRedemptions()
        except TryAgainLater, e:
            pass
        return Task.again

    def getLotNameFromCode(self, code):
        assert self.notify.debugCall()

        code = TTCodeDict.getFromReadableCode(code)
        assert TTCodeDict.isLegalCode(code)

        if self.CacheAllCodes:
            return self._code2lotName.get(code, None)

        cachedLotName = self._code2lotNameCache.getInfo(code)
        if cachedLotName is not self._code2lotNameCache.NotFound:
            return cachedLotName

        assert self.notify.debug('lotNameFromCode CACHE MISS (%s)' % u2ascii(code))

        self._doCleanup()
        conn = TTCRDBConnection(self)
        cursor = conn.getDictCursor()

        lotNames = self.getLotNames()
        result = None
        for lotName in lotNames:
            if conn.WantTableLocking:
                cursor.execute(
                    """
                    LOCK TABLES code_set_%s READ;
                    """ % (lotName, )
                    )

            # client hack prevention:
            # safe; code is between quotes and can only contain letters, numbers and dashes
            cursor.execute(
                unicode("""
                SELECT code FROM code_set_%s WHERE code='%s';
                """, 'utf-8') % (lotName, code)
                )
            rows = cursor.fetchall()

            if conn.WantTableLocking:
                cursor.execute(
                    """
                    UNLOCK TABLES;
                    """
                    )

            if len(rows) > 0:
                result = lotName
                break

        conn.destroy()

        if result is not None:
            self._code2lotNameCache.cacheInfo(code, result)

        return result

    def getRewardFromCode(self, code):
        assert self.notify.debugCall()
        
        code = TTCodeDict.getFromReadableCode(code)
        assert TTCodeDict.isLegalCode(code)

        lotName = self.getLotNameFromCode(code)
        assert lotName is not None

        cachedReward = self._code2rewardCache.getInfo(code)
        if cachedReward is not self._code2rewardCache.NotFound:
            return cachedReward

        assert self.notify.debug('reward from code CACHE MISS (%s)' % u2ascii(code))
        
        self._doCleanup()

        conn = TTCRDBConnection(self, {'code_set_%s' % lotName: self.READ,
                                       'lot': self.READ, })
        cursor = conn.getDictCursor()

        # client hack prevention:
        # safe; code is between quotes and can only contain letters, numbers and dashes
        cursor.execute(
            unicode("""
            SELECT %s, %s FROM code_set_%s INNER JOIN lot
            WHERE lot.lot_id=code_set_%s.lot_id AND CODE='%s';
            """, 'utf-8') % (self.RewardTypeFieldName, self.RewardItemIdFieldName, lotName, lotName, code)
            )
        rows = cursor.fetchall()

        conn.destroy()

        assert len(rows) == 1
        reward = (int(rows[0][self.RewardTypeFieldName]), int(rows[0][self.RewardItemIdFieldName]))

        self._code2rewardCache.cacheInfo(code, reward)

        return reward

    def lotExists(self, lotName):
        return lotName in self.getLotNames()

    def codeExists(self, code):
        return self.getLotNameFromCode(code) != None

    def getRedemptions(self, code):
        assert self.notify.debugCall()
        self._doCleanup()
        code = TTCodeDict.getFromReadableCode(code)

        lotName = self.getLotNameFromCode(code)

        if lotName is None:
            self.notify.error('getRedemptions: could not find code %s' % u2ascii(code))

        conn = TTCRDBConnection(self, {'code_set_%s' % lotName: self.READ, })
        cursor = conn.getDictCursor()

        cursor.execute(
            unicode("""
            SELECT redemptions FROM code_set_%s WHERE code='%s';
            """, 'utf-8') % (lotName, code)
            )
        rows = cursor.fetchall()

        conn.destroy()

        return int(rows[0]['redemptions'])
        
    def redeemCode(self, code, avId, rewarder, callback):
        assert self.notify.debugCall()
        self._doCleanup()
        # callback takes a RedeemError
        # 'code' can come from a client, treat with care
        origCode = code
        code = TTCodeDict.getFromReadableCode(code)
        assert TTCodeDict.isLegalCode(code)
        
        lotName = self.getLotNameFromCode(code)
        if lotName is None:
            self.air.writeServerEvent('invalidCodeRedemption', avId, '%s' % (u2ascii(origCode), ))
            callback(TTCodeRedemptionConsts.RedeemErrors.CodeDoesntExist, 0)
            return

        conn = TTCRDBConnection(self, {'code_set_%s' % lotName: self.READ,
                                       'lot': self.READ, })
        cursor = conn.getDictCursor()

        cachedManual = self._lotName2manualCache.getInfo(lotName)
        if cachedManual is not self._lotName2manualCache.NotFound:
            manualCode = cachedManual
        else:
            assert self.notify.debug('manualFromCode CACHE MISS (%s)' % u2ascii(code))
            
            cursor.execute(
                """
                SELECT manual FROM lot WHERE name='%s';
                """ % (lotName)
                )

            rows = cursor.fetchall()
            assert len(rows) == 1

            manualCode = (rows[0]['manual'] == 'T')

            self._lotName2manualCache.cacheInfo(lotName, manualCode)

        if not manualCode:
            # client hack prevention:
            # safe; code is between quotes and can only contain letters, numbers and dashes
            cursor.execute(
                unicode("""
                SELECT redemptions FROM code_set_%s INNER JOIN lot WHERE
                code_set_%s.lot_id=lot.lot_id AND code='%s' AND ((expiration IS NULL) OR (CURDATE()<=expiration));
                """, 'utf-8') % (lotName, lotName, code)
                )

            rows = cursor.fetchall()
            assert len(rows) <= 1

        conn.destroy()

        if not manualCode:
            if len(rows) == 0:
                # code is expired
                callback(TTCodeRedemptionConsts.RedeemErrors.CodeIsExpired, 0)
                return

            redemptions = rows[0]['redemptions']

            if redemptions > 0:
                callback(TTCodeRedemptionConsts.RedeemErrors.CodeAlreadyRedeemed, 0)
                return

        rewardTypeId, rewardItemId = self.getRewardFromCode(code)

        rewarder._giveReward(avId, rewardTypeId, rewardItemId, Functor(
            self._handleRewardResult, code, manualCode, avId, lotName, rewardTypeId, rewardItemId,
            callback))

    def _updateRedemptionCount(self, cursor, code, manualCode, avId, lotName, count):
        # client hack prevention:
        # safe; code is between quotes and can only contain letters, numbers and dashes
        cursor.execute(
            unicode("""
            UPDATE code_set_%s SET redemptions=redemptions+%s%s WHERE code='%s';
            """, 'utf-8') % (lotName, count, choice(manualCode, '', ', av_id=%s' % avId), code)
            )

    def _handleRewardResult(self, code, manualCode, avId, lotName, rewardTypeId, rewardItemId,
                            callback, result):
        assert self.notify.debugCall()
        self._doCleanup()
        assert TTCodeDict.isLegalCode(code)
        awardMgrResult = result
        if awardMgrResult:
            callback(TTCodeRedemptionConsts.RedeemErrors.AwardCouldntBeGiven, awardMgrResult)
            return
        
        conn = TTCRDBConnection(self, {'code_set_%s' % lotName: self.WRITE, })
        cursor = conn.getDictCursor()

        if manualCode:
            # queue up redemption count for manual code and write every N minutes
            key = (code, lotName)
            self._manualCode2outstandingRedemptions.setdefault(key, 0)
            self._manualCode2outstandingRedemptions[key] += 1
        else:
            self._updateRedemptionCount(cursor, code, manualCode, avId, lotName, 1)

        conn.release()
        conn.commit()
        conn.destroy()

        if not self._testing:
            self.air.writeServerEvent('codeRedeemed', avId, '%s|%s|%s|%s' % (
                u2ascii(choice(manualCode, code, TTCodeDict.getReadableCode(code))),
                lotName, rewardTypeId, rewardItemId, ))

        callback(TTCodeRedemptionConsts.RedeemErrors.Success, awardMgrResult)

    def lookupCodesRedeemedByAvId(self, avId):
        assert self.notify.debugCall()
        self._doCleanup()
        conn = TTCRDBConnection(self)
        cursor = conn.getDictCursor()

        codes = []

        # manual lots don't record redeemer avIds since they are single-code-multi-toon
        for lotName in self.getAutoLotNames():
            if conn.WantTableLocking:
                cursor.execute(
                    """
                    LOCK TABLES code_set_%s READ;
                    """ % (lotName, )
                    )

            cursor.execute(
                """
                SELECT code FROM code_set_%s WHERE av_id=%s;
                """ % (lotName, avId)
                )
            rows = cursor.fetchall()

            if conn.WantTableLocking:
                cursor.execute(
                    """
                    UNLOCK TABLES;
                    """
                    )

            for row in rows:
                code = unicode(row['code'], 'utf-8')
                codes.append(code)

        conn.destroy()

        return codes

    def getExpiration(self, lotName):
        assert self.notify.debugCall()
        self._doCleanup()
        conn = TTCRDBConnection(self, {'lot': self.READ, })
        cursor = conn.getDictCursor()

        cursor.execute(
            """
            SELECT expiration FROM lot WHERE name=\'%s\';
            """ % (lotName, )
            )

        rows = cursor.fetchall()

        conn.destroy()

        # just get the date component
        expiration = str(rows[0]['expiration'].date())
        return expiration

    def setExpiration(self, lotName, expiration):
        assert self.notify.debugCall()
        self._doCleanup()
        conn = TTCRDBConnection(self, {'lot': self.WRITE, })
        cursor = conn.getDictCursor()

        cursor.execute(
            """
            UPDATE lot SET expiration=%s WHERE name=\'%s\';
            """ % (self._getExpirationString(expiration), lotName, )
            )

        conn.release()
        conn.commit()
        conn.destroy()

    def getCodeDetails(self, code):
        assert self.notify.debugCall()
        self._doCleanup()
        conn = TTCRDBConnection(self)
        cursor = conn.getDictCursor()

        for lotName in self.getLotNames():
            if conn.WantTableLocking:
                cursor.execute(
                    """
                    LOCK TABLES lot READ, code_set_%s READ;
                    """ % (lotName, )
                    )

            cursor.execute(
                """
                SELECT * FROM code_set_%(lotName)s INNER JOIN lot
                WHERE code_set_%(lotName)s.lot_id=lot.lot_id
                AND code='%(code)s';
                """ % ({
                'lotName': lotName,
                'code': TTCodeDict.getFromReadableCode(code)
                })
                )
            rows = cursor.fetchall()

            if conn.WantTableLocking:
                cursor.execute(
                    """
                    UNLOCK TABLES;
                    """
                    )

            assert len(rows) <= 1
            if len(rows):
                conn.destroy()
                row = rows[0]
                row['code'] = unicode(row['code'], 'utf-8')
                return row

        self.notify.error('code \'%s\' not found' % u2ascii(code))

    def _testSubProc(self):
        self.notify.info('running subprocess test...')
        proc = subprocess.Popen('%s -OO %s' % (choice(__dev__, 'python', os.getenv('PYTHON')), __file__),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        proc.stdin.write('test' + '\n')
        result = proc.stdout.readline()
        print 'main process: %s' % repr(result)
        while result[-1] in ('\r', '\n'):
            result = result[:-1]
        if (result == 'testtest'):
            self.notify.info('subprocess test succeeded!')
        else:
            self.notify.info('subprocess test failed! (%s)' % repr(result))

    if __debug__:
        def runTests(self):
            self._doRunTests(self._initializedSV.get())
            self._runTestsFC = FunctionCall(self._doRunTests, self._initializedSV)

        def _doRunTests(self, initialized):
            if initialized and self.DoSelfTest:
                jobMgr.add(TTCodeRedemptionDBTester(self))

# this file itself is the SQL communication subprocess when run directly
if __name__ == '__main__':
    # restore stdout
    sys.stdout = stdOut

    l = sys.stdin.readline()
    sys.stderr.write('subprocess: %s\n' % repr(l))
    sys.stderr.flush()
    while l[-1] in ('\r', '\n'):
        l = l[:-1]
    sys.stdout.write((l * 2) + '\n')
    sys.stdout.flush()
