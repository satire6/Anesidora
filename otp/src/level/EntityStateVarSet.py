from direct.fsm.StatePush import StateVar
from direct.showbase.PythonUtil import getSetterName
from otp.level.Entity import Entity

# given an entity type, acts as an entity that has a StateVar attribute for each attribute of the entity type
class EntityStateVarSet(Entity):
    def __init__(self, entType):
        self._entType = entType
        self._attribNames = []
        for attrib in self._entType.attribs:
            name, defaultVal, type = attrib
            self._addAttrib(name, defaultVal, type)

    def initializeEntity(self, level, entId):
        # Entity.initializeEntity hammers attributes directly into self.__dict__
        # set the StateVars aside and restore them afterward
        stateVars = {}
        for attribName in self._attribNames:
            stateVars[attribName] = getattr(self, attribName)
        Entity.initializeEntity(self, level, entId)
        # update the values
        for attribName in self._attribNames:
            stateVars[attribName].set(getattr(self, attribName))
        # restore the StateVars
        for attribName in self._attribNames:
            setattr(self, attribName, stateVars[attribName])

    def _getAttributeNames(self):
        return self._attribNames[:]

    def _setter(self, name, value):
        getattr(self, name).set(value)

    def _addAttrib(self, name, defaultVal, type):
        setattr(self, name, StateVar(defaultVal))
        setattr(self, getSetterName(name), Functor(self._setter, name))
        self._attribNames.append(name)
