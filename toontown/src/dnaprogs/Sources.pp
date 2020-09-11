#define LOCAL_LIBS \
  dnaLoader
#define OTHER_LIBS \
  event:c mathutil:c linmath:c putil:c parametrics:c panda:m \
  express:c pandaexpress:m \
  dtoolutil:c dtoolbase:c prc:c dconfig:c dtoolconfig:m dtool:m \
  pipeline:c pstatclient:c cull:c \
  prc:c interrogatedb:c pandaexpress:c pandabase:c downloader:c pgraph:c \
  pgraphnodes:c gobj:c pnmimage:c lerp:c gsgbase:c text:c display:c \
  $[if $[HAVE_NET],net:c] $[if $[WANT_NATIVE_NET],nativenet:c] \
  pystub

#if $[HAVE_FREETYPE]
    #define OTHER_LIBS $[OTHER_LIBS] pnmtext:c
  #endif

#define UNIX_SYS_LIBS m

#begin bin_target
  #define TARGET dna-trans

  #define SOURCES \
    dnaTrans.cxx

#end bin_target
