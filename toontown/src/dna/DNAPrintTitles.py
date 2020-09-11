"""
This module reads in all the street DNA files and prints
out the building titles for each block ID
"""

import direct
from pandac.PandaModules import *
import time

dnaStorageFiles = [
    'phase_4/dna/storage.dna',
    'phase_5/dna/storage_town.dna',
    'phase_5.5/dna/storage_estate.dna',
    'phase_5.5/dna/storage_house_interior.dna',
    'phase_4/dna/storage_TT.dna',
    'phase_4/dna/storage_TT_sz.dna',
    'phase_5/dna/storage_TT_town.dna',
    'phase_6/dna/storage_DD.dna',
    'phase_6/dna/storage_DD_sz.dna',
    'phase_6/dna/storage_DD_town.dna',
    'phase_6/dna/storage_MM.dna',
    'phase_6/dna/storage_MM_sz.dna',
    'phase_6/dna/storage_MM_town.dna',
    'phase_8/dna/storage_BR.dna',
    'phase_8/dna/storage_BR_sz.dna',
    'phase_8/dna/storage_BR_town.dna',
    'phase_8/dna/storage_DG.dna',
    'phase_8/dna/storage_DG_sz.dna',
    'phase_8/dna/storage_DG_town.dna',
    'phase_8/dna/storage_DL.dna',
    'phase_8/dna/storage_DL_sz.dna',
    'phase_8/dna/storage_DL_town.dna',
    ]

dnaFiles = [
    "phase_4/dna/toontown_central_sz.dna",
    "phase_5/dna/toontown_central_2100.dna",
    "phase_5/dna/toontown_central_2200.dna",
    "phase_5/dna/toontown_central_2300.dna",
    "phase_6/dna/donalds_dock_sz.dna",
    "phase_6/dna/donalds_dock_1100.dna",
    "phase_6/dna/donalds_dock_1200.dna",
    "phase_6/dna/donalds_dock_1300.dna",
    "phase_6/dna/minnies_melody_land_sz.dna",
    "phase_6/dna/minnies_melody_land_4100.dna",
    "phase_6/dna/minnies_melody_land_4200.dna",
    "phase_6/dna/minnies_melody_land_4300.dna",
    "phase_8/dna/daisys_garden_sz.dna",
    "phase_8/dna/daisys_garden_5100.dna",
    "phase_8/dna/daisys_garden_5200.dna",
    "phase_8/dna/daisys_garden_5300.dna",
    "phase_8/dna/donalds_dreamland_sz.dna",
    "phase_8/dna/donalds_dreamland_9100.dna",
    "phase_8/dna/donalds_dreamland_9200.dna",
    "phase_8/dna/the_burrrgh_sz.dna",
    "phase_8/dna/the_burrrgh_3100.dna",
    "phase_8/dna/the_burrrgh_3200.dna",
    "phase_8/dna/the_burrrgh_3300.dna",
    ]

dnaStore = DNAStorage()

for file in dnaStorageFiles:
    loadDNAFile(dnaStore, file, CSDefault, 1)

print ("zone2TitleDict = {")
for file in dnaFiles:
    print ("    # titles for: %s" % (file))
    loadDNAFile(dnaStore, file, CSDefault, 0)
    for blockIndex in range(dnaStore.getNumBlockTitles()):
        blockNumber = dnaStore.getTitleBlockAt(blockIndex)
        title = dnaStore.getTitleFromBlockNumber(blockNumber)
        zone = dnaStore.getZoneFromBlockNumber(blockNumber)
        article = dnaStore.getArticleFromBlockNumber(blockNumber)        
        branchZone = zone-(zone%100)
        finalZone = branchZone + 500 + blockNumber
        print ('    %s : ("%s", "%s"),' % (finalZone, title, article))
    dnaStore.resetBlockTitle()
    dnaStore.resetBlockNumbers()
    dnaStore.resetBlockArticle()
