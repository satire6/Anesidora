// Filename: chatBalloon.cxx
// Created by:  drose (23Jul01)
//
////////////////////////////////////////////////////////////////////

#include "chatBalloon.h"
#include "config_nametag.h"
#include "nametagGlobals.h"

#include "pandaNode.h"
#include "modelNode.h"
#include "nodePath.h"
#include "transparencyAttrib.h"
#include "textNode.h"
#include "colorAttrib.h"
#include "decalEffect.h"
#include "transformState.h"
#include "sceneGraphReducer.h"
#include "cullBinAttrib.h"
#include "cullFaceAttrib.h"

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::Constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
ChatBalloon::
ChatBalloon(PandaNode *root_node) {
  _hscale = 0.0f;
  _text_height = 0.0f;
  _text_frame.set(0.0f, 0.0f, 0.0f, 0.0f);

  bool found_geom = scan(root_node);
  nassertv(found_geom);
}

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::Destructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
ChatBalloon::
~ChatBalloon() {
}

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::generate
//       Access: Public
//  Description: Generates a new subgraph representing the text in the
//               indicated TextNode framed within the balloon.
//
//               If for_3d is true, the text will be decalled onto the
//               balloon geometry; otherwise, it will simply be
//               parented so that it will be rendered second (in the
//               2-d scene graph).
//
//               If has_draw_order is true, the geometry will be
//               assigned to the fixed bin with the indicated
//               draw_order.
////////////////////////////////////////////////////////////////////
PT(PandaNode) ChatBalloon::
generate(const string &text, TextFont *font, float wordwrap,
         const Colorf &text_color, const Colorf &balloon_color,
         bool for_3d, bool has_draw_order, int draw_order,
         const NodePath &page_button, bool space_for_button,
         bool reversed, NodePath &new_button) {
  // First, create a node to parent everything to.
  PT(PandaNode) root = new PandaNode("chat");

  // No point in backface culling a chat balloon, since it will always
  // face the camera.
  root->set_attrib(CullFaceAttrib::make(CullFaceAttrib::M_cull_none));

  // First, set up the text.
  TextNode *text_node = NametagGlobals::get_text_node();
  text_node->set_font(font);
  text_node->set_wordwrap(wordwrap);
  text_node->set_align(TextNode::A_left);
  text_node->set_text(text);

  // How does the text fit within the balloon?
  float xoffset = NametagGlobals::balloon_text_origin[0];
  if (reversed) {
    xoffset += NametagGlobals::balloon_internal_width;
  }
  _hscale = text_node->get_width() / NametagGlobals::balloon_internal_width;
  if (_hscale < NametagGlobals::balloon_min_hscale) {
    // If our text is too narrow, center it instead of left-justifying.
    _hscale = NametagGlobals::balloon_min_hscale;
    text_node->set_align(TextNode::A_center);
    if (reversed) {
      xoffset -= NametagGlobals::balloon_internal_width * 0.5f;
    } else {
      xoffset += NametagGlobals::balloon_internal_width * 0.5f;
    }
  }

  if (reversed) {
    _hscale = -_hscale;
  }

  _text_frame = text_node->get_card_actual();

  // Determine how to transform the pieces of the chat balloon
  // appropriately to fit the text.
  float button_space = 0.0f;
  if (space_for_button) {
    button_space = 0.2f;
  }

  int num_lines = max(text_node->get_num_rows(), 1);
  float line_height = text_node->get_line_height();
  _text_height = num_lines * line_height + button_space;
  float text_height_below = (num_lines - 1) * line_height + button_space;

  // Scale the overall balloon to be as wide as the text.
  LMatrix4f parent_mat = LMatrix4f::scale_mat(_hscale, 1.0f, 1.0f);

  // Scale the middle part of the balloon to be as tall as the text.
  LMatrix4f middle_mat =
    LMatrix4f::scale_mat(1.0f, 1.0f, _text_height) *
    _middle_mat;

  // Translate the top part to match the middle.
  LMatrix4f top_mat =
    LMatrix4f::translate_mat(0.0f, 0.0f, _text_height - 1.0f) * _top_mat;

  // Position the text within the balloon.
  LVector3f text_trans(xoffset * _hscale, 0.0f,
                       NametagGlobals::balloon_text_origin[2] + text_height_below + 0.2f);
  _text_frame.set(_text_frame[0] + text_trans[0],
                  _text_frame[1] + text_trans[0],
                  _text_frame[2] + text_trans[2],
                  _text_frame[3] + text_trans[2]);

  // Now apply the various transforms and copy in the pieces.

  if (_top_node != (PandaNode *)NULL) {
    _top_node->set_transform(TransformState::make_mat(top_mat));
  }
  if (_middle_node != (PandaNode *)NULL) {
    _middle_node->set_transform(TransformState::make_mat(middle_mat));
  }

  PT(PandaNode) parent = _parent->copy_subgraph();
  root->add_child(parent);
  parent->set_transform(TransformState::make_mat(parent_mat));

  if (has_draw_order) {
    parent->set_attrib(CullBinAttrib::make(nametag_fixed_bin, draw_order));
  }

  parent->set_attrib(ColorAttrib::make_flat(balloon_color));
  if (balloon_color[3] != 1.0f) {
    parent->set_attrib(TransparencyAttrib::make(TransparencyAttrib::M_alpha));
  }

  // Apply the transforms to the balloon vertices, and flatten into
  // one Geom if possible.
  SceneGraphReducer reducer;
  reducer.apply_attribs(parent);
  reducer.flatten(root, ~0);

  // parent is now invalid, because it might have been flattened out.
  parent = (PandaNode *)NULL;

  // Now generate the actual text geometry.
  PT(PandaNode) text_geom_node = text_node->generate();
  text_node->clear_text();

  PandaNode *text_parent_node = (PandaNode *)NULL;

  if (for_3d) {
    // If this is to be a 3-d chat balloon, we have to decal the text
    // onto the middle piece.
    text_parent_node = find_middle_geom(root);
    if (text_parent_node == (PandaNode *)NULL) {
      // If there's no "middle", probably it was flattened out.  Just
      // use whatever GeomNode we can find.
      text_parent_node = find_geom_node(root);
    }
    nassertr(text_parent_node != (PandaNode *)NULL, root);
    text_parent_node->set_effect(DecalEffect::make());

  } else {
    text_parent_node = root;
    if (has_draw_order) {
      text_geom_node->set_attrib(CullBinAttrib::make(nametag_fixed_bin, draw_order + 1));
    }
  }

  nassertr(text_parent_node != (PandaNode *)NULL, root);
  NodePath text_parent(text_parent_node);
  NodePath text_geom = text_parent.attach_new_node(text_geom_node);

  text_geom.set_pos(text_trans);
  text_geom.set_color(text_color);
  if (text_color[3] != 1.0f) {
    text_geom.set_transparency(TransparencyAttrib::M_alpha);
  }

  if (!page_button.is_empty()) {
    // Put the page button, if we have one, with the text.
    PT(ModelNode) new_button_node = new ModelNode("button");
    new_button = text_parent.attach_new_node(new_button_node);
    NodePath button = page_button.copy_to(new_button);

    if (reversed) {
      button.set_pos(_hscale * 1.7f, 0.0f, 1.8f);
    } else {
      float balloon_width =
        _hscale * NametagGlobals::balloon_internal_width;
      button.set_pos(balloon_width, 0.0f, 1.8f);
    }
    button.set_scale(8.0f);
  }

  // Apply the transforms to the text vertices too, and flatten once more.
  reducer.apply_attribs(text_geom_node);
  reducer.flatten(root, true);

  return root;
}

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::scan
//       Access: Private
//  Description: Recursively scans the indicated hierarchy until a
//               node named "chatBalloon" is found.  Returns true if
//               the node and its three children are found, false
//               otherwise.
////////////////////////////////////////////////////////////////////
bool ChatBalloon::
scan(PandaNode *node) {
  if (node->get_name() == "chatBalloon") {
    return scan_balloon(node);
  }

  int num_children = node->get_num_children();
  for (int i = 0; i < num_children; i++) {
    PandaNode *child = node->get_child(i);
    if (scan(child)) {
      return true;
    }
  }

  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::scan_balloon
//       Access: Private
//  Description: Once the "chatBalloon" node is found, gets the three
//               children out of it.
////////////////////////////////////////////////////////////////////
bool ChatBalloon::
scan_balloon(PandaNode *node) {
  _parent = node->copy_subgraph();
  _top_node = (PandaNode *)NULL;
  _middle_node = (PandaNode *)NULL;
  _bottom_node = (PandaNode *)NULL;

  int num_children = _parent->get_num_children();
  for (int i = 0; i < num_children; i++) {
    PandaNode *child = _parent->get_child(i);
    const string &name = child->get_name();

    if (name == "top") {
      _top_node = child;
      _top_mat = child->get_transform()->get_mat();

    } else if (name == "middle") {
      _middle_node = child;
      _middle_mat = child->get_transform()->get_mat();

    } else if (name == "bottom") {
      _bottom_node = child;
    }
  }

  if (_top_node == (PandaNode *)NULL ||
      _middle_node == (PandaNode *)NULL ||
      _bottom_node == (PandaNode *)NULL) {
    nametag_cat.error()
      << "ChatBalloon geometry does not include top, middle, and bottom nodes.\n";
    return false;
  }

  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::find_middle_geom
//       Access: Private, Static
//  Description: Returns the GeomNode below the first child node found
//               named "middle", if there is such a thing.
////////////////////////////////////////////////////////////////////
PandaNode *ChatBalloon::
find_middle_geom(PandaNode *parent) {
  int num_children = parent->get_num_children();
  for (int i = 0; i < num_children; i++) {
    PandaNode *child = parent->get_child(i);
    const string &name = child->get_name();

    if (name == "middle") {
      // Here's a child named "middle"; now let's go down to the first
      // GeomNode below that.
      return find_geom_node(child);
    }

    PandaNode *result = find_middle_geom(child);
    if (result != (PandaNode *)NULL) {
      return result;
    }
  }

  return (PandaNode *)NULL;
}

////////////////////////////////////////////////////////////////////
//     Function: ChatBalloon::find_geom_node
//       Access: Private, Static
//  Description: Returns the first GeomNode at or below this level.
////////////////////////////////////////////////////////////////////
PandaNode *ChatBalloon::
find_geom_node(PandaNode *parent) {
  if (parent->is_geom_node()) {
    return parent;
  }

  int num_children = parent->get_num_children();
  for (int i = 0; i < num_children; i++) {
    PandaNode *found = find_geom_node(parent->get_child(i));
    if (found != (PandaNode *)NULL) {
      return found;
    }
  }

  // Nothing.
  return (PandaNode *)NULL;
}
