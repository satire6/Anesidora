// Filename: cPetChase.h
// Created by:  dcranall (15Jul04)
//
////////////////////////////////////////////////////////////////////

#ifndef CPETCHASE_H
#define CPETCHASE_H

#include "toontownbase.h"
#include "cImpulse.h"

class EXPCL_TOONTOWN CPetChase : public CImpulse {
PUBLISHED:
  CPetChase(NodePath *target = 0, float min_dist = 5., float move_angle = 20.);
  ~CPetChase();

  void process(float dt);

  void set_mover(CMover &mover);

  INLINE void set_target(const NodePath &target);
  INLINE NodePath get_target() const;
  INLINE void set_min_dist(float min_dist);
  INLINE float get_min_dist() const;

private:
  NodePath _target;
  float _min_dist;
  float _move_angle;

  NodePath _look_at_node;
  LVector3f _vel;
  LVector3f _rot_vel;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    CImpulse::init_type();
    register_type(_type_handle, "CPetChase",
                  CImpulse::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "cPetChase.I"

#endif
