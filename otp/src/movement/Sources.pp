#define USE_PACKAGES cg  // from gobj.

#begin lib_target
  #define TARGET movement
  #define LOCAL_LIBS \
    otpbase
  #define OTHER_LIBS \
    panda:m downloader:c express:c pandabase:c recorder:c \
    pgraph:c pgraphnodes:c pipeline:c grutil:c chan:c pstatclient:c \
    char:c collide:c cull:c device:c dgraph:c display:c \
    event:c gobj:c gsgbase:c linmath:c mathutil:c parametrics:c \
    pnmimagetypes:c pnmimage:c tform:c lerp:c text:c \
    putil:c audio:c pgui:c interrogatedb:c dconfig:c \
    $[if $[HAVE_NET],net:c] $[if $[WANT_NATIVE_NET],nativenet:c] \
    dtoolutil:c dtoolbase:c prc:c

  #if $[HAVE_FREETYPE]
    #define OTHER_LIBS $[OTHER_LIBS] pnmtext:c
  #endif

  #define SOURCES \
    config_movement.cxx config_movement.h \
    cMover.h cMover.I cMover.cxx cImpulse.h cImpulse.I cImpulse.cxx \
    cMoverGroup.h cMoverGroup.I cMoverGroup.cxx

  #define INSTALL_HEADERS \
    config_movement.h \
    cMover.h cMover.I cImpulse.h cImpulse.I cMoverGroup.h cMoverGroup.I

  #define IGATESCAN all
#end lib_target
