"""
Low-Level PIPA - Python interface for PAPI (Performance Application Programming Interface)
"""

from . import core
from . import events
from . import consts
from . import exceptions
from . import structs

# Export core functions at the top level
from .core import (
    library_init, shutdown, 
    create_eventset, add_event, add_events, 
    start, stop, read, reset,
    cleanup_eventset, destroy_eventset,
    num_components, get_real_cyc, get_real_usec, 
    get_virt_cyc, get_virt_usec,
    flops, flips, ipc, epc,
    is_initialized, strerror,
    remove_event, remove_events, remove_named_event,
    list_events, num_events, state,
    get_event_info, event_code_to_name, event_name_to_code,
    enum_event, get_component_info, get_hardware_info,
    get_executable_info, get_dmem_info,
    get_real_nsec, get_virt_nsec
)

__all__ = [
    "core",
    "events",
    "consts",
    "exceptions",
    "structs",
    "library_init",
    "shutdown",
    "create_eventset",
    "add_event",
    "add_events",
    "remove_event",
    "remove_events",
    "remove_named_event",
    "list_events",
    "num_events",
    "start",
    "stop",
    "read",
    "reset",
    "state",
    "cleanup_eventset",
    "destroy_eventset",
    "get_event_info",
    "event_code_to_name",
    "event_name_to_code",
    "enum_event",
    "num_components",
    "get_component_info",
    "get_hardware_info",
    "get_executable_info",
    "get_dmem_info",
    "get_real_cyc",
    "get_real_usec",
    "get_real_nsec",
    "get_virt_cyc",
    "get_virt_usec",
    "get_virt_nsec",
    "flops",
    "flips",
    "ipc",
    "epc",
    "is_initialized",
    "strerror",
]

__version__ = "0.1.0"
