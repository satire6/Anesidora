from otp.level.LevelSpec import LevelSpec
from toontown.cogdominium import CogdoCraneGameSpec
from toontown.cogdominium import CogdoCraneGameConsts as Consts
from direct.fsm.StatePush import FunctionCall

class CogdoCraneGameBase:
    def startHandleEdits(self):
        if __dev__:
            fcs = []
            # each attribute in the game settings entity can have a handler, e.g.
            # def _handleGameDurationChanged(self, gameDuration): ...
            for attribName in Consts.Settings._getAttributeNames():
                handler = getattr(self, '_handle%sChanged' % attribName, None)
                if handler:
                    stateVar = getattr(Consts.Settings, attribName)
                    fcs.append(FunctionCall(handler, stateVar))
            self._functionCalls = fcs

    def stopHandleEdits(self):
        if __dev__:
            for fc in self._functionCalls:
                fc.destroy()
            self._functionCalls = None

    def getLevelSpec(self):
        return LevelSpec(CogdoCraneGameSpec)

    if __dev__:
        def getEntityTypeReg(self):
            # return an EntityTypeRegistry with information about the
            # entity types that the crane game uses
            import CogdoEntityTypes
            from otp.level import EntityTypeRegistry
            typeReg = EntityTypeRegistry.EntityTypeRegistry(CogdoEntityTypes)
            return typeReg
