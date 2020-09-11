#begin lib_target
  #define TARGET pets
  #define LOCAL_LIBS \
    toontownbase

  #define OTHER_LIBS \
    otp:m otpbase:c movement:c \
    panda:m downloader:c express:c pandabase:c recorder:c \
    pgraph:c pgraphnodes:c pipeline:c grutil:c chan:c pstatclient:c \
    char:c collide:c cull:c device:c dgraph:c display:c \
    event:c gobj:c gsgbase:c linmath:c mathutil:c parametrics:c \
    pnmimagetypes:c pnmimage:c tform:c lerp:c text:c \
    putil:c audio:c pgui:c interrogatedb:c dconfig:c \
    $[if $[HAVE_NET],net:c] $[if $[WANT_NATIVE_NET],nativenet:c] \
    $[if $[HAVE_FREETYPE],pnmtext:c] \
    dtoolutil:c dtoolbase:c prc:c

  #define SOURCES \
    config_pets.h config_pets.cxx \
    cPetBrain.h cPetBrain.cxx cPetChase.h cPetChase.I cPetChase.cxx \
    cPetFlee.h cPetFlee.I cPetFlee.cxx

  #define INSTALL_HEADERS \
    config_pets.h \
    cPetBrain.h cPetChase.h cPetChase.I cPetFlee.h cPetFlee.I

  #define IGATESCAN all
#end lib_target
