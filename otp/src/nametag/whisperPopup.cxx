// Filename: whisperPopup.cxx
// Created by:  drose (25Jul01)
//
////////////////////////////////////////////////////////////////////

#include "whisperPopup.h"
#include "nametagGlobals.h"
#include "chatBalloon.h"
#include "marginManager.h"
#include "config_nametag.h"

#include "transformState.h"
#include "sceneGraphReducer.h"
#include "clockObject.h"
#include "throw_event.h"
#include "eventParameter.h"

TypeHandle WhisperPopup::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::Constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
WhisperPopup::
WhisperPopup(const string &text, TextFont *font,
             WhisperPopup::WhisperType whisper_type) :
  _text(text),
  _font(font),
  _whisper_type(whisper_type)
{
  set_cull_callback();

  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Creating WhisperPopup " << (void *)this << "\n";
  }
  _has_rendered = false;
  _first_appeared = 0.0f;
  _clickable = false;
  _avatar_id = 0;
  _state = PGButton::S_inactive;
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::Destructor
//       Access: Published, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
WhisperPopup::
~WhisperPopup() {
  nassertv(!is_visible());
  nassertv(!is_managed());
  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Destructing Whisper " << (void *)this << ": " << _text << "\n";
  }
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::set_clickable
//       Access: Published
//  Description: Makes the popup clickable.  When the user clicks on
//               the popup, an event named "whisperTo" is generated
//               with the two supplied parameters.
////////////////////////////////////////////////////////////////////
void WhisperPopup::
set_clickable(const string &avatar_name, int avatar_id, int is_player_id) {
  //had to add is player to tell avIds from playerIds input is int because it's coming from python
  _clickable = true;
  _avatar_name = avatar_name;
  _avatar_id = avatar_id;
  if (is_player_id != 0)
	{
		_is_player_id = true;
	}
  else
  	{
		_is_player_id = false;
	}
  _state = PGButton::S_ready;
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::manage
//       Access: Published
//  Description: Adds the popup to the pool of available popups to be
//               made visible when appropriate (i.e. when there is
//               room available).
////////////////////////////////////////////////////////////////////
void WhisperPopup::
manage(MarginManager *manager) {
  nassertv(!is_managed());
  manager->manage_popup(this);
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::unmanage
//       Access: Published
//  Description: Removes the popup from the pool of available popups
//               to be made visible.
////////////////////////////////////////////////////////////////////
void WhisperPopup::
unmanage(MarginManager *manager) {
  nassertv(is_managed());
  manager->unmanage_popup(this);
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::cull_callback
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
bool WhisperPopup::
cull_callback(CullTraverser *, CullTraverserData &) {
  // We just want to record the time the popup first appeared
  // onscreen.
  if (!_has_rendered) {
    nassertr(is_visible(), true);
    _has_rendered = true;
    _first_appeared = ClockObject::get_global_clock()->get_frame_time();
  }

  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::get_score
//       Access: Public, Virtual
//  Description: Returns a number representing how much this
//               particular MarginPopup deserves to be onscreen.
//               This is used to resolve conflicts when there are too
//               many MarginPopups that all want to be onscreen
//               simultaneously.  The larger the number, the more
//               likely this particular popup is to be made visible.
////////////////////////////////////////////////////////////////////
float WhisperPopup::
get_score() {
  // The newer the Whisper, the higher the score; the newest whispers
  // get a score of 2000 (which makes them more important than any
  // Nametag2d).  Whispers that are whisper_priority_time seconds old
  // or older earn a score of 1000 or below, which allows other
  // Nametag2d's to compete with them.
  if (!_has_rendered) {
    return 2000.0f;
  }

  double seconds_elapsed =
    ClockObject::get_global_clock()->get_frame_time() - _first_appeared;

  return 2000.0f - 1000.0f * seconds_elapsed / NametagGlobals::whisper_priority_time;
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::click
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever a
//               mouse or keyboard button previously depressed with
//               press() is released.
////////////////////////////////////////////////////////////////////
void WhisperPopup::
click() {
  throw_event("clickedWhisper", _avatar_id, _is_player_id);
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::update_contents
//       Access: Protected, Virtual
//  Description: Causes the popup to regenerate its contents
//               appropriately.
////////////////////////////////////////////////////////////////////
void WhisperPopup::
update_contents() {
  _balloon.remove_node();

  if (is_visible()) {
    generate_text(NametagGlobals::get_speech_balloon_2d(),
                  _text, _font);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::consider_manage
//       Access: Protected, Virtual
//  Description: This is called once a frame by the
//               MarginManager to query whether the MarginPopup
//               believes it should continue to be managed.  If it
//               returns false, the popup will be removed from the
//               list of managed popups.
////////////////////////////////////////////////////////////////////
bool WhisperPopup::
consider_manage() {
  // A WhisperPopup is ready to be unmanaged after whisper_total_time
  // seconds.
  if (!_has_rendered) {
    return true;
  }

  double seconds_elapsed =
    ClockObject::get_global_clock()->get_frame_time() - _first_appeared;

  return seconds_elapsed < NametagGlobals::whisper_total_time;
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::consider_visible
//       Access: Protected, Virtual
//  Description: This is called once a frame by the
//               MarginManager to query whether the MarginPopup
//               believes it should be made visible.  If it returns
//               true, the popup will be made visible; otherwise, it
//               will be made invisible.
////////////////////////////////////////////////////////////////////
bool WhisperPopup::
consider_visible() {
  if (_clickable && is_visible() &&
      _mouse_watcher != NametagGlobals::get_mouse_watcher()) {
    // If we're already visible but the current mouse watcher has
    // changed, make us be invisible for just one frame.  When we pop
    // back in next frame, the mouse watcher will be set correctly.
    return false;
  }

  return MarginPopup::consider_visible();
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::set_visible
//       Access: Protected, Virtual
//  Description: This is called only by the MarginManager to
//               change the state of the is_visible() flag.  It
//               provides a hook for the MarginPopup to do something
//               special about it at that moment, if necessary.
////////////////////////////////////////////////////////////////////
void WhisperPopup::
set_visible(bool flag) {
  MarginPopup::set_visible(flag);
  update_contents();

  if (_clickable && _region != (PopupMouseWatcherRegion *)NULL) {
    if (is_visible()) {
      _mouse_watcher = NametagGlobals::get_mouse_watcher();
      if (_mouse_watcher != (MouseWatcher *)NULL) {
        _mouse_watcher->add_region(_region);
      }

    } else {
      if (_mouse_watcher != (MouseWatcher *)NULL) {
        _mouse_watcher->remove_region(_region);
        _mouse_watcher = NULL;
      }
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::generate_text
//       Access: Private
//  Description: Generates the ChatBalloon text and parents it to the
//               popup.
////////////////////////////////////////////////////////////////////
void WhisperPopup::
generate_text(ChatBalloon *balloon, const string &text, TextFont *font) {
  if (nametag_cat.is_debug()) {
    nametag_cat.debug()
      << "Generating text for " << *this << "\n";
  }

  nassertv(balloon != (ChatBalloon *)NULL);
  nassertv(font != (TextFont *)NULL);
  nassertv(!text.empty());

  const NametagGlobals::Colors &colors =
    NametagGlobals::get_whisper_colors(_whisper_type, ClickablePopup::get_state());

  Colorf text_color = colors._chat_fg;
  Colorf balloon_color = colors._chat_bg;
  balloon_color[3] =
    max(min(balloon_color[3], NametagGlobals::get_max_2d_alpha()),
        NametagGlobals::get_min_2d_alpha());

  float wordwrap = NametagGlobals::chat_2d_wordwrap;
  NodePath new_button;
  PT(PandaNode) geom =
    balloon->generate(text, font, wordwrap,
                      text_color, balloon_color, false,
                      false, 0, NodePath(), false, false, new_button);
  _balloon = _this_np.attach_new_node(geom);

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


  // Finally, set up the clickable region.
  if (_clickable) {
    CPT(TransformState) transform = _this_np.get_net_transform();
    const LMatrix4f &rel_mat = transform->get_mat();

    half_height += 1.0f;
    LPoint3f ll(-half_width * scale, 0.0f, -half_height * scale);
    LPoint3f ur(half_width * scale, 0.0f, half_height * scale);
    ll = ll * rel_mat;
    ur = ur * rel_mat;
    set_region(LVecBase4f(ll[0], ur[0], ll[2], ur[2]));
  }
}


////////////////////////////////////////////////////////////////////
//     Function: WhisperPopup::set_region
//       Access: Protected
//  Description: Sets the associated MouseWatcherRegion to the
//               indicated dimensions, and ensures it will be active
//               next frame.
////////////////////////////////////////////////////////////////////
void WhisperPopup::
set_region(const LVecBase4f &frame, int sort) {
  if (_region == (PopupMouseWatcherRegion *)NULL) {
    // Create a new region.
    string name = "Whisper from " + _avatar_name;
    _region = new PopupMouseWatcherRegion(this, name, frame);

  } else {
    // Update the old region.
    _region->set_frame(frame);
  }
  _region->set_sort(sort);
}
