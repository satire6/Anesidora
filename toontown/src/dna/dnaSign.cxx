// Filename: dnaSign.cxx
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////

#include "dnaSign.h"
#include "nodePath.h"
#include "decalEffect.h"
#include "sceneGraphReducer.h"
#include "config_linmath.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNASign::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: DNASign::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNASign::DNASign(const string &initial_name) :
  DNANode(initial_name)
{
  _code = "";
  _color.set(1.0, 1.0, 1.0, 1.0);
}

////////////////////////////////////////////////////////////////////
//     Function: DNASign::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNASign::DNASign(const DNASign &sign) :
  DNANode(sign)
{
  _code = sign.get_code();
  _color = sign.get_color();
}


////////////////////////////////////////////////////////////////////
//     Function: DNASign::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNASign::traverse(NodePath &parent, DNAStorage *store, int editing) {
  // Make this a decal onto the wall

  // First look for a node called sign_decal
  // If it is there, use it otherwise just use the _front node like the door does
  NodePath building_front = parent.find("**/sign_decal");
  if (building_front.is_empty()) {
    building_front = parent.find("**/*_front");
  }

  nassertr(!building_front.is_empty(), parent);

  // If the _front is not a GeomNode, look for the first geom node under that
  if (!building_front.node()->is_geom_node()) {
    building_front = building_front.find("**/+GeomNode");
    nassertr(!building_front.is_empty(), parent);
  }

  PandaNode *node = building_front.node();
  node->set_effect(DecalEffect::make());

  // Try to find this sign in the node map
  NodePath sign_node_path;
  if (!_code.empty()) {
    sign_node_path = (store->find_node(_code)).copy_to(building_front);
    if (sign_node_path.is_empty()) {
      nout << "Sign not found in storage: " << _code << endl;
      return parent;
    }
    sign_node_path.node()->set_name("sign");
  } else {
    sign_node_path = building_front.attach_new_node(new ModelNode("sign"));
  }
  nassertr(!sign_node_path.is_empty(), parent);

  // Turn off the writing of z-buffer information:
  sign_node_path.set_depth_write(0);
  //sign_node_path.node()->set_name("sign");

  // The Sign_origin is a special node in the model with a local
  // origin that we position the sign wrt
  NodePath sign_origin = parent.find("**/*sign_origin");
  nassertr(!sign_origin.is_empty(), parent);

  // Place the sign on the building:
  sign_node_path.set_pos_hpr_scale(sign_origin, _pos, _hpr, _scale);
  sign_node_path.set_color(_color);

  // Traverse each node in our vector
  pvector<PT(DNAGroup)>::iterator i = _group_vector.begin();
  for(; i != _group_vector.end(); ++i) {
    PT(DNAGroup) group = *i;
    group->traverse(sign_node_path, store, editing);
  }
  if (editing) {
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(sign_node_path.node(), this);
  } else {
    // Remember the sign origin for later.  For this we have to find
    // the building node, which is usually parent, but might be
    // farther up.
    NodePath building = parent;
    while (!building.is_empty() && 
           (building.get_name().empty() ||
            building.get_name().substr(0, 2) != "tb")) {
      building = building.get_parent();
    }
    // We only want do this is we have found a building and it is a landmark building (avoids billboards)
    if ((!building.is_empty()) && strstr(building.get_name().c_str(), "landmark") != 0) {
      string block=store->get_block(building.get_name());
      store->store_block_sign_transform(block, sign_origin.get_transform(building)->get_mat());
    }

    // Get rid of the transitions and flatten
    if (!sign_node_path.is_empty()) {
      SceneGraphReducer gr;
      gr.apply_attribs(sign_node_path.node());
      gr.flatten(sign_node_path.node(), ~0);
    }
  }
  return sign_node_path;
}


////////////////////////////////////////////////////////////////////
//     Function: DNASign::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNASign::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "sign [\n";

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
//     Function: DNASign::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNASign::make_copy() {
  return new DNASign(*this);
}
