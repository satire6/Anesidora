// Filename: nametag3d.cxx
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#include "nametag3d.h"
#include "nametagGroup.h"
#include "nametagGlobals.h"
#include "chatFlags.h"
#include "config_nametag.h"

#include "camera.h"
#include "pointerTo.h"
#include "colorAttrib.h"
#include "transformState.h"
#include "transparencyAttrib.h"
#include "look_at.h"
#include "cardMaker.h"
#include "decalEffect.h"
#include "cullBinAttrib.h"
#include "boundingSphere.h"
#include "pStatTimer.h"
#include "mouseButton.h"
#include "mouseWatcherParameter.h"
#include "perspectiveLens.h"
#include "compose_matrix.h"
#include "nodePath.h"
#include "cullTraverserData.h"
#include "cullBinManager.h"
#include "dcast.h"

TypeHandle Nametag3d::_type_handle;

#ifndef CPPPARSER
PStatCollector Nametag3d::_contents_pcollector("App:Show code:Nametags:3d:Contents");
PStatCollector Nametag3d::_adjust_pcollector("App:Show code:Nametags:3d:Adjust");
#endif

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
Nametag3d::
Nametag3d() :
  Nametag(NametagGlobals::chat_3d_wordwrap),
  PandaNode("")
{
#ifdef DO_MEMORY_USAGE
  MemoryUsage::update_type(this, this);
#endif
  set_cull_callback();

  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Creating Nametag3d " << (void *)this << "\n";
  }
  set_name("unnamed");

  _billboard_offset = NametagGlobals::billboard_offset;

  _top = NodePath("top");
  _for_3d = true;
  _has_frame = false;
  _frame.set(0.0f, 0.0f, 0.0f, 0.0f);

  // We set up the Nametag3d node with a phantom bounding volume, a
  // sphere with radius 2.0.  This is likely to include most of what
  // would appear within the Nametag3d itself, thus guaranteeing that
  // app_traverse() gets called even when the Nametag3d is initially
  // empty.
  BoundingSphere bsphere(LPoint3f(0.0f, 0.0f, 0.0f), 2.0f);
  set_bounds(&bsphere);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::Destructor
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
Nametag3d::
~Nametag3d() {
  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Destructing Nametag3d " << (void *)this << ": "
      << get_name() << "\n";
  }
  
  stop_flash();
  _top.remove_node();
  _name.remove_node();
  _card.remove_node();
  _balloon.remove_node();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::safe_to_flatten
//       Access: Public, Virtual
//  Description: Returns true if it is generally safe to flatten out
//               this particular kind of PandaNode by duplicating
//               instances (by calling dupe_for_flatten()), false
//               otherwise (for instance, a Camera cannot be safely
//               flattened, because the Camera pointer itself is
//               meaningful).
////////////////////////////////////////////////////////////////////
bool Nametag3d::
safe_to_flatten() const {
  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::safe_to_flatten_below
//       Access: Public, Virtual
//  Description: Returns true if a flatten operation may safely
//               continue past this node, or false if nodes below this
//               node may not be molested.
////////////////////////////////////////////////////////////////////
bool Nametag3d::
safe_to_flatten_below() const {
  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::cull_callback
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
bool Nametag3d::
cull_callback(CullTraverser *, CullTraverserData &data) {
  if (has_group()) {
    NametagGroup *group = get_group();

    if (group->is_managed()) {
      PStatTimer timer(_adjust_pcollector);
      NodePath this_np = data._node_path.get_node_path();

      // We need to know the sorting property of the bin in which the
      // nametag is rendered.
      int bin_index = data._state->get_bin_index();
      int bin_sort = CullBinManager::get_global_ptr()->get_bin_sort(bin_index);

      adjust_to_camera(this_np, bin_sort);
    }
  }

  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::release
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever a
//               mouse or keyboard button previously depressed with
//               press() is released.
//
//               Nametag3d overrides the definition from Nametag, to
//               cause the Nametag to be clicked regardless of whether
//               the mouse was within the region at the time we
//               released.  We do this because Nametags in the world
//               are difficult to catch (they tend to move around),
//               and we need to give the user an advantage here.
////////////////////////////////////////////////////////////////////
void Nametag3d::
release(const MouseWatcherParameter &param) {
  if (param.get_button() == MouseButton::one()) {
    Nametag::set_state(PGButton::S_rollover);

    if (has_group()) {
      NametagGroup *group = get_group();
      group->click();
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::update_contents
//       Access: Protected, Virtual
//  Description: Recomputes the Nametag according to its
//               NametagGroup's current state.
////////////////////////////////////////////////////////////////////
void Nametag3d::
update_contents() {
  PStatTimer timer(_contents_pcollector);
  stop_flash();

  if (_has_draw_order) {
    _top.set_bin(nametag_fixed_bin, _draw_order);
  } else {
    _top.clear_bin();
  }

  if (has_group()) {
    NametagGroup *group = get_group();
    set_name(group->get_name());
  } else {
    set_name("unnamed");
  }

  _name.remove_node();
  _card.remove_node();
  _balloon.remove_node();

  _top.node()->remove_all_children();

  _has_frame = false;

  _current_contents = determine_contents();

  if (is_group_managed()) {
    if ((_current_contents & C_speech) != 0) {
      generate_chat(NametagGlobals::get_speech_balloon_3d());
    } else if ((_current_contents & C_thought) != 0) {
      generate_chat(NametagGlobals::get_thought_balloon_3d());
    } else if ((_current_contents & C_name) != 0) {
      generate_name();
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::manage
//       Access: Protected, Virtual
//  Description: This is called only by NametagGroup::manage().
////////////////////////////////////////////////////////////////////
void Nametag3d::
manage(MarginManager *manager) {
  // Attach the _top node back to our own node.  We don't care about
  // ambiguity here; any path will do.
  NodePath this_np = NodePath::any_path(this);
  _top.reparent_to(this_np);

  Nametag::manage(manager);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::unmanage
//       Access: Protected, Virtual
//  Description: This is called only by NametagGroup::unmanage().
////////////////////////////////////////////////////////////////////
void Nametag3d::
unmanage(MarginManager *manager) {
  // Detach the _top node from our own node, so we won't be circularly
  // reference counting.
  _top.detach_node();
  Nametag::unmanage(manager);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::generate_name
//       Access: Private
//  Description: Sets up the Nametag3d to display the name.
////////////////////////////////////////////////////////////////////
void Nametag3d::
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

  // Get the size of the generated name, and expand it a bit to make
  // the card aesthetically pleasing.
  _frame = group->get_name_frame();
  _frame.set(_frame[0] - NametagGlobals::card_pad[0],
             _frame[1] + NametagGlobals::card_pad[1],
             _frame[2] - NametagGlobals::card_pad[2],
             _frame[3] + NametagGlobals::card_pad[3]);
  _has_frame = true;

  // This will be the node we should attach a decal to, if we have one.
  NodePath decal_node;

  if (card_color[3] != 0.0f) {
    // Now, before we create the name itself, create a card behind the
    // name, with the same dimensions.

    CardMaker card_maker("nametag");
    card_maker.set_frame(_frame);
    card_maker.set_color(card_color);

    const NodePath &card_source = NametagGlobals::get_nametag_card();
    if (!card_source.is_empty()) {
      // We have a frame model to use.
      card_maker.set_source_geometry(card_source.node(),
                                     NametagGlobals::get_nametag_card_frame());
    }

    _card = _top.attach_new_node(card_maker.generate());

    if (card_color[3] != 1.0f) {
      _card.set_transparency(TransparencyAttrib::M_alpha);
    }

    decal_node = _top.find("**/+GeomNode");
  }

  if (_for_3d) {
    // Instance the name icon just in front of the name.  For now, we
    // only do this in the 3-d case.
    // ZAC: bandaid to keep instances from blowing up on render
    if(group->get_name_icon())
      group->get_name_icon().instance_to(_top);
  }

  // Create the name itself.  If we are creating geometry for 3-d, we
  // decal this onto the card; otherwise, it simply follows the card
  // in the scene graph.
  if (_for_3d && !decal_node.is_empty()) {
    _name = group->copy_name_to(decal_node);
    _name.set_depth_write(false);

    decal_node.node()->set_effect(DecalEffect::make());

  } else {
    _name = group->copy_name_to(_top);

    if (_has_draw_order) {
      group->get_name_icon().set_bin(nametag_fixed_bin, _draw_order + 1);
      _name.set_bin(nametag_fixed_bin, _draw_order + 2);
    }
  }

  _name.set_color(text_color);
  if (text_color[3] != 1.0f) {
    _name.set_transparency(TransparencyAttrib::M_alpha);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::generate_chat
//       Access: Private
//  Description: Sets up the Nametag3d to display a chat message.
////////////////////////////////////////////////////////////////////
void Nametag3d::
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

  TextFont *font = group->get_chat_font();
  nassertv(font != (TextFont *)NULL);

  string text = group->get_chat();
  nassertv(!text.empty());

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

  bool reversed = ((group->get_chat_flags() & CF_reversed) != 0);

  NodePath new_button;
  PT(PandaNode) geom =
    balloon->generate(text, font, get_chat_wordwrap(),
                      text_color, balloon_color, _for_3d,
                      _has_draw_order, _draw_order, page_button,
                      group->will_have_button(), reversed, new_button);
  _balloon = _top.attach_new_node(geom);
  if (!new_button.is_empty()) {
    start_flash(new_button);
  }

  _frame = balloon->get_text_frame();
  _has_frame = true;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag3d::adjust_to_camera
//       Access: Private
//  Description: Rotates and scales the Nametag3d to face the camera,
//               and sets up its MouseWatcherRegion appropriately.
////////////////////////////////////////////////////////////////////
void Nametag3d::
adjust_to_camera(const NodePath &this_np, int bin_sort) {
  nassertv(has_group());
  NametagGroup *group = get_group();

  if (!_for_3d) {
    // If the Nametag is intended for the 2-d graph, we don't need to
    // mess with any of this stuff.  However, we do want to claim to
    // be onscreen (to automatically disable the Nametag2d).
    group->increment_nametag3d_flag(NametagGroup::NF_onscreen);

    // We also may need to define a region.  In this case, no
    // computation is necessary; the frame coordinates themselves,
    // converted to world coordinates, define the region.
    if (display_as_active() && _has_frame) {
      CPT(TransformState) transform = this_np.get_net_transform();
      if (!transform->has_mat()) {
        return;
      }

      const LMatrix4f &this_to_top = transform->get_mat();   

      LPoint3f ll(_frame[0] - 0.5f, 0.0f, _frame[2] - 1.0f);
      LPoint3f ur(_frame[1] + 0.5f, 0.0f, _frame[3] + 1.0f);
      ll = this_to_top.xform_point(ll);
      ur = this_to_top.xform_point(ur);

      // Here we duplicate the logic for composing the local sort (set
      // artificially high to 10000) with the bin sort.  Logic copied
      // from pgItem.cxx.
      int sort = (bin_sort << 16) | 10000;
      
      LVecBase4f nametag_frame(ll[0], ur[0], ll[2], ur[2]);
      set_region(nametag_frame, sort);
    }

    return;
  }

  const NodePath &camera = NametagGlobals::get_camera();
  nassertv(!camera.is_empty());
  nassertv(camera.node()->is_of_type(Camera::get_class_type()));
  Camera *camera_node = DCAST(Camera, camera.node());

  Lens *lens = camera_node->get_lens();
  nassertv(lens != (Lens *)NULL);

  const NodePath &avatar = get_avatar();

  // First, billboard the top node around to face the camera.
  CPT(TransformState) transform1 = camera.get_transform(this_np);
  if (!transform1->has_mat()) {
    return;
  }
  const LMatrix4f &cam_to_this = transform1->get_mat();   

  LVector3f up = LVector3f::up() * cam_to_this;
  LVector3f rel_pos = LVector3f::forward() * cam_to_this;

  LMatrix4f mat;
  ::look_at(mat, rel_pos, up);

  // Now compute the appropriate scale based on the distance from the
  // camera plane.  For this we need the inverse matrix.
  CPT(TransformState) transform2 = this_np.get_transform(camera);
  const LMatrix4f &this_to_cam = transform2->get_mat();   

  float distance = this_to_cam(3, 1);

  float norm_distance = max(distance, 0.1f) / NametagGlobals::far_distance;
  float scale = pow(norm_distance, NametagGlobals::scale_exponent) *
    NametagGlobals::far_scale * NametagGlobals::get_global_nametag_scale();

  if (_billboard_offset != 0.0f) {
    // Also slide the geometry towards the camera according to the
    // offset factor.

    // Assume the nametag is under a proportional scale only, and
    // determine the net scale that affects the nametag.  We'll need
    // this to compute the actual offset to the camera.
    LVector3f axis;
    cam_to_this.get_row3(axis, 0);
    float net_scale = axis.length();

    float local_offset = _billboard_offset;
    float world_offset = _billboard_offset / net_scale;

    if (distance > 0.0f) {
      // Normally, the camera is a perspective camera, which will
      // scale the nametag when we slide it.  Figure out the amount of
      // this scale, so we can compensate for it.
      if (lens->is_of_type(PerspectiveLens::get_class_type())) {
        // But don't let the nametag slide closer than the near plane.
        float near_dist = lens->get_near();
        if (distance - world_offset < near_dist + 0.001f) {
          world_offset = distance - (near_dist + 0.001f);
          local_offset = world_offset * net_scale;
        }

        scale *= (distance - world_offset) / distance;
      }
    }

    LVector3f translate;
    cam_to_this.get_row3(translate, 3);
    translate.normalize();
    translate *= local_offset;
    mat.set_row(3, translate);
  }

  LMatrix4f final_mat = LMatrix4f::scale_mat(scale) * mat;
  _top.set_mat(final_mat);

  // Now everything's rotated nicely to the camera.

  // Determine the onscreen area occupied by the nametag and/or the
  // avatar, so we can click on one or the other with the mouse.

  // We always need to compute the region around the nametag, if
  // nothing else to determine whether the nametag is partially
  // offscreen.  Sometimes we also need to compute the region around
  // the avatar as well, particularly if the avatar will be clickable.
  bool compute_avatar = false;
  if (display_as_active()) {
    // If the nametag is clickable, we should be able to click on
    // either the avatar or the nametag.

    bool has_button = false;
    if ((_current_contents & (C_speech | C_thought)) != 0) {
      NametagGroup *group = get_group();
      if (group != (NametagGroup *)NULL) {
        has_button = group->has_button();
      }
    }

    if (!has_button) {
      // But only if the nametag's chat balloon doesn't have a button
      // within it.  (If it does have a button, we can only click on
      // the nametag).
      compute_avatar = true;
    }
  }

  LVecBase4f frame;
  bool computed_frame = false;
  int frame_sort = 0;

  const LMatrix4f &proj_mat = lens->get_projection_mat();

  if (compute_avatar) {
    // We need to guesstimate how wide the avatar is in screen space.
    // First, we start with a left and right point over his head.
    float width = NametagGlobals::nominal_avatar_width*0.5f;

    LPoint3f ul(-width, 0.0f, 1.0f);
    LPoint3f ur(width, 0.0f, 1.0f);

    // Rotate these points to face the camera.  We use xform_vec so we
    // don't pick up the translation component of the matrix, which we
    // don't want right now.
    ul = final_mat.xform_vec(ul);
    ur = final_mat.xform_vec(ur);

    // We actually need those coordinates in the space of our avatar.
    CPT(TransformState) transform3 = this_np.get_transform(avatar);
    if (!transform3->has_mat()) {
      return;
    }
    const LMatrix4f &this_to_av = transform3->get_mat();   
    ul = ul * this_to_av;
    ur = ur * this_to_av;

    // And get the corresponding lower-left corner on the floor below
    // the upper-left corner.
    LPoint3f ll(ul[0], ul[1], 0.0f);

    // Finally, convert the lower-left and upper-right corners to the
    // space of the camera, so we can project them to screen space.
    CPT(TransformState) transform4 = avatar.get_transform(camera);
    if (!transform4->has_mat()) {
      return;
    }
    const LMatrix4f &av_to_cam = transform4->get_mat();   
    ur = ur * av_to_cam;
    ll = ll * av_to_cam;

    // Now project the points to the screen.  We must use the general
    // xform() call because it is a perspective transform matrix.
    LPoint4f pur = proj_mat.xform(LPoint4f(ur[0], ur[1], ur[2], 1.0f));
    LPoint4f pll = proj_mat.xform(LPoint4f(ll[0], ll[1], ll[2], 1.0f));

    if (pll[3] <= 0.0f || pur[3] <= 0.0f) {
      // The frame is behind the camera plane.  Forget it.
      group->increment_nametag3d_flag(NametagGroup::NF_offscreen);
      clear_region();
      return;
    }

    // The result is the rectangular region from the top of the nametag
    // to the floor, generally around the avatar.
    float recip_pll3=1.0f/pll[3];
    float recip_pur3=1.0f/pur[3];
    frame.set(pll[0] * recip_pll3, pur[0] * recip_pur3,
              pll[1] * recip_pll3, pur[1] * recip_pur3);
    computed_frame = true;
  }

  bool partly_offscreen = false;

  // Now do the whole thing again, just to get the part of the frame
  // exactly covered by the nametag.
  if (_has_frame) {
    LPoint3f ll(_frame[0] - 0.5f, 0.0f, _frame[2] - 1.0f);
    LPoint3f ur(_frame[1] + 0.5f, 0.0f, _frame[3] + 1.0f);
    ll = final_mat.xform_point(ll);
    ur = final_mat.xform_point(ur);

    ll = ll * this_to_cam;
    ur = ur * this_to_cam;

    LPoint4f pur = proj_mat.xform(LPoint4f(ur[0], ur[1], ur[2], 1.0f));
    LPoint4f pll = proj_mat.xform(LPoint4f(ll[0], ll[1], ll[2], 1.0f));

    if (pll[3] <= 0.0f || pur[3] <= 0.0f) {
      // The frame is behind the camera plane.
      partly_offscreen = true;

    } else {
      // The result is the rectangular region around just the nametag.

      float recip_pll3=1.0f/pll[3];
      float recip_pur3=1.0f/pur[3];
      LVecBase4f nametag_frame(pll[0] * recip_pll3, pur[0] * recip_pur3,
                               pll[1] * recip_pll3, pur[1] * recip_pur3);

      // Is any part of the nametag itself offscreen?
      partly_offscreen =
        (nametag_frame[0] < -1.0f || nametag_frame[1] > 1.0f ||
         nametag_frame[2] < -1.0f || nametag_frame[3] > 1.0f);

      // And our resulting clickable frame is the union of the two
      // frames.
      if (computed_frame) {
        frame.set(min(frame[0], nametag_frame[0]),
                  max(frame[1], nametag_frame[1]),
                  min(frame[2], nametag_frame[2]),
                  max(frame[3], nametag_frame[3]));
      } else {
        frame = nametag_frame;
        computed_frame = true;
      }

      // We base the sorting index arbitrarily on the distance from the
      // camera plane.  The farther away it is from the plane, the lower
      // the sorting index (and all sort numbers are negative).  That
      // way, a nearer nametag will be preferred over a more distant
      // nametag.
      frame_sort = (int)(ll[1] * -100.0f);
    }
  }

  if (computed_frame && display_as_active()) {
    set_region(frame, frame_sort);
  }

  // If any part of the nametag is offscreen, tell the 2-d nametag to
  // activate itself.
  if (partly_offscreen) {
    group->increment_nametag3d_flag(NametagGroup::NF_partly_offscreen);

  } else {
    // otherwise, we don't need the 2-d nametag at all.
    group->increment_nametag3d_flag(NametagGroup::NF_onscreen);
  }
}
