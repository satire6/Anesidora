// Filename: dnaSignText.cxx
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////

#include "dnaSignText.h"
#include "dnaSignBaseline.h"
#include "dnaSign.h"
#include "modelPool.h"
#include "nodePath.h"
#include "textNode.h"
#include "staticTextFont.h"
#include "decalEffect.h"
#include "config_linmath.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNASignText::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: DNASignText::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNASignText::DNASignText(const string &initial_name) :
  DNANode(initial_name)
{
  _code = "";
  _color.set(1.0, 1.0, 1.0, 1.0);
  _letters = "";
  _use_baseline_color = true;
}

////////////////////////////////////////////////////////////////////
//     Function: DNASignText::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNASignText::DNASignText(const DNASignText &signText) :
  DNANode(signText)
{
  _code = signText.get_code();
  _color = signText.get_color();
  _letters = signText.get_letters();
  _use_baseline_color = signText._use_baseline_color;
}


////////////////////////////////////////////////////////////////////
//     Function: DNASignText::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNASignText::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Make this a decal onto the baseline.  Walk up to the previous
  // GeomNode in the parent history.
  NodePath geom_parent = parent;
  PandaNode *node = geom_parent.node();
  while (!node->is_geom_node() && !geom_parent.is_singleton()) {
    geom_parent = geom_parent.get_parent();
    node = geom_parent.node();
  }
  if (node->is_geom_node()) {
    node->set_effect(DecalEffect::make());
  }

  // Try to find this signText in the node map
  // NodePath signText_node_path = parent.attach_new_node("text");

  PT(DNASignBaseline) baseline = DCAST(DNASignBaseline, get_parent());

  // Use the baseline font, if available:
  TextFont *font = (TextFont *)NULL;
  if (_code.empty()) {
    font = baseline->get_font();
  } else {
    PT(PandaNode) font_node = (store->find_node(_code)).node();
    if (!font_node) {
      dna_cat.error()
        << "unable to find SignText font " << _code << endl;
    } else {
      font = new StaticTextFont(font_node);
    }
  }
  if (font == (TextFont *)NULL && !_letters.empty()) {
    font = TextNode::get_default_font();
    if (font == (TextFont *)NULL) {
      dna_cat.error()
        << "no font specified for '" << _letters 
        << "', and no default font available.\n";
    } else {
      dna_cat.warning()
        << "no font specified for '" << _letters << "', using default font.\n";
    }
  }

  // Use the baseline color, if available:
  Colorf color = _color;
  if (_use_baseline_color) {
    color = baseline->get_color();
  }

  // Try to find this signText in the node map
  PT(TextNode) text_node = new TextNode("sign");
  text_node->set_text_color(color);
  text_node->set_font(font);
  string letters = _letters;
  // Check for upper case flag:

  if (baseline->get_flags().find('c') != string::npos) {
    // We have to uppercase this carefully, allowing for encoded text.
    TextEncoder encoder;
    encoder.set_text(letters);
    int num_chars = encoder.get_num_chars();
    for (int i = 0; i < num_chars; i++) {
      int character = encoder.get_unicode_char(i);
      encoder.set_unicode_char(i, encoder.unicode_toupper(character));
    }
  }

  // Check for drop shadow flag:
  if (baseline->get_flags().find('d') != string::npos) {
    // A black shadow is too harsh: text_node->set_shadow_color(0.0, 0.0, 0.0, 1.0);
    text_node->set_shadow_color(
      color[0]*0.3, color[1]*0.3, color[2]*0.3, color[3]*0.7);
    text_node->set_shadow(0.03, 0.03);
  }
  text_node->set_text(letters); // set the text last.

  LVector3f bl_pos = _pos;
  LVector3f bl_hpr = _hpr;
  LVector3f bl_scale = _scale;
  if ((baseline->get_flags().find('b') != string::npos)
      && (baseline->isFirstLetterOfWord(letters))) {
    bl_scale[0]*=1.5;
    bl_scale[2]*=1.5;
  }
  baseline->baseline_next_pos_hpr_scale(bl_pos, bl_hpr, bl_scale,
    LVector3f(text_node->get_width(), 0.0, text_node->get_height()));

  NodePath signText_node_path = parent.attach_new_node(text_node->generate());
  // Place the signText at the bottom center of the building,
  // three feet out from the origin where the wall is
  signText_node_path.set_pos_hpr_scale(parent,
           bl_pos,
           bl_hpr,
           bl_scale);
  // Clear parent color higher in the hierarchy
  signText_node_path.set_color_off();
  signText_node_path.set_color(color);

  // Traverse each node in our vector
  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    PT(DNAGroup) group = *i;
    group->traverse(signText_node_path, store, editing);
  }

  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(signText_node_path.node(), this);
  }

  return signText_node_path;
}



////////////////////////////////////////////////////////////////////
//     Function: DNASignText::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNASignText::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "text [\n";

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
      _pos[0] << " " << _pos[1] << " " << _pos[2] << " ]\n";
  }
  if (!_hpr.almost_equal(LVecBase3f::zero())) {
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
      _scale[0] << " " << _scale[1] << " " << _scale[2] << " ]\n";
  }
  //TODO: enquote_string(_letters), to fix output like """
  // (which is a doublequoted doublequote), and "well "hello" there!"
  if (_letters=="\"") {
    indent(out, indent_level + 1) << "letters [ '\"' ]\n";
  } else {
    indent(out, indent_level + 1) << "letters [ " <<
      '"' << _letters << '"' << " ]\n";
  }

  indent(out, indent_level) << "]\n";

}

////////////////////////////////////////////////////////////////////
//     Function: DNASignText::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNASignText::make_copy() {
  return new DNASignText(*this);
}
