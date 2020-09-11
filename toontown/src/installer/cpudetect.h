/******************************************************************************

 Copyright (c) 1999 Advanced Micro Devices, Inc.

 LIMITATION OF LIABILITY:  THE MATERIALS ARE PROVIDED *AS IS* WITHOUT ANY
 EXPRESS OR IMPLIED WARRANTY OF ANY KIND INCLUDING WARRANTIES OF MERCHANTABILITY,
 NONINFRINGEMENT OF THIRD-PARTY INTELLECTUAL PROPERTY, OR FITNESS FOR ANY
 PARTICULAR PURPOSE.  IN NO EVENT SHALL AMD OR ITS SUPPLIERS BE LIABLE FOR ANY
 DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, DAMAGES FOR LOSS OF PROFITS,
 BUSINESS INTERRUPTION, LOSS OF INFORMATION) ARISING OUT OF THE USE OF OR
 INABILITY TO USE THE MATERIALS, EVEN IF AMD HAS BEEN ADVISED OF THE POSSIBILITY
 OF SUCH DAMAGES.  BECAUSE SOME JURISDICTIONS PROHIBIT THE EXCLUSION OR LIMITATION
 OF LIABILITY FOR CONSEQUENTIAL OR INCIDENTAL DAMAGES, THE ABOVE LIMITATION MAY
 NOT APPLY TO YOU.

 AMD does not assume any responsibility for any errors which may appear in the
 Materials nor any responsibility to support or update the Materials.  AMD retains
 the right to make changes to its test specifications at any time, without notice.

 NO SUPPORT OBLIGATION: AMD is not obligated to furnish, support, or make any
 further information, software, technical information, know-how, or show-how
 available to you.

 So that all may benefit from your experience, please report  any  problems
 or  suggestions about this software to 3dsdk.support@amd.com

 AMD Developer Technologies, M/S 585
 Advanced Micro Devices, Inc.
 5900 E. Ben White Blvd.
 Austin, TX 78741
 3dsdk.support@amd.com

*****************************************************************************

 ADETECT.H

 AMD3D 3D library code: CPU Feature detection

*****************************************************************************/

// Miscellaneous routines
#ifndef _AMD_DETECT_H
#define _AMD_DETECT_H

#ifdef __cplusplus
extern "C" {
#endif

// Detected CPU Vendors - returned by GetCPUCaps (CPU_VENDOR_STRING);
typedef enum CPU_VENDORS
{
    VENDOR_UNKNOWN,
    VENDOR_AMD,
    VENDOR_INTEL,
    VENDOR_CYRIX,
    VENDOR_CENTAUR
} CPU_VENDORS;

// Detected CPU models - returned by GetCPUCaps (CPU_TYPE);
typedef enum CPU_TYPES
{
    UNKNOWN,
    AMD_Am486,
    AMD_K5,
    AMD_K6,
    AMD_K6_2,
    AMD_K6_3,
    AMD_ATHLON,

    INTEL_486DX,
    INTEL_486SX,
    INTEL_486DX2,
    INTEL_486SL,
    INTEL_486SX2,
    INTEL_486DX2E,
    INTEL_486DX4,
    INTEL_Pentium,
    INTEL_Pentium_MMX,
    INTEL_Pentium_Pro,
    INTEL_Pentium_II,
    INTEL_Celeron,
    INTEL_Pentium_III,
    INTEL_Pentium_4,
    INTEL_Pentium_M,
    INTEL_Core_Duo,
    INTEL_Core2_Duo
} CPU_TYPES;


// Detected CPU capabilities - used as input to the GetCPUCaps() function
typedef enum CPUCAPS
{
    // Synthesized values
    CPU_VENDOR,     // Manufacturer (returns enum CPU_VENDORS)
    CPU_TYPE,       // CPU type (return enum CPU_TYPES)
    CPU_VENDOR_STRING,  // CPU vendor name string (return const char *)
    CPU_NAME_STRING,// CPU Processor string (extended functions 0x80000002 - 0x80000004, return const char *)

    // Processor Features - returned as boolean values
    HAS_CPUID,      // Supports CPUID instruction
    HAS_FPU,        // FPU present
    HAS_VME,        // Virtual Mode Extensions
    HAS_DEBUG,      // Debug extensions
    HAS_PSE,        // Page Size Extensions
    HAS_TSC,        // Time Stamp Counter
    HAS_MSR,        // Model Specific Registers
    HAS_PAE,        // Page Address Extensions
    HAS_MCE,        // Machine Check Extensions
    HAS_CMPXCHG8,   // CMPXCHG8 instruction
    HAS_APIC,       // APIC
    HAS_SYSENTER,   // SYSENTER/SYSEXIT instruction
    HAS_MTRR,       // Memory Type Range Registers
    HAS_GPE,        // Global Paging Extensions
    HAS_MCA,        // Machine Check Architecture
    HAS_CMOV,       // CMOV instruction
    HAS_PAT,        // Page Attribue Table
    HAS_PSE36,      // PSE36 (Page Size Extensions)

    HAS_MMX_EXT,    // MMX Extensions
    HAS_MMX,        // MMX support
    HAS_FXSAVE,     // FXSAVE/FXRSTOR instruction

    HAS_3DNOW_EXT,  // Extended 3DNow! support
    HAS_3DNOW,      // 3DNow! support

    HAS_SSE_MMX,    // SSE MMX support (same as HAS_MMXEXT)
    HAS_SSE,        // SSE
    HAS_SSE_FP,     // SSE FP support
    HAS_SSE2,       // SSE2
    HAS_SSE3,       // SSE3

    // Cache parameters (not all values apply to all cpus)
    CPU_L1_DTLB_ASSOC,      // L1 Data Cache TLB Associativity
    CPU_L1_DTLB_ENTRIES,    // L1 Data Cache TLB Entries
    CPU_L1_ITLB_ASSOC,      // L1 Instruction Cache TLB Associativity (0xff = full associativity)
    CPU_L1_ITLB_ENTRIES,    // L1 Instruction Cache TLB Entries

    CPU_L1_EDTLB_ASSOC,     // Extended (2/4 Mbyte) L1 Data Cache TLB Associativity (0xff = full associativity)
    CPU_L1_EDTLB_ENTRIES,   // Extended (2/4 Mbyte) L1 Data Cache TLB Entries
    CPU_L1_EITLB_ASSOC,     // Extended (2/4 Mbyte) L1 Instruction Cache TLB Associativity
    CPU_L1_EITLB_ENTRIES,   // Extended (2/4 Mbyte) L1 Instruction Cache TLB Entries

    CPU_L1_DCACHE_SIZE,     // L1 Data Cache Size (kbytes)
    CPU_L1_DCACHE_ASSOC,    // L1 Data Cache Associativity (0xff = full associativity)
    CPU_L1_DCACHE_LINES,    // L1 Data Cache Lines
    CPU_L1_DCACHE_LSIZE,    // L1 Data Cache Line Size (bytes)

    CPU_L1_ICACHE_SIZE,     // L1 Instruction Cache Size (kbytes)
    CPU_L1_ICACHE_ASSOC,    // L1 Instruction Cache Associativity (0xff = full associativity)
    CPU_L1_ICACHE_LINES,    // L1 Instruction Cache Lines
    CPU_L1_ICACHE_LSIZE,    // L1 Instruction Cache Line Size (bytes)

    CPU_L2_CACHE_SIZE,      // L2 Unified Cache Size (Kbytes)
    CPU_L2_CACHE_ASSOC,     // L2 Unified Cache Associativity (0xf = full associativity)
    CPU_L2_CACHE_LINES,     // L2 Unified Cache Lines (lines per tag)
    CPU_L2_CACHE_LSIZE,     // L2 Unified Cache Line Size (bytes)

    CPU_L2_DTLB_ASSOC,      // L2 Data Cache TLB Associativity
    CPU_L2_DTLB_ENTRIES,    // L2 Data Cache TLB Entries
    CPU_L2_UTLB_ASSOC,      // L2 Instruction or Unified Cache TLB Associativity (0xf = full associativity)
    CPU_L2_UTLB_ENTRIES,    // L2 Instruction or Unified Cache TLB Entries

    CPU_L2_EDTLB_ASSOC,     // Extended (2/4 Mbyte) L2 Data Cache TLB Associativity (0xf = full associativity)
    CPU_L2_EDTLB_ENTRIES,   // Extended (2/4 Mbyte) L2 Data Cache TLB Entries
    CPU_L2_EUTLB_ASSOC,     // Extended (2/4 Mbyte) L2 Instruction or Unified Cache TLB Associativity
    CPU_L2_EUTLB_ENTRIES,   // Extended (2/4 Mbyte) L2 Instruction or Unified Cache TLB Entries

} CPUCAPS;

unsigned long GetCPUCaps (CPUCAPS);

// has3DNow() use is deprecated - use GetCPUCaps()
//int has3DNow (void);
#define has3DNow() GetCPUCaps (HAS_3DNOW)

#ifdef __cplusplus
};
#endif

#endif

// eof
