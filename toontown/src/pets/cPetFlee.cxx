// Filename: cPetFlee.cxx
// Created by:  dcranall (15Jul04)
//
////////////////////////////////////////////////////////////////////

#include "cPetFlee.h"
#include "cMover.h"

TypeHandle CPetFlee::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: CPetFlee::Constructor
//       Access: Public
//  Description: 
////////////////////////////////////////////////////////////////////
CPetFlee::
CPetFlee(NodePath *chaser, float max_dist, float move_angle) :
  _max_dist(max_dist),
  _move_angle(move_angle),
  _look_at_node("lookatNode"),
  _vel(0),
  _rot_vel(0)
{
  if (chaser) {
    _chaser = *chaser;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: CPetFlee::Destructor
//       Access: Public, Virtual
//  Description: 
////////////////////////////////////////////////////////////////////
CPetFlee::
~CPetFlee() {
  _look_at_node.remove_node();
}

////////////////////////////////////////////////////////////////////
//     Function: CPetFlee::process
//       Access: Public, Virtual
//  Description: override this and set your impulse's influence for
//               this pass on its mover
////////////////////////////////////////////////////////////////////
void CPetFlee::
process(float dt) {
  CImpulse::process(dt);

  if (_chaser.is_empty()) {
    return;
  }

  // calc distance to chaser
  LVector3f chaser_pos = _chaser.get_pos(_node_path);
  float distance = chaser_pos.length();

  // calc angle between us and the chaser
  _look_at_node.look_at(_chaser);
  // run away from chaser
  float rel_h = _look_at_node.get_h(_node_path) + 180.;
  rel_h = (fmod((rel_h + 180), 360) - 180);

  // turn away from chaser
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
  if ((distance < _max_dist) && (fabs(rel_h) < _move_angle)) {
    v_forward = _mover->get_fwd_speed();
  }

  // don't get too far away
  const float distance_left = _max_dist - distance;
  /*
  cerr << "distance " << distance << endl;
  cerr << "distanceLeft " << distance_left << endl;
  */
  if ((distance_left > 0.) && ((v_forward * dt) > distance_left)) {
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
//     Function: CPetFlee::set_mover
//       Access: Public, Virtual
//  Description: called internally by cMover when we're added
////////////////////////////////////////////////////////////////////
void CPetFlee::
set_mover(CMover &mover) {
  CImpulse::set_mover(mover);
  _look_at_node.reparent_to(_node_path);
  _vel = 0;
  _rot_vel = 0;
}
