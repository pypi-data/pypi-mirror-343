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

LibChrony message handling functions

"""

import socket
import struct
import math
import ipaddress
from typing import List, Optional, Tuple, Union, Dict, Any, cast

from chrony_formats import (
    ChronyError, FieldType, ChronyFieldType, ChronyFieldContent,
    Field, Message, Request, Response, Report, Constant, TimeSpec,
    REPORTS, SOURCES_REPORT_FIELDS,
    REQUEST_HEADER_LEN, RESPONSE_HEADER_LEN, MAX_RESPONSES
)


def get_response_len(response: Response) -> int:
    """Get the expected length of a response message.
    
    Args:
        response: The response definition
        
    Returns:
        int: The expected length of the response message, or 0 if no response
    """
    if response.code == 0:
        return 0
    
    if not response.fields:
        return RESPONSE_HEADER_LEN
    
    # Count fields and calculate offset
    field_count = 0
    for field in response.fields:
        if field.type == FieldType.NONE:
            break
        field_count += 1
    
    # Calculate total field length
    fields_len = 0
    for i in range(field_count):
        fields_len += get_field_len(response.fields[i].type)
    
    return RESPONSE_HEADER_LEN + fields_len


def format_request(msg: Message, sequence: int, request: Request, 
                  values: List[Any], expected_responses: List[Response]) -> None:
    """Format a request message to be sent to chronyd.
    
    Args:
        msg: Message object to populate
        sequence: Sequence number for the request
        request: Request definition
        values: Values for the request fields
        expected_responses: Expected response types
    """
    # Initialize message
    msg.msg = bytearray(len(msg.msg))
    msg.length = 0
    msg.num_fields = 0
    msg.fields = request.fields
    
    # Set protocol version (6) and request type (1)
    msg.msg[0] = 6
    msg.msg[1] = 1
    
    # Set request code
    struct.pack_into(">H", msg.msg, 4, request.code)
    
    # Set sequence number
    struct.pack_into(">I", msg.msg, 8, sequence)
    
    # Add fields
    if request.fields:
        for i, field in enumerate(request.fields):
            if field.type == FieldType.NONE:
                break
            
            msg.num_fields = i + 1
            pos = get_field_position(msg, i)
            
            if pos <= 0:
                continue
            
            if field.type == FieldType.UINT32:
                struct.pack_into(">I", msg.msg, pos, values[i])
            elif field.type == FieldType.ADDRESS:
                # Copy address data (20 bytes)
                for j in range(20):
                    msg.msg[pos + j] = values[i][j]
            else:
                raise ValueError(f"Unsupported field type: {field.type}")
    
    # Calculate length
    if request.fields:
        msg.num_fields += 1
        msg.length = get_field_position(msg, len(request.fields))
        msg.num_fields -= 1
    else:
        msg.length = REQUEST_HEADER_LEN
    
    # Ensure message is long enough for expected response
    max_res_len = 0
    for resp in expected_responses:
        if resp.fields:  # Check if the response has fields defined
            res_len = get_response_len(resp)
            max_res_len = max(max_res_len, res_len)
    
    if msg.length < max_res_len:
        msg.length = max_res_len


def is_response_valid(request: Message, response: Message) -> bool:
    """Check if a response is valid for the given request.
    
    Args:
        request: The request message
        response: The response message
        
    Returns:
        bool: True if the response is valid, False otherwise
    """
    if (response.length < RESPONSE_HEADER_LEN or
            response.msg[0] != 6 or    # Version
            response.msg[1] != 2 or    # Response type
            response.msg[2] != 0 or    # Reserved
            response.msg[3] != 0):     # Reserved
        return False
    
    # Check that response code matches request code
    if (response.msg[4] != request.msg[4] or 
        response.msg[5] != request.msg[5]):
        return False
    
    # Check sequence number matches
    req_seq = struct.unpack_from(">I", request.msg, 8)[0]
    res_seq = struct.unpack_from(">I", response.msg, 16)[0]
    if req_seq != res_seq:
        return False
    
    return True


def process_response(msg: Message, expected_responses: List[Response]) -> ChronyError:
    """Process a response from chronyd.
    
    Args:
        msg: The response message to process
        expected_responses: List of expected response types
        
    Returns:
        ChronyError: Error code (CHRONY_OK on success)
    """
    msg.num_fields = 0
    msg.fields = None
    
    # Extract code and status from the response
    code = struct.unpack_from(">H", msg.msg, 6)[0]
    status = struct.unpack_from(">H", msg.msg, 8)[0]
    
    # Check the status code
    if status != 0:
        if status == 2:
            return ChronyError.UNAUTHORIZED
        elif status == 3:
            return ChronyError.OLD_SERVER
        elif status in (6, 13):
            return ChronyError.DISABLED
        elif status in (18, 19):
            return ChronyError.NEW_SERVER
        else:
            return ChronyError.UNEXPECTED_STATUS
    
    # Find matching response type
    for resp in expected_responses:
        if resp.code == code and resp.fields:
            msg.fields = resp.fields
            break
    
    if not msg.fields:
        return ChronyError.NEW_SERVER
    
    # Count fields and check length
    fields_count = 0
    for field in msg.fields:
        if field.type == FieldType.NONE:
            break
        fields_count += 1
    
    msg.num_fields = fields_count
    required_len = get_field_position(msg, fields_count)
    
    if msg.length < required_len:
        msg.num_fields = 0
        msg.fields = None
        return ChronyError.INVALID_RESPONSE
    
    return ChronyError.OK


def get_field_len(field_type: FieldType) -> int:
    """Get the length of a field type.
    
    Args:
        field_type: Type of the field
        
    Returns:
        int: Length of the field in bytes
    """
    if field_type == FieldType.NONE:
        return 0
    elif field_type == FieldType.UINT64:
        return 8
    elif field_type == FieldType.UINT32:
        return 4
    elif field_type in (FieldType.UINT16, FieldType.INT16):
        return 2
    elif field_type in (FieldType.UINT8, FieldType.INT8):
        return 1
    elif field_type == FieldType.FLOAT:
        return 4
    elif field_type in (FieldType.ADDRESS, FieldType.ADDRESS_OR_UINT32_IN_ADDRESS):
        return 20
    elif field_type == FieldType.TIMESPEC:
        return 12
    else:
        raise ValueError(f"Unknown field type: {field_type}")


def get_field_offset(fields: List[Field], field_index: int) -> int:
    """Get the offset of a field in a message.
    
    Args:
        fields: List of fields
        field_index: Index of the field
        
    Returns:
        int: Byte offset of the field
    """
    if not fields or field_index < 0:
        return 0
    
    offset = 0
    for i in range(field_index):
        offset += get_field_len(fields[i].type)
    
    return offset


def get_field_position(msg: Message, field_index: int) -> int:
    """Get the position of a field in a message.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        int: Position of the field in the message, or -1 if invalid
    """
    if not msg.fields or field_index < 0 or field_index >= msg.num_fields:
        return -1
    
    # Different header length for request vs response
    header_len = RESPONSE_HEADER_LEN if msg.msg[1] == 2 else REQUEST_HEADER_LEN
    
    return header_len + get_field_offset(msg.fields, field_index)


def resolve_field_type(msg: Message, field_index: int) -> FieldType:
    """Get the actual type of a field, resolving context-specific types.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        FieldType: The resolved field type
    """
    if not msg.fields or field_index < 0 or field_index >= msg.num_fields:
        return FieldType.NONE
    
    field_type = msg.fields[field_index].type
    
    # Handle special case for ADDRESS_OR_UINT32_IN_ADDRESS
    if field_type == FieldType.ADDRESS_OR_UINT32_IN_ADDRESS:
        if msg.fields == SOURCES_REPORT_FIELDS:
            # Mode is at index 4, reference clock is mode 2
            mode = get_field_uinteger(msg, 4)
            return FieldType.UINT32 if mode == 2 else FieldType.ADDRESS
        # Unsupported context
        raise ValueError("Unsupported context for ADDRESS_OR_UINT32_IN_ADDRESS")
    
    return field_type


def resolve_field_name(msg: Message, field_index: int) -> Optional[str]:
    """Get the name of a field, resolving context-specific names.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        str or None: The field name, or None if invalid
    """
    if not msg.fields or field_index < 0 or field_index >= msg.num_fields:
        return None
    
    name = msg.fields[field_index].name
    
    # Handle special case for ADDRESS_OR_UINT32_IN_ADDRESS
    if msg.fields[field_index].type == FieldType.ADDRESS_OR_UINT32_IN_ADDRESS:
        if msg.fields == SOURCES_REPORT_FIELDS:
            # Mode is at index 4, reference clock is mode 2
            mode = get_field_uinteger(msg, 4)
            
            # The name has two variants separated by null character
            parts = name.split('\0')
            if len(parts) > 1:
                return parts[1] if mode == 2 else parts[0]
            
        raise ValueError("Unsupported context for ADDRESS_OR_UINT32_IN_ADDRESS")
    
    return name


def resolve_field_content(msg: Message, field_index: int) -> ChronyFieldContent:
    """Get the content type of a field, resolving context-specific content.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        ChronyFieldContent: The field content type
    """
    if not msg.fields or field_index < 0 or field_index >= msg.num_fields:
        return ChronyFieldContent.NONE
    
    content = msg.fields[field_index].content
    
    # Handle special case for ADDRESS_OR_UINT32_IN_ADDRESS
    if msg.fields[field_index].type == FieldType.ADDRESS_OR_UINT32_IN_ADDRESS:
        if msg.fields == SOURCES_REPORT_FIELDS:
            # Mode is at index 4, reference clock is mode 2
            mode = get_field_uinteger(msg, 4)
            content = (ChronyFieldContent.REFERENCE_ID if mode == 2 
                    else ChronyFieldContent.ADDRESS)
        else:
            raise ValueError("Unsupported context for ADDRESS_OR_UINT32_IN_ADDRESS")
    
    # For address fields, verify we can extract a string
    if content == ChronyFieldContent.ADDRESS:
        if not get_field_string(msg, field_index):
            return ChronyFieldContent.NONE
    
    return content


def get_field_uinteger(msg: Message, field_index: int) -> int:
    """Extract an unsigned integer value from a field.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        int: The unsigned integer value
    """
    pos = get_field_position(msg, field_index)
    if pos < 0:
        return 0
    
    field_type = resolve_field_type(msg, field_index)
    
    if field_type == FieldType.UINT64:
        high = struct.unpack_from(">I", msg.msg, pos)[0]
        low = struct.unpack_from(">I", msg.msg, pos + 4)[0]
        return (high << 32) | low
    elif field_type == FieldType.UINT32:
        return struct.unpack_from(">I", msg.msg, pos)[0]
    elif field_type == FieldType.UINT16:
        return struct.unpack_from(">H", msg.msg, pos)[0]
    elif field_type == FieldType.UINT8:
        return msg.msg[pos]
    else:
        return 0


def get_field_integer(msg: Message, field_index: int) -> int:
    """Extract a signed integer value from a field.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        int: The signed integer value
    """
    pos = get_field_position(msg, field_index)
    if pos < 0:
        return 0
    
    field_type = resolve_field_type(msg, field_index)
    
    if field_type == FieldType.INT16:
        return struct.unpack_from(">h", msg.msg, pos)[0]
    elif field_type == FieldType.INT8:
        # Python doesn't have a direct way to unpack a signed byte
        # So we use the ctypes c_int8 to convert
        return int.from_bytes([msg.msg[pos]], byteorder='big', signed=True)
    else:
        return 0


def get_field_float(msg: Message, field_index: int) -> float:
    """Extract a floating-point value from a field.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        float: The floating-point value, or NaN if invalid
    """
    pos = get_field_position(msg, field_index)
    if pos < 0:
        return float('nan')
    
    field_type = resolve_field_type(msg, field_index)
    
    if field_type == FieldType.FLOAT:
        # Chronyd uses a special floating-point format
        x = struct.unpack_from(">I", msg.msg, pos)[0]
        
        # Extract exponent (7 bits signed) and coefficient (25 bits signed)
        exp = x >> 25
        if exp >= (1 << 6):
            exp -= (1 << 7)
        
        coef = x % (1 << 25)
        if coef >= (1 << 24):
            coef -= (1 << 25)
        
        # Calculate the actual value
        return coef * (2.0 ** (exp - 25))
    else:
        return float('nan')


def get_field_timespec(msg: Message, field_index: int) -> TimeSpec:
    """Extract a timespec value from a field.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        TimeSpec: The timespec value
    """
    pos = get_field_position(msg, field_index)
    if pos < 0:
        return TimeSpec()
    
    field_type = resolve_field_type(msg, field_index)
    
    if field_type == FieldType.TIMESPEC:
        high = struct.unpack_from(">I", msg.msg, pos)[0]
        low = struct.unpack_from(">I", msg.msg, pos + 4)[0]
        nsec = struct.unpack_from(">I", msg.msg, pos + 8)[0]
        
        return TimeSpec(
            tv_sec=(high << 32) | low,
            tv_nsec=nsec
        )
    else:
        return TimeSpec()


def get_field_string(msg: Message, field_index: int) -> Optional[str]:
    """Extract a string value from a field.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        
    Returns:
        str or None: The string value, or None if invalid
    """
    pos = get_field_position(msg, field_index)
    if pos < 0:
        return None
    
    field_type = resolve_field_type(msg, field_index)
    
    if field_type == FieldType.ADDRESS:
        # Get the address family (2 bytes at offset 16)
        family = struct.unpack_from(">H", msg.msg, pos + 16)[0]
        
        if family == 0:
            return None
        elif family == 1:  # IPv4
            try:
                ip = ipaddress.IPv4Address(msg.msg[pos:pos+4])
                return str(ip)
            except ValueError:
                return None
        elif family == 2:  # IPv6
            try:
                ip = ipaddress.IPv6Address(msg.msg[pos:pos+16])
                return str(ip)
            except ValueError:
                return None
        elif family == 3:  # ID (reference clock)
            id_num = struct.unpack_from(">I", msg.msg, pos)[0]
            return f"ID#{id_num:010d}"
        else:
            return "?"
    else:
        return None


def get_field_constant_name(msg: Message, field_index: int, value: int) -> Optional[str]:
    """Get the name of a constant value for a field.
    
    Args:
        msg: Message containing the field
        field_index: Index of the field
        value: The value to look up
        
    Returns:
        str or None: The constant name, or None if not found
    """
    if not msg.fields or field_index < 0 or field_index >= msg.num_fields:
        return None
    
    constants = msg.fields[field_index].constants
    if not constants:
        return None
    
    for constant in constants:
        if constant.value == value:
            return constant.name
    
    return None


def get_report_index(name: str) -> int:
    """Get the index of a report by name.
    
    Args:
        name: Name of the report
        
    Returns:
        int: Index of the report, or -1 if not found
    """
    for i, report in enumerate(REPORTS):
        if report.name == name:
            return i
    return -1


def get_report(report_index: int) -> Optional[Report]:
    """Get a report by index.
    
    Args:
        report_index: Index of the report
        
    Returns:
        Report or None: The report, or None if invalid
    """
    if report_index < 0 or report_index >= len(REPORTS):
        return None
    return REPORTS[report_index]


def is_report_fields(report_name: str, fields: List[Field]) -> bool:
    """Check if fields are from a specific report.
    
    Args:
        report_name: Name of the report
        fields: List of fields to check
        
    Returns:
        bool: True if the fields are from the report, False otherwise
    """
    report_index = get_report_index(report_name)
    if report_index < 0:
        return False
    
    report = REPORTS[report_index]
    if not report.record_responses:
        return False
    
    # Check if fields match any of the report's response fields
    for response in report.record_responses:
        if response.fields == fields:
            return True
    
    return False


def chrony_get_number_supported_reports() -> int:
    """Get the number of reports supported by the client.
    
    Returns:
        int: Number of supported reports
    """
    return len(REPORTS)


def chrony_get_report_name(report_index: int) -> Optional[str]:
    """Get the name of a report.
    
    Args:
        report_index: Index of the report
        
    Returns:
        str or None: Name of the report, or None if invalid
    """
    if report_index < 0 or report_index >= len(REPORTS):
        return None
    return REPORTS[report_index].name

