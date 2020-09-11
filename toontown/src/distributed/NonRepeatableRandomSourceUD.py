from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
import random

class NonRepeatableRandomSourceUD(DistributedObjectGlobalUD):
    """
    Source of non-repeatable random number sequences. Queries multiple 'AI' servers for random
    samples and relies on those servers' non-determinism (as well as a random process of sampling
    the servers) to create non-repeatability.
    """
    notify = directNotify.newCategory('NonRepeatableRandomSourceUD')

    RandomNumberCacheSize = 2000000

    class Request(ScratchPad):
        def __init__(self, replyTo, replyToClass, context, num):
            ScratchPad.__init__(self, replyTo=replyTo, replyToClass=replyToClass,
                                context=context, num=num, randoms=[])

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self._randoms = []
        self._requests = []
        self._fakeIt = 0
        if __dev__:
            # don't bloat RAM in dev
            NonRepeatableRandomSourceUD.RandomNumberCacheSize = config.GetInt(
                'random-source-cache-size', 5000)
            self._fakeIt = config.GetBool('fake-non-repeatable-random-source', self._fakeIt)

    def randomSample(self, nrrsDoId, random):
        # receive a random sample from an AI server
        self._randoms = [random,] + self._randoms
        if len(self._randoms) > self.RandomNumberCacheSize:
            self._randoms.pop()
        self._processRequests()
        self.air.sendUpdateToDoId('NonRepeatableRandomSource',
                                  'randomSampleAck',
                                  nrrsDoId,
                                  []
                                  )

    def getRandomSamples(self, replyTo, replyToClass, context, num):
        self._requests.append(self.Request(replyTo, replyToClass, context, num))
        self._processRequests()

    def _processRequests(self):
        while len(self._requests):
            request = self._requests[0]
            # is oldest pending request still pending, and we're out of random samples?
            if (not self._fakeIt) and (len(request.randoms) < request.num):
                if len(self._randoms) == 0:
                    break
            needed = (request.num - len(request.randoms))
            if needed > 0:
                # pull in random samples to the oldest pending request
                numRandoms = min(needed, len(self._randoms))
                if self._fakeIt:
                    # if we're in fake-it mode, just generate random numbers locally
                    # (and repeatably)
                    for i in xrange(numRandoms):
                        request.randoms.append(random.random() * 0xffffffff)
                else:
                    request.randoms += self._randoms[:numRandoms]
                    self._randoms = self._randoms[numRandoms:]
            if request.num == len(request.randoms):
                # if the request is fulfilled, send it out
                self._requests.pop(0)
                self.air.dispatchUpdateToDoId(request.replyToClass, 'getRandomSamplesReply',
                                              request.replyTo,
                                              [request.context, request.randoms, ])
