from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

REPORT_PLAYER = "REPORT_PLAYER"

# Report categories
# Moderation
ReportFoulLanguage = "MODERATION_FOUL_LANGUAGE"
ReportPersonalInfo = "MODERATION_PERSONAL_INFO"
ReportRudeBehavior = "MODERATION_RUDE_BEHAVIOR"
ReportBadName = "MODERATION_BAD_NAME"

class CentralLogger(DistributedObjectGlobal):

    # Keep track of all the players reported.
    # We only allow 1 report per target per session.
    PlayersReportedThisSession = {}

    def hasReportedPlayer(self, targetDISLId, targetAvId):
        # Has this playerId, avatarId already been reported this session?
        return self.PlayersReportedThisSession.has_key((targetDISLId, targetAvId))

    def reportPlayer(self, category, targetDISLId, targetAvId, description = "None"):
        # You can only report another player once per session.
        if self.hasReportedPlayer(targetDISLId, targetAvId):
            # Already reported, dont resend the report.
            return False

        # Remember that we reported this user already.
        self.PlayersReportedThisSession[(targetDISLId, targetAvId)] = 1
        # Send the update. This shows up in the server event log.
        self.sendUpdate("sendMessage", [category, REPORT_PLAYER, targetDISLId, targetAvId])
        return True

    def writeClientEvent(self, eventString):
        # This one does not relate to moderation, but to client side
        # reporting in general. The idea is to use the existing infrastructure
        # to get message to the event log.
        self.sendUpdate("sendMessage", ['ClientEvent', eventString, 0, 0])
