// Filename: dnaSignBaseline.cxx
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////

#include "dnaSignBaseline.h"
#include "dnaSign.h"
#include "dnaSignText.h"
#include "staticTextFont.h"
#include "nodePath.h"
#include "config_linmath.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNASignBaseline::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNASignBaseline::DNASignBaseline(const string &initial_name) :
  DNANode(initial_name)
{
  _code = "";
  _color.set(1.0, 1.0, 1.0, 1.0);
  _next_pos.set(0.0, 0.0, 0.0);
  _next_hpr.set(0.0, 0.0, 0.0);
  _next_scale.set(1.0, 1.0, 1.0);
  _indent = 0.0;
  _kern = 0.0;
  _wiggle = 0.0;
  _stumble = 0.0;
  _stomp = 0.0;
  _counter = 0;
  _total_width = 0.0;
  _flags = "";
  _priorCharWasBlank=true;

  _width = 0.0;
  _height = 0.0;
  _prior_cursor = 0.0;
  _cursor=0.0;
}

////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNASignBaseline::DNASignBaseline(const DNASignBaseline &signBaseline) :
  DNANode(signBaseline)
{
  _code = signBaseline.get_code();
  _color = signBaseline.get_color();
  _next_pos = signBaseline._next_pos;
  _next_hpr = signBaseline._next_hpr;
  _next_scale = signBaseline._next_scale;
  _indent = signBaseline.get_indent();
  _kern = signBaseline.get_kern();
  _wiggle = signBaseline.get_wiggle();
  _stumble = signBaseline.get_stumble();
  _stomp = signBaseline.get_stomp();
  _counter = signBaseline._counter;
  _total_width = signBaseline._total_width;
  _flags = signBaseline.get_flags();
  _priorCharWasBlank = signBaseline._priorCharWasBlank;

  _width = signBaseline.get_width();
  _height = signBaseline.get_height();
  _prior_cursor = signBaseline._prior_cursor;
  _cursor = signBaseline._cursor;
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::baseline_pos_hpr_scale
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNASignBaseline::baseline_next_pos_hpr_scale(
    LVector3f &pos, LVector3f &hpr, LVector3f &scale,
    const LVector3f &size) {
  if (_width!=0.0 || _height!=0.0) {
    circle_next_pos_hpr_scale(pos, hpr, scale, size);
  } else {
    line_next_pos_hpr_scale(pos, hpr, scale, size);
  }
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::reset
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNASignBaseline::reset() {
  _next_pos.set(0.0, 0.0, 0.0);
  _next_hpr.set(0.0, 0.0, 0.0);
  _next_scale.set(1.0, 1.0, 1.0);
  _counter = 0;
  _priorCharWasBlank=true;
  _total_width = 0.0;
  _prior_cursor = 0.0;
  _cursor = 0.0;
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::isFirstLetterOfWord
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
bool DNASignBaseline::isFirstLetterOfWord(string letter) {
  if (letter[0] == ' ') {
    _priorCharWasBlank = true;
    return false;
  } else if (_priorCharWasBlank) {
    _priorCharWasBlank=false;
    return true;
  }
  _priorCharWasBlank=false;
  return false;
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNASignBaseline::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Reset counters, etc.
  reset();

  NodePath signBaseline_node_path = parent.attach_new_node("baseline");

  if (!_code.empty()) {
    _font = store->find_font(_code);
    if (_font.is_null()) {
      dna_cat.error()
        << "unable to find baseline font " << _code << endl;
    }
  }

  //signBaseline_node_path.node()->set_name("signBaseline");

  signBaseline_node_path.set_color(_color);

  // Traverse each node in our vector
  if (_width < 0.0 || _height < 0.0) {
    // ...inner circle.
    // Reverse the order of the items:
    pvector<PT(DNAGroup)>::reverse_iterator i = _group_vector.rbegin();
    for(; i != _group_vector.rend(); ++i) {
      PT(DNAGroup) group = *i;
      NodePath np = group->traverse(signBaseline_node_path, store, editing);
    }
  } else {
    // ...line or outer circle.
    pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
    for(; i != _group_vector.end(); ++i) {
      PT(DNAGroup) group = *i;
      group->traverse(signBaseline_node_path, store, editing);
    }
  }

  // Center the text and graphics:
  LVector3f pos = _pos;
  LVector3f hpr = _hpr;
  center(pos, hpr);

  // Place the signBaseline on the sign:
  signBaseline_node_path.set_pos_hpr_scale(parent,
           pos,
           hpr,
           LVector3f(1.0));

  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(signBaseline_node_path.node(), this);
  }

  return signBaseline_node_path;
}



////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNASignBaseline::write(ostream &out,
    DNAStorage *store, int indent_level) const {
  if (_group_vector.empty()) {
    // ...no text or graphics.
    // Don't write the baseline:
    return;
  }

  indent(out, indent_level) << "baseline [\n";

  // Write out all properties
  if (!_code.empty()) {
      indent(out, indent_level + 1) << "code [ " <<
        '"' << _code << '"' << " ]\n";
  }
  if (!_color.almost_equal(LVecBase4f(1.0, 1.0, 1.0, 1.0))) {
      indent(out, indent_level + 1) << "color [ " <<
        _color[0] << " " << _color[1] << " " <<
        _color[2] << " " << _color[3] << " ]\n";
  }
  if (!_pos.almost_equal(LVecBase3f::zero())) {
    indent(out, indent_level + 1) << "pos [ " <<
      _pos[0] << " " << _pos[1] << " " <<
      _pos[2] << " ]\n";
  }
  if ((!_hpr.almost_equal(LVecBase3f::zero()))) {
    if (temp_hpr_fix) {
      indent(out, indent_level + 1) << "nhpr [ " <<
        _hpr[0] << " " << _hpr[1] << " " << _hpr[2] << " ]\n";
    } else {
      indent(out, indent_level + 1) << "hpr [ " <<
        _hpr[0] << " " << _hpr[1] << " " << _hpr[2] << " ]\n";
    }
  }
  if (!_scale.almost_equal(LVecBase3f(1.0, 1.0, 1.0))) {
    indent(out, indent_level + 1) << "scale [ " <<
      _scale[0] << " " << _scale[1] << " " <<
      _scale[2] << " ]\n";
  }
  if (_indent) {
    indent(out, indent_level + 1) << "indent [ " <<
      _indent << " ]\n";
  }
  if (_kern) {
    indent(out, indent_level + 1) << "kern [ " <<
      _kern << " ]\n";
  }
  if (_wiggle) {
    indent(out, indent_level + 1) << "wiggle [ " <<
      _wiggle << " ]\n";
  }
  if (_stumble) {
    indent(out, indent_level + 1) << "stumble [ " <<
      _stumble << " ]\n";
  }
  if (_stomp) {
    indent(out, indent_level + 1) << "stomp [ " <<
      _stomp << " ]\n";
  }
  if (_width) {
    indent(out, indent_level + 1) << "width [ " <<
      _width << " ]\n";
  }
  if (_height) {
    indent(out, indent_level + 1) << "height [ " <<
      _height << " ]\n";
  }
  if (!_flags.empty()) {
      indent(out, indent_level + 1) << "flags [ " <<
        '"' << _flags << '"' << " ]\n";
  }

  // Write all the children
  pvector<PT(DNAGroup)>::const_iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    // Traverse each node in our vector
    PT(DNAGroup) group = *i;
    group->write(out, store, indent_level + 1);
  }

  indent(out, indent_level) << "]\n";
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::center
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNASignBaseline::center(LVector3f &pos, LVector3f &hpr) {
  const float pi = 3.141592653589793;
  const float quarter_circle = pi*0.5;
  const float degrees_to_radians = pi/180.0;

  float angle;
  if (temp_hpr_fix) {
    angle = -_hpr[2]*degrees_to_radians;
  } else {
    angle = _hpr[2]*degrees_to_radians;
  }

  if (_width!=0.0 || _height!=0.0) {
    float x_radius = _width*0.5;
    float z_radius = _height*0.5;

    angle+=quarter_circle;

    float cos_ang,sin_ang;
    csincos(angle,&sin_ang,&cos_ang);

    pos[0] -= x_radius*cos_ang;
    pos[2] -= z_radius*sin_ang;

    ///hpr[2] -= _cursor*0.5;
    if (temp_hpr_fix) {
      hpr[2] += _prior_cursor*0.5;
    } else {
      hpr[2] -= _prior_cursor*0.5;
    }
  } else {
    --_counter;
    float gap_width = get_current_kern()+get_current_stumble();
    ++_counter;
    float radius = (_total_width+gap_width)*0.5;

    float cos_ang,sin_ang;
    csincos(angle,&sin_ang,&cos_ang);

    pos[0] -= radius*cos_ang;
    pos[2] -= radius*sin_ang;
  }
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::line_next_pos_hpr_scale
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNASignBaseline::line_next_pos_hpr_scale(
    LVector3f &pos, LVector3f &hpr, LVector3f &scale,
    const LVector3f &size) {
  scale[0] *= _scale[0];
  scale[1] *= _scale[1];
  scale[2] *= _scale[2];

  pos += _next_pos;
  pos[0] += get_current_kern()+get_current_stumble();
  pos[2] += get_current_stomp();

  float scaled_width = scale[0]*size[0];
  _next_pos[0] += scaled_width;
  _total_width += scaled_width;

  if (temp_hpr_fix) {
    hpr[2] -= get_current_wiggle();
  } else {
    hpr[2] += get_current_wiggle();
  }
  inc_counter();
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::circle_next_pos_hpr_scale
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNASignBaseline::circle_next_pos_hpr_scale(
    LVector3f &pos, LVector3f &hpr, LVector3f &scale,
    const LVector3f &size) {
  nassertv(!cnan(_cursor));
  const float pi = 3.141592653589793;
  const float quarter_circle = pi*0.5;
  const float degrees_to_radians = pi/180.0;
  const float radians_to_degrees = 180.0/pi;

  scale[0] *= _scale[0];
  scale[1] *= _scale[1];
  scale[2] *= _scale[2];

  float x_radius = _width*0.5;
  float z_radius = _height*0.5;

  // Make pos[0] match DNASignBaselineLine:
  float x_offset = (_width<0.0)? pos[0]: -pos[0];
  float half_circ = pi*x_radius;
  float radian_width_delta = x_offset/half_circ*pi;
  // Because indent is in degrees, we have it match hpr directions:
  float degree_delta = (_width<0.0)? -get_indent(): get_indent();
  float radian_delta = degree_delta*degrees_to_radians+radian_width_delta;
  float radian_cursor = _cursor*degrees_to_radians;
  float radian_total = radian_cursor+quarter_circle+radian_delta;

  float radius_delta = pos[2]+get_current_stomp();
  if (_width<0.0) {
    radius_delta = -radius_delta;
  }

  // Place the current item:

  float cos_ang,sin_ang;
  csincos(radian_total,&sin_ang,&cos_ang);

  float new_x = (x_radius+radius_delta)*cos_ang;
  float new_z = (z_radius+radius_delta)*sin_ang;
  pos[0] = new_x;
  pos[2] = new_z;

  nassertv(!cnan(_cursor));
  nassertv(!cnan(hpr[2]));
  if (temp_hpr_fix) {
    hpr[2] -= _cursor+degree_delta+get_current_wiggle();
  } else {
    hpr[2] += _cursor+degree_delta+get_current_wiggle();
  }
  nassertv(!cnan(hpr[2]));

  // Setup the cursor for next time:

  float hypot = csqrt(new_x*new_x+new_z*new_z);

  // Save _prior_cursor for centering:
  if (_width < 0.0) {
    _prior_cursor = radian_cursor*radians_to_degrees;
  }
  float scaled_width = scale[0]*size[0];
  radian_cursor = radian_cursor-2.0*asin(min(scaled_width/(2.0f*hypot), 1.0f));
  if (_width >= 0.0) {
    _prior_cursor = radian_cursor*radians_to_degrees;
  }

  // We subtract the get_current_stumble() so that it will more closely
  // match the stumble on a DNASignBaselineLine.
  float gap_width = get_kern()-get_current_stumble();
  radian_cursor = radian_cursor-2.0*asin(gap_width/(2.0*hypot));
  float temp_cursor = _cursor;
  nassertv(!cnan(_cursor));
  _cursor = radian_cursor*radians_to_degrees;
  nassertv(!cnan(_cursor));

  // Knock back the roll by half of the angle used for the letter.
  float knock_back=(_cursor - temp_cursor) * 0.5;
  if (_width >= 0.0) {
    if (temp_hpr_fix) {
      hpr[2] -= knock_back;
    } else {
      hpr[2] += knock_back;
    }
  } else {
    // hpr[2] -= knock_back; // inner circles seem upset.
  }

  inc_counter();
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignBaseline::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNASignBaseline::make_copy() {
  return new DNASignBaseline(*this);
}
