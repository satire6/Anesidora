import sys
import getopt
import os
import string

helpString ="""
Usage:
  ppython WiseScrubber -h
  ppython WiseScrubber persistDirectory
 
Example:
ppython WiseScrubber C:/toontown-persist/

Generates launcherFileDb.ddb if needed and replaces the inserts a new InstallLauncher.exe md5

Required:
  persistDirectory
      The full path to a directory that retains persistant state
      between publishes.

"""

try:
    opts, pargs = getopt.getopt(sys.argv[1:], 'h')
except Exception, e:
    # User passed in a bad option, print the error and the help, then exit
    print e
    print helpString
    sys.exit(1)

for opt in opts:
    flag, value = opt
    if (flag == '-h'):
        print helpString
        sys.exit(1)
    else:
        print 'illegal option: ' + flag

if (not (len(pargs) == 1)):
    print 'Must specify a persistDirectory'
    sys.exit(1)
else:
    persistDirectory = pargs[0]
    
#persistDirectory = '/c/ttown-persist/english'

from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *

# create a DirectNotify category for the Launcher
notify = directNotify.newCategory("WiseScrubber")
mainFunc()

def mainFunc():
 
    persistDir = Filename.fromOsSpecific(persistDirectory)
    oldLauncherFilename = Filename(persistDir, Filename('launcherFileDb'))
    oldLauncherFile = open(oldLauncherFilename.toOsSpecific(), 'r')
    wiseInstallFile = Filename(os.path.expandvars('$TOONTOWN/src/launcher/InstallLauncher.exe'))
    oldInstallFile = Filename(persistDir,Filename('InstallLauncher.exe'))
    
    # Compute the md5 on the file
    md5 = HashVal()
    md5AFile(wiseInstallFile, md5)

    # Compute the md5 on the old file
    md5Old = HashVal()
    md5AFile(oldInstallFile, md5Old)

    # If the hash values are equal, no need to update the file
    if (md5.eq(md5Old)):
        notify.debug('File has not changed.')
        return
    
    # output the md5 to a linestream
    lineStream = LineStream()
    md5.output(lineStream)
    # Strip off the brackets that the md5 output puts on
    md5str = lineStream.getLine()[1:-1]
    
    # Write the file and md5 to the launcherFileDb
    # Read in the lines that are there now
    lines = oldLauncherFile.readlines()
    oldLauncherFile.close()

    """
    # Prepend the install launcher line
    lines = [('InstallLauncher.exe ' + md5str + '\n')] + lines
    """
    
    # Lookup the line about InstallLauncher, prepend the new md5 at the list of md5's
    notify.info('number of lines in launcherdb = ' + `len(lines)`)
    for i in range (0, len(lines)):
        if (lines[i].find('InstallLauncher.exe') > -1):
            # add the new md5 in there
            notify.info('-----------changing line ' + lines[i])
            lines[i] = lines[i].replace('InstallLauncher.exe', 'InstallLauncher.exe ' + md5str)
            # also save this in dbLauncherFile, first read it, then write it
            dbLauncherFilename = Filename(os.path.expandvars('$TOONTOWN/src/launcher/launcherFileDb.ddb'))
            dbLauncherFile = open(dbLauncherFilename.toOsSpecific(), 'r')
            oldline = dbLauncherFile.readlines()
            dbLauncherFile.close()
            dbLauncherFile = open(dbLauncherFilename.toOsSpecific(), 'w')
            notify.info('-----------to ' + lines[i])
            dbLauncherFile.write(lines[i])
            dbLauncherFile.close()

    # Reopen the file in writing mode, and write the lines out
    newLauncherFile = open(oldLauncherFilename.toOsSpecific(), 'w')
    newLauncherFile.writelines(lines)
    newLauncherFile.close()

    notify.info('File has changed. Installing new version.')

    # Generate the patch file and then rename the new file into place.
    generatePatch(oldInstallFile,
                  wiseInstallFile, md5)
    return
    
def getHighestVersion(persistFilename):
    """
    Look to find the latest version of this file
    relFilePath should be the relative path from the installDir or
    persistDir down to and including the file
    This looks for all the relFilePath.v1.pch style versioned
    files and returns the current version number of the real
    relFilePath
    """
    if (not persistFilename.exists()):
        # There is not even the first file here, return 0
        return 0
    else:
        curVer = 1
        while 1:
            # Look for the next version
            possibleFile = patchVer(persistFilename, curVer+1)
            if possibleFile.exists():
                curVer = curVer + 1
            else:
                return curVer

def fileVer(filename, version):
    # Return the name of the versioned file
    return Filename(filename.cStr() + '.v' + `version`)

def compFile(filename):
    # Return the name of the compressed file
    return Filename(filename.cStr() + '.pz')

def patchVer(filename, version):
    # Return the name of the patch file for this version
    return Filename(fileVer(filename, version).cStr() + '.pch')

def compPatchVer(filename, version):
    # Return the compressed patch file name for this version
    return Filename(patchVer(filename, version).cStr() + '.pz')

def generatePatch(persistFilename, newFilename, newHash):
    # This function renames all of the previously existing patch
    # files down one version, generates a new .v2.pch.pz file for
    # the current version, and moves the new filename onto the old
    # install file.
    
    # Returns the highest version in the directory after completion.
    
    highVer = getHighestVersion(persistFilename)
    
    # Slide all the patch files up one
    if (highVer >= 2):
        # Count down over the versions
        for version in range(highVer, 1, -1):
            # Move this version up one
            curFile = patchVer(persistFilename, version)
            movedName = patchVer(persistFilename, version+1)
            moveFile(curFile, movedName)
            
            # Also touch each version so CVS will recognize it has
            # changed.
            movedName.touch()
            
    notify.info('Building patch for %s' % (persistFilename.cStr()))
    
    # Generate the patch from the previous version to the new version.
    patchFilename = patchVer(persistFilename, 2)
    
    # Build the actual patch
    patchFile = Patchfile()
    # patchFile.setFootprintLength(1024)
    patchFile.build(persistFilename, newFilename, patchFilename)
    # compress it to .pz file
    patchFileCompress = Filename(patchFilename.cStr() + '.pz')
    compressFile(patchFilename, patchFileCompress)
    
    # Now copy the new file in the persist dir
    copyFile(newFilename, persistFilename)
    
def copyFile(fromFilename, toFilename):
    notify.debug('Copying %s to %s' % (fromFilename.cStr(), toFilename.cStr()))
    shutil.copy(fromFilename.toOsSpecific(), toFilename.toOsSpecific())
    os.chmod(toFilename.toOsSpecific(), 0666)
    
def moveFile(fromFilename, toFilename):
    notify.debug('Moving %s to %s' % (fromFilename.cStr(), toFilename.cStr()))
    toFilename.unlink()
    if not fromFilename.renameTo(toFilename):
        notify.error('Unable to move %s to %s.' % (fromFilename.cStr(), toFilename.cStr()))

def compressFile(sourceFilename, destFilename):
    notify.debug('Compressing from %s to %s' % (sourceFilename.cStr(), destFilename.cStr()))
    os.system('pzip -o "%s" "%s"' % (destFilename.toOsSpecific(),
                                     sourceFilename.toOsSpecific()))

