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

LibChrony client implementation - core functionality for connecting to
and interacting with chronyd

"""

import os
import socket
import struct
import random
from typing import List, Optional, Tuple, Union, Dict, Any, cast

from chrony_formats import (
    ChronyError, FieldType, ChronyFieldType, ChronyFieldContent,
    Field, Message, Request, Response, Report, Constant, TimeSpec,
    SessionState, REPORTS, SOURCES_REPORT_FIELDS,
    REQUEST_HEADER_LEN, RESPONSE_HEADER_LEN, MAX_RESPONSES
)

import message
import chrony_socket


class ChronySession:
    """Class representing a session with chronyd."""
    
    def __init__(self, sock: socket.socket):
        """Initialize a new chronyd session.
        
        Args:
            sock: Socket connected to chronyd
        """
        self.state = SessionState.IDLE
        self.sock = sock
        self.num_expected_responses = 0
        self.count_requested = False
        self.requested_record = 0
        self.expected_responses: List[Response] = []
        self.request_msg = Message()
        self.response_msg = Message()
        self.num_records = 0
        self.follow_report: Optional[str] = None
        
        # Open /dev/urandom for secure sequence numbers
        try:
            self.urandom = open("/dev/urandom", "rb")
        except OSError:
            raise OSError("Failed to open /dev/urandom")
    
    def __del__(self):
        """Clean up resources when the session is destroyed."""
        if hasattr(self, 'urandom') and self.urandom:
            self.urandom.close()
    
    def get_fd(self) -> int:
        """Get the socket file descriptor.
        
        Returns:
            int: Socket file descriptor
        """
        return self.sock.fileno()
    
    def needs_response(self) -> bool:
        """Check if the session is waiting for a server response.
        
        Returns:
            bool: True if waiting for a response, False otherwise
        """
        return self.state == SessionState.REQUEST_SENT
    

    def process_response(self) -> ChronyError:
        """Process a server response.
        
        Returns:
            ChronyError: Error code (CHRONY_OK on success)
        """
        if self.state != SessionState.REQUEST_SENT:
            return ChronyError.UNEXPECTED_CALL
        
        # Clear the response message
        self.response_msg = Message()
        
        # Receive the response with a timeout to prevent hanging
        try:
            # Set socket to non-blocking mode temporarily
            self.sock.setblocking(False)
            try:
                data = self.sock.recv(len(self.response_msg.msg))
                if not data:
                    self.sock.setblocking(True)
                    return ChronyError.RECV_FAILED
            
                # Copy received data to the response message
                self.response_msg.msg[:len(data)] = data
                self.response_msg.length = len(data)
            except BlockingIOError:
                # No data available
                self.sock.setblocking(True)
                return ChronyError.RECV_FAILED
            except (socket.error, OSError):
                self.sock.setblocking(True)
                return ChronyError.RECV_FAILED
            finally:
                # Restore blocking mode
                self.sock.setblocking(True)
        except Exception:
            return ChronyError.RECV_FAILED
    
        self.state = SessionState.RESPONSE_RECEIVED
    
        # Check if the response is valid for our request
        if not message.is_response_valid(self.request_msg, self.response_msg):
            # Ignore the response and wait for another
            self.state = SessionState.REQUEST_SENT
            return ChronyError.OK
    
        # Process the response
        r = message.process_response(self.response_msg, self.expected_responses)
        if r != ChronyError.OK:
            return r
    
        self.state = SessionState.RESPONSE_ACCEPTED
    
        # If this was a count request, store the number of records
        if self.count_requested:
            assert self.response_msg.fields[0].type == FieldType.UINT32
            self.num_records = message.get_field_uinteger(self.response_msg, 0)
    
        # If we need to follow up with another request
        if self.follow_report:
            return self.request_record(self.follow_report, self.requested_record)
    
        return ChronyError.OK

#    def process_response(self) -> ChronyError:
#        """Process a server response.
#        
#        Returns:
#            ChronyError: Error code (CHRONY_OK on success)
#        """
#        if self.state != SessionState.REQUEST_SENT:
#            return ChronyError.UNEXPECTED_CALL
#        
#        # Clear the response message
#        self.response_msg = Message()
#        
#        # Receive the response
#        try:
#            data = self.sock.recv(len(self.response_msg.msg))
#            if not data:
#                return ChronyError.RECV_FAILED
#            
#            # Copy received data to the response message
#            self.response_msg.msg[:len(data)] = data
#            self.response_msg.length = len(data)
#        except (socket.error, OSError):
#            return ChronyError.RECV_FAILED
#        
#        self.state = SessionState.RESPONSE_RECEIVED
#        
#        # Check if the response is valid for our request
#        if not message.is_response_valid(self.request_msg, self.response_msg):
#            # Ignore the response and wait for another
#            self.state = SessionState.REQUEST_SENT
#            return ChronyError.OK
#        
#        # Process the response
#        r = message.process_response(self.response_msg, self.expected_responses)
#        if r != ChronyError.OK:
#            return r
#        
#        self.state = SessionState.RESPONSE_ACCEPTED
#        
#        # If this was a count request, store the number of records
#        if self.count_requested:
#            assert self.response_msg.fields[0].type == FieldType.UINT32
#            self.num_records = message.get_field_uinteger(self.response_msg, 0)
#        
#        # If we need to follow up with another request
#        if self.follow_report:
#            return self.request_record(self.follow_report, self.requested_record)
#        
#        return ChronyError.OK
    
    def _send_request(self, request: Request, values: List[Any], 
                     expected_responses: List[Response]) -> ChronyError:
        """Send a request to the server.
        
        Args:
            request: Request definition
            values: Values for the request fields
            expected_responses: Expected response types
            
        Returns:
            ChronyError: Error code (CHRONY_OK on success)
        """
        # Generate a random sequence number
        try:
            sequence_bytes = self.urandom.read(4)
            sequence = int.from_bytes(sequence_bytes, byteorder='big')
        except (OSError, IOError):
            self.state = SessionState.IDLE
            return ChronyError.RANDOM_FAILED
        
        # Format the request
        message.format_request(
            self.request_msg, sequence, request, values, expected_responses
        )
        
        # Send the request
        try:
            sent = self.sock.send(self.request_msg.msg[:self.request_msg.length])
            if sent != self.request_msg.length:
                self.state = SessionState.IDLE
                return ChronyError.SEND_FAILED
        except (socket.error, OSError):
            self.state = SessionState.IDLE
            return ChronyError.SEND_FAILED
        
        self.state = SessionState.REQUEST_SENT
        return ChronyError.OK
    
    def request_report_number_records(self, report_name: str) -> ChronyError:
        """Send a request to get the number of records for a report.
        
        Args:
            report_name: Name of the report
            
        Returns:
            ChronyError: Error code (CHRONY_OK on success)
        """
        report_index = message.get_report_index(report_name)
        if report_index < 0:
            return ChronyError.UNKNOWN_REPORT
        
        report = message.get_report(report_index)
        if not report:
            return ChronyError.UNKNOWN_REPORT
        
        # If the report doesn't have count requests, it always has one record
        if not report.count_requests or report.count_requests[0].code == 0:
            self.num_records = 1
            return ChronyError.OK
        
        # Send the count request
        r = self._send_request(report.count_requests[0], [], report.count_responses)
        if r != ChronyError.OK:
            return r
        
        self.num_expected_responses = 1
        self.expected_responses = report.count_responses
        self.count_requested = True
        self.num_records = 0
        
        return ChronyError.OK
    
    def get_report_number_records(self) -> int:
        """Get the number of records available for the requested report.
        
        Returns:
            int: Number of records
        """
        return self.num_records
    
    def request_record(self, report_name: str, record: int) -> ChronyError:
        """Send a request to get a record of a report.
        
        Args:
            report_name: Name of the report
            record: Index of the record (starting at 0)
            
        Returns:
            ChronyError: Error code (CHRONY_OK on success)
        """
        self.follow_report = None
        
        report_index = message.get_report_index(report_name)
        if report_index < 0:
            return ChronyError.UNKNOWN_REPORT
        
        report = message.get_report(report_index)
        if not report:
            return ChronyError.UNKNOWN_REPORT
        
        if not report.record_requests:
            if record != 0:
                return ChronyError.INVALID_ARGUMENT
            # Empty request with no arguments
            args: List[Any] = []
        else:
            fields = report.record_requests[0].fields
            
            if fields:
                if fields[0].type == FieldType.ADDRESS:
                    # Get the address from sourcestats report
                    if (self.state != SessionState.RESPONSE_ACCEPTED or
                            not message.is_report_fields("sourcestats", self.response_msg.fields) or
                            self.requested_record != record):
                        self.follow_report = report_name
                        report_name = "sourcestats"
                        return self.request_record(report_name, record)
                    
                    # Get the address from the current response
                    addr_pos = message.get_field_position(self.response_msg, 1)
                    
                    # Check if address is valid (not a reference clock)
                    if not message.get_field_string(self.response_msg, 1):
                        self.response_msg.num_fields = 0
                        return ChronyError.OK
                    
                    # Extract the 20 bytes of address data
                    addr_data = bytearray(20)
                    for i in range(20):
                        addr_data[i] = self.response_msg.msg[addr_pos + i]
                    
                    args = [addr_data]
                elif fields[0].type == FieldType.UINT32:
                    args = [record]
                else:
                    raise ValueError(f"Unexpected field type: {fields[0].type}")
                
                # Check if there's a second field
                if len(fields) > 1:
                    if fields[1].type != FieldType.NONE:
                        raise ValueError(f"Unexpected field type for second field: {fields[1].type}")
                else:
                    # Only one field in the list, which is fine
                    pass
                
                # args list is populated above based on field type
            else:
                if record != 0:
                    return ChronyError.INVALID_ARGUMENT
                args = []
        
        # Send the record request
        r = self._send_request(report.record_requests[0], args, report.record_responses)
        if r != ChronyError.OK:
            return r
        
        self.num_expected_responses = 1
        self.expected_responses = report.record_responses
        self.count_requested = False
        self.requested_record = record
        
        return ChronyError.OK
    
    def get_record_number_fields(self) -> int:
        """Get the number of fields in the requested record.
        
        Returns:
            int: Number of fields
        """
        return self.response_msg.num_fields
    
    def get_field_name(self, field: int) -> Optional[str]:
        """Get the name of a field.
        
        Args:
            field: Index of the field
            
        Returns:
            str or None: Name of the field, or None if invalid
        """
        return message.resolve_field_name(self.response_msg, field)
    
    def get_field_index(self, name: str) -> int:
        """Get the index of a field given by its name.
        
        Args:
            name: Name of the field
            
        Returns:
            int: Index of the field, or -1 if not found
        """
        for i in range(self.get_record_number_fields()):
            if name == self.get_field_name(i):
                return i
        return -1
    
    def get_field_type(self, field: int) -> ChronyFieldType:
        """Get the type of a field.
        
        Args:
            field: Index of the field
            
        Returns:
            ChronyFieldType: Type of the field
        """
        field_type = message.resolve_field_type(self.response_msg, field)
        
        if field_type in (FieldType.UINT64, FieldType.UINT32, FieldType.UINT16, FieldType.UINT8):
            return ChronyFieldType.UINTEGER
        elif field_type in (FieldType.INT16, FieldType.INT8):
            return ChronyFieldType.INTEGER
        elif field_type == FieldType.FLOAT:
            return ChronyFieldType.FLOAT
        elif field_type == FieldType.ADDRESS:
            return ChronyFieldType.STRING
        elif field_type == FieldType.TIMESPEC:
            return ChronyFieldType.TIMESPEC
        else:
            return ChronyFieldType.NONE
    
    def get_field_content(self, field: int) -> ChronyFieldContent:
        """Get the content type of a field.
        
        Args:
            field: Index of the field
            
        Returns:
            ChronyFieldContent: Content type of the field
        """
        return message.resolve_field_content(self.response_msg, field)
    
    def get_field_uinteger(self, field: int) -> int:
        """Get the value of an unsigned integer field.
        
        Args:
            field: Index of the field
            
        Returns:
            int: Value of the field
        """
        return message.get_field_uinteger(self.response_msg, field)
    
    def get_field_integer(self, field: int) -> int:
        """Get the value of a signed integer field.
        
        Args:
            field: Index of the field
            
        Returns:
            int: Value of the field
        """
        return message.get_field_integer(self.response_msg, field)
    
    def get_field_float(self, field: int) -> float:
        """Get the value of a floating-point field.
        
        Args:
            field: Index of the field
            
        Returns:
            float: Value of the field
        """
        return message.get_field_float(self.response_msg, field)
    
    def get_field_timespec(self, field: int) -> TimeSpec:
        """Get the value of a timespec field.
        
        Args:
            field: Index of the field
            
        Returns:
            TimeSpec: Value of the field
        """
        return message.get_field_timespec(self.response_msg, field)
    
    def get_field_string(self, field: int) -> Optional[str]:
        """Get the value of a string field.
        
        Args:
            field: Index of the field
            
        Returns:
            str or None: Value of the field, or None if invalid
        """
        return message.get_field_string(self.response_msg, field)
    
    def get_field_constant_name(self, field: int, value: int) -> Optional[str]:
        """Get the name of a constant value for a field.
        
        Args:
            field: Index of the field
            value: Value to look up
            
        Returns:
            str or None: Name of the constant, or None if not found
        """
        return message.get_field_constant_name(self.response_msg, field, value)

    
#def request_record(self, report_name: str, record: int) -> ChronyError:
#    """Send a request to get a record of a report.
#    
#    Args:
#        report_name: Name of the report
#        record: Index of the record (starting at 0)
#        
#    Returns:
#        ChronyError: Error code (CHRONY_OK on success)
#    """
#    self.follow_report = None
#    
#    report_index = message.get_report_index(report_name)
#    if report_index < 0:
#        return ChronyError.UNKNOWN_REPORT
#    
#    report = message.get_report(report_index)
#    if not report:
#        return ChronyError.UNKNOWN_REPORT
#    
#    if not report.record_requests:
#        if record != 0:
#            return ChronyError.INVALID_ARGUMENT
#        # Empty request with no arguments
#        args: List[Any] = []
#    else:
#        fields = report.record_requests[0].fields
#        
#        if fields:
#            if fields[0].type == FieldType.ADDRESS:
#                # Get the address from sourcestats report
#                if (self.state != SessionState.RESPONSE_ACCEPTED or
#                        not message.is_report_fields("sourcestats", self.response_msg.fields) or
#                        self.requested_record != record):
#                    self.follow_report = report_name
#                    report_name = "sourcestats"
#                    return self.request_record(report_name, record)
#                
#                # Get the address from the current response
#                addr_pos = message.get_field_position(self.response_msg, 1)
#                
#                # Check if address is valid (not a reference clock)
#                if not message.get_field_string(self.response_msg, 1):
#                    self.response_msg.num_fields = 0
#                    return ChronyError.OK
#                
#                # Extract the 20 bytes of address data
#                addr_data = bytearray(20)
#                for i in range(20):
#                    addr_data[i] = self.response_msg.msg[addr_pos + i]
#                
#                args = [addr_data]
#            elif fields[0].type == FieldType.UINT32:
#                args = [record]
#            else:
#                raise ValueError(f"Unexpected field type: {fields[0].type}")
#            
#            # Check if there's a second field - the error occurs here when fields has only one element
#            # Replace the assertion with a proper check
#            if len(fields) > 1:
#                if fields[1].type != FieldType.NONE:
#                    raise ValueError(f"Unexpected field type for second field: {fields[1].type}")
#            else:
#                # Only one field in the list, which is fine
#                pass
#            
#            # args list is populated above based on field type
#        else:
#            if record != 0:
#                return ChronyError.INVALID_ARGUMENT
#            args = []
#    
#    # Send the record request
#    r = self._send_request(report.record_requests[0], args, report.record_responses)
#    if r != ChronyError.OK:
#        return r
#    
#    self.num_expected_responses = 1
#    self.expected_responses = report.record_responses
#    self.count_requested = False
#    self.requested_record = record
#    
#    return ChronyError.OK
    
    def get_record_number_fields(self) -> int:
        """Get the number of fields in the requested record.
        
        Returns:
            int: Number of fields
        """
        return self.response_msg.num_fields
    
    def get_field_name(self, field: int) -> Optional[str]:
        """Get the name of a field.
        
        Args:
            field: Index of the field
            
        Returns:
            str or None: Name of the field, or None if invalid
        """
        return message.resolve_field_name(self.response_msg, field)
    
    def get_field_index(self, name: str) -> int:
        """Get the index of a field given by its name.
        
        Args:
            name: Name of the field
            
        Returns:
            int: Index of the field, or -1 if not found
        """
        for i in range(self.get_record_number_fields()):
            if name == self.get_field_name(i):
                return i
        return -1
    
    def get_field_type(self, field: int) -> ChronyFieldType:
        """Get the type of a field.
        
        Args:
            field: Index of the field
            
        Returns:
            ChronyFieldType: Type of the field
        """
        field_type = message.resolve_field_type(self.response_msg, field)
        
        if field_type in (FieldType.UINT64, FieldType.UINT32, FieldType.UINT16, FieldType.UINT8):
            return ChronyFieldType.UINTEGER
        elif field_type in (FieldType.INT16, FieldType.INT8):
            return ChronyFieldType.INTEGER
        elif field_type == FieldType.FLOAT:
            return ChronyFieldType.FLOAT
        elif field_type == FieldType.ADDRESS:
            return ChronyFieldType.STRING
        elif field_type == FieldType.TIMESPEC:
            return ChronyFieldType.TIMESPEC
        else:
            return ChronyFieldType.NONE
    
    def get_field_content(self, field: int) -> ChronyFieldContent:
        """Get the content type of a field.
        
        Args:
            field: Index of the field
            
        Returns:
            ChronyFieldContent: Content type of the field
        """
        return message.resolve_field_content(self.response_msg, field)
    
    def get_field_uinteger(self, field: int) -> int:
        """Get the value of an unsigned integer field.
        
        Args:
            field: Index of the field
            
        Returns:
            int: Value of the field
        """
        return message.get_field_uinteger(self.response_msg, field)
    
    def get_field_integer(self, field: int) -> int:
        """Get the value of a signed integer field.
        
        Args:
            field: Index of the field
            
        Returns:
            int: Value of the field
        """
        return message.get_field_integer(self.response_msg, field)
    
    def get_field_float(self, field: int) -> float:
        """Get the value of a floating-point field.
        
        Args:
            field: Index of the field
            
        Returns:
            float: Value of the field
        """
        return message.get_field_float(self.response_msg, field)
    
    def get_field_timespec(self, field: int) -> TimeSpec:
        """Get the value of a timespec field.
        
        Args:
            field: Index of the field
            
        Returns:
            TimeSpec: Value of the field
        """
        return message.get_field_timespec(self.response_msg, field)
    
    def get_field_string(self, field: int) -> Optional[str]:
        """Get the value of a string field.
        
        Args:
            field: Index of the field
            
        Returns:
            str or None: Value of the field, or None if invalid
        """
        return message.get_field_string(self.response_msg, field)
    
    def get_field_constant_name(self, field: int, value: int) -> Optional[str]:
        """Get the name of a constant value for a field.
        
        Args:
            field: Index of the field
            value: Value to look up
            
        Returns:
            str or None: Name of the constant, or None if not found
        """
        return message.get_field_constant_name(self.response_msg, field, value)


# Module-level functions that correspond to the C API

def chrony_get_error_string(error: ChronyError) -> str:
    """Get a string describing a libchrony error code.
    
    Args:
        error: Error code
        
    Returns:
        str: Description of the error
    """
    error_strings = {
        ChronyError.OK: "Success",
        ChronyError.NO_MEMORY: "Failed to allocate memory",
        ChronyError.NO_RANDOM: "Failed to open /dev/urandom",
        ChronyError.UNKNOWN_REPORT: "Unknown report",
        ChronyError.RANDOM_FAILED: "Failed to read /dev/urandom",
        ChronyError.SEND_FAILED: "Failed to send request",
        ChronyError.RECV_FAILED: "Failed to receive response",
        ChronyError.INVALID_ARGUMENT: "Invalid argument",
        ChronyError.UNEXPECTED_CALL: "Unexpected function call",
        ChronyError.UNAUTHORIZED: "Not authorized",
        ChronyError.DISABLED: "Disabled",
        ChronyError.UNEXPECTED_STATUS: "Unexpected status",
        ChronyError.OLD_SERVER: "Unsupported server version (too old)",
        ChronyError.NEW_SERVER: "Unsupported server version (too new)",
        ChronyError.INVALID_RESPONSE: "Invalid response",
    }
    
    return error_strings.get(error, "Unknown error")

def chrony_init_session(sock_or_fd: Union[socket.socket, int]) -> Tuple[ChronyError, Optional[ChronySession]]:
    """Create a new client-server session.
    
    Args:
        sock_or_fd: Socket object or file descriptor
        
    Returns:
        Tuple[ChronyError, Optional[ChronySession]]: Error code and session object
    """
    try:
        # Handle both socket objects and file descriptors
        if isinstance(sock_or_fd, socket.socket):
            sock = sock_or_fd
        else:
            # Create a socket object from the file descriptor
            sock = socket.socket(fileno=sock_or_fd)
            
        session = ChronySession(sock)
        return ChronyError.OK, session
    except (OSError, socket.error) as e:
        if str(e).startswith("Failed to open /dev/urandom"):
            return ChronyError.NO_RANDOM, None
        return ChronyError.NO_MEMORY, None


def chrony_deinit_session(session: ChronySession) -> None:
    """Destroy the session.
    
    Args:
        session: Session to destroy
    """
    # Python's garbage collector will handle most cleanup
    if hasattr(session, 'urandom') and session.urandom:
        session.urandom.close()


def chrony_get_fd(session: ChronySession) -> int:
    """Get the socket used by the session.
    
    Args:
        session: Session
        
    Returns:
        int: Socket file descriptor
    """
    return session.get_fd()


def chrony_needs_response(session: ChronySession) -> bool:
    """Check if the session is waiting for a server response.
    
    Args:
        session: Session
        
    Returns:
        bool: True if waiting for a response, False otherwise
    """
    return session.needs_response()


def chrony_process_response(session: ChronySession) -> ChronyError:
    """Process a server response.
    
    Args:
        session: Session
        
    Returns:
        ChronyError: Error code (CHRONY_OK on success)
    """
    return session.process_response()


def chrony_request_report_number_records(session: ChronySession, report_name: str) -> ChronyError:
    """Send a request to get the number of records for a report.
    
    Args:
        session: Session
        report_name: Name of the report
        
    Returns:
        ChronyError: Error code (CHRONY_OK on success)
    """
    return session.request_report_number_records(report_name)


def chrony_get_report_number_records(session: ChronySession) -> int:
    """Get the number of records available for the requested report.
    
    Args:
        session: Session
        
    Returns:
        int: Number of records
    """
    return session.get_report_number_records()


def chrony_request_record(session: ChronySession, report_name: str, record: int) -> ChronyError:
    """Send a request to get a record of a report.
    
    Args:
        session: Session
        report_name: Name of the report
        record: Index of the record (starting at 0)
        
    Returns:
        ChronyError: Error code (CHRONY_OK on success)
    """
    return session.request_record(report_name, record)


def chrony_get_record_number_fields(session: ChronySession) -> int:
    """Get the number of fields in the requested record.
    
    Args:
        session: Session
        
    Returns:
        int: Number of fields
    """
    return session.get_record_number_fields()


def chrony_get_field_name(session: ChronySession, field: int) -> Optional[str]:
    """Get the name of a field.
    
    Args:
        session: Session
        field: Index of the field
        
    Returns:
        str or None: Name of the field, or None if invalid
    """
    return session.get_field_name(field)


def chrony_get_field_index(session: ChronySession, name: str) -> int:
    """Get the index of a field given by its name.
    
    Args:
        session: Session
        name: Name of the field
        
    Returns:
        int: Index of the field, or -1 if not found
    """
    return session.get_field_index(name)


def chrony_get_field_type(session: ChronySession, field: int) -> ChronyFieldType:
    """Get the type of a field.
    
    Args:
        session: Session
        field: Index of the field
        
    Returns:
        ChronyFieldType: Type of the field
    """
    return session.get_field_type(field)


def chrony_get_field_content(session: ChronySession, field: int) -> ChronyFieldContent:
    """Get the content type of a field.
    
    Args:
        session: Session
        field: Index of the field
        
    Returns:
        ChronyFieldContent: Content type of the field
    """
    return session.get_field_content(field)


def chrony_get_field_uinteger(session: ChronySession, field: int) -> int:
    """Get the value of an unsigned integer field.
    
    Args:
        session: Session
        field: Index of the field
        
    Returns:
        int: Value of the field
    """
    return session.get_field_uinteger(field)


def chrony_get_field_integer(session: ChronySession, field: int) -> int:
    """Get the value of a signed integer field.
    
    Args:
        session: Session
        field: Index of the field
        
    Returns:
        int: Value of the field
    """
    return session.get_field_integer(field)


def chrony_get_field_float(session: ChronySession, field: int) -> float:
    """Get the value of a floating-point field.
    
    Args:
        session: Session
        field: Index of the field
        
    Returns:
        float: Value of the field
    """
    return session.get_field_float(field)


def chrony_get_field_timespec(session: ChronySession, field: int) -> TimeSpec:
    """Get the value of a timespec field.
    
    Args:
        session: Session
        field: Index of the field
        
    Returns:
        TimeSpec: Value of the field
    """
    return session.get_field_timespec(field)


def chrony_get_field_string(session: ChronySession, field: int) -> Optional[str]:
    """Get the value of a string field.
    
    Args:
        session: Session
        field: Index of the field
        
    Returns:
        str or None: Value of the field, or None if invalid
    """
    return session.get_field_string(field)


def chrony_get_field_constant_name(session: ChronySession, field: int, value: int) -> Optional[str]:
    """Get the name of a constant value for a field.
    
    Args:
        session: Session
        field: Index of the field
        value: Value to look up
        
    Returns:
        str or None: Name of the constant, or None if not found
    """
    return session.get_field_constant_name(field, value)


def chrony_get_number_supported_reports() -> int:
    """Get the number of reports supported by the client.
    
    Returns:
        int: Number of supported reports
    """
    return message.chrony_get_number_supported_reports()


def chrony_get_report_name(report: int) -> Optional[str]:
    """Get the name of a report.
    
    Args:
        report: Index of the report
        
    Returns:
        str or None: Name of the report, or None if invalid
    """
    return message.chrony_get_report_name(report)
