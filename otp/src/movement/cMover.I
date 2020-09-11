// Filename: cMover.I
// Created by:  darren (13Jul04)
//
////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
//     Function: CMover::set_fwd_speed
//       Access: Published
//  Description: Sets the speed that impulses should use when moving
//               forward
////////////////////////////////////////////////////////////////////
INLINE void CMover::
set_fwd_speed(float fwd_speed) {
  _fwd_speed = fwd_speed;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::set_rot_speed
//       Access: Published
//  Description: Sets the speed that impulses should use when rotating
////////////////////////////////////////////////////////////////////
INLINE void CMover::
set_rot_speed(float rot_speed) {
  _rot_speed = rot_speed;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::get_fwd_speed
//       Access: Published
//  Description: Returns the speed that impulses should use when moving
//               forward
////////////////////////////////////////////////////////////////////
INLINE float CMover::
get_fwd_speed() const {
  return _fwd_speed;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::get_rot_speed
//       Access: Published
//  Description: Returns the speed that impulses should use when rotating
////////////////////////////////////////////////////////////////////
INLINE float CMover::
get_rot_speed() const {
  return _rot_speed;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::add_force
//       Access: Published
//  Description: Called by impulses during CMover::move()
////////////////////////////////////////////////////////////////////
INLINE void CMover::
add_force(const LVector3f &force) {
  _acc += force;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::add_rot_force
//       Access: Published
//  Description: Called by impulses during CMover::move()
////////////////////////////////////////////////////////////////////
INLINE void CMover::
add_rot_force(const LVector3f &rot_force) {
  _rot_acc += rot_force;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::add_shove
//       Access: Published
//  Description: Called by impulses during CMover::move()
////////////////////////////////////////////////////////////////////
INLINE void CMover::
add_shove(const LVector3f &shove) {
  _shove += shove;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::add_rot_shove
//       Access: Published
//  Description: Called by impulses during CMover::move()
////////////////////////////////////////////////////////////////////
INLINE void CMover::
add_rot_shove(const LVector3f &rot_shove) {
  _rot_shove += rot_shove;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::get_node_path
//       Access: Published
//  Description: Returns nodepath being moved by this mover
////////////////////////////////////////////////////////////////////
INLINE NodePath CMover::
get_node_path() const {
  return _node_path;
}

////////////////////////////////////////////////////////////////////
//     Function: CMover::get_dt
//       Access: Published
//  Description: Returns dt from last call to move()
////////////////////////////////////////////////////////////////////
INLINE float CMover::
get_dt() const {
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
INLINE void CMover::
reset_dt() {
  _last_ft = ClockObject::get_global_clock()->get_frame_time();
}
