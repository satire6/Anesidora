// Filename: dnaStreet.cxx
// Created by:  shochet (26May00)
//
////////////////////////////////////////////////////////////////////


#include "dnaStreet.h"
#include "dnaStorage.h"
#include "pandaNode.h"
#include "pointerTo.h"
#include "compose_matrix.h"
#include "config_linmath.h"
#include "luse.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNAStreet::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: DNAStreet::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAStreet::DNAStreet(const string &initial_name) :
  DNANode(initial_name)
{
  _code = "";
  _street_texture = "";
  _sidewalk_texture = "";
  _curb_texture = "";
  _street_color.set(1.0, 1.0, 1.0, 1.0);
  _sidewalk_color.set(1.0, 1.0, 1.0, 1.0);
  _curb_color.set(1.0, 1.0, 1.0, 1.0);
}

////////////////////////////////////////////////////////////////////
//     Function: DNAStreet::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAStreet::DNAStreet(const DNAStreet &street) :
  DNANode(street)
{
  _code = street.get_code();
  _street_texture = street.get_street_texture();
  _sidewalk_texture = street.get_sidewalk_texture();
  _curb_texture = street.get_curb_texture();
  _street_color = street.get_street_color();
  _sidewalk_color = street.get_sidewalk_color();
  _curb_color = street.get_curb_color();
}


////////////////////////////////////////////////////////////////////
//     Function: DNAStreet::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNAStreet::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Try to find this street in the node map
  NodePath street_node_path = (store->find_node(_code)).copy_to(parent);
  nassertr(!street_node_path.is_empty(), street_node_path);
  street_node_path.node()->set_name(get_name());

  // Find the street and sidewalk texture in dna storage
  PT(Texture) street_texture = store->find_texture(_street_texture);
  PT(Texture) sidewalk_texture = store->find_texture(_sidewalk_texture);
  PT(Texture) curb_texture = store->find_texture(_curb_texture);

  NodePath street_street = street_node_path.find("**/*_street");
  NodePath street_sidewalk = street_node_path.find("**/*_sidewalk");
  NodePath street_curb = street_node_path.find("**/*_curb");

  // Set the textures and colors
  if (!street_street.is_empty()) {
    // we call set_texture() with a small override to force the
    // texture to replace whatever is already on the Geoms.
    street_street.set_texture(street_texture, 1);
    street_street.set_color_scale(_street_color);
  };
  if (!street_sidewalk.is_empty()) {
    street_sidewalk.set_texture(sidewalk_texture, 1);
    street_sidewalk.set_color_scale(_sidewalk_color);
  };
  if (!street_curb.is_empty()) {
    street_curb.set_texture(curb_texture, 1);
    street_curb.set_color_scale(_curb_color);
  };

  street_node_path.set_pos_hpr_scale(_pos, _hpr, _scale);

  // Do not traverse because we do not have children

  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(street_node_path.node(), this);
  }

  return street_node_path;
}



////////////////////////////////////////////////////////////////////
//     Function: DNAStreet::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNAStreet::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "street ";
  out << '"' << get_name() << '"' << " [\n";

  // Write out all properties
  indent(out, indent_level + 1) << "code [ " <<
    '"' << _code << '"' << " ]\n";
  indent(out, indent_level + 1) << "pos [ " <<
    _pos[0] << " " << _pos[1] << " " << _pos[2] << " ]\n";
  if (temp_hpr_fix) {
    indent(out, indent_level + 1) << "nhpr [ " <<
      _hpr[0] << " " << _hpr[1] << " " << _hpr[2] << " ]\n";
  } else {
    indent(out, indent_level + 1) << "hpr [ " <<
      _hpr[0] << " " << _hpr[1] << " " << _hpr[2] << " ]\n";
  }

  // Only write out color if it is not white. This saves unnecessary work
  if ((!_street_color.almost_equal(LVecBase4f(1.0, 1.0, 1.0, 1.0))) ||
      (!_sidewalk_color.almost_equal(LVecBase4f(1.0, 1.0, 1.0, 1.0))) ||
      (!_curb_color.almost_equal(LVecBase4f(1.0, 1.0, 1.0, 1.0)))) {
    indent(out, indent_level + 1) << "color [ " <<
      _street_color[0] << " " << _street_color[1] << " " << _street_color[2] << " " << _street_color[3] <<
      " ]\n";
    indent(out, indent_level + 1) << "color [ " <<
      _sidewalk_color[0] << " " << _sidewalk_color[1] << " " << _sidewalk_color[2] << " " << _sidewalk_color[3] <<
      " ]\n";
    indent(out, indent_level + 1) << "color [ " <<
      _curb_color[0] << " " << _curb_color[1] << " " << _curb_color[2] << " " << _curb_color[3] <<
      " ]\n";
  }


  indent(out, indent_level + 1) << "texture [ " <<
    '"' << _street_texture << '"' << " ]\n";
  indent(out, indent_level + 1) << "texture [ " <<
    '"' << _sidewalk_texture << '"' << " ]\n";
  indent(out, indent_level + 1) << "texture [ " <<
    '"' << _curb_texture << '"' << " ]\n";

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
//     Function: DNAStreet::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNAStreet::make_copy() {
  return new DNAStreet(*this);
}
