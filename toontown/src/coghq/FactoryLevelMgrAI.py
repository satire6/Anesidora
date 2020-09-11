"""FactoryLevelMgrAI module: contains the FactoryLevelMgrAI class"""

from otp.level import LevelMgrAI

class FactoryLevelMgrAI(LevelMgrAI.LevelMgrAI):
    """This class manages editable factory attributes"""
    def __init__(self, level, entId):
        LevelMgrAI.LevelMgrAI.__init__(self, level, entId)
        self.callSettersAndDelete('cogLevel',)

    def setCogLevel(self, cogLevel):
        self.level.cogLevel = cogLevel
