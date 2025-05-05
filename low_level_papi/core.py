"""
Core functionality for the low_level_pipa module.

This module provides direct bindings to PAPI's low-level functions, making them
accessible from Python with proper error handling and data conversion.
"""

from ctypes import c_longlong, c_ulonglong
import os
import sys

try:
    from ._papi import lib, ffi
except ModuleNotFoundError:
    raise ImportError(
        "The _papi module was not found. You need to build the CFFI module first.\n"
        "Try running:\n"
        "    python -m low_level_pipa.papi_build\n"
        "or:\n"
        "    python setup.py build_ext --inplace\n"
        "from the project root directory."
    )

from .exceptions import papi_error, PapiError
from .consts import PAPI_VER_CURRENT, PAPI_NULL
from .structs import (
    EVENT_info, HARDWARE_info, DMEM_info, EXECUTABLE_info,
    COMPONENT_info, SHARED_LIB_info, Flips, Flops, IPC
)

@papi_error
def library_init(version=PAPI_VER_CURRENT):
    """Initialize the PAPI library.

    This function must be called before any other PAPI functions can be used.
    It may be called multiple times.

    Parameters
    ----------
    version : int, optional
        PAPI version number. Defaults to the current PAPI version.

    Returns
    -------
    int
        PAPI version of the library or a PAPI error code if negative.

    Raises
    ------
    PapiError
        If the initialization fails.
    """
    rcode = lib.PAPI_library_init(version)
    return rcode, rcode


def shutdown():
    """Shut down the PAPI library.

    This function frees all memory and resources used by the PAPI library.
    """
    lib.PAPI_shutdown()


@papi_error
def is_initialized():
    """Check if the PAPI library is initialized.

    Returns
    -------
    bool
        True if the library is initialized, False otherwise.
    """
    rcode = lib.PAPI_is_initialized()
    return rcode, bool(rcode)


@papi_error
def create_eventset():
    """Create a new empty PAPI event set.

    Returns
    -------
    int
        The new event set identifier.

    Raises
    ------
    PapiError
        If the event set cannot be created.
    """
    eventSet = ffi.new("int*", 0)
    rcode = lib.PAPI_create_eventset(eventSet)
    return rcode, ffi.unpack(eventSet, 1)[0]


@papi_error
def add_event(eventSet, eventCode):
    """Add a single event to an existing event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier returned by create_eventset().
    eventCode : int
        Code of the event to add to the event set.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the event cannot be added to the event set.
    """
    rcode = lib.PAPI_add_event(eventSet, eventCode)
    return rcode, None


@papi_error
def add_named_event(eventSet, eventName):
    """Add an event by name to an existing event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier returned by create_eventset().
    eventName : str
        Name of the event to add to the event set.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the event cannot be added to the event set.
    """
    eventName_p = ffi.new("char[]", eventName.encode("ascii"))
    rcode = lib.PAPI_add_named_event(eventSet, eventName_p)
    return rcode, None


@papi_error
def add_events(eventSet, eventCodes):
    """Add multiple events to an existing event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier returned by create_eventset().
    eventCodes : list of int
        List of event codes to add to the event set.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the events cannot be added to the event set.
    """
    number = len(eventCodes)
    eventCodes_p = ffi.new("int[]", eventCodes)
    rcode = lib.PAPI_add_events(eventSet, eventCodes_p, number)
    return rcode, None


@papi_error
def remove_event(eventSet, eventCode):
    """Remove a single event from an existing event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.
    eventCode : int
        Code of the event to remove from the event set.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the event cannot be removed from the event set.
    """
    rcode = lib.PAPI_remove_event(eventSet, eventCode)
    return rcode, None


@papi_error
def remove_named_event(eventSet, eventName):
    """Remove an event by name from an existing event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.
    eventName : str
        Name of the event to remove from the event set.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the event cannot be removed from the event set.
    """
    eventName_p = ffi.new("char[]", eventName.encode("ascii"))
    rcode = lib.PAPI_remove_named_event(eventSet, eventName_p)
    return rcode, None


@papi_error
def remove_events(eventSet, eventCodes):
    """Remove multiple events from an existing event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.
    eventCodes : list of int
        List of event codes to remove from the event set.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the events cannot be removed from the event set.
    """
    number = len(eventCodes)
    eventCodes_p = ffi.new("int[]", eventCodes)
    rcode = lib.PAPI_remove_events(eventSet, eventCodes_p, number)
    return rcode, None


@papi_error
def list_events(eventSet):
    """List the events that are members of an event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    list of int
        List of event codes in the event set.

    Raises
    ------
    PapiError
        If the events cannot be listed.
    """
    number_p = ffi.new("int*", 0)
    rcode = lib.PAPI_num_events(eventSet)
    if rcode < 0:
        return rcode, []

    number = rcode
    number_p[0] = number
    events_p = ffi.new("int[]", number)
    rcode = lib.PAPI_list_events(eventSet, events_p, number_p)
    
    if rcode == 0:
        return rcode, [events_p[i] for i in range(number)]
    else:
        return rcode, []


@papi_error
def num_events(eventSet):
    """Return the number of events in an event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    int
        Number of events in the event set.

    Raises
    ------
    PapiError
        If the number of events cannot be determined.
    """
    rcode = lib.PAPI_num_events(eventSet)
    return rcode, rcode


@papi_error
def cleanup_eventset(eventSet):
    """Remove all events from an event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the event set cannot be cleaned up.
    """
    rcode = lib.PAPI_cleanup_eventset(eventSet)
    return rcode, None


@papi_error
def destroy_eventset(eventSet):
    """Destroy an event set and free its resources.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the event set cannot be destroyed.
    """
    eventSet_p = ffi.new("int*", eventSet)
    rcode = lib.PAPI_destroy_eventset(eventSet_p)
    return rcode, None


@papi_error
def start(eventSet):
    """Start counting hardware events in an event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the event set cannot be started.
    """
    rcode = lib.PAPI_start(eventSet)
    return rcode, None


@papi_error
def stop(eventSet):
    """Stop counting hardware events in an event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    list of int
        List of event values.

    Raises
    ------
    PapiError
        If the event set cannot be stopped.
    """
    eventCount = lib.PAPI_num_events(eventSet)
    if eventCount < 0:
        return eventCount, []

    values = ffi.new("long long[]", eventCount)
    rcode = lib.PAPI_stop(eventSet, values)
    
    if rcode == 0:
        return rcode, list(ffi.unpack(values, eventCount))
    else:
        return rcode, []


@papi_error
def read(eventSet):
    """Read hardware events from an event set without resetting.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    list of int
        List of event values.

    Raises
    ------
    PapiError
        If the event set cannot be read.
    """
    eventCount = lib.PAPI_num_events(eventSet)
    if eventCount < 0:
        return eventCount, []

    values = ffi.new("long long[]", eventCount)
    rcode = lib.PAPI_read(eventSet, values)
    
    if rcode == 0:
        return rcode, list(ffi.unpack(values, eventCount))
    else:
        return rcode, []


@papi_error
def reset(eventSet):
    """Reset the hardware event counts in an event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    int
        PAPI error code (0 if successful).

    Raises
    ------
    PapiError
        If the event set cannot be reset.
    """
    rcode = lib.PAPI_reset(eventSet)
    return rcode, None


@papi_error
def state(eventSet):
    """Return the counting state of an event set.

    Parameters
    ----------
    eventSet : int
        Event set identifier.

    Returns
    -------
    int
        The state of the event set.

    Raises
    ------
    PapiError
        If the state cannot be determined.
    """
    status = ffi.new("int*", 0)
    rcode = lib.PAPI_state(eventSet, status)
    return rcode, ffi.unpack(status, 1)[0]


@papi_error
def get_event_info(eventCode):
    """Get information about a PAPI event.

    Parameters
    ----------
    eventCode : int
        The PAPI event code.

    Returns
    -------
    EVENT_info
        Information about the event.

    Raises
    ------
    PapiError
        If the event information cannot be obtained.
    """
    info = ffi.new("PAPI_event_info_t*")
    rcode = lib.PAPI_get_event_info(eventCode, info)
    
    if rcode == 0:
        return rcode, EVENT_info(
            event_code=info.event_code,
            symbol=ffi.string(info.symbol).decode('utf-8'),
            short_descr=ffi.string(info.short_descr).decode('utf-8'),
            long_descr=ffi.string(info.long_descr).decode('utf-8'),
            component_index=info.component_index,
            units=ffi.string(info.units).decode('utf-8'),
            location=info.location,
            data_type=info.data_type,
            value_type=info.value_type,
            timescope=info.timescope,
            update_type=info.update_type,
            update_freq=info.update_freq,
            count=info.count,
            event_type=info.event_type,
            derived=ffi.string(info.derived).decode('utf-8'),
            postfix=ffi.string(info.postfix).decode('utf-8'),
            code=[info.code[i] for i in range(info.count)],
            name=[ffi.string(info.name[i]).decode('utf-8') for i in range(info.count)],
            note=ffi.string(info.note).decode('utf-8')
        )
    else:
        return rcode, None


@papi_error
def event_code_to_name(eventCode):
    """Convert a PAPI event code to a name.

    Parameters
    ----------
    eventCode : int
        The PAPI event code.

    Returns
    -------
    str
        The name of the event.

    Raises
    ------
    PapiError
        If the event code cannot be converted.
    """
    name = ffi.new("char[]", 256)  # PAPI_MAX_STR_LEN
    rcode = lib.PAPI_event_code_to_name(eventCode, name)
    
    if rcode == 0:
        return rcode, ffi.string(name).decode('utf-8')
    else:
        return rcode, None


@papi_error
def event_name_to_code(eventName):
    """Convert a PAPI event name to a code.

    Parameters
    ----------
    eventName : str
        The name of the event.

    Returns
    -------
    int
        The PAPI event code.

    Raises
    ------
    PapiError
        If the event name cannot be converted.
    """
    eventName_p = ffi.new("char[]", eventName.encode("ascii"))
    code = ffi.new("int*", 0)
    rcode = lib.PAPI_event_name_to_code(eventName_p, code)
    
    if rcode == 0:
        return rcode, ffi.unpack(code, 1)[0]
    else:
        return rcode, None


@papi_error
def enum_event(eventCode, modifier=0):
    """Enumerate the next PAPI event after the given one.

    Parameters
    ----------
    eventCode : int
        The PAPI event code to start from.
    modifier : int, optional
        A modifier to control how the enumeration is done.

    Returns
    -------
    int
        The next PAPI event code.

    Raises
    ------
    PapiError
        If there are no more events to enumerate.
    """
    eventCode_p = ffi.new("int*", eventCode)
    rcode = lib.PAPI_enum_event(eventCode_p, modifier)
    
    if rcode == 0:
        return rcode, ffi.unpack(eventCode_p, 1)[0]
    else:
        return rcode, None


@papi_error
def num_components():
    """Get the number of components available in the PAPI library.

    Returns
    -------
    int
        The number of components.

    Raises
    ------
    PapiError
        If the number of components cannot be determined.
    """
    rcode = lib.PAPI_num_components()
    return rcode, rcode


@papi_error
def get_component_info(cidx):
    """Get information about a PAPI component.

    Parameters
    ----------
    cidx : int
        The component index.

    Returns
    -------
    COMPONENT_info
        Information about the component.

    Raises
    ------
    PapiError
        If the component information cannot be obtained.
    """
    info = lib.PAPI_get_component_info(cidx)
    
    if info == ffi.NULL:
        return -1, None
    
    pmu_names = []
    for i in range(40):  # PAPI_PMU_MAX
        if info.pmu_names[i] == ffi.NULL:
            break
        pmu_names.append(ffi.string(info.pmu_names[i]).decode('utf-8'))
    
    return 0, COMPONENT_info(
        name=ffi.string(info.name).decode('utf-8'),
        short_name=ffi.string(info.short_name).decode('utf-8'),
        description=ffi.string(info.description).decode('utf-8'),
        version=ffi.string(info.version).decode('utf-8'),
        support_version=ffi.string(info.support_version).decode('utf-8'),
        kernel_version=ffi.string(info.kernel_version).decode('utf-8'),
        disabled_reason=ffi.string(info.disabled_reason).decode('utf-8'),
        disabled=info.disabled,
        cmp_idx=info.CmpIdx,
        num_cntrs=info.num_cntrs,
        num_mpx_cntrs=info.num_mpx_cntrs,
        num_preset_events=info.num_preset_events,
        num_native_events=info.num_native_events,
        default_domain=info.default_domain,
        available_domains=info.available_domains,
        default_granularity=info.default_granularity,
        available_granularities=info.available_granularities,
        hardware_intr_sig=info.hardware_intr_sig,
        pmu_names=pmu_names,
        hardware_intr=bool(info.hardware_intr),
        precise_intr=bool(info.precise_intr),
        posix1b_timers=bool(info.posix1b_timers),
        kernel_profile=bool(info.kernel_profile),
        kernel_multiplex=bool(info.kernel_multiplex),
        data_address_range=bool(info.data_address_range),
        instr_address_range=bool(info.instr_address_range),
        fast_counter_read=bool(info.fast_counter_read),
        fast_real_timer=bool(info.fast_real_timer),
        fast_virtual_timer=bool(info.fast_virtual_timer),
        attach=bool(info.attach),
        attach_must_ptrace=bool(info.attach_must_ptrace),
        edge_detect=bool(info.edge_detect),
        invert=bool(info.invert),
        read_reset=bool(info.read_reset),
        inherit=bool(info.inherit),
        cpu=bool(info.cpu),
        cntr_umasks=bool(info.cntr_umasks)
    )


@papi_error
def get_hardware_info():
    """Get information about the system hardware.

    Returns
    -------
    HARDWARE_info
        Information about the system hardware.

    Raises
    ------
    PapiError
        If the hardware information cannot be obtained.
    """
    info = lib.PAPI_get_hardware_info()
    
    if info == ffi.NULL:
        return -1, None
    
    return 0, HARDWARE_info(
        ncpu=info.ncpu,
        threads=info.threads,
        cores=info.cores,
        sockets=info.sockets,
        nnodes=info.nnodes,
        totalcpus=info.totalcpus,
        vendor=info.vendor,
        vendor_string=ffi.string(info.vendor_string).decode('utf-8'),
        model=info.model,
        model_string=ffi.string(info.model_string).decode('utf-8'),
        revision=info.revision,
        cpuid_family=info.cpuid_family,
        cpuid_model=info.cpuid_model,
        cpuid_stepping=info.cpuid_stepping,
        cpu_max_mhz=info.cpu_max_mhz,
        cpu_min_mhz=info.cpu_min_mhz
    )


@papi_error
def get_executable_info():
    """Get information about the executable.

    Returns
    -------
    EXECUTABLE_info
        Information about the executable.

    Raises
    ------
    PapiError
        If the executable information cannot be obtained.
    """
    info = lib.PAPI_get_executable_info()
    
    if info == ffi.NULL:
        return -1, None
    
    address_info = {
        'name': ffi.string(info.address_info.name).decode('utf-8'),
        'text_start': int(ffi.cast("long", info.address_info.text_start)),
        'text_end': int(ffi.cast("long", info.address_info.text_end)),
        'data_start': int(ffi.cast("long", info.address_info.data_start)),
        'data_end': int(ffi.cast("long", info.address_info.data_end)),
        'bss_start': int(ffi.cast("long", info.address_info.bss_start)),
        'bss_end': int(ffi.cast("long", info.address_info.bss_end)),
    }
    
    return 0, EXECUTABLE_info(
        fullname=ffi.string(info.fullname).decode('utf-8'),
        address_info=address_info
    )


@papi_error
def get_dmem_info():
    """Get dynamic memory information.

    Returns
    -------
    DMEM_info
        Dynamic memory information.

    Raises
    ------
    PapiError
        If the memory information cannot be obtained.
    """
    info = ffi.new("PAPI_dmem_info_t*")
    rcode = lib.PAPI_get_dmem_info(info)
    
    if rcode == 0:
        return rcode, DMEM_info(
            peak=info.peak,
            size=info.size,
            resident=info.resident,
            high_water_mark=info.high_water_mark,
            shared=info.shared,
            text=info.text,
            library=info.library,
            heap=info.heap,
            locked=info.locked,
            stack=info.stack,
            pagesize=info.pagesize,
            pte=info.pte
        )
    else:
        return rcode, None


@papi_error
def get_real_cyc():
    """Get real (wall-clock) cycle count.

    Returns
    -------
    int
        The real cycle count.

    Raises
    ------
    PapiError
        If the cycle count cannot be obtained.
    """
    rcode = lib.PAPI_get_real_cyc()
    return 0, rcode


@papi_error
def get_real_nsec():
    """Get real time in nanoseconds.

    Returns
    -------
    int
        The real time in nanoseconds.

    Raises
    ------
    PapiError
        If the time cannot be obtained.
    """
    rcode = lib.PAPI_get_real_nsec()
    return 0, rcode


@papi_error
def get_real_usec():
    """Get real time in microseconds.

    Returns
    -------
    int
        The real time in microseconds.

    Raises
    ------
    PapiError
        If the time cannot be obtained.
    """
    rcode = lib.PAPI_get_real_usec()
    return 0, rcode


@papi_error
def get_virt_cyc():
    """Get virtual (CPU) cycle count.

    Returns
    -------
    int
        The virtual cycle count.

    Raises
    ------
    PapiError
        If the cycle count cannot be obtained.
    """
    rcode = lib.PAPI_get_virt_cyc()
    return 0, rcode


@papi_error
def get_virt_nsec():
    """Get virtual time in nanoseconds.

    Returns
    -------
    int
        The virtual time in nanoseconds.

    Raises
    ------
    PapiError
        If the time cannot be obtained.
    """
    rcode = lib.PAPI_get_virt_nsec()
    return 0, rcode


@papi_error
def get_virt_usec():
    """Get virtual time in microseconds.

    Returns
    -------
    int
        The virtual time in microseconds.

    Raises
    ------
    PapiError
        If the time cannot be obtained.
    """
    rcode = lib.PAPI_get_virt_usec()
    return 0, rcode


@papi_error
def flips(event=0):
    """Get floating point instruction rate.

    Parameters
    ----------
    event : int, optional
        The event to use for the measurement.

    Returns
    -------
    Flips
        Flips measurement data.

    Raises
    ------
    PapiError
        If the measurement cannot be obtained.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    flpins = ffi.new("long long*", 0)
    mflips = ffi.new("float*", 0)

    rcode = lib.PAPI_flips(rtime, ptime, flpins, mflips)

    if rcode == 0:
        return rcode, Flips(
            event_name="PAPI_FP_INS" if event == 0 else event_code_to_name(event),
            real_time=ffi.unpack(rtime, 1)[0],
            proc_time=ffi.unpack(ptime, 1)[0],
            flpins=ffi.unpack(flpins, 1)[0],
            mflips=ffi.unpack(mflips, 1)[0]
        )
    else:
        return rcode, None


@papi_error
def flops(event=0):
    """Get floating point operation rate.

    Parameters
    ----------
    event : int, optional
        The event to use for the measurement.

    Returns
    -------
    Flops
        Flops measurement data.

    Raises
    ------
    PapiError
        If the measurement cannot be obtained.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    flpops = ffi.new("long long*", 0)
    mflops = ffi.new("float*", 0)

    rcode = lib.PAPI_flops(rtime, ptime, flpops, mflops)

    if rcode == 0:
        return rcode, Flops(
            event_name="PAPI_FP_OPS" if event == 0 else event_code_to_name(event),
            real_time=ffi.unpack(rtime, 1)[0],
            proc_time=ffi.unpack(ptime, 1)[0],
            flpops=ffi.unpack(flpops, 1)[0],
            mflops=ffi.unpack(mflops, 1)[0]
        )
    else:
        return rcode, None


@papi_error
def ipc():
    """Get instructions per cycle.

    Returns
    -------
    IPC
        Instructions per cycle measurement data.

    Raises
    ------
    PapiError
        If the measurement cannot be obtained.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    ins = ffi.new("long long*", 0)
    ipc = ffi.new("float*", 0)

    rcode = lib.PAPI_ipc(rtime, ptime, ins, ipc)

    if rcode == 0:
        return rcode, IPC(
            real_time=ffi.unpack(rtime, 1)[0],
            proc_time=ffi.unpack(ptime, 1)[0],
            ins=ffi.unpack(ins, 1)[0],
            ipc=ffi.unpack(ipc, 1)[0]
        )
    else:
        return rcode, None


@papi_error
def epc(event=0):
    """Get events per cycle.

    Parameters
    ----------
    event : int, optional
        The event to use for the measurement.

    Returns
    -------
    dict
        Events per cycle measurement data.

    Raises
    ------
    PapiError
        If the measurement cannot be obtained.
    """
    rtime = ffi.new("float*", 0)
    ptime = ffi.new("float*", 0)
    ref = ffi.new("long long*", 0)
    core = ffi.new("long long*", 0)
    evt = ffi.new("long long*", 0)
    epc = ffi.new("float*", 0)

    rcode = lib.PAPI_epc(event, rtime, ptime, ref, core, evt, epc)

    if rcode == 0:
        return rcode, {
            "real_time": ffi.unpack(rtime, 1)[0],
            "proc_time": ffi.unpack(ptime, 1)[0],
            "ref": ffi.unpack(ref, 1)[0],
            "core": ffi.unpack(core, 1)[0],
            "evt": ffi.unpack(evt, 1)[0],
            "epc": ffi.unpack(epc, 1)[0]
        }
    else:
        return rcode, None


def strerror(errcode):
    """Get the error message for a PAPI error code.

    Parameters
    ----------
    errcode : int
        The PAPI error code.

    Returns
    -------
    str
        The error message.
    """
    msg = lib.PAPI_strerror(errcode)
    if msg == ffi.NULL:
        return f"Unknown error: {errcode}"
    return ffi.string(msg).decode('utf-8')
