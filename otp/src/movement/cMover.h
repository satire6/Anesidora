// Filename: cMover.h
// Created by:  darren (13Jul04)
//
////////////////////////////////////////////////////////////////////

#ifndef CMOVER_H
#define CMOVER_H

#include "otpbase.h"
#include "typedReferenceCount.h"
#include "config_movement.h"
#include "nodePath.h"
#include "luse.h"
#include "pmap.h"
#include "cImpulse.h"

class EXPCL_OTP CMover : public TypedReferenceCount {
PUBLISHED:
  CMover(NodePath &objNodePath, float fwd_speed = 1, float rot_speed = 1);
  ~CMover();

  INLINE void set_fwd_speed(float fwd_speed);
  INLINE void set_rot_speed(float rot_speed);
  INLINE float get_fwd_speed() const;
  INLINE float get_rot_speed() const;

  void add_c_impulse(const string &name, CImpulse *impulse);
  bool remove_c_impulse(const string &name);

  void process_c_impulses(float dt = -1);
  void integrate();

  INLINE void add_force(const LVector3f &force);
  INLINE void add_rot_force(const LVector3f &rot_force);
  INLINE void add_shove(const LVector3f &shove);
  INLINE void add_rot_shove(const LVector3f &rot_shove);

  INLINE NodePath get_node_path() const;
  INLINE float get_dt() const;

  INLINE void reset_dt();

private:
  float _fwd_speed;
  float _rot_speed;

  NodePath _node_path;
  float _dt;
  float _last_ft;

  LVector3f _acc;
  LVector3f _vel;

  LVector3f _rot_acc;
  LVector3f _rot_vel;

  LVector3f _acc_accum;
  LVector3f _rot_acc_accum;
  LVector3f _shove;
  LVector3f _rot_shove;

  typedef pmap<string, PT(CImpulse) > ImpulseMap;
  ImpulseMap _impulses;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedReferenceCount::init_type();
    register_type(_type_handle, "CMover",
                  TypedReferenceCount::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "cMover.I"

#endif
