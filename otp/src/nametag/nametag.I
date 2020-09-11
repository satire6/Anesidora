// Filename: nametag.I
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: Nametag::set_contents
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
INLINE void Nametag::
set_contents(int flags) {
  _contents = flags;
  update_contents();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::get_contents
//       Access: Published
//  Description: Returns the bitmask that indicates the set of
//               contents the Nametag may represent.  See
//               set_contents().
////////////////////////////////////////////////////////////////////
INLINE int Nametag::
get_contents() const {
  return _contents;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::set_active
//       Access: Published
//  Description: Changes the active flag.  When the Nametag is active,
//               it can be clicked on; when it is not active, it
//               cannot be clicked on.  The active flag may be set
//               either on the individual Nametag, or on the entire
//               group.
////////////////////////////////////////////////////////////////////
INLINE void Nametag::
set_active(bool active) {
  _active = active;
  update_contents();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::is_active
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool Nametag::
is_active() const {
  return _active;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::has_group
//       Access: Published
//  Description: Returns true if the Nametag is associated with a
//               NametagGroup, false otherwise.  A Nametag must be
//               associated with a group to be useful.
////////////////////////////////////////////////////////////////////
INLINE bool Nametag::
has_group() const {
  return (_group != (NametagGroup *)NULL);
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::get_group
//       Access: Published
//  Description: Returns the NametagGroup that the Nametag is
//               associated with, or NULL if it is not associated with
//               any group.
////////////////////////////////////////////////////////////////////
INLINE NametagGroup *Nametag::
get_group() const {
  return _group;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::set_draw_order
//       Access: Published
//  Description: Causes the Nametag to be rendered in the fixed bin
//               with the indicated sort order.  This is only relevant
//               if the Nametag will be parented in a scene graph
//               where the cull traversal is in effect.
////////////////////////////////////////////////////////////////////
INLINE void Nametag::
set_draw_order(int draw_order) {
  _draw_order = draw_order;
  _has_draw_order = true;
  update_contents();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::clear_draw_order
//       Access: Published
//  Description: Removes the sort order previously specified with
//               set_draw_order().
////////////////////////////////////////////////////////////////////
INLINE void Nametag::
clear_draw_order() {
  _has_draw_order = false;
  update_contents();
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::set_chat_wordwrap
//       Access: Published
//  Description: Specifies the width at which the Nametag will
//               wordwrap the text in its chat balloons.  For
//               Nametag2d type nametags, this will indirectly affect
//               the scale of the text, since the text will be scaled
//               so that this width fills the cell it is assigned to.
//               For in-the-world type nametags, this only affects how
//               wide the chat balloon is allowed to be.
////////////////////////////////////////////////////////////////////
INLINE void Nametag::
set_chat_wordwrap(float wordwrap) {
  _chat_wordwrap = wordwrap;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::get_chat_wordwrap
//       Access: Published
//  Description: Returns the width at which the Nametag will
//               wordwrap the text in its chat balloons.
////////////////////////////////////////////////////////////////////
INLINE float Nametag::
get_chat_wordwrap() const {
  return _chat_wordwrap;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::set_avatar
//       Access: Published
//  Description: Specifies the particular node that represents the
//               Avatar for this Nametag.  The default if this is
//               unset is the node specified to the NametagGroup that
//               owns this Nametag.  The user is responsible for
//               ensuring that this node does not get deleted during
//               the lifetime of the Nametag.
//
//               This is generally a node that the Nametag is parented
//               to, representing the position of the avatar.
//               Normally, this is the avatar itself, but certain
//               specialty Nametags may be parented to other nodes
//               that represent the avatar (for instance, a head).
//
//               This should be some node in the 3-d scene graph,
//               never a node in the 2-d graph.
////////////////////////////////////////////////////////////////////
INLINE void Nametag::
set_avatar(const NodePath &node) {
  _avatar = node;
}

////////////////////////////////////////////////////////////////////
//     Function: Nametag::clear_avatar
//       Access: Published
//  Description: Removes the node previously specified with
//               set_avatar(), and allows the node specified by
//               NametagGroup::set_avatar() to apply.
////////////////////////////////////////////////////////////////////
INLINE void Nametag::
clear_avatar() {
  _avatar = NodePath();
}
