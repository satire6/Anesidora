class DBKeepAlive:
    """
    Keeps the provided MySQL DB connection from timing out.
    Should only be used in dev.
    """

    instanceCount = 0

    def __init__(self, db, interval = 60.0):
        """
        db should be an active DB connection (returned by MySQLdb.connect).
        interval is the time between keepalives in seconds.
        """
        assert __dev__
        
        self.db = db

        DBKeepAlive.instanceCount += 1

        taskMgr.doMethodLater(interval,
                              self.keepAlive,
                              'DBKeepAlive%s' % DBKeepAlive.instanceCount)

    def keepAlive(self, task):
        cursor = self.db.cursor()
        cursor.execute("SHOW DATABASES")
        cursor.fetchall()
        return task.again
