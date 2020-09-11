//
// This file controls how to build the Toontown client for publishes.
//

// We want to ship Opt4 for maximum performance and smallness.
#define OPTIMIZE 4
#define DO_MEMORY_USAGE

// On OSX, we need universal binaries.
#define UNIVERSAL_BINARIES 1

// We don't want to build these optional packages.
#define HAVE_TIFF
#define HAVE_PNG
#define HAVE_VRPN
#define HAVE_NSPR
#define WANT_NATIVE_NET
#define HAVE_CG
#define HAVE_OPENCV
#define HAVE_FFMPEG
#define HAVE_MESA
#define HAVE_FMODEX
#define COMPILE_IN_DEFAULT_FONT
#define HAVE_THREADS

// Awesomium for Panda - may never become a requirement
// #define AWESOMIUM_IPATH $[WINTOOLS]/sdk/awesomium/include
// #define AWESOMIUM_LPATH $[WINTOOLS]/sdk/awesomium/lib

// We want to instrument only these specific libraries.
#define GENPYCODE_LIBS libpandaexpress libpanda libpandaphysics libdirect libpandafx libpandaode libotp libtoontown
#define CTA_GENERIC_GENPYCODE


#define PANDA_DISTRIBUTOR Toontown Client

// We need a special set of config options for the client publish.
// These particular options are a stopgap to run Configrc.exe the way
// it has always been run in the old DConfig system; soon we should
// replace Configrc.exe with the new signed prc file system.
#define DEFAULT_PRC_DIR .
#define PRC_DIR_ENVVARS
#define PRC_PATH_ENVVARS
#define PRC_PATTERNS
#define PRC_EXECUTABLE_PATTERNS $[if $[WINDOWS_PLATFORM],Configrc.exe,Configrc]
#define PRC_RESPECT_TRUST_LEVEL

// This is to point libdtool at the public keys file, so the client
// can recognize signed prc files.
#define PRC_PUBLIC_KEYS_FILENAME $[OTP]/src/secure/otp_keys.cxx

#if $[USE_TESTSERVER]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_TESTSERVER
    // use separate build directory for test server
    #define ODIR_SUFFIX -test
#endif

#if $[LANGUAGE]
  #print Configuring $[LANGUAGE] build

  #if $[eq $[LANGUAGE], castillian]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_CASTILLIAN PRODUCT_NAME="_ES"
  #elif $[eq $[LANGUAGE], japanese]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_JAPANESE PRODUCT_NAME="_JP"
  #elif $[eq $[LANGUAGE], german]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_GERMAN PRODUCT_NAME="_DE"
  #elif $[eq $[LANGUAGE], portuguese]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_PORTUGUESE PRODUCT_NAME="_BR"
  #elif $[eq $[LANGUAGE], french]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_FRENCH PRODUCT_NAME="_FR"
  #else
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_ENGLISH PRODUCT_NAME=""
  #endif
#else   // set up defaults
  #print Configuring ENGLISH build
  #define LANGUAGE english
  #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_ENGLISH PRODUCT_NAME=""
#endif


// In the new web plugin world, we will want to have SIMPLE_THREADS
// enabled to support background downloading.
#define HAVE_THREADS 1
#defer SIMPLE_THREADS 1
