## """
## The Guild handles all the guilds accross all shards.
## """

## from direct.distributed.ClockDelta import *

## from direct.directnotify import DirectNotifyGlobal
## from direct.distributed import DistributedObject

## class DistributedGuild(DistributedObject.DistributedObject):
    ## """
    ## The Guild is a global object.

    ## See Also:
        ## "otp/src/configfiles/otp.dc"
        ## "otp/src/guild/DistributedGuildAI.py"
    ## """
    ## if __debug__:
        ## notify = DirectNotifyGlobal.directNotify.newCategory('guild')

    ## def __init__(self, cr):
        ## assert self.notify.debugCall()
        ## DistributedObject.DistributedObject.__init__(self, cr)

    ## def delete(self):
        ## assert self.notify.debugCall()
        ## self.ignoreAll()
        ## DistributedObject.DistributedObject.delete(self)


    ## def setName(self, name):
        ## self.name=name

    ## def setDateCreated(self, dateCreated):
        ## self.dateCreated=dateCreated

    ## def setOwnerAvatarId(self, ownerAvatarId):
        ## self.ownerAvatarId=ownerAvatarId

    ## def setFlagDna(self, flagDna):
        ## self.flagDna=flagDna

    ## def setApplicationHandling(self, handler):
        ## """
        ## handler is one of "ask", "accept", "reject"
        ## """
        ## self.applicationHandler=handler

    ## def setGuildStatus(self, guildStatus):
        ## self.guildStatus=guildStatus

    ## def setGuildTaxLevel(self, guildStatus):
        ## self.guildStatus=guildStatus


## if 0:
 ## class DistributedGuildOffices(DistributedObject.DistributedObject):
    ## def __init__(self, cr):
        ## pass

    ## """
    ## hrPerm
        ## invitePerm
        ## addMemberPerm
        ## removeMemberPerm
        ## promotePerm
        ## demotePerm
    ## rulerPerm
        ## deplomacyPerm -- not in first version
        ## createOfficePerm -- not in first version
    ## propogandaPerm -- founder (all together)
        ## newsAddPerm
        ## newsEditPerm
        ## newsRemovePerm
        ## pollAddPerm
        ## pollRemovePerm
    ## treasurerPerm -- founder (all together)
        ## taxPerm
        ## bankPerm
        ## salaryPerm
    ## auctionierPerm -- tbd (buy and sell together) anybody
        ## auctionSellPerm
        ## auctionBuyPerm
        ## auctionRemovePerm -- not in first version
    ## governorPerm -- founder (all together)
        ## placeBuildingPerm
        ## removeBuildingPerm
        ## npcHirePerm
        ## npcFirePerm
    ## admiralPerm
        ## shipSellPerm -- founder
        ## shipBuyPerm -- founder
        ## shipScuttlePerm -- nope
        ## shipUsePerm -- captain
    ## leaderPerm
        ## captainShipPerm (redundant with shipUsePerm) -- captain
        ## leadCrewPerm -- any member
    ## inventoryPerm
        ## inventoryBrowsePerm -- any
        ## inventoryAddPerm -- any
        ## inventoryBorrowPerm -- any with limits by title
        ## inventoryRemovePerm -- founder
        ## inventoryAuctionPerm -- nope
    ## memberPerm
        ## votePerm -- any
    ## """

    ## """
                ## Data Attributes:
                        ## guildName (RO string)
                        ## dateCreated (RO date)
                        ## owner (reference)
                        ## guildFlag (DNA)
                        ## autoApplicationHandling (off, accept, or reject)
                        ## guildTaxLevel
                        ## pollTax

                        ## current (list)
                            ## currentQuests (list)
                            ## currentNews (list)
                            ## currentPoll
                        ## #chatLog (RO list)
                        ## reputations (list)
                            ## reputations: Totals
                            ## reputations: Highest
                        ## offices (list)
                            ## office: <unnamed> (Membership/application Management) (gets hrPerm)
                            ## office: foriegn affairs
                            ## office: (News Mgmt)
                            ## office: Tax Collector (Tax Mgmt)
                            ## office: Treasurer (Inventory Mgmt)
                            ## office: (Salary Mgmt)
                            ## office: Auctionier (Auction Mgmt)
                            ## office: Governor (Island/building Mgmt)
                            ## office: (NPC Mgmt)
                            ## office: (Officer/promotion Mgmt)
                            ## office: (Poll Mgmt)
                            ## office: Admiral (Ship Mgmt)

                        ## members (list)
                        ## applicants (list)
                        ## invitations (list)

                        ## Quest History (RO list)
                        ## News History (RO list)
                        ## Tax History (RO list)
                        ## Poll History (RO list)

                        ## Inventory (list)
                                ## bank? (or is this part of gear?)
                                ## islands (hide out)
                                ## gear
                                ## burried treasure?
                                ## treasure maps? (or are these quests?)
                            ## inventory: ships (list)
                            ## inventory: buildings (list)
                            ## inventory: locations that are buildable? (list)
                            ## inventory: NPCs (do NPCs pay taxes?)
                            ## inventory: auctions (to members (and non-members?))

                        ## leaderboard (between guilds and inside guild, who contributed money or completed quests).
                        ## community tools
                                ## meetings ? (events?) calender
                                ## message board
    ## """
