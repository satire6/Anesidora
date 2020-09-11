// Filename: config_movement.h
// Created by:  dcranall (15Jul04)
//
////////////////////////////////////////////////////////////////////

#ifndef CONFIG_MOVEMENT_H
#define CONFIG_MOVEMENT_H

#include "otpbase.h"
#include "notifyCategoryProxy.h"
#include "dconfig.h"

NotifyCategoryDecl(movement, EXPCL_OTP, EXPTP_OTP);

extern EXPCL_OTP void init_libmovement();

#endif
