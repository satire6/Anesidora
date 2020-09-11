from direct.directnotify import DirectNotifyGlobal
from toontown.uberdog.DataStore import *

class TrickOrTreatScavengerHuntDataStore(DataStore):
    """
    This is a specialized DataStore class designed to handle
    the TrickOrTreat holiday event.  It responds to two query
    types: one to get a toon's current progress in the
    scavenger hunt, and one to update it's progress with a
    newly completed goal.
    """

    # Define the available query strings
    # We'll only need two types of queries.
    # If for some strange reason this class is subclassed,
    # in the subclass use the following line:
    # QueryTypes = TrickOrTreatScavengerHuntDataStore.addQueryTypes(['Type_1',...])
    QueryTypes = DataStore.addQueryTypes(['GetGoals', 'AddGoal'])
    
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'TrickOrTreatScavengerHuntDataStore')
    
    def __init__(self, filepath):
        """
        filepath is where this store's data will be held on the disk.
        This path should be unique to this data store.
        """
        DataStore.__init__(self,filepath)

    def handleQuery(self,query):
        """
        This function parses the query and performs the
        necessary operations on the data store.  If a
        response is necessary, it is created here.

        Queries are of the format:
        (queryId, (avId, goal))

        queryId is QueryTypes['GetGoals'] or
                   QueryTypes['AddGoal']
        avId is the toon's id.
        goal is the goal they're attempting to complete.

        A queryId of 'GetGoals' will return a list of the toon's
        completed goals:
        (queryId, (avId, goal, (goal1,goal2,...)))

        A queryId of 'AddGoals' will return a confirmation message:
        (qId, (avId,))
        """

        # extract the queryId
        qId, qData = query

        # they're requesting a list of the toon's goals
        if qId == self.QueryTypes['GetGoals']:
            avId,goal = qData
            goals = self.__getGoalsForAvatarId(avId)
            # build the return message
            return (qId,(avId,goal,goals))
        # they're trying to add a goal to the toon's list
        elif qId == self.QueryTypes['AddGoal']:
            avId,goal = qData
            self.__addGoalToAvatarId(avId,goal)
            # confirm the update
            return (qId,(avId,))

        # if not a valid queryId, return an empty result
        return None

    
    def __addGoalToAvatarId(self, avId, goal):
        """
        Add the goal to avId's list of completed goals.
        If the goal is already present, this function
        has no effect.
        """

        if self.wantAnyDbm:
            pAvId = cPickle.dumps(avId)
            pGoal = cPickle.dumps(goal)
            
            pData = self.data.get(pAvId,None)
            if pData is not None:
                data = cPickle.loads(pData)
            else:
                data = set()

            data.add(goal)

            pData = cPickle.dumps(data)
            self.data[pAvId] = pData
        else:
            self.data.setdefault(avId,set())
            self.data[avId].add(goal)
        self.incrementWriteCount()


    def __getGoalsForAvatarId(self, avId):
        """
        Return a [] of goals for avid.
        """
        if self.wantAnyDbm:
            pAvId = cPickle.dumps(avId)
            pData = self.data.get(pAvId,None)
            if pData is not None:
                data = list(cPickle.loads(pData))
            else:
                data = []
            return data
        else:
            return list(self.data.get(avId,[]))


