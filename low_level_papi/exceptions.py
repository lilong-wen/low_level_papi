"""
Exception handling for the low_level_pipa module.
"""
import functools
from ._papi import lib, ffi

class PapiError(Exception):
    """Base class for all PAPI errors."""
    def __init__(self, code=None, message=None):
        self.code = code
        if message is None and code is not None:
            message = ffi.string(lib.PAPI_strerror(code)).decode("utf-8")
        super().__init__(message)

class PapiInvalidValueError(PapiError):
    """Raised when a PAPI function is passed an invalid value."""
    pass

class PapiNoMemoryError(PapiError):
    """Raised when a PAPI function cannot allocate memory."""
    pass

class PapiSystemError(PapiError):
    """Raised when a PAPI function encounters a system error."""
    pass

class PapiComponentError(PapiError):
    """Raised when a PAPI component encounters an error."""
    pass

class PapiCountersLostError(PapiError):
    """Raised when access to counters was lost or interrupted."""
    pass

class PapiBugError(PapiError):
    """Raised when a PAPI internal error occurs."""
    pass

class PapiNoEventError(PapiError):
    """Raised when a PAPI event does not exist."""
    pass

class PapiConflictError(PapiError):
    """Raised when a PAPI event cannot be counted due to counter resource limitations."""
    pass

class PapiNotRunningError(PapiError):
    """Raised when an EventSet is currently not running."""
    pass

class PapiIsRunningError(PapiError):
    """Raised when an EventSet is currently counting."""
    pass

class PapiNoEventSetError(PapiError):
    """Raised when no such EventSet is available."""
    pass

class PapiNotPresetError(PapiError):
    """Raised when an event is not a valid preset."""
    pass

class PapiNoCounterError(PapiError):
    """Raised when hardware does not support performance counters."""
    pass

class PapiMiscError(PapiError):
    """Raised for unknown error codes."""
    pass

class PapiPermissionError(PapiError):
    """Raised when permission level does not permit operation."""
    pass

class PapiNotInitializedError(PapiError):
    """Raised when PAPI hasn't been initialized yet."""
    pass

class PapiNoComponentError(PapiError):
    """Raised when a component index isn't set."""
    pass

class PapiNotSupportedError(PapiError):
    """Raised when an operation is not supported."""
    pass

class PapiNotImplementedError(PapiError):
    """Raised when a feature is not implemented."""
    pass

class PapiBufferError(PapiError):
    """Raised when a buffer size is exceeded."""
    pass

class PapiInvalidDomainError(PapiError):
    """Raised when an EventSet domain is not supported for the operation."""
    pass

class PapiAttributeError(PapiError):
    """Raised when event attributes are invalid or missing."""
    pass

class PapiCountError(PapiError):
    """Raised when there are too many events or attributes."""
    pass

class PapiComboError(PapiError):
    """Raised for a bad combination of features."""
    pass

class PapiComponentDisabledError(PapiError):
    """Raised when a component containing an event is disabled."""
    pass

class PapiDelayInitError(PapiError):
    """Raised when a component cannot be initialized."""
    pass

# Map PAPI error codes to exception classes
ERROR_MAP = {
    lib.PAPI_EINVAL: PapiInvalidValueError,
    lib.PAPI_ENOMEM: PapiNoMemoryError,
    lib.PAPI_ESYS: PapiSystemError,
    lib.PAPI_ECMP: PapiComponentError,
    lib.PAPI_ECLOST: PapiCountersLostError,
    lib.PAPI_EBUG: PapiBugError,
    lib.PAPI_ENOEVNT: PapiNoEventError,
    lib.PAPI_ECNFLCT: PapiConflictError,
    lib.PAPI_ENOTRUN: PapiNotRunningError,
    lib.PAPI_EISRUN: PapiIsRunningError,
    lib.PAPI_ENOEVST: PapiNoEventSetError,
    lib.PAPI_ENOTPRESET: PapiNotPresetError,
    lib.PAPI_ENOCNTR: PapiNoCounterError,
    lib.PAPI_EMISC: PapiMiscError,
    lib.PAPI_EPERM: PapiPermissionError,
    lib.PAPI_ENOINIT: PapiNotInitializedError,
    lib.PAPI_ENOCMP: PapiNoComponentError,
    lib.PAPI_ENOSUPP: PapiNotSupportedError,
    lib.PAPI_ENOIMPL: PapiNotImplementedError,
    lib.PAPI_EBUF: PapiBufferError,
    lib.PAPI_EINVAL_DOM: PapiInvalidDomainError,
    lib.PAPI_EATTR: PapiAttributeError,
    lib.PAPI_ECOUNT: PapiCountError,
    lib.PAPI_ECOMBO: PapiComboError,
    lib.PAPI_ECMP_DISABLED: PapiComponentDisabledError,
    lib.PAPI_EDELAY_INIT: PapiDelayInitError,
}

def papi_error(func):
    """Decorator to check PAPI return codes and raise appropriate exceptions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        
        if isinstance(ret, tuple):
            rcode, result = ret
        else:
            rcode, result = ret, None
            
        if rcode < 0:
            error_class = ERROR_MAP.get(rcode, PapiError)
            raise error_class(rcode)
        
        if result is not None:
            return result
        else:
            return rcode
            
    return wrapper
