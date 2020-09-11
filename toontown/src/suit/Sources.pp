#begin lib_target
  #define TARGET suit
  #define LOCAL_LIBS dnaLoader toontownbase
  #define OTHER_LIBS \
    panda:m pandaexpress:m \
    interrogatedb:c dconfig:c dtoolconfig:m \
    dtoolutil:c dtoolbase:c dtool:m \
    prc:c

  #define COMBINED_SOURCES $[TARGET]_composite1.cxx
  
  #define SOURCES \
    suitLeg.I suitLeg.h \
    suitLegList.I suitLegList.h
    
  #define INCLUDED_SOURCES  \
    suitLeg.cxx suitLegList.cxx

  #define IGATESCAN all

#end lib_target

