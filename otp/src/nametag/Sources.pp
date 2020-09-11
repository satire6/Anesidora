#define USE_PACKAGES cg  // from gobj.

#begin lib_target
  #define TARGET nametag
  #define LOCAL_LIBS otpbase
  #define OTHER_LIBS \
    panda pandaexpress \
    interval:c direct:m \
    interrogatedb:c dconfig:c dtoolconfig:m \
    dtoolutil:c dtoolbase:c dtool:m \
    express:c prc:c event:c pgraph:c pgraphnodes:c linmath:c gobj:c lerp:c \
    char:c putil:c mathutil:c downloader:c mathutil:c  chan:c \
    pandabase:c recorder:c grutil:c chan:c  collide:c device:c \
    dgraph:c display:c gsgbase:c parametrics:c text:c pnmimage:c \
    pipeline:c pstatclient:c cull:c pnmimagetypes:c tform:c \
    audio:c pgui:c directbase:c movies:c \
    $[if $[HAVE_NET],net:c] $[if $[WANT_NATIVE_NET],nativenet:c]

  #if $[HAVE_FREETYPE]
    #define OTHER_LIBS $[OTHER_LIBS] pnmtext:c
  #endif

  #define COMBINED_SOURCES $[TARGET]_composite1.cxx $[TARGET]_composite2.cxx
  
  #define SOURCES \
    chatBalloon.I chatBalloon.h \
    chatFlags.h \
    clickablePopup.I clickablePopup.h \
    config_nametag.h \
    nametag.I nametag.h \
    nametag2d.I nametag2d.h \
    nametag3d.I nametag3d.h \
    nametagFloat2d.h nametagFloat3d.h \
    nametagGroup.I nametagGroup.h \
    nametagGlobals.I nametagGlobals.h \
    popupMouseWatcherRegion.I popupMouseWatcherRegion.h \
    marginPopup.I marginPopup.h \
    marginManager.I marginManager.h \
    whisperPopup.I whisperPopup.h
    
  #define INCLUDED_SOURCES  \
    chatBalloon.cxx \
    clickablePopup.cxx \
    config_nametag.cxx \
    nametag.cxx \
    nametag2d.cxx \
    nametag3d.cxx \
    nametagFloat2d.cxx nametagFloat3d.cxx \
    nametagGroup.cxx \
    nametagGlobals.cxx \
    popupMouseWatcherRegion.cxx \
    marginPopup.cxx \
    marginManager.cxx \
    whisperPopup.cxx

  #define IGATESCAN all

#end lib_target
