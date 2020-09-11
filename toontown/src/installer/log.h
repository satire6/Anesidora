// Filename: log.h
// Created by:
//
////////////////////////////////////////////////////////////////////

#ifndef LOG_H
#define LOG_H

#include <iostream>
#include <fstream>

using namespace std;

extern ofstream errorLog;

extern int openLogFile(const char *filename);

#if _MSC_VER < 1300
// int64 stream handlers
extern std::ostream& operator<<(std::ostream& os, __int64 i );
extern std::ostream& operator<<(std::ostream& os, unsigned __int64 i );
#endif

#endif
