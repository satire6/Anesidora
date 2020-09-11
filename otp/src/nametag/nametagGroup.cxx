// Filename: nametagGroup.cxx
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#include "nametagGroup.h"
#include "nametagGlobals.h"
#include "nametag2d.h"
#include "nametag3d.h"
#include "chatFlags.h"
#include "config_nametag.h"

#include "throw_event.h"
#include "string_utils.h"
#include "clockObject.h"

#include <algorithm>

int NametagGroup::_unique_index = 0;

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::Constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
NametagGroup::
NametagGroup() {
  _name_icon = NodePath("icon");
  _name_wordwrap = -1.0f;
  _color_code = CC_normal;
  _qt_color = NametagGlobals::default_qt_color;
  _balloon_modulation_color = NametagGlobals::get_balloon_modulation_color();
  _shadow_offset.set(0.0f, 0.0f);
  _has_shadow = false;
  _chat_flags = 0;
  _chat_timeout = 0.0f;
  _button_timeout = 0.0f;
  _page_number = 0;
  _buttons_pending = false;
  _chat_stomp_accum = 0;
  _chat_timeblock = 0.0f;
  _chat_block_length = 0.5f;

  _unique_id = "nametag-" + format_string(++_unique_index);
  _object_code = 0;

  _nametag3d_flag = NF_offscreen;
  _manager = (MarginManager *)NULL;

  // Ensure our starting value for the region sequence number is more
  // than UpdateSeq::initial().
  _region_seq++;

  _contents =
    Nametag::C_name | Nametag::C_speech | Nametag::C_thought;
  _active = true;
  _master_active = NametagGlobals::get_master_nametags_active();
  _master_visible = NametagGlobals::get_master_nametags_visible();

  _nametag2d = new Nametag2d;
  _nametag3d = new Nametag3d;
  add_nametag(_nametag2d);
  add_nametag(_nametag3d);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::Destructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
NametagGroup::
~NametagGroup() {
  // Tell all our child nametags that they're no longer associated
  // with a NametagGroup.
  Nametags::iterator ti;
  for (ti = _nametags.begin(); ti != _nametags.end(); ++ti) {
    Nametag *tag = (*ti);
    tag->_group = (NametagGroup *)NULL;
    tag->update_contents();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::add_nametag
//       Access: Published
//  Description: Adds the indicated Nametag to the group.  The Nametag
//               must not already be a member of any NametagGroup.
////////////////////////////////////////////////////////////////////
void NametagGroup::
add_nametag(Nametag *tag) {
  if (tag->has_group() && tag->get_group() == this) {
    // Already added.
    nametag_cat.info()
      << "Attempt to add " << tag->get_type() << " twice to "
      << get_name() << ".\n";
    return;
  }

  nassertv(!tag->has_group());

  tag->_group = this;
  tag->update_contents();
  _nametags.push_back(tag);

  if (is_managed()) {
    tag->manage(_manager);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::remove_nametag
//       Access: Published
//  Description: Removes the indicated Nametag to the group.  The
//               Nametag must have previously been added to the
//               NametagGroup.  It is an error to attempt to remove
//               either of the two default nametags created with the
//               group.
////////////////////////////////////////////////////////////////////
void NametagGroup::
remove_nametag(Nametag *tag) {
  if (!tag->has_group()) {
    // Already removed.
    nametag_cat.info()
      << "Attempt to remove " << tag->get_type() << " twice from "
      << get_name() << ".\n";
    return;
  }

  nassertv(tag->get_group() == this);
  nassertv(tag != _nametag2d && tag != _nametag3d);

  if (is_managed()) {
    tag->unmanage(_manager);
  }

  tag->_group = (NametagGroup *)NULL;
  tag->update_contents();

  PT(Nametag) ptag = tag;
  Nametags::iterator ti =
    find(_nametags.begin(), _nametags.end(), ptag);
  nassertv(ti != _nametags.end());
  _nametags.erase(ti);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::clear_aux_nametags
//       Access: Published
//  Description: Removes any Nametags from the group except the
//               default Nametag2d and Nametag3d that are created with
//               the group itself.
////////////////////////////////////////////////////////////////////
void NametagGroup::
clear_aux_nametags() {
  Nametags new_nametags;
  new_nametags.reserve(2);

  Nametags::iterator ti;
  for (ti = _nametags.begin(); ti != _nametags.end(); ++ti) {
    Nametag *tag = (*ti);

    if (tag == _nametag2d || tag == _nametag3d) {
      new_nametags.push_back(tag);

    } else {
      tag->_group = (NametagGroup *)NULL;
      tag->update_contents();
    }
  }

  _nametags.swap(new_nametags);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_num_nametags
//       Access: Published
//  Description: Returns the number of Nametags in to the group.
//               Originally, this is 2, but there may be more added by
//               user control.
////////////////////////////////////////////////////////////////////
int NametagGroup::
get_num_nametags() const {
  return _nametags.size();
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_nametag
//       Access: Published
//  Description: Returns the nth Nametag in the group.
////////////////////////////////////////////////////////////////////
Nametag *NametagGroup::
get_nametag(int n) const {
  nassertr(n >= 0 && n < (int)_nametags.size(), (Nametag *)NULL);
  return _nametags[n];
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_name_wordwrap
//       Access: Published
//  Description: Specifies the point at which the name is wrapped; and
//               indirectly, the scale of the font in the nametag
//               (since the nametag text is scaled to fit its
//               available space).
//
//               Set this to -1 to use the default wordwrap.
////////////////////////////////////////////////////////////////////
void NametagGroup::
set_name_wordwrap(float name_wordwrap) {
  _name_wordwrap = name_wordwrap;
  set_display_name(_display_name);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_name_wordwrap
//       Access: Published
//  Description: Returns either the value set by set_name_wordwrap(),
//               or the default wordwrap value for nametags of this
//               type.
////////////////////////////////////////////////////////////////////
float NametagGroup::
get_name_wordwrap() const {
  if (_name_wordwrap > 0.0f) {
    return _name_wordwrap;
  }
  if (_color_code == CC_toon_building || _color_code == CC_suit_building) {
    return NametagGlobals::building_name_wordwrap;
  } else if (_color_code == CC_house_building) {
    return NametagGlobals::house_name_wordwrap;
  } else {
    return NametagGlobals::name_wordwrap;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_color_code
//       Access: Published
//  Description: Sets the color code of this particular avatar.  This
//               indicates which of a family of colors the nametag
//               should be drawn in, according to the avatar's
//               properties.
////////////////////////////////////////////////////////////////////
void NametagGroup::
set_color_code(ColorCode code) {
  _color_code = code;

  update_contents_all();
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_display_name
//       Access: Published
//  Description: Changes the name displayed by all the nametags in
//               this group.  This does not change the name that is
//               printed within the Nametag2d's for this avatar; see
//               set_name().
////////////////////////////////////////////////////////////////////
void NametagGroup::
set_display_name(const string &name) {
  _display_name = name;

  if (!_display_name.empty() && _name_font != (TextFont *)NULL) {
    TextNode *text_node = NametagGlobals::get_text_node();
    text_node->set_font(_name_font);
    text_node->set_wordwrap(get_name_wordwrap());
    text_node->set_align(TextNode::A_center);
    text_node->set_text(_display_name);
    _name_geom = text_node->generate();
    _name_frame = text_node->get_card_actual();
    text_node->clear_text();

    // If we're making a shadow, create two instances of the name geom
    // under a common root node, and make one of them the shadow.  We
    // don't want to do this with the TextNode interface, since that
    // will flatten the shadow into the same group with the text
    // geometry, making it impossible to apply color to the text
    // geometry without also coloring the shadow.
    if (has_shadow()) {
      PT(PandaNode) name = _name_geom;
      _name_geom = new PandaNode("name");
      NodePath np(_name_geom);

      // The shadow text
      NodePath shadow = np.attach_new_node("shadow");
      shadow.attach_new_node(name);
      shadow.set_pos(_shadow_offset[0], 0.0f, -_shadow_offset[1]);
      shadow.set_color(0.0f, 0.0f, 0.0f, 1.0f);

      // The original text
      np.attach_new_node(name);
    }

  } else {
    _name_geom.clear();
  }

  update_contents_all();
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_chat
//       Access: Published
//  Description: Changes the chat message displayed by all the
//               nametags in this group.
////////////////////////////////////////////////////////////////////
void NametagGroup::
set_chat(const string &chat, int chat_flags, int page_number) {
  _chat_flags = chat_flags;
  _page_number = page_number;
  double now = ClockObject::get_global_clock()->get_frame_time();

  if (chat_flags == 0 || chat.empty()) {
    // Chat flags 0, or empty chat message: no chat message.
    _chat_pages.clear();
    _chat_flags = 0;

  } 
  else {
    _chat_pages.clear();
    _chat_stomp_accum++;
    if(_chat_stomp_accum < 2 || (_chat_block_length < 0.05)){
      // Break the chat message up and store it by pages.
      tokenize(chat, _chat_pages, "\a");
    }
    else{
      _chat_block_hold = "" + chat;
      _chat_timeblock = now + _chat_block_length;
      _chat_flags_hold = _chat_flags;
      _chat_pages.clear();
      _chat_flags = 0;
    }
    
  }

  

  if (((_chat_flags & CF_timeout) != 0) && (_chat_timeblock < now)) {
    // If we requested a timeout, determine when that will happen.
    double keep_for = max(min((double)chat.length() * 0.5, 12.0), 4.0);
    _chat_timeout = now + keep_for;
  }

  if (will_have_button()) {
    // If we expect a button to appear, determine when *that* will
    // happen.
    _button_timeout = now + NametagGlobals::button_delay_time;
    _buttons_pending = true;
  } else {
    _button_timeout = 0.0;
    _buttons_pending = false;
  }

  update_contents_all();
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_page_number
//       Access: Published
//  Description: Sets the page that is displayed for multi-page chat
//               messages.
////////////////////////////////////////////////////////////////////
void NametagGroup::
set_page_number(int page_number) {
  if (_page_number != page_number) {
    _page_number = page_number;

    if (will_have_button()) {
      double now = ClockObject::get_global_clock()->get_frame_time();
      _button_timeout = now + NametagGlobals::button_delay_time;
      _buttons_pending = true;
    }

    update_contents_all();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::click
//       Access: Published
//  Description: This is normally called in response to a mouse button
//               down-and-up on one of our nametags, but it may be
//               called directly by the user for debugging purposes or
//               to simulate a nametag click.
//
//               This throws the unique ID of this group as an event.
//               This ID can be queried or changed via get_unique_id()
//               and set_unique_id().
////////////////////////////////////////////////////////////////////
void NametagGroup::
click() {
  throw_event(get_unique_id());
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::manage
//       Access: Published
//  Description: Activates all the Nametags in the group and makes
//               them visible onscreen when appropriate.  The supplied
//               MarginManager will be responsible for managing
//               the 2-d Nametag with the group; the remaining
//               Nametags can take care of themselves.
//
//               This should be called whenever an avatar with a
//               Nametag is brought into the world.
////////////////////////////////////////////////////////////////////
void NametagGroup::
manage(MarginManager *manager) {
  if (!is_managed()) {
    _manager = manager;

    Nametags::iterator ti;
    for (ti = _nametags.begin(); ti != _nametags.end(); ++ti) {
      Nametag *tag = (*ti);
      tag->manage(manager);
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::unmanage
//       Access: Published
//  Description: Deactivates the Nametags in the group and ensures
//               their MouseWatcherRegions are removed, etc.  This
//               should be called whenever an avatar with a Nametag is
//               removed from the world.
////////////////////////////////////////////////////////////////////
void NametagGroup::
unmanage(MarginManager *manager) {
  if (is_managed()) {
    nassertv(manager == _manager);
    _manager = (MarginManager *)NULL;

    Nametags::iterator ti;
    for (ti = _nametags.begin(); ti != _nametags.end(); ++ti) {
      Nametag *tag = (*ti);
      tag->unmanage(manager);
    }
  }
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::display_as_active
//       Access: Published
//  Description: Returns true if the group is effectively active,
//               false otherwise.  This includes all the things that
//               affect groups, including whether it has been
//               explicitly set inactive, whether global nametags have
//               been set inactive, and whether the group has a page
//               button.
////////////////////////////////////////////////////////////////////
bool NametagGroup::
display_as_active() const {
  // A group is active if it is set active *and* all nametags are
  // active.  A group is also always active if it has a page button,
  // whether or not global nametags are supposed to be active.
  return (is_active() && NametagGlobals::get_master_nametags_active()) ||
    has_button();
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::copy_name_to
//       Access: Public
//  Description: Parents a copy of the name geometry to the indicated
//               NodePath, and returns the resulting path.
////////////////////////////////////////////////////////////////////
NodePath NametagGroup::
copy_name_to(const NodePath &dest) const {
  nassertr(_name_geom != (PandaNode *)NULL, (PandaNode *)NULL);
  PT(PandaNode) copy =
    _name_geom->copy_subgraph();
  return dest.attach_new_node(copy);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::update_regions
//       Access: Public
//  Description: This calls update_region on each Nametag in the
//               group, which activates or deactivates each Nametag's
//               MouseWatcherRegion according to whether it matches
//               the current region_seq.  See get_region_seq().
////////////////////////////////////////////////////////////////////
void NametagGroup::
update_regions() {
  Nametags::iterator ti;
  for (ti = _nametags.begin(); ti != _nametags.end(); ++ti) {
    Nametag *tag = (*ti);
    tag->update_region(_region_seq);
  }

  // Now increment the region_seq for next time.
  _region_seq++;

  // Also decide whether it's time to reset the chat message.
  double now = ClockObject::get_global_clock()->get_frame_time();
  if((_chat_timeblock < now) && _chat_stomp_accum > 1){
      _chat_stomp_accum = 0;
      set_chat(_chat_block_hold, _chat_flags_hold, _page_number);
  }      
  
  if ((_chat_flags & CF_timeout) != 0) {
    if (now >= _chat_timeout) {
      clear_chat();
      _chat_stomp_accum = 0;
    }
  }

  bool force_update = false;
  // Is it time to reveal the buttons?
  if (_buttons_pending) {
    if (now >= _button_timeout) {
      _buttons_pending = false;
      force_update = true;
    }
  }

  // And should we change active state based on the global switch?
  if (_master_active != NametagGlobals::get_master_nametags_active()) {
    _master_active = NametagGlobals::get_master_nametags_active();
    force_update = true;
  }
  if (_master_visible != NametagGlobals::get_master_nametags_visible()) {
    _master_visible = NametagGlobals::get_master_nametags_visible();
    force_update = true;
  }

  if (force_update) {
    update_contents_all();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::update_contents_all
//       Access: Private
//  Description: Calls update_contents() on each Nametag within the
//               group, to cause each Nametag to pick up the latest
//               changes.
////////////////////////////////////////////////////////////////////
void NametagGroup::
update_contents_all() {
  Nametags::iterator ti;
  for (ti = _nametags.begin(); ti != _nametags.end(); ++ti) {
    Nametag *tag = (*ti);
    tag->update_contents();
  }
}
