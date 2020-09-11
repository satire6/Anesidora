// Filename: dnaSign.I
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////


INLINE void DNASign::
set_color(const Colorf &color) {
  _color = color;
}

INLINE Colorf DNASign::
get_color() const {
  return _color;
}

INLINE void DNASign::
set_code(string code) {
  _code = code;
}

INLINE string DNASign::
get_code() const {
  return _code;
}
