# Python libchrony

A Python interface for monitoring the [chrony](https://chrony-project.org/) time synchronization daemon.

## Version

Version 1.0.3 (2025-04-26)

## Acknowledgements

This library is a Python port of [libchrony](https://gitlab.com/chrony/libchrony), created by Miroslav Lichvar. All credit for the protocol implementation and design goes to him and the chrony project contributors.

## Overview

Python libchrony provides a way for Python applications to communicate with and monitor the chrony time synchronization daemon (chronyd). Using this library, you can:

- Check the current synchronization status of your system's clock
- View information about configured time sources
- Monitor performance metrics and statistics
- Access detailed timing data

This library is useful for:

- System administrators who want to monitor their time servers
- Applications that need to verify clock synchronization
- Monitoring tools that track NTP performance
- Anyone who wants to access chrony information from Python code

## Features

- **Easy to use**: Simple, Pythonic interface to monitor chronyd
- **Comprehensive**: Access to all reports and data that the original libchrony library provides
- **Flexible connections**: Connect via Unix sockets or network (IPv4/IPv6)
- **Backward compatible**: Original C-like API is also available

## Quick Start

```python
import libchrony

# Connect to chronyd using the default connection method
with libchrony.connect() as chrony:
    # Get the current synchronization status
    tracking = chrony.get_tracking()
    
    # Print basic information
    print(f"Reference ID: {tracking['reference ID'].value}")
    print(f"Stratum: {tracking['stratum'].value}")
    print(f"Current correction: {tracking['current correction'].value} seconds")
    
    # Get information about time sources
    sources = chrony.get_sources()
    print(f"\nTime sources ({len(sources)}):")
    
    for source in sources:
        address = next((f.value for f in source.fields if 'address' in f.name), "unknown")
        state = source['state'].value
        print(f"  {address} - {state}")
```

## Installation

```bash
pip install libchrony
```

## Requirements

- Python 3.10 or newer
- A running chrony daemon (chronyd)
- The user running the Python code must have permission to access the chronyd socket

## Documentation

For detailed information on how to use this library, see:

- Library_Functions.md - Comprehensive documentation of all functions in both the direct and Pythonic APIs
- Example Scripts example-methods.py and example-reports.py - Example scripts demonstrating various use cases
- API_Reference.md - Complete reference of all classes, methods, and properties

## License

This library is licensed under the GNU Lesser General Public License (LGPL) version 2.1 or later. See the [LICENSE](LICENSE.md) file for details.

The GNU LGPL allows you to use the library in your applications (even proprietary ones) without releasing your application code, but requires that any modifications to the library itself be distributed under the terms of the LGPL.
