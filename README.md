# Low-Level PAPI

Low-Level PAPI is a Python binding for the Performance Application Programming Interface (PAPI).
PAPI provides access to hardware performance counters on most modern processors.

## Installation

```bash
pip install low_level_papi
```

Or from source:

```bash
git clone https://github.com/your-organization/low_level_papi.git
cd low_level_papi
pip install -e .
```

## Usage

```python
import low_level_papi as llp

# Initialize the PAPI library
llp.library_init()

# Create an event set
event_set = llp.create_eventset()

# Add an event to the event set
llp.add_event(event_set, llp.events.PAPI_TOT_CYC)

# Start counting
llp.start(event_set)

# Your code to measure
for i in range(1000000):
    pass

# Stop counting and get results
values = llp.stop(event_set)
print(f"Total cycles: {values[0]}")

# Clean up
llp.cleanup_eventset(event_set)
llp.destroy_eventset(event_set)
llp.shutdown()
```

## Features

- Access to all PAPI preset events
- Support for hardware performance counters
- Easy-to-use Python API
- Efficient CFFI-based implementation

