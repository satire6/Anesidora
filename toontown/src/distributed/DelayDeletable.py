from direct.distributed.DistributedObject import ESGenerating, ESGenerated

class DelayDeletable:
    # mixin for DistributedObjects that can be DelayDeleted via
    # toontown.distributed.DelayDelete.DelayDelete
    
    DelayDeleteSerialGen = SerialNumGen()

    def delayDelete(self):
        """
        Inheritors should redefine this to take appropriate action on delayDelete
        """
        pass

    def acquireDelayDelete(self, name):
        # Also see DelayDelete.py
        global ESGenerating, ESGenerated
        if ((not self._delayDeleteForceAllow) and
            (self.activeState not in (ESGenerating, ESGenerated))):
            self.notify.error(
                'cannot acquire DelayDelete "%s" on %s because it is in state %s' % (
                name, self.__class__.__name__, ESNum2Str[self.activeState]))

        if self.getDelayDeleteCount() == 0:
            self.cr._addDelayDeletedDO(self)

        token = DelayDeletable.DelayDeleteSerialGen.next()
        self._token2delayDeleteName[token] = name

        assert self.notify.debug(
            "delayDelete count for doId %s now %s" %
            (self.doId, len(self._token2delayDeleteName)))

        # Return the token, user must pass token to releaseDelayDelete
        return token

    def releaseDelayDelete(self, token):
        name = self._token2delayDeleteName.pop(token)
        assert self.notify.debug("releasing delayDelete '%s'" % name)
        if len(self._token2delayDeleteName) == 0:
            assert self.notify.debug(
                "delayDelete count for doId %s now 0" % (self.doId))
            self.cr._removeDelayDeletedDO(self)
            # do we have a pending delete?
            if self._delayDeleted:
                self.disableAnnounceAndDelete()

    def getDelayDeleteNames(self):
        return self._token2delayDeleteName.values()

    def forceAllowDelayDelete(self):
        # Toontown has code that creates a DistributedObject manually and then
        # DelayDeletes it. That code should call this method, otherwise the
        # DelayDelete system will crash because the object is not generated
        self._delayDeleteForceAllow = True
