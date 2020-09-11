#define USE_PACKAGES cg  // from gobj.

#begin lib_target
  #define TARGET toontownbase

  #define OTHER_LIBS \
      dtool:m dtoolconfig:m \
      prc:c dtoolutil:c dtoolbase:c
  
  #define SOURCES \
    toontownbase.cxx toontownbase.h toontownsymbols.h \

  #define INSTALL_HEADERS \
    toontownbase.h toontownsymbols.h

#end lib_target
