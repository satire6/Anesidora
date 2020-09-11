#define BUILD_TYPE unix

#if $[< $[shell gcc -dumpversion], 3]	// redhat7.2 doesn't use gcc3
  #define OPTIMIZE 1
  #define HAVE_WSTRING
#else
  // Use opt 3 when we have redhat 8 running
  #define OPTIMIZE 3
#endif

// use cached distributed compiles
#if $[eq $[shell uname -i], x86_64]
  #define CC x86_64-redhat-linux-gcc
  #define CXX x86_64-redhat-linux-g++
#else
  #define CC ccache distcc i386-redhat-linux-gcc
  #define CXX ccache distcc i386-redhat-linux-g++
#endif

// python 2.4
#define PYTHON_COMMAND python2.4
#define PYTHON_IPATH /usr/local/include/python2.4
#define PYTHON_LPATH /usr/local/lib/python2.4
#define INSTALL_PYTHON_SOURCE

// The latest version of Panda comes with this alternative malloc
// utility, which appears to cause problems on Linux in certain
// contexts.  Turn it off.
#define ALTERNATIVE_MALLOC

// defining HAVE_GETOPT_LONG_ONLY to empty so panda will use
// our own gnu_getopt.h ** COMMENTED OUT FOR NOW *** - dlo
//#define HAVE_GETOPT_LONG_ONLY

// These lines enable building with Mesa, in case that package is
// actually installed.  This is necessary for the TopToonPics program.
#define MESA_IPATH /usr/local/include
#define MESA_LPATH /usr/local/lib
#define MESA_LIBS OSMesa
#define MESA_MGL 1
#define MIN_MESA_VERSION 1 3

// Need libjpeg to write jpeg images
// required for Top Toons head shot rendering
#define JPEG_IPATH
#define JPEG_LPATH /usr/lib64

// Need PNG support for new Top Toons head shot rendering
#define PNG_IPATH
#define PNG_LPATH /usr/lib64

// Need fftw for Top Toons headshot rendering
#define FFTW_IPATH
#define FFTW_LPATH /usr/lib64


#define INSTALL_DIR $[PLAYER]/install

// Ensure no environment variables pollute the build scripts.
#define CTPROJS
#define DTOOL
#define PANDA
#define DIRECT
#define OTP
#define TOONTOWN

#define PANDA_DISTRIBUTOR Toontown Server

#define GENPYCODE_LIBS libpandaexpress libpanda libpandaode libpandaphysics libdirect libotp libtoontown

#if $[eq $[shell uname -i], x86_64]
  #define OPTFLAGS -Os -march=opteron -mmmx -msse -mfpmath=sse -fomit-frame-pointer -finline-functions -frename-registers -pipe
#else
  #define OPTFLAGS -Os -march=pentium3 -mmmx -msse -mfpmath=sse -fomit-frame-pointer -finline-functions -frename-registers -pipe
#endif

// temp for drose
//#define PYTHON_IPATH /usr/include/python2.2
//#define PYTHON_LPATH

// NSPR is no longer needed
//#define NSPR_IPATH $[wildcard /usr/include/nspr*]
//#define NSPR_LPATH /usr/lib
//#define NSPR_LIBS nspr4
//#defer HAVE_NSPR $[libtest $[NSPR_LPATH],$[NSPR_LIBS]]

//#if $[not $[HAVE_NSPR]]
//    #error Please install NSPR!
//#endif

#if $[eq $[shell uname -i], x86_64]
  // Is OpenSSL installed, and where?
  #define OPENSSL_IPATH /usr/include/openssl
  #define OPENSSL_LPATH /usr/lib64
  #define OPENSSL_LIBS ssl crypto
  #defer HAVE_OPENSSL $[libtest $[OPENSSL_LPATH],$[OPENSSL_LIBS]]
  // Redefine this to empty if your version of OpenSSL is prior to 0.9.7.
  #define OPENSSL_097 1
#endif

// Is ODE installed, and where?
#if $[eq $[shell uname -i], x86_64]
  #define ODE_IPATH /usr/include
  #define ODE_LPATH /usr/lib64
#else
  #define ODE_IPATH /usr/local/include
  #define ODE_LPATH /usr/local/lib
#endif
#define ODE_LIBS ode
#defer HAVE_ODE $[libtest $[ODE_LPATH],$[ODE_LIBS]]

#if $[eq $[shell uname -i], x86_64]
  // Is ZLIB installed, and where?
  #define ZLIB_IPATH /usr/include
  #define ZLIB_LPATH /usr/lib64
  #define ZLIB_LIBS z
  #defer HAVE_ZLIB $[libtest $[ZLIB_LPATH],$[ZLIB_LIBS]]
#endif

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
