// Filename: nametagGroup.h
// Created by:  drose (19Jul01)
//
////////////////////////////////////////////////////////////////////

#ifndef NAMETAGGROUP_H
#define NAMETAGGROUP_H

#include "otpbase.h"
#include "nametag.h"
#include "chatFlags.h"

#include "textFont.h"
#include "pointerTo.h"
#include "updateSeq.h"
#include "pvector.h"
#include "nodePath.h"
#include "vector_string.h"

class MarginManager;
class Nametag2d;
class Nametag3d;

////////////////////////////////////////////////////////////////////
//       Class : NametagGroup
// Description : This is a collection of Nametags that are associated
//               with a particular avatar.  The primary interface to
//               all the nametags is through this Group object.
////////////////////////////////////////////////////////////////////
class EXPCL_OTP NametagGroup {
PUBLISHED:
  enum ColorCode {
    CC_normal,
    CC_no_chat,
    CC_non_player,
    CC_suit,
    CC_toon_building,
    CC_suit_building,
    CC_house_building,
    CC_speed_chat,
    CC_free_chat,
  };

  NametagGroup();
  ~NametagGroup();

  INLINE Nametag2d *get_nametag2d();
  INLINE Nametag3d *get_nametag3d();

  void add_nametag(Nametag *tag);
  void remove_nametag(Nametag *tag);
  void clear_aux_nametags();

  int get_num_nametags() const;
  Nametag *get_nametag(int n) const;

  INLINE void set_font(TextFont *font);
  INLINE void set_name_font(TextFont *font);
  INLINE TextFont *get_name_font() const;
  INLINE void set_chat_font(TextFont *font);
  INLINE TextFont *get_chat_font() const;

  INLINE void set_avatar(const NodePath &node);
  INLINE const NodePath &get_avatar() const;

  INLINE NodePath &get_name_icon();

  void set_name_wordwrap(float name_wordwrap);
  float get_name_wordwrap() const;

  void set_color_code(ColorCode code);
  INLINE ColorCode get_color_code() const;

  INLINE void set_qt_color(const Colorf &color);
  INLINE const Colorf &get_qt_color() const;
  INLINE const Colorf &get_balloon_modulation_color() const;

  INLINE void set_shadow(float xoffset, float yoffset);
  INLINE void clear_shadow();
  INLINE bool has_shadow() const;
  INLINE LVecBase2f get_shadow() const;

  INLINE void set_name(const string &name);
  INLINE const string &get_name() const;

  void set_display_name(const string &name);
  INLINE const string &get_display_name() const;

  void set_chat(const string &chat, int chat_flags, int page_number = 0);
  INLINE void clear_chat();
  INLINE string get_chat() const;
  INLINE string get_stomp_text() const;
  INLINE const string &get_chat(int page_number) const;
  INLINE int get_chat_flags() const;

  void set_page_number(int page_number);
  INLINE int get_page_number() const;

  INLINE int get_num_chat_pages() const;
  INLINE int get_chat_stomp() const;
  INLINE float get_stomp_delay() const;

  INLINE void set_unique_id(const string &event);
  INLINE const string &get_unique_id() const;

  INLINE void set_object_code(int code);
  INLINE int get_object_code() const;

  void click();

  void manage(MarginManager *manager);
  void unmanage(MarginManager *manager);
  INLINE bool is_managed() const;

  INLINE void set_contents(int flags);
  INLINE int get_contents() const;

  INLINE void set_active(bool active);
  INLINE bool is_active() const;
  INLINE bool has_page_button() const;
  INLINE bool has_quit_button() const;
  INLINE bool has_no_quit_button() const;
  INLINE bool has_button() const;
  INLINE bool will_have_button() const;
  bool display_as_active() const;

public:
  // These methods are for the benefit of Nametag2d, Nametag3d, etc.;
  // even though they're public, they aren't intended to be called
  // directly by user code.
  NodePath copy_name_to(const NodePath &dest) const;
  INLINE const LVecBase4f &get_name_frame() const;

  enum Nametag3dFlag {
    NF_offscreen,
    NF_partly_offscreen,
    NF_onscreen
  };

  INLINE void set_nametag3d_flag(Nametag3dFlag flag);
  INLINE void increment_nametag3d_flag(Nametag3dFlag flag);
  INLINE Nametag3dFlag get_nametag3d_flag() const;

  INLINE UpdateSeq get_region_seq() const;
  void update_regions();


private:
  void update_contents_all();

  Nametag2d *_nametag2d;
  Nametag3d *_nametag3d;

  typedef pvector< PT(Nametag) > Nametags;
  Nametags _nametags;

  PT(TextFont) _name_font;
  PT(TextFont) _chat_font;

  NodePath _avatar;
  PT(PandaNode) _name_geom;
  LVecBase4f _name_frame;

  NodePath _name_icon;

  float _name_wordwrap;
  ColorCode _color_code;
  Colorf _qt_color;
  Colorf _balloon_modulation_color;
  LVecBase2f _shadow_offset;
  bool _has_shadow;

  string _name;
  string _display_name;
  vector_string _chat_pages;
  int _chat_flags;

  double _chat_timeout;
  double _button_timeout;
  
  string _chat_block_hold;
  int    _chat_flags_hold;
  double _chat_block_length;
  double _chat_timeblock;
  int _chat_stomp_accum;
  
  int _page_number;
  bool _buttons_pending;

  string _unique_id;
  int _object_code;

  Nametag3dFlag _nametag3d_flag;
  MarginManager *_manager;
  UpdateSeq _region_seq;

  int _contents;
  bool _active;
  bool _master_active;
  bool _master_visible;

  static int _unique_index;
  
};

#include "nametagGroup.I"

#endif
