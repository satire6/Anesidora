// Filename: nametagFloat3d.h
// Created by:  drose (25Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef NAMETAGFLOAT3D_H
#define NAMETAGFLOAT3D_H

#include "otpbase.h"

#include "nametag3d.h"

////////////////////////////////////////////////////////////////////
//       Class : NametagFloat3d
// Description : This is a user-created Nametag that can be parented
//               to some object, not necessarily the avatar, in the
//               3-d scene graph.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP NametagFloat3d : public Nametag3d {
PUBLISHED:
  NametagFloat3d();
  virtual ~NametagFloat3d();

public:
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    Nametag3d::init_type();
    register_type(_type_handle, "NametagFloat3d",
                  Nametag3d::get_class_type());
  }

private:
  static TypeHandle _type_handle;
};

#endif

