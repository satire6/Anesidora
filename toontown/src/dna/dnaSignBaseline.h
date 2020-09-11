// Filename: dnaSignBaseline.h
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////
#ifndef DNASignBaseline_H
#define DNASignBaseline_H
//

#include "dnaNode.h"
#include "dnaBuildings.h"
#include "textFont.h"

#include "pandaNode.h"
#include "nodePath.h"
#include "luse.h"
#include "pvector.h"

class DNASignText;


////////////////////////////////////////////////////////////////////
//   Class : DNASignBaseline
// Description : A Sign
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN DNASignBaseline : public DNANode  {
PUBLISHED:
  DNASignBaseline(const string &initial_name = "");
  DNASignBaseline(const DNASignBaseline &Sign);

  virtual NodePath traverse(NodePath &parent, DNAStorage *store, int editing=0);
  virtual void write(ostream &out, DNAStorage *store, int indent_level = 0) const;

  INLINE void set_code(string code);
  INLINE string get_code() const;

  INLINE void set_color(const Colorf &color);
  INLINE Colorf get_color() const;

  INLINE void set_font(TextFont *font);
  INLINE TextFont *get_font() const;

  INLINE void set_indent(float indent);
  INLINE float get_indent() const;

  INLINE void set_kern(float kern);
  INLINE float get_kern() const;
  INLINE float get_current_kern();

  INLINE void set_wiggle(float wiggle);
  INLINE float get_wiggle() const;
  INLINE float get_current_wiggle();

  INLINE void set_stumble(float stumble);
  INLINE float get_stumble() const;
  INLINE float get_current_stumble();

  INLINE void set_stomp(float stomp);
  INLINE float get_stomp() const;
  INLINE float get_current_stomp();

  INLINE void set_width(float width);
  INLINE float get_width() const;

  INLINE void set_height(float height);
  INLINE float get_height() const;

  INLINE void set_flags(string flags);
  INLINE string get_flags() const;

  bool isFirstLetterOfWord(string letter);

  void reset_counter();
  void inc_counter();

  virtual void baseline_next_pos_hpr_scale(
    LVector3f &pos, LVector3f &hpr, LVector3f &scale,
    const LVector3f &size);

protected:
  string _code;
  string _flags;
  Colorf _color;
  PT(TextFont) _font;
  LVector3f _next_pos;
  LVector3f _next_hpr;
  LVector3f _next_scale;
  float _indent;
  float _kern;
  float _wiggle;
  float _stumble;
  float _stomp;
  float _total_width;
  int _counter;

  float _width;
  float _height;
  float _prior_cursor;
  float _cursor;
  bool _priorCharWasBlank;

  virtual void reset();
  void center(LVector3f &pos, LVector3f &hpr);

  // Lines:
  void line_next_pos_hpr_scale(
    LVector3f &pos, LVector3f &hpr, LVector3f &scale,
    const LVector3f &size);

  // Circles:
  void circle_next_pos_hpr_scale(
    LVector3f &pos, LVector3f &hpr, LVector3f &scale,
    const LVector3f &size);

private:
  virtual DNAGroup* make_copy();

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    DNANode::init_type();
    register_type(_type_handle, "DNASignBaseline",
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

#include "dnaSignBaseline.I"

#endif
