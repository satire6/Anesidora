import RepairAvatars
import DatabaseObject
import time
from direct.showbase import PythonUtil
from toontown.toonbase import ToontownGlobals
from toontown.pets import PetTraits, PetConstants
from toontown.minigame import MinigameGlobals

# Fix up Doodle trait problems.
# Up until toontown_1_0_14_30, pets were assigned traits as if they were bought
# in TTC, regardless of where they were actually bought. This patcher recalcs
# the traits as if the pet was bought in a non-TTC safezone. The choice of
# safezone is based on a metric of how advanced the owner Toon is.
# This process also incidentally fixes several pet traits that were
# accidentally inverted, such that TTC pets are in some respects
# better-behaved than DL pets. This is fixed as a by-product of the way we
# recalculate the pet's traits.
# Also fills in safezone-ID field with a sensible value
class PetTraitFixer(RepairAvatars.PetIterator):
    def __init__(self, air, startId=None, endId=None):
        # startId will be the first id that is checked
        # if endId is provided, will check IDs up to but NOT including endId
        RepairAvatars.PetIterator.__init__(self, air)
        self.startId = startId
        self.endId = endId

    def timeToStop(self):
        if self.endId is not None:
            return self.nextObjId >= self.endId
        return RepairAvatars.PetIterator.timeToStop(self)

    def fieldsToGet(self, db):
        return ['setOwnerId', 'setTraitSeed', 'setSafeZone']

    def readIdsFromFile(self, filename='doodle.list'):
        file = open(filename)
        self.objIdList = file.readlines()
        print 'Fixing %s pets' % len(self.objIdList)

    def processPet(self, pet, db):
        RepairAvatars.PetIterator.processPet(self, pet, db)
        # the safezone should be TTC
        if pet.getSafeZone() != ToontownGlobals.ToontownCentral:
            print (
                'Warning: pet %s is a pet that does not need to be patched!' %
                pet.doId)
            # prevent mem leak
            pet.patchDelete()
            # this will request another pet if there are more to request
            self.getNextPet()
            return

        # grab the pet's owner
        print 'requesting owner %s of pet %s' % (pet.getOwnerId(), pet.doId)
        ag = RepairAvatars.AvatarGetter(self.air)
        event = 'getOwner-%s' % pet.doId
        ag.getAvatar(pet.getOwnerId(), fields=['setName', 'setMaxHp',
                                               'setMaxMoney',
                                               'setMaxBankMoney'],
                     event = event)
        self.acceptOnce(event, PythonUtil.Functor(self.gotOwner, pet=pet))

    def gotOwner(self, toon, pet):
        # this will request another pet if there are more to request
        # this is not called until we get to this point because we need to
        # request the pet's owner after we get the pet, and we don't count
        # the pet as 'processed' until we've got the owner
        self.getNextPet()

        if toon is None:
            # prevent mem leak
            pet.patchDelete()
            return

        minHp = 15
        maxHp = ToontownGlobals.MaxHpLimit
        normHp = (toon.getMaxHp() - minHp) / float(maxHp - minHp)
        normHp = PythonUtil.clampScalar(normHp, 0., 1.)

        maxMoney = toon.getMaxMoney() + toon.getMaxBankMoney()

        print '%s HP, %s, %s, %s, %s' % (toon.getMaxHp(), normHp,
                                         toon.getMaxMoney(),
                                         toon.getMaxBankMoney(),
                                         maxMoney)

        szList = MinigameGlobals.SafeZones
        numSz = len(szList)
        for i in range(numSz):
            if normHp < (float(i+1) / numSz):
                break
            # check that they can even afford a pet from the next sz
            if i < (numSz-1):
                if maxMoney < PetConstants.ZoneToCostRange[szList[i+1]][0]:
                    print "toon %s can't afford pet from sz %s" % (
                        pet.getOwnerId(), szList[i+1])
                    break
        newSz = szList[i]

        # this will hold the names of modified values for the pet
        fields = []

        if newSz != ToontownGlobals.ToontownCentral:
            print 'newSafezone: %s' % newSz
            # recalculate the pet's traits
            newTraits = PetTraits.PetTraits(pet.getTraitSeed(), newSz)
            pet.setTraits(newTraits.getValueList())
            fields.extend(map(pet.getSetterName, PetTraits.getTraitNames()))

            pet.setSafeZone(newSz)
            fields.append('setSafeZone')

        if len(fields):
            print '== Fixing pet %s' % pet.doId
            db = DatabaseObject.DatabaseObject(self.air, pet.doId)
            db.storeObject(pet, fields)

        # prevent mem leak
        pet.patchDelete()
        toon.patchDelete()

"""
from toontown.ai import UtilityStart
from toontown.ai.FixPetTraits import PetTraitFixer
#f = PetTraitFixer(simbase.air, 128100052, 132507398)
f = PetTraitFixer(simbase.air)
f.readIdsFromFile('doodle.list')
f.start()
run()
"""
