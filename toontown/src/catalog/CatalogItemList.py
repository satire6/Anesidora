import CatalogItem
from pandac.PandaModules import *
import types
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

class CatalogItemList:
    """CatalogItemList

    This class presents itself as a list of CatalogItem objects.  It
    behaves like a normal Python list, except it supports lazy
    decoding: it can be initialized from a blob received by the
    network system; it won't attempt to decode the blob until some
    properties of the catalog list are requested.  This saves some CPU
    time for the majority of cases when we download the
    CatalogItemList but don't care about inspecting it.
    """

    def __init__(self, source = None, store = 0):
        # The source may be either a list, a string blob, or another
        # CatalogItemList object.

        # The store parameter indicates the bitmask of additional
        # properties we will store in (or decode from) the blob along
        # with each CatalogItem.  See CatalogItem.py.
        self.store = store
        
        # The data is stored in either or both of self.__blob and
        # self.__list.  If either one is None, the current data is
        # stored in the other.  If both are None, the data represents
        # an empty list.
        self.__blob = None
        self.__list = None

        if isinstance(source, types.StringType):
            self.__blob = source
        elif isinstance(source, types.ListType):
            self.__list = source[:]
        elif isinstance(source, CatalogItemList):
            # Copy from another CatalogItemList.
            if source.store == store:
                # If the store types are the same, we can get away
                # with copying the list (if it is defined), and also
                # copying the blob.
                if source.__list != None:
                    self.__list = source.__list[:]
                self.__blob = source.__blob
            else:
                # If the store types are different, we must copy the list.
                self.__list = source[:]
        else:
            assert(source == None)

    def markDirty(self):
        # Call this whenever you know one of the items has changed
        # internally and you need to regenerate a new blob that
        # reflects that change.
        if self.__list:
            self.__blob = None

    def getBlob(self, store = None):
        if store == None or store == self.store:
            # If we are asking for a blob that matches our store type,
            # we can just return our cached value.
            if self.__blob == None:
                self.__encodeList()
            return self.__blob

        # Otherwise, we must compute a new blob according to the
        # indicated store type.
        return self.__makeBlob(store)

    def getNextDeliveryDate(self):
        # Returns the minimum of all the listed items' delivery times,
        # or None if the list is empty.
        if len(self) == 0:
            return None
        
        nextDeliveryDate = None
        for item in self:
            #print ("item %s" %(item))
            if item:
                if nextDeliveryDate == None or \
                   item.deliveryDate < nextDeliveryDate:
                    nextDeliveryDate = item.deliveryDate

        return nextDeliveryDate
        
    def getNextDeliveryItem(self):
        # Returns the minimum of all the listed items' delivery times,
        # or None if the list is empty.
        if len(self) == 0:
            return None
        
        nextDeliveryDate = None
        nextDeliveryItem = None
        for item in self:
            if item:
                if nextDeliveryDate == None or \
                   item.deliveryDate < nextDeliveryDate:
                    nextDeliveryDate = item.deliveryDate
                    nextDeliveryItem = item

        return nextDeliveryItem

    def extractDeliveryItems(self, cutoffTime):
        # Extracts from the list the set of items whose delivery time
        # is on or before the cutoff time.  Returns a list of items to
        # be delivered and a list of items still on the way.
        
        beforeTime = []
        afterTime = []
        for item in self:
            if item.deliveryDate <= cutoffTime:
                beforeTime.append(item)
            else:
                afterTime.append(item)

        return (CatalogItemList(beforeTime, store = self.store),
                CatalogItemList(afterTime, store = self.store))

    def extractOldestItems(self, count):
        # Extracts from the list the count oldest items.  Returns a
        # list of the extracted items and a list of remaining items.

        # Actually, we can cheat because we know new items are always
        # appended to the end of the list.  So just extract the first
        # n items.
        return (self[0:count], self[count:])
    
    def __encodeList(self):
        # We shouldn't try to call this function twice.
        assert(self.__blob == None)
        self.__blob = self.__makeBlob(self.store)

    def __makeBlob(self, store):
        # Construct a new datagram and fill it up with the items in
        # the list.
        dg = PyDatagram()
        if self.__list:  # empty list or None means nothing on the list.
            dg.addUint8(CatalogItem.CatalogItemVersion)
            for item in self.__list:
                CatalogItem.encodeCatalogItem(dg, item, store)
        return dg.getMessage()
        
    def __decodeList(self):
        # We shouldn't try to call this function twice.
        assert(self.__list == None)
        self.__list = self.__makeList(self.store)

    def __makeList(self, store):
        # Construct a new list and populate it with the items decoded
        # from the blob.
        list = []
        if self.__blob:  # empty string or None means nothing on the list.
            dg = PyDatagram(self.__blob)
            di = PyDatagramIterator(dg)
            versionNumber = di.getUint8()
            while di.getRemainingSize() > 0:
                item = CatalogItem.decodeCatalogItem(di, versionNumber, store)
                list.append(item)
        return list


    # Functions to make this act just like a Python list.
    
    def append(self, item):
        if self.__list == None:
            self.__decodeList()
        self.__list.append(item)
        self.__blob = None

    def extend(self, items):
        self += items

    def count(self, item):
        if self.__list == None:
            self.__decodeList()
        return self.__list.count(item)

    def index(self, item):
        if self.__list == None:
            self.__decodeList()
        return self.__list.index(item)

    def insert(self, index, item):
        if self.__list == None:
            self.__decodeList()
        self.__list.insert(index, item)
        self.__blob = None

    def pop(self, index = None):
        if self.__list == None:
            self.__decodeList()
        self.__blob = None
        if index == None:
            return self.__list.pop()
        else:
            return self.__list.pop(index)

    def remove(self, item):
        if self.__list == None:
            self.__decodeList()
        self.__list.remove(item)
        self.__blob = None

    def reverse(self):
        if self.__list == None:
            self.__decodeList()
        self.__list.reverse()
        self.__blob = None

    def sort(self, cmpfunc = None):
        if self.__list == None:
            self.__decodeList()
        if cmpfunc == None:
            self.__list.sort()
        else:
            self.__list.sort(cmpfunc)
        self.__blob = None

    def __len__(self):
        if self.__list == None:
            self.__decodeList()
        return len(self.__list)

    def __getitem__(self, index):
        if self.__list == None:
            self.__decodeList()
        return self.__list[index]

    def __setitem__(self, index, item):
        if self.__list == None:
            self.__decodeList()
        self.__list[index] = item
        self.__blob = None

    def __delitem__(self, index):
        if self.__list == None:
            self.__decodeList()
        del self.__list[index]
        self.__blob = None

    def __getslice__(self, i, j):
        if self.__list == None:
            self.__decodeList()
        return CatalogItemList(self.__list[i : j], store = self.store)

    def __setslice__(self, i, j, s):
        if self.__list == None:
            self.__decodeList()
        if isinstance(s, CatalogItemList):
            self.__list[i : j] = s.__list
        else:
            self.__list[i : j] = s
        self.__blob = None

    def __delslice__(self, i, j):
        if self.__list == None:
            self.__decodeList()
        del self.__list[i : j]
        self.__blob = None

    def __iadd__(self, other):
        if self.__list == None:
            self.__decodeList()
        self.__list += list(other)
        self.__blob = None
        return self

    def __add__(self, other):
        copy = CatalogItemList(self, store = self.store)
        copy += other
        return copy


    def __repr__(self):
        return self.output()

    def __str__(self):
        return self.output()

    def output(self, store = ~0):
        if self.__list == None:
            self.__decodeList()
        inner = ""
        for item in self.__list:
            inner += ", %s" % (item.output(store))
        return "CatalogItemList([%s])" % (inner[2:])

