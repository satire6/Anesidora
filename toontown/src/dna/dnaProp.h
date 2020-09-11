// Filename: dnaProp.h
// Created by:  shochet (28Mar00)
//
////////////////////////////////////////////////////////////////////
#ifndef DNAPROP_H
#define DNAPROP_H
//

#include "dnaStorage.h"
#include "dnaNode.h"
#include "pandaNode.h"
#include "nodePath.h"
#include "luse.h"
#include "pvector.h"

////////////////////////////////////////////////////////////////////
//       Class : DNAProp
// Description : A prop like a tree or fire hydrant.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNAProp : public DNANode  {
PUBLISHED:
  DNAProp(const string &initial_name = "");
  DNAProp(const DNAProp &prop);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  INLINE void set_code(string code);
  INLINE string get_code() const;

  INLINE void set_color(const Colorf &color);
  INLINE Colorf get_color() const;

private:
  virtual DNAGroup* make_copy();

protected:
  string _code;
  Colorf _color;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNANode::init_type();
    register_type(_type_handle, "DNAProp",
                  DNANode::get_class_type()
                  );
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "dnaProp.I"

#endif
