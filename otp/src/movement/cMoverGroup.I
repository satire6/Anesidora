// Filename: cMoverGroup.I
// Created by:  darren (13Mar07)
//
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
//     Function: CMoverGroup::get_dt
//       Access: Published
//  Description: Returns dt from last call to set_dt
////////////////////////////////////////////////////////////////////
INLINE float CMoverGroup::
get_dt() const {
  return _dt;
}

////////////////////////////////////////////////////////////////////
//     Function: CMoverGroup::set_dt
//       Access: Published
//  Description: sets dt for current frame, calculates if -1 is passed
//               returns dt for current frame
////////////////////////////////////////////////////////////////////
INLINE float CMoverGroup::
set_dt(float dt) {
  _dt = dt;
  if (_dt == -1) {
    // We can't use globalClock.getDt() because we don't require
    // that movement happen every frame.
    float ft = ClockObject::get_global_clock()->get_frame_time();
    _dt = ft - _last_ft;
    _last_ft = ft;
  }
  return _dt;
}

////////////////////////////////////////////////////////////////////
//     Function: CMoverGroup::reset_dt
//       Access: Published
//  Description: ignores time elapsed since last set_dt, call if
//               mover group has not been moved in a long time
//               and you don't want objects to move as if they
//               were moving the whole time
////////////////////////////////////////////////////////////////////
INLINE void CMoverGroup::
reset_dt() {
  _last_ft = ClockObject::get_global_clock()->get_frame_time();
}
