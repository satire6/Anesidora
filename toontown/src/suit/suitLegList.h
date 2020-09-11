// Filename: suitLegList.h
// Created by:  drose (08Nov01)
//
////////////////////////////////////////////////////////////////////

#ifndef SUITLEGLIST_H
#define SUITLEGLIST_H

#include "toontownbase.h"
#include "suitLeg.h"

#include "pvector.h"

class DNASuitPath;
class DNAStorage;
class DNASuitPoint;

////////////////////////////////////////////////////////////////////
//       Class : SuitLegList
// Description : This is a list of SuitLegs.  See SuitLeg for a more
//               detailed explanation of its purpose.
////////////////////////////////////////////////////////////////////
class EXPCL_TOONTOWN SuitLegList {
PUBLISHED:
  SuitLegList(const DNASuitPath *path, const DNAStorage &storage,
              double suit_walk_speed, double from_sky_time,
              double to_sky_time, double from_suit_building_time,
              double to_suit_building_time, double to_toon_building_time);
  ~SuitLegList();

  int get_num_legs() const;
  const SuitLeg &get_leg(int n) const;
  INLINE const SuitLeg &operator[] (int n) const;

  int get_leg_index_at_time(double time, int start) const;

  INLINE SuitLeg::Type get_type(int n) const;
  INLINE double get_start_time(int n) const;
  INLINE double get_leg_time(int n) const;
  INLINE int get_zone_id(int n) const;
  INLINE int get_block_number(int n) const;

  INLINE int get_point_a(int n) const;
  INLINE int get_point_b(int n) const;

  bool is_point_in_range(const DNASuitPoint *point, double begin,
                         double end) const;

  void output(ostream &out) const;
  void write(ostream &out) const;

private:
  static SuitLeg::Type get_first_leg_type(const DNASuitPoint *point);
  static SuitLeg::Type get_next_leg_type(const DNASuitPoint *prev_point,
                                         const DNASuitPoint *curr_point);
  static SuitLeg::Type get_last_leg_type(const DNASuitPoint *point);
  static int get_zone_id(const DNAStorage &storage, int pi_a, int pi_b);


  typedef pvector<SuitLeg> Legs;
  Legs _legs;
};

INLINE ostream &operator << (ostream &out, const SuitLegList &list);

#include "suitLegList.I"

#endif

