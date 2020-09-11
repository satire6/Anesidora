// Only build this directory if the user has set the variable
// WANT_INSTALLER.  Most people don't need to build this, and it
// causes headaches some of the time.
#define BUILD_DIRECTORY $[and $[WANT_INSTALLER],$[WINDOWS_PLATFORM]]

#if $[USE_TESTSERVER]
    #print Configuring Toontown ActiveX Installer build for TEST server
    #define INSTALLER_TARGETNAME tt_test
    #define HDRGEN_SERVER_TGT test
#else
    #print Configuring Toontown ActiveX Installer build for LIVE server
    #define INSTALLER_TARGETNAME ttinst
    #define HDRGEN_SERVER_TGT release
#endif

#if $[eq $[LANGUAGE],]
  #define LANGUAGE english
#endif

#if $[ne $[LANGUAGE], english]
  #define ODIR_SUFFIX $[ODIR_SUFFIX]-$[LANGUAGE]
  #define INSTALLER_TARGETNAME $[INSTALLER_TARGETNAME]-$[LANGUAGE]
  #print Configuring $[LANGUAGE] ActiveX build
#else
  #print Configuring ENGLISH ActiveX build
#endif

#define USE_SINGLE_COMPOSITE_SOURCEFILE   // defined to NULL since winhttp, dx8 cxx's must be built separately
#define DONT_USE_PANDA_DLL_NAMING 1

#define USE_PACKAGES openssl zlib dx9 native_net

#define WIN_SYS_LIBS wininet.lib version.lib winmm.lib

#define LINK_FORCE_STATIC_RELEASE_C_RUNTIME 1
#define OPT_MINSIZE 1
// get rid of _DEBUG for Opt1/2, we dont want to build ATL with _DEBUG since assumes link to debug c runtime
#define NO_DEBUG_CDEF 1

#define LIBBASENAME installer
#define IDL_BASENAME $[LIBBASENAME]
#define RC_BASENAME $[LIBBASENAME]

// want these to be NULL!!!
//#define HAVE_PYTHON   // why dont these do anything??
//#define HAVE_NSPR
#define dllext
#define DEBUG_D
#define DLLBASEARG

// no nspr, python in alt_libs in Global.pp
#define IGNORE_LIB_DEFAULTS_HACK 1

#defer SOURCES \
    cpudetect.c \
    fileDB.cxx  \
    installerApplyPatch.cxx  \
    installerBase.cxx  \
    installerDecompress.cxx  \
    installerFilename.cxx  \
    installerHTTP.cxx  \
    installer_md5.cxx  \
    log.cxx  \
    urlencode.cxx \
    sysinfo_dx9.cxx  \
    sysinfo_ogl.cxx  \
    sysinfo_dx8.cxx  \
    sysinfo.cxx  \
    winhttp.cxx  \
    ie_proxy.cxx  \
    toontownInstaller.cxx \
    StdAfx.cpp \
    installerCtrl.cpp \
    installer.cpp \
    resource.h StdAfx.h installerCtrl.h \
    registry.cxx registry.h \
    toontownInstaller.h \
    cpudetect.h installerBase.h  installerHTTP.h  pragma.h \
    fileDB.h installerDecompress.h  installer_md5.h  sysinfo.h sysinfodefs.h \
    installerApplyPatch.h installerFilename.h log.h \
    strl.cxx strl.h \
    $[GENERATED_SOURCES]

#defer GENERATED_SOURCES \
    $[ODIR]/$[LIBBASENAME].rgs \
    $[ODIR]/$[LIBBASENAME].rc \
    $[ODIR]/$[LIBBASENAME].res \
    $[ODIR]/$[LIBBASENAME].idl \
    $[IDL_GENERATED_SOURCES] \
    $[GENERATED_VERHEADER]


#defer COMPILED_RESOURCES $[ODIR]/$[LIBBASENAME].res

#defer EXTRA_CDEFS _WINDOWS _USRDLL _MBCS _ATL_STATIC_REGISTRY _WINDLL $[EXTRA_CDEFS]
#defer END_CFLAGS $[END_CFLAGS] /GF /Gy /I$[ODIR]

//#defer EXTRA_INCPATH $[ODIR] $[OPENSSL_IPATH] $[ZLIB_IPATH] $[DX_IPATH] $[WIN32_PLATFORMSDK_INCPATH] $[EXTRA_INCPATH]
//#defer EXTRA_LIBPATH $[OPENSSL_LPATH] $[ZLIB_LPATH] $[DX_LPATH] $[WIN32_PLATFORMSDK_LIBPATH] $[EXTRA_LIBPATH]
#defer EXTRA_INCPATH $[ODIR] $[OPENSSL_IPATH] $[ZLIB_IPATH] $[DX_IPATH] $[EXTRA_INCPATH] $[VC7_ROOT]/Vc7/atlmfc/include
#defer EXTRA_LIBPATH $[OPENSSL_LPATH] $[ZLIB_LPATH] $[DX_LPATH] $[EXTRA_LIBPATH] $[VC7_ROOT]/Vc7/atlmfc/lib

#defer GENERATED_RC_DEPENDENCIES  $[LIBBASENAME]_template.rc version.txt hdrgen.pl toontown.ico minnie.ico \
                                  $[ODIR]/$[LIBBASENAME].tlb $[ODIR]/$[LIBBASENAME].rgs
#defer GENERATED_INF_DEPENDENCIES $[LIBBASENAME]_template.inf version.txt hdrgen.pl
#defer GENERATED_RGS_DEPENDENCIES $[LIBBASENAME]_template.rgs hdrgen.pl
#defer GENERATED_IDL_DEPENDENCIES $[LIBBASENAME]_template.idl hdrgen.pl

#defer GENERATED_VERHEADER $[ODIR]/$[LIBBASENAME]Version.h
#defer GENERATED_VERHEADER_DEPENDENCIES $[LIBBASENAME]Version_template.h version.txt hdrgen.pl

// ugly hack, but ppremake ignores non-existent generated .h otherwise
#defer VERHEADER_DEPENDENTS $[ODIR]/$[INSTALLER_TARGETNAME]_installerBase.obj

// pp.dep incorrectly assumes installer.h is in the main dir, not ODIR, so use this hack to tell template
// to explictly add installer.h to the dependencies of these files
#defer GENERATED_IDL_H_DEPENDENTS installer.cpp installerCtrl.cpp StdAfx.h

#defer IDL_GENERATED_SOURCES $[ODIR]/$[LIBBASENAME].h $[ODIR]/$[LIBBASENAME].tlb

#defer RC_GENERATOR_RULE  perl hdrgen.pl $[HDRGEN_SERVER_TGT] rc $[ODIR] $[LANGUAGE]
#defer INF_GENERATOR_RULE perl hdrgen.pl $[HDRGEN_SERVER_TGT] inf $[ODIR] $[LANGUAGE]
#defer IDL_GENERATOR_RULE perl hdrgen.pl $[HDRGEN_SERVER_TGT] idl $[ODIR] $[LANGUAGE]
#defer RGS_GENERATOR_RULE perl hdrgen.pl $[HDRGEN_SERVER_TGT] rgs $[ODIR] $[LANGUAGE]
#defer VERHEADER_GENERATOR_RULE perl hdrgen.pl $[HDRGEN_SERVER_TGT] ver_h $[ODIR] $[LANGUAGE]

#define LINKER_DEF_FILE ttinst.def

#begin noinst_lib_target
#define TARGET $[INSTALLER_TARGETNAME]

// want .inf to match dll name, since it will exist in user dir
#defer INSTALLER_INF $[ODIR]/$[INSTALLER_TARGETNAME].inf
#defer GENERATED_SOURCES $[INSTALLER_INF] $[GENERATED_SOURCES]
#defer GENERATED_RC_DEPENDENCIES  $[INSTALLER_INF] $[GENERATED_RC_DEPENDENCIES]
#end noinst_lib_target

// separate tgt in same makefile doesnt work, ODIR is set to 1 thing and test/non-test rules conflict
//#begin test_lib_target
//#defer ODIR $[ODIR]-test
//#define TARGET tt_test
//#define HDRGEN_SERVER_TGT test
//#end test_lib_target

