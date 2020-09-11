// Filename: config_dna.h
// Created by:  shochet (26Jun00)
//
////////////////////////////////////////////////////////////////////

#ifndef CONFIG_DNA_H
#define CONFIG_DNA_H

#include "toontownbase.h"

#include "notifyCategoryProxy.h"
#include "dconfig.h"
#include "configVariableList.h"
#include "configVariableSearchPath.h"

class DSearchPath;

NotifyCategoryDecl(dna, EXPCL_TOONTOWN, EXPTP_TOONTOWN);

extern ConfigVariableList dna_preload;
extern ConfigVariableSearchPath dna_path;

BEGIN_PUBLISH
EXPCL_TOONTOWN const ConfigVariableSearchPath &get_dna_path();
END_PUBLISH

#endif
