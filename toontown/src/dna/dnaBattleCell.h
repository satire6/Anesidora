// Filename: dnaBattleCell.h
// Created by:  shochet (31Jan01)
//
////////////////////////////////////////////////////////////////////
#ifndef DNABATTLECELL_H
#define DNABATTLECELL_H
//
////////////////////////////////////////////////////////////////////
// Includes
////////////////////////////////////////////////////////////////////
#include "toontownbase.h"
#include "typedObject.h"
#include "pointerTo.h"
#include "typedReferenceCount.h"
#include "luse.h"
#include "nodePath.h"

class DNAStorage;


////////////////////////////////////////////////////////////////////
//       Class : DNABattleCell
// Description : A representation of an area where a battle may occur.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNABattleCell : public TypedReferenceCount  {
PUBLISHED:
  DNABattleCell(float width, float height, LPoint3f pos);

  INLINE void set_width_height(float width, float height);
  INLINE float get_width() const;
  INLINE float get_height() const;
  INLINE void set_pos(LPoint3f pos);
  INLINE LPoint3f get_pos() const;
  void output(ostream &out) const;

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

private:
  float _width;
  float _height;
  LPoint3f _pos;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedReferenceCount::init_type();
    register_type(_type_handle, "DNABattleCell",
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


INLINE ostream &operator << (ostream &out, const DNABattleCell &cell) {
  cell.output(out);
  return out;
}


#include "dnaBattleCell.I"

#endif
