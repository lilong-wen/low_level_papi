"""
Constants for the low_level_pipa module.
"""
from ._papi import lib, ffi

def _papi_version_number(maj, min_, rev, inc):
    return ((maj) << 24) | ((min_) << 16) | ((rev) << 8) | (inc)

# Version
PAPI_VER_CURRENT = lib.PAPI_VERSION_CURRENT

# Masks
PAPI_PRESET_MASK = lib.PAPI_PRESET_MASK
PAPI_NATIVE_MASK = lib.PAPI_NATIVE_MASK

# String lengths
PAPI_MAX_STR_LEN = lib.PAPI_MAX_STR_LEN
PAPI_MIN_STR_LEN = lib.PAPI_MIN_STR_LEN
PAPI_2MAX_STR_LEN = lib.PAPI_2MAX_STR_LEN
PAPI_HUGE_STR_LEN = lib.PAPI_HUGE_STR_LEN

# Special values
PAPI_NULL = lib.PAPI_NULL

# Domains
PAPI_DOM_USER = lib.PAPI_DOM_USER
PAPI_DOM_KERNEL = lib.PAPI_DOM_KERNEL
PAPI_DOM_OTHER = lib.PAPI_DOM_OTHER
PAPI_DOM_SUPERVISOR = lib.PAPI_DOM_SUPERVISOR
PAPI_DOM_ALL = (PAPI_DOM_USER | PAPI_DOM_KERNEL | PAPI_DOM_OTHER | PAPI_DOM_SUPERVISOR)
PAPI_DOM_HWSPEC = lib.PAPI_DOM_HWSPEC

# Granularities
PAPI_GRN_THR = lib.PAPI_GRN_THR
PAPI_GRN_PROC = lib.PAPI_GRN_PROC
PAPI_GRN_PROCG = lib.PAPI_GRN_PROCG
PAPI_GRN_SYS = lib.PAPI_GRN_SYS
PAPI_GRN_SYS_CPU = lib.PAPI_GRN_SYS_CPU
PAPI_GRN_MIN = PAPI_GRN_THR
PAPI_GRN_MAX = PAPI_GRN_SYS_CPU

# Debug levels
PAPI_QUIET = lib.PAPI_QUIET
PAPI_VERB_ECONT = lib.PAPI_VERB_ECONT
PAPI_VERB_ESTOP = lib.PAPI_VERB_ESTOP

# Event states
PAPI_STOPPED = lib.PAPI_STOPPED
PAPI_RUNNING = lib.PAPI_RUNNING
PAPI_PAUSED = lib.PAPI_PAUSED
PAPI_NOT_INIT = lib.PAPI_NOT_INIT
PAPI_OVERFLOWING = lib.PAPI_OVERFLOWING
PAPI_PROFILING = lib.PAPI_PROFILING
PAPI_MULTIPLEXING = lib.PAPI_MULTIPLEXING
PAPI_ATTACHED = lib.PAPI_ATTACHED
PAPI_CPU_ATTACHED = lib.PAPI_CPU_ATTACHED

# Locks
PAPI_USR1_LOCK = lib.PAPI_USR1_LOCK
PAPI_USR2_LOCK = lib.PAPI_USR2_LOCK
PAPI_NUM_LOCK = lib.PAPI_NUM_LOCK

# Special events
PAPI_FP_INS = lib.PAPI_FP_INS
PAPI_FP_OPS = lib.PAPI_FP_OPS
PAPI_VEC_SP = lib.PAPI_VEC_SP
PAPI_VEC_DP = lib.PAPI_VEC_DP
