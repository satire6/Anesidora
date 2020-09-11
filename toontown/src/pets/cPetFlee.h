// Filename: cPetFlee.h
// Created by:  dcranall (15Jul04)
//
////////////////////////////////////////////////////////////////////

#ifndef CPETFLEE_H
#define CPETFLEE_H

#include "toontownbase.h"
#include "cImpulse.h"

class EXPCL_TOONTOWN CPetFlee : public CImpulse {
PUBLISHED:
  CPetFlee(NodePath *chaser = 0, float max_dist = 50., float move_angle = 20.);
  ~CPetFlee();

  void process(float dt);

  void set_mover(CMover &mover);

  INLINE void set_chaser(NodePath &chaser);

private:
  NodePath _chaser;
  float _max_dist;
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
    register_type(_type_handle, "CPetFlee",
                  CImpulse::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "cPetFlee.I"

#endif
