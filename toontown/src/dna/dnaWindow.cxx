// Filename: dnaWindow.cxx
// Created by:  shochet (11Jun00)
//
////////////////////////////////////////////////////////////////////

#include "dnaWindow.h"
#include "dnaStorage.h"
#include "dnaBuildings.h"
#include "nodePath.h"
#include "compose_matrix.h"
#include "luse.h"
#include "decalEffect.h"
#include <stdlib.h>

////////////////////////////////////////////////////////////////////
// Static variables
////////////////////////////////////////////////////////////////////
TypeHandle DNAWindows::_type_handle;

// Jitter values for the windows pos hpr and scale to give them some character
float pos_jitter = 0.025;
float pos_jitter_div_2 = (pos_jitter / 2.0);
float hpr_jitter = 6.0;
float hpr_jitter_div_2 = (hpr_jitter / 2.0);
float scale_jitter = 0.025;
float scale_jitter_div_2 = (scale_jitter / 2.0);

#define rand_pos_jitter ((rand()/(RAND_MAX+1.0) * pos_jitter) - pos_jitter_div_2)
#define rand_hpr_jitter ((rand()/(RAND_MAX+1.0) * hpr_jitter) - hpr_jitter_div_2)
#define rand_scale_jitter ((rand()/(RAND_MAX+1.0) * scale_jitter) - scale_jitter_div_2)

////////////////////////////////////////////////////////////////////
//     Function: DNAWindows::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAWindows::DNAWindows(const string &initial_name) :
  DNAGroup(initial_name)
{
  _code = "";
  _window_count = 1;
  _color.set(1.0, 1.0, 1.0, 1.0);
}

////////////////////////////////////////////////////////////////////
//     Function: DNAWindows::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
DNAWindows::DNAWindows(const DNAWindows &windows) :
  DNAGroup(windows)
{
  _code = windows.get_code();
  _window_count = windows.get_window_count();
  _color = windows.get_color();
}


////////////////////////////////////////////////////////////////////
//     Function: DNAWindows::traverse
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
NodePath DNAWindows::traverse(NodePath &parent, DNAStorage *store, int editing) {

  // No windows
  if (_window_count == 0) {
    return parent;
  }

  // Ok you have windows

  NodePath window_node_path;

  // Check the width of the flat building (your grandparent)
  float width = parent.get_parent().get_sx();

  // Position is set in the case statement. hpr and scale are computed here
  LVector3f hpr;
  hpr.set(0.0, 0.0, rand_hpr_jitter);

  // Smaller walls get smaller windows
  LVector3f scale;
  if (width <= 5.0) {
    scale.fill(1.0 + rand_scale_jitter);
  } else if (width <= 10.0) {
    scale.fill(1.15 + rand_scale_jitter);
  } else {
    scale.fill(1.3 + rand_scale_jitter);
  };

  // 1 window, center it
  if (_window_count == 1) {
    // Parent the new windows node to the parent
    window_node_path = (store->find_node(_code)).copy_to(parent);
    // window_node_path.node()->set_name("window");
    // Set the colors
    window_node_path.set_color(_color);

    // Position the window
    window_node_path.set_scale(NodePath(), scale);
    window_node_path.set_pos(LVector3f((0.5 + rand_pos_jitter),
                                       0.0,
                                       (0.5 + rand_pos_jitter)));
    window_node_path.set_hpr(hpr);
  }

  // 2 windows, center them and mirror them to face each other
  else if (_window_count == 2) {
    int code_size = _code.size();
    string mirror_code;
    for (int i=1; i <= _window_count; i++) {
      if (i == 1) {
        // left window
        mirror_code = _code.replace(code_size - 2, code_size, "ur");
      } else if (i == 2) {
        // right window
        mirror_code = _code.replace(code_size - 2, code_size, "ul");
      }
      // Parent the new windows node to the parent
      window_node_path = (store->find_node(mirror_code)).copy_to(parent);
      // window_node_path.node()->set_name("window");
      // Set the colors
      window_node_path.set_color(_color);

      // Position the window
      window_node_path.set_scale(NodePath(), scale);
      window_node_path.set_pos(LVector3f(((i / (float)(_window_count+1)) + rand_pos_jitter),
                                         0.0,
                                         (0.5 + rand_pos_jitter)));
      window_node_path.set_hpr(hpr);
    }
  }


  // 3 windows, place them 2 on top, one on bottom
  else if (_window_count == 3) {
    for (int i=1; i <= _window_count; i++) {

      // Parent the new windows node to the parent
      window_node_path = (store->find_node(_code)).copy_to(parent);
      // window_node_path.node()->set_name("window");
      // Set the colors
      window_node_path.set_color(_color);

      // Position the window
      window_node_path.set_scale(NodePath(), scale);
      if (i == 1) {
        window_node_path.set_pos(LVector3f(0.33 + rand_pos_jitter, 0.0, 0.66 + rand_pos_jitter));
      } else if (i == 2) {
        window_node_path.set_pos(LVector3f(0.5 + rand_pos_jitter, 0.0, 0.33 + rand_pos_jitter));
      } else if (i == 3) {
        window_node_path.set_pos(LVector3f(0.66 + rand_pos_jitter, 0.0, 0.66 + rand_pos_jitter));
      }
      window_node_path.set_hpr(hpr);
    }
  }

  // 4 windows, place 2 on top, 2 on bottom
  else if (_window_count == 4) {
    for (int i=1; i <= _window_count; i++) {

      // Parent the new windows node to the parent
      window_node_path = (store->find_node(_code)).copy_to(parent);
      // node_path.node()->set_name("window");
      // Set the colors
      window_node_path.set_color(_color);

      // Position the window
      window_node_path.set_scale(NodePath(), scale);
      if (i == 1) {
        window_node_path.set_pos(LVector3f(0.33 + rand_pos_jitter, 0.0, 0.75 + rand_pos_jitter));
      } else if (i == 2) {
        window_node_path.set_pos(LVector3f(0.66 + rand_pos_jitter, 0.0, 0.75 + rand_pos_jitter));
      } else if (i == 3) {
        window_node_path.set_pos(LVector3f(0.33 + rand_pos_jitter, 0.0, 0.25 + rand_pos_jitter));
      } else if (i == 4) {
        window_node_path.set_pos(LVector3f(0.66 + rand_pos_jitter, 0.0, 0.25 + rand_pos_jitter));
      }

      window_node_path.set_hpr(hpr);
    }
  }

  if (editing) {
    // Make this a decal onto the walls
    PandaNode *node = parent.node();
    node->set_effect(DecalEffect::make());
    // Remember that this nodepath is associated with this dna group
    store->store_DNAGroup(window_node_path.node(), this);
  }

  return parent;
}


////////////////////////////////////////////////////////////////////
//     Function: DNAWindows::write
//       Access: Public
//  Description: Writes the group and all children to output
////////////////////////////////////////////////////////////////////
void DNAWindows::write(ostream &out, DNAStorage *store, int indent_level) const {
  indent(out, indent_level) << "windows [\n";

  // Write out all properties
  indent(out, indent_level + 1) << "code [ " <<
    '"' << _code << '"' << " ]\n";
  indent(out, indent_level + 1) << "color [ " <<
    _color[0] << " " << _color[1] << " " << _color[2] << " " << _color[3] <<
    " ]\n";
  indent(out, indent_level + 1) << "count [ " << _window_count << " ]\n";

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
//     Function: DNAWindows::make_copy
//       Access: Public
//  Description: Copies all the children into our own vector
////////////////////////////////////////////////////////////////////
DNAGroup* DNAWindows::make_copy() {
  return new DNAWindows(*this);
}
