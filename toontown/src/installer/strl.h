#pragma once
#ifndef __STRL_H__
#define __STRL_H__

#include <sys/types.h>

size_t strlcpy(char *dst, const char *src, size_t siz);
size_t strlcat(char *dst, const char *src, size_t siz);

#endif
