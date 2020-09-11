"""TTSCToontaskMenu.py: contains the SCToontaskMenu class"""

from otp.speedchat.SCMenu import SCMenu
from TTSCToontaskTerminal   import TTSCToontaskTerminal
from otp.speedchat.SCStaticTextTerminal import SCStaticTextTerminal
from toontown.quest import Quests

class TTSCToontaskMenu(SCMenu):
    """ TTSCToontaskMenu represents a menu of SCToontaskTerminals. """
    def __init__(self):
        SCMenu.__init__(self)

        # listen for changes to localtoon's quests
        # whenever localtoon is generated, we're going to get
        # this msg twice, once for setQuests and once for
        # setQuestCarryLimit
        self.accept("questsChanged", self.__tasksChanged)
        self.__tasksChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __tasksChanged(self):
        # clear out everything from our menu
        self.clearMenu()

        # if local toon has not been created, don't panic
        try:
            lt = base.localAvatar
        except:
            return

        # keep a list of the phrases we've added to the menu, to
        # detect duplicates
        phrases = []
        def addTerminal(terminal, self=self, phrases=phrases):
            displayText = terminal.getDisplayText()
            if displayText not in phrases:
                self.append(terminal)
                phrases.append(displayText)

        # rebuild our menu
        for task in lt.quests:
            taskId, fromNpcId, toNpcId, rewardId, toonProgress = task
            q = Quests.getQuest(taskId)
            if q is None:
                continue
            msgs = q.getSCStrings(toNpcId, toonProgress)
            # getSCStrings might return a list of strings, or just a string
            if type(msgs) != type([]):
                msgs = [msgs]
            for i in xrange(len(msgs)):
                addTerminal(TTSCToontaskTerminal(msgs[i], taskId, toNpcId,
                                               toonProgress, i))

        # if toon has open task slots, or no task slots,
        # append 'i need a toontask'.
        needToontask = 1
        if hasattr(lt, 'questCarryLimit'):
            needToontask = (len(lt.quests) != lt.questCarryLimit)
        if needToontask:
            # add 'I need to get a ToonTask'
            # see Localizer.SpeedChatStaticText
            addTerminal(SCStaticTextTerminal(1299))
