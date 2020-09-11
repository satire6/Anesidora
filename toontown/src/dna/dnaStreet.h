// Filename: dnaStreet.h
// Created by:  shochet (26May00)
//
////////////////////////////////////////////////////////////////////

//
#ifndef DNASTREET_H
#define DNASTREET_H
//
////////////////////////////////////////////////////////////////////
// Includes
////////////////////////////////////////////////////////////////////
#include "dnaStorage.h"
#include "dnaNode.h"
#include "pandaNode.h"
#include "nodePath.h"
#include "luse.h"
#include "pvector.h"


////////////////////////////////////////////////////////////////////
//       Class : DNAStreet
// Description : A street.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNAStreet : public DNANode  {
PUBLISHED:
  DNAStreet(const string &initial_name);
  DNAStreet(const DNAStreet &street);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  INLINE void set_code(string code);
  INLINE string get_code() const;

  INLINE void set_street_texture(string street_texture);
  INLINE string get_street_texture() const;

  INLINE void set_sidewalk_texture(string sidewalk_texture);
  INLINE string get_sidewalk_texture() const;

  INLINE void set_curb_texture(string curb_texture);
  INLINE string get_curb_texture() const;

  // For now we no longer support color on streets to allow vertex color

  INLINE void set_street_color(const Colorf &color);
  INLINE Colorf get_street_color() const;

  INLINE void set_sidewalk_color(const Colorf &color);
  INLINE Colorf get_sidewalk_color() const;

  INLINE void set_curb_color(const Colorf &color);
  INLINE Colorf get_curb_color() const;

private:
  virtual DNAGroup* make_copy();

private:
  string _code;
  string _street_texture;
  string _sidewalk_texture;
  string _curb_texture;
  Colorf _street_color;
  Colorf _sidewalk_color;
  Colorf _curb_color;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNANode::init_type();
    register_type(_type_handle, "DNAStreet",
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

#include "dnaStreet.I"

#endif
