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

LibChrony socket handling functions

"""

import os
import socket
import ipaddress
import errno
import re
from typing import Optional, Tuple, Union, List
from pathlib import Path

from chrony_formats import MAX_UNIX_SOCKET_INDEX

def remove_unix_socket(sock: socket.socket) -> None:
    """Remove a Unix domain socket file if it exists.
    
    Args:
        sock: The socket to check and potentially remove
    """
    try:
        # Get the socket name
        sock_name = sock.getsockname()
        
        # Check if it's a Unix domain socket
        if isinstance(sock_name, str):
            # It's a Unix domain socket, so unlink the file
            if os.path.exists(sock_name):
                os.unlink(sock_name)
    except (OSError, socket.error):
        # Ignore errors during cleanup
        pass

def open_unix_socket(path: str) -> Optional[socket.socket]:
    """Open a Unix domain socket at the specified path.
    
    Args:
        path: Path to the socket file
        
    Returns:
        socket.socket or None: The connected socket or None if it fails
        
    Raises:
        ValueError: If the path is invalid
        socket.error: If there's a problem with socket operations
        OSError: If there's a filesystem error
    """
    # Validate path
    if not path or len(path) > 255:
        raise ValueError(errno.EINVAL, "Invalid socket path")
    
    # Get the directory from the path
    directory = os.path.dirname(path)
    if not directory:
        raise ValueError(errno.EINVAL, "Invalid socket directory")
    
    # Create a new Unix domain datagram socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    
    # Try to bind the socket to a temporary path in the same directory
    for i in range(1, MAX_UNIX_SOCKET_INDEX + 1):
        temp_path = f"{directory}/libchrony.{i}"
        
        try:
            sock.bind(temp_path)
            break
        except OSError as e:
            if e.errno != errno.EADDRINUSE:
                sock.close()
                return None
            
            # Try to clean up if the socket exists but is no longer in use
            try:
                test_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                test_sock.connect(temp_path)
                test_sock.close()
            except OSError as connect_err:
                if connect_err.errno == errno.ECONNREFUSED:
                    # Socket exists but is no longer in use, remove it and retry
                    try:
                        os.unlink(temp_path)
                        # Don't increment i so we retry this index
                        i -= 1
                    except OSError:
                        pass
                test_sock.close()
    else:
        # We've exhausted all possible indices
        sock.close()
        return None
    
    # Allow chronyd running under a different user to send responses to our socket
    try:
        os.chmod(temp_path, 0o666)
    except OSError:
        pass
    
    # Connect to the target socket
    try:
        sock.connect(path)
    except OSError:
        remove_unix_socket(sock)
        sock.close()
        return None
    
    return sock

def open_inet_socket(address: str) -> Optional[socket.socket]:
    """Open an Internet domain socket to the specified address.
    
    Args:
        address: IP address with optional port (default 323)
        
    Returns:
        socket.socket or None: The connected socket or None if it fails
        
    Raises:
        ValueError: If the address is invalid
        socket.error: If there's a problem with socket operations
    """
    if not address:
        return None
    
    # Default port for chrony
    port = 323
    addr = address
    
    # Parse IPv6 address with port [2001:db8::1]:323
    ipv6_match = re.match(r'^\[([0-9a-fA-F:]+)\]:(\d+)$', address)
    if ipv6_match:
        addr = ipv6_match.group(1)
        port = int(ipv6_match.group(2))
    # Parse IPv4 address with port 192.0.2.1:323
    elif ':' in address and address.count(':') == 1:
        addr, port_str = address.split(':')
        if port_str:
            port = int(port_str)
    
    # Try to parse as IPv4 or IPv6 address
    try:
        # Try IPv4
        ipv4 = ipaddress.IPv4Address(addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((str(ipv4), port))
        return sock
    except ipaddress.AddressValueError:
        try:
            # Try IPv6
            ipv6 = ipaddress.IPv6Address(addr)
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            sock.connect((str(ipv6), port))
            return sock
        except ipaddress.AddressValueError:
            # Not a valid IP address
            return None
    except OSError:
        # Failed to connect
        return None

def chrony_open_socket(address: Optional[str] = None) -> Optional[socket.socket]:
    """Open a socket connection to chronyd.
    
    Args:
        address: Address of the server socket. If it starts with '/',
                 it is interpreted as a Unix domain socket path.
                 Otherwise it's an IPv4 or IPv6 address, optionally
                 with port.
                 
    Returns:
        socket.socket or None: Connected socket or None if all connection attempts fail
        
    Note:
        This is a Python adaptation of the C function which returns a socket object
        instead of a file descriptor integer for better integration with Python.
    """
    if not address:
        # Try default connections in order
        # 1. Unix socket
        sock = open_unix_socket("/var/run/chrony/chronyd.sock")
        if sock:
            return sock
        
        # 2. IPv4 localhost
        sock = open_inet_socket("127.0.0.1")
        if sock:
            return sock
        
        # 3. IPv6 localhost
        sock = open_inet_socket("::1")
        return sock
    
    # User-specified address
    if address.startswith('/'):
        return open_unix_socket(address)
    else:
        return open_inet_socket(address)

def chrony_close_socket(sock: socket.socket) -> None:
    """Close a chrony socket connection.
    
    Args:
        sock: The socket to close
        
    Note:
        Takes a socket object rather than a file descriptor as in the C version.
    """
    if sock:
        remove_unix_socket(sock)
        sock.close()

