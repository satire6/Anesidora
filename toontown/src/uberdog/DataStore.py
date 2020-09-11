from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import ConfigVariableBool
from direct.task import Task

from string import maketrans
import cPickle
import os
import sys
import anydbm
import time

class DataStore:
    """
    This is the base class for all temporary data storage containers on
    the Uberdog.  It handles all the disk access needs for us.  In order
    to create a usable store, subclass this class and override the
    handleQuery() function.  Also, instantiate a corresponding
    DataStoreAIClient on the AI.

    See DataStoreGlobals.py, TrickOrTreatScavengerHuntDataStore.py,
    and TrickOrTreatMgrAI.py for an example of how to use this class.
    """

    # Define the available query strings.
    # The DataStoreAIClient will take one of these strings
    #    as a parameter to send a query.
    # This is here in case we think of any universal queries.
    QueryTypes = [] # ['Query_one','Query_two',...]
    QueryTypes = dict(zip(QueryTypes,range(len(QueryTypes))))

    @classmethod
    def addQueryTypes(cls,typeStrings):
        superTypes = zip(cls.QueryTypes.values(),cls.QueryTypes.keys())
        superTypes.sort()
        newTypes = [item[1] for item in superTypes] + typeStrings
        newTypes = dict(zip(newTypes,range(1+len(newTypes))))
        return newTypes

    notify = DirectNotifyGlobal.directNotify.newCategory('DataStore')
    
    wantAnyDbm = ConfigVariableBool('want-ds-anydbm',1).getValue()
    
    def __init__(self,filepath,writePeriod = 300, writeCountTrigger = 100):
        """
        filepath is where the data for this store will be held on the disk.
        writePeriod is a value, in seconds, for how often we should check
           to see if the data needs to synchronized with the disk data. If
           they match already, the timer resets to 0 without writing.
        writeCountTrigger is maximum number of writes we can perform before
           synchronizing with the disk data.  This will also reset the
           writePeriod timer to 0.
        """
        self.filepath = filepath
        self.writePeriod = writePeriod
        self.writeCountTrigger = writeCountTrigger
        self.writeCount = 0
        self.data = None
        self.className = self.__class__.__name__

        if self.wantAnyDbm:
            self.filepath += '-anydbm'
            self.notify.debug('anydbm default module used: %s ' % anydbm._defaultmod.__name__)

        self.open()
        
    def readDataFromFile(self):
        """
        Looks for a backup data file, ie. A file that only exists
        while the current data is being written to disk.  If it is
        present, we assume there was some failure during the last
        data synchronization and we should use the backup data instead.
        If it is not present we look for the normal data file.

        We then set self.data to the values loaded from the chosen
        file and return True.

        If no file is present, self.data is set to None, and we
        return False.
        """
        #import pdb; pdb.set_trace()
        if self.wantAnyDbm:
            try:
                if os.path.exists(self.filepath):
                    self.data = anydbm.open(self.filepath,'w')
                    self.notify.debug('Opening existing anydbm database at: %s.' % \
                                       (self.filepath,))
                else:
                    self.data = anydbm.open(self.filepath,'c')
                    self.notify.debug('Creating new anydbm database at: %s.' % \
                                      (self.filepath,))
            except anydbm.error:
                self.notify.warning('Cannot open anydbm database at: %s.' % \
                                    (self.filepath,))
                
        else:
            try:
                # Try to open the backup file:
                file = open(self.filepath + '.bu', 'r')
                self.notify.debug('Opening backup pickle data file at %s.' % \
                                  (self.filepath+'.bu',))
                # Remove the (assumed) broken file:
                if os.path.exists(self.filepath):
                    os.remove(self.filepath)
            except IOError:
                # OK, there's no backup file, good.
                try:
                    # Open the real file:
                    file = open(self.filepath, 'r')
                    self.notify.debug('Opening old pickle data file at %s..' % \
                                      (self.filepath,))
                except IOError:
                    # OK, there's no file.
                    file = None
                    self.notify.debug('New pickle data file will be written to %s.' % \
                                      (self.filepath,))
            if file:
                data = cPickle.load(file)
                file.close()
                self.data = data
            else:
                self.data = {}
        
    def writeDataToFile(self):
        """
        Attempt to store the contents of self.data to disk.

        If not using anydbm, a backup file is created for
        the duration of this process and then deleted when
        complete.
        """
        if self.data is not None:
            self.notify.debug('Data is now synced with disk at %s' % \
                              self.filepath)
            if self.wantAnyDbm:
                self.data.sync()
            else:
                try:
                    backuppath = self.filepath+ '.bu'
                    if os.path.exists(self.filepath):
                        os.rename(self.filepath,backuppath)
                        
                    outfile = open(self.filepath, 'w')
                    cPickle.dump(self.data,outfile)
                    outfile.close()
                        
                    if os.path.exists(backuppath):
                        os.remove(backuppath)
                except EnvironmentError:
                    self.notify.warning(str(sys.exc_info()[1]))
        else:
            self.notify.warning('No data to write. Aborting sync.')

        
    def syncTask(self,task):
        """
        This task is responsible for synchronizing the data in memory with
        the data on the disk.

        It will write under two conditions:
        1 - The data is out of sync and a specified amount of time
            has passed.
        2 - There have been a specified number of updates to the
            data in memory.
        """
        task.timeElapsed += globalClock.getDt()
        
        if task.timeElapsed > self.writePeriod:
            if self.writeCount:
                self.writeDataToFile()
                self.resetWriteCount()
            task.timeElapsed = 0.0


        if self.writeCount > self.writeCountTrigger:
            self.writeDataToFile()
            self.resetWriteCount()
            task.timeElapsed = 0.0

        return Task.cont

    def incrementWriteCount(self):
        """
        Record that we have updated the data.
        """
        self.writeCount += 1

    def resetWriteCount(self):
        """
        Clear the update status of the data.
        """
        self.writeCount = 0
        
    def close(self):
        """
        Syncs the RAM data with the disk.
        Removes the syncTask from the taskMgr.
        sets self.data to None.
        """
        if self.data is not None:
            self.writeDataToFile()
            if self.wantAnyDbm:
                self.data.close()
            taskMgr.remove('%s-syncTask'%(self.className,))
            self.data = None

    def open(self):
        """
        Loads the data from disk into RAM.
        Starts the periodic update task.
        """
        self.close()        
        self.readDataFromFile()        
        self.resetWriteCount()
        
        taskMgr.remove('%s-syncTask'%(self.className,))
        t = taskMgr.add(self.syncTask,'%s-syncTask'%(self.className,))
        t.timeElapsed = 0.0
        
    def reset(self):
        """
        Destroys the store's data and opens a blank store.
        """
        self.destroy()
        self.open()
        
    def destroy(self):
        """
        Closes the store.
        Creates a backup (anydbm) or deletes the data from the disk.
        """
        self.close()
        if self.wantAnyDbm:
            lt = time.asctime(time.localtime())
            trans = maketrans(': ','__')
            t = lt.translate(trans)
            head, tail = os.path.split(self.filepath)
            newFileName = 'UDStoreBak'+t
            if os.path.exists(self.filepath):
                try:
                    os.rename(tail, newFileName)
                    uber.air.writeServerEvent('Uberdog data store Info', 0 \
                                                    , 'Creating backup of file: %s saving as: %s' %(tail, newFileName))
                except:
                    uber.air.writeServerEvent('Uberdog data store Info', 0 \
                                                    , 'Unable to create backup of file: %s ' %tail)
            else:
                # Remove the filename with all sufix's
                # .bak, .dir, .dat
                files = os.listdir(head)
                for file in files:
                    if file.find(tail)>-1:
                        filename, ext = os.path.splitext(file)
                        try:
                            os.rename(file, newFileName+ext)
                            uber.air.writeServerEvent('Uberdog data store Info', 0 \
                                                    , 'Creating backup of file: %s saving as: %s' %(file,newFileName+ext))
                        except:
                            uber.air.writeServerEvent('Uberdog data store Info', 0 \
                                                    , 'Unable to create backup of file: %s ' %newFileName+ext)
        else:
            if os.path.exists(self.filepath + '.bu'):
                os.remove(self.filepath + '.bu')
            if os.path.exists(self.filepath):
                os.remove(self.filepath)

    def query(self,query):
        """
        Unpacks a query and sends the unpacked data
        to handleQuery().  It then packs the results from
        the handleQuery() call and returns them.
        """
        if self.data is not None:
            qData = cPickle.loads(query)
            results = self.handleQuery(qData)
            qResults = cPickle.dumps(results)
        else:
            results = None
            qResults = cPickle.dumps(results)
        return qResults

    def handleQuery(self,query):
        """
        This should be overridden by subclasses.
        """
        results = None
        return results

