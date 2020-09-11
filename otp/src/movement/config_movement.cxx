// Filename: config_movement.cxx
// Created by:  dcranall (15Jul04)
//
////////////////////////////////////////////////////////////////////

#include "config_movement.h"
#include "cMover.h"
#include "cImpulse.h"
#include "cMoverGroup.h"

#include "dconfig.h"

Configure(config_movement);
NotifyCategoryDef(movement, "");

ConfigureFn(config_movement) {
  init_libmovement();
}

////////////////////////////////////////////////////////////////////
//     Function: init_libmovement
//  Description: Initializes the library.  This must be called at
//               least once before any of the functions or classes in
//               this library can be used.  Normally it will be
//               called by the static initializers and need not be
//               called explicitly, but special cases exist.
////////////////////////////////////////////////////////////////////
void
init_libmovement() {
  static bool initialized = false;
  if (initialized) {
    return;
  }
  initialized = true;

  CMover::init_type();
  CImpulse::init_type();
  CMoverGroup::init_type();
}
