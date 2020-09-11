## """
## """

## from direct.distributed.ClockDelta import *

## from direct.directnotify import DirectNotifyGlobal
## from direct.distributed import DistributedObject

## class DistributedGuildMember(DistributedObject.DistributedObject):
    ## """
    ## The Guild is a global object.
    
    ## See Also:
        ## "otp/src/guild/DistributedGuildMemberAI.py"
        ## "otp/src/configfiles/otp.dc"
    ## """
    ## if __debug__:
        ## notify = DirectNotifyGlobal.directNotify.newCategory(
                ## 'guild')

    ## def __init__(self, cr):
        ## assert self.notify.debugCall()
        ## DistributedObject.DistributedObject.__init__(self, cr)
        ## self.permissions=0

    ## def announceGenerate(self):
        ## assert self.notify.debugCall()
        ## #todo: add self as a child of the guild this is a member of.
        ## DistributedObject.DistributedObject.announceGenerate(self)

    ## def delete(self):
        ## assert self.notify.debugCall()
        ## self.ignoreAll()
        ## DistributedObject.DistributedObject.delete(self)

    ## def setSince(self, dateJoined):
        ## assert self.notify.debugCall()
        ## self.dateJoined=dateJoined

    ## def setName(self, name):
        ## assert self.notify.debugCall()
        ## self.name=name
    
    ## def setReputations(self, reputations):
        ## assert self.notify.debugCall()
        ## self.reputations=reputations
    
    ## def hasPermissionTo(self, permission):
        ## assert self.notify.debugCall()
        ## #return self.permissions & permission
        ## return True
        
    
    ## if 0:
        ## def setRank(self, guildRank):
            ## self.guildRank=guildRank
            ## if guildRank>=250:
                ## self.permissions=GUILD_PERM_OWNER
            ## elif guildRank>=200:
                ## self.permissions=GUILD_PERM_CO_OWNER
            ## elif guildRank>=100:
                ## self.permissions=GUILD_PERM_CAPTAIN
            ## elif guildRank>=1:
                ## self.permissions=GUILD_PERM_MEMBER
            ## else:
                ## self.permissions=GUILD_PERM_APPLICANT

        ## def setAuthority(self, authority):
            ## """
            ## authority determines what the avatar is allowed
                ## to do within the guild.
                ## The authority bits are:
                ## 1 = grant authority
                ## 2 = member, news, polling, guild buildings, guild npcs
                ## 3 = borrow ships
                ## 4 = 
            ## """
            ## self.authority=authority

        ## def setTake(self, take):
            ## """
            ## take is the number of shares the pirate will
                ## get of the total treasure available.
            ## """
            ## self.take=take
    
    
    
    ## """
    ## notes:
    
    ## hrPerm
        ## invitePerm -- nope
        ## addMemberPerm = 8
        ## removeMemberPerm = 8
        ## promotePerm = 8
        ## demotePerm = 8
    ## rulerPerm
        ## deplomacyPerm -- not in first version
        ## createOfficePerm -- not in first version
    ## propogandaPerm -- founder (all together)
        ## newsAddPerm = 8
        ## newsEditPerm = 8
        ## newsRemovePerm = 8
        ## pollAddPerm = 8
        ## pollRemovePerm = 8
    ## treasurerPerm -- founder (all together)
        ## taxPerm = 8
        ## bankPerm = 8
        ## salaryPerm = 8
    ## auctionierPerm -- tbd (buy and sell together) anybody
        ## auctionSellPerm = 1
        ## auctionBuyPerm = 1
        ## auctionRemovePerm -- not in first version
    ## governorPerm -- founder (all together)
        ## placeBuildingPerm = 16
        ## removeBuildingPerm = 16
        ## npcHirePerm = 16
        ## npcFirePerm = 16
    ## admiralPerm
        ## shipSellPerm = 32 -- founder
        ## shipBuyPerm = 32 -- founder
        ## shipScuttlePerm -- nope
        ## shipUsePerm = 4 -- captain
    ## leaderPerm
        ## captainShipPerm (redundant with shipUsePerm) -- captain
        ## leadCrewPerm = 2 -- any member
    ## inventoryPerm
        ## inventoryBrowsePerm = 1 -- any
        ## inventoryAddPerm = 1 -- any
        ## inventoryBorrowPerm -- any with limits by title
        ## inventoryRemovePerm = 64 -- founder
        ## inventoryAuctionPerm -- nope
    ## memberPerm
        ## votePerm = 1 -- any
    ## """

