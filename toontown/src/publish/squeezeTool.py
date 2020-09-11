#!/usr/bin/env python
#
# SQUEEZE
#
# squeeze a python program 
#
# installation:
# - use this script as is, or squeeze it using the following command:
# 
# python squeezeTool.py -1su -o squeeze -b squeezeTool squeezeTool.py
#
# notes:
# - this is pretty messy.  make sure to test everything carefully
#   if you change anything
#
# - the name "squeeze" is taken from an ABC800 utility which did
#   about the same thing with Basic II bytecodes.
#
# history:
# 1.0   97-04-22 fl     Created
# 1.1   97-05-25 fl     Added base64 embedding option (-1)
#       97-05-25 fl     Check for broken package file
# 1.2   97-05-26 fl     Support uncompressed packages (-u)
# 1.3   97-05-27 fl     Check byte code magic, eliminated StringIO, etc.
# 1.4   97-06-04 fl     Removed last bits of white space, removed try/except
# 1.5   97-06-17 fl     Added squeeze archive capabilities (-x)
# 1.6   98-05-04 fl     Minor fixes in preparation for public source release
#
# 1.6d  04-06-01 drose  Extended to support dotted module names.
#
# reviews:
#       "Fredrik Lundh is a friggin genius"
#       -- Aaron Watters, author of 'Internet Programming with Python'
#
#       "I agree ... this is a friggin Good Thing"
#       -- Paul Everitt, Digital Creations
#
# Copyright (c) 1997 by Fredrik Lundh.
# Copyright (c) 1997-1998 by Secret Labs AB
#
# info@pythonware.com
# http://www.pythonware.com
#
# --------------------------------------------------------------------
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted.  This software is provided as is.
# --------------------------------------------------------------------

VERSION = "1.6d/04-06-01"
MAGIC   = "[TTSQUEEZE]"

import base64, imp, marshal, os, string, sys, md5

# --------------------------------------------------------------------
# usage

def usage():
    print
    print "SQUEEZE", VERSION, "(c) 1997-1998 by Secret Labs AB"
    print """\
Convert a Python application to a compressed module package.

Usage: squeeze [-1ux] -o app [-b start] modules... [-d files...]

This utility creates a compressed package file named "app.pyz", which
contains the given module files.  It also creates a bootstrap script
named "app.py", which loads the package and imports the given "start"
module to get things going.  Example:

        squeeze -o app -b appMain app*.py

The -1 option tells squeeze to put the package file inside the boot-
strap script using base64 encoding.  The result is a single text file
containing the full application.

The -u option disables compression.  Otherwise, the package will be
compressed using zlib, and the user needs zlib to run the resulting
application.

The -d option can be used to put additional files in the package file.
You can access these files via "__main__.open(filename)" (returns a
StringIO file object).

The -x option can be used with -d to create a self-extracting archive,
instead of a package.  When the resulting script is executed, the
data files are extracted.  Omit the -b option in this case.
"""
    sys.exit(1)


# --------------------------------------------------------------------
# squeezer -- collect squeezed modules

class Squeezer:

    def __init__(self, archiveid):

        self.archiveid = archiveid
        self.rawbytes = self.bytes = 0
        self.modules = {}

    def addmodule(self, file, moduleName):
        if file[-1] == "c":
            file = file[:-1]

        # read sourcefile
        path = None
        if os.path.isdir(file):
            init = os.path.join(file, '__init__.py')
            if not os.path.exists(init):
                # Directories without __init__.py are quietly ignored,
                # just like the standard Python importer.
                return

            # Recursively compile all files within the directory.
            for subfile in os.listdir(file):
                base, ext = os.path.splitext(subfile)
                if ext == '.py':
                    self.addmodule(os.path.join(file, subfile),
                                   '%s.%s' % (moduleName, base))
            return

        basename = os.path.split(file)[-1]
        dot = moduleName.rfind('.')
        if dot != -1 and moduleName[dot + 1:] == '__init__':
            # Compile __init__.py as the directory name itself.
            moduleName = moduleName[:dot]
            path = moduleName

        f = open(file)
        codestring = f.read()
        f.close()

        if path:
            codestring = "__path__ = ['%s']\n%s" % (path, codestring)

        try:
            module = compile(codestring, basename, "exec")
        except:
            print ":: There's an error preventing compiling in " + file
            raise
            #sys.exit(1)

        self.modules[moduleName] = module

        # Make sure the prefixes of the moduleName can be found in the
        # dictionary also.
        modulePath = moduleName.split('.')
        for i in range(len(modulePath)):
            prefix = '.'.join(modulePath[:i + 1])
            if not self.modules.has_key(prefix):
                self.modules[prefix] = None
        
    def adddata(self, file):

        self.modules["+"+file] = open(file, "rb").read()

    def getarchive(self):

        # marshal our module dictionary
        data = marshal.dumps((self.archiveid, self.modules))
        self.rawbytes = len(data)

        # return (compressed) dictionary
        data = zlib.compress(data, 9)
        self.bytes = len(data)

        return data

    def getstatus(self):
        return self.bytes, self.rawbytes


# --------------------------------------------------------------------
# loader (used in bootstrap code)

loader = """
print "Beginning squeezetool loader"
import ihooks
import types

PYZ_MODULE = 64

class Loader(ihooks.ModuleLoader):

    def __init__(self, archiveid, modules):
        self.archiveid = archiveid
        self.__modules = modules
        return ihooks.ModuleLoader.__init__(self)

    def find_module(self, name, path = None):
        #print "%%s: find '%%s' on %%s" %% (self.archiveid, name, path)
        if path != None:
            for dirname in path:
                moduleName = dirname + '.' + name
                if self.__modules.has_key(moduleName):
                    #print "%%s: found as %%s" %% (self.archiveid, moduleName)
                    return None, moduleName, (None, None, PYZ_MODULE)
        else:
            if self.__modules.has_key(name):
                #print "%%s: found as %%s" %% (self.archiveid, name)
                return None, name, (None, None, PYZ_MODULE)

        return ihooks.ModuleLoader.find_module(self, name, path)

    def load_module(self, name, stuff):
        file, filename, (suff, mode, type) = stuff
        if type != PYZ_MODULE:
            return ihooks.ModuleLoader.load_module(self, name, stuff)
        #print "%%s: load_module %%s" %% (self.archiveid, filename)
        code = self.__modules[filename]
        del self.__modules[filename] # no need to keep this one around
        m = self.hooks.add_module(name)
        m.__file__ = filename
        if code:
            exec code in m.__dict__
        else:
            m.__path__ = [filename]

        return m

def boot(name, fp, size, offset = 0):

    global data

    try:
        import %(modules)s
    except ImportError:
        print "PYZ:", "failed to load marshal and zlib libraries"
        return # cannot boot from PYZ file
    #print "PYZ:", "boot from", name+".PYZ"

    # load archive and install import hook
    if offset:
        data = fp[offset:]
    else:
        data = fp.read(size)
        fp.close()

    if len(data) != size:
        raise IOError, "package is truncated"

    data = marshal.loads(%(data)s)

    ihooks.install(ihooks.ModuleImporter(Loader(*data)))
"""

loaderopen = """

def open(name):
    import StringIO
    try:
        return StringIO.StringIO(data["+"+name])
    except KeyError:
        raise IOError, (0, "no such file")
"""

loaderexplode = """

def explode():
    for k, v in data.items():
        if k[0] == "+":
            try:
                open(k[1:], "wb").write(v)
                print k[1:], "extracted ok"
            except IOError, v:
                print k[1:], "failed:", "IOError", v

"""

def getloader(data, package):

    s = loader

    if data:
        if explode:
            s = s + loaderexplode
        else:
            s = s + loaderopen

    dict = {
        "modules": "marshal, zlib",
        "data":    "zlib.decompress(data)",
        }

    s = s % dict

    return marshal.dumps(compile(s, "<package>", "exec"))


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

#
# parse options

import getopt, glob, sys
import zlib

embed = 0
explode = 0

def squeeze(app, start, filelist):
    localMagic = MAGIC
    data = None

    bootstrap = app + ".py"
    archive   = app + ".pyz"

    archiveid = app

    #
    # avoid overwriting files not generated by squeeze

    try:
        fp = open(bootstrap)
        s = fp.readline()
        string.index(s, MAGIC)
    except IOError:
        pass
    except ValueError:
        print bootstrap, "was not created by squeeze.  You have to manually"
        print "remove the file to proceed."
        sys.exit(1)

    #
    # collect modules

    sq = Squeezer(archiveid)
    for file, moduleName in filelist:
        # print 'addmodule:', file, moduleName
        sq.addmodule(file, moduleName)

    package = sq.getarchive()
    size = len(package)

    #
    # get loader

    loader = getloader(data, package)

    zbegin, zend = "zlib.decompress(", ")"
    loader = zlib.compress(loader, 9)

    loaderlen = len(loader)

    magic = repr(imp.get_magic())
    version = string.split(sys.version)[0]

    #
    # generate script and package files

    if embed:

        # embedded archive
        data = base64.encodestring(loader + package)

        fp = open(bootstrap, "w")
        fp.write('''\
#%(localMagic)s %(archiveid)s
import ihooks,zlib,base64,marshal
s=base64.decodestring("""
%(data)s""")
exec marshal.loads(%(zbegin)ss[:%(loaderlen)d]%(zend)s)
boot("%(app)s",s,%(size)d,%(loaderlen)d)
exec "import %(start)s"
''' % locals())
        bytes = fp.tell()

    else:

        # separate archive file

        fp = open(archive, "wb")

        fp.write(loader)
        fp.write(package)

        bytes = fp.tell()
        fp.close()
        #
        # create bootstrap code

        fp = open(bootstrap, "w")
        fp.write("""\
#%(localMagic)s %(archiveid)s
import ihooks,zlib,marshal
f=open("%(archive)s","rb")
exec marshal.loads(%(zbegin)sf.read(%(loaderlen)d)%(zend)s)
boot("%(app)s",f,%(size)d)
exec "import %(start)s"
""" % locals())
        bytes = bytes + fp.tell()
        fp.close()

    #
    # show statistics

    dummy, rawbytes = sq.getstatus()

    print "squeezed", rawbytes, "to", bytes, "bytes",
    print "(%d%%)" % (bytes * 100 / rawbytes)
