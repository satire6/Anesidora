class LRUlist:
    """
    A list of data that only gets to size cacheSize before removing the
    LRU (least recently used) element 
    """
    def __init__(self, cacheSize = 256):
        self.cacheSize = cacheSize
        self.dataDictionary = {}
        self.keyList = []
        
    def __pruneData__(self):
        """
        removes the LRU elements beyond cacheSize
        """
        while len(self.keyList) > self.cacheSize:
            _removeKey = self.keyList[self.cacheSize]
            del self.dataDictionary[_removeKey] #optimize
            self.keyList = self.keyList[:-1] #optimize
            #self.removeData(_removeKey)
            
    def setCacheSize(self, cacheSize):
        """
        sets the cacheSize and prunes the data
        """
        self.cacheSize = cacheSize
        self.__pruneData__()
        
    def putData(self, indexKey, data):
        #puts data to the list, then prunes the list
        self.dataDictionary[indexKey] = data
        count = self.keyList.count(indexKey)
        for i in range(count):
            self.keyList.remove(indexKey)
        #if self.keyList.count(indexKey):
        #   self.keyList.remove(indexKey)
        self.keyList.insert(0, indexKey)
        self.__pruneData__()
        
    def removeData(self, indexKey):
        #removes a datum        
        del self.dataDictionary[indexKey]
        self.keyList.remove(indexKey)
        
    def getData(self, indexKey):
        
        if self.dataDictionary.has_key(indexKey):
        #if a datum exists
            _returnData = self.dataDictionary[indexKey]
            self.removeData(indexKey)
            self.putData(indexKey, _returnData)
            return _returnData
            #retreives, removes, adds, and then returns a datum
        else:
        # otherwise return "none"
            return None
            
