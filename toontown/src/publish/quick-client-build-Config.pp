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

// Awesomium for Panda - which may never become a requirement
// #define AWESOMIUM_IPATH $[WINTOOLS]/sdk/awesomium/include
// #define AWESOMIUM_LPATH $[WINTOOLS]/sdk/awesomium/lib

// We want to instrument only these specific libraries.
#define GENPYCODE_LIBS libpandaexpress libpanda libpandaphysics libdirect libpandafx libpandaode libotp libtoontown
#define CTA_GENERIC_GENPYCODE


#define PANDA_DISTRIBUTOR Toontown Client

// We need a special set of config options for the client publish.
// These options insist that every .prc file be signed, and also
// allows the client to read encrypted prc files (Config.pre).
#define PRC_EXECUTABLE_PATTERNS
#define DEFAULT_PRC_DIR .
#define PRC_PATH_ENVVARS PRC_PATH
#define PRC_DIR_ENVVARS
#define PRC_PATTERNS *.prc
#define PRC_ENCRYPTED_PATTERNS *.pre
#define PRC_RESPECT_TRUST_LEVEL 1
#define PRC_INC_TRUST_LEVEL 1

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
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_CASTILLIAN PRODUCT_NAME="_Terra-DMC"
  #elif $[eq $[LANGUAGE], japanese]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_JAPANESE PRODUCT_NAME="_JP"
  #elif $[eq $[LANGUAGE], german]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_GERMAN PRODUCT_NAME="_T-Online"
  #elif $[eq $[LANGUAGE], portuguese]
    #defer EXTRA_CDEFS $[EXTRA_CDEFS] USE_PORTUGUESE PRODUCT_NAME="_Terra"
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

// For the p3d (web plugin) build, we need to specify a version string
// for this Panda build.  This is different from the server-version,
// and doesn't change with each new Toontown release; the point is just
// to differentiate this Panda build from, say, the Pirates Panda
// build, or a panda build intended for any other purpose.
#define PANDA_PACKAGE_VERSION toontown

// We also need to specify the host string.  This is the official URL
// that hosts the downloadable contents.  It's not necessarily the
// site that the contents will actually be downloaded from (because we
// have the clients go through Akamai instead), but this URL is the
// formal authority on what the downloaded bits *should* be.
// #define PANDA_PACKAGE_HOST_URL http://download.toontown.com/english/inbrowser
#define PANDA_PACKAGE_HOST_URL http://download.toontown.com/english/inbrowser

// Provides the handy ppackage shell script, so we don't have to run
// this program out of the direct source tree.
#define BUILD_P3D_SCRIPTS ppackage
