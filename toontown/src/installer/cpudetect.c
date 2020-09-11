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

*******************************************************************************

 DETECT.C

 AMD3D 3D library code: Code to detect for 3DNow! capability.

*******************************************************************************/

#include <string.h>
//DCR#include "adetect.h"
#include "cpudetect.h"

/******************************************************************************
  Private data cache
******************************************************************************/
typedef unsigned long DWORD;
static DWORD detect_base (void);
static DWORD features     = 0;
static DWORD features2    = 0;	// more std features
static DWORD ext_features = 0;
static DWORD processor    = 0;
static char  proc_idstr[16];
static char  proc_namestr[48];
static DWORD proc_cache_l1[4] = { 0, 0, 0, 0 };
static DWORD proc_cache_l2[4] = { 0, 0, 0, 0 };


/******************************************************************************
 Routine:   GetCPUCaps
 Input:     Which capability to query (see enum CPUCAPS for an exhaustive list)
 Returns:   Depends on input:
            CPU_TYPE        - enum CPU_TYPES
            CPU_VENDOR      - enum CPU_VENDORS
            CPU_*_STRING    - const char *
            CPU CACHE DATA  - Cache size in KB
            All others      - Boolean
 Comment:   This function returns information about the capabilies of the
            CPU on which it is called.  The input enumeration covers both
            processor feature bits (the HAS_* values) and "synthesized"
            information.

            THE HAS_* QUERIES SHOULD ALWAYS BE USED IN PREFERENCE TO DIRECTLY
            CHECKING THE CPU TYPE WHEN LOOKING FOR FEATURES.  For instance,
            it is *always* better to check for HAS_3DNOW directly, rather
            than rely on checking for a K6_2, K6_3, or Athlon.  Likewise,
            HAS_MMX should always be used in preference to other methods
            of checking for MMX instructions.

            The features bits are checked against either the base feature
            bits (CPUID function 1, edx) or the extended feature bits
            (CPUID function 0x80000001, edx), as appropriate.  The return
            value is 1 for feature present or 0 for feature not present,

            The synthesized information is created by interpreting the CPUID
            results in some way.

            The full set of feature bits (both base and extended) are
            implemented in this version.

            Note that this routine caches the feature bits when first called,
            so checking multiple features is relatively efficient after the
            first invocation.  However, tt is not recommended practice to
            use GetCPUCaps() inside time-critical code.

******************************************************************************/
DWORD GetCPUCaps (CPUCAPS cap)
{
    static int init = 0;

    DWORD res = 0;

    // Detect CPUID presence once, since all other requests depend on it
    if (init == 0)
        init = detect_base();

    if (init == -1)
    {
        // No CPUID, so no CPUID functions are supported
        return 0;
    }

    // Otherwise, perform the requested tests
    switch (cap)
    {
    // Synthesized Capabilities
    case HAS_CPUID:
        // Always true if this code gets executed
        res = 1;
        break;

    // Return CPU vendor string for inspection.
    // Note that the CPU_VENDOR call is preferred for vendor detection
    case CPU_VENDOR_STRING:
        res = (DWORD)proc_idstr;
        break;

    // Return the CPU name string for inspection.
    // Note that the CPU_TYPE call is preferred for cpu type detection
    case CPU_NAME_STRING:
        res = (DWORD)proc_namestr;
        break;

    // Detect CPU vendor strings
    case CPU_VENDOR:
        if (     !strncmp (proc_idstr, "AuthenticAMD", 12))
            res = VENDOR_AMD;
        else if (!strncmp (proc_idstr, "GenuineIntel", 12))
            res = VENDOR_INTEL;
        else if (!strncmp (proc_idstr, "CyrixInstead", 12))
            res = VENDOR_CYRIX;
        else if (!strncmp (proc_idstr, "CentaurHauls", 12))
            res = VENDOR_CENTAUR;
        else
            res = VENDOR_UNKNOWN;
        break;

    case CPU_TYPE:
        // Return a member of the CPUTYPES enumeration
        // Note: do NOT use this for determining presence of chip features, such
        // as MMX and 3DNow!  Instead, use GetCPUCaps (HAS_MMX) and GetCPUCaps (HAS_3DNOW),
        // which will accurately detect the presence of these features on all chips which
        // support them.
        res = UNKNOWN;
        switch (GetCPUCaps (CPU_VENDOR))
        {
        case VENDOR_AMD:
            switch ((processor >> 8) & 0xf) // extract family code
            {
            case 4: // Am486/AM5x86
                res = AMD_Am486;
                break;

            case 5: // K6
                switch ((processor >> 4) & 0xf) // extract model code
                {
                case 0:
                case 1:
                case 2:
                case 3: res = AMD_K5;       break;
                case 4: // Not really used
                case 5: // Not really used
                case 6:
                case 7: res = AMD_K6;       break;
                case 8: res = AMD_K6_2;     break;
                case 9: // K6-III starts here, all subsequent K6 family processors
                case 10:// are recognized as K6-III.  If new product releases
                case 11:// invalidate this, the new CPU models will be referenced
                case 12:// in here
                case 13:
                case 14:
                case 15:res = AMD_K6_3;     break;
                }
                break;

            case 6: // Athlon
                // No model numbers are currently defined
                res = AMD_ATHLON;
                break;
            }
            break;

        case VENDOR_INTEL:
            switch ((processor >> 8) & 0xf) // extract family code
            {
            case 4:
                switch ((processor >> 4) & 0xf) // extract model code
                {
                case 0: res = INTEL_486DX;  break;
                case 1: res = INTEL_486DX;  break;
                case 2: res = INTEL_486SX;  break;
                case 3: res = INTEL_486DX2; break;
                case 4: res = INTEL_486SL;  break;
                case 5: res = INTEL_486SX2; break;
                case 7: res = INTEL_486DX2E;break;
                case 8: res = INTEL_486DX4; break;
                }
                break;

            case 5:
                switch ((processor >> 4) & 0xf) // extract model code
                {
                case 1: res = INTEL_Pentium;    break;
                case 2: res = INTEL_Pentium;    break;
                case 3: res = INTEL_Pentium;    break;
                case 4: res = INTEL_Pentium_MMX;break;
                }
                break;

            case 6:
                switch ((processor >> 4) & 0xf) // extract model code
                {
                case 1: res = INTEL_Pentium_Pro;break;
                case 3: res = INTEL_Pentium_II; break;
                case 5: res = INTEL_Pentium_II; break;  // actual differentiation depends on cache settings
                case 6: res = INTEL_Celeron;    break;
                case 7:
				case 8:
				case 10:
                case 11: res = INTEL_Pentium_III;break;  // actual differentiation depends on cache settings
				case 9: 
				case 13: res = INTEL_Pentium_M; break;
				case 14: res = INTEL_Core_Duo; break;
				case 15: res = INTEL_Core2_Duo; break;
                }
                break;
            case 15:
                res = INTEL_Pentium_4; break;
            }
            break;

        case VENDOR_CYRIX:
            res = UNKNOWN;
            break;

        case VENDOR_CENTAUR:
            res = UNKNOWN;
            break;
        }
        break;


    // Feature Bit Test Capabilities
    case HAS_FPU:       res = (features >>  0) & 1;     break;  // bit  0 = FPU
    case HAS_VME:       res = (features >>  1) & 1;     break;  // bit  1 = VME
    case HAS_DEBUG:     res = (features >>  2) & 1;     break;  // bit  2 = Debugger extensions
    case HAS_PSE:       res = (features >>  3) & 1;     break;  // bit  3 = Page Size Extensions
    case HAS_TSC:       res = (features >>  4) & 1;     break;  // bit  4 = Time Stamp Counter
    case HAS_MSR:       res = (features >>  5) & 1;     break;  // bit  5 = Model Specific Registers
    case HAS_PAE:       res = (features >>  6) & 1;     break;  // bit  6 = PAE
    case HAS_MCE:       res = (features >>  7) & 1;     break;  // bit  7 = Machine Check Extensions
    case HAS_CMPXCHG8:  res = (features >>  8) & 1;     break;  // bit  8 = CMPXCHG8 instruction
    case HAS_APIC:      res = (features >>  9) & 1;     break;  // bit  9 = APIC
    case HAS_SYSENTER:  res = (features >> 11) & 1;     break;  // bit 11 = SYSENTER instruction
    case HAS_MTRR:      res = (features >> 12) & 1;     break;  // bit 12 = Memory Type Range Registers
    case HAS_GPE:       res = (features >> 13) & 1;     break;  // bit 13 = Global Paging Extensions
    case HAS_MCA:       res = (features >> 14) & 1;     break;  // bit 14 = Machine Check Architecture
    case HAS_CMOV:      res = (features >> 15) & 1;     break;  // bit 15 = CMOV instruction
    case HAS_PAT:       res = (features >> 16) & 1;     break;  // bit 16 = Page Attribue Table
    case HAS_PSE36:     res = (features >> 17) & 1;     break;  // bit 17 = PSE36 (Page Size Extensions)
    case HAS_MMX:       res = (features >> 23) & 1;     break;  // bit 23 = MMX
    case HAS_FXSAVE:    res = (features >> 24) & 1;     break;  // bit 24 = FXSAVE/FXRSTOR instruction

    case HAS_SSE:       res = (features >> 25) & 1;     break;  // bit 25 = SSE
    case HAS_SSE2:      res = (features >> 26) & 1;     break;  // bit 26 = SSE2
	case HAS_SSE3:		res = (features2 >> 0) & 1;		break;	// bit 0 = SSE3

    case HAS_SSE_FP:
        // Check for actual presence of SSE FP operations
        if (GetCPUCaps (HAS_SSE))
      {
                __try
                {
                        __asm _emit 0x0f
                        __asm _emit 0x56
                        __asm _emit 0xc0        // orps xmm0, xmm0
                        res = 1;
                }
                __except (1)
                {
                        // bad instruction - do not set res = 1
                return 0;
                }
           }
       break;

    case HAS_SSE_MMX:   res = (ext_features >> 22) & 1; break;  // bit 22 (ext) = SSE MMX Extensions

    case HAS_MMX_EXT:   res = ((features >> 25)&1)
                            | ((ext_features >> 22)&1); break;  // bits 25|22(ext) = MMX Extensions

    // AMD extended information
    case HAS_3DNOW_EXT: res = (ext_features >> 30) & 1; break;  // bit 30 (ext) = Extended 3DNow!
    case HAS_3DNOW:     res = (ext_features >> 31) & 1; break;  // bit 31 (ext) = 3DNow!

    default:
        // These are CPU-specific, so guard their access
        if (GetCPUCaps (CPU_VENDOR) == VENDOR_AMD)
        {
            // K5/K6 supports a restricted range
            switch (cap)
            {
            case CPU_L1_DTLB_ASSOC:     res = (proc_cache_l1[1] >> 24) & 0xff; break;
            case CPU_L1_DTLB_ENTRIES:   res = (proc_cache_l1[1] >> 16) & 0xff; break;
            case CPU_L1_ITLB_ASSOC:     res = (proc_cache_l1[1] >>  8) & 0xff; break;
            case CPU_L1_ITLB_ENTRIES:   res = (proc_cache_l1[1] >>  0) & 0xff; break;

            case CPU_L1_DCACHE_SIZE:    res = (proc_cache_l1[2] >> 24) & 0xff; break;
            case CPU_L1_DCACHE_ASSOC:   res = (proc_cache_l1[2] >> 16) & 0xff; break;
            case CPU_L1_DCACHE_LINES:   res = (proc_cache_l1[2] >>  8) & 0xff; break;
            case CPU_L1_DCACHE_LSIZE:   res = (proc_cache_l1[2] >>  0) & 0xff; break;

            case CPU_L1_ICACHE_SIZE:    res = (proc_cache_l1[3] >> 24) & 0xff; break;
            case CPU_L1_ICACHE_ASSOC:   res = (proc_cache_l1[3] >> 16) & 0xff; break;
            case CPU_L1_ICACHE_LINES:   res = (proc_cache_l1[3] >>  8) & 0xff; break;
            case CPU_L1_ICACHE_LSIZE:   res = (proc_cache_l1[3] >>  0) & 0xff; break;

            case CPU_L2_CACHE_SIZE:     res = (proc_cache_l2[2] >> 16) & 0xffff;  break;
            case CPU_L2_CACHE_ASSOC:    res = (proc_cache_l2[2] >> 12) & 0x0f;    break;
            case CPU_L2_CACHE_LINES:    res = (proc_cache_l2[2] >>  8) & 0x0f;    break;
            case CPU_L2_CACHE_LSIZE:    res = (proc_cache_l2[2] >>  0) & 0xff;    break;
            }

            if (GetCPUCaps (CPU_TYPE) == AMD_ATHLON)
            {
                // Athlon supports these additional parameters
                switch (cap)
                {
                case CPU_L1_EDTLB_ASSOC:    res = (proc_cache_l1[0] >> 24) & 0xff; break;
                case CPU_L1_EDTLB_ENTRIES:  res = (proc_cache_l1[0] >> 16) & 0xff; break;
                case CPU_L1_EITLB_ASSOC:    res = (proc_cache_l1[0] >>  8) & 0xff; break;
                case CPU_L1_EITLB_ENTRIES:  res = (proc_cache_l1[0] >>  0) & 0xff; break;

                case CPU_L2_DTLB_ASSOC:     res = (proc_cache_l2[0] >> 28) & 0x0f;    break;
                case CPU_L2_DTLB_ENTRIES:   res = (proc_cache_l2[0] >> 16) & 0xfff;   break;
                case CPU_L2_UTLB_ASSOC:     res = (proc_cache_l2[0] >> 12) & 0x0f;    break;
                case CPU_L2_UTLB_ENTRIES:   res = (proc_cache_l2[0] >>  0) & 0xfff;   break;

                case CPU_L2_EDTLB_ASSOC:    res = (proc_cache_l2[1] >> 28) & 0x0f;    break;
                case CPU_L2_EDTLB_ENTRIES:  res = (proc_cache_l2[1] >> 16) & 0xfff;   break;
                case CPU_L2_EUTLB_ASSOC:    res = (proc_cache_l2[1] >> 12) & 0x0f;    break;
                case CPU_L2_EUTLB_ENTRIES:  res = (proc_cache_l2[1] >>  0) & 0xfff;   break;
                }
            }
        }
        break;
    }

    return res;
}



/******************************************************************************
 Routine:   detect_base (void)
 Comment:   This routine is separate from GetCPUCaps() for ease of
            comprehension.  It also encapsulates the only parts of the
            algorithm that are compiler specific.
******************************************************************************/
static DWORD detect_base (void)
{
    DWORD res;

#ifdef __WIN32__   // Use SEH to determine CPUID presence
    __try
    {
        __asm
        {
            mov     eax,0           ; function 0 = manufacturer string
            CPUID
        }
    }
    __except (1)
    {
        return (DWORD)-1;
    }

#else
    // The "right" way, which doesn't work under certain Windows versions
    __asm
    {
        pushfd                      ; save EFLAGS to stack.
        pop     eax                 ; store EFLAGS in EAX.
        mov     edx, eax            ; save in EBX for testing later.
        xor     eax, 0200000h       ; switch bit 21.
        push    eax                 ; copy "changed" value to stack.
        popfd                       ; save "changed" EAX to EFLAGS.
        pushfd
        pop     eax
        xor     eax, edx            ; See if bit changeable.
        jnz     short foundit       ; if so, mark
        mov     eax,-1              ; If not, then never try to init again
        jmp     no_features

        ALIGN   4
foundit:

        ; Check to see if processor supports extended CPUID queries
        mov     eax,0               ; function 0 = manufacturer string
        CPUID
    }
#endif

    __asm
    {
        mov     DWORD PTR [proc_idstr+0],ebx  ; Stash the manufacturer string for later
        mov     DWORD PTR [proc_idstr+4],edx
        mov     DWORD PTR [proc_idstr+8],ecx
        test    eax,eax             ; 0 is highest function, then don't query more info
        mov     eax,1               ; but the init DID happen
        jz      no_features


        ; Load up the features and (where appropriate) extended features flags
        mov     eax,1               ; Check for processor features
        CPUID
        mov     [processor],eax     ; Store processor family/model/step
        mov     [features],edx      ; Store features bits
		mov		[features2],ecx		; More features bits

        mov     eax,080000000h      ; Check for support of extended functions.
        CPUID

        ; Check which extended functions can be called
        cmp     eax,080000001h      ; Extended Feature Bits
        jb      no_features         ; jump if not supported
        cmp     eax, 080000004h     ; CPU Name string
        jb      just_extfeat        ; jump if not supported
        cmp     eax, 080000005h     ; L1 Cache information
        jb      short just_name     ; jump if not supported
        cmp     eax, 080000006h     ; L2 Cache information
        jb      short just_L1       ; jump if not supported

        ; Query and save L2 cache information
        mov     eax,080000006h      ; L2 Cache Information
        CPUID                       ; Interpretation is CPU specific, but
                                    ; fetching is not.
        mov     DWORD PTR [proc_cache_l2+0],eax
        mov     DWORD PTR [proc_cache_l2+4],ebx
        mov     DWORD PTR [proc_cache_l2+8],ecx
        mov     DWORD PTR [proc_cache_l2+12],edx


just_L1:
        ; Query and save L1 cache informatin
        mov     eax,080000005h      ; L1 Cache Information
        CPUID                       ; Interpretation is CPU specific, but
                                    ; fetching is not.
        mov     DWORD PTR [proc_cache_l1+0],eax
        mov     DWORD PTR [proc_cache_l1+4],ebx
        mov     DWORD PTR [proc_cache_l1+8],ecx
        mov     DWORD PTR [proc_cache_l1+12],edx


just_name:
        ; Query and save the CPU name string
        mov     eax,080000002h
        CPUID
        mov     DWORD PTR [proc_namestr+0],eax
        mov     DWORD PTR [proc_namestr+4],ebx
        mov     DWORD PTR [proc_namestr+8],ecx
        mov     DWORD PTR [proc_namestr+12],edx
        mov     eax,080000003h
        CPUID
        mov     DWORD PTR [proc_namestr+16],eax
        mov     DWORD PTR [proc_namestr+20],ebx
        mov     DWORD PTR [proc_namestr+24],ecx
        mov     DWORD PTR [proc_namestr+28],edx
        mov     eax,080000004h
        CPUID
        mov     DWORD PTR [proc_namestr+32],eax
        mov     DWORD PTR [proc_namestr+36],ebx
        mov     DWORD PTR [proc_namestr+40],ecx
        mov     DWORD PTR [proc_namestr+44],edx

just_extfeat:
        ; Query and save the extended features bits
        mov     eax,080000001h      ; Select function 0x80000001
        CPUID
        mov     [ext_features],edx  ; Store extended features bits
        mov     eax,1               ; Set "Has CPUID" flag to true

no_features:
        mov     res,eax
    }

    return res;
}


// eof
