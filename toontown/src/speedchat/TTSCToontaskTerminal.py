"""TTSCToontaskTerminal.py: contains the SCToontaskTerminal class"""

from otp.speedchat.SCTerminal import *
from toontown.quest import Quests
from toontown.toon import NPCToons

# args: taskId, toNpcId, toonProgress, msgIndex
TTSCToontaskMsgEvent = 'SCToontaskMsg'

def decodeTTSCToontaskMsg(taskId, toNpcId, toonProgress, msgIndex):
    q = Quests.getQuest(taskId)
    if q is None:
        return None
    # validate toNpcId
    name = NPCToons.getNPCName(toNpcId)
    if name is None:
        return None
    msgs = q.getSCStrings(toNpcId, toonProgress)
    if type(msgs) != type([]):
        msgs = [msgs]
    if msgIndex >= len(msgs):
        return None
    return msgs[msgIndex]

class TTSCToontaskTerminal(SCTerminal):
    """ TTSCToontaskTerminal represents a terminal SpeedChat node that
    contains a ToonTask-generated phrase. """
    def __init__(self, msg, taskId, toNpcId, toonProgress, msgIndex):
        SCTerminal.__init__(self)
        self.msg = msg
        self.taskId = taskId
        self.toNpcId = toNpcId
        self.toonProgress = toonProgress
        self.msgIndex = msgIndex

    def getDisplayText(self):
        return self.msg

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(TTSCToontaskMsgEvent),
                       [self.taskId, self.toNpcId,
                        self.toonProgress, self.msgIndex])
