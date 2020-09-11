#from ShowBaseGlobal import *
#import ToontownClientRepository

#cr = ToontownClientRepository.ToontownClientRepository("D:\\Cygwin\\home\\jnschell\\player\\toontown\\src\\configfiles\\toon.dc")

#import FSMInspector
#ins = FSMInspector.FSMInspector(ClassicFSM=cr.fsm)

#cr.fsm.request("connect", ["206.18.93.17", 6667])

from ToonBaseGlobal import *
from toontown.distributed import ToontownClientRepository
import os
from pandac.PandaModules import Filename

# Start up the client repository
fname = Filename(os.getenv("TOONTOWN") + "/src/configfiles/toon.dc")
cr = ToontownClientRepository.ToontownClientRepository(fname.toOsSpecific())

# Start the show
base.startShow(cr)
run()
