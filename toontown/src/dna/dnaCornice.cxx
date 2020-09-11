// Filename: dnaCornice.cxx
// Created by:  shochet (28Mar00)
//
////////////////////////////////////////////////////////////////////

#include "dnaCornice.h"
#include "nodePath.h"

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNACornice::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: DNACornice::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNACornice::DNACornice(const string &initial_name) :
  DNAGroup(initial_name)
{
  _code = "";
  _color.set(1.0, 1.0, 1.0, 1.0);
}

////////////////////////////////////////////////////////////////////
//     Function: DNACornice::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNACornice::DNACornice(const DNACornice &cornice) :
  DNAGroup(cornice)
{
  _code = cornice.get_code();
  _color = cornice.get_color();
}


////////////////////////////////////////////////////////////////////
//     Function: DNACornice::set_color
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNACornice::set_color(const Colorf &color) {
  _color = color;
}


////////////////////////////////////////////////////////////////////
//     Function: DNACornice::get_color
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
Colorf DNACornice::get_color() const {
  return _color;
}


////////////////////////////////////////////////////////////////////
//     Function: DNACornice::set_code
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
void DNACornice::set_code(string code) {
  _code = code;
}


////////////////////////////////////////////////////////////////////
//     Function: DNACornice::get_code
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
string DNACornice::get_code() const {
  return _code;
}


////////////////////////////////////////////////////////////////////
//     Function: DNACornice::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNACornice::traverse(NodePath &parent, DNAStorage *store, int editing) {
  float height = parent.get_sz();
  float width = parent.get_parent().get_sx();
  float z = current_wall_height + height;

  // Try to find this cornice in the node map
  NodePath cornice_node_path = (store->find_node(_code));

  // Find the part of the cornice that should be decalled to the wall
  NodePath cornice_node_path_d = (cornice_node_path.find("**/*_d")).copy_to(parent);

  // Since the width is already scaled, we need to compensate on the
  // cornice in the other 2 axes. Also, we need to divide out the height
  // scale that the wall above us has

  // Place the cornice at the top of the flat building
  cornice_node_path_d.set_pos_hpr_scale(LVector3f(0.0, 0.0, 1.0),
          LVector3f(0.0),
          LVector3f(1.0, (width / height), (width / height)));
  cornice_node_path_d.set_color(_color);

  // The top part of the cornice should not be decalled so
  // parent it to the flat wall (our grandparent)
  NodePath cornice_node_path_nd = (cornice_node_path.find("**/*_nd")).copy_to(parent.get_parent());

  // Since the width is already scaled, we need to compensate on the
  // cornice in the other 2 axes. Also, we do NOT need to divide out the height
  // since this non-decal portion is parented above the node with the height scale

  // Place the cornice at the top of the flat building
  cornice_node_path_nd.set_pos_hpr_scale(LVector3f(0.0, 0.0, z),
                                         LVector3f(0.0),
                                         LVector3f(1.0, width, width));

  cornice_node_path_nd.set_color(_color);

  if (editing) {
    // Remember that this nodepath is associated with this dna group
    // Well, which nodePath should we store? The decal or not?
    // Not sure there is a good answer here. Mark says use the bottom part.
    store->store_DNAGroup(cornice_node_path_d.node(), this);
  }

  // We don't traverse our children because there will not be any

  // Well, which nodePath should we return? The decal or not?
  // Not sure there is a good answer here either.
  return cornice_node_path_d;
}



////////////////////////////////////////////////////////////////////
//     Function: DNACornice::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNACornice::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "cornice [\n";

  // Write out all properties
  indent(out, indent_level + 1) << "code [ " <<
    '"' << _code << '"' << " ]\n";
  indent(out, indent_level + 1) << "color [ " <<
    _color[0] << " " << _color[1] << " " << _color[2] << " " << _color[3] <<
    " ]\n";

  // We dont traverse our children because we do not have any
  indent(out, indent_level) << "]\n";

}

////////////////////////////////////////////////////////////////////
//     Function: DNACornice::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNACornice::make_copy() {
  return new DNACornice(*this);
}
