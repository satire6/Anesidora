from direct.fsm.StatePush import StateVar

class Setting:
    # simple setting value representation
    # see SettingsMgrAI
    def __init__(self, name, value):
        self._name = name
        self.setValue(value)
        
    def getName(self):
        return self._name

    def setValue(self, value):
        self._value = value
        
    def getValue(self):
        return self._value

class StateVarSetting(Setting, StateVar):
    # setting as a StateVar that will push value changes to listeners
    def __init__(self, name, value):
        StateVar.__init__(self, value)
        Setting.__init__(self, name, value)

    def setValue(self, value):
        StateVar.set(self, value)
    
    def getValue(self):
        return StateVar.get(self)
