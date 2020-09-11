""" This module contains code to freeze a number of Python modules
into a single (mostly) standalone DLL or EXE. """

import modulefinder
import sys
import os
import marshal
import imp

import direct
from pandac.PandaModules import *

ctprojs = os.getenv("CTPROJS")
if not ctprojs:
    print "CTPROJS is not defined."
    sys.exit(1)

# These are modules that Python always tries to import up-front.  They
# must be frozen in any main.exe.
startupModules = [
    'site', 'sitecustomize', 'os', 'encodings.cp1252',
    'org',
    ]

sourceTrees = ['direct', 'otp', 'toontown', 'pirates']
packages = []

if sys.platform == 'win32':
    Python = '$WINTOOLS/sdk/python/Python-2.4.1'
    PythonLib = 'python24'
    MSVS = '/c/Program Files/Microsoft Visual Studio .NET 2003'
elif sys.platform == 'darwin':
    Python = '$OSXTOOLS/src/python'
    PythonIpath = '$OSXTOOLS/built/include/python2.4'
    PythonLpath = '$OSXTOOLS/built/lib'
    PythonLib = 'python2.4_panda'
else:
    Python = '/home/piratepub/player/hack/src/python'
    PythonIpath = '/usr/include/python2.5'
    PythonLpath = '/usr/lib/python2.5'
    PythonLib = 'python2.5'


winCompileObj = 'cl /nologo /c /Fo"%(basename)s.obj" /I"%(python)s\Include" /I"%(python)s\PC" /I"%(msvs)s\Vc7\PlatformSDK\include" /I"%(msvs)s\Vc7\include" /MD /O2 /Ob2 /G6 /GL /Zi /EHsc /Zm500 /W3 %(basename)s.c'
winLinkExe = 'link /nologo /OUT:"%(basename)s.exe" /LIBPATH:"%(msvs)s\Vc7\PlatformSDK\lib" /LIBPATH:"%(msvs)s\Vc7\lib" /LIBPATH:"%(python)s\PCbuild"  /NODEFAULTLIB:LIBCI.LIB /NODEFAULTLIB:MSVCRTD.LIB /NODEFAULTLIB:LIBCMT.LIB /LTCG %(objList)s'
winLinkDll = 'link /nologo /DLL /OUT:"%(basename)s.pyd" /LIBPATH:"%(msvs)s\Vc7\PlatformSDK\lib" /LIBPATH:"%(msvs)s\Vc7\lib" /LIBPATH:"%(python)s\PCbuild"  /NODEFAULTLIB:LIBCI.LIB /NODEFAULTLIB:MSVCRTD.LIB /NODEFAULTLIB:LIBCMT.LIB /LTCG %(objList)s'

osxUniversal = '-arch i386 -arch ppc'
#osxUniversal = ''

osxCompileObj = 'gcc -c %(universal)s -o %(basename)s.o -fPIC -I%(pythonIpath)s %(basename)s.c'
osxLinkExe = 'gcc -u _PyMac_Error %(universal)s -o %(basename)s %(objList)s -L%(pythonLpath)s -l%(pythonLib)s -ldl'
osxLinkDll = 'env MACOSX_DEPLOYMENT_TARGET=10.3 gcc -undefined dynamic_lookup -bundle %(universal)s -o %(basename)s.so %(objList)s'

linuxCompileObj = 'gcc -c -o %(basename)s.o -fPIC -I%(pythonIpath)s %(basename)s.c'
linuxLinkExe = 'gcc -o %(basename)s %(objList)s -L%(pythonLpath)s -l%(pythonLib)s -ldl'
linuxLinkDll = 'gcc -shared -o %(basename)s.so %(objList)s -L%(pythonLpath)s -l%(pythonLib)s -ldl'

mainInitCode = """
%(frozenMainCode)s

int
main(int argc, char **argv) {
  Py_OptimizeFlag++;
  /*Py_VerboseFlag += 2;*/
  PyImport_FrozenModules = _PyImport_FrozenModules;
  return Py_FrozenMain(argc, argv);
}
"""

dllInitCode = """
static PyMethodDef nullMethods[] = {
  {NULL, NULL}
};

%(dllexport)svoid init%(moduleName)s() {
  int count;
  struct _frozen *new_FrozenModules;

  count = 0;
  while (PyImport_FrozenModules[count].name != NULL) {
    ++count;
  }
  new_FrozenModules = (struct _frozen *)malloc((count + %(newcount)s + 1) * sizeof(struct _frozen));
  memcpy(new_FrozenModules, _PyImport_FrozenModules, %(newcount)s * sizeof(struct _frozen));
  memcpy(new_FrozenModules + %(newcount)s, PyImport_FrozenModules, count * sizeof(struct _frozen));
  memset(new_FrozenModules + count + %(newcount)s, 0, sizeof(struct _frozen));

  PyImport_FrozenModules = new_FrozenModules;

  Py_InitModule("%(moduleName)s", nullMethods);
}
"""

ProgramFile = """
#include "Python.h"

%(moduleDefs)s

static struct _frozen _PyImport_FrozenModules[] = {
%(moduleList)s
  {NULL, NULL, 0}
};

%(initCode)s
"""

ExternProgramFile = """
#include "Python.h"

%(moduleDefs)s
"""

# Windows needs this bit.
FrozenExtensions = """

static struct _inittab extensions[] = {
        /* Sentinel */
        {0, 0}
};
extern DL_IMPORT(int) PyImport_ExtendInittab(struct _inittab *newtab);

int PyInitFrozenExtensions()
{
        return PyImport_ExtendInittab(extensions);
}
"""

okMissing = [
    'Carbon.Folder', 'Carbon.Folders', 'HouseGlobals', 'Carbon.File',
    'MacOS', '_emx_link', 'ce', 'mac', 'org.python.core', 'os.path',
    'os2', 'posix', 'pwd', 'readline', 'riscos', 'riscosenviron',
    'riscospath', 'dbm', 'fcntl', 'win32api',
    '_winreg', 'ctypes', 'ctypes.wintypes', 'nt','msvcrt',
    'EasyDialogs', 'SOCKS', 'ic', 'rourl2path', 'termios',
    'OverrideFrom23._Res', 'email', 'email.Utils', 'email.Generator',
    'email.Iterators', '_subprocess', 'gestalt',
    'direct.extensions_native.extensions_darwin',
    ]

def setupPackages():
    # First, get the list of packages, then reverse the list to
    # put it in ctattach order.  (The reversal may not matter too
    # much these days, but let's be as correct as we can be.)
    global packages
    packages = []
    for proj in ctprojs.split():
        projName = proj.split(':')[0]
        moduleName = projName.lower()
        if moduleName in sourceTrees:
            packages.append(moduleName)
    packages.reverse()

    for moduleName in packages:
        str = 'import %s' % (moduleName)
        exec str

        module = sys.modules[moduleName]
        modulefinder.AddPackagePath(moduleName, module.__path__[0])
    

class Freezer:
    # Module tokens:
    MTAuto = 0
    MTInclude = 1
    MTExclude = 2
    MTForbid = 3
    
    def __init__(self, previous = None, debugLevel = 0):
        self.previousModules = {}
        self.modules = {}

        if previous:
            self.previousModules = dict(previous.modules)
            self.modules = dict(previous.modules)
            
        self.mainModule = None
        self.mf = None

    def excludeModule(self, moduleName, forbid = False):
        """ Adds a module to the list of modules not to be exported by
        this tool.  If forbid is true, the module is furthermore
        forbidden to be imported, even if it exists on disk. """
        
        if forbid:
            self.modules[moduleName] = self.MTForbid
        else:
            self.modules[moduleName] = self.MTExclude

    def getModulePath(self, moduleName):
        """ Looks for the indicated directory module and returns its
        __path__ member: the list of directories in which its python
        files can be found.  If the module is a .py file and not a
        directory, returns None. """

        # First, try to import the module directly.  That's the most
        # reliable answer, if it works.
        try:
            module = __import__(moduleName)
        except:
            module = None

        if module != None:
            for symbol in moduleName.split('.')[1:]:
                module = getattr(module, symbol)
            return module.__path__
        
        # If it didn't work--maybe the module is unimportable because
        # it makes certain assumptions about the builtins, or
        # whatever--then just look for file on disk.  That's usually
        # good enough.
        path = None
        baseName = moduleName
        if '.' in baseName:
            parentName, baseName = moduleName.rsplit('.', 1)
            path = self.getModulePath(parentName)
            if path == None:
                return None

        file, pathname, description = imp.find_module(baseName, path)

        if os.path.isdir(pathname):
            return [pathname]
        else:
            return None
            
    def addModule(self, moduleName, implicit = False):
        """ Adds a module to the list of modules to be exported by
        this tool.  If implicit is true, it is OK if the module does
        not actually exist.

        The module name may end in ".*", which means to add all of the
        .py files (other than __init__.py) in a particular directory.
        """

        if implicit:
            token = self.MTAuto
        else:
            token = self.MTInclude

        if moduleName.endswith('.*'):
            # Find the parent module, so we can get its directory.
            parentName = moduleName[:-2]
            path = self.getModulePath(parentName)

            if path == None:
                # It's actually a regular module.
                self.modules[parentName] = token

            else:
                # Now get all the py files in the parent directory.
                for dirname in path:
                    for filename in os.listdir(dirname):
                        if filename.endswith('.py') and filename != '__init__.py':
                            moduleName = '%s.%s' % (parentName, filename[:-3])
                            self.modules[moduleName] = token
        else:
            # A normal, explicit module name.
            self.modules[moduleName] = token

    def setMain(self, moduleName):
        self.addModule(moduleName)
        self.mainModule = moduleName

    def done(self):
        assert self.mf == None

        if self.mainModule:
            # Ensure that each of our required startup modules is
            # on the list.
            for moduleName in startupModules:
                if moduleName not in self.modules:
                    self.modules[moduleName] = self.MTAuto
        
        excludes = []
        includes = []
        autoIncludes = []
        for moduleName, token in self.modules.items():
            if token == self.MTInclude:
                includes.append(moduleName)
            elif token == self.MTAuto:
                autoIncludes.append(moduleName)
            elif token == self.MTExclude or token == self.MTForbid:
                excludes.append(moduleName)

        self.mf = modulefinder.ModuleFinder(excludes = excludes)

        # Attempt to import the explicit modules into the modulefinder.
        for moduleName in includes:
            self.mf.import_hook(moduleName)

        # Also attempt to import any implicit modules.  If any of
        # these fail to import, we don't care.
        for moduleName in autoIncludes:
            try:
                self.mf.import_hook(moduleName)
            except ImportError:
                pass

        # Now, any new modules we found get added to the export list.
        for moduleName in self.mf.modules.keys():
            if moduleName not in self.modules:
                self.modules[moduleName] = self.MTAuto

        missing = []
        for moduleName in self.mf.any_missing():
            if moduleName in startupModules:
                continue
            if moduleName in self.previousModules:
                continue

            # This module is missing.  Let it be missing in the
            # runtime also.
            self.modules[moduleName] = self.MTExclude

            if moduleName in okMissing:
                # If it's listed in okMissing, don't even report it.
                continue

            prefix = moduleName.split('.')[0]
            if prefix not in sourceTrees:
                # If it's in not one of our standard source trees, assume
                # it's some whacky system file we don't need.
                continue
                
            missing.append(moduleName)
                
        if missing:
            error = "There are some missing modules: %r" % missing
            print error
            raise StandardError, error

    def mangleName(self, moduleName):
        return 'M_' + moduleName.replace('.', '__')        

    def generateCode(self, basename):

        # Collect a list of all of the modules we will be explicitly
        # referencing.
        moduleNames = []

        for moduleName, token in self.modules.items():
            prevToken = self.previousModules.get(moduleName, None)
            if token == self.MTInclude or token == self.MTAuto:
                # Include this module (even if a previous pass
                # excluded it).  But don't bother if we exported it
                # previously.
                if prevToken != self.MTInclude and prevToken != self.MTAuto:
                    if moduleName in self.mf.modules or \
                       moduleName in startupModules:
                        moduleNames.append(moduleName)
            elif token == self.MTForbid:
                if prevToken != self.MTForbid:
                    moduleNames.append(moduleName)

        # Build up the replacement pathname table, so we can eliminate
        # the personal information in the frozen pathnames.  The
        # actual filename we put in there is meaningful only for stack
        # traces, so we'll just use the module name.
        replace_paths = []
        for moduleName, module in self.mf.modules.items():
            if module.__code__:
                origPathname = module.__code__.co_filename
                replace_paths.append((origPathname, moduleName))
        self.mf.replace_paths = replace_paths

        # Now that we have built up the replacement mapping, go back
        # through and actually replace the paths.
        for moduleName, module in self.mf.modules.items():
            if module.__code__:
                co = self.mf.replace_paths_in_code(module.__code__)
                module.__code__ = co;

        # Now generate the actual export table.
        moduleNames.sort()

        # Ensure there are no more than a certain number of function
        # definitions per c file.
        maxPerFile = 100
        numSourceFiles = int((len(moduleNames) + maxPerFile - 1) / maxPerFile)
        isStatic = (numSourceFiles <= 1)

        moduleDefs = []
        moduleExterns = []
        moduleList = []

        for moduleName in moduleNames:
            token = self.modules[moduleName]
            if token == self.MTForbid:
                # Explicitly disallow importing this module.
                moduleList.append(self.makeForbiddenModuleListEntry(moduleName))
            else:
                assert token != self.MTExclude
                # Allow importing this module.
                module = self.mf.modules.get(moduleName, None)
                code = getattr(module, "__code__", None)
                if not code and moduleName in startupModules:
                    # Forbid the loading of this startup module.
                    moduleList.append(self.makeForbiddenModuleListEntry(moduleName))
                else:
                    if moduleName in packages:
                        # This is one of our Python source trees.
                        # These are a special case: we don't compile
                        # the __init__.py files within them, since
                        # their only purpose is to munge the __path__
                        # variable anyway.  Instead, we pretend the
                        # __init__.py files are empty.
                        code = compile('', moduleName, 'exec')

                    if code:
                        code = marshal.dumps(code)

                        mangledName = self.mangleName(moduleName)
                        moduleDefs.append(self.makeModuleDef(mangledName, code, isStatic))
                        moduleExterns.append(self.makeModuleExtern(mangledName))
                        moduleList.append(self.makeModuleListEntry(mangledName, code, moduleName, module))
                        if moduleName == self.mainModule:
                            # Add a special entry for __main__.
                            moduleList.append(self.makeModuleListEntry(mangledName, code, '__main__', module))

        if self.mainModule:
            frozenMainCode = self.getFrozenMainCode()
            if sys.platform == 'win32':
                frozenMainCode += self.getFrozenDllMainCode()
            initCode = mainInitCode % {
                'frozenMainCode' : frozenMainCode,
                'programName' : basename,
                }
            if sys.platform == 'win32':
                initCode += FrozenExtensions
                target = basename + '.exe'
            else:
                target = basename

            doCompile = self.compileExe
            
        else:
            dllexport = ''
            if sys.platform == 'win32':
                dllexport = '__declspec(dllexport) '
                target = basename + '.pyd'
            else:
                target = basename + '.so'
                
            initCode = dllInitCode % {
                'dllexport' : dllexport,
                'moduleName' : basename,
                'newcount' : len(moduleList),
                }
            doCompile = self.compileDll

        if isStatic:
            # It all fits into one source file, no problem.

            text = ProgramFile % {
                'moduleDefs' : '\n'.join(moduleDefs),
                'moduleList' : '\n'.join(moduleList),
                'initCode' : initCode,
                }

            filename = basename + '.c'
            file = open(filename, 'w')
            file.write(text)
            file.close()

            doCompile(basename, [basename])

        else:
            # We have to generate multiple source files to keep the
            # size of each individual source file down.

            text = ProgramFile % {
                'moduleDefs' : '\n'.join(moduleExterns),
                'moduleList' : '\n'.join(moduleList),
                'initCode' : initCode,
                }

            filename = basename + '.c'
            file = open(filename, 'w')
            file.write(text)
            file.close()

            sourceList = [basename]
            prevLines = 0
            for i in range(numSourceFiles):
                nextLines = (i + 1) * maxPerFile
                text = ExternProgramFile % {
                    'moduleDefs' : '\n'.join(moduleDefs[prevLines : nextLines]),
                    'initCode' : initCode,
                    }
                prevLines = nextLines

                source = '%s_%s' % (basename, i)
                filename = source + '.c'
                file = open(filename, 'w')
                file.write(text)
                file.close()
                sourceList.append(source)
                
            doCompile(basename, sourceList)

        return target

    def getFrozenMainCode(self):
        """ Reads frozenmain.c from the Python source directory."""

        python = Filename(ExecutionEnvironment.expandString(Python)).toOsSpecific()
        filename = os.path.join(python, 'Python', 'frozenmain.c')
        return open(filename, 'r').read()

    def getFrozenDllMainCode(self):
        """ Reads frozen_dllmain.c from the Python source directory."""

        python = Filename(ExecutionEnvironment.expandString(Python)).toOsSpecific()
        filename = os.path.join(python, 'PC', 'frozen_dllmain.c')
        return open(filename, 'r').read()

    def compileExe(self, basename, sourceList):
        if sys.platform == 'win32':
            msvs = Filename(ExecutionEnvironment.expandString(MSVS)).toOsSpecific()
            python = Filename(ExecutionEnvironment.expandString(Python)).toOsSpecific()
            compileList = []
            objList = []
            for source in sourceList:
                compile = winCompileObj % {
                    'python' : python,
                    'msvs' : msvs,
                    'basename' : source,
                    }
                compileList.append(compile)
                objList.append(source + '.obj')
                
            link = winLinkExe % {
                'python' : python,
                'pythonLib' : PythonLib,
                'msvs' : msvs,
                'objList' : ' '.join(objList),
                'basename' : basename,
                }
        elif sys.platform == 'darwin':
            pythonIpath = Filename(ExecutionEnvironment.expandString(PythonIpath)).toOsSpecific()
            pythonLpath = Filename(ExecutionEnvironment.expandString(PythonLpath)).toOsSpecific()
            compileList = []
            objList = []
            for source in sourceList:
                compile = osxCompileObj % {
                    'universal' : osxUniversal,
                    'basename' : source,
                    'pythonIpath' : pythonIpath,
                    }
                compileList.append(compile)
                objList.append(source + '.o')
            link = osxLinkExe % {
                'universal' : osxUniversal,
                'objList' : ' '.join(objList),
                'basename' : basename,
                'pythonLpath' : pythonLpath,
                'pythonLib' : PythonLib,
                }
	else:
	    pythonIpath = Filename(ExecutionEnvironment.expandString(PythonIpath)).toOsSpecific()
            pythonLpath = Filename(ExecutionEnvironment.expandString(PythonLpath)).toOsSpecific()
            compileList = []
            objList = []
            for source in sourceList:
                compile = linuxCompileObj % {
                    'basename' : source,
                    'pythonIpath' : pythonIpath,
                    }
                compileList.append(compile)
                objList.append(source + '.o')

            link = linuxLinkExe % {
                'objList' : ' '.join(objList),
                'basename' : basename,
                'pythonLpath' : pythonLpath,
                'pythonLib' : PythonLib,
                }


        for compile in compileList:
            print compile
            if os.system(compile) != 0:
                raise StandardError

        print link
        if os.system(link) != 0:
            raise StandardError

    def compileDll(self, basename, sourceList):
        if sys.platform == 'win32':
            msvs = Filename(ExecutionEnvironment.expandString(MSVS)).toOsSpecific()
            python = Filename(ExecutionEnvironment.expandString(Python)).toOsSpecific()
            compileList = []
            objList = []
            for source in sourceList:
                compile = winCompileObj % {
                    'python' : python,
                    'msvs' : msvs,
                    'basename' : source,
                    }
                compileList.append(compile)
                objList.append(source + '.obj')

            link = winLinkDll % {
                'python' : python,
                'pythonLib' : PythonLib,
                'msvs' : msvs,
                'objList' : ' '.join(objList),
                'basename' : basename,
                }
        elif sys.platform == 'darwin':
            pythonIpath = Filename(ExecutionEnvironment.expandString(PythonIpath)).toOsSpecific()
            compileList = []
            objList = []
            for source in sourceList:
                compile = osxCompileObj % {
                    'universal' : osxUniversal,
                    'basename' : source,
                    'pythonIpath' : pythonIpath,
                    }
                compileList.append(compile)
                objList.append(source + '.o')
            link = osxLinkDll % {
                'universal' : osxUniversal,
                'objList' : ' '.join(objList),
                'basename' : basename,
                }
	else:
            pythonIpath = Filename(ExecutionEnvironment.expandString(PythonIpath)).toOsSpecific()
            compileList = []
            objList = []
            for source in sourceList:
                compile = linuxCompileObj % {
                    'basename' : source,
                    'pythonIpath' : pythonIpath,
                    }
                compileList.append(compile)
                objList.append(source + '.o')

            link = linuxLinkDll % {
                'objList' : ' '.join(objList),
                'basename' : basename,
		'pythonLpath':  PythonLpath,
		'pythonLib' : PythonLib,
                }


        for compile in compileList:
            print compile
            if os.system(compile) != 0:
                raise StandardError

        print link
        if os.system(link) != 0:
            raise StandardError

    def makeModuleDef(self, mangledName, code, isStatic):
        result = ''
        if isStatic:
            result += 'static '
        result += 'unsigned char %s[] = {' % (mangledName)
        for i in range(0, len(code), 16):
            result += '\n  '
            for c in code[i:i+16]:
                result += ('%d,' % ord(c))
        result += '\n};\n'
        return result

    def makeModuleExtern(self, mangledName):
        result = 'extern unsigned char %s[];' % (mangledName)
        return result

    def makeModuleListEntry(self, mangledName, code, moduleName, module):
        size = len(code)
        if getattr(module, "__path__", None):
            # Indicate package by negative size
            size = -size
        return '  {"%s", %s, %s},' % (moduleName, mangledName, size)

    def makeForbiddenModuleListEntry(self, moduleName):
        return '  {"%s", NULL, 0},' % (moduleName)
    
setupPackages()
