// Filename: cMover.cxx
// Created by:  darren (13Jul04)
//
////////////////////////////////////////////////////////////////////

#include "cMover.h"
#include "clockObject.h"

TypeHandle CMover::_type_handle;

CMover::
CMover(NodePath &objNodePath, float fwd_speed, float rot_speed) :
  _acc(0), _vel(0), _rot_acc(0), _rot_vel(0),
  _acc_accum(0), _rot_acc_accum(0), _shove(0), _rot_shove(0)
{
  set_fwd_speed(fwd_speed);
  set_rot_speed(rot_speed);
  _node_path = objNodePath;

  _dt = 1;
  _last_ft = ClockObject::get_global_clock()->get_frame_time();
}

CMover::
~CMover() {
  while (!_impulses.empty()) {
    cerr << "removing C++ impulse: " << (*_impulses.begin()).first << endl;
    remove_c_impulse((*_impulses.begin()).first);
  }
}

void CMover::
add_c_impulse(const string &name, CImpulse *impulse) {
  // if there is already an impulse of this name, make sure it's removed
  // first
  remove_c_impulse(name);
  _impulses[name] = impulse;
  impulse->set_mover(*this);
}

bool CMover::
remove_c_impulse(const string &name) {
  ImpulseMap::iterator ii = _impulses.find(name);
  if (ii != _impulses.end()) {
    (*ii).second->clear_mover(*this);
    _impulses.erase(ii);
    return true;
  }
  return false;
}

void CMover::
process_c_impulses(float dt) {
  // call this before calling integrate
  _dt = dt;
  if (_dt == -1) {
    // We can't use globalClock.getDt() because we don't require
    // that move() be called every frame.
    float ft = ClockObject::get_global_clock()->get_frame_time();
    _dt = ft - _last_ft;
    _last_ft = ft;
  }

  for (ImpulseMap::iterator ii = _impulses.begin();
       ii != _impulses.end();
       ++ii) {
    (*ii).second->process(_dt);
  }
}

void CMover::
integrate() {
  // integreat!
  _acc = _acc_accum;
  _rot_acc = _rot_acc_accum;
  _vel += (_acc * _dt);
  _rot_vel += (_rot_acc * _dt);

  float dt2 = _dt*_dt;

  // (self.vel * dt) + (self.acc * dt2 * .5) + (self._shove * dt)
  _node_path.set_fluid_pos(_node_path, 
                           (_vel * _dt) +
                           (_acc * dt2 * .5) +
                           (_shove * _dt));
  
  // (self.rotVel * dt) + (self.rotAcc * dt2 * .5) + (self._rotShove * dt)
  _node_path.set_hpr(_node_path,
                     (_rot_vel * _dt) +
                     (_rot_acc * dt2 * .5) +
                     (_rot_shove * _dt));

  // set up for next frame
  // don't overwrite _acc etc. yet, impulses might want to use
  // last frame's data. Accumulate in these vectors.
  _acc_accum = 0;
  _rot_acc_accum = 0;
  // allow the impulses to directly shove without going through acceleration
  _shove = 0;
  _rot_shove = 0;
}
