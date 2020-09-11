import CatalogItem
from toontown.toonbase import TTLocalizer
from direct.showbase import PythonUtil
from toontown.toonbase import ToontownGlobals

class CatalogInvalidItem(CatalogItem.CatalogItem):
    """CatalogInvalidItem

    This special item type may be returned by CatalogItem.getItem()
    and similar functions.  It represents a CatalogItem that was not
    correctly decoded from the encoded blob; its purposes is to stand
    in as a placeholder for the broken item, so that AI code will not
    necessarily crash when an invalid message is received from a
    client.

    """

    def requestPurchase(self, phone, callback):
        self.notify.error("Attempt to purchase invalid item.")

    def acceptItem(self, mailbox, index, callback):
        self.notify.error("Attempt to accept invalid item.")

    def output(self, store = ~0):
        return "CatalogInvalidItem()"
