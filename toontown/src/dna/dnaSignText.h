// Filename: dnaSignText.h
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////
#ifndef DNASignText_H
#define DNASignText_H
//

#include "dnaNode.h"
#include "dnaBuildings.h"
#include "pandaNode.h"
#include "nodePath.h"
#include "luse.h"
#include "pvector.h"

////////////////////////////////////////////////////////////////////
//       Class : DNASignText
// Description : A Sign
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNASignText : public DNANode  {
PUBLISHED:
  DNASignText(const string &initial_name = "");
  DNASignText(const DNASignText &signText);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  INLINE void set_code(string code);
  INLINE string get_code() const;

  INLINE void set_color(const Colorf &color);
  INLINE Colorf get_color() const;

  INLINE void set_letters(string letters);
  INLINE string get_letters() const;

private:
  virtual DNAGroup* make_copy();

protected:
  string _code;
  Colorf _color;
  string _letters;
  bool _use_baseline_color;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNANode::init_type();
    register_type(_type_handle, "DNASignText",
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

#include "dnaSignText.I"

#endif
