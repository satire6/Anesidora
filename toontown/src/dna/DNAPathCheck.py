"""
This module reads in all the street DNA files and computes
a path from every point to every other point, looking for errors.
It prints out a list of every point that is not connected
in each file at the end
"""


from pandac.PandaModules import *
import time
import pprint
import os

dnaFiles = [
    "toontown_central_2100.dna",
    "toontown_central_2200.dna",
    "toontown_central_2300.dna",

    "donalds_dock_1100.dna",
    "donalds_dock_1200.dna",
    "donalds_dock_1300.dna",

    "minnies_melody_land_4100.dna",
    "minnies_melody_land_4200.dna",
    "minnies_melody_land_4300.dna",

    "daisys_garden_5100.dna",
    "daisys_garden_5200.dna",
    "daisys_garden_5300.dna",
    
    "donalds_dreamland_9100.dna",
    "donalds_dreamland_9200.dna",
   
    "the_burrrgh_3100.dna",
    "the_burrrgh_3200.dna",
    "the_burrrgh_3300.dna",

    "cog_hq_sellbot_sz.dna",
    
    # These paths are not connected!
    # "cog_hq_cashbot_sz.dna",

    "cog_hq_lawbot_sz.dna",
    ]

errors = []




dnaSearchPath = DSearchPath()
if os.getenv('TTMODELS'):
    dnaSearchPath.appendDirectory(Filename.expandFrom('$TTMODELS/built/phase_3.5/dna'))
    dnaSearchPath.appendDirectory(Filename.expandFrom('$TTMODELS/built/phase_4/dna'))
    dnaSearchPath.appendDirectory(Filename.expandFrom('$TTMODELS/built/phase_5/dna'))
    dnaSearchPath.appendDirectory(Filename.expandFrom('$TTMODELS/built/phase_5.5/dna'))
    dnaSearchPath.appendDirectory(Filename.expandFrom('$TTMODELS/built/phase_6/dna'))
    dnaSearchPath.appendDirectory(Filename.expandFrom('$TTMODELS/built/phase_8/dna'))
    dnaSearchPath.appendDirectory(Filename.expandFrom('$TTMODELS/built/phase_9/dna'))
    dnaSearchPath.appendDirectory(Filename.expandFrom('$TTMODELS/built/phase_10/dna'))

    # In the publish environment, TTMODELS won't be on the model
    # path by default, so we always add it there.  In the dev
    # environment, it'll be on the model path already, but it
    # doesn't hurt to add it again.
    getModelPath().appendDirectory(Filename.expandFrom("$TTMODELS"))
else:
    dnaSearchPath.appendDirectory(Filename('.'))
    dnaSearchPath.appendDirectory(Filename('ttmodels/src/dna'))


def lookupDNAFileName(filename):
    dnaFile = Filename(filename)
    found = dnaFile.resolveFilename(dnaSearchPath)
    return dnaFile.cStr()

for file in dnaFiles:
    print ("Checking file: %s" % (file))
    dnaStore = DNAStorage()
    file = lookupDNAFileName(file)
    dnaData = loadDNAFileAI(dnaStore, file, CSDefault)
    streetPointList = []
    frontdoorPointList = []
    sidedoorPointList = []
    for i in range(dnaStore.getNumSuitPoints()):
        point = dnaStore.getSuitPointAtIndex(i)
        if (point.getPointType() == DNASuitPoint.STREETPOINT):
            streetPointList.append(point)
        elif (point.getPointType() == DNASuitPoint.FRONTDOORPOINT):
            frontdoorPointList.append(point)
        elif (point.getPointType() == DNASuitPoint.SIDEDOORPOINT):
            sidedoorPointList.append(point)
    allPoints = streetPointList + frontdoorPointList + sidedoorPointList
    numPoints = len(allPoints)
    if numPoints == 0:
        print ("No points found in file: %s" % (file))
        continue
    count = 0
    startTime = time.time()
    for point1 in allPoints:
        count += 1
        print ("Checking point index: %s,  %s/%s" % (point1.getIndex(), count, numPoints))
        for point2 in allPoints:
            if point1 != point2:
                minPathLen = 40
                maxPathLen = 300
                path = dnaStore.getSuitPath(point1, point2, minPathLen, maxPathLen)
                if path is None:
                    errors.append([point1.getIndex(), point2.getIndex(), file])
    endTime = time.time()
    dt = endTime - startTime
    totalPaths = numPoints * numPoints
    print ("Computed %s paths in %s seconds. Avg %s sec/path" %
           (totalPaths, dt, dt/float(totalPaths)))

pprint.pprint(errors)
