// Filename: nametagGroup.I
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_nametag2d
//       Access: Published
//  Description: Returns the default Nametag2d object associated with
//               the group.  This is the Nametag that is displayed
//               along the edge of the screen when the avatar is not
//               visible.
////////////////////////////////////////////////////////////////////
INLINE Nametag2d *NametagGroup::
get_nametag2d() {
  return _nametag2d;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_nametag3d
//       Access: Published
//  Description: Returns the default Nametag3d object associated with
//               the group.  This is the Nametag that floats over the
//               avatar's head in the world.
////////////////////////////////////////////////////////////////////
INLINE Nametag3d *NametagGroup::
get_nametag3d() {
  return _nametag3d;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_font
//       Access: Published
//  Description: Simultaneously sets both the name font and the chat
//               font.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_font(TextFont *font) {
  _name_font = font;
  _chat_font = font;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_name_font
//       Access: Published
//  Description: Redefines the TextFont used by this group to
//               generate text for the names.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_name_font(TextFont *font) {
  _name_font = font;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_name_font
//       Access: Published
//  Description: Returns the TextFont used by this group to
//               generate text for the names.
////////////////////////////////////////////////////////////////////
INLINE TextFont *NametagGroup::
get_name_font() const {
  return _name_font;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_chat_font
//       Access: Published
//  Description: Redefines the TextFont used by this group to
//               generate text for the chat messages.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_chat_font(TextFont *font) {
  _chat_font = font;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_chat_font
//       Access: Published
//  Description: Returns the TextFont used by this group to
//               generate text for the chat messages.
////////////////////////////////////////////////////////////////////
INLINE TextFont *NametagGroup::
get_chat_font() const {
  return _chat_font;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_avatar
//       Access: Published
//  Description: Sets the node that indicates the avatar that
//               corresponds to this Nametag.  If this is non-NULL,
//               the Nametag2d will take advantage of this to rotate
//               the little arrow to face in the right direction.
//
//               It is the responsibility of the user to ensure that
//               the avatar node does not destruct during the lifetime
//               of the NametagGroup.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_avatar(const NodePath &node) {
  _avatar = node;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_avatar
//       Access: Published
//  Description: Returns the node that indicates the avatar that
//               corresponds to this Nametag.  See set_avatar().
////////////////////////////////////////////////////////////////////
INLINE const NodePath &NametagGroup::
get_avatar() const {
  return _avatar;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_name_icon
//       Access: Published
//  Description: Returns a NodePath to which geometry may be parented
//               to draw stuff behind the name (but in front of the
//               name's background card).
////////////////////////////////////////////////////////////////////
INLINE NodePath &NametagGroup::
get_name_icon() {
  return _name_icon;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_color_code
//       Access: Published
//  Description: Returns the color code set for this particular
//               avatar.  See set_color_code().
////////////////////////////////////////////////////////////////////
INLINE NametagGroup::ColorCode NametagGroup::
get_color_code() const {
  return _color_code;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_qt_color
//       Access: Published
//  Description: Sets the background color for quicktalker (SpeedChat)
//               messages from this avatar.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_qt_color(const Colorf &color) {
  _qt_color = color;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_qt_color
//       Access: Published
//  Description: Returns the background color set for quicktalker
//               (SpeedChat) messages from this avatar.
////////////////////////////////////////////////////////////////////
INLINE const Colorf &NametagGroup::
get_qt_color() const {
  return _qt_color;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_balloon_modulation_color
//       Access: Published
//  Description: Returns the balloon modulation color.
////////////////////////////////////////////////////////////////////
INLINE const Colorf &NametagGroup::
get_balloon_modulation_color() const {
  return _balloon_modulation_color;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_shadow
//       Access: Published
//  Description: Specifies that the name should be drawn with a
//               shadow, by creating a second copy of the name and
//               offsetting it slightly behind the first.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_shadow(float xoffset, float yoffset) {
  _has_shadow = true;
  _shadow_offset.set(xoffset, yoffset);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::clear_shadow
//       Access: Published
//  Description: Specifies that a shadow will not be drawn behind the
//               name.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
clear_shadow() {
  _has_shadow = false;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::has_shadow
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool NametagGroup::
has_shadow() const {
  return _has_shadow;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_shadow
//       Access: Published
//  Description: Returns the offset of the shadow as set by
//               set_shadow().  It is an error to call this if
//               has_shadow() is false.
////////////////////////////////////////////////////////////////////
INLINE LVecBase2f NametagGroup::
get_shadow() const {
  nassertr(has_shadow(), LVecBase2f(0.0, 0.0));
  return _shadow_offset;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_name
//       Access: Published
//  Description: Changes both the name of the avatar, which is used to
//               prefix messages displayed by the Nametag2d, as well
//               as the display name of the avatar, which is what is
//               displayed for every Nametag.
//
//               See also set_display_name(), which sets only the name
//               that is displayed on the Nametags.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_name(const string &name) {
  _name = name;
  set_display_name(name);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_name
//       Access: Published
//  Description: Returns the name that was set on this group.
////////////////////////////////////////////////////////////////////
INLINE const string &NametagGroup::
get_name() const {
  return _name;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_display_name
//       Access: Published
//  Description: Returns the display_name that was set on this group.
////////////////////////////////////////////////////////////////////
INLINE const string &NametagGroup::
get_display_name() const {
  return _display_name;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::clear_chat
//       Access: Published
//  Description: Removes the current chat message from this group.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
clear_chat() {
  set_chat(string(), 0);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_chat
//       Access: Published
//  Description: Returns the current page of the chat message.
////////////////////////////////////////////////////////////////////
INLINE string NametagGroup::
get_chat() const {
  if (_chat_pages.empty()) {
    return string();
  }
  return get_chat(_page_number);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_stomp_text
//       Access: Published
//  Description: Returns the current page of the chat message.
////////////////////////////////////////////////////////////////////
INLINE string NametagGroup::
get_stomp_text() const {
  if (_chat_stomp_accum < 1) {
    return string();
  }
  return _chat_block_hold;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_chat
//       Access: Published
//  Description: Returns the nth page of the chat message.
////////////////////////////////////////////////////////////////////
INLINE const string &NametagGroup::
get_chat(int page_number) const {
#ifndef NDEBUG
  static string empty_string;
  nassertr(page_number >= 0 && page_number < (int)_chat_pages.size(), empty_string);
#endif
  return _chat_pages[page_number];
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_chat_flags
//       Access: Published
//  Description: Returns the chat flags that were set on this group.
////////////////////////////////////////////////////////////////////
INLINE int NametagGroup::
get_chat_flags() const {
  return _chat_flags;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_page_number
//       Access: Published
//  Description: Returns the current page number on multi-page
//               messages.
////////////////////////////////////////////////////////////////////
INLINE int NametagGroup::
get_page_number() const {
  return _page_number;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_num_chat_pages
//       Access: Published
//  Description: Returns the number of pages available in the current
//               chat message.
////////////////////////////////////////////////////////////////////
INLINE int NametagGroup::
get_num_chat_pages() const {
  return _chat_pages.size();
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_chat_stomp
//       Access: Published
//  Description: Returns the number of pages available in the current
//               chat message.
////////////////////////////////////////////////////////////////////
INLINE int NametagGroup::
get_chat_stomp() const {
  return _chat_stomp_accum;
}


////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_stomp_delay
//       Access: Published
//  Description: Returns the number of pages available in the current
//               chat message.
////////////////////////////////////////////////////////////////////
INLINE float NametagGroup::
get_stomp_delay() const {
  return _chat_block_length;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_unique_id
//       Access: Published
//  Description: Changes the event which will be thrown in response to
//               the user's clicking on any of the nametags in this
//               group.  This is arbitrarily defined to a unique
//               string by default, but it may be redefined by the
//               user.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_unique_id(const string &event) {
  _unique_id = event;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_unique_id
//       Access: Published
//  Description: Returns the event which will be thrown in response to
//               the user's clicking on any of the nametags in this
//               group.  This is arbitrarily defined to a unique
//               string by default, but it may be redefined by the
//               user.
////////////////////////////////////////////////////////////////////
INLINE const string &NametagGroup::
get_unique_id() const {
  return _unique_id;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_object_code
//       Access: Published
//  Description: Associates a code number with the nametags in this
//               group.  If the code number is nonzero, and any two
//               nametags with the same code would be onscreen
//               simultaneously, only the nearest one is displayed.
//               This is intended to prevent redundant display of
//               multiple nametags for the same object (e.g. a
//               building with multiple doors).
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_object_code(int code) {
  _object_code = code;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_object_code
//       Access: Published
//  Description: Returns the code number associated with the nametags
//               in this group.  See set_object_code().
////////////////////////////////////////////////////////////////////
INLINE int NametagGroup::
get_object_code() const {
  return _object_code;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::is_managed
//       Access: Published
//  Description: Returns the managed flag.  This flag indicates that
//               the Nametags associated with this group are attached
//               to an active avatar in the world, and they should be
//               given live MouseWatcherRegions, etc.
////////////////////////////////////////////////////////////////////
INLINE bool NametagGroup::
is_managed() const {
  return (_manager != (MarginManager *)NULL);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_contents
//       Access: Published
//  Description: Changes the bitmask that indicates the set of
//               contents the Nametag may represent.  This is the
//               union of all the bits corresponding to name, speech,
//               or thoughts, that may be displayed in the Nametag.
//               Set it to 0 to disable the Nametag altogether.
//
//               This mask is defined both for NametagGroup as well as
//               for the individual Nametags within the group; the
//               actual mask in effect for a particular Nametag is the
//               intersection of the two masks.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_contents(int flags) {
  _contents = flags;
  update_contents_all();
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_contents
//       Access: Published
//  Description: Returns the bitmask that indicates the set of
//               contents the Nametag may represent.  See
//               set_contents().
////////////////////////////////////////////////////////////////////
INLINE int NametagGroup::
get_contents() const {
  return _contents;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_active
//       Access: Published
//  Description: Changes the active flag.  When the Nametag is active,
//               it can be clicked on; when it is not active, it
//               cannot be clicked on.  The active flag may be set
//               either on the individual Nametag, or on the entire
//               group.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_active(bool active) {
  _active = active;
  update_contents_all();
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::is_active
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool NametagGroup::
is_active() const {
  return _active;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::has_page_button
//       Access: Published
//  Description: Returns true if the group should be displaying a page
//               button at the end of each page, false otherwise.
////////////////////////////////////////////////////////////////////
INLINE bool NametagGroup::
has_page_button() const {
  return !_buttons_pending && (_chat_flags & CF_page_button) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::has_quit_button
//       Access: Published
//  Description: Returns true if the group should be displaying a quit
//               button at the end of the last page, false otherwise.
////////////////////////////////////////////////////////////////////
INLINE bool NametagGroup::
has_quit_button() const {
  return !_buttons_pending && (_chat_flags & CF_quit_button) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::has_no_quit_button
//       Access: Published
//  Description: Returns true if the group not display any button at
//               all on the final page of a multi-page chat.  If
//               neither this nor has_quit_button is true, the group
//               will display a page-advance arrow on the final page.
////////////////////////////////////////////////////////////////////
INLINE bool NametagGroup::
has_no_quit_button() const {
  return !_buttons_pending && (_chat_flags & CF_no_quit_button) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::has_button
//       Access: Published
//  Description: Returns true if the group should be displaying any
//               button.
////////////////////////////////////////////////////////////////////
INLINE bool NametagGroup::
has_button() const {
  if (_buttons_pending) {
    // Buttons will be along later.
    return false;
  }

  if ((_chat_flags & (CF_page_button | CF_quit_button)) != 0) {
    if ((_chat_flags & CF_no_quit_button) != 0 &&
        get_page_number() >= get_num_chat_pages() - 1) {
      // If we're on the last page and the no_quit_button flag is set,
      // we don't have a visible button.
      return false;
    }

    // Otherwise, we have a button on every page if the page_button or
    // quit_button flags are set.
    return true;
  }

  // The page_button flag is set; no button.
  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::will_have_button
//       Access: Published
//  Description: Returns true if the group should be displaying a
//               page-advance or quit button now, or will eventually
//               be displaying a button, once the button timeout
//               expires.
////////////////////////////////////////////////////////////////////
INLINE bool NametagGroup::
will_have_button() const {
  return (_chat_flags & (CF_page_button | CF_quit_button)) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_name_frame
//       Access: Public
//  Description: Returns the size of the frame around (or card behind)
//               the text for the avatar's name.
////////////////////////////////////////////////////////////////////
INLINE const LVecBase4f &NametagGroup::
get_name_frame() const {
  return _name_frame;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::set_nametag3d_flag
//       Access: Public
//  Description: Sets the state of the nametag3d flag.  This is used
//               to determine whether the nametag3d was in the scene
//               last frame, and hence whether the nametag2d should be
//               made active or not.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
set_nametag3d_flag(NametagGroup::Nametag3dFlag flag) {
  _nametag3d_flag = flag;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::increment_nametag3d_flag
//       Access: Public
//  Description: This is similar to set_nametag3d_flag(), except that
//               it only changes the flag in if the new value is
//               greater (i.e. more onscreen) than the original value.
//               This is useful in possibilities where there might be
//               multiple Nametag3d's onscreen, any one of which is
//               sufficient to turn off the Nametag2d.
////////////////////////////////////////////////////////////////////
INLINE void NametagGroup::
increment_nametag3d_flag(NametagGroup::Nametag3dFlag flag) {
  _nametag3d_flag = max(_nametag3d_flag, flag);
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_nametag3d_flag
//       Access: Public
//  Description: Returns the state of the nametag3d flag.  This is used
//               to determine whether the nametag3d was in the scene
//               last frame, and hence whether the nametag2d should be
//               made active or not.
////////////////////////////////////////////////////////////////////
INLINE NametagGroup::Nametag3dFlag NametagGroup::
get_nametag3d_flag() const {
  return _nametag3d_flag;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGroup::get_region_seq
//       Access: Public
//  Description: Returns the sequence number currently associated with
//               MouseWatcherRegions.  This is used to ensure that
//               only currently rendering Nametags have active
//               MouseWatcherRegions.
//
//               Whenever a Nametag calls set_region(), it updates its
//               internal region_seq with this number.  If a frame
//               goes by when it fails to call set_region(), the
//               NametagGroup will remove its region from the
//               MouseWatcher.
//
//               This is necessary because the Nametags generally
//               depend on their scene graph callback to update their
//               region, but if they are removed from the scene graph
//               (or are culled out), their callback will never be
//               called, and they will not have an opportunity to
//               remove their own region.
////////////////////////////////////////////////////////////////////
INLINE UpdateSeq NametagGroup::
get_region_seq() const {
  return _region_seq;
}
