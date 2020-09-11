// Filename: cImpulse.h
// Created by:  darren (13Jul04)
//
////////////////////////////////////////////////////////////////////

#ifndef CIMPULSE_H
#define CIMPULSE_H

#include "otpbase.h"
#include "typedReferenceCount.h"
#include "config_movement.h"
#include "nodePath.h"

class CMover;

class EXPCL_OTP CImpulse : public TypedReferenceCount {
PUBLISHED:
  CImpulse();
  virtual ~CImpulse();

  virtual void process(float dt);

  virtual void set_mover(CMover &mover);
  virtual void clear_mover(CMover &mover);

  INLINE CMover *get_mover() const;
  INLINE NodePath get_node_path() const;

  INLINE bool is_cpp() const;

protected:
  CMover *_mover;
  NodePath _node_path;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedReferenceCount::init_type();
    register_type(_type_handle, "CImpulse",
                  TypedReferenceCount::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "cImpulse.I"

#endif
