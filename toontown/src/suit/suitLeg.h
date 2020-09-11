// Filename: suitLeg.h
// Created by:  drose (08Nov01)
//
////////////////////////////////////////////////////////////////////

#ifndef SUITLEG_H
#define SUITLEG_H

#include "toontownbase.h"
#include "dnaSuitPoint.h"
#include "luse.h"

////////////////////////////////////////////////////////////////////
//       Class : SuitLeg
// Description : This class is used by SuitBase, which is the base for
//               both DistributedSuit and DistributedSuitAI, to build
//               up a list of legs along the suit's path.
//
//               Each leg corresponds to a small segment of the suit's
//               path as it walks along the street.  Generally, there
//               is one leg between each two DNASuitPoints that make
//               up the path, with some additional legs at both ends
//               to manage the transitions in and out of the world.
//
//               The client-side DistributedSuit object uses these
//               legs to define intervals to lerp it from place to
//               place, while the AI side is mainly concerned about
//               setting the zone properly each time.
//
//               This class is defined in C++ instead of in Python
//               because we have to create a long list of SuitLegs
//               every time we encounter a new suit, a process which
//               takes substantial time in Python but is negligible in
//               C++.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN SuitLeg {
PUBLISHED:
  // Various types of legs.  These leg types also correspond to named
  // states in the client-side DistributedSuit fsm.
  enum Type {
    T_walk_from_street,
    T_walk_to_street,
    T_walk,
    T_from_sky,
    T_to_sky,
    T_from_suit_building,
    T_to_suit_building,
    T_to_toon_building,
    T_from_coghq,
    T_to_coghq,
    T_off
  };

public:
  SuitLeg(Type type, double start_time, double leg_time, int zone_id,
          int block_number,
          const DNASuitPoint *point_a, const DNASuitPoint *point_b);

PUBLISHED:
  INLINE Type get_type() const;
  INLINE double get_start_time() const;
  INLINE double get_leg_time() const;
  INLINE int get_zone_id() const;
  INLINE int get_block_number() const;

  INLINE int get_point_a() const;
  INLINE int get_point_b() const;
  INLINE LPoint3f get_pos_a() const;
  INLINE LPoint3f get_pos_b() const;
  LPoint3f get_pos_at_time(double time) const;

  static string get_type_name(Type type);

  void output(ostream &out) const;

private:
  Type _type;
  double _start_time;
  double _leg_time;
  int _zone_id;
  int _block_number;
  int _point_a;
  int _point_b;
  LPoint3f _pos_a;
  LPoint3f _pos_b;

  friend class SuitLegList;
};

INLINE ostream &operator << (ostream &out, const SuitLeg &leg);
INLINE ostream &operator << (ostream &out, SuitLeg::Type type);

#include "suitLeg.I"

#endif

