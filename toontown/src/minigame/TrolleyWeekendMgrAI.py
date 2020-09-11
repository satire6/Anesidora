from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.ai import HolidayBaseAI

class TrolleyWeekendMgrAI(HolidayBaseAI.HolidayBaseAI):

    notify = DirectNotifyGlobal.directNotify.newCategory(
        'TrolleyWeekendMgrAI')

    PostName = 'TrolleyWeekend'
    StartStopMsg = 'TrolleyWeekendStartStop'

    def __init__(self, air, holidayId):
        HolidayBaseAI.HolidayBaseAI.__init__(self, air, holidayId)

    def start(self):
        # let the holiday system know we started
        bboard.post(TrolleyWeekendMgrAI.PostName, True)

        # tell everyone race night is starting
        simbase.air.newsManager.trolleyWeekendStart()

        messenger.send(TrolleyWeekendMgrAI.StartStopMsg)

    def stop(self):
        # let the holiday system know we stopped
        bboard.remove(TrolleyWeekendMgrAI.PostName)

        # tell everyone race night is stopping
        simbase.air.newsManager.trolleyWeekendEnd()

        messenger.send(TrolleyWeekendMgrAI.StartStopMsg)
