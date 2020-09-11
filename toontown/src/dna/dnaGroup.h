// Filename: dnaGroup.h
// Created by:  shochet (24May00)
//
////////////////////////////////////////////////////////////////////

//
#ifndef DNAGROUP_H
#define DNAGROUP_H
//
////////////////////////////////////////////////////////////////////
// Includes
////////////////////////////////////////////////////////////////////
#include "toontownbase.h"

#include "typedObject.h"
#include "namable.h"
#include "nodePath.h"
#include "pvector.h"
#include <string>
#include "pointerTo.h"
#include "typedReferenceCount.h"

class DNAStorage;

////////////////////////////////////////////////////////////////////
//       Class : DNAGroup
// Description : A group of dna nodes
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNAGroup : public TypedReferenceCount, public Namable {
PUBLISHED:
  DNAGroup(const string &initial_name = "");
  DNAGroup(const DNAGroup &group);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  NodePath top_level_traverse(NodePath &parent, DNAStorage *store, int editing=0);

  void add(PT(DNAGroup) group);
  void remove(PT(DNAGroup) group);
  INLINE PT(DNAGroup) at(uint index);
  INLINE PT(DNAGroup) current();
  INLINE int get_num_children();
  INLINE PT(DNAGroup) get_parent() const;

  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  void ls() const;

public:
  INLINE void set_parent(PT(DNAGroup));
  INLINE void clear_parent();

protected:
  pvector<PT(DNAGroup)> _group_vector;

private:
  virtual DNAGroup* make_copy();
  // Ok, the parent pointer is not going to be a PointerTo to prevent
  // circular references from being leaked
  // TODO: in this destructor, null out all the children's parent pointers
  // so they will have NULL pointers, and not "bad" pointers
  DNAGroup* _parent;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedReferenceCount::init_type();
    Namable::init_type();
    register_type(_type_handle, "DNAGroup",
                  TypedReferenceCount::get_class_type(),
                  Namable::get_class_type()
                  );
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};


#include "dnaGroup.I"

#endif
