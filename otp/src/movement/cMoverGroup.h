// Filename: cMoverGroup.h
// Created by:  darren (13Mar07)
//
////////////////////////////////////////////////////////////////////

#ifndef CMOVERGROUP_H
#define CMOVERGROUP_H

#include "otpbase.h"
#include "typedReferenceCount.h"
#include "config_movement.h"
#include "nodePath.h"
#include "luse.h"
#include "pmap.h"
#include "cMover.h"
#include "clockObject.h"

/* 
This class allows multiple CMovers to be moved in one efficient pass.
MoverGroup.py derives from this and allows multiple Python Movers to
be moved in one pass.
*/

class EXPCL_OTP CMoverGroup : public TypedReferenceCount {
PUBLISHED:
  CMoverGroup();
  ~CMoverGroup();

  void add_c_mover(const string &name, CMover *mover);
  bool remove_c_mover(const string &name);

  INLINE float set_dt(float dt = -1);
  INLINE float get_dt() const;

  INLINE void reset_dt();

  // processes C++ impulses and integrates; call set_dt first
  void process_c_impulses_and_integrate();

private:
  float _dt;
  float _last_ft;

  typedef pmap<string, PT(CMover) > MoverMap;
  MoverMap _movers;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedReferenceCount::init_type();
    register_type(_type_handle, "CMoverGroup",
                  TypedReferenceCount::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "cMoverGroup.I"

#endif
