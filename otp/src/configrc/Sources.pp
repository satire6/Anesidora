#define BUILD_DIRECTORY $[HAVE_OPENSSL]

#define OTHER_LIBS \
    dtoolutil:c dtoolbase:c dtool:m

#define WIN_SYS_LIBS advapi32.lib user32.lib gdi32.lib
#define USE_PACKAGES openssl

#begin lib_target
  #define TARGET settings
  #define SOURCES settingsFile.h settingsFile.cxx
  #define IGATESCAN settingsFile.h
#end lib_target

#if $[USE_TESTSERVER]
    #print Configuring Configrc.exe build for test server
#endif

#if $[and $[ne $[LANGUAGE],], $[ne $[LANGUAGE], english]]
  #print Configuring $[LANGUAGE] Configrc.exe build for server
  #define ODIR_SUFFIX $[ODIR_SUFFIX]-$[LANGUAGE]
  // This is also defined in $TOONTOWN/src/publish/client-build-Config.pp.
  // But this is probably a better place to put it, so we can successfully
  // compile this file in OPT3 for development purposes.
  #define EXTRA_CDEFS $[EXTRA_CDEFS] USE_$[upcase $[LANGUAGE]]
#else
  #print Defaulting to ENGLISH Configrc.exe build for server
  #define EXTRA_CDEFS $[EXTRA_CDEFS] USE_ENGLISH
#endif

// FIX early evaluation flaw with DTOOLS
#defer ODIR Opt$[OPTIMIZE]-$[PLATFORM]$[ODIR_SUFFIX]

#begin bin_target

  #define OTHER_LIBS $[OTHER_LIBS] pystub

#if $[or $[eq $[PLATFORM], Cygwin], $[eq $[PLATFORM],Win32]]
// UPX writes 'UPX' in the exe, but it's better than nothing until I can find a better encrypter
// test_pfstream Configrc.exe -stdout works, so should work in publish
  #define bin_postprocess_cmd upx
  #define bin_postprocess_arg1 --force   // upx bombs on vc7.1 .exes w/o this
  #define bin_postprocess_arg2 -o
  #define bin_postprocess_target Configrc
  #define TARGET Configrc_u
#else
  #define TARGET Configrc
#endif

  #define SOURCES Configrc.cxx settingsFile.cxx key_src.cxx \
     serialization.h serialization.I
#end bin_target
