// Filename: dnaSignGraphic.h
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////
#ifndef DNASignGraphic_H
#define DNASignGraphic_H
//

#include "dnaNode.h"
#include "dnaBuildings.h"
#include "pandaNode.h"
#include "nodePath.h"
#include "luse.h"
#include "pvector.h"

////////////////////////////////////////////////////////////////////
//   Class : DNASignGraphic
// Description : A graphic
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNASignGraphic : public DNANode  {
PUBLISHED:
  DNASignGraphic(const string &initial_name = "");
  DNASignGraphic(const DNASignGraphic &graphic);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  void set_code(string code);
  string get_code() const;

  void set_color(const Colorf &color);
  Colorf get_color() const;

  void set_width(float width);
  float get_width() const;

  void set_height(float height);
  float get_height() const;

private:
  virtual DNAGroup* make_copy();

private:
  string _code;
  Colorf _color;
  float _width;
  float _height;
  bool _use_baseline_color;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNAGroup::init_type();
    register_type(_type_handle, "DNASignGraphic",
                  DNAGroup::get_class_type()
                  );
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "dnaSignGraphic.I"

#endif
