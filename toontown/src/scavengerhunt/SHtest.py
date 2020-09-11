######################################################################
# This file is meant for unit testing the ScavengerHunt system.      #
# It can also be used to demonstrate how the system should be        #
# used.                                                              #
#                                                                    #
# It's meant to be run after any changes are made to the system.     #
#                                                                    #
# Usage: python SHtest.py                                            #
######################################################################

from ScavengerHuntBase import ScavengerHuntBase
import unittest,copy

hunt = ScavengerHuntBase(scavengerHuntId = 12,scavengerHuntType = 3)
hunt.defineGoals(range(1,6))
hunt.defineMilestones([[0,range(1,4)],[1,range(1,6)]])

class MilestoneTestCase(unittest.TestCase):
    def testDefineGoals(self):
        gc = set(range(1,6))
        self.assertEqual(hunt.goals,gc)

    def testDefineMilestones(self):
        m = {}

        gc = range(1,4)
        m[frozenset(gc)] = 0

        gc = range(1,6)
        m[frozenset(gc)] = 1

        self.assertEqual(hunt.milestones,m)

    def testRecentMilestonesHit(self):
        gc = range(1,4)
        m = hunt.getRecentMilestonesHit(gc,2)
        self.assertEqual([0],m)

        gc = range(1,6)
        m = hunt.getRecentMilestonesHit(gc,2)
        m.sort()
        self.assertEqual([0,1],m)

    def testRecentMilestonesMissed(self):
        gc = range(1,5)
            
        m = hunt.getRecentMilestonesHit(gc,4)
        self.assertEqual([],m)
    
    def testAllMilestonesHit(self):
        gc = range(1,6)

        m = hunt.getAllMilestonesHit(gc)
        m.sort()
        M = hunt.milestones.values()
        M.sort()
        self.assertEqual(M,m)

if __name__ == "__main__":    
    unittest.main()
