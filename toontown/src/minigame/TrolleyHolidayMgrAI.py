from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.ai import HolidayBaseAI

class TrolleyHolidayMgrAI(HolidayBaseAI.HolidayBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'TrolleyHolidayMgrAI')

    PostName = 'TrolleyHoliday'
    StartStopMsg = 'TrolleyHolidayStartStop'

    def __init__(self, air, holidayId):
        HolidayBaseAI.HolidayBaseAI.__init__(self, air, holidayId)

    def start(self):
        # let the holiday system know we started
        bboard.post(TrolleyHolidayMgrAI.PostName, True)

        # tell everyone race night is starting
        simbase.air.newsManager.trolleyHolidayStart()

        messenger.send(TrolleyHolidayMgrAI.StartStopMsg)

    def stop(self):
        # let the holiday system know we stopped
        bboard.remove(TrolleyHolidayMgrAI.PostName)

        # tell everyone race night is stopping
        simbase.air.newsManager.trolleyHolidayEnd()

        messenger.send(TrolleyHolidayMgrAI.StartStopMsg)
