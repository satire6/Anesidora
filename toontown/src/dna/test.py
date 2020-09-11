



from pandac.PandaModules import *

# Create a DNA Store
dnaStore = DNAStorage()
# Fill up that DNA Store
loadDNAFile(dnaStore, "phase_4/dna/storage.dna", CSDefault, 1)
loadDNAFile(dnaStore, "phase_4/dna/storage_TT.dna", CSDefault, 1)
loadDNAFile(dnaStore, "phase_5/dna/storage_TT_town.dna", CSDefault, 1)

r = loadDNAFileAI(dnaStore, "phase_4/dna/tutorial_street.dna", CSDefault, 1)


# Make some test pieces
dnaFB = DNAFlatBuilding()
dnaWall = DNAWall()
dnaWall.setCode("wall_lg_brick_ur")
dnaFB.setWidth(10.0)
dnaWin = DNAWindows()
dnaWin.setCode("window_md_curtains_ur")
dnaWin.setWindowCount(1)
dnaFB.add(dnaWall)
dnaWall.add(dnaWin)

# Traverse
fb = dnaFB.traverse(render, dnaStore, 1)

# Test parenting
assert(dnaWin.getParent() == dnaWall)
assert(dnaWall.getParent() == dnaFB)
assert(dnaFB.getParent() == None)
# Test finding the node in the storage
assert(dnaStore.findDNAGroup(fb.node()) == dnaFB)
# Test removing the node from the storage
assert(dnaStore.removeDNAGroup(fb.node()) >= 1)
# Test failing to remove the node from the storage
assert(dnaStore.removeDNAGroup(fb.node()) == 0)

# Storage should be empty now
dnaStore.printNodeRelations()

# Traverse again
fb = dnaFB.traverse(render, dnaStore, 1)
# Test finding the node in the storage
assert(dnaStore.findDNAGroup(fb.node()) == dnaFB)
# Test removing the node from the storage by the group
assert(dnaStore.removeDNAGroup(dnaFB) >= 1)
# Test failing to remove the node from the storage by the group
assert(dnaStore.removeDNAGroup(dnaFB) == 0)
