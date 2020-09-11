// Filename: get_fingerprint.cxx
// Created by:  drose (19May10)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

#include "get_fingerprint.h"
#include "pnotify.h"

#ifdef WIN32
#include <windows.h>
#include <Iphlpapi.h>
#endif

#ifdef IS_OSX
#include <SystemConfiguration/SystemConfiguration.h>
#endif

// Obscures the Mac address so it won't be conspicuous to anyone
// sniffing the network stream.
static string
hash_str(const string &input) {
  // We simply xor the string with each letter of our key in sequence.
  // This isn't cryptography; we're only obfuscating here.
  static const char *key = "outrageous";

  string result;
  size_t p = 0;
  for (size_t i = 0; i < input.size(); ++i) {
    char v = (char)(input[i] ^ key[p]);
    result += v;

    ++p;
    if (key[p] == '\0') {
      p = 0;
    }
  }

  return result;
}

string
preload_cache() {
  ostringstream strm;

#ifdef WIN32
  void *buffer = NULL;
  ULONG buffer_size;

  // First, determine the required buffer size.
  DWORD result = GetAdaptersInfo(NULL, &buffer_size);
  if (result == ERROR_BUFFER_OVERFLOW) {
    // Then allocate an appropriately-sized buffer.
    buffer = alloca(buffer_size);
    result = GetAdaptersInfo((IP_ADAPTER_INFO *)buffer, &buffer_size);
  }

  if (result != ERROR_SUCCESS) {
    // Some error calling GetAdaptersInfo.  No Mac address available.
    strm << "&gai=" << result;

  } else {
    // Walk through the linked list of adapters.
    IP_ADAPTER_INFO *ap;
    ap = (IP_ADAPTER_INFO *)buffer;
    while (ap != NULL) {
      if (ap->Type == MIB_IF_TYPE_ETHERNET) {
        strm << "&mac=";
        for (unsigned int i = 0; i < ap->AddressLength; ++i) {
          char hex[32];
          sprintf(hex, "%02x", ap->Address[i]);
          strm << hex;
        }
      }
      ap = ap->Next;
    }
  }
#endif  // WIN32

#ifdef IS_OSX
  CFArrayRef interfaces;
  interfaces = SCNetworkInterfaceCopyAll();
  if (interfaces != NULL) {
    CFIndex num_interfaces = CFArrayGetCount(interfaces);

    for (CFIndex i = 0; i < num_interfaces; ++i) {
      SCNetworkInterfaceRef ap;
      ap = (SCNetworkInterfaceRef)CFArrayGetValueAtIndex(interfaces, i);
      assert(ap != NULL);

      CFStringRef type;
      type = SCNetworkInterfaceGetInterfaceType(ap);
      if (type != NULL) {
        if (CFEqual(type, kSCNetworkInterfaceTypeEthernet)) {
          CFStringRef mac_address;
          mac_address = SCNetworkInterfaceGetHardwareAddressString(ap);
          if (mac_address != NULL) {
            strm << "&mac=";
            CFIndex length = CFStringGetLength(mac_address);
            for (CFIndex n = 0; n < length; ++n) {
              strm << (char)CFStringGetCharacterAtIndex(mac_address, n);
            }
          }
        }
      }
    }
  }
  CFRelease(interfaces);

#endif  // IS_OSX


  string fingerprint = strm.str();
  if (!fingerprint.empty()) {
    fingerprint = fingerprint.substr(1);
  }
  return hash_str(fingerprint);
}

