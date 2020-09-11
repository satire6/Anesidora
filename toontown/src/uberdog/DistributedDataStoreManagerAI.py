from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.AsyncRequest import AsyncRequest
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem

class DistributedDataStoreManagerAI(DistributedObjectAI):
    """
    This is the main gateway for any DataStoreAIClients to
    communicate to the Uberdog.  There should only be one of these
    per AI.

    We should only use the queryStore functions from now on.  The
    start/stopStore functions are provided for backwards compatibility
    for some Toontown uses.
    """
    
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def startStore(self,storeId):
        """
        Causes the Uberdog to bring up the desired store.
        If it's already up, this has no effect.
        """
        self.ud_startStore(storeId)

    def stopStore(self,storeId):
        """
        Causes the Uberdog to bring down the desired store.
        If it's already down, this has no effect.

        CAUTION: this will cause the permanent destruction
        of any data currently in the store.
        """
        self.ud_stopStore(storeId)

    def queryStore(self,storeId,query):
        """
        Send a formatted query to the store.  The format
        should be defined in a subclass of the 
        DataStore class.
        """
        self.ud_queryStore(storeId,query)

    # To UD
    def ud_startStore(self,storeId):
        self.sendUpdate('startStore',[storeId])

    def ud_stopStore(self,storeId):
        self.sendUpdate('stopStore',[storeId])

    def ud_queryStore(self,storeId,query):
        self.sendUpdate('queryStore',[storeId,query])

    # From UD
    def receiveResults(self,storeId,data):
        """
        Sends a message to be received by any interested
        DataStoreAIClients on the AI.

        Since all requests to all data stores must go through
        this class, this is where the data gets dispatched from
        this Uberdog data trunk to the AI client branches
        """
        messenger.send('TDS-results-%d'%storeId,sentArgs=[data])
        
    def deleteBackupStores(self):
        """
        Delete the backedup stores from previous years
        """
        self.sendUpdate('deleteBackupStores')
