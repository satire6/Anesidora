import cPickle as pickle
from otp.navigation.NavMesh import NavMesh
import sys


args = sys.stdin.read()

filepath,filename,startRow,endRow = pickle.loads(args)

mesh = NavMesh(filepath, filename)
mesh.generatePathData((startRow,endRow))
mesh.printPathData()
sys.stdout.flush()
sys.stdout.close()
