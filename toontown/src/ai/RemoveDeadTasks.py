import RepairAvatars
import DatabaseObject
import time

# this removes all traces of a list of tasks from all avatars; if they are
# working on the task, it will disappear
class DeadTaskRemover(RepairAvatars.AvatarIterator):
    # When we come to this many non-avatars in a row, assume we have
    # reached the end of the database.
    endOfListCount = 2000

    def __init__(self, air, deadTaskIds):
        # pass in list of questIds of tasks to remove
        self.deadTaskIds = deadTaskIds
        RepairAvatars.AvatarIterator.__init__(self, air)

    def fieldsToGet(self, db):
        return ['setName', 'setMoney',
                'setQuests', 'setQuestHistory', 'setRewardHistory']

    def processAvatar(self, av, db):
        self.printSometimes(av)

        # grab a copy of the av's quests
        flatQuests = av.getQuests()

        # unflatten the quests
        questList = []
        questLen = 5
        for i in range(0, len(flatQuests), questLen):
            questList.append(flatQuests[i:i+questLen])

        # make list of quests to remove
        toRemove = []
        for quest in questList:
            id = quest[0]
            if id in self.deadTaskIds:
                reward = quest[3]
                toRemove.append([id, reward])

        # remove the quests
        questsChanged = (len(toRemove) > 0)
        questHistoryChanged = 0
        rewardHistoryChanged = 0
        for questId, rewardId in toRemove:
            av.removeQuest(questId)
            if av.removeQuestFromHistory(questId):
                questHistoryChanged = 1
            if av.removeRewardFromHistory(rewardId):
                rewardHistoryChanged = 1

        # and store the changes in the DB
        if questsChanged:
            print "Fixing %s: %s" % (av.doId, av.name)
            fields = ['setQuests']
            if questHistoryChanged:
                fields.append('setQuestHistory')
            if rewardHistoryChanged:
                fields.append('setRewardHistory')
            db2 = DatabaseObject.DatabaseObject(self.air, av.doId)
            db2.storeObject(av, fields)
    
    def printSometimes(self, av):
        now = time.time()
        if now - self.lastPrintTime > self.printInterval:
            print "Avatar %d: %s" % (av.doId, av.name)
            self.lastPrintTime = now

import UtilityStart
f = DeadTaskRemover(simbase.air, (range(6979, 6999+1) +
                                  range(7979, 7999+1) +
                                  range(8979, 8999+1) +
                                  range(9979, 9999+1) +
                                  range(10979, 10999+1)))
f.start()
run()

