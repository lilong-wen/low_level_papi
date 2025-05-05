# low_level_papi

This is a standalone Python performance counter interface, designed based on the PAPI (Performance Application Programming Interface) API, but doesn't require installation of the external PAPI library.

## Features

- No need to install PAPI library
- Provides basic performance counting capabilities: cycle counting, instruction counting, IPC measurements, etc.
- Python interface compatible with the standard PAPI API
- Easy to install and use in any environment

## Installation

```bash
cd low_level_papi
pip install .
```

## Simple Usage

```python
import low_level_papi as llp

# Initialize the library
llp.library_init()

# Create an event set
eventset = llp.create_eventset()

# Add counting events
llp.add_event(eventset, llp.events.PAPI_TOT_CYC)  # Total cycles
llp.add_event(eventset, llp.events.PAPI_TOT_INS)  # Total instructions

# Start counting
llp.start(eventset)

# Run the code to measure
result = 0
for i in range(1000000):
    result += i

# Stop counting and get results
values = llp.stop(eventset)
print(f"Total cycles: {values[0]:,}")
print(f"Total instructions: {values[1]:,}")
print(f"Instructions per cycle: {values[1]/values[0]:.2f}")

# Clean up resources
llp.cleanup_eventset(eventset)
llp.destroy_eventset(eventset)
llp.shutdown()
```

## Notes

This library implements core PAPI functionality, primarily for simple performance counting and analysis. For more complex requirements or when specific hardware counters are needed, it's recommended to use the complete PAPI library.


