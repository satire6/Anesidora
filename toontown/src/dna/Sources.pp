#define YACC_PREFIX dnayy
#define LFLAGS -i

#define USE_PACKAGES freetype

#begin lib_target
  #define TARGET dnaLoader
  #define LOCAL_LIBS toontownbase
  #define OTHER_LIBS \
    panda:m pandaexpress:m \
    interrogatedb:c dconfig:c dtoolconfig:m \
    dtoolutil:c dtoolbase:c dtool:m \
    prc:c
  
  #define COMBINED_SOURCES $[TARGET]_composite1.cxx  $[TARGET]_composite2.cxx

  #define SOURCES \
     config_dna.h dnaBuildings.h dnaConstants.h dnaCornice.h dnaData.I  \
     dnaData.h dnaDoor.h dnaGroup.h dnaVisGroup.h dnaSign.I  \
     dnaSign.h dnaSignBaseline.I dnaSignBaseline.h  \
     dnaSignGraphic.I dnaSignGraphic.h dnaSignText.I  \
     dnaSignText.h dnaSuitPoint.I dnaSuitPoint.h dnaSuitEdge.I  \
     dnaSuitEdge.h dnaSuitPath.h dnaBattleCell.I dnaBattleCell.h  \
     dnaLoader.h dnaNode.I dnaNode.h dnaProp.h dnaProp.I \
     dnaAnimProp.h dnaAnimProp.I dnaInteractiveProp.h \
     dnaInteractiveProp.I dnaAnimBuilding.h dnaAnimBuilding.I \
     dnaStorage.h dnaStorage.I \
     dnaStreet.h dnaWindow.h lexerDefs.h load_dna_file.h  \
     loaderFileTypeDNA.h parserDefs.h parser.yxx lexer.lxx  \
    
  #define INCLUDED_SOURCES \
     config_dna.cxx dnaBuildings.cxx dnaCornice.cxx dnaData.cxx   \
     dnaDoor.cxx dnaGroup.cxx dnaVisGroup.cxx dnaSign.cxx   \
     dnaSignBaseline.cxx dnaSignGraphic.cxx dnaSignText.cxx   \
     dnaSuitPoint.cxx dnaSuitEdge.cxx dnaSuitPath.cxx   \
     dnaBattleCell.cxx dnaLoader.cxx dnaNode.cxx dnaProp.cxx   \
     dnaStorage.cxx dnaStreet.cxx dnaWindow.cxx load_dna_file.cxx   \
     dnaAnimProp.cxx dnaInteractiveProp.cxx dnaAnimBuilding.cxx \
     loaderFileTypeDNA.cxx

  #define IGATESCAN all

#end lib_target

// #begin test_bin_target
//   #define TARGET dnaTester
//   #define LOCAL_LIBS \
//     dnaLoader
//   #define OTHER_LIBS \
//     panda:m pandaexpress:m framework \
//     interrogatedb:c dconfig:c dtoolconfig:m \
//     dtoolutil:c dtoolbase:c dtool:m \
//     putil:c collide:c loader:c sgmanip:c chan:c text:c chancfg:c cull:c \
//     pnmimage:c pnmimagetypes:c event:c graph:c gobj:c display:c \
//     mathutil:c sgattrib:c express:c light:c dgraph:c device:c tform:c sgraph:c \
//     linmath:c pstatclient:c sgraphutil:c downloader:c \
//     pystub



//   #define SOURCES \
//     dnaTester.cxx

// #end test_bin_target

#begin test_bin_target
  #define TARGET validate_suit_path
  #define LOCAL_LIBS \
    dnaLoader
  #define OTHER_LIBS \
    express:c pandaexpress:m \
    panda:m \
    interrogatedb:c dconfig:c dtoolconfig:m \
    dtoolutil:c dtoolbase:c dtool:m \
    pystub

  #define SOURCES \
    validateSuitPath.cxx

#end test_bin_target

