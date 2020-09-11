// Filename: installer_md5.h
// Created by:  darren (09Nov00)
// $Id$
////////////////////////////////////////////////////////////////////

#ifndef INSTALLER_MD5_H
#define INSTALLER_MD5_H

typedef unsigned long MD5HashVal[4];

extern void md5_a_file(const char *fname, MD5HashVal &ret);

#endif
