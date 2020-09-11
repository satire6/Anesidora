// Filename: lexerDefs.h
// Created by:  shochet (25May00)
//
////////////////////////////////////////////////////////////////////

#ifndef LEXERDEFS_H
#define LEXERDEFS_H

#include "toontownbase.h"

#include "typedef.h"

#include <string>

void dna_init_lexer(istream &in, ostream &err, const string &filename);
int dna_error_count();
int dna_warning_count();

void dnayyerror(const string &msg);
void dnayyerror(ostringstream &strm);

void dnayywarning(const string &msg);
void dnayywarning(ostringstream &strm);

int dnayylex();

// we never read .dna files from the terminal, always from files
#define YY_NEVER_INTERACTIVE 1

#endif

