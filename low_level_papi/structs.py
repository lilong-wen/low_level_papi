"""
Data structures for the low_level_pipa module.
"""
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class EVENT_info:
    """Information about a PAPI event."""
    event_code: int
    symbol: str
    short_descr: str
    long_descr: str
    component_index: int
    units: str
    location: int
    data_type: int
    value_type: int
    timescope: int
    update_type: int
    update_freq: int
    count: int
    event_type: int
    derived: str
    postfix: str
    code: List[int]
    name: List[str]
    note: str


@dataclass
class HARDWARE_info:
    """Information about the system hardware."""
    ncpu: int
    threads: int
    cores: int
    sockets: int
    nnodes: int
    totalcpus: int
    vendor: int
    vendor_string: str
    model: int
    model_string: str
    revision: float
    cpuid_family: int
    cpuid_model: int
    cpuid_stepping: int
    cpu_max_mhz: int
    cpu_min_mhz: int


@dataclass
class DMEM_info:
    """Dynamic memory usage information."""
    peak: int
    size: int
    resident: int
    high_water_mark: int
    shared: int
    text: int
    library: int
    heap: int
    locked: int
    stack: int
    pagesize: int
    pte: int


@dataclass
class EXECUTABLE_info:
    """Information about the executable."""
    fullname: str
    address_info: Dict[str, int]


@dataclass
class COMPONENT_info:
    """Information about a PAPI component."""
    name: str
    short_name: str
    description: str
    version: str
    support_version: str
    kernel_version: str
    disabled_reason: str
    disabled: int
    cmp_idx: int
    num_cntrs: int
    num_mpx_cntrs: int
    num_preset_events: int
    num_native_events: int
    default_domain: int
    available_domains: int
    default_granularity: int
    available_granularities: int
    hardware_intr_sig: int
    pmu_names: List[str]
    hardware_intr: bool
    precise_intr: bool
    posix1b_timers: bool
    kernel_profile: bool
    kernel_multiplex: bool
    data_address_range: bool
    instr_address_range: bool
    fast_counter_read: bool
    fast_real_timer: bool
    fast_virtual_timer: bool
    attach: bool
    attach_must_ptrace: bool
    edge_detect: bool
    invert: bool
    read_reset: bool
    inherit: bool
    cpu: bool
    cntr_umasks: bool


@dataclass
class SHARED_LIB_info:
    """Information about shared libraries."""
    count: int
    map_: List[Dict[str, int]]


@dataclass
class Flips:
    """Result of the flips function."""
    event_name: str
    real_time: float
    proc_time: float
    flpins: int
    mflips: float


@dataclass
class Flops:
    """Result of the flops function."""
    event_name: str
    real_time: float
    proc_time: float
    flpops: int
    mflops: float


@dataclass
class IPC:
    """Result of the ipc function."""
    real_time: float
    proc_time: float
    ins: int
    ipc: float


@dataclass
class EPC:
    """Result of the epc function."""
    real_time: float
    proc_time: float
    ref: int
    core: int
    evt: int
    epc: float
