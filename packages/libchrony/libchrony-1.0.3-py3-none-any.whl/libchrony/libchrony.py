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

LibChrony - a Pythonic interface for interacting with chronyd

This module provides a higher-level, more Pythonic interface to the 
functionality ported from the original C library. It aims to make it easier
for modern Python programs to interact with the chrony time synchronization
service.
"""

import os
import select  # Required for socket operations
import socket
import logging
import time
from typing import Dict, List, Optional, Iterator, Union, Any, Tuple, Generator
from contextlib import contextmanager
from dataclasses import dataclass, field

from chrony_formats import (
    ChronyError, ChronyFieldType, ChronyFieldContent, TimeSpec
)
import client
import chrony_socket

# Configure logging
logger = logging.getLogger(__name__)


class ChronyException(Exception):
    """Base exception for all chrony-related errors."""
    
    def __init__(self, error_code: ChronyError, message: Optional[str] = None):
        self.error_code = error_code
        self.message = message or client.chrony_get_error_string(error_code)
        super().__init__(self.message)


class ConnectionError(ChronyException):
    """Exception raised for connection-related errors."""
    pass


class RequestError(ChronyException):
    """Exception raised for request-related errors."""
    pass


class ResponseError(ChronyException):
    """Exception raised for response-related errors."""
    pass


class AuthorizationError(ChronyException):
    """Exception raised for authorization-related errors."""
    pass


@dataclass
class FieldValue:
    """Class representing a field value with metadata."""
    name: str
    value: Any
    type: ChronyFieldType
    content: ChronyFieldContent
    
    def __str__(self) -> str:
        """String representation of the field value."""
        if self.type == ChronyFieldType.TIMESPEC:
            ts = self.value
            return f"{ts.tv_sec}.{ts.tv_nsec:09d}"
        
        if self.type == ChronyFieldType.FLOAT:
            # Format floats with appropriate precision
            return f"{self.value:.9f}"
        
        return str(self.value)
    
    @property
    def unit(self) -> Optional[str]:
        """Get the unit for the field content."""
        units = {
            ChronyFieldContent.INTERVAL_LOG2_SECONDS: "log2(seconds)",
            ChronyFieldContent.INTERVAL_SECONDS: "seconds",
            ChronyFieldContent.OFFSET_SECONDS: "seconds",
            ChronyFieldContent.MEASURE_SECONDS: "seconds",
            ChronyFieldContent.OFFSET_PPM: "ppm",
            ChronyFieldContent.MEASURE_PPM: "ppm",
            ChronyFieldContent.OFFSET_PPM_PER_SECOND: "ppm/s",
            ChronyFieldContent.LENGTH_BITS: "bits",
            ChronyFieldContent.LENGTH_BYTES: "bytes",
        }
        return units.get(self.content)


@dataclass
class Record:
    """Class representing a record from a chrony report."""
    report_name: str
    index: int
    fields: List[FieldValue] = field(default_factory=list)

    def __getitem__(self, key: Union[int, str]) -> FieldValue:
        """Get a field by index or name."""
        if isinstance(key, int):
            if 0 <= key < len(self.fields):
                return self.fields[key]
            raise IndexError(f"Field index {key} out of range")
    
        # Find field by name
        for field in self.fields:
            # Special handling for field names with null characters
            if isinstance(key, str) and '\0' in key:
                parts = key.split('\0')
                field_parts = field.name.split('\0')
                if any(part in field_parts for part in parts):
                    return field
            elif field.name == key:
                return field
    
        raise KeyError(f"Field '{key}' not found")
    
    def __iter__(self) -> Iterator[FieldValue]:
        """Iterate over fields."""
        return iter(self.fields)
    
    def __len__(self) -> int:
        """Number of fields in the record."""
        return len(self.fields)
    
    def as_dict(self) -> Dict[str, Any]:
        """Convert record to a dictionary mapping field names to values."""
        return {field.name: field.value for field in self.fields}


@dataclass
class Report:
    """Class representing a chrony report with multiple records."""
    name: str
    records: List[Record] = field(default_factory=list)
    
    def __getitem__(self, key: int) -> Record:
        """Get a record by index."""
        if 0 <= key < len(self.records):
            return self.records[key]
        raise IndexError(f"Record index {key} out of range")
    
    def __iter__(self) -> Iterator[Record]:
        """Iterate over records."""
        return iter(self.records)
    
    def __len__(self) -> int:
        """Number of records in the report."""
        return len(self.records)


class Chrony:
    """High-level interface for chrony."""
    
    def __init__(self, address: Optional[str] = None):
        """Initialize the chrony interface.
        
        Args:
            address: Address of chronyd (Unix socket path or IP:port).
                    If None, will try default connections.
        
        Raises:
            ConnectionError: If connection to chronyd fails.
        """
        self._socket = None
        self._session = None
        self._connect(address)
    
    def __del__(self):
        """Clean up resources."""
        self.close()
    
    def _connect(self, address: Optional[str] = None) -> None:
        """Connect to chronyd.
        
        Args:
            address: Address of chronyd.
            
        Raises:
            ConnectionError: If connection fails.
        """
        try:
            # Open socket
            self._socket = chrony_socket.chrony_open_socket(address)
            if not self._socket:
                raise ConnectionError(
                    ChronyError.RECV_FAILED, 
                    f"Failed to connect to chronyd at {address or 'default locations'}"
                )
            
            # Initialize session
            fd = self._socket.fileno()
            result, session = client.chrony_init_session(fd)
            
            if result != ChronyError.OK or not session:
                raise ConnectionError(
                    result,
                    f"Failed to initialize session: {client.chrony_get_error_string(result)}"
                )
            
            self._session = session
        
        except Exception as e:
            # Ensure socket is closed if initialization fails
            if self._socket:
                try:
                    chrony_socket.chrony_close_socket(self._socket)
                except Exception:
                    pass
                self._socket = None
            
            if isinstance(e, ChronyException):
                raise
            raise ConnectionError(
                ChronyError.RECV_FAILED, 
                f"Failed to connect to chronyd: {str(e)}"
            )
    
    def close(self) -> None:
        """Close the connection to chronyd."""
        if self._session:
            client.chrony_deinit_session(self._session)
            self._session = None
    
        if self._socket:
            try:
                chrony_socket.chrony_close_socket(self._socket)
            except OSError:
                # Socket might already be closed or invalid
                pass
            self._socket = None
    
    def _wait_for_response(self, timeout: float = 1.0) -> None:
        """Wait for a response from chronyd.
    
        Args:
            timeout: Timeout in seconds.
            
        Raises:
            ResponseError: If receiving the response fails.
        """
        if not self._session:
            raise ConnectionError(ChronyError.UNEXPECTED_CALL, "Not connected to chronyd")
    
        start_time = time.time()
        fd = client.chrony_get_fd(self._session)
    
        while client.chrony_needs_response(self._session):
            # Calculate remaining timeout
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise ResponseError(
                    ChronyError.RECV_FAILED, 
                    "Timeout waiting for response from chronyd"
                )
        
            # Wait for socket to be readable
            remaining = max(0.1, timeout - elapsed)  # Always wait at least 0.1s to prevent CPU spinning
            readable, _, _ = select.select([fd], [], [], remaining)
        
            if not readable:
                continue  # No data available yet, retry
        
            # Process the response
            result = client.chrony_process_response(self._session)
        
            if result != ChronyError.OK:
                error_msg = client.chrony_get_error_string(result)
            
                if result == ChronyError.UNAUTHORIZED:
                    raise AuthorizationError(result, f"Not authorized: {error_msg}")
                else:
                    raise ResponseError(result, f"Error processing response: {error_msg}")

#    def _wait_for_response(self, timeout: float = 1.0) -> None:
#        """Wait for a response from chronyd.
#        
#        Args:
#            timeout: Timeout in seconds.
#            
#        Raises:
#            ResponseError: If receiving the response fails.
#        """
#        if not self._session:
#            raise ConnectionError(ChronyError.UNEXPECTED_CALL, "Not connected to chronyd")
#        
#        start_time = time.time()
#        
#        while client.chrony_needs_response(self._session):
#            # Calculate remaining timeout
#            elapsed = time.time() - start_time
#            if elapsed >= timeout:
#                raise ResponseError(
#                    ChronyError.RECV_FAILED, 
#                    "Timeout waiting for response from chronyd"
#                )
#            
#            # Wait for socket to be readable
#            remaining = max(0.0, timeout - elapsed)
#            readable, _, _ = select.select([client.chrony_get_fd(self._session)], [], [], remaining)
#            
#            if not readable:
#                continue
#            
#            # Process the response
#            result = client.chrony_process_response(self._session)
#            
#            if result != ChronyError.OK:
#                error_msg = client.chrony_get_error_string(result)
#                
#                if result == ChronyError.UNAUTHORIZED:
#                    raise AuthorizationError(result, f"Not authorized: {error_msg}")
#                else:
#                    raise ResponseError(result, f"Error processing response: {error_msg}")
#    
    def _fetch_record(self, report_name: str, record_index: int) -> Record:
        """Fetch a single record from chronyd.
        
        Args:
            report_name: Name of the report.
            record_index: Index of the record.
            
        Returns:
            Record: The fetched record.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        if not self._session:
            raise ConnectionError(ChronyError.UNEXPECTED_CALL, "Not connected to chronyd")
        
        # Request the record
        result = client.chrony_request_record(self._session, report_name, record_index)
        if result != ChronyError.OK:
            raise RequestError(
                result,
                f"Failed to request record {record_index} of report '{report_name}': "
                f"{client.chrony_get_error_string(result)}"
            )
        
        # Wait for the response
        self._wait_for_response()
        
        # Create the record
        record = Record(report_name=report_name, index=record_index)
        
        # Extract fields
        num_fields = client.chrony_get_record_number_fields(self._session)
        for i in range(num_fields):
            field_name = client.chrony_get_field_name(self._session, i)
            field_type = client.chrony_get_field_type(self._session, i)
            field_content = client.chrony_get_field_content(self._session, i)
            
            if not field_name or field_content == ChronyFieldContent.NONE:
                continue
            
            # Extract the value based on type
            value = None
            if field_type == ChronyFieldType.UINTEGER:
                value = client.chrony_get_field_uinteger(self._session, i)
                
                # If this is an enum or flags, try to resolve constant names
                if field_content == ChronyFieldContent.ENUM:
                    name = client.chrony_get_field_constant_name(self._session, i, value)
                    if name:
                        value = name
                elif field_content == ChronyFieldContent.FLAGS:
                    # For flags, collect all set bits
                    flag_names = []
                    for bit in range(64):  # Max 64 bits in a uint64
                        flag = 1 << bit
                        if value & flag:
                            name = client.chrony_get_field_constant_name(self._session, i, flag)
                            if name:
                                flag_names.append(name)
                    
                    if flag_names:
                        value = flag_names
                elif field_content == ChronyFieldContent.BOOLEAN:
                    value = bool(value)
            
            elif field_type == ChronyFieldType.INTEGER:
                value = client.chrony_get_field_integer(self._session, i)
            
            elif field_type == ChronyFieldType.FLOAT:
                value = client.chrony_get_field_float(self._session, i)
            
            elif field_type == ChronyFieldType.STRING:
                value = client.chrony_get_field_string(self._session, i)
            
            elif field_type == ChronyFieldType.TIMESPEC:
                value = client.chrony_get_field_timespec(self._session, i)
            
            # Add the field to the record
            record.fields.append(FieldValue(
                name=field_name,
                value=value,
                type=field_type,
                content=field_content
            ))
        
        return record
    
    def get_record_count(self, report_name: str) -> int:
        """Get the number of records in a report.
        
        Args:
            report_name: Name of the report.
            
        Returns:
            int: Number of records.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        if not self._session:
            raise ConnectionError(ChronyError.UNEXPECTED_CALL, "Not connected to chronyd")
        
        # Request the record count
        result = client.chrony_request_report_number_records(self._session, report_name)
        if result != ChronyError.OK:
            raise RequestError(
                result,
                f"Failed to request record count for report '{report_name}': "
                f"{client.chrony_get_error_string(result)}"
            )
        
        # Wait for the response if needed
        if client.chrony_needs_response(self._session):
            self._wait_for_response()
        
        # Get the count
        return client.chrony_get_report_number_records(self._session)
    
    def get_record(self, report_name: str, record_index: int = 0) -> Record:
        """Get a single record from a report.
        
        Args:
            report_name: Name of the report.
            record_index: Index of the record (default: 0).
            
        Returns:
            Record: The requested record.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self._fetch_record(report_name, record_index)
    
    def get_report(self, report_name: str) -> Report:
        """Get all records from a report.
        
        Args:
            report_name: Name of the report.
            
        Returns:
            Report: The complete report with all records.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        # Get the number of records
        record_count = self.get_record_count(report_name)
        
        # Create the report
        report = Report(name=report_name)
        
        # Fetch all records
        for i in range(record_count):
            record = self._fetch_record(report_name, i)
            report.records.append(record)
        
        return report
    
    def iter_records(self, report_name: str) -> Generator[Record, None, None]:
        """Iterate over all records in a report.
        
        Args:
            report_name: Name of the report.
            
        Yields:
            Record: Each record in the report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        # Get the number of records
        record_count = self.get_record_count(report_name)
        
        # Yield each record
        for i in range(record_count):
            yield self._fetch_record(report_name, i)
    
    def get_available_reports(self) -> List[str]:
        """Get a list of all available reports.
        
        Returns:
            List[str]: Names of all available reports.
        """
        reports = []
        count = client.chrony_get_number_supported_reports()
        
        for i in range(count):
            name = client.chrony_get_report_name(i)
            if name:
                reports.append(name)
        
        return reports
    
    def get_tracking(self) -> Record:
        """Get the tracking report (current synchronization state).
        
        Returns:
            Record: The tracking report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self.get_record("tracking")
    
    def get_sources(self) -> Report:
        """Get the sources report (time sources).
        
        Returns:
            Report: The sources report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self.get_report("sources")
    
    def get_sourcestats(self) -> Report:
        """Get the sourcestats report (statistics for time sources).
        
        Returns:
            Report: The sourcestats report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self.get_report("sourcestats")
    
    def get_serverstats(self) -> Record:
        """Get the serverstats report (server statistics).
        
        Returns:
            Record: The serverstats report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self.get_record("serverstats")
    
    def get_activity(self) -> Record:
        """Get the activity report (source activity statistics).
        
        Returns:
            Record: The activity report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self.get_record("activity")
    
    def get_selectdata(self) -> Report:
        """Get the selectdata report (source selection data).
        
        Returns:
            Report: The selectdata report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self.get_report("selectdata")
    
    def get_rtcdata(self) -> Record:
        """Get the rtcdata report (real-time clock data).
        
        Returns:
            Record: The rtcdata report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self.get_record("rtcdata")
    
    def get_smoothing(self) -> Record:
        """Get the smoothing report (clock smoothing parameters).
        
        Returns:
            Record: The smoothing report.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        return self.get_record("smoothing")
    
    def get_all_reports(self) -> Dict[str, Union[Report, Record]]:
        """Get all available reports.
        
        Returns:
            Dict[str, Union[Report, Record]]: Dictionary mapping report names to reports.
            
        Raises:
            RequestError: If the request fails.
            ResponseError: If receiving or processing the response fails.
        """
        reports = {}
        
        for name in self.get_available_reports():
            try:
                # Get the record count
                count = self.get_record_count(name)
                
                if count == 1:
                    # Single-record report
                    reports[name] = self.get_record(name)
                else:
                    # Multi-record report
                    reports[name] = self.get_report(name)
            
            except ChronyException as e:
                # Log the error but continue with other reports
                logger.warning(f"Failed to get report '{name}': {e}")
                continue
        
        return reports


@contextmanager
def connect(address: Optional[str] = None) -> Generator[Chrony, None, None]:
    """Context manager for connecting to chronyd.
    
    Args:
        address: Address of chronyd (Unix socket path or IP:port).
                If None, will try default connections.
    
    Yields:
        Chrony: Connected chrony interface.
        
    Raises:
        ConnectionError: If connection to chronyd fails.
    """
    chrony = None
    try:
        chrony = Chrony(address)
        yield chrony
    finally:
        if chrony:
            chrony.close()


