from direct.directnotify import DirectNotifyGlobal
from otp.ai import AIDistrict

class UtilityAIRepository(AIDistrict.AIDistrict):
    """
    This class serves as the AI repository for a maintenance utility
    (e.g. RepairAvatars) that wants to get an AI-level connection to
    the message director without actually creating an AI district.
    """    
    notify = DirectNotifyGlobal.directNotify.newCategory(
            "UtilityAIRepository")


    def __init__(self, *args, **kw):
        AIDistrict.AIDistrict.__init__(self, *args, **kw)

        # The UtilityAIRepository sets this to 0 to indicate we should
        # not do things like issue new catalogs to toons that we load
        # in.  However, in the normal AI repository, we should do
        # these things.
        self.doLiveUpdates = 0

    def requestNewDistrict(self):
        pass

    def createDistrict(self, districtId, districtName):
        self.fsm.request('playGame')

    def deleteDistrict(self, districtId):
        pass
