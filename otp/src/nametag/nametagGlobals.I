// Filename: nametagGlobals.I
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_name_wordwrap
//       Access: Published, Static
//  Description: Returns the width at which all avatar nametags will
//               be wordwrapped.
////////////////////////////////////////////////////////////////////
INLINE float NametagGlobals::
get_name_wordwrap() {
  return name_wordwrap;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_card_pad
//       Access: Published, Static
//  Description: Returns the amount of padding applied to the card
//               behind the nametags, in each direction (left, right,
//               bottom, top).
////////////////////////////////////////////////////////////////////
INLINE const LVecBase4f &NametagGlobals::
get_card_pad() {
  return card_pad;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_camera
//       Access: Published, Static
//  Description: Sets the node that indicates the camera.  The
//               Nametags will rotate and scale (or spin their little
//               arrows around) according to the relative position of
//               the camera node.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_camera(const NodePath &node) {
  _camera = node;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_camera
//       Access: Published, Static
//  Description: Returns the node that indicates the camera.  See
//               See set_camera().
////////////////////////////////////////////////////////////////////
INLINE const NodePath &NametagGlobals::
get_camera() {
  return _camera;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_toon
//       Access: Published, Static
//  Description: Sets the node that indicates the LocalToon.  This is
//               important for 2-d Nametags to determine how to rotate
//               their arrows correctly.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_toon(const NodePath &node) {
  _toon = node;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_toon
//       Access: Published, Static
//  Description: Returns the node that indicates the LocalToon.  See
//               See set_toon().
////////////////////////////////////////////////////////////////////
INLINE const NodePath &NametagGlobals::
get_toon() {
  return _toon;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_arrow_model
//       Access: Published, Static
//  Description: Sets the node that will be instanced to each
//               Nametag2d to draw a little arrow.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_arrow_model(const NodePath &node) {
  _arrow_model = node;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_arrow_model
//       Access: Published, Static
//  Description: Returns the node that will be instanced to each
//               Nametag2d to draw a little arrow.
////////////////////////////////////////////////////////////////////
INLINE const NodePath &NametagGlobals::
get_arrow_model() {
  return _arrow_model;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_page_button_ready
//       Access: Published, Static
//  Description: Sets the node that will be used to draw a
//               page-advance button in the bottom corner of chat
//               balloons when CF_page_button is set, in the indicated
//               button state.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_page_button(int state, const NodePath &node) {
  nassertv(state >= 0 && state < max_button_states);
  _page_button[state] = node;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_page_button_ready
//       Access: Published, Static
//  Description: Returns the node that will be used to draw a
//               page-advance button in the indicated button state.
////////////////////////////////////////////////////////////////////
INLINE const NodePath &NametagGlobals::
get_page_button(int state) {
  nassertr(state >= 0 && state < max_button_states, _page_button[0]);
  return _page_button[state];
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_quit_button_ready
//       Access: Published, Static
//  Description: Sets the node that will be used to draw a
//               quit button in the bottom corner of chat balloons
//               when CF_page_button is set, in the indicated button
//               state.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_quit_button(int state, const NodePath &node) {
  nassertv(state >= 0 && state < max_button_states);
  _quit_button[state] = node;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_quit_button_ready
//       Access: Published, Static
//  Description: Returns the node that will be used to draw a
//               quit button in the indicated button state.
////////////////////////////////////////////////////////////////////
INLINE const NodePath &NametagGlobals::
get_quit_button(int state) {
  nassertr(state >= 0 && state < max_button_states, _quit_button[0]);
  return _quit_button[state];
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_nametag_card
//       Access: Published, Static
//  Description: Sets the geometry that will be parented behind each
//               Nametag as a background card, and simultaneously
//               specifies the size of the model.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_nametag_card(const NodePath &node, const LVecBase4f &frame) {
  _nametag_card = node;
  _nametag_card_frame = frame;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_nametag_card
//       Access: Published, Static
//  Description: Returns the geometry that will be parented behind
//               each Nametag as a background card.
////////////////////////////////////////////////////////////////////
INLINE const NodePath &NametagGlobals::
get_nametag_card() {
  return _nametag_card;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_nametag_card_frame
//       Access: Published, Static
//  Description: Returns the size of the geometry returned by
//               get_nametag_card().
////////////////////////////////////////////////////////////////////
INLINE const LVecBase4f &NametagGlobals::
get_nametag_card_frame() {
  return _nametag_card_frame;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_rollover_sound
//       Access: Published, Static
//  Description: Sets the sound effect that will be played whenever
//               the mouse rolls over a Nametag, either in the world
//               or on the screen.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_rollover_sound(AudioSound *sound) {
  _rollover_sound = sound;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_rollover_sound
//       Access: Published, Static
//  Description: Returns the sound effect that will be played whenever
//               the mouse rolls over a Nametag.
////////////////////////////////////////////////////////////////////
INLINE AudioSound *NametagGlobals::
get_rollover_sound() {
  return _rollover_sound;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_click_sound
//       Access: Published, Static
//  Description: Sets the sound effect that will be played whenever
//               the mouse clicks on a Nametag, either in the world
//               or on the screen.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_click_sound(AudioSound *sound) {
  _click_sound = sound;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_click_sound
//       Access: Published, Static
//  Description: Returns the sound effect that will be played whenever
//               the mouse clicks on a Nametag.
////////////////////////////////////////////////////////////////////
INLINE AudioSound *NametagGlobals::
get_click_sound() {
  return _click_sound;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_mouse_watcher
//       Access: Published, Static
//  Description: Sets a pointer to the MouseWatcher node in effect.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_mouse_watcher(MouseWatcher *watcher) {
  _mouse_watcher = watcher;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_mouse_watcher
//       Access: Published, Static
//  Description: Returns a pointer to the MouseWatcher node in effect.
////////////////////////////////////////////////////////////////////
INLINE MouseWatcher *NametagGlobals::
get_mouse_watcher() {
  return _mouse_watcher;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_speech_balloon_2d
//       Access: Published, Static
//  Description: Sets the ChatBalloon geometry that will be used for
//               rendering speech chat messages by Nametag2d objects.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_speech_balloon_2d(ChatBalloon *balloon) {
  _speech_balloon_2d = balloon;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_speech_balloon_2d
//       Access: Published, Static
//  Description: Returns the ChatBalloon geometry that will be used
//               for rendering speech chat messages by Nametag2d
//               objects.
////////////////////////////////////////////////////////////////////
INLINE ChatBalloon *NametagGlobals::
get_speech_balloon_2d() {
  return _speech_balloon_2d;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_thought_balloon_2d
//       Access: Published, Static
//  Description: Sets the ChatBalloon geometry that will be used for
//               rendering thought chat messages by Nametag2d objects.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_thought_balloon_2d(ChatBalloon *balloon) {
  _thought_balloon_2d = balloon;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_thought_balloon_2d
//       Access: Published, Static
//  Description: Returns the ChatBalloon geometry that will be used
//               for rendering thought chat messages by Nametag2d
//               objects.
////////////////////////////////////////////////////////////////////
INLINE ChatBalloon *NametagGlobals::
get_thought_balloon_2d() {
  return _thought_balloon_2d;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_speech_balloon_3d
//       Access: Published, Static
//  Description: Sets the ChatBalloon geometry that will be used for
//               rendering speech chat messages by Nametag3d objects.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_speech_balloon_3d(ChatBalloon *balloon) {
  _speech_balloon_3d = balloon;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_speech_balloon_3d
//       Access: Published, Static
//  Description: Returns the ChatBalloon geometry that will be used
//               for rendering speech chat messages by Nametag3d
//               objects.
////////////////////////////////////////////////////////////////////
INLINE ChatBalloon *NametagGlobals::
get_speech_balloon_3d() {
  return _speech_balloon_3d;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_thought_balloon_3d
//       Access: Published, Static
//  Description: Sets the ChatBalloon geometry that will be used for
//               rendering thought chat messages by Nametag3d objects.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_thought_balloon_3d(ChatBalloon *balloon) {
  _thought_balloon_3d = balloon;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_thought_balloon_3d
//       Access: Published, Static
//  Description: Returns the ChatBalloon geometry that will be used
//               for rendering thought chat messages by Nametag3d
//               objects.
////////////////////////////////////////////////////////////////////
INLINE ChatBalloon *NametagGlobals::
get_thought_balloon_3d() {
  return _thought_balloon_3d;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_master_nametags_active
//       Access: Published, Static
//  Description: Changes the global flag to disable all Nametags at
//               once.  Setting this flag to false makes all Nametags
//               in the world inactive (i.e. not pickable); setting
//               this to true allows individual Nametags to be active
//               or inactive.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_master_nametags_active(bool active) {
  _master_nametags_active = active;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_master_nametags_active
//       Access: Published, Static
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool NametagGlobals::
get_master_nametags_active() {
  return _master_nametags_active;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_master_nametags_visible
//       Access: Published, Static
//  Description: Changes the global flag to hide all Nametags at
//               once.  Setting this flag to false makes all Nametags
//               in the world invisible, including onscreen nametags.
//               It affects only the display of names; it does not
//               affect chat bubbles or onscreen chat balloons.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_master_nametags_visible(bool visible) {
  _master_nametags_visible = visible;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_master_nametags_visible
//       Access: Published, Static
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool NametagGlobals::
get_master_nametags_visible() {
  return _master_nametags_visible;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_master_arrows_on
//       Access: Published, Static
//  Description: Changes the global flag to disable all Nametag2d
//               names & arrows at once.  Setting this flag to false
//               makes all Nametag2ds in the world not display a name
//               or arrow (but they will still display speech for
//               nearby avatars).  Setting this true lets the
//               Nametag2ds display what they want.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_master_arrows_on(bool on) {
  _master_arrows_on = on;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_master_arrows_on
//       Access: Published, Static
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool NametagGlobals::
get_master_arrows_on() {
  return _master_arrows_on;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_onscreen_chat_forced
//       Access: Published, Static
//  Description: Changes the global flag force all chat messages to
//               also be displayed as onscreen chat messages, even if
//               their corresponding 3-d nametag appears to be
//               onscreen.  This can be used when we're confident that
//               that 3-d nametag is obscured by some large onscreen
//               panel (like the battle menu).
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_onscreen_chat_forced(bool on) {
  _onscreen_chat_forced = on;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_onscreen_chat_forced
//       Access: Published, Static
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool NametagGlobals::
get_onscreen_chat_forced() {
  return _onscreen_chat_forced;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_max_2d_alpha
//       Access: Published, Static
//  Description: Sets the highest level of alpha that is allowed for a
//               Nametag2d background.  The Nametag2d will never be
//               more opaque than this, despite its color setting in
//               NametagGlobals.cxx.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_max_2d_alpha(float alpha) {
  _max_2d_alpha = alpha;
  margin_prop_seq++;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_max_2d_alpha
//       Access: Published, Static
//  Description: Returns the highest level of alpha that is allowed
//               for a Nametag2d background.  See set_max_2d_alpha().
////////////////////////////////////////////////////////////////////
INLINE float NametagGlobals::
get_max_2d_alpha() {
  return _max_2d_alpha;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_min_2d_alpha
//       Access: Published, Static
//  Description: Sets the lowest level of alpha that is allowed for a
//               Nametag2d background.  The Nametag2d will never be
//               less opaque than this, despite its color setting in
//               NametagGlobals.cxx.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_min_2d_alpha(float alpha) {
  _min_2d_alpha = alpha;
  margin_prop_seq++;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_min_2d_alpha
//       Access: Published, Static
//  Description: Returns the lowest level of alpha that is allowed
//               for a Nametag2d background.  See set_min_2d_alpha().
////////////////////////////////////////////////////////////////////
INLINE float NametagGlobals::
get_min_2d_alpha() {
  return _min_2d_alpha;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_global_nametag_scale
//       Access: Published, Static
//  Description: Specifies a global scale factor on all the 3-d
//               nametags in the world.  This is in addition to the
//               scaling to match the distance from the camera.
////////////////////////////////////////////////////////////////////
INLINE void NametagGlobals::
set_global_nametag_scale(float scale) {
  _global_nametag_scale = scale;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_global_nametag_scale
//       Access: Published, Static
//  Description: Returns the global scale factor on all the 3-d
//               nametags in the world.  Normally, this will be 1.0,
//               but it might be temporarily adjusted for special
//               purposes.
////////////////////////////////////////////////////////////////////
INLINE float NametagGlobals::
get_global_nametag_scale() {
  return _global_nametag_scale;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_name_fg
//       Access: Published, Static
//  Description: Returns the color of the indicated type of nametag.
////////////////////////////////////////////////////////////////////
INLINE const Colorf &NametagGlobals::
get_name_fg(NametagGroup::ColorCode color_code, PGButton::State state) {
  return get_colors(color_code, state)._name_fg;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_name_bg
//       Access: Published, Static
//  Description: Returns the color of the indicated type of nametag.
////////////////////////////////////////////////////////////////////
INLINE const Colorf &NametagGlobals::
get_name_bg(NametagGroup::ColorCode color_code, PGButton::State state) {
  return get_colors(color_code, state)._name_bg;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::get_balloon_modulation_color
//       Access: Public, Static
//  Description: Returns the balloon modulation color.
////////////////////////////////////////////////////////////////////
const Colorf &NametagGlobals::
get_balloon_modulation_color() {
  return NametagGlobals::balloon_modulation_color;
}

////////////////////////////////////////////////////////////////////
//     Function: NametagGlobals::set_balloon_modulation_color
//       Access: Public, Static
//  Description: Sets the balloon modulation color.
////////////////////////////////////////////////////////////////////
void NametagGlobals::
set_balloon_modulation_color(const Colorf &color) {
  NametagGlobals::balloon_modulation_color = color;
}
