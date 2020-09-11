from otp.ai.AIBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.suit import SuitDNA
from CogPageGlobals import *

class CogPageManagerAI:

    notify = DirectNotifyGlobal.directNotify.newCategory("CogPageManagerAI")

    def __init__(self, air):
        self.air = air

    def toonEncounteredCogs(self, av, cogList, zoneId):
        # This lets the battle system notify us when we have encountered cogs.
        # If we have not encountered them before, update the avatar
        avId = av.getDoId()
        avCogs = av.cogs[:]
        changed = 0
        self.notify.debug("toonEncounteredCogs: avId: %s, avCogs: %s, cogList: %s, zoneId: %s"
                          % (avId, avCogs, cogList, zoneId))
        for encounter in cogList:
            cog = encounter['type']
            activeToons = encounter['activeToons']
            index = SuitDNA.suitHeadTypes.index(cog)
            if (avCogs[index] == COG_UNSEEN) and (avId in activeToons):
                avCogs[index] = COG_BATTLED
                changed = 1

        # update cog status only if we've seen someone new
        if changed:
            av.b_setCogStatus(avCogs)
                
        
    def toonKilledCogs(self, av, cogList, zoneId):
        # This lets the battle system notify us when we have killed cogs.
        avId = av.getDoId()
        avCogs = av.cogs[:]
        cogs_changed = 0
        avCogCounts = av.cogCounts[:]
        counts_changed = 0
        avCogRadar = av.cogRadar[:]
        cog_radar_changed = 0
        avBuildingRadar = av.buildingRadar[:]
        building_radar_changed = 0
        self.notify.debug("toonKilledCogs: avId: %s, cogCounts: %s, cogList: %s, zoneId: %s"
                          % (avId, avCogCounts, cogList, zoneId))

        eventMsg = {}
        for encounter in cogList:
            if encounter['isVP'] or encounter['isCFO']:
                continue
            cog = encounter['type']
            level = encounter['level']
            track = encounter['track']
            activeToons = encounter['activeToons']
            index = SuitDNA.suitHeadTypes.index(cog)
            quotaIndex = index % SuitDNA.suitsPerDept
            # if we were active when the cog was defeated, update the count
            if (avId in activeToons):
                msgName = '%s%s' % (cog, level)
                if encounter['isSkelecog']:
                    msgName += "+"
                if eventMsg.has_key(msgName):
                    eventMsg[msgName] += 1
                else:
                    eventMsg[msgName] = 1

                # update but don't exceed the quota
                if (avCogCounts[index] < COG_QUOTAS[1][quotaIndex]):
                    avCogCounts[index] += 1
                    counts_changed = 1
                # if we have met the first quota, set to complete1
                if (avCogCounts[index] == COG_QUOTAS[0][quotaIndex]):
                    avCogs[index] = COG_COMPLETE1
                    cogs_changed = 1
                # if we have met the second quota, set to complete2
                elif (avCogCounts[index] == COG_QUOTAS[1][quotaIndex]):
                    avCogs[index] = COG_COMPLETE2
                    cogs_changed = 1
                # otherwise if not already defeated, set to defeated
                elif ((avCogs[index] == COG_BATTLED) or
                      (avCogs[index] == COG_UNSEEN)):
                    avCogs[index] = COG_DEFEATED
                    cogs_changed = 1

        # Now format the message for the AI.
        msgText = ''
        for msgName, count in eventMsg.items():
            if msgText != '':
                msgText += ','
            msgText += '%s%s' % (count, msgName)
        
        self.air.writeServerEvent(
            'cogsDefeated', avId, "%s|%s" % (msgText, zoneId))
                
        # update cog status only if we've had a change of state
        if cogs_changed:
            av.b_setCogStatus(avCogs)

            # check the quotas for each dept and see if cog radar has been achieved
            deptSize = SuitDNA.suitsPerDept
            for dept in range(0, len(SuitDNA.suitDepts)):
                # only check if it hasn't been achieved yet!
                if avCogRadar[dept] == 0:
                    if min(avCogs[deptSize*dept:deptSize*(dept+1)]) == COG_COMPLETE1:
                        avCogRadar[dept] = 1
                        cog_radar_changed = 1

            if cog_radar_changed:
                av.b_setCogRadar(avCogRadar)

            # check the quotas for each dept and see if bldg radar has been achieved
            for dept in range(0, len(SuitDNA.suitDepts)):
                # only check if it hasn't been achieved yet!                
                if avBuildingRadar[dept] == 0:
                    if min(avCogs[deptSize*dept:deptSize*(dept+1)]) == COG_COMPLETE2:
                        avBuildingRadar[dept] = 1
                        building_radar_changed = 1

            if building_radar_changed:
                av.b_setBuildingRadar(avBuildingRadar)

        # update cog counts only if we've seen someone new
        if counts_changed:
            av.b_setCogCount(avCogCounts)

