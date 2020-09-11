
import sys
import getopt
import os
import shutil
import string
import py_compile
import time
import re
import PRCEncryptionKey
from otp.publish import FreezeTool

helpString ="""
Usage:
  python Scrubber [opts] command installDirectory persistDirectory

Options:

  -h   Display this help

  -R   Run in CD mode

  -f filelist
       Specify pathname of filelist file.

  -p platform
       Should be WIN32 or OSX.

Example:
python Scrubber scrub J:/ C:/toontown-persist/

Generates phased multifiles suitable for publishing
Creates a persist directory

Required:
  command
      The action to perform.  This is either 'scrub' to update the
      contents of the persistDirectory and build launcherFileDb,
      'wise' to build patches against InstallLauncher.exe and build
      launcherFileDb.ddb, or 'copy' to copy from the persistDirectory
      to the installDirectory, compressing as it goes.

  installDirectory
      The full path to a temporary directory to copy the
      ready-to-be-published files into.

  persistDirectory
      The full path to a directory that retains persistant state
      between publishes.
"""

#
# filelist syntax:
#
#   multifile <mfname> <phase>
#
#     Begins a new multifile.  All files named after this line and
#     until the next multifile line will be a part of this multifile.
#
#     <mfname>
#       The filename of the multifile, no directory.
#
#     <phase>
#       The numeric phase in which this multifile should be downloaded.
#
#
#   file <extractFlag> <filename> <dirname> <platforms>
#
#     Adds a single file to the current multifile.
#
#     <extractFlag>
#       One of:
#         0 - Leave this file within the multifile; it can be read by
#             Panda from there.
#         1 - Extract this file from the multifile, but do not bother
#             to hash check it on restart.
#         2 - Extract this file, and hash check it every time the
#             client starts, to ensure it is not changed.
#
#     <filename>
#       The name of the file to add.  This is the full path to the
#       file on the publishing machine at the time this script is run.
#
#     <dirname>
#       The directory in which to install the file, on the client.
#       This should be a relative pathname from the game directory.
#       The file is written to the multifile with its directory part
#       taken from this, and its basename taken from the source
#       filename, above.  Also, if the file is extracted, it will be
#       written into this directory on the client machine.
#
#       The directory name "toplevel" is treated as a special case;
#       this maps to the game directory itself, and is used for files
#       in the initial download.
#
#     <platforms>
#       A comma-delimited list of platforms for which this file should
#       be included with the distribution.  Presently, the only
#       options are WIN32 and/or OSX.
#
#
#   dir <extractFlag> <localDirname> <dirname>
#
#     Adds an entire directory tree to the current multifile.  The
#     named directory is searched recursively and all files found are
#     added to the current multifile, as if they were listed one a
#     time with a file command.
#
#     <extractFlag>
#       (Same as for the file command, above.)
#
#     <localDirname>
#       The name of the local directory to scan on the publishing
#       machine.
#
#     <dirname>
#       The name of the corresponding local directory on the client
#       machine; similar to <dirname> in the file command, above.
#
#
#   module modulename
#
#     Adds the named Python module to the exe or dll archive.  All files
#     named by module, until the next freeze_exe or freeze_dll command (below),
#     will be compiled and placed into the same archive.  
#
#   exclude_module modulename
#
#     Excludes the named Python module from the archive.  This module
#     will not be included in the archive, but an import command may
#     still find it if a .py file exists on disk.
#
#   forbid_module modulename
#
#     Excludes the named Python module from the archive.  This module
#     will specifically never be imported by the resulting executable,
#     even if a .py file exists on disk.  (However, a module command
#     appearing in a later phase--e.g. Phase3.pyd--can override an
#     earlier forbid_module command.)
#
#   dc_module file.dc
#
#     Adds the modules imported by the indicated dc file to the
#     archive.  Normally this is not necessary if the file.dc is
#     explicitly included in the filelist; but this command may be
#     useful if the file.dc is imported in a later phase.
#
#   freeze_exe <extractFlag> <exeFilename> <mainModule> <dirname>
#
#     <extractFlag>
#       (Same as for the file command, above.)
#
#     <exeFilename>
#       The name of the executable file to generate.  Do not include
#       an extension name; on Windows, the default extension is .exe;
#       on OSX there is no extension.
#
#     <mainModule>
#       The name of the python module that will be invoked first (like
#       main()) when the resulting executable is started.
#
#     <dirname>
#       (Same as for the file command, above.)
#
#   freeze_dll <extractFlag> <dllFilename> <dirname>
#
#     <extractFlag>
#       (Same as for the file command, above.)
#
#     <dllFilename>
#       The name of the shared library file to generate.  Do not include
#       an extension name; on Windows, the default extension is .pyd;
#       on OSX the extension is .so.
#
#     <dirname>
#       (Same as for the file command, above.)

filelistPath = '$TOONTOWN/src/publish/QuickFilelist'
installDirectory = None
persistDirectory = None

#
# This is the list of filename extensions for files that will be be
# stored in a compressed form within the multifiles.  These files will
# remain compressed within their multifiles and will thus be stored
# compressed on the client's machine, and transparently decompressed
# on-the-fly at runtime when they are accessed out of the multifile.
#
# There's no real advantage for doing this in terms of improving
# download time, since we already compress the whole multifile for
# download.  Load-time performance doesn't seem to be much affected
# one way or the other (on the one hand, now we have pay extra CPU to
# decompress the file at load time; on the other hand, since the
# actual file stored on disk is smaller, there is less I/O overhead).
#
# The real reason we do this is to provide a tiny bit more
# obfuscation: since these are text files, their contents would be
# immediately apparent if the user did a 'strings' command on the
# multifile.  Compressing them incidentally makes them binary and
# therefore difficult to read.  Of course, this is mere obfuscation,
# not real security.
#

compressExtensions = ['ptf', 'dna', 'txt', 'dc']
compressFiles = []

server_ddb = 'server.ddb'
client_ddb = 'client.ddb'

cdmode=0

downloadParText = """#
# Generated by %s on %s.
#
# launcherFileDb  %s
# server.ddb.pz   %s
#

VALIDATE_DOWNLOAD=%s

"""

try:
    opts, pargs = getopt.getopt(sys.argv[1:], 'hRf:p:m:')
except Exception, e:
    # User passed in a bad option, print the error and the help, then exit
    print e
    print helpString
    sys.exit(1)

platform = 'WIN32'
if os.name != 'nt':
    platform = 'OSX'

for opt in opts:
    flag, value = opt
    if (flag == '-h'):
        print helpString
        sys.exit(1)
    elif (flag == '-R'):
        cdmode = 1
    elif (flag == '-f'):
        filelistPath = value
    elif (flag == '-p'):
        platform = value
    elif (flag == '-m'):
        mode = value
    else:
        print 'illegal option: ' + flag
        sys.exit(1)

if (not (len(pargs) == 3)):
    print 'Must specify a command, an installDirectory, and a persistDirectory'
    sys.exit(1)
else:
    command = pargs[0]
    installDirectory = pargs[1]
    persistDirectory = pargs[2]


from direct.directnotify.DirectNotifyGlobal import *
from pandac.PandaModules import *

# Now that we have PandaModules, make Filename objects for our
# parameters.
filelistPath = Filename.expandFrom(filelistPath)
installDirectory = Filename.fromOsSpecific(installDirectory)
persistDirectory = Filename.fromOsSpecific(persistDirectory)

class Scrubber:
    def __init__(self):

        # create a DirectNotify category for the Launcher
        self.notify = directNotify.newCategory("Scrubber")

        self.persistDir = persistDirectory
        self.persistServerDbFilename = Filename(self.persistDir,
                                                Filename(server_ddb))
        self.persistClientDbFilename = Filename(self.persistDir,
                                                Filename(client_ddb))
        self.launcherFileDb = Filename(self.persistDir, Filename('launcherFileDb'))

        # The new-style publish allows the use of hexadecimal as well
        # as decimal-format hashes.  The old-style publish only
        # supports decimal hashes.
        self.ddbHexHashes = True

        # The multifiles and patches live in a subdirectory called content
        self.installDir = installDirectory
        self.contentDir = Filename(self.installDir, Filename('content/'))
        self.contentDir.makeDir()

        self.phase1 = re.compile('phase_1.mf')

        if command == 'scrub':
            self.doScrubCommand()

        elif command == 'copy':
            self.doCopyCommand()

        else:
            print "Invalid command: %s" % (command)
            sys.exit(1)

    def doCopyCommand(self):
        # First, open the existing download database (in two files).
        if not self.persistServerDbFilename.exists() or \
           not self.persistClientDbFilename.exists():
            print "server.ddb or client.ddb not found."
            sys.exit(1)

        self.dldb = DownloadDb(self.persistServerDbFilename, self.persistClientDbFilename)

        # Walk through each multifile in the download database and
        # copy it, along with all of its patches, to the content dir.
        numMfiles = self.dldb.getServerNumMultifiles()

        # Get a file called 'progress' in the content directory to
        # contain the lengths of all of these downloadable files.
        self.readProgressFile()

        for mi in range(numMfiles):
            mfname = self.dldb.getServerMultifileName(mi)
            if self.phase1.match(mfname) == None:    # don't copy phase_1 files
              self.installMfile(Filename(mfname))

        # Finally, copy the ddb files, compressed, to the content dir.
        installServerDbFilename = Filename(self.contentDir,
                                           Filename(server_ddb + '.pz'))
        installClientDbFilename = Filename(self.contentDir,
                                           Filename(client_ddb + '.pz'))
        self.compressFile(self.persistServerDbFilename, installServerDbFilename)
        self.compressFile(self.persistClientDbFilename, installClientDbFilename)

        # close the progressFile
        self.writeProgressFile()

        # Copy in the launcherFileDb, launcherFileDb.ddb, and bs.ddb
        # files as well.
        for file in ['launcherFileDb', 'launcherFileDb.ddb', 'bs.ddb']:
            persistFile = Filename(self.persistDir, Filename(file))
            installFile = Filename(self.installDir, Filename(file))
            self.copyFile(persistFile, installFile)

        # Finally, generate hash values for the launcherFileDb and
        # server.ddb.pz files, so we can install this on the server
        # to validate the client download.
        installLauncherFileDb = Filename(self.installDir, Filename('launcherFileDb'))
        launcherFileDbHash = HashVal()
        launcherFileDbHash.hashFile(installLauncherFileDb)
        serverDbFileHash = HashVal()
        serverDbFileHash.hashFile(installServerDbFilename)

        downloadHash = HashVal()
        downloadHash.mergeWith(launcherFileDbHash)
        downloadHash.mergeWith(serverDbFileHash)

        self.notify.info("Download hash is %s" % (downloadHash.asHex()))

        # Write the download hash to $TOONTOWN/src/configfiles/download.par
        downloadParFilename = Filename.expandFrom('$TOONTOWN/src/configfiles/download.par')
        downloadPar = open(downloadParFilename.toOsSpecific(), "w")
        downloadPar.write(downloadParText % (
            os.environ.get('USER'),
            time.asctime(time.localtime()),
            launcherFileDbHash.asHex(),
            serverDbFileHash.asHex(),
            downloadHash.asHex(),
            ))
        downloadPar.close()

    def flushIO(self):
        sys.stdout.flush()      # MAKE python flush I/O for more interactive response

    def readProgressFile(self):
        self.progressMap = {}
        progressFilename = Filename(self.contentDir, Filename('progress'))

        if progressFilename.exists():
            self.notify.info('reading ' + progressFilename.toOsSpecific())
            self.flushIO()
            progressFile = open(progressFilename.toOsSpecific(), "r")

            for line in progressFile.readlines():
                line = line.strip()
                if ' ' in line:
                    filename, size = line.strip().split(' ', 1)
                    try:
                        size = int(size)
                    except:
                        continue
                    self.progressMap[filename] = size

            progressFile.close()

    def writeProgressFile(self):
        progressFilename = Filename(self.contentDir, Filename('progress'))
        self.notify.info('writing ' + progressFilename.toOsSpecific())
        self.flushIO()
        progressFilename.unlink()
        progressFile = open(progressFilename.toOsSpecific(), "w")

        items = self.progressMap.items()

        # Sort it into alphabetical order by filename, for no good reason.
        items.sort()

        for filename, size in items:
            progressFile.write('%s %d\n' % (filename, size))

        progressFile.close()

    def doCDPatch(self):

        if self.lineList[0] == 'multifile':
            if self.currentMfname:
                self.closePreviousMfile()

            self.currentMfname = Filename(self.lineList[1])
            self.currentMfphase = eval(self.lineList[2])
            self.notify.info('doCDPatch: scanning multifile: ' + self.currentMfname.cStr() + ' phase: ' + `self.currentMfphase`)

            # copy in the webmode multifile instead of generating a new one
            baseName = self.currentMfname.getBasenameWoExtension()

            srcName = Filename(self.persistDir, Filename('../' + baseName))
            dstName = Filename(self.mfTempDir, Filename(baseName))
            self.copyFile(srcName, dstName)

            # parseMfile subset
            mfsize = 0 # This will be filled in later
            mfstatus = DownloadDb.StatusIncomplete
            self.dldb.serverAddMultifile(self.currentMfname.getFullpath(), self.currentMfphase, mfsize, mfstatus)

        # Add a file to the current multifile
        elif self.lineList[0] == 'file' or self.lineList[0] == 'freeze_exe' or self.lineList[0] == 'freeze_dll':
            if self.lineList[0] == 'file' and len(self.lineList) > 4 and self.lineList[4]:
                platforms = self.lineList[4].split(',')
                if platform not in platforms:
                    return
                
            extractFlag = int(self.lineList[1])
            # The original file we want to install, at its full path
            sourceFilename = Filename.expandFrom(self.lineList[2])
            #self.notify.debug('doCDPatch: ' + sourceFilename.cStr())

            # The relative path where we want to put this file
            dir = Filename.expandFrom(self.lineList[3])
            # The relative path plus the file name
            basename = Filename(sourceFilename.getBasename())
            relInstallFilename = Filename(dir, basename)

            if extractFlag >= 1:
                # Add this file to the current downloadDb
                self.dldb.serverAddFile(self.currentMfname.getFullpath(),
                                        relInstallFilename.getFullpath())


    def doScrubCommand(self):

        # The launcher phase writes out the launcherFileDb
        # The launcher phase is special because the ActiveX does the hash checks
        # To do the hash checks it reads in a special file called launcherFileDb
        self.launcherPhase = 1

        # The filelist is a developer maintained text file listing all the files
        # to publish, in each phase.
        self.notify.info('init: Reading filelist: ' + filelistPath.cStr())
        self.filelist = open(filelistPath.toOsSpecific())
        self.lines = self.filelist.readlines()
        self.filelist.close()

        # Initialize some placeholder variables
        self.currentMfname = None
        self.currentMfile = None
        self.currentMfphase = 0
        self.lineNum = -1

        # This records the current list of modules we have added so
        # far.
        self.freezer = FreezeTool.Freezer()

        # The persist dir is the directory in which the results from
        # past publishes are stored so we can generate patches against
        # them.  If it is empty when we begin, we will generate a
        # brand new publish with no previous patches.
        self.persistDir.makeDir()

        # Generate launcherFileDb within the persist dir.
        if (not cdmode):
            self.launcherFile = open(self.launcherFileDb.toOsSpecific(), 'w')

        # Within the persist dir, we make a temporary holding dir for
        # generating multifiles.
        self.mfTempDir = Filename(self.persistDir, Filename('mftemp/'))
        self.mfTempDir.makeDir()

        # We also need a temporary holding dir for squeezing py files.
        self.pyzTempDir = Filename(self.persistDir, Filename('pyz/'))
        self.pyzTempDir.makeDir()

        # Change to the persist directory so the temp files will be
        # created there
        os.chdir(self.persistDir.toOsSpecific())

        self.notify.info('init: persist dir: ' + self.persistDir.cStr())

        # Make sure we have a server.ddb and a client.ddb file.
        if not self.persistServerDbFilename.exists():
            self.notify.info("Creating new %s" % (self.persistServerDbFilename.cStr()))
            dldb = DownloadDb()
            dldb.createNewServerDb()
            dldb.writeServerDb(self.persistServerDbFilename)

        if not self.persistClientDbFilename.exists():
            self.notify.info("Creating new %s" % (self.persistClientDbFilename.cStr()))
            dldb = DownloadDb()
            dldb.writeClientDb(self.persistClientDbFilename)

        self.dldb = DownloadDb(self.persistServerDbFilename, self.persistClientDbFilename)

        # The server db maintains the files (with hash values) for the latest
        # versions of each file on the server. The clients download this file
        # every session at startup
        self.dldb.createNewServerDb()

        self.notify.info('init: creating launcherFileDb at: ' + self.launcherFileDb.cStr())

        # Now start parsing the filelist lines
        self.lineList = self.getNextLine()
        while self.lineList:
            if cdmode:
                # Just Copy dont create new multifile
                self.doCDPatch()

            # If we get to a new multifile, we know we are done with the previous one
            # close it and make a new one
            elif self.lineList[0] == 'multifile':
                if self.currentMfname:
                    self.closePreviousMfile()
                # Make a new file
                self.parseMfile()

            # Add a Python file to the executable
            elif self.lineList[0] == 'module':
                self.parseModule(self.lineList)

            elif self.lineList[0] == 'exclude_module':
                self.parseExcludeModule(self.lineList, forbid = False)

            elif self.lineList[0] == 'forbid_module':
                self.parseExcludeModule(self.lineList, forbid = True)

            elif self.lineList[0] == 'dc_module':
                self.parseDCModule(self.lineList)

            # Add a file to the current multifile
            elif self.lineList[0] == 'freeze_exe':
                self.freezeExe(self.lineList)

            # Add a file to the current multifile
            elif self.lineList[0] == 'freeze_dll':
                self.freezeDll(self.lineList)

            # Add a file to the current multifile
            elif self.lineList[0] == 'file':
                self.parseFile(self.lineList)

            # Grab the files in this directory
            elif self.lineList[0] == 'dir':
                self.parseDir()

            else:
                # error
                raise StandardError, ('Unknown directive: ' + `self.lineList[0]`
                                      + ' on line: ' + `self.lineNum+1`)
            self.lineList = self.getNextLine()

        # All done, close the final multifile
        if self.currentMfname:
            self.closePreviousMfile()

        if not cdmode:
            self.launcherFile.close()

        # Write the server ddb
        self.dldb.writeServerDb(self.persistServerDbFilename)

        # For the CDROM, we need the client db to already have every multifile
        # complete. We'll just set the fields and write out a new client ddb
        # The Wise CDsetup.wse looks for and installs this clientCD.ddb
        # self.clientDbFilename = Filename('clientCD.ddb')
        # self.absClientDbFilename = Filename(self.persistDir, self.clientDbFilename)

        # We trick the clientDb into thinking it has downloaded everything
        # by setting the size to fullsize and extrated to true
        # for i in range(self.dldb.getServerNumMultifiles()):
        #    # What is this multifile's name?
        #    mfname = self.dldb.getServerMultifileName(i)
        #    fullSize = self.dldb.getServerMultifileSize(mfname)
        #    self.dldb.addClientMultifile(mfname)
        #    self.dldb.setClientMultifileSize(mfname, fullSize)
        #    self.dldb.setClientMultifileExtracted(mfname)
        ## Now write it to disk
        #self.dldb.writeClientDb(self.absClientDbFilename)

        self.notify.info('init: Scrubber finished')

    def getNextLine(self):
        """
        Read in the next line of the line list
        """
        self.lineNum = self.lineNum + 1
        while (self.lineNum < len(self.lines)):
            # Eat python style comments
            if (self.lines[self.lineNum][0] == '#'):
                self.lineNum = self.lineNum + 1
            else:
                # Return the line as an array split at whitespace, and
                # do not include the newline character (at index -1)
                line = self.lines[self.lineNum][:-1].split()
                if line:
                    return line
                # Skip the line, it was just a blank line
                else:
                    self.lineNum = self.lineNum + 1
        else:
            return None

    def parseMfile(self):
        """
        The current line is a multifile description.
        Read in the properties and add the multifile to the downloadDb
        """
        self.currentMfname = Filename(self.lineList[1])
        self.currentMfname.setBinary()

        sourceFilename = Filename(self.mfTempDir,
                                  Filename(self.currentMfname.getBasenameWoExtension()))
        self.currentMfile = Multifile()
        self.currentMfile.setRecordTimestamp(False)
        sourceFilename.unlink()
        if not self.currentMfile.openWrite(sourceFilename):
            self.notify.error("Unable to open multifile %s for writing." % (sourceFilename.cStr()))
        self.currentMfphase = eval(self.lineList[2])
        self.notify.info('parseMfile: creating multifile: ' + self.currentMfname.cStr()
                          + ' phase: ' + `self.currentMfphase`)
        mfsize = 0 # This will be filled in later
        mfstatus = DownloadDb.StatusIncomplete
        self.dldb.serverAddMultifile(self.currentMfname.getFullpath(),
                                     self.currentMfphase, mfsize, mfstatus)

    def getHighestVersion(self, persistFilename):
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
                possibleFile = self.patchVer(persistFilename, curVer+1)
                if possibleFile.exists():
                    curVer = curVer + 1
                else:
                    return curVer

    def fileVer(self, filename, version):
        # Return the name of the versioned file
        return Filename(filename.cStr() + '.v' + `version`)

    def compFile(self, filename):
        # Return the name of the compressed file
        return Filename(filename.cStr() + '.pz')

    def patchVer(self, filename, version):
        # Return the name of the patch file for this version
        return Filename(self.fileVer(filename, version).cStr() + '.pch')

    def compPatchVer(self, filename, version, useBzip2 = 0):
        # Return the compressed patch file name for this version
        if useBzip2:
            return Filename(self.patchVer(filename, version).cStr() + '.bz2')
        else:
            return Filename(self.patchVer(filename, version).cStr() + '.pz')

    def patchMFile(self, sourceFilename, newHash,
                   persistFilename, relInstallFilename):
        # Compares the newly-generated multifile to the previous
        # one in the persist directory, and generates whatever patches
        # are necessary.  Returns the highest (oldest) version number
        # in the directory after completion.

        # If the file has never been installed, do it, and we have no patches.
        if (not persistFilename.exists()):
            # Copy the new file in its place
            self.moveFile(sourceFilename, persistFilename)
            self.dldb.addVersion(relInstallFilename, newHash, 1)
            # We'd better write out the server.ddb file now, to make sure
            # it stays in sync with the directory, just in case we get
            # aborted later.
            self.dldb.writeServerDb(self.persistServerDbFilename)
            return 1

        oldHash = HashVal()
        oldHash.hashFile(persistFilename)

        # If the hash values are equal, no need to update the file
        if (newHash.eq(oldHash)):
            self.notify.debug('File has not changed.')
            return self.getHighestVersion(persistFilename)
        else:
            self.notify.info('%s has changed. Installing new version.' % (persistFilename.getBasename()))
            self.notify.debug('  Old hash: %s' % (oldHash.asDec()))
            self.notify.debug('  New hash: %s' % (newHash.asDec()))
            # Generate the patch file and then rename the new file
            # into place.
            if (self.phase1.search(sourceFilename.cStr()) == None):
                return self.generatePatch(persistFilename,
                                          sourceFilename, newHash,
                                          relInstallFilename)
            else:
                self.moveFile(sourceFilename, persistFilename)
                return self.getHighestVersion(persistFilename)

    def checkDbIntegrity(self, relInstallFilename, fileHash, highVer,
                         persistFilename):
        # Make sure our downloadDb agrees with the patch files in the
        # directory about the number and hash codes of past versions
        # of the given multifile.  If they don't agree, most likely a
        # previous attempt to run the publish script was interrupted
        # for some reason; you will need to restore everything to a
        # known state (e.g. by cvs updating from scratch).

        dbHighVer = self.dldb.getNumVersions(relInstallFilename)
        if (dbHighVer != highVer):
            self.notify.warning("server.ddb shows %d versions of %s, while %s versions are found in the directory!" %
                                (dbHighVer, relInstallFilename.cStr(), highVer))
            if (dbHighVer < highVer):
                # Remove the extra files from the directory.
                for version in range(highVer, dbHighVer, -1):
                    patchFilename = self.patchVer(persistFilename, version)
                    patchFilename.unlink()
                highVer = dbHighVer
            else:
                # Remove the extra versions from server.ddb.
                self.dldb.setNumVersions(relInstallFilename, highVer)
                dbHighVer = highVer

        # Now walk through all of the patches and make sure they chain
        # end-to-end sensibly, and also that they agree with the
        # versions in the dldb.
        nextHash = None
        for version in range(highVer, 1, -1):
            patchFilename = self.patchVer(persistFilename, version)
            patchFile = Patchfile()
            patchFile.readHeader(patchFilename)

            patchHash = nextHash
            if patchFile.hasSourceHash():
                patchHash = patchFile.getSourceHash()
                if nextHash != None:
                    # Make sure the patch files chain end-to-end
                    # sensibly.
                    if not nextHash.eq(patchHash):
                        self.notify.error("Patch file %s does not follow from %s!" %
                                          (patchFilename.cStr(),
                                           self.patchVer(persistFilename, version + 1).cStr()))

            if patchHash != None:
                dbHash = self.dldb.getHash(relInstallFilename, version)
                if not patchHash.eq(dbHash):
                    self.notify.error("server.ddb version %d for %s disagrees with %s!" %
                                      (version, persistFilename.cStr(), patchFilename.cStr()))


            # We must use a copy constructor here, to force a copy of
            # the HashVal instead of the pointer that getResultHash()
            # would normally return.
            nextHash = HashVal(patchFile.getResultHash())

        if nextHash != None:
            if not nextHash.eq(fileHash):
                self.notify.error("Patch file %s does not lead to %s!" %
                                  (self.patchVer(persistFilename, 2).cStr(),
                                   persistFilename.cStr()))
            dbHash = self.dldb.getHash(relInstallFilename, 1)
            if not fileHash.eq(dbHash):
                self.notify.error("server.ddb version 1 disagrees with %s!" %
                                  (persistFilename.cStr()))

        return highVer

    def parseModule(self, lineList):
        moduleName = lineList[1]
        self.freezer.addModule(moduleName)

    def parseExcludeModule(self, lineList, forbid):
        moduleName = lineList[1]
        self.freezer.excludeModule(moduleName, forbid = forbid)

    def parseDCModule(self, lineList):
        sourceFilename = Filename.expandFrom(lineList[1])

        # First, read in the dc file
        dcFile = DCFile()
        if (not dcFile.read(sourceFilename)):
            self.notify.error("Unable to parse %s." % (sourceFilename.cStr()))

        # Then add all of the .py files imported by the dc file.
        self.addDCImports(dcFile)

    def addDCImports(self, dcFile):

        # This is the list of DC import suffixes that should be
        # available to the client.  Other suffixes, like AI and UD,
        # are server-side only and should be ignored by the Scrubber.
        clientSuffixes = ['OV']

        for n in range(dcFile.getNumImportModules()):
            moduleName = dcFile.getImportModule(n)
            moduleSuffixes = []
            if '/' in moduleName:
                moduleName, suffixes = moduleName.split('/', 1)
                moduleSuffixes = suffixes.split('/')
            self.freezer.addModule(moduleName)

            for suffix in clientSuffixes:
                if suffix in moduleSuffixes:
                    self.freezer.addModule(moduleName + suffix)
                

            for i in range(dcFile.getNumImportSymbols(n)):
                symbolName = dcFile.getImportSymbol(n, i)
                symbolSuffixes = []
                if '/' in symbolName:
                    symbolName, suffixes = symbolName.split('/', 1)
                    symbolSuffixes = suffixes.split('/')
            
                # "from moduleName import symbolName".

                # Maybe this symbol is itself a module; if that's
                # the case, we need to add it to the list also.
                self.freezer.addModule('%s.%s' % (moduleName, symbolName),
                                       implicit = True)
                for suffix in clientSuffixes:
                    if suffix in symbolSuffixes:
                        self.freezer.addModule('%s.%s%s' % (moduleName, symbolName, suffix),
                                               implicit = True)


    def parseFile(self, lineList):
        if len(lineList) > 4 and lineList[4]:
            platforms = lineList[4].split(',')
            if platform not in platforms:
                return
        
        extractFlag = int(lineList[1])
        # The original file we want to install, at its full path
        sourceFilename = Filename.expandFrom(lineList[2])
        sourceFilename.setBinary()
        # self.notify.debug('parseFile: ' + sourceFilename.cStr())

        # It may be ok if the named file does not exist yet.  It might
        # be generated during the whole Scrubber process.  Phase3.pyo,
        # for instance, is one such file.

        # If the original file is a py file, make sure it is compiled first
        if (sourceFilename.getExtension() == 'pyo'):
            pyfile = Filename(sourceFilename)
            pyfile.setExtension('py')
            if pyfile.exists():
                py_compile.compile(pyfile.toOsSpecific(),
                                   sourceFilename.toOsSpecific(),
                                   sourceFilename.getBasename())

        # The relative path where we want to put this file
        dir = Filename.expandFrom(lineList[3])
        # The relative path plus the file name
        basename = Filename(sourceFilename.getBasename())
        relInstallFilename = Filename(dir, basename)
        relInstallFilename.standardize()
        relInstallFilename.setBinary()

        # If we are storing a dc file, strip out the comments and
        # parameter names first, to provide a bit less useful
        # information to inquisitive hackers.
        if (sourceFilename.getExtension() == 'dc'):
            # First, read in the dc file
            dcFile = DCFile()
            if (not dcFile.read(sourceFilename)):
                self.notify.error("Unable to parse %s." % (sourceFilename.cStr()))

            # And then write it back out to a different filename, in
            # brief.  Here we change the filename of the
            # sourceFilename to our generated file.  We do this after
            # we have already assigned relInstallFilename, above, from
            # the original sourceFilename.
            sourceFilename.setExtension('dcb')
            if (not dcFile.write(sourceFilename, 1)):
                self.notify.error("Unable to write %s." % (sourceFilename.cStr()))

            # Adding a dc file implicitly adds all of the .py files
            # imported by the dc file.
            self.addDCImports(dcFile)

        # If we are storing a prc file, sign it and encrypt it.
        if (sourceFilename.getExtension() == 'prc'):
            # Read the config file first
            osFilename = sourceFilename.toOsSpecific()
            temp = open(osFilename, 'r')
            textLines = temp.readlines()
            temp.close()

            # Then write it out again, without the comments
            sourceFilename.setExtension('pre')
            relInstallFilename.setExtension('pre')
            osFilename = sourceFilename.toOsSpecific()
            temp = open(osFilename, 'w')
            for line in textLines:
                # Skip initial whitespace
                c = 0
                while c < len(line) and line[c] in ' \r\n\t':
                    c += 1
                if c < len(line) and line[c] != '#':
                    # Write the line out only if it's not a comment.
                    temp.write(line)
            temp.close()

            # Now sign the file.
            command = 'otp-sign1 -n %s' % (sourceFilename)
            print command
            exitStatus = os.system(command)
            if exitStatus != 0:
                raise 'Command failed: %s' % (command)

            # And now encrypt it in-place.
            temp = open(osFilename, 'r')
            text = temp.read()
            temp.close()
            text = encryptString(text, PRCEncryptionKey.key)
            temp = open(osFilename, 'wb')
            temp.write(text)
            temp.close()
            
        # Should we compress this subfile?
        compressLevel = 0
        if relInstallFilename.getExtension() in compressExtensions or \
           relInstallFilename.getBasename() in compressFiles:
            compressLevel = 6

        # Add the actual file contents to the actual multifile
        if self.currentMfile.addSubfile(relInstallFilename.getFullpath(),
                sourceFilename, compressLevel) == "":
          self.notify.info("warn: %s does not exist!" % (sourceFilename.cStr()))

        # Should we extract this file individually?
        if extractFlag >= 1:
            # Add this file to the current downloadDb
            self.dldb.serverAddFile(self.currentMfname.getFullpath(),
                                    relInstallFilename.getFullpath())

            if extractFlag >= 2:
                # Not only will we extract the file, but we'll also
                # want to hash check it for security and version
                # control.

                # Compute the hash value for the current version file
                newHash = HashVal()
                newHash.hashFile(sourceFilename)
                self.dldb.addVersion(relInstallFilename, newHash, 1)

                # If this is the launcher phase, write an entry to the
                # launcherFileDb

                if (self.currentMfphase == self.launcherPhase):
                    filename = relInstallFilename.cStr()
                    # If this file goes at the toplevel, strip off the toplevel directory token
                    if (filename[0:9] == 'toplevel/'):
                        filename = filename[9:]
                    # Write the file and md5 to the launcherFileDb
                    self.launcherFile.write(filename + ' ' + newHash.asDec() + '\n')

    def parseDirCallback(self, args, dirname, filenames):
        dirnameBase = os.path.split(dirname)[1]
        if dirnameBase == 'CVS':
            # Ignore CVS directories.
            return
        
        # Parse out the args
        installDir, extractFlag = args
        for filename in filenames:
            fullname = dirname + '/' + filename
            fullname = string.replace(fullname, '\\', '/')
            index = dirname.find(installDir)
            if (index < 0):
                self.notify.error("installDir not found in dirname")
            relInstallDir = dirname[index:]
            relInstallDir = string.replace(relInstallDir, '\\', '/')
            if os.path.isfile(fullname):
                self.parseFile(['file', extractFlag, fullname, relInstallDir])

    def parseDir(self):
        # Grab all the files in this dir
        extractFlag = self.lineList[1]
        sourceDir = Filename.expandFrom(self.lineList[2])
        dirName = sourceDir.toOsSpecific()
        installDir = self.lineList[3]
        if os.path.exists(dirName):
            os.path.walk(dirName, self.parseDirCallback, (installDir, extractFlag))
        else:
            self.notify.error("Directory does not exist: %s" % dirName)

    def freezeExe(self, lineList):
        basename = lineList[2]
        mainModule = lineList[3]
        
        self.freezer.setMain(mainModule)
        self.freezer.done()

        target = self.freezer.generateCode(basename)
        self.freezer = FreezeTool.Freezer(previous = self.freezer)

        # Now add the generated file just like any other file, except
        # we do not want to make a copy of it since it is already
        # sitting in the persist dir
        self.parseFile(['file', lineList[1], target, lineList[4]])

    def freezeDll(self, lineList):
        basename = lineList[2]
        
        self.freezer.done()

        target = self.freezer.generateCode(basename)
        self.freezer = FreezeTool.Freezer(previous = self.freezer)

        self.parseFile(['file', lineList[1], target, lineList[3]])

    def closePreviousMfile(self):
        if not cdmode:
            self.notify.info('closePreviousMfile: writing mfile: ' + self.currentMfname.toOsSpecific())

        self.flushIO()
        # Get the mf name out of the mf.pz name
        sourceFilename = Filename(self.mfTempDir,
                                  Filename(self.currentMfname.getBasenameWoExtension()))
        relInstallFilename = Filename(sourceFilename.getBasename())
        persistFilename = Filename(self.persistDir, relInstallFilename)

        persistFilename.setBinary()
        relInstallFilename.setBinary()
        sourceFilename.setBinary()

        # Write the mf to disk
        if not cdmode:
            self.currentMfile.close()

        # Get the MD5 of our new multifile.
        newHash = HashVal()
        newHash.hashFile(sourceFilename)

        highVer = self.patchMFile(sourceFilename, newHash, persistFilename,
                                  relInstallFilename)

##         highVer = self.checkDbIntegrity(relInstallFilename, newHash, highVer,
##                                         persistFilename)

    def installMfile(self, mfname):
        self.flushIO()
        relInstallFilename = Filename(mfname.getBasenameWoExtension())
        persistFilename = Filename(self.persistDir, relInstallFilename)

        relCompressedFilename = self.compFile(relInstallFilename)
        compressedInstallFilename = Filename(self.contentDir, relCompressedFilename)

        absInstallFilename = Filename(self.contentDir, relInstallFilename)
        absInstallFilename.setBinary()

        highVer = self.dldb.getNumVersions(relInstallFilename)
        self.compressFile(persistFilename, compressedInstallFilename)

        # Get the size of the compressed file.
        actualFileSize = compressedInstallFilename.getFileSize()

        # write the file and its size to progress
        self.progressMap[mfname.getBasenameWoExtension()] = actualFileSize

        # Keep a running total of the patch sizes so we do not exceed the
        # size of the actual file
        totalPatchesSize = 0

        # Remember what the last version of patches that is worth
        # downloading before the size of the patches overshadows the
        # size of the actual file
        lastVersion = 1

        # Compress the patch files into the install directory, and
        # compute the size of all the compressed patch files as we go.
        # Also create a list consisting of these filenames and their sizes
        for version in range(2, highVer+1):
            patchFilename = self.patchVer(persistFilename, version)
            compPatchFilename = self.compPatchVer(absInstallFilename, version)
            self.compressFile(patchFilename, compPatchFilename)

            patchSize = compPatchFilename.getFileSize()
            potentialTotal = totalPatchesSize + patchSize
            if (potentialTotal > actualFileSize):
                self.notify.debug('parseFile: Truncating patch list at version: '
                                  + `version` + '\n'
                                  + '    total would have been: ' + `potentialTotal` + '\n'
                                  + '    but entire file is only: ' + `actualFileSize`)
                compPatchFilename.unlink()
                try:
                    del self.progressMap[compPatchFilename.getBasenameWoExtension()]
                except KeyError:
                    pass
                
                # Break out of the for loop
                break
            else:
                # Throw this patch size in the total
                totalPatchesSize = totalPatchesSize + patchSize
                lastVersion = version

            # write the patch file basename and its size to progress
            self.progressMap[patchFilename.getBasename()] = patchSize

        # Remove any versions that we do not need anymore
        for version in range(lastVersion+1, highVer+1):
            self.notify.debug('parseFile: Removing obsolete version: ' + `version`)
            patchFilename = self.patchVer(persistFilename, version)
            patchFilename.unlink()
            try:
                del self.progressMap[patchFilename.getBasename()]
            except KeyError:
                pass
        if lastVersion < highVer:
            self.dldb.setNumVersions(relInstallFilename, lastVersion)

        # Record the hash value and size of the compressed multifile.
        pzHash = HashVal()
        pzHash.hashFile(compressedInstallFilename)
        self.dldb.setServerMultifileHash(mfname.cStr(), pzHash)
        self.dldb.setServerMultifileSize(mfname.cStr(), actualFileSize)

        self.dldb.writeServerDb(self.persistServerDbFilename)

    def bunzipToTemporary(self, filename):
        # Runs bunzip2 on the indicated file, writing the result to a
        # temporary filename, and returns the temporary filename.
        tempFilename = Filename.temporary('', 'Scrub_')
        command = 'bunzip2 <"%s" >"%s"' % (filename.toOsSpecific(), tempFilename.toOsSpecific())
        print command
        exitStatus = os.system(command)
        if exitStatus != 0:
            raise 'Command failed: %s' % (command)

        return tempFilename

    def generatePatch(self, persistFilename, newFilename,
                      newHash, relInstallFilename = 0):
        # This function renames all of the previously existing patch
        # files down one version, generates a new .v2.pch.pz file for
        # the current version, and moves the new filename onto the old
        # install file.

        # Returns the highest version in the directory after completion.

        highVer = self.getHighestVersion(persistFilename)

        # Slide all the patch files up one
        if (highVer >= 2):
            # Count down over the versions
            for version in range(highVer, 1, -1):
                # Move this version up one
                curFile = self.patchVer(persistFilename, version)
                movedName = self.patchVer(persistFilename, version+1)
                self.moveFile(curFile, movedName)

                # Also touch each version so CVS will recognize it has
                # changed.
                movedName.touch()

        self.notify.info('Building patch for %s' % (persistFilename.cStr()))
        self.flushIO()

        if (relInstallFilename):
            # Insert a new version into the database, and slide all the
            # database versions up also.
            self.dldb.insertNewVersion(relInstallFilename, newHash)

            # We'd better write out the server.ddb file now, to make sure
            # it stays in sync with the directory, just in case we get
            # aborted later.
            self.dldb.writeServerDb(self.persistServerDbFilename)

        # Generate the patch from the previous version to the new version.
        patchFilename = self.patchVer(persistFilename, 2)

        # Build the actual patch
        patchFile = Patchfile()
        if not patchFile.build(persistFilename, newFilename, patchFilename):
            self.notify.error("Couldn't generate patch file.")
            
        # Now remove the old file, and move the new file in.
        self.moveFile(newFilename, persistFilename)

        return highVer + 1


    def copyFile(self, fromFilename, toFilename):
        if fromFilename.cStr() != toFilename.cStr():
            self.notify.debug('Copying %s to %s' % (fromFilename.cStr(), toFilename.cStr()))
            shutil.copy(fromFilename.toOsSpecific(), toFilename.toOsSpecific())
            os.system('chmod 644 "%s"' % toFilename.toOsSpecific())

    def moveFile(self, fromFilename, toFilename):
        self.notify.debug('Moving %s to %s' % (fromFilename.cStr(), toFilename.cStr()))
        toFilename.unlink()
        if not fromFilename.renameTo(toFilename):
            self.notify.error('Unable to move %s to %s.' % (fromFilename.cStr(), toFilename.cStr()))
        os.system('chmod 644 "%s"' % toFilename.toOsSpecific())

    def compressFile(self, sourceFilename, destFilename, useBzip2 = 0):
        self.notify.debug('Compressing from %s to %s' % (sourceFilename.cStr(), destFilename.cStr()))
        if useBzip2:
            command = 'bzip2 <"%s" >"%s"' % (sourceFilename.toOsSpecific(),
                                             destFilename.toOsSpecific())
        else:
            command = 'pzip -o "%s" "%s"' % (destFilename.toOsSpecific(),
                                             sourceFilename.toOsSpecific())
        print command
        exitStatus = os.system(command)
        if exitStatus != 0:
            raise 'Command failed: %s' % (command)
        os.system('chmod 644 "%s"' % destFilename.toOsSpecific())

    def installerCopy(self, highVer, fname, fileSize = None, useBzip2 = 0):
        basename = Filename(fname.getBasename())
        self.notify.info('wiseScrubber: Filename is ' + basename.cStr())
        persistFilename = Filename(self.persistDir, basename)
        self.notify.info('wiseScrubber: persistFilename is ' + persistFilename.cStr())
        contentFilename = Filename(self.installDir, basename)
        self.notify.info('wiseScrubber: contentFilename is ' + contentFilename.cStr())

        # Get the size of the compressed file.
        actualFileSize = fileSize
        if actualFileSize == None:
            actualFileSize = contentFilename.getFileSize()
        self.notify.info('actualFileSize = ' + `actualFileSize`)
        # Keep a running total of the patch sizes so we do not exceed the
        # size of the actual file
        totalPatchesSize = 0

        # Remember what the last version of patches that is worth
        # downloading before the size of the patches overshadows the
        # size of the actual file
        lastVersion = 1

        # Copy (or compress) the patch files into the install
        # directory, and compute the size of all the copied patch
        # files as we go.  Also create a list consisting of these
        # filenames and their sizes.
        for version in range(2, highVer+1):
            patchFilename = self.patchVer(persistFilename, version)
            if useBzip2:
                copyPatchFilename = self.compPatchVer(contentFilename, version,
                                                      useBzip2 = True)
                self.compressFile(patchFilename, copyPatchFilename,
                                  useBzip2 = True)
            else:
                copyPatchFilename = self.patchVer(contentFilename, version)
                self.copyFile(patchFilename, copyPatchFilename)

            patchSize = copyPatchFilename.getFileSize()
            potentialTotal = totalPatchesSize + patchSize
            if (version > 15 or potentialTotal > actualFileSize):
                self.notify.debug('wiseScrubber: Truncating patch list at version: '
                                  + `version` + '\n'
                                  + '    total would have been: ' + `potentialTotal` + '\n'
                                  + '    but entire file is only: ' + `actualFileSize`)
                copyPatchFilename.unlink()
                try:
                    del self.progressMap[copyPatchFilename.getBasenameWoExtension()]
                except KeyError:
                    pass
                # Break out of the for loop
                break
            else:
                # Throw this patch size in the total
                totalPatchesSize = totalPatchesSize + patchSize
                lastVersion = version

            # write the patch file basename and its size to progress
            #self.notify.info('progress info '+patchFilename.getBasename()+' '+`patchSize`)
            self.progressMap[patchFilename.getBasename()] = patchSize

        # Remove any versions that we do not need anymore
        for version in range(lastVersion+1, highVer+1):
            self.notify.debug('wiseScrubber: Removing obsolete version: ' + `version`)
            patchFilename = self.patchVer(persistFilename, version)
            patchFilename.unlink()
            try:
                del self.progressMap[patchFilename.getBasename()]
            except KeyError:
                pass

        # Return the last version. Based on that, we have to remove some
        # obsolete hash values from the launcherFileDb.ddb and launcherFileDb
        return lastVersion

    def readDdbHashes(self, filename, newStyle):
        """ Reads the list of previous hashes from the
        installLauncherDb.ddb or bs.ddb file.  Returns the list.  If
        newStyle is true, the .ddb file is expected to include a
        file size reference. """
        
        ddbFile = open(filename.toOsSpecific(), 'r')
        ddbLine = ddbFile.readline()
        ddbFile.close()

        index = ddbLine.find(" ")
        hashes = ''
        if index > 0:
            hashes = ddbLine[index:].strip()

        ddbHashes = []

        hashes = hashes.split(' ')
        if newStyle:
            # We expect a file size as the first parameter.
            hashes = hashes[1:]

        if len(hashes) > 0 and len(hashes[0]) == 32:
            # These should be hexadecimal hashes.
            for hashStr in hashes:
                hash = HashVal()
                if not hash.setFromHex(hashStr):
                    self.notify.error('invalid hash value: ' + hashStr)
                ddbHashes.append(hash)

        else:
            # These should be decimal hashes.
            if len(hashes) % 4 != 0:
                self.notify.error('invalid hash value in line: ' + ddbLine)

            # Collect them up in groups of 4.  These are our hash values.
            for i in range(0, len(hashes), 4):
                hash = HashVal()
                hashStr = ' '.join(hashes[i : i + 4])
                if not hash.setFromDec(hashStr):
                    self.notify.error('invalid hash value: ' + hashStr)
                ddbHashes.append(hash)

        return ddbHashes

    def writeDdbHashes(self, basename, ddbHashes, filename, newStyle, fileSize = None):
        if newStyle:
            ddbLine = '%s %s' % (basename, fileSize)
        else:
            ddbLine = basename

        if newStyle and False:
            for hash in ddbHashes:
                ddbLine += ' ' + hash.asHex()
        else:
            for hash in ddbHashes:
                ddbLine += ' ' + hash.asDec()

        ddbFile = open(filename.toOsSpecific(), 'w')
        ddbFile.write(ddbLine + '\n')
        ddbFile.close()

scrubber = Scrubber()
