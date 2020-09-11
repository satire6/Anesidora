// Filename: nametag2d.cxx
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#include "nametag2d.h"
#include "nametag3d.h"
#include "nametagGroup.h"
#include "nametagGlobals.h"
#include "marginManager.h"
#include "chatFlags.h"
#include "config_nametag.h"

#include "colorAttrib.h"
#include "transformState.h"
#include "compose_matrix.h"
#include "sceneGraphReducer.h"
#include "cardMaker.h"
#include "cullBinAttrib.h"
#include "transparencyAttrib.h"
#include "nodePath.h"
#include "deg_2_rad.h"
#include "cmath.h"
#include "pStatTimer.h"

TypeHandle Nametag2d::_type_handle;

#ifndef CPPPARSER
PStatCollector Nametag2d::_contents_pcollector("App:Show code:Nametags:2d:Contents");
PStatCollector Nametag2d::_adjust_pcollector("App:Show code:Nametags:2d:Adjust");
#endif

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
Nametag2d::
Nametag2d() : Nametag(NametagGlobals::chat_2d_wordwrap) {
#ifdef DO_MEMORY_USAGE
  MemoryUsage::update_type(this, this);
#endif
  set_cull_callback();

  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Creating Nametag2d " << (void *)this << "\n";
  }
  set_name("unnamed");

  /*
  // For now, the default is to have a draw order of 2000 on Nametag2d
  // objects.  This enables us to be parented directly to aspect2d and
  // still render correctly.
  set_draw_order(2000);
  */

  // By default, Nametag2d objects don't display thoughts.
  set_contents(C_name | C_speech);

  _master_arrows = NametagGlobals::get_master_arrows_on();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::Destructor
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
Nametag2d::
~Nametag2d() {
  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Destructing Nametag2d " << (void *)this << ": "
      << get_name() << "\n";
  }

  stop_flash();
  _name.remove_node();
  _card.remove_node();
  _arrow.remove_node();
  _balloon.remove_node();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::cull_callback
//       Access: Public, Virtual
//  Description: This function will be called during the cull
//               traversal to perform any additional operations that
//               should be performed at cull time.  This may include
//               additional manipulation of render state or additional
//               visible/invisible decisions, or any other arbitrary
//               operation.
//
//               Note that this function will *not* be called unless
//               set_cull_callback() is called in the constructor of
//               the derived class.  It is necessary to call
//               set_cull_callback() to indicated that we require
//               cull_callback() to be called.
//
//               By the time this function is called, the node has
//               already passed the bounding-volume test for the
//               viewing frustum, and the node's transform and state
//               have already been applied to the indicated
//               CullTraverserData object.
//
//               The return value is true if this node should be
//               visible, or false if it should be culled.
////////////////////////////////////////////////////////////////////
bool Nametag2d::
cull_callback(CullTraverser *, CullTraverserData &) {
  PStatTimer timer(_adjust_pcollector);
  rotate_arrow();

  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::get_score
//       Access: Public, Virtual
//  Description: Returns a number representing how much this
//               particular MarginPopup deserves to be onscreen.
//               This is used to resolve conflicts when there are too
//               many MarginPopups that all want to be onscreen
//               simultaneously.  The larger the number, the more
//               likely this particular popup is to be made visible.
////////////////////////////////////////////////////////////////////
float Nametag2d::
get_score() {
  if (!has_group()) {
    // No group, score of 0.
    return 0.0f;
  }

  // If the Nametag2d is in the "name" state, its score is entirely
  // based on the square of the distance of the avatar from the toon.
  float distance2 = get_distance2();

  // The greater the distance, the lower the score.  The closest
  // avatars get a score of 1000.
  return 1000.0f - distance2;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::get_object_code
//       Access: Public, Virtual
//  Description: Returns an integer that represents a uniquifying code
//               for this popup.  If the code is nonzero, then of any
//               two popups that are simultaneously onscreen and share
//               the same unique code, only the one with the highest
//               score will actually be shown.  This is intended to
//               prevent display of multiple nametags that refer to
//               the same object.
////////////////////////////////////////////////////////////////////
int Nametag2d::
get_object_code() {
  if (has_group()) {
    NametagGroup *group = get_group();
    return group->get_object_code();
  } else {
    return 0;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::update_contents
//       Access: Protected, Virtual
//  Description: Recomputes the Nametag according to its
//               NametagGroup's current state.
////////////////////////////////////////////////////////////////////
void Nametag2d::
update_contents() {
  PStatTimer timer(_contents_pcollector);
  stop_flash();

  if (has_group()) {
    NametagGroup *group = get_group();
    set_name(group->get_name());
  } else {
    set_name("unnamed");
  }

  _name.remove_node();
  _card.remove_node();
  _arrow.remove_node();
  _balloon.remove_node();

  _current_contents = determine_contents();
  if (!NametagGlobals::get_master_arrows_on()) {
    _current_contents &= ~C_name;
  }

  if (is_visible() && is_group_managed()) {
    if ((_current_contents & C_speech) != 0) {
      generate_chat(NametagGlobals::get_speech_balloon_2d());
    } else if ((_current_contents & C_thought) != 0) {
      generate_chat(NametagGlobals::get_thought_balloon_2d());
    } else if ((_current_contents & C_name) != 0) {
      generate_name();
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::manage
//       Access: Protected, Virtual
//  Description: This is called only by NametagGroup::manage().
////////////////////////////////////////////////////////////////////
void Nametag2d::
manage(MarginManager *manager) {
  Nametag::manage(manager);
  manager->manage_popup(this);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::unmanage
//       Access: Protected, Virtual
//  Description: This is called only by NametagGroup::unmanage().
////////////////////////////////////////////////////////////////////
void Nametag2d::
unmanage(MarginManager *manager) {
  Nametag::unmanage(manager);
  manager->unmanage_popup(this);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::frame_callback
//       Access: Protected, Virtual
//  Description: This is called exactly once every frame by the
//               MarginManager for each managed popup, whether the
//               popup is visible or not.  It does whatever the popup
//               might need to do once per frame.
////////////////////////////////////////////////////////////////////
void Nametag2d::
frame_callback() {
  // If we were visible last time, we must have had an active region,
  // and we will want to keep that region.
  if (is_visible()) {
    keep_region();
  }

  // The tail wags the dog a bit here: we'll tell the NametagGroup to
  // fire off its once-a-frame check that the MouseWatcherRegions in
  // effect are still current.  Somebody has to do it.  This assumes
  // that the Nametag2d's consider_visible() function gets called
  // exactly once each frame, and ideally towards the end of the
  // frame.
  if (has_group()) {
    NametagGroup *group = get_group();
    group->update_regions();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::consider_visible
//       Access: Protected, Virtual
//  Description: This is called once a frame by the
//               MarginManager to query whether the MarginPopup
//               believes it should be made visible.  If it returns
//               true, the popup will be made visible; otherwise, it
//               will be made invisible.
////////////////////////////////////////////////////////////////////
bool Nametag2d::
consider_visible() {
  // Make sure the master "on" switch for arrows hasn't changed.
  bool force_update = false;
  if (_master_arrows != NametagGlobals::get_master_arrows_on()) {
    _master_arrows = NametagGlobals::get_master_arrows_on();
    force_update = true;
  }
  // And also that no other important properties have changed.
  if (_master_margin_prop_seq != NametagGlobals::margin_prop_seq) {
    _master_margin_prop_seq = NametagGlobals::margin_prop_seq;
    force_update = true;
  }

  if (force_update) {
    update_contents();
  }

  if (_current_contents == 0) {
    // If we have no contents, there's no need to be visible.
    return false;
  }

  nassertr(has_group(), false);
  NametagGroup *group = get_group();

  // We want to be visible if our associated Nametag3d was not
  // completely onscreen.
  NametagGroup::Nametag3dFlag flag = group->get_nametag3d_flag();
  bool visible = (flag != NametagGroup::NF_onscreen);

  // Or if we've got a chat message and the global onscreen chat flag
  // is set.
  if (NametagGlobals::get_onscreen_chat_forced() &&
      (_current_contents & (C_speech | C_thought)) != 0) {
    visible = true;
  }

  // And we must then clear the flag for next time.
  group->set_nametag3d_flag(NametagGroup::NF_offscreen);

  NametagGroup::ColorCode color_code = group->get_color_code();
  if (visible && (color_code == NametagGroup::CC_toon_building ||
                  color_code == NametagGroup::CC_suit_building || 
                  color_code == NametagGroup::CC_house_building)) {
    // If it's a building-type nametag, it's only visible up to a
    // certain distance away.
    float distance2 = get_distance2();
    visible = (distance2 <= (NametagGlobals::building_nametag_distance *
                             NametagGlobals::building_nametag_distance));
  }

  return visible;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::set_managed
//       Access: Protected, Virtual
//  Description: This is called only by the MarginManager to
//               change the state of the is_managed() flag.  It
//               provides a hook for the MarginPopup to do something
//               special about it at that moment, if necessary.
////////////////////////////////////////////////////////////////////
void Nametag2d::
set_managed(bool flag) {
  MarginPopup::set_managed(flag);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::set_visible
//       Access: Protected, Virtual
//  Description: This is called only by the MarginManager to
//               change the state of the is_visible() flag.  It
//               provides a hook for the MarginPopup to do something
//               special about it at that moment, if necessary.
////////////////////////////////////////////////////////////////////
void Nametag2d::
set_visible(bool flag) {
  MarginPopup::set_visible(flag);
  update_contents();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::generate_name
//       Access: Private
//  Description: Sets up the Nametag2d to display the name and the
//               little red arrow.
////////////////////////////////////////////////////////////////////
void Nametag2d::
generate_name() {
  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Generating name for " << *this << "\n";
  }

  nassertv(has_group());
  NametagGroup *group = get_group();

  // Get the colors appropriate for this name.
  const NametagGlobals::Colors &colors =
    NametagGlobals::get_colors(group->get_color_code(), Nametag::get_state());

  Colorf text_color = colors._name_fg;
  Colorf card_color = colors._name_bg;
  card_color[3] =
    max(min(card_color[3], NametagGlobals::get_max_2d_alpha()),
        NametagGlobals::get_min_2d_alpha());

  // Get the size of the generated name, and expand it a bit to make
  // the card aesthetically pleasing.
  LVecBase4f frame = group->get_name_frame();
  frame.set(frame[0] - NametagGlobals::card_pad[0],
            frame[1] + NametagGlobals::card_pad[1],
            frame[2] - NametagGlobals::card_pad[2],
            frame[3] + NametagGlobals::card_pad[3]);

  // Compute the appropriate scale for the name so that its wordwrap
  // width exactly fits within the popup.
  float name_wordwrap = group->get_name_wordwrap();
  float scale = 2.0f * get_cell_width() / name_wordwrap;
  
  LMatrix4f mat = LMatrix4f::scale_mat(scale);

  // Now compute the translation for the name vertically so it is
  // roughly centered in the top two-thirds of the popup, but does
  // not extend above it.
  float y_center = (frame[2] + frame[3]) * 0.5f;
  float y_trans = min(0.333f / scale - y_center, 1.0f / scale - frame[3]);

  mat = LMatrix4f::translate_mat(0.0f, 0.0f, y_trans) * mat;

  // Ok, we've got the name position.
  if (card_color[3] != 0.0f) {
    // Now, before we create the name itself, create a card behind the
    // name, with the same dimensions and transformation.

    CardMaker card_maker("nametag");
    card_maker.set_frame(frame);
    card_maker.set_color(card_color);

    const NodePath &card_source = NametagGlobals::get_nametag_card();
    if (!card_source.is_empty()) {
      // We have a frame model to use.
      card_maker.set_source_geometry(card_source.node(),
                                     NametagGlobals::get_nametag_card_frame());
    }

    _card = _this_np.attach_new_node(card_maker.generate());
    _card.set_mat(mat);

    if (card_color[3] != 1.0f) {
      _card.set_transparency(TransparencyAttrib::M_alpha);
    }

    if (_has_draw_order) {
      _card.set_bin(nametag_fixed_bin, _draw_order);
    }
  }

  // Create the name itself by copying it in.
  _name = group->copy_name_to(_this_np);
  _name.set_mat(mat);

  if (_has_draw_order) {
    _name.set_bin(nametag_fixed_bin, _draw_order + 1);
  }

  _name.set_color(text_color);
  if (text_color[3] != 1.0f) {
    _name.set_transparency(TransparencyAttrib::M_alpha);
  }

  // Now apply those transforms onto the vertices, since we expect
  // it'll be a few frames before the name changes state again.
  SceneGraphReducer reducer;
  reducer.apply_attribs(_name.node());
  reducer.apply_attribs(_card.node());

  // Put the arrow directly below the name.
  const NodePath &arrow_model = NametagGlobals::get_arrow_model();
  if (arrow_model.is_empty()) {
    _arrow.remove_node();

  } else {
    _arrow = arrow_model.copy_to(_this_np);

    if (_has_draw_order) {
      _arrow.set_bin(nametag_fixed_bin, _draw_order);
    }

    _arrow_center.set(0.0f, 0.0f, frame[2] - NametagGlobals::arrow_offset);
    _arrow_center = _arrow_center * mat;

    Colorf arrow_color =
      NametagGlobals::get_arrow_color(group->get_color_code());
    _arrow.set_color(arrow_color);
    if (arrow_color[3] != 1.0f) {
      _arrow.set_transparency(TransparencyAttrib::M_alpha);
    }

    rotate_arrow();
  }

  // Finally, set up the MouseWatcherRegion corresponding to the frame.
  CPT(TransformState) transform = _this_np.get_net_transform();
  LMatrix4f rel_mat = transform->get_mat();   

  rel_mat = mat * rel_mat;
  LPoint3f ll(frame[0], 0.0f, frame[2]);
  LPoint3f ur(frame[1], 0.0f, frame[3]);
  ll = ll * rel_mat;
  ur = ur * rel_mat;
  set_region(LVecBase4f(ll[0], ur[0], ll[2], ur[2]));
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::generate_chat
//       Access: Private
//  Description: Sets up the Nametag2d to display a chat message.
////////////////////////////////////////////////////////////////////
void Nametag2d::
generate_chat(ChatBalloon *balloon) {
  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Generating chat message for " << *this << "\n";
  }

  nassertv(balloon != (ChatBalloon *)NULL);

  nassertv(has_group());
  NametagGroup *group = get_group();

  // Get the appropriate colors.
  const NametagGlobals::Colors &colors =
    NametagGlobals::get_colors(group->get_color_code(), Nametag::get_state());

  Colorf text_color = colors._chat_fg;
  Colorf balloon_color = colors._chat_bg;

  if ((group->get_chat_flags() & CF_quicktalker) != 0) {
    // It's a quicktalker message; therefore, modify it by the QT
    // background color.
    const Colorf &qt = group->get_qt_color();
    text_color.set(text_color[0] * qt[0],
                   text_color[1] * qt[1],
                   text_color[2] * qt[2],
                   text_color[3] * qt[3]);
    balloon_color.set(balloon_color[0] * qt[0],
                      balloon_color[1] * qt[1],
                      balloon_color[2] * qt[2],
                      balloon_color[3] * qt[3]);
  }
  
  const Colorf &balloon_modulation_color = group->get_balloon_modulation_color();
  balloon_color.set(balloon_color[0] * balloon_modulation_color [0],
                    balloon_color[1] * balloon_modulation_color [1],
                    balloon_color[2] * balloon_modulation_color [2],
                    balloon_color[3] * balloon_modulation_color [3]);

  balloon_color[3] =
    max(min(balloon_color[3], NametagGlobals::get_max_2d_alpha()),
        NametagGlobals::get_min_2d_alpha());

  TextFont *font = group->get_chat_font();
  nassertv(font != (TextFont *)NULL);

  string text = group->get_chat();
  nassertv(!text.empty());

  if (!group->get_name().empty()) {
    text = group->get_name() + ": " + text;
  }

  NodePath page_button;
  if (group->has_page_button()) {
    if (group->get_page_number() >= group->get_num_chat_pages() - 1) {
      // The last page is a special case.  We might draw a quit
      // button, a page button, or no button at all.
      if (group->has_quit_button()) {
        page_button = NametagGlobals::get_quit_button(Nametag::get_state());

      } else if (!group->has_no_quit_button()) {
        page_button = NametagGlobals::get_page_button(Nametag::get_state());
      }

    } else {
      // Pages preceding the last page get a page button.
      page_button = NametagGlobals::get_page_button(Nametag::get_state());
    }

  } else if (group->has_quit_button()) {
    // Just a quit button, please.
    page_button = NametagGlobals::get_quit_button(Nametag::get_state());
  }

  float wordwrap = get_chat_wordwrap();
  NodePath new_button;
  PT(PandaNode) geom =
    balloon->generate(text, font, wordwrap,
                      text_color, balloon_color, false,
                      _has_draw_order, _draw_order, page_button,
                      group->will_have_button(), false, new_button);
  _balloon = _this_np.attach_new_node(geom);
  if (!new_button.is_empty()) {
    start_flash(new_button);
  }

  // Fit the balloon snugly within our cell.
  float scale = 2.0f * get_cell_width() / (wordwrap + 1.0f);

  float width =
    NametagGlobals::balloon_external_width * balloon->get_hscale();
  float height = balloon->get_text_height() * balloon->get_hscale();

  float half_width = width * 0.5f;
  float half_height = height * 0.5f;

  float x_trans = half_width + 0.5f * balloon->get_hscale();
  float y_trans = half_height + NametagGlobals::balloon_text_origin[2];

  LMatrix4f mat =
    LMatrix4f::translate_mat(-x_trans, 0.0f, -y_trans) *
    LMatrix4f::scale_mat(scale);
  _balloon.set_mat(mat);

  // Apply this transform to the vertices.
  SceneGraphReducer reducer;
  reducer.apply_attribs(_balloon.node());


  // Finally, set up the MouseWatcherRegion corresponding to the whole
  // cell.
  CPT(TransformState) transform = _this_np.get_net_transform();
  const LMatrix4f &rel_mat = transform->get_mat();   

  half_height += 1.0f;
  LPoint3f ll(-half_width * scale, 0.0f, -half_height * scale);
  LPoint3f ur(half_width * scale, 0.0f, half_height * scale);
  ll = ll * rel_mat;
  ur = ur * rel_mat;
  set_region(LVecBase4f(ll[0], ur[0], ll[2], ur[2]));
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::rotate_arrow
//       Access: Private
//  Description: Rotates the arrow to point in the appropriate
//               direction.
////////////////////////////////////////////////////////////////////
void Nametag2d::
rotate_arrow() {
  if (_arrow.is_empty()) {
    // No arrow, no rotate.
    return;
  }

  nassertv(has_group());

  // Determine the direction toward the avatar, relative to the
  // camera, as if the camera were centered on the toon.
  const NodePath &toon = NametagGlobals::get_toon();
  const NodePath &camera = NametagGlobals::get_camera();
  const NodePath &avatar = get_avatar();

  LPoint3f rel_center_to_camera = toon.get_pos(camera);
  LPoint3f rel_pos_to_camera = avatar.get_pos(camera);

  LVector3f rel_pos_to_center =
    rel_pos_to_camera - rel_center_to_camera;

  float rotate = rad_2_deg(catan2(rel_pos_to_center[1],
                                  rel_pos_to_center[0]));

  LMatrix4f mat;
  compose_matrix(mat,
                 LVecBase3f(NametagGlobals::arrow_scale,
                            NametagGlobals::arrow_scale,
                            NametagGlobals::arrow_scale),
                 LVecBase3f(0.0f, 0.0f, -rotate),
                 _arrow_center);

  _arrow.set_mat(mat);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag2d::get_distance2
//       Access: Private
//  Description: Returns the square of the distance of the avatar from
//               the local toon.
////////////////////////////////////////////////////////////////////
float Nametag2d::
get_distance2() const {
  const NodePath &avatar = get_avatar();
  nassertr(!avatar.is_empty(), 0);

  const NodePath &toon = NametagGlobals::get_toon();
  nassertr(!toon.is_empty(), 0);

  LPoint3f rel_pos = avatar.get_pos(toon);
  float distance2 = rel_pos.dot(rel_pos);

  return distance2;
}
