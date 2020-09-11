// Filename: cPetChase.cxx
// Created by:  dcranall (15Jul04)
//
////////////////////////////////////////////////////////////////////

#include "cPetChase.h"
#include "cMover.h"

TypeHandle CPetChase::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: CPetChase::Constructor
//       Access: Public
//  Description: 
////////////////////////////////////////////////////////////////////
CPetChase::
CPetChase(NodePath *target, float min_dist, float move_angle) :
  _min_dist(min_dist),
  _move_angle(move_angle),
  _look_at_node("lookatNode"),
  _vel(0),
  _rot_vel(0)
{
  if (target) {
    _target = *target;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: CPetChase::Destructor
//       Access: Public, Virtual
//  Description: 
////////////////////////////////////////////////////////////////////
CPetChase::
~CPetChase() {
  _look_at_node.remove_node();
}

////////////////////////////////////////////////////////////////////
//     Function: CPetChase::process
//       Access: Public, Virtual
//  Description: override this and set your impulse's influence for
//               this pass on its mover
////////////////////////////////////////////////////////////////////
void CPetChase::
process(float dt) {
  CImpulse::process(dt);

  if (_target.is_empty()) {
    return;
  }

  // calc distance to target
  LVector3f target_pos = _target.get_pos(_node_path);
  float distance = sqrt((target_pos[0]*target_pos[0]) + (target_pos[1]*target_pos[1]));

  // calc angle between us and the target
  _look_at_node.look_at(_target);
  float rel_h = _look_at_node.get_h(_node_path);
  rel_h = (fmod((rel_h + 180), 360) - 180);

  // turn towards the target
  const float epsilon = .005;
  const float rot_speed = _mover->get_rot_speed();
  float v_h = 0;
  if (rel_h < -epsilon) {
    v_h = -rot_speed;
  } else if (rel_h > epsilon) {
    v_h = rot_speed;
  }

  // don't oversteer
  if (fabs(v_h * dt) > fabs(rel_h)) {
    v_h = rel_h / dt;
  }

  float v_forward = 0;
  if ((distance > _min_dist) && (fabs(rel_h) < _move_angle)) {
    v_forward = _mover->get_fwd_speed();
  }

  // don't get too close
  const float distance_left = distance - _min_dist;
  /*
  cerr << "distance " << distance << endl;
  cerr << "distanceLeft " << distance_left << endl;
  */
  if ((distance > _min_dist) && ((v_forward * dt) > distance_left)) {
    v_forward = distance_left / dt;
  }

  if (v_forward) {
    _vel.set_y(v_forward);
    _mover->add_shove(_vel);
  }
  if (v_h) {
    _rot_vel.set_x(v_h);
    _mover->add_rot_shove(_rot_vel);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: CPetChase::set_mover
//       Access: Public, Virtual
//  Description: called internally by cMover when we're added
////////////////////////////////////////////////////////////////////
void CPetChase::
set_mover(CMover &mover) {
  CImpulse::set_mover(mover);
  _look_at_node.reparent_to(_node_path);
  _vel = 0;
  _rot_vel = 0;
}
