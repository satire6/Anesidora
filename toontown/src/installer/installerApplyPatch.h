// Filename: installerApplyPatch.h
// Created by:  darren (03Jan01)
//
////////////////////////////////////////////////////////////////////

#ifndef INSTALLER_APPLY_PATCH_H
#define INSTALLER_APPLY_PATCH_H

#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

extern int apply_patch(const char *patchFileName, const char *fileName);

#endif
