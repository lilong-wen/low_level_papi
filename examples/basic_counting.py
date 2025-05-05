#!/usr/bin/env python3
"""
A simple example of using low_level_pipa to count events.
"""
import sys
import time
import os

# Add the parent directory to sys.path to properly import the package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import low_level_pipa as llp
from low_level_papi.events import (
    PAPI_TOT_CYC, 
    PAPI_TOT_INS
)

def main():
    """Main function."""
    # Initialize the PAPI library
    llp.library_init()
    
    # Create an event set
    try:
        eventset = llp.create_eventset()
    except llp.exceptions.PapiError as e:
        print(f"Error creating event set: {e}")
        return 1
    
    # Add events to count
    try:
        llp.add_event(eventset, PAPI_TOT_CYC)  # Total cycles
        llp.add_event(eventset, PAPI_TOT_INS)  # Total instructions
    except llp.exceptions.PapiError as e:
        print(f"Error adding events: {e}")
        return 1
    
    # Start counting
    try:
        llp.start(eventset)
    except llp.exceptions.PapiError as e:
        print(f"Error starting event set: {e}")
        return 1
    
    # Execute some code to measure
    print("Performing calculations...")
    start_time = time.time()
    result = 0
    for i in range(10000000):
        result += i
    end_time = time.time()
    print(f"Result: {result}")
    print(f"Python time: {end_time - start_time:.6f} seconds")
    
    # Stop counting and get results
    try:
        values = llp.stop(eventset)
        print(f"Total cycles: {values[0]:,}")
        print(f"Total instructions: {values[1]:,}")
        print(f"Instructions per cycle: {values[1]/values[0]:.2f}")
    except llp.exceptions.PapiError as e:
        print(f"Error stopping event set: {e}")
        return 1
    
    # Clean up resources
    try:
        llp.cleanup_eventset(eventset)
        llp.destroy_eventset(eventset)
    except llp.exceptions.PapiError as e:
        print(f"Error cleaning up: {e}")
        return 1
    
    # Try using IPC measurement
    print("\nUsing the IPC utility function:")
    try:
        ipc_result = llp.ipc()
        print(f"Real time: {ipc_result.real_time:.6f} seconds")
        print(f"CPU time: {ipc_result.proc_time:.6f} seconds")
        print(f"Instructions: {ipc_result.ins:,}")
        print(f"IPC: {ipc_result.ipc:.2f}")
    except llp.exceptions.PapiError as e:
        print(f"Error measuring IPC: {e}")
        return 1
    
    llp.shutdown()
    return 0

if __name__ == "__main__":
    sys.exit(main())
