// Filename: cMoverGroup.cxx
// Created by:  darren (13Mar07)
//
////////////////////////////////////////////////////////////////////

#include "cMoverGroup.h"
#include "clockObject.h"

TypeHandle CMoverGroup::_type_handle;

CMoverGroup::
CMoverGroup()
{
  _dt = 1;
  _last_ft = ClockObject::get_global_clock()->get_frame_time();
}

CMoverGroup::
~CMoverGroup() {
  while (!_movers.empty()) {
    cerr << "removing C++ movers: " << (*_movers.begin()).first << endl;
    remove_c_mover((*_movers.begin()).first);
  }
}

void CMoverGroup::
add_c_mover(const string &name, CMover *mover) {
  // if there is already a mover of this name, make sure it's removed
  // first
  remove_c_mover(name);
  _movers[name] = mover;
}

bool CMoverGroup::
remove_c_mover(const string &name) {
  MoverMap::iterator mi = _movers.find(name);
  if (mi != _movers.end()) {
    _movers.erase(mi);
    return true;
  }
  return false;
}

void CMoverGroup::
process_c_impulses_and_integrate() {
  for (MoverMap::iterator mi = _movers.begin();
       mi != _movers.end();
       ++mi) {
    (*mi).second->process_c_impulses(_dt);
    (*mi).second->integrate();
  }
}
