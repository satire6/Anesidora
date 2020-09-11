# This file will hold the object that handles setting up long-term
# (multiple day) do-later tasks for announcing a new catalog to a
# player and/or scheduling deliveries of recently-ordered catalog
# items.  It also handles the actual purchase of items from the
# catalog.

from direct.distributed import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
import CatalogGenerator
import CatalogItem
from toontown.toonbase import ToontownGlobals
import time
import math
from toontown.ai.RepairAvatars import AvatarGetter
from direct.showbase.PythonUtil import Functor
from toontown.catalog import CatalogItemList
from toontown.catalog import CatalogItem


CatalogInterval = 7 * 24 * 60  # 1 week (in minutes)

class CatalogManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("CatalogManagerAI")

    timeScale = simbase.config.GetFloat('catalog-time-scale', 1.0)
    catalogInterval = CatalogInterval / timeScale

    # If this is true, the catalog manager will deliver catalogs based
    # on real time elapsed, even if the user has not played for more
    # than one week.  If false, each next catalog delivered will be no
    # more than one more than the previous catalog delivered, no
    # matter how much time has elapsed in the interim.
    skipWeeks = simbase.config.GetBool('catalog-skip-weeks', 0)

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.generator = CatalogGenerator.CatalogGenerator()
        self.uniqueIdToReturnCode = {} #cache for return phone calls

        self.notify.info("Catalog time scale %s." % (self.timeScale))
        
        #DATA holders for gifting an item. So item can be handled on response
        
        
    def generate(self):
        DistributedObjectAI.DistributedObjectAI.generate(self)

    def delete(self):
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def forceCatalog(self, avatar, week, afterMinutes = 0):
        # Forces the catalog to the indicated week for the given
        # avatar by fiddling with the avatar's start date.  Mainly
        # used for testing and magic words.
        weekDelta = week - avatar.catalogScheduleCurrentWeek - 1
        now = (int)(time.time() / 60 + 0.5)
        avatar.catalogScheduleNextTime = now - (weekDelta  * self.catalogInterval) + afterMinutes

        # Temporarily force skipWeeks to true by setting a local
        # instance variable.
        self.skipWeeks = 1
        
        self.deliverCatalogFor(avatar)

        # Delete the instance variable to re-expose the class variable.
        del self.skipWeeks

    def forceMonthlyCatalog(self, avatar, month, day):
        # Forces the avatar's monthly catalog to be delivered as if it
        # were the indicated month and day.  Used for testing and
        # magic words.
        nowtuple = time.localtime(time.time())
        thentuple = list(nowtuple)
        thentuple[1] = month
        thentuple[2] = day
        then = time.mktime(thentuple)

        monthlyCatalog = self.generator.generateMonthlyCatalog(avatar, then / 60)
        avatar.b_setCatalog(monthlyCatalog, avatar.weeklyCatalog, avatar.backCatalog)


    def deliverCatalogFor(self, avatar):
        # Computes the next catalog time for and delivers the catalog
        # to the indicated avatar.

        # Get the current time in minutes.
        now = (int)(time.time() / 60 + 0.5)

        if avatar.catalogScheduleNextTime == 0:
            # This avatar has never received a catalog before; this
            # becomes the first one.
            currentWeek = 1

            weekStart = now
            nextTime = weekStart + self.catalogInterval

        else:
            # This avatar has received a catalog before, so determine
            # which week it is for him.

            # We start the week at the avatar's next scheduled
            # delivery time; this represents the start of the next
            # following week.  Usually (if the player logs in often
            # enough) this will be the correct value to keep.
            weekStart = avatar.catalogScheduleNextTime
            currentWeek = avatar.catalogScheduleCurrentWeek + 1

            # However, perhaps the player hasn't logged in for some
            # time, in which case we also need to skip the intervening
            # weeks.

            # On second thought, that seems to be vexing to users.
            # Maybe the right thing to do is not to skip any
            # intervening weeks.
            interval = now - weekStart
            weekDelta = int(math.floor(float(interval) / float(self.catalogInterval)))
            if self.skipWeeks:
                currentWeek += weekDelta
            weekStart += weekDelta * self.catalogInterval

            nextTime = weekStart + self.catalogInterval

            assert(weekStart <= now)

            # We might come up with nextTime within one minute of now due
            # to small roundoff error in the above.  If so, just jump to
            # the next week.

            if nextTime <= now + 1:
                if self.skipWeeks:
                    currentWeek += 1
                weekStart += self.catalogInterval
                nextTime += self.catalogInterval

        assert(nextTime > now)

        newMonthlyCatalog = (currentWeek != avatar.catalogScheduleCurrentWeek)

        previousWeek = avatar.catalogScheduleCurrentWeek
        
        newWeeklyCatalog = (currentWeek != avatar.catalogScheduleCurrentWeek)

        self.notify.debug("Avatar %s at catalog week %s (previous %s)." % (
            avatar.doId, currentWeek, previousWeek))

        # Now schedule the next week's catalog delivery.
        avatar.b_setCatalogSchedule(currentWeek, nextTime)

        # We decided that we should wrap around to the beginning of the
        # catalogs instead of holding on the last.
        modCurrentWeek = ((currentWeek - 1) % ToontownGlobals.CatalogNumWeeks) + 1

        if newMonthlyCatalog or newWeeklyCatalog:
            # Finally, generate a new catalog for the avatar.
            monthlyCatalog = self.generator.generateMonthlyCatalog(avatar, weekStart)
            if newWeeklyCatalog:
                weeklyCatalog = self.generator.generateWeeklyCatalog(avatar, modCurrentWeek, monthlyCatalog)
                backCatalog = self.generator.generateBackCatalog(avatar, modCurrentWeek, previousWeek, weeklyCatalog)
                # Truncate the old items in the back catalog if it's too
                # long.
                

                #import pdb; pdb.set_trace()
                            
                if len(backCatalog) > ToontownGlobals.MaxBackCatalog:
                    stickDict = {}
                    #print ("Back Catalog \n\n%s\n\nend back" % (backCatalog))
                    for item in backCatalog:
                        itemType, numSticky = item.getBackSticky()
                        #print ("type %s numSticky %s" % (itemType, numSticky))
                        if numSticky > 0:
                            if stickDict.has_key(itemType):
                                #print("has Key")
                                if (len(stickDict[itemType]) < numSticky):
                                    stickDict[itemType].append(item)
                            else:
                                #print ("no key")
                                stickDict[itemType] = [item]
                            #print ("stickDict %s" % (stickDict))
                        backCatalog.remove(item)
                    backCatalog = backCatalog[ : ToontownGlobals.MaxBackCatalog]
                    for key in stickDict:
                        stickList = stickDict[key]
                        for item in stickList:
                            backCatalog.append(item)
                    #import pdb; pdb.set_trace()
            else:
                weeklyCatalog = avatar.weeklyCatalog
                backCatalog = avatar.backCatalog
                
            avatar.b_setCatalog(monthlyCatalog, weeklyCatalog, backCatalog)
            if (len(monthlyCatalog) + len(weeklyCatalog) != 0):
                avatar.b_setCatalogNotify(ToontownGlobals.NewItems, avatar.mailboxNotify)

            self.air.writeServerEvent(
                'issue-catalog', avatar.doId, "%s" % (modCurrentWeek))

    def purchaseItem(self, avatar, item, optional):
        # Purchases the item for the given avatar.  Returns the
        # appropriate status code from ToontownGlobals.py.  If the item
        # requires a delayed delivery, this will schedule the
        # delivery; otherwise, it will be purchased immediately.
        
        retcode = None

        if item in avatar.monthlyCatalog:
            catalogType = CatalogItem.CatalogTypeMonthly
        elif item in avatar.weeklyCatalog:
            catalogType = CatalogItem.CatalogTypeWeekly
        elif item in avatar.backCatalog:
            catalogType = CatalogItem.CatalogTypeBackorder
        else:
            self.air.writeServerEvent('suspicious', avatar.doId, 'purchaseItem %s not in catalog' % (item))
            self.notify.warning("Avatar %s attempted to purchase %s, not on catalog." % (avatar.doId, item))
            self.notify.warning("Avatar %s weekly: %s" % (avatar.doId, avatar.weeklyCatalog))
            return ToontownGlobals.P_NotInCatalog

        price = item.getPrice(catalogType)
        if price > avatar.getTotalMoney():
            self.air.writeServerEvent('suspicious', avatar.doId, 'purchaseItem %s not enough money' % (item))
            self.notify.warning("Avatar %s attempted to purchase %s, not enough money." % (avatar.doId, item))
            return ToontownGlobals.P_NotEnoughMoney

        deliveryTime = item.getDeliveryTime() / self.timeScale
        if deliveryTime == 0:
            # Deliver the item immediately.
            self.notify.debug("Avatar %s purchased %s, delivered immediately." % (avatar.doId, item))
            retcode = item.recordPurchase(avatar, optional)

        else:
            # Schedule a future delivery.
            retcode = self.setDelivery(avatar, item, deliveryTime, retcode, doUpdateLater = True)

        if retcode >= 0:
            # Now deduct the avatar's money.  We do this last, since there
            # is a tiny window in which the player might log out between
            # these transactions and miss the last transaction; we'd
            # rather err in the player's favor.
            self.deductMoney(avatar, price, item)

        return retcode
        
    def deductMoney(self, avatar, price, item):

            bankPrice = min(avatar.getBankMoney(), price)
            walletPrice = price - bankPrice

            avatar.b_setBankMoney(avatar.getBankMoney() - bankPrice)
            avatar.b_setMoney(avatar.getMoney() - walletPrice)

            self.air.writeServerEvent(
                'catalog-purchase', avatar.doId, "%s|%s" %
                (price, item))
            #pdb.set_trace()
            
    def refundMoney(self, avatarId, refund):
            avatar = self.air.doId2do.get(avatarId)
            if avatar:
                avatar.addMoney(refund)
                self.air.writeServerEvent(
                    'refunded-money', avatar.doId, "%s" %
                    (refund))
                #pdb.set_trace()
        
    def setDelivery(self, avatar, item, deliveryTime, retcode, doUpdateLater):
        if len(avatar.mailboxContents) + len(avatar.onOrder) >= ToontownGlobals.MaxMailboxContents:
            self.notify.debug("Avatar %s has %s in mailbox and %s on order, too many." % (avatar.doId, len(avatar.mailboxContents), len(avatar.onOrder)))
            if len(avatar.mailboxContents) == 0:
                # If the mailbox is empty, don't tell the user to
                # delete something out of his mailbox--he just has
                # to wait for some of the stuff on his delivery
                # list to arrive.
                retcode = ToontownGlobals.P_OnOrderListFull
            else:
                # If there's stuff in the mailbox to delete,
                # advise the user to do so.
                retcode = ToontownGlobals.P_MailboxFull
        else:
            self.notify.debug("Avatar %s purchased %s, to be delivered later." % (avatar.doId, item))
            now = (int)(time.time() / 60 + 0.5)
            item.deliveryDate = int(now + deliveryTime)
            avatar.onOrder.append(item)
            avatar.b_setDeliverySchedule(avatar.onOrder, doUpdateLater = doUpdateLater)
            retcode = ToontownGlobals.P_ItemOnOrder
        #pdb.set_trace()
        return retcode

        
    def payForGiftItem(self, avatar, item, retcode):
        print("in pay for Gift Item")
        if item in avatar.monthlyCatalog:
            catalogType = CatalogItem.CatalogTypeMonthly
        elif item in avatar.weeklyCatalog:
            catalogType = CatalogItem.CatalogTypeWeekly
        elif item in avatar.backCatalog:
            catalogType = CatalogItem.CatalogTypeBackorder
        else:
            self.air.writeServerEvent('suspicious', avatar.doId, 'purchaseItem %s not in catalog' % (item))
            self.notify.warning("Avatar %s attempted to purchase %s, not on catalog." % (avatar.doId, item))
            self.notify.warning("Avatar %s weekly: %s" % (avatar.doId, avatar.weeklyCatalog))
            retcode = ToontownGlobals.P_NotInCatalog
            return 0
            
        price = item.getPrice(catalogType)
        if price > avatar.getTotalMoney():
            self.air.writeServerEvent('suspicious', avatar.doId, 'purchaseItem %s not enough money' % (item))
            self.notify.warning("Avatar %s attempted to purchase %s, not enough money." % (avatar.doId, item))
            retcode = ToontownGlobals.P_NotEnoughMoney
            return 0
            
        self.deductMoney(avatar, price, item)
        return 1



    def startCatalog(self):
        # This message is sent by the client when he believes it is
        # time to start the catalog system for himself.
        avId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avId)

        if avatar and avatar.catalogScheduleNextTime == 0:
            print("starting catalog for %s" % (avatar.getName()))
            self.deliverCatalogFor(avatar)

