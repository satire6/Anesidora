from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
import DistributedSuitBase
from toontown.toonbase import ToontownGlobals
from toontown.battle import MovieUtil

class DistributedLawbotBossSuit(DistributedSuitBase.DistributedSuitBase):
    """
    These are meant to represent the lawyers in battle three of Lawbot Boss
    """

    notify = DirectNotifyGlobal.directNotify.newCategory(
                                        'DistributedLawbotBossSuit')

    timeToShow = 1.0 #how much time to wait before we show evidence
    timeToRelease = 3.15 #how much time to wait before evidence flies off to toon or pan
    throwPaperEndTime = 4.33
 

    def __init__(self, cr):
        """__init__(cr)"""

        self.flyingEvidenceTrack = None
        
        try:
            self.DistributedSuit_initialized
        except:
            self.DistributedSuit_initialized = 1
            DistributedSuitBase.DistributedSuitBase.__init__(self, cr)

            self.activeIntervals = {}
            self.boss = None

            # Set up the DistributedSuit state machine
            self.fsm = ClassicFSM.ClassicFSM(
                'DistributedLawbotBossSuit',
                [State.State('Off',
                             self.enterOff,
                             self.exitOff,
                             ['Walk',
                              'Battle',
                              'neutral']),
                 State.State('Walk',
                             self.enterWalk,
                             self.exitWalk,
                             ['WaitForBattle',
                              'Battle']
                             ),
                 State.State('Battle',
                             self.enterBattle,
                             self.exitBattle,
                             []),
                 State.State('neutral',
                             self.enterNeutral,
                             self.exitNeutral,
                             ['PreThrowProsecute',
                              'PreThrowAttack',
                              'Stunned']
                             ),
                 State.State('PreThrowProsecute',
                             self.enterPreThrowProsecute,
                             self.exitPreThrowProsecute,
                             ['PostThrowProsecute',
                              'neutral',
                              'Stunned']
                             ),
                 State.State('PostThrowProsecute',
                             self.enterPostThrowProsecute,
                             self.exitPostThrowProsecute,
                             ['neutral',
                              'Stunned']
                             ),
                 State.State('PreThrowAttack',
                             self.enterPreThrowAttack,
                             self.exitPreThrowAttack,
                             ['PostThrowAttack',
                              'neutral',
                              'Stunned']
                              ),
                 State.State('PostThrowAttack',
                             self.enterPostThrowAttack,
                             self.exitPostThrowAttack,
                             ['neutral',
                              'Stunned']
                             ),
                 State.State('Stunned',
                             self.enterStunned,
                             self.exitStunned,
                             ['neutral']
                             ),
                 State.State('WaitForBattle',
                             self.enterWaitForBattle,
                             self.exitWaitForBattle,
                             ['Battle']),
                 ],
                        # Initial state
                        'Off',
                        # Final state
                        'Off',
                       )

            self.fsm.enterInitialState()

        return None

    def generate(self):
        self.notify.debug('DLBS.generate:')
        DistributedSuitBase.DistributedSuitBase.generate(self)

    def announceGenerate(self):
        DistributedSuitBase.DistributedSuitBase.announceGenerate(self)
        self.notify.debug('DLBS.announceGenerate')

        colNode = self.find('**/distAvatarCollNode*')
        colNode.setTag('pieCode',str(ToontownGlobals.PieCodeLawyer))

        self.attackEvidenceA = self.getEvidence(True)
        self.attackEvidenceB = self.getEvidence(True)
        self.attackEvidence = self.attackEvidenceA


        
        self.prosecuteEvidence = self.getEvidence(False)
        #self.setState('neutral')

        self.hideName()
        self.setPickable(False)

    def disable(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    This method is called when the DistributedObject
        //              is removed from active duty and stored in a cache.
        // Parameters:
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        self.notify.debug("DistributedSuit %d: disabling" % self.getDoId())
        self.setState('Off')
        DistributedSuitBase.DistributedSuitBase.disable(self)
        self.cleanupIntervals()
        

        #del self.boss.gavels[self.index]

        self.boss = None

        
        return

    def delete(self):
        """
        ////////////////////////////////////////////////////////////////////
        // Function:    This method is called when the DistributedObject is
        //              permanently removed from the world and deleted from
        //              the cache.
        // Parameters:  none
        // Changes:
        ////////////////////////////////////////////////////////////////////
        """
        try:
            self.DistributedSuit_deleted
        except:
            self.DistributedSuit_deleted = 1
            self.notify.debug("DistributedSuit %d: deleting" % self.getDoId())

            del self.fsm
            DistributedSuitBase.DistributedSuitBase.delete(self)
        return

    def d_requestBattle(self, pos, hpr):
        """d_requestBattle(toonId)
        """
        # Make sure the local toon can't continue to run around (and
        # potentially start battles with other suits!)
        self.cr.playGame.getPlace().setState('WaitForBattle')
        self.sendUpdate('requestBattle', [pos[0], pos[1], pos[2],
                                          hpr[0], hpr[1], hpr[2]])
        return None

    def __handleToonCollision(self, collEntry):
        """
        /////////////////////////////////////////////////////////////
        // Function:    This function is the callback for any
        //              collision events that the collision sphere
        //              for this bad guy might receive
        // Parameters:  collEntry, the collision entry object
        // Changes:     None
        /////////////////////////////////////////////////////////////
        """

        toonId = base.localAvatar.getDoId()
        self.notify.debug('Distributed suit: requesting a Battle with ' +
                           'toon: %d' % toonId)
        self.d_requestBattle(self.getPos(), self.getHpr())

        # the suit on this machine only will go into wait for battle while it
        # is waiting for word back from the server about our battle request
        #
        self.setState('WaitForBattle')

        return None


    # Each state will have an enter function, an exit function,
    # and a datagram handler, which will be set during each enter function.

    # Specific State functions

    ##### Off state #####

    # Defined in DistributedSuitBase.py

    ##### Walk state #####

    def enterWalk(self):
        self.notify.debug("enterWalk")
        self.enableBattleDetect('walk', self.__handleToonCollision)
        # Just stand here waiting for a toon to approach.
        self.loop('walk', 0)
        pathPoints = [Vec3(50, 15, 0),
                      Vec3(50, 25, 0),
                      Vec3(20, 25, 0),
                      Vec3(20, 15, 0),
                      Vec3(50, 15, 0),
                      ]
        self.tutWalkTrack = self.makePathTrack(self, pathPoints,
                                               4.5, "tutFlunkyWalk")
        self.tutWalkTrack.loop()

    def exitWalk(self):
        self.notify.debug("exitWalk")
        self.disableBattleDetect()
        self.tutWalkTrack.pause()
        self.tutWalkTrack = None
        return

    ##### Battle state #####

    # Defined in DistributedSuitBase.py


    ##### Neutral state #####

    def enterNeutral(self):
        self.notify.debug("enterNeutral")
        # Get ready to pass through a door.
        self.notify.debug('DistributedLawbotBossSuit: Neutral')
        #self.resumePath(0)
        self.loop('neutral', 0)
        

    def exitNeutral(self):
        self.notify.debug("exitNeutral")
        return

    ##### WaitForBattle state #####
    

    ##### WaitForBattle state #####

    # Defined in DistributedSuitBase.py

    def doAttack(self, x1, y1, z1, x2,y2,z2):
        self.notify.debug("x1=%.2f y1=%.2f z2=%.2f x2=%.2f y2=%.2f z2=%.2f" % (x1,y1,z1,x2,y2,z2))
        #import pdb; pdb.set_trace()
        
        self.curTargetPt = Point3(x2,y2,z2)
        self.fsm.request('PreThrowAttack')
        return

        attackEvidence = self.getEvidence(True)

        #nodePath = self.nodePath
        nodePath = render

        node = nodePath.attachNewNode('attackEvidence-%s' % self.doId)
        node.setPos(x1,y1,z1)
        #attackEvidence.reparentTo(node)

        duration = 3.0; #decrease this to make it the books fly faster

        throwName = self.uniqueName('lawyerAttack')

        throwingSeq = self.makeAttackThrowingTrack(attackEvidence, duration, Point3(x2,y2,z2))
        
        fullSequence = Sequence(
            throwingSeq,
            name = throwName
            )

            
            
        self.activeIntervals[throwName] = fullSequence
        fullSequence.start()
            
        pass


    def doProsecute(self):
        self.notify.debug('doProsecute')
        #import pdb; pdb.set_trace()

        
        bounds = self.boss.prosecutionColNodePath.getBounds()
        panCenter = bounds.getCenter();
        localPos = panCenter
        prosecutionPanPos = render.getRelativePoint(self.boss.prosecutionColNodePath,localPos)
        self.curTargetPt = prosecutionPanPos
        
        self.fsm.request('PreThrowProsecute')
        return

        
        attackEvidence = self.getEvidence(False)

        #nodePath = self.nodePath
        nodePath = render

        node = nodePath.attachNewNode('prosecuteEvidence-%s' % self.doId)
        node.setPos(self.getPos())
        #attackEvidence.reparentTo(node)

        duration = ToontownGlobals.LawbotBossLawyerToPanTime; #decrease this to make it the books fly faster

        
        throwName = self.uniqueName('lawyerProsecute')

        """
        evidenceSeq = Sequence(
            Func(node.show),
            Parallel(
               node.posInterval( duration , prosecutionPanPos, fluid = 1),
               #node.hprInterval(1, VBase3(720,0,0), fluid = 1)
               ),                      
            Func(node.detachNode),
            Func(self.boss.flashGreen),
            Func(self.clearInterval, throwName)
            )
        """
        #throwingSeq = self.makeThrowingTrack(node, duration, prosecutionPanPos)
        throwingSeq = self.makeProsecuteThrowingTrack(attackEvidence, duration, prosecutionPanPos)
        
        
        
        fullSequence = Sequence(
            throwingSeq,
            Func(self.boss.flashGreen),
            Func(self.clearInterval,throwName),
            name = throwName
            )

        self.activeIntervals[throwName] = fullSequence
        fullSequence.start()

    def makeDummySequence(self):
        #import pdb; pdb.set_trace()
        retval =Sequence(Wait(10))
        return retval
    
    def makeProsecuteThrowingTrack(self, evidence, inFlightDuration, hitPos):
       
        suitTrack = Sequence()
        suitTrack.append(ActorInterval(self,'throw-paper'))

        throwPaperDuration = suitTrack.getDuration();
        #self.notify.debug('throwPaperDuration=%f' % throwPaperDuration)

        inFlight = Parallel(
            evidence.posInterval(inFlightDuration,hitPos,fluid=1)
            )

        origHpr = self.getHpr()
        self.headsUp(hitPos)
        newHpr = self.getHpr()
        self.setHpr(origHpr)
        rotateTrack = Sequence(
            self.hprInterval( self.timeToShow, newHpr, fluid = 1)
            )

        
        propTrack = Sequence(
            Func(evidence.hide),
            Func(evidence.setPos,0,0.5,-0.3), #do some jiggerring to center it on the hand
            Func(evidence.reparentTo, self.getRightHand()),
            Wait(self.timeToShow),
            Func(evidence.show),
            Wait(self.timeToRelease - self.timeToShow),
            Func(evidence.wrtReparentTo, render),
            Func(self.makeDummySequence),
            inFlight,
            Func(evidence.detachNode)
            )
            
        
        throwingTrack =  Parallel(suitTrack, propTrack, rotateTrack)
        #suitTrackDuration = suitTrack.getDuration()
        #propTrackDuration = propTrack.getDuration()
        #throwingTrackDuration = throwingTrack.getDuration()

        #self.notify.debug("suit=%f prop=%f throwing=%f" %
        #                  (suitTrackDuration, propTrackDuration,throwingTrackDuration))
        return throwingTrack

    def makeAttackThrowingTrack(self, evidence, inFlightDuration, hitPos):
        suitTrack = Sequence()
        suitTrack.append(ActorInterval(self,'throw-paper'))

        throwPaperDuration = suitTrack.getDuration();
        #self.notify.debug('throwPaperDuration=%f' % throwPaperDuration)

        origHpr = self.getHpr()
        self.headsUp(hitPos)
        newHpr = self.getHpr()
        self.setHpr(origHpr)
        rotateTrack = Sequence(
            self.hprInterval( self.timeToShow, newHpr, fluid = 1)
            )
               
        propTrack = Sequence(
            Func(evidence.hide),
            Func(evidence.setPos,0,0.5,-0.3), #do some jiggerring to center it on the hand
            Func(evidence.reparentTo, self.getRightHand()),
            Wait(self.timeToShow),
            Func(evidence.show),
            Wait(self.timeToRelease - self.timeToShow),
            Func(evidence.wrtReparentTo, render),
            Func(evidence.setZ,1.3), #lower so big cogs like legal eagle won't be firing too high
            evidence.posInterval(inFlightDuration,hitPos,fluid=1),
            Func(evidence.detachNode)
            )
            
        
        throwingTrack =  Parallel(suitTrack, propTrack, rotateTrack)
        #suitTrackDuration = suitTrack.getDuration()
        #propTrackDuration = propTrack.getDuration()
        #throwingTrackDuration = throwingTrack.getDuration()

        #self.notify.debug("suit=%f prop=%f throwing=%f" %
        #                  (suitTrackDuration, propTrackDuration,throwingTrackDuration))
        return throwingTrack


    def makePreThrowAttackTrack(self, evidence, inFlightDuration, hitPos):
        suitTrack = Sequence()
        suitTrack.append(ActorInterval(self,'throw-paper', endTime=self.timeToRelease))

        throwPaperDuration = suitTrack.getDuration();
        #self.notify.debug('throwPaperDuration=%f' % throwPaperDuration)

        origHpr = self.getHpr()
        self.headsUp(hitPos)
        newHpr = self.getHpr()
        self.setHpr(origHpr)
        rotateTrack = Sequence(
            self.hprInterval( self.timeToShow, newHpr, fluid = 1)
            )
               
        propTrack = Sequence(
            Func(evidence.hide),
            Func(evidence.setPos,0,0.5,-0.3), #do some jiggerring to center it on the hand
            Func(evidence.setScale,1),
            Func(evidence.setHpr,0,0,0),
            Func(evidence.reparentTo, self.getRightHand()),
            Wait(self.timeToShow),
            Func(evidence.show),
            Wait(self.timeToRelease - self.timeToShow),
            )
            
        
        throwingTrack =  Parallel(suitTrack, propTrack, rotateTrack)
        #suitTrackDuration = suitTrack.getDuration()
        #propTrackDuration = propTrack.getDuration()
        #throwingTrackDuration = throwingTrack.getDuration()

        #self.notify.debug("suit=%f prop=%f throwing=%f" %
        
        return throwingTrack

    def makePostThrowAttackTrack(self, evidence, inFlightDuration, hitPos):
        """
        will return two tracks, one for the suit, other for the evidence in flight
        """
        suitTrack = Sequence()
        suitTrack.append(ActorInterval(self,'throw-paper', startTime=self.timeToRelease))

        propTrack = Sequence(
            Func(evidence.wrtReparentTo, render),
            Func(evidence.setScale,1),
            Func(evidence.show),            
            Func(evidence.setZ,1.3), #lower so big cogs like legal eagle won't be firing too high
            evidence.posInterval(inFlightDuration,hitPos,fluid=1),
            Func(evidence.hide)
            )

        return suitTrack, propTrack

    def makePreThrowProsecuteTrack(self, evidence, inFlightDuration, hitPos):
        return self.makePreThrowAttackTrack( evidence, inFlightDuration, hitPos)
        pass


    def makePostThrowProsecuteTrack(self, evidence, inFlightDuration, hitPos):
        suitTrack = Sequence()
        suitTrack.append(ActorInterval(self,'throw-paper', startTime=self.timeToRelease))

        propTrack = Sequence(
            Func(evidence.wrtReparentTo, render),
            Func(evidence.setScale,1),            
            Func(evidence.show),
            evidence.posInterval(inFlightDuration,hitPos,fluid=1),
            Func(evidence.hide)
            )

        return suitTrack, propTrack
    
        pass

    
    def getEvidence(self, usedForAttack = False):
        model =  loader.loadModel('phase_5/models/props/lawbook')

        if usedForAttack:
            bounds = model.getBounds()
            center = bounds.getCenter()
            radius = bounds.getRadius()

            sphere = CollisionSphere(center.getX(),center.getY(),center.getZ(), radius)
            colNode = CollisionNode('BossZap')
            colNode.setTag('attackCode',str(ToontownGlobals.BossCogLawyerAttack))
            colNode.addSolid(sphere)

            #self.evidenceNodePath = model.attachNewNode(colNode)
            model.attachNewNode(colNode)

            #make it ghostly to explain why it passes through the scale =)
            model.setTransparency(1)
            model.setAlphaScale(0.5)                      

        return model
    
 
    def cleanupIntervals(self):
        for interval in self.activeIntervals.values():
            interval.finish()
        self.activeIntervals = {}

    def clearInterval(self, name, finish=1):
        """ Clean up the specified Interval
        """
        if (self.activeIntervals.has_key(name)):
            ival = self.activeIntervals[name]
            if finish:
                ival.finish()
            else:
                ival.pause()
            if self.activeIntervals.has_key(name):
                del self.activeIntervals[name]
        else:
            self.notify.debug('interval: %s already cleared' % name)


    def setBossCogId(self, bossCogId):
        self.bossCogId = bossCogId

        # This would be risky if we had toons entering the zone during
        # a battle--but since all the toons are always there from the
        # beginning, we can be confident that the BossCog has already
        # been generated by the time we receive the generate for its
        # associated battles.
        self.boss = base.cr.doId2do[bossCogId]

    def doStun(self):
        self.notify.debug('doStun')
        self.fsm.request('Stunned')
        

    def enterPreThrowProsecute(self):
        assert(self.notify.debug('enterPreThrowProsecute'))

        #just in case he got stunned
        #self.attackEvidence.hide()
        
        duration = ToontownGlobals.LawbotBossLawyerToPanTime; #decrease this to make it the books fly faster
        throwName = self.uniqueName('preThrowProsecute')


        preThrowTrack = self.makePreThrowProsecuteTrack(self.prosecuteEvidence,duration, self.curTargetPt)

        #postThrowTrack, self.flyingEvidenceTrack = self.makePostThrowProsecuteTrack(
        #    attackEvidence,duration, self.curTargetPt)

        fullSequence = Sequence(
            preThrowTrack,
            Func(self.requestStateIfNotInFlux,'PostThrowProsecute'),
            #Func(self.fsm.request,'PostThrowProsecute'),
            #Parallel(postThrowTrack, self.flyingEvidenceTrack),
            name = throwName,
            )
            
            
        self.activeIntervals[throwName] = fullSequence
        fullSequence.start()
        
        return

    def exitPreThrowProsecute(self):
        assert(self.notify.debug('exitPreThrowProsecute'))
        throwName = self.uniqueName('preThrowProsecute')
        if (self.activeIntervals.has_key(throwName)):
            #self.activeIntervals[throwName].finish()
            self.activeIntervals[throwName].pause()
            del self.activeIntervals[throwName]
        return
        
             
    def enterPostThrowProsecute(self):
        assert(self.notify.debug('enterPostThrowProsecute'))
        duration = ToontownGlobals.LawbotBossLawyerToPanTime; #decrease this to make it the books fly faster
        throwName = self.uniqueName('postThrowProsecute')


        postThrowTrack, self.flyingEvidenceTrack = self.makePostThrowProsecuteTrack(
            self.prosecuteEvidence,duration, self.curTargetPt)

        #waitKludgeTime = 1.0 
        fullSequence = Sequence(
            postThrowTrack,
            #Wait(waitKludgeTime),
            Func(self.requestStateIfNotInFlux,'neutral'),   
            #Func(self.fsm.request,'neutral'),
            name = throwName,
            )
            
            
        self.activeIntervals[throwName] = fullSequence
        fullSequence.start()

        flyName = self.uniqueName('flyingEvidence')
        self.activeIntervals[flyName] = self.flyingEvidenceTrack
        self.flyingEvidenceTrack.append(Func(self.finishedWithFlying,'prosecute'))        
        self.flyingEvidenceTrack.start()
        return


    def exitPostThrowProsecute(self):
        assert(self.notify.debug('exitPostThrowProsecute'))

        #RAU note that we do not stop the flyingEvidenceTrack
        throwName = self.uniqueName('postThrowProsecute')
        if (self.activeIntervals.has_key(throwName)):
            self.activeIntervals[throwName].finish()
            del self.activeIntervals[throwName]
        return
        
    def requestStateIfNotInFlux(self, state):
        if not self.fsm._ClassicFSM__internalStateInFlux:
            self.fsm.request(state)
    
    def enterPreThrowAttack(self):
        assert(self.notify.debug('enterPreThrowAttack'))

        #just in case he got stunned
        #self.prosecuteEvidence.hide()

        if self.attackEvidence == self.attackEvidenceA:
            self.attackEvidence = self.attackEvidenceB
        else:
            self.attackEvidence = self.attackEvidenceA
        
        
        duration = 3.0; #decrease this to make it the books fly faster


        throwName = self.uniqueName('preThrowAttack')


        preThrowTrack = self.makePreThrowAttackTrack(self.attackEvidence,duration, self.curTargetPt)

        #postThrowTrack, self.flyingEvidenceTrack = self.makePostThrowAttackTrack(
        #    attackEvidence,duration, self.curTargetPt)

        fullSequence = Sequence(
            preThrowTrack,
            Func(self.requestStateIfNotInFlux,'PostThrowAttack'),
            #Func(self.fsm.request,'PostThrowAttack'),
            #Parallel(postThrowTrack, self.flyingEvidenceTrack),
            name = throwName,
            )
            
            
        self.activeIntervals[throwName] = fullSequence
        fullSequence.start()
        
        return

    def exitPreThrowAttack(self):
        assert(self.notify.debug('exitPreThrowAttack'))
        throwName = self.uniqueName('preThrowAttack')
        if (self.activeIntervals.has_key(throwName)):
            #self.activeIntervals[throwName].finish()
            self.activeIntervals[throwName].pause()
            del self.activeIntervals[throwName]
        return
             
    def enterPostThrowAttack(self):
        assert(self.notify.debug('enterPostThrowAttack'))
        #attackEvidence = self.getEvidence(True)        
        duration = 3.0; #decrease this to make it the books fly faster

        throwName = self.uniqueName('postThrowAttack')


        postThrowTrack, self.flyingEvidenceTrack = self.makePostThrowAttackTrack(
            self.attackEvidence,duration, self.curTargetPt)

        #waitKludgeTime = ToontownGlobals.LawbotBossLawyerCycleTime - self.throwPaperEndTime - 0.1
        fullSequence = Sequence(
            postThrowTrack,
            #Wait(waitKludgeTime),
            Func(self.requestStateIfNotInFlux,'neutral'),   
            #Func(self.fsm.request,'neutral'),
            name = throwName,
            )

        self.notify.debug('duration of postThrowAttack = %f' % fullSequence.getDuration())
            
        self.activeIntervals[throwName] = fullSequence
        fullSequence.start()

        flyName = self.uniqueName('flyingEvidence')
        self.activeIntervals[flyName] = self.flyingEvidenceTrack
        self.flyingEvidenceTrack.append(Func(self.finishedWithFlying,'attack'))        
        self.flyingEvidenceTrack.start()
        return

    def finishedWithFlying(self, str):
        self.notify.debug('finished flyingEvidenceTrack %s' % str)

    def exitPostThrowAttack(self):
        assert(self.notify.debug('exitPostThrowAttack'))
        #RAU note that we do not stop the flyingEvidenceTrack
        throwName = self.uniqueName('postThrowAttack')
        if (self.activeIntervals.has_key(throwName)):
            self.activeIntervals[throwName].finish()
            del self.activeIntervals[throwName]
        return

    def enterStunned(self):
        assert(self.notify.debug('enterStunned'))

        stunSequence = MovieUtil.createSuitStunInterval(self, 0, ToontownGlobals.LawbotBossLawyerStunTime)
        #seqName = self.uniqueName('stunSequence')
        seqName = stunSequence.getName()
        stunSequence.append(Func(self.fsm.request,'neutral'))
        self.activeIntervals[seqName] = stunSequence
        stunSequence.start()
        
        return
        
    def exitStunned(self):
        assert(self.notify.debug('exitStunned'))
        self.prosecuteEvidence.hide()
        self.attackEvidence.hide()
        return

     
