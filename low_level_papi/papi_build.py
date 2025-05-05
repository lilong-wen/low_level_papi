"""
CFFI build script for the low_level_pipa module.
"""
import os
import sys
from cffi import FFI

_ROOT = os.path.abspath(os.path.dirname(__file__))
_PAPI_H = os.path.join(_ROOT, "papi.h")
_PAPI_ROOT = os.path.abspath(os.path.join(_ROOT, "..", "..", "papi"))

# Find PAPI library and headers
if not os.path.exists(os.path.join(_PAPI_ROOT, "src", "libpapi.a")):
    _PAPI_ROOT = os.environ.get("PAPI_ROOT", _PAPI_ROOT)
    if not os.path.exists(os.path.join(_PAPI_ROOT, "src", "libpapi.a")):
        print("ERROR: Cannot find PAPI library (libpapi.a)")
        print("Please set the PAPI_ROOT environment variable to your PAPI installation directory")
        print("or install PAPI in the default location")
        sys.exit(1)

ffibuilder = FFI()
ffibuilder.set_source(
    "low_level_pipa._papi",
    '#include "papi.h"',
    extra_objects=[os.path.join(_PAPI_ROOT, "src", "libpapi.a")],
    include_dirs=[_ROOT, os.path.join(_PAPI_ROOT, "src")],
    libraries=["pthread", "rt"],  # Common dependencies for PAPI
)
ffibuilder.cdef(open(_PAPI_H, "r").read())

if __name__ == "__main__":
    print(f"Building _papi extension module using PAPI from: {_PAPI_ROOT}")
    ffibuilder.compile(verbose=True)
