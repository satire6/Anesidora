from otp.ai.AIBaseGlobal import *
from pandac.PandaModules import *

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from toontown.uberdog import DataStoreGlobals

import time
import os


class DistributedDataStoreManagerUD(DistributedObjectGlobalUD):
    """
    This is UD gateway to all DataStores.  It receives queries
    from various AIs, locates the desired store, runs the query, and sends
    back a response(if specified).

    It looks for two config variables:

    'server-data-folder' is a string that specifies the directory in
    which each of the Stores will write their data. It defaults to '.'.

    'enable-destroy-data-stores' controls whether the DataStore can be
    destroyed by calling destroy().  If not, destroy() has no effect.
    It defaults to 'False'.
    """
    
    notify = directNotify.newCategory('DistributedDataStoreManagerUD')

    serverDataFolder = simbase.config.GetString('server-data-folder', '.')
    enableDestroyStore = simbase.config.GetBool('enable-destroy-data-stores', True)
    
    def __init__(self,air):
        DistributedObjectGlobalUD.__init__(self,air)
        self.stores = {}

    def __getFilePath(self,storeId):
        #import pdb; pdb.set_trace()
        return '%s/TUDS-%s'%(self.serverDataFolder,
                             `storeId`)

    def __str__(self):
        outStr = self.__class__.__name__ + ' - ' + `len(self.stores)` + ' Stores\n'
        outStr += '-'*40 + '\n'
        for id in self.stores.keys():
            outStr += `id` + '\t:  ' + self.stores[id].className + '\n'
        return outStr

    # From AI
    def startStore(self,storeId):
        """
        Starts a store corresponding to the id as specified
        in DataStoreGlobals.
        If the store is already present, it has no effect.
        """
        storeClass = DataStoreGlobals.getStoreClass(storeId)
        
        if not self.stores.get(storeId,None):            
            if storeClass is not None:
                store = storeClass(self.__getFilePath(storeId))
                if store:
                    self.stores[storeId] = store
            else:
                self.notify.debug('DataStore type \'%d\' not found DataStoreGlobals. Store not started.' % \
                                  (storeId,))
        else:
            self.notify.debug('%s already present on uberdog.' % \
                              (storeClass.__name__,))
                
    def stopStore(self,storeId):
        """
        Closes the store corresponding to the id as specified
        in DataStoreGlobals if the config variable
        'enable-destroy-data-stores' is True.  Otherwise
        it just closes it, leaving the data on disk
        intact.
        
        If the store is not present, it has no effect.
        """
        # import pdb; pdb.set_trace()
        store = self.stores.pop(storeId,None)
        if store:
            if self.enableDestroyStore:
                self.notify.debug('Destroying %s.' % `DataStoreGlobals.getStoreClass(storeId)`)
                store.destroy()
            else:
                self.notify.debug('Closing %s.' % `DataStoreGlobals.getStoreClass(storeId)`)
                store.close()
        else:
            self.notify.debug('%s not present on uberdog.' % `DataStoreGlobals.getStoreClass(storeId)`)
            
    def queryStore(self,storeId,query,retry = False):
        """
        Pass a query on to the specified store and
        respond with any results.  If the store is
        not present, return an error message to let
        the client know.

        'retry' is to let us know that this call is
        an attempt to re-send a query that failed
        because the desired store was not yet active.
        We will try to start the store here and send
        the query again.  We only do this once per
        query, otherwise we could get into an
        infinite loop if the store cannot be started.
        """
        store = self.stores.get(storeId,None)
        
        if store:
            result = store.query(query)
            self.respondToQuery(storeId,result)
        else:
            if retry:
                result = 'Store not found'
                self.respondToQuery(storeId,result)
                
                storeClass = DataStoreGlobals.getStoreClass(storeId)
                if storeClass:
                    self.notify.debug('%s not present on uberdog. Query dropped.' % \
                                      (storeClass.__name__,))
                else:
                    self.notify.debug('Store of typeId %s not defined in DataStoreGlobals. Query dropped.' % \
                                      (storeId,))
            else:
                self.startStore(storeId)
                self.queryStore(storeId,query,True)
                
                    
    # To AI
    def respondToQuery(self,storeId,data):
        """
        Sends a message back to the querying AI with
        the results of its query.
        """
        replyToChannel = self.air.getSenderReturnChannel()
        self.sendUpdateToChannel(
            replyToChannel, 'receiveResults', [storeId,data])
            
    def deleteBackupStores(self):
        """
        Delete any backed up stores from previous year's
        """
        year = time.localtime()[0]
        for file in os.listdir(self.serverDataFolder):
            if file.find('UDStoreBak')>-1 and file.find(str(year))==-1:
                os.remove(file)
                uber.air.writeServerEvent('Uberdog data store Info', 0 \
                                                    , 'Removing backup file: %s ' %file)