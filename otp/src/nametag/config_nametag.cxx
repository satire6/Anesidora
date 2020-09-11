// Filename: config_nametag.cxx
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#include "config_nametag.h"
#include "clickablePopup.h"
#include "nametag.h"
#include "nametag2d.h"
#include "nametag3d.h"
#include "nametagFloat2d.h"
#include "nametagFloat3d.h"
#include "popupMouseWatcherRegion.h"
#include "marginPopup.h"
#include "marginManager.h"
#include "whisperPopup.h"
#include "eventParameter.h"

#include "dconfig.h"

ConfigureDef(config_nametag);
NotifyCategoryDef(nametag, "");

ConfigureFn(config_nametag) {
  init_libnametag();
}

ConfigVariableString nametag_fixed_bin
("nametag-fixed-bin", "fixed",
 PRC_DESC("This is the name of the bin into which all of the nametags with a "
          "particular draw order is assigned."));


////////////////////////////////////////////////////////////////////
//     Function: init_libnametag
//  Description: Initializes the library.  This must be called at
//               least once before any of the functions or classes in
//               this library can be used.  Normally it will be
//               called by the static initializers and need not be
//               called explicitly, but special cases exist.
////////////////////////////////////////////////////////////////////
void
init_libnametag() {
  static bool initialized = false;
  if (initialized) {
    return;
  }
  initialized = true;

  ClickablePopup::init_type();
  Nametag::init_type();
  Nametag2d::init_type();
  Nametag3d::init_type();
  NametagFloat2d::init_type();
  NametagFloat3d::init_type();
  PopupMouseWatcherRegion::init_type();
  MarginPopup::init_type();
  MarginManager::init_type();
  WhisperPopup::init_type();

  // We need to duplicate these here in case template instantiation
  // makes them different classes then the ones defined in Panda.
  EventStoreInt::init_type("EventStoreInt");
  EventStoreString::init_type("EventStoreString");
}
