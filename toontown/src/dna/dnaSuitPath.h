// Filename: dnaSuitPath.h
// Created by:  shochet (28Jan01)
//
////////////////////////////////////////////////////////////////////
#ifndef DNASUITPATH_H
#define DNASUITPATH_H
//

#include "toontownbase.h"
#include "config_dna.h"
#include "typedObject.h"
#include "pointerTo.h"
#include "typedReferenceCount.h"
#include "pvector.h"
#include <algorithm>
#include "vector_int.h"

////////////////////////////////////////////////////////////////////
//       Class : DNASuitPath
// Description :
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNASuitPath : public TypedReferenceCount {

PUBLISHED:
  DNASuitPath();
  DNASuitPath(int reserve_length);
  DNASuitPath(const DNASuitPath &path);
  INLINE int get_num_points() const;
  void copy(const DNASuitPath &path);
  INLINE int get_point_index(int i) const;
  void output(ostream &out) const;

public:
  INLINE void add_point(int index);
  INLINE void reverse_path();

private:
  vector_int _path;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedReferenceCount::init_type();
    register_type(_type_handle, "DNASuitPath",
                  TypedReferenceCount::get_class_type()
                  );
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};


INLINE ostream &operator << (ostream &out, const DNASuitPath &path) {
  path.output(out);
  return out;
}

#include "dnaSuitPath.I"

#endif
