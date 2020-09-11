from direct.pyinst import imputil
from direct.pyinst import archive_rt

za = archive_rt.ZlibArchive("Toontown.pyz")
imputil.FuncImporter(za.get_code).install()

from toontown.toonbase.ToontownStart import *
