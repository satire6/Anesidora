from pandac.PandaModules import *
from otp.movement.PyVec3 import PyVec3
from direct.showbase.PythonUtil import startProfile
from direct.ffi.FFIExternalObject import FFIExternalObject

class NullClass:
    pass

class SimpleClass:
    def __init__(self, x, y, z):
        self.x = x; self.y = y; self.z = z

class ArgsClass:
    def __init__(self, *args):
        self.x = args[0]; self.y = args[1]; self.z = args[2]

class DerivedClass(SimpleClass):
    def __init__(self, x, y, z):
        self.x = x; self.y = y; self.z = z

class ComplexClass(SimpleClass):
    def __init__(self, x, y, z):
        SimpleClass.__init__(self, x, y, z)

class FFIClass(FFIExternalObject):
    def __init__(self, x, y, z):
        FFIExternalObject.__init__(self)
        self.x = x; self.y = y; self.z = z

Sorts = ['cumulative']
CallInfo = 0
Reps = 100000

def nullLoop(n=Reps):
    for i in xrange(n):
        pass
def createNullClass(n=Reps):
    for i in xrange(n):
        v = NullClass()
def createSimpleClass(n=Reps):
    for i in xrange(n):
        v = SimpleClass(1,2,3)
def createArgsClass(n=Reps):
    for i in xrange(n):
        v = ArgsClass(1,2,3)
def createDerivedClass(n=Reps):
    for i in xrange(n):
        v = DerivedClass(1,2,3)
def createComplexClass(n=Reps):
    for i in xrange(n):
        v = ComplexClass(1,2,3)
def createFFIClass(n=Reps):
    for i in xrange(n):
        v = FFIClass(1,2,3)
def createPyVec3(n=Reps):
    for i in xrange(n):
        v = PyVec3(1,2,3)
def createVec3Direct(n=Reps):
    for i in xrange(n):
        v = Vec3(None)
        v._Vec3__overloaded_constructor_float_float_float(1,2,3)
def createVec3(n=Reps):
    for i in xrange(n):
        v = Vec3(1,2,3)

def doProfile(cmd, filename):
    startProfile(cmd=cmd, filename=filename, callInfo=CallInfo, sorts=Sorts)

"""
profiling

from pandac.PandaModules import *
from otp.movement import ProfVec

ProfVec.doProfile('ProfVec.nullLoop()', 'nullLoop.prof')
ProfVec.doProfile('ProfVec.createNullClass()', filename='createNullClass.prof')
ProfVec.doProfile('ProfVec.createSimpleClass()', filename='createSimpleClass.prof')
ProfVec.doProfile('ProfVec.createArgsClass()', filename='createArgsClass.prof')
ProfVec.doProfile('ProfVec.createDerivedClass()', filename='createDerivedClass.prof')
ProfVec.doProfile('ProfVec.createComplexClass()', filename='createComplexClass.prof')
ProfVec.doProfile('ProfVec.createFFIClass()', filename='createFFIClass.prof')
ProfVec.doProfile('ProfVec.createPyVec3()', filename='createPyVec3.prof')
ProfVec.doProfile('ProfVec.createVec3Direct()', filename='createVec3Direct.prof')
ProfVec.doProfile('ProfVec.createVec3()', filename='createVec3.prof')

"""
