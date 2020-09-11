#!/usr/bin/env python

import sys
import RepairAvatars

class CatalogAdjuster(RepairAvatars.AvatarIterator):
    def __init__(self, air, adjustmentMinutes):
        RepairAvatars.AvatarIterator.__init__(self, air)
        self.adjustmentMinutes = adjustmentMinutes

        self.numVisited = 0
        self.numChanged = 0
        
    def fieldsToGet(self, db):
        return ["setName", "setDNAString",
                "setCatalogSchedule", "setDeliverySchedule"]
    
    def processAvatar(self, av, db):
        self.numVisited += 1
        self.printSometimes(av)

        anyChanged = 0
        if av.catalogScheduleNextTime:
            av.catalogScheduleNextTime += self.adjustmentMinutes
            anyChanged = 1
            
        if av.onOrder:
            for item in av.onOrder:
                item.deliveryDate += self.adjustmentMinutes
            av.onOrder.markDirty()
            anyChanged = 1

        if anyChanged:
            db.storeObject(av, ["setCatalogSchedule", "setDeliverySchedule"])
            self.numChanged += 1

    def done(self):
        print "done, %s avatars visited, %s changed." % (self.numVisited, self.numChanged)
        sys.exit(0)

def usage():
    print ""
    print "DelayCatalog.py <days>"
    print ""
    print "This Python script is meant to be run on a live database to "
    print "adjust all of the catalog delivery dates into the future by "
    print "a certain number of days, to compensate for the catalog system "
    print "being offline for a length of time."
    print ""

def main(argv):
    if len(argv) != 2:
        usage()
        sys.exit(1)

    try:
        numDays = float(argv[1])
    except:
        usage()
        sys.exit(1)

    adjustmentMinutes = int(numDays * 24 * 60)

    print "Adjusting catalog deliveries by %s days, or %s minutes." % (
        numDays, adjustmentMinutes)

    import UtilityStart
    adj = CatalogAdjuster(simbase.air, adjustmentMinutes)
    adj.start()
    run()

main(sys.argv)
