from pandac.PandaModules import *
from ToontownAIMsgTypes import *
from direct.directnotify.DirectNotifyGlobal import *
from toontown.toon import DistributedToonAI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
import types

class DatabaseObject:
    """DatabaseObject

    This class stores an object as retrieved directly from the
    database via some special direct-to-database queries.  It is used
    for in-game operations as well as offline database repair utilities.
    """

    notify = directNotify.newCategory("DatabaseObject")
    notify.setInfo(0)
    
    def __init__(self, air, doId=None, doneEvent="DatabaseObject"):
        self.air = air
        self.doId = doId
        self.values = {}
        self.gotDataHandler = None
        self.doneEvent = doneEvent

    def readToon(self, fields = None):
        # Reads and returns a DistributedToonAI object.  Note that an
        # empty DistributedToonAI will be returned by this call; the
        # values will be filled in on the toon at some later point in
        # time, after the database has responded to the query.
        toon = DistributedToonAI.DistributedToonAI(self.air)
        self.readObject(toon, fields)
        return toon

    if simbase.wantPets:
        def readPet(self):
            # Reads and returns a Pet object. Note that the same warnings
            # apply as readToon() re: empty object and fields being filled
            # in later
            from toontown.pets import DistributedPetAI
            pet = DistributedPetAI.DistributedPetAI(self.air)
            self.readObject(pet, None)
            return pet

        def readPetProxy(self):
            # Reads and returns a Pet Proxy object. Note that the same warnings
            # apply as readToon() re: empty object and fields being filled
            # in later
            from toontown.pets import DistributedPetProxyAI
            petProxy = DistributedPetProxyAI.DistributedPetProxyAI(self.air)
            self.readObject(petProxy, None)
            return petProxy   

    def readObject(self, do, fields = None):
        # Reads a DistributedObject from the database and fills in its
        # data.  The data is not available immediately, but rather
        # when the self.doneEvent is thrown.
        self.do = do
        className = do.__class__.__name__
        self.dclass = self.air.dclassesByName[className]
        self.gotDataHandler = self.fillin

        # If fields is supplied, it is a subset of fields to read.
        if fields != None:
            self.getFields(fields)
        else:
            self.getFields(self.getDatabaseFields(self.dclass))

    def storeObject(self, do, fields = None):
        # Copies the data from the indicated DistributedObject and
        # writes it to the database.
        self.do = do
        className = do.__class__.__name__
        self.dclass = self.air.dclassesByName[className]

        if fields != None:
            self.reload(self.do, self.dclass, fields)
        else:
            dbFields = self.getDatabaseFields(self.dclass)
            self.reload(self.do, self.dclass, dbFields)

        values = self.values
        if fields != None:
            # If fields is supplied, it is a subset of fields to update.
            values = {}
            for field in fields:
                if self.values.has_key(field):
                    values[field] = self.values[field]
                else:
                    self.notify.warning("Field %s not defined." % (field))
                    
        self.setFields(values)

    def getFields(self, fields):
        # Get a unique context for this query and associate ourselves
        # in the map.
        context = self.air.dbObjContext
        self.air.dbObjContext += 1
        self.air.dbObjMap[context] = self
        
        dg = PyDatagram()
        dg.addServerHeader(DBSERVER_ID, self.air.ourChannel, DBSERVER_GET_STORED_VALUES)
        dg.addUint32(context)
        dg.addUint32(self.doId)
        dg.addUint16(len(fields))
        for f in fields:
            dg.addString(f)
            
        self.air.send(dg)

    def getFieldsResponse(self, di):
        objId = di.getUint32()
        if objId != self.doId:
            self.notify.warning("Unexpected doId %d" % (objId))
            return

        count = di.getUint16()
        fields = []
        for i in range(count):
            name = di.getString()
            fields.append(name)

        retCode = di.getUint8()
        if retCode != 0:
            self.notify.warning("Failed to retrieve data for object %d" % (self.doId))

        else:
            values = []
            for i in range(count):
                value = di.getString()
                values.append(value)

            for i in range(count):
                found = di.getUint8()

                if not found:
                    # this occurs for all DB fields on a pet when it's first created
                    # this should be a warning, but until we can create pets with
                    # their required fields initialized in the DB, keep this as 'info'
                    self.notify.info("field %s is not found" % (fields[i]))

                    try:
                        del self.values[fields[i]]
                    except:
                        pass
                else:
                    self.values[fields[i]] = PyDatagram(values[i])

            self.notify.info("got data for %d" % (self.doId))

            if self.gotDataHandler != None:
                self.gotDataHandler(self.do, self.dclass)
                self.gotDataHandler = None

        if self.doneEvent != None:
            messenger.send(self.doneEvent, [self, retCode])

    def setFields(self, values):
        dg = PyDatagram()
        dg.addServerHeader(DBSERVER_ID, self.air.ourChannel, DBSERVER_SET_STORED_VALUES)
        
        dg.addUint32(self.doId)
        dg.addUint16(len(values))

        items = values.items()
        for field, value in items:
            dg.addString(field)
        for field, value in items:
            dg.addString(value.getMessage())
            
        self.air.send(dg)

    def getDatabaseFields(self, dclass):
        """getDatabaseFields(self, DCClass dclass)

        Returns the list of fields associated with the indicated
        DCClass that should be stored on the database.
        """
        fields = []
        for i in range(dclass.getNumInheritedFields()):
            dcf = dclass.getInheritedField(i)
            af = dcf.asAtomicField()
            if af:
                if af.isDb():
                    fields.append(af.getName())

        return fields
    
    def fillin(self, do, dclass):
        """fillin(self, DistributedObjectAI do, DCClass dclass)

        Fills in all the data from the DatabaseObject into the
        indicated distributed object by calling the appropriate set*()
        functions, where defined.

        """
        do.doId = self.doId
        for field, value in self.values.items():
            # Special-case kludge for broken fields.
            if field == "setZonesVisited" and value.getLength() == 1:
                self.notify.warning("Ignoring broken setZonesVisited")
            else:
                dclass.directUpdate(do, field, value)
            
    def reload(self, do, dclass, fields):
        """reload(self, DistributedObjectAI do, DCClass dclass)

        Re-reads all of the data from the DistributedObject and stores
        it in the values table.
        """
        self.doId = do.doId

        self.values = {}
        for fieldName in fields:
            field = dclass.getFieldByName(fieldName)
            if field == None:
                self.notify.warning("No definition for %s" % (fieldName))
            else:
                dg = PyDatagram()
                packOk = dclass.packRequiredField(dg, do, field)
                assert(packOk)
                self.values[fieldName] = dg
            
    def createObject(self, objectType):
        # If we just want the default values for the new object's fields,
        # there's no need to specify any field values here. (Upon generation,
        # fields that are not stored in the database are assigned their
        # default values).
        # In the future, when creating an object in the DB, we may want
        # to provide values that differ from the default; this dict is
        # the place to put those values.
        # Note that the values in this dict must be specially formatted in
        # a datagram; I haven't sussed that out. See self.reload() and
        # AIDistUpdate.insertArg().
        values = {}

        for key, value in values.items():
            values[key] = PyDatagram(str(value))

        # objectType is an integer that the DB uses to distinguish object
        # types, i.e. ToontownAIMsgTypes.DBSERVER_PET_OBJECT_TYPE
        assert type(objectType) is types.IntType

        # Get a unique context for this query and associate ourselves
        # in the map.
        context = self.air.dbObjContext
        self.air.dbObjContext += 1
        self.air.dbObjMap[context] = self

        self.createObjType = objectType

        dg = PyDatagram()
        dg.addServerHeader(DBSERVER_ID, self.air.ourChannel, DBSERVER_CREATE_STORED_OBJECT)
        
        dg.addUint32(context)
        dg.addString('')
        dg.addUint16(objectType)
        dg.addUint16(len(values))

        for field in values.keys():
            dg.addString(field)
        for value in values.values():
            dg.addString(value.getMessage())

        self.air.send(dg)

    def handleCreateObjectResponse(self, di):
        retCode = di.getUint8()
        if retCode != 0:
            self.notify.warning("Database object %s create failed" %
                                (self.createObjType))
        else:
            del self.createObjType
            # The object has just been created in the database. We do not
            # have an instance of it, but we know its doId.
            self.doId = di.getUint32()

        if self.doneEvent != None:
            messenger.send(self.doneEvent, [self, retCode])

    def deleteObject(self):
        self.notify.warning('deleting object %s' % self.doId)

        dg = PyDatagram()
        dg.addServerHeader(DBSERVER_ID, self.air.ourChannel, DBSERVER_DELETE_STORED_OBJECT)
        
        dg.addUint32(self.doId)
        dg.addUint32(0xdeadbeefL)

        # bye bye
        self.air.send(dg)
