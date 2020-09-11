// Filename: dnaSignBaseline.I
// Created by:  skyler (2001-30-01)
//
////////////////////////////////////////////////////////////////////


INLINE void DNASignBaseline::
set_code(string code) {
  _code = code;
}

INLINE string DNASignBaseline::
get_code() const {
  return _code;
}

INLINE void DNASignBaseline::
set_color(const Colorf &color) {
  _color = color;
}

INLINE Colorf DNASignBaseline::
get_color() const {
  return _color;
}

INLINE void DNASignBaseline::
set_font(TextFont *font) {
  _font = font;
}

INLINE TextFont *DNASignBaseline::
get_font() const {
  return _font;
}

INLINE void DNASignBaseline::
set_indent(float indent) {
  _indent = indent;
}

INLINE float DNASignBaseline::
get_indent() const {
  return _indent;
}

INLINE void DNASignBaseline::
set_kern(float kern) {
  _kern = kern;
}

INLINE float DNASignBaseline::
get_kern() const {
  return _kern;
}

INLINE float DNASignBaseline::
get_current_kern() {
  return _counter*_kern;
}

INLINE void DNASignBaseline::
set_wiggle(float wiggle) {
  _wiggle = wiggle;
}

INLINE float DNASignBaseline::
get_wiggle() const {
  return _wiggle;
}

INLINE float DNASignBaseline::
get_current_wiggle() {
  return (_counter & 0x1) ? _wiggle: -_wiggle;
}

INLINE void DNASignBaseline::
set_stumble(float stumble) {
  _stumble = stumble;
}

INLINE float DNASignBaseline::
get_stumble() const {
  return _stumble;
}

INLINE float DNASignBaseline::
get_current_stumble() {
  return (_counter & 0x1) ? _stumble: -_stumble;
}

INLINE void DNASignBaseline::
set_stomp(float stomp) {
  _stomp = stomp;
}

INLINE float DNASignBaseline::
get_stomp() const {
  return _stomp;
}

INLINE float DNASignBaseline::
get_current_stomp() {
  return (_counter & 0x1) ? _stomp: -_stomp;
}

INLINE void DNASignBaseline::
reset_counter() {
  _counter = 0;
}

INLINE void DNASignBaseline::
inc_counter() {
  ++_counter;
}

INLINE void DNASignBaseline::
set_width(float width) {
  _width = width;
}

INLINE float DNASignBaseline::
get_width() const {
  return _width;
}

INLINE void DNASignBaseline::
set_height(float height) {
  _height = height;
}

INLINE float DNASignBaseline::
get_height() const {
  return _height;
}

INLINE void DNASignBaseline::
set_flags(string flags) {
  _flags = flags;
}

INLINE string DNASignBaseline::
get_flags() const {
  return _flags;
}



