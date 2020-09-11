#define INSTALL_CONFIG \
  toontown.init 60_toontown.prc

#include $[THISDIRPREFIX]toontown.prc.pp

#if $[LANGUAGE]
  #if $[eq $[LANGUAGE], castillian]
    #set INSTALL_CONFIG $[INSTALL_CONFIG] castillianPRC
  #elif $[eq $[LANGUAGE], japanese]
    #set INSTALL_CONFIG $[INSTALL_CONFIG] japanesePRC
  #elif $[eq $[LANGUAGE], german]
    #set INSTALL_CONFIG $[INSTALL_CONFIG] germanPRC
  #elif $[eq $[LANGUAGE], portuguese]
    #set INSTALL_CONFIG $[INSTALL_CONFIG] portuguesePRC
  #elif $[eq $[LANGUAGE], french]
    #set INSTALL_CONFIG $[INSTALL_CONFIG] frenchPRC
  #endif
#endif
