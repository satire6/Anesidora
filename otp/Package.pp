//
// Package.pp
//
// This file defines certain configuration variables that are to be
// written into the various make scripts.  It is processed by ppremake
// (along with the Sources.pp files in each of the various
// directories) to generate build scripts appropriate to each
// environment.
//
// This is the package-specific file, which should be at the top of
// every source hierarchy.  It generally gets the ball rolling, and is
// responsible for explicitly including all of the relevent Config.pp
// files.



// What is the name and version of this source tree?
#if $[eq $[PACKAGE],]
  #define PACKAGE otp
  #define VERSION 0.80
#endif


// Where should we find the DIRECT source directory?
#if $[DIRECT_SOURCE]
  #define DIRECT_SOURCE $[unixfilename $[DIRECT_SOURCE]]
#elif $[or $[CTPROJS],$[DIRECT]]
  // If we are presently attached, use the environment variable.
  #define DIRECT_SOURCE $[unixfilename $[DIRECT]]
  #if $[eq $[DIRECT],]
    #error You seem to be attached to some trees, but not DIRECT!
  #endif
#else
  // Otherwise, if we are not attached, we guess that the source is a
  // sibling directory to this source root.
  #define DIRECT_SOURCE $[standardize $[TOPDIR]/../direct]
#endif

// Where should we install OTP?
#if $[OTP_INSTALL]
  #define OTP_INSTALL $[unixfilename $[OTP_INSTALL]]
#elif $[CTPROJS]
  #set OTP $[unixfilename $[OTP]]
  #define OTP_INSTALL $[OTP]/built
  #if $[eq $[OTP],]
    #error You seem to be attached to some trees, but not OTP!
  #endif
#else
  #defer OTP_INSTALL $[unixfilename $[INSTALL_DIR]]
#endif


// Also get the DIRECT Package file and everything that includes.
#if $[not $[isfile $[DIRECT_SOURCE]/Package.pp]]
  #printvar DIRECT_SOURCE
  #error DIRECT source directory not found from otp!  Are you attached properly?
#endif

#include $[DIRECT_SOURCE]/Package.pp

// Define the inter-tree dependencies.
#define NEEDS_TREES direct $[NEEDS_TREES]
#define DEPENDABLE_HEADER_DIRS $[DEPENDABLE_HEADER_DIRS] $[DIRECT_INSTALL]/include
