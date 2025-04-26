#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright ©2025 Rob Gill
Based upon libchrony by Miroslav Lichvar

Version 1.0

SPDX-License-Identifier: LGPL-2.1-or-later

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library.  If not, see
<http://www.gnu.org/licenses/>.

*****************************************************************************

Example program for the Python port of libchrony
Shows both the direct client API (C-style) and the Pythonic interface

"""

import sys
import argparse
import socket
import select
import time
from typing import List, Optional, Dict, Any, Union

# Import both client API (C-style) and Pythonic interface
import chrony_socket
import client
from chrony_formats import ChronyError, ChronyFieldContent, ChronyFieldType, TimeSpec
import libchrony


def process_responses(session) -> ChronyError:
    """Process responses from chronyd, similar to the C example.
    
    Args:
        session: Session object
        
    Returns:
        ChronyError: Error code (0 on success)
    """
    # Get the socket file descriptor
    fd = client.chrony_get_fd(session)
    
    # Create a poll object
    poll_obj = select.poll()
    poll_obj.register(fd, select.POLLIN)
    
    # Timeout (1 second)
    timeout = 1000  # milliseconds
    
    # Process responses
    while client.chrony_needs_response(session):
        # Wait for the socket to be readable
        events = poll_obj.poll(timeout)
        if not events:
            print("Error: No valid response received", file=sys.stderr)
            return -1
        
        # Process the response
        error = client.chrony_process_response(session)
        if error != ChronyError.OK:
            return error
        
        # Reduce timeout
        timeout = max(0, timeout - 100)
    
    return ChronyError.OK


def print_report_direct_api(session, report_index: int) -> int:
    """Print a report using the direct client API.
    
    Args:
        session: Session object
        report_index: Index of the report
        
    Returns:
        int: Error code (0 on success)
    """
    # Get the report name
    report_name = client.chrony_get_report_name(report_index)
    print(f"{report_name}:")
    
    # Request the number of records
    error = client.chrony_request_report_number_records(session, report_name)
    if error != ChronyError.OK:
        return error
    
    # Process the responses
    error = process_responses(session)
    if error != ChronyError.OK:
        return error
    
    # Get the number of records
    num_records = client.chrony_get_report_number_records(session)
    
    # Process each record
    for i in range(num_records):
        print(f"  Record #{i + 1}:")
        
        # Request the record
        error = client.chrony_request_record(session, report_name, i)
        if error != ChronyError.OK:
            return error
        
        # Process the responses
        error = process_responses(session)
        if error != ChronyError.OK:
            return error
        
        # Get the number of fields
        num_fields = client.chrony_get_record_number_fields(session)
        
        # Print each field
        for j in range(num_fields):
            # Get the field content type
            content = client.chrony_get_field_content(session, j)
            if content == ChronyFieldContent.NONE:
                continue
            
            # Get the field name
            field_name = client.chrony_get_field_name(session, j)
            print(f"    {field_name}: ", end="")
            
            # Get and print the field value based on its type
            field_type = client.chrony_get_field_type(session, j)
            
            match field_type:
                case client.ChronyFieldType.UINTEGER:
                    uval = client.chrony_get_field_uinteger(session, j)
                    
                    if content == ChronyFieldContent.REFERENCE_ID:
                        print(f"{uval:08X}", end="")
                    elif content == ChronyFieldContent.ENUM:
                        const_name = client.chrony_get_field_constant_name(session, j, uval)
                        if const_name:
                            print(f"{const_name}", end="")
                        else:
                            print(f"{uval}", end="")
                    elif content == ChronyFieldContent.FLAGS:
                        # Print flags
                        flag = 1
                        while flag > 0:
                            if (uval & flag) != 0:
                                const_name = client.chrony_get_field_constant_name(session, j, flag)
                                if const_name:
                                    print(f"{const_name} ", end="")
                            flag >>= 1
#                            flag <<= 1
                    elif content == ChronyFieldContent.BOOLEAN:
                        print("Yes" if uval else "No", end="")
                    else:
                        print(f"{uval}", end="")
                
                case client.ChronyFieldType.INTEGER:
                    print(f"{client.chrony_get_field_integer(session, j)}", end="")
                
                case client.ChronyFieldType.FLOAT:
                    print(f"{client.chrony_get_field_float(session, j)}", end="")
                
                case client.ChronyFieldType.STRING:
                    string_val = client.chrony_get_field_string(session, j)
                    if string_val:
                        print(f"{string_val}", end="")
                
                case client.ChronyFieldType.TIMESPEC:
                    ts = client.chrony_get_field_timespec(session, j)
                    print(f"{ts.tv_sec}.{ts.tv_nsec:09d}", end="")
                
                case _:
                    print("?", end="")
            
            # Print units if applicable
            match content:
                case ChronyFieldContent.INTERVAL_LOG2_SECONDS:
                    print(" log2(seconds)")
                case ChronyFieldContent.INTERVAL_SECONDS | ChronyFieldContent.OFFSET_SECONDS | ChronyFieldContent.MEASURE_SECONDS:
                    print(" seconds")
                case ChronyFieldContent.OFFSET_PPM | ChronyFieldContent.MEASURE_PPM:
                    print(" ppm")
                case ChronyFieldContent.OFFSET_PPM_PER_SECOND:
                    print(" ppm per second")
                case ChronyFieldContent.LENGTH_BITS:
                    print(" bits")
                case ChronyFieldContent.LENGTH_BYTES:
                    print(" bytes")
                case _:
                    print()
    
    return ChronyError.OK


def print_all_reports_direct_api(session):
    """Print all reports using the direct client API.
    
    Args:
        session: Session object
    """
    # Get the number of supported reports
    num_reports = client.chrony_get_number_supported_reports()
    
    # Print each report
    for i in range(num_reports):
        error = print_report_direct_api(session, i)
        if error != ChronyError.OK and error != -1:
            print(f"Error: {client.chrony_get_error_string(error)}")
        print()


def print_report_pythonic(report) -> None:
    """Print a report using the Pythonic interface.
    
    Args:
        report: Report object (either Record or Report)
    """
    # Check if it's a single record or a collection of records
    if isinstance(report, libchrony.Record):
        # Single record
        print_record_pythonic(report)
    else:
        # Multiple records
        for i, record in enumerate(report):
            print(f"  Record #{i + 1}:")
            print_record_pythonic(record, indent=4)


def print_record_pythonic(record, indent=0) -> None:
    """Print a record using the Pythonic interface.
    
    Args:
        record: Record object
        indent: Indentation level
    """
    indent_str = " " * indent
    
    # Print each field
    for field in record:
        print(f"{indent_str}{field.name}: ", end="")
        
        # Print the value based on its type and content
        if isinstance(field.value, TimeSpec):
            print(f"{field.value.tv_sec}.{field.value.tv_nsec:09d}", end="")
        elif isinstance(field.value, list) and field.content == ChronyFieldContent.FLAGS:
            print(" ".join(field.value), end="")
        else:
            print(f"{field.value}", end="")
        
        # Print unit if applicable
        if field.unit:
            print(f" {field.unit}")
        else:
            print()


def print_all_reports_pythonic(chrony):
    """Print all reports using the Pythonic interface.
    
    Args:
        chrony: Chrony interface
    """
    # Get all available reports
    for report_name in chrony.get_available_reports():
        print(f"{report_name}:")
        
        try:
            # Get record count
            record_count = chrony.get_record_count(report_name)
            
            if record_count == 1:
                # Single record report
                record = chrony.get_record(report_name)
                print_record_pythonic(record, indent=2)
            else:
                # Multi-record report
                report = chrony.get_report(report_name)
                for i, record in enumerate(report):
                    print(f"  Record #{i + 1}:")
                    print_record_pythonic(record, indent=4)
        
        except libchrony.ChronyException as e:
            print(f"  Error: {e}")
        
        print()


def direct_api_example(address: Optional[str] = None) -> int:
    """Example using the direct client API.
    
    Args:
        address: Address of chronyd
        
    Returns:
        int: Exit code (0 on success)
    """
    print("\n=== DIRECT API EXAMPLE ===\n")
    
    # Open the socket
    sock = chrony_socket.chrony_open_socket(address)
    if sock is None:
        print(f"Could not open socket to {address or 'default locations'}", file=sys.stderr)
        return 1
    
    # Initialize the session - adjusted to work with socket objects instead of file descriptors
    result, session = client.chrony_init_session(sock.fileno())
    if result != ChronyError.OK:
        chrony_socket.chrony_close_socket(sock)
        return 1
    
    # Print all reports
    print_all_reports_direct_api(session)
    
    # Clean up
    client.chrony_deinit_session(session)
    chrony_socket.chrony_close_socket(sock)
    
    return 0


def pythonic_example(address: Optional[str] = None) -> int:
    """Example using the Pythonic interface.
    
    Args:
        address: Address of chronyd
        
    Returns:
        int: Exit code (0 on success)
    """
    print("\n=== PYTHONIC INTERFACE EXAMPLE ===\n")
    
    try:
        # Using the context manager (recommended)
        with libchrony.connect(address) as chrony:
            print("Connected to chronyd\n")
            
            # Print tracking information (current synchronization state)
            print("Tracking information:")
            tracking = chrony.get_tracking()
            ref_id = tracking["reference ID"].value
            ref_id_str = f"{ref_id:08X}" if isinstance(ref_id, int) else ref_id
            
            print(f"  Reference ID: {ref_id_str}")
            print(f"  Stratum: {tracking['stratum'].value}")
            print(f"  Current correction: {tracking['current correction'].value} seconds")
            print(f"  Root delay: {tracking['root delay'].value} seconds")
            print(f"  Root dispersion: {tracking['root dispersion'].value} seconds")
            print()
            
            # Print sources information (time sources)
            print("Time sources:")
            sources = chrony.get_sources()
            for i, source in enumerate(sources):
                print(f"  Source #{i + 1}:")
                address_field = None
                for field in source.fields:
                    if "address" in field.name:
                        address_field = field
                        break

                if address_field:
                    address = address_field.value
                    print(f"    Address: {address}")
                else:
                    print("    Address: Unknown")
                print(f"    Stratum: {source['stratum'].value}")
                print(f"    State: {source['state'].value}")
                print(f"    Last sample offset: {source['adjusted last sample offset'].value} seconds")
                print()
            
            # Access a field by name
            try:
                activity = chrony.get_activity()
                online = activity["online sources"].value
                offline = activity["offline sources"].value
                print(f"Source statistics: {online} online, {offline} offline\n")
            except (KeyError, libchrony.ChronyException) as e:
                print(f"Could not get activity report: {e}\n")
            
            # Print all reports
            print("All available reports:")
            print_all_reports_pythonic(chrony)
    
    except libchrony.ConnectionError as e:
        print(f"Error connecting to chronyd: {e}", file=sys.stderr)
        return 1
    except libchrony.ChronyException as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def main() -> int:
    """Main function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Example program for the Python port of libchrony")
    parser.add_argument("address", nargs="?", help="Address of chronyd (Unix socket path or IP:port)")
    parser.add_argument("--direct-only", action="store_true", help="Only use the direct client API")
    parser.add_argument("--pythonic-only", action="store_true", help="Only use the Pythonic interface")
    args = parser.parse_args()
    
    # Run the examples
    exit_code = 0
    
    if not args.pythonic_only:
        exit_code = direct_api_example(args.address)
    
    if exit_code == 0 and not args.direct_only:
        exit_code = pythonic_example(args.address)
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
