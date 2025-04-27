#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright ©2025 Rob Gill

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
Tests three different connection methods:
1. Unix socket
2. IPv4 address (127.0.0.1)
3. IPv6 address (::1)

"""

import sys
import argparse
import socket
import select
import time
from typing import List, Optional, Dict, Any, Union

import libchrony
from chrony_formats import ChronyError, ChronyFieldContent, ChronyFieldType

# Connection methods to test
CONNECTION_METHODS = [
    {
        "name": "Unix Socket",
        "address": "/var/run/chrony/chronyd.sock",
        "fallback": None  # Will try default socket paths
    },
    {
        "name": "IPv4",
        "address": "127.0.0.1:323",
        "fallback": "127.0.0.1"  # Try without explicit port
    },
    {
        "name": "IPv6",
        "address": "[::1]:323",
        "fallback": "::1"  # Try without explicit port
    }
]


def print_tracking_info(chrony, indent=''):
    """Print tracking information from chronyd.
    
    Args:
        chrony: Connected Chrony interface
        indent: String to prepend to each line for indentation
    """
    print(f"{indent}Tracking Information:")
    
    try:
        tracking = chrony.get_tracking()
        
        # Get reference ID (format depends on stratum)
        ref_id = tracking["reference ID"].value
        ref_id_str = f"{ref_id:08X}" if isinstance(ref_id, int) else ref_id
        
        # Print key tracking details
        print(f"{indent}  Reference ID: {ref_id_str}")
        print(f"{indent}  Stratum: {tracking['stratum'].value}")
        
        # Look for address field which may not exist for all reference types
        try:
            address = tracking["address"].value
            if address:
                print(f"{indent}  Address: {address}")
        except KeyError:
            pass
        
        # Print synchronization information
        print(f"{indent}  Leap status: {tracking['leap status'].value}")
        print(f"{indent}  Current correction: {tracking['current correction'].value:.9f} seconds")
        print(f"{indent}  Frequency offset: {tracking['frequency offset'].value:.3f} ppm")
        print(f"{indent}  Root delay: {tracking['root delay'].value:.6f} seconds")
        print(f"{indent}  Root dispersion: {tracking['root dispersion'].value:.6f} seconds")
    
    except (KeyError, libchrony.ChronyException) as e:
        print(f"{indent}  Error getting tracking data: {e}")


def print_source_summary(chrony, indent=''):
    """Print a summary of the time sources.
    
    Args:
        chrony: Connected Chrony interface
        indent: String to prepend to each line for indentation
    """
    print(f"{indent}Source Summary:")
    
    try:
        sources = chrony.get_sources()
        
        if not sources or len(sources) == 0:
            print(f"{indent}  No sources available")
            return
        
        selected_count = 0
        ref_clock_count = 0
        
        # Count source types
        for source in sources:
            try:
                # Count by state
                if source["state"].value == "selected":
                    selected_count += 1
                
                # Count by mode
                if source["mode"].value == "reference clock":
                    ref_clock_count += 1
            except KeyError:
                continue
        
        # Print summary
        print(f"{indent}  Total sources: {len(sources)}")
        print(f"{indent}  Selected sources: {selected_count}")
        print(f"{indent}  Reference clocks: {ref_clock_count}")
        print(f"{indent}  Network sources: {len(sources) - ref_clock_count}")
        
        # Print the selected source(s)
        print(f"{indent}  Selected Sources:")
        for i, source in enumerate(sources):
            try:
                if source["state"].value == "selected":
                    addr_field = None
                    for field in source.fields:
                        if "address" in field.name:
                            addr_field = field
                            break
                    
                    if addr_field:
                        addr = addr_field.value
                        print(f"{indent}    {addr} (stratum {source['stratum'].value})")
            except KeyError:
                continue
    
    except libchrony.ChronyException as e:
        print(f"{indent}  Error getting sources: {e}")


def print_activity_info(chrony, indent=''):
    """Print activity information.
    
    Args:
        chrony: Connected Chrony interface
        indent: String to prepend to each line for indentation
    """
    print(f"{indent}Activity Information:")
    
    try:
        activity = chrony.get_activity()
        
        print(f"{indent}  Online sources: {activity['online sources'].value}")
        print(f"{indent}  Offline sources: {activity['offline sources'].value}")
        print(f"{indent}  Burst online sources: {activity['burst online-return sources'].value}")
        print(f"{indent}  Burst offline sources: {activity['burst offline-return sources'].value}")
        
        # Calculate total
        total = (activity['online sources'].value + 
                activity['offline sources'].value + 
                activity['burst online-return sources'].value + 
                activity['burst offline-return sources'].value)
        
        print(f"{indent}  Total tracked sources: {total}")
    
    except (KeyError, libchrony.ChronyException) as e:
        print(f"{indent}  Error getting activity data: {e}")


def test_connection(address=None, fallback=None, method_name="Default"):
    """Test a specific connection method.
    
    Args:
        address: Address to connect to
        fallback: Fallback address if the first one fails
        method_name: Name of the connection method (for display)
    
    Returns:
        bool: True if connection succeeded, False otherwise
    """
    print(f"\n=== Testing {method_name} Connection ===\n")
    print(f"Attempting to connect to: {address or 'default'}")
    
    try:
        # Try the primary address
        with libchrony.connect(address) as chrony:
            print(f"Connection successful!\n")
            
            # Print key information
            print_tracking_info(chrony)
            print()
            print_source_summary(chrony)
            print()
            print_activity_info(chrony)
            
            return True
    
    except libchrony.ConnectionError as e:
        print(f"Failed to connect to {address}: {e}")
        print("Please check that you have sufficient priveleges.")
        
        # Try fallback if provided
        if fallback and fallback != address:
            print(f"Trying fallback: {fallback}")
            try:
                with libchrony.connect(fallback) as chrony:
                    print(f"Fallback connection successful!\n")
                    
                    # Print key information
                    print_tracking_info(chrony, indent='  ')
                    print()
                    print_source_summary(chrony, indent='  ')
                    print()
                    print_activity_info(chrony, indent='  ')
                    
                    return True
            
            except libchrony.ConnectionError as e2:
                print(f"Failed to connect to fallback {fallback}: {e2}")
    
    except libchrony.ChronyException as e:
        print(f"Error while connected: {e}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False


def main():
    """Main function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Test different connection methods to chronyd"
    )
    parser.add_argument(
        "--unix-only", action="store_true", 
        help="Only test Unix socket connection"
    )
    parser.add_argument(
        "--ipv4-only", action="store_true", 
        help="Only test IPv4 connection"
    )
    parser.add_argument(
        "--ipv6-only", action="store_true", 
        help="Only test IPv6 connection"
    )
    parser.add_argument(
        "--socket-path", type=str, 
        help="Custom Unix socket path"
    )
    parser.add_argument(
        "--ipv4-addr", type=str, 
        help="Custom IPv4 address[:port]"
    )
    parser.add_argument(
        "--ipv6-addr", type=str, 
        help="Custom IPv6 address (format: [addr]:port or addr)"
    )
    
    args = parser.parse_args()
    
    # Apply custom addresses if provided
    if args.socket_path:
        CONNECTION_METHODS[0]["address"] = args.socket_path
    
    if args.ipv4_addr:
        CONNECTION_METHODS[1]["address"] = args.ipv4_addr
        CONNECTION_METHODS[1]["fallback"] = args.ipv4_addr.split(':')[0]
    
    if args.ipv6_addr:
        CONNECTION_METHODS[2]["address"] = args.ipv6_addr
        # Handle both formats: [::1]:123 and ::1
        if args.ipv6_addr.startswith('['):
            CONNECTION_METHODS[2]["fallback"] = args.ipv6_addr.split(']')[0][1:]
        else:
            CONNECTION_METHODS[2]["fallback"] = args.ipv6_addr
    
    # Track which methods succeeded
    successful_methods = []
    total_methods = 0
    
    # Test each connection method based on args
    for method in CONNECTION_METHODS:
        # Skip methods that aren't requested
        if ((args.unix_only and method["name"] != "Unix Socket") or
                (args.ipv4_only and method["name"] != "IPv4") or
                (args.ipv6_only and method["name"] != "IPv6")):
            continue
        
        total_methods += 1
        success = test_connection(
            address=method["address"],
            fallback=method["fallback"],
            method_name=method["name"]
        )
        
        if success:
            successful_methods.append(method["name"])
    
    # Print summary
    print("\n=== Connection Test Summary ===")
    print(f"Total methods tested: {total_methods}")
    print(f"Successful methods: {len(successful_methods)}")
    
    if successful_methods:
        print("Working connections:")
        for method in successful_methods:
            print(f"  - {method}")
    else:
        print("No successful connections. Check if chronyd is running.")
    
    # Return success if at least one method worked
    return 0 if successful_methods else 1


if __name__ == "__main__":
    sys.exit(main())
