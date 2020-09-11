// Filename: nametag.cxx
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#include "nametag.h"
#include "nametagGroup.h"
#include "nametagGlobals.h"
#include "popupMouseWatcherRegion.h"
#include "chatFlags.h"

#include "audioSound.h"
#include "mouseWatcherParameter.h"
#include "mouseButton.h"
#include "cMetaInterval.h"
#include "cLerpNodePathInterval.h"

#include <stdio.h>  // for sprintf

TypeHandle Nametag::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: Nametag::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
Nametag::
Nametag(float chat_wordwrap) {
  _draw_order = 0;
  _has_draw_order = false;
  _contents = C_name | C_speech | C_thought;
  _active = true;
  _current_contents = 0;
  _group = (NametagGroup *)NULL;
  _chat_wordwrap = chat_wordwrap;
  _state = PGButton::S_ready;
  _region_active = false;

  char buffer[128];
  sprintf(buffer, "flash-%p", this);
  _flash_track_name = buffer;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::Destructor
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
Nametag::
~Nametag() {
  // The group had better be NULL by the time we destruct, or
  // something's pretty screwed up.
  nassertv(_group == (NametagGroup *)NULL);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::deactivate
//       Access: Public
//  Description: Removes the MouseWatcherRegion associated with this
//               Nametag.  This is sometimes necessary so an outside
//               party can clean up for an errant Nametag.
////////////////////////////////////////////////////////////////////
void Nametag::
deactivate() {
  clear_region();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::display_as_active
//       Access: Published
//  Description: Returns true if the nametag is effectively active,
//               false otherwise.  This includes all the things that
//               affect nametags, including whether it has been
//               explicitly set inactive, whether global nametags have
//               been set inactive, and whether the group has a page
//               button.
////////////////////////////////////////////////////////////////////
bool Nametag::
display_as_active() const {
  bool active = is_active();

  if (has_group()) {
    NametagGroup *group = get_group();
    active = active && group->display_as_active();
  } else {
    active = active && NametagGlobals::get_master_nametags_active();
  }

  return active;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::get_avatar
//       Access: Published
//  Description: Returns the node that represents the Avatar for this
//               Nametag.  This is either the node set by
//               set_avatar() on this nametag, or if no node was
//               set, the one specified by set_avatar() on this
//               nametag's group.
////////////////////////////////////////////////////////////////////
const NodePath &Nametag::
get_avatar() const {
  if (!_avatar.is_empty()) {
    return _avatar;
  }
  if (has_group()) {
    return get_group()->get_avatar();
  }
  return _avatar;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::is_group_managed
//       Access: Public
//  Description: Returns true if the Nametag is associated with a
//               group, and that group is managed, or false otherwise.
//               If this is true, the Nametag is generally expected to
//               be visible when onscreen.
////////////////////////////////////////////////////////////////////
bool Nametag::
is_group_managed() const {
  return has_group() && get_group()->is_managed();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::click
//       Access: Public, Virtual
//  Description: This is a callback hook function, called whenever a
//               mouse or keyboard button previously depressed with
//               press() is released.
////////////////////////////////////////////////////////////////////
void Nametag::
click() {
  if (has_group()) {
    NametagGroup *group = get_group();
    group->click();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::get_state
//       Access: Public, Virtual
//  Description: Returns the current visual state of this Nametag,
//               with respect to the mouse.
////////////////////////////////////////////////////////////////////
PGButton::State Nametag::
get_state() const {
  return display_as_active() ? _state : PGButton::S_inactive;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::determine_contents
//       Access: Protected, Virtual
//  Description: Determines what the _current_contents ought to
//               contain, based on the current state of the
//               NametagGroup and of the various _contents flags in
//               effect.
//
//               The appropriate value for _current_contents is
//               returned; it is not assigned into _current_contents
//               by this function.
////////////////////////////////////////////////////////////////////
int Nametag::
determine_contents() {
  int current_contents = 0;

  if (has_group()) {
    NametagGroup *group = get_group();

    if (group->is_managed()) {
      int contents = get_contents() & group->get_contents();

      int chat_flags = group->get_chat_flags();
      if ((chat_flags & CF_speech) != 0) {
        // The NametagGroup has a speech chat; can we display speech?
        if ((contents & C_speech) != 0) {
          current_contents = C_speech;
        }

      } else if ((chat_flags & CF_thought) != 0) {
        // The NametagGroup has a thought chat; can we display thought?
        if ((contents & C_thought) != 0) {
          current_contents = C_thought;
        }
      }

      if (current_contents == 0) {
        // We aren't displaying either kind of chat; can we display a
        // name?
        if ((contents & C_name) != 0 && !group->get_name().empty() &&
            NametagGlobals::get_master_nametags_visible()) {
          current_contents = C_name;
        }
      }
    }
  }

  return current_contents;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::manage
//       Access: Protected, Virtual
//  Description: This is called only by NametagGroup::manage().
////////////////////////////////////////////////////////////////////
void Nametag::
manage(MarginManager *) {
  update_contents();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::unmanage
//       Access: Protected, Virtual
//  Description: This is called only by NametagGroup::unmanage().
////////////////////////////////////////////////////////////////////
void Nametag::
unmanage(MarginManager *) {
  update_contents();
  clear_region();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::set_region
//       Access: Protected
//  Description: Sets the associated MouseWatcherRegion to the
//               indicated dimensions, and ensures it will be active
//               next frame.
////////////////////////////////////////////////////////////////////
void Nametag::
set_region(const LVecBase4f &frame, int sort) {
  nassertv(has_group());

  NametagGroup *group = get_group();
  if (_region == (PopupMouseWatcherRegion *)NULL) {
    // Create a new region.
    string name = get_type().get_name() + "-" + group->get_name();
    _region = new PopupMouseWatcherRegion(this, name, frame);

  } else {
    // Update the old region.
    _region->set_frame(frame);
  }
  _region->set_sort(sort);

  // Now update the _region_seq, so that the group will know we expect
  // to be active this frame.
  _region_seq = group->get_region_seq();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::keep_region
//       Access: Protected
//  Description: Indicates that the region that was in effect last
//               frame (or at some point in the past, whenever
//               set_region() was last called) should still be in
//               effect this frame.  Either this call or set_region()
//               should be called every frame or the NametagGroup will
//               deactivate the MouseWatcherRegion.
//
//               It is valid to call clear_region() to remove a region
//               and later call keep_region() to restore it.
////////////////////////////////////////////////////////////////////
void Nametag::
keep_region() {
  nassertv(has_group());
  if (_region != (PopupMouseWatcherRegion *)NULL) {
    NametagGroup *group = get_group();
    _region_seq = group->get_region_seq();
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::clear_region
//       Access: Protected
//  Description: Explicitly removes the MouseWatcherRegion from the
//               MouseWatcher.  This will get done next frame anyway
//               if we don't call set_region() this frame, but calling
//               this function ensures that it happens right away.
////////////////////////////////////////////////////////////////////
void Nametag::
clear_region() {
  if (_region_active) {
    nassertv(_region != (PopupMouseWatcherRegion *)NULL);
    if (_mouse_watcher != (MouseWatcher *)NULL) {
      _mouse_watcher->remove_region(_region);
      _mouse_watcher = NULL;
    }
    _region_active = false;
  }
  _region_seq = UpdateSeq::initial();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::start_flash
//       Access: Protected
//  Description: Starts a LerpColorScale sequence flashing the
//               indicated NodePath, which is assumed to represent a
//               click button.
////////////////////////////////////////////////////////////////////
void Nametag::
start_flash(NodePath &button) {
  stop_flash();
  
  // Apparently, a gcc compiler bug compels us to pre-define these
  // LVecBase4f's.  Not a bad idea to do anyway.
  static const LVecBase4f solid(1.0f, 1.0f, 1.0f, 1.0f);
  static const LVecBase4f faded(1.0f, 1.0f, 1.0f, 0.5f);

  PT(CLerpNodePathInterval) fade_out = 
    new CLerpNodePathInterval("", 0.5, CLerpInterval::BT_ease_out,
                              true, false, button, NodePath());
  fade_out->set_start_color_scale(solid);
  fade_out->set_end_color_scale(faded);

  PT(CLerpNodePathInterval) fade_in = 
    new CLerpNodePathInterval("", 0.5, CLerpInterval::BT_ease_in,
                              true, false, button, NodePath());
  fade_in->set_start_color_scale(faded);
  fade_in->set_end_color_scale(solid);
  
  PT(CMetaInterval) sequence = new CMetaInterval(_flash_track_name);
  sequence->add_c_interval(fade_out, 0.0, CMetaInterval::RS_previous_end);
  sequence->add_c_interval(fade_in, 0.0, CMetaInterval::RS_previous_end);
  sequence->set_auto_pause(true);
  sequence->loop();

  _flash_track = sequence;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::stop_flash
//       Access: Protected
//  Description: Stops the previously-started button flash track, if
//               any.
////////////////////////////////////////////////////////////////////
void Nametag::
stop_flash() {
  if (_flash_track != (CInterval *)NULL) {
    _flash_track->finish();
    _flash_track = (CInterval *)NULL;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::update_region
//       Access: Private
//  Description: This is called once a frame by
//               NametagGroup::update_regions().  It should add the
//               region to the MouseWatcher if its region_seq matches
//               the current seq, or remove it if it doesn't.
//
//               See NametagGroup::get_region_seq() for an explanation
//               of the strategy here.
////////////////////////////////////////////////////////////////////
void Nametag::
update_region(UpdateSeq region_seq) {
  nassertv(has_group());

  bool wants_active =
    (_region_seq == region_seq) && display_as_active();

  MouseWatcher *watcher = NametagGlobals::get_mouse_watcher();
  if (_region_active && _mouse_watcher != watcher) {
    // Whoops, we've changed mouse watchers.
    if (_mouse_watcher != (MouseWatcher *)NULL) {
      _mouse_watcher->remove_region(_region);
    }
    _region_active = false;
    set_state(PGButton::S_ready);
  }

  if (wants_active) {
    if (!_region_active) {
      _mouse_watcher = watcher;
      if (_mouse_watcher != (MouseWatcher *)NULL) {
        nassertv(_region != (PopupMouseWatcherRegion *)NULL);
        _mouse_watcher->add_region(_region);
      }
      _region_active = true;
    }
  } else {
    if (_region_active) {
      if (_mouse_watcher != (MouseWatcher *)NULL) {
        nassertv(_region != (PopupMouseWatcherRegion *)NULL);
        _mouse_watcher->remove_region(_region);
      }
      _region_active = false;
      _mouse_watcher = NULL;
      set_state(PGButton::S_ready);
    }
  }
}
