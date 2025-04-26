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

LibChrony data formats and structures

"""

from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from typing import Dict, List, Optional, Tuple, Union, Any
import socket
import struct
import time
from ctypes import c_int8, c_uint8, c_int16, c_uint16, c_uint32, c_uint64


# Maximum values and constants
MAX_MESSAGE_LEN = 1024
MAX_UNIX_SOCKET_INDEX = 1000
MAX_REQUESTS = 2
MAX_RESPONSES = 4
REQUEST_HEADER_LEN = 20
RESPONSE_HEADER_LEN = 28


class ChronyError(IntEnum):
    """Enum for error codes."""
    OK = 0
    NO_MEMORY = 1
    NO_RANDOM = 2
    UNKNOWN_REPORT = 3
    RANDOM_FAILED = 4
    SEND_FAILED = 5
    RECV_FAILED = 6
    INVALID_ARGUMENT = 7
    UNEXPECTED_CALL = 8
    UNAUTHORIZED = 9
    DISABLED = 10
    UNEXPECTED_STATUS = 11
    OLD_SERVER = 12
    NEW_SERVER = 13
    INVALID_RESPONSE = 14


class FieldType(IntEnum):
    """Enum for field data types."""
    NONE = 0
    UINT64 = 1
    UINT32 = 2
    UINT16 = 3
    UINT8 = 4
    INT16 = 5
    INT8 = 6
    FLOAT = 7
    ADDRESS = 8
    TIMESPEC = 9
    STRING = 10
    # Context-specific types
    ADDRESS_OR_UINT32_IN_ADDRESS = 11


class ChronyFieldType(IntEnum):
    """Enum for chrony field types returned to the API."""
    NONE = 0
    UINTEGER = 1
    INTEGER = 2
    FLOAT = 3
    TIMESPEC = 4
    STRING = 5


class ChronyFieldContent(IntEnum):
    """Enum for record field content types (e.g. units)."""
    NONE = 0
    COUNT = 1
    TIME = 2
    INTERVAL_LOG2_SECONDS = 3
    INTERVAL_SECONDS = 4
    OFFSET_SECONDS = 5
    MEASURE_SECONDS = 6
    OFFSET_PPM = 7
    MEASURE_PPM = 8
    OFFSET_PPM_PER_SECOND = 9
    RATIO = 10
    REFERENCE_ID = 11
    ENUM = 12
    BITS = 13
    FLAGS = 14
    ADDRESS = 15
    PORT = 16
    INDEX = 17
    LENGTH_BITS = 18
    LENGTH_BYTES = 19
    BOOLEAN = 20


class SessionState(IntEnum):
    """Session state enum."""
    IDLE = 0
    REQUEST_SENT = 1
    RESPONSE_RECEIVED = 2
    RESPONSE_ACCEPTED = 3


@dataclass
class Constant:
    """Constants used for enum/flag values."""
    value: int
    name: str


@dataclass
class Field:
    """Field definition for reports."""
    name: str
    type: FieldType
    content: ChronyFieldContent
    constants: Optional[List[Constant]] = None


@dataclass
class Request:
    """Request definition."""
    code: int
    fields: Optional[List[Field]] = None


@dataclass
class Response:
    """Response definition."""
    code: int
    fields: Optional[List[Field]] = None


@dataclass
class Report:
    """Report definition."""
    name: str
    count_requests: List[Request] = field(default_factory=list)
    count_responses: List[Response] = field(default_factory=list)
    record_requests: List[Request] = field(default_factory=list)
    record_responses: List[Response] = field(default_factory=list)


@dataclass
class Message:
    """Message for communication with chronyd."""
    msg: bytearray = field(default_factory=lambda: bytearray(MAX_MESSAGE_LEN))
    length: int = 0
    num_fields: int = 0
    fields: Optional[List[Field]] = None


@dataclass
class TimeSpec:
    """TimeSpec structure (equivalent to struct timespec)."""
    tv_sec: int = 0
    tv_nsec: int = 0


# Constant definitions from reports.h
# Leap status enum
LEAP_ENUMS = [
    Constant(0, "normal"),
    Constant(1, "insert second"),
    Constant(2, "delete second"),
    Constant(3, "not synchronized")
]

# Sources state enum
SOURCES_STATE_ENUMS = [
    Constant(0, "selected"),
    Constant(1, "nonselectable"),
    Constant(2, "falseticker"),
    Constant(3, "jittery"),
    Constant(4, "unselected"),
    Constant(5, "selectable")
]

# Sources mode enum
SOURCES_MODE_ENUMS = [
    Constant(0, "client"),
    Constant(1, "peer"),
    Constant(2, "reference clock")
]

# Selectdata state enum
SELECTDATA_STATE_ENUMS = [
    Constant(ord('N'), "ignored"),
    Constant(ord('s'), "not synchronized"),
    Constant(ord('M'), "missing samples"),
    Constant(ord('d'), "unacceptable distance"),
    Constant(ord('D'), "large distance"),
    Constant(ord('~'), "jittery"),
    Constant(ord('w'), "waiting for others"),
    Constant(ord('W'), "missing selectable sources"),
    Constant(ord('S'), "stale"),
    Constant(ord('O'), "orphan"),
    Constant(ord('T'), "not trusted"),
    Constant(ord('P'), "not preferred"),
    Constant(ord('U'), "waiting for update"),
    Constant(ord('x'), "falseticker"),
    Constant(ord('+'), "combined"),
    Constant(ord('*'), "best")
]

# Selectdata option flags
SELECTDATA_OPTION_FLAGS = [
    Constant(0x1, "noselect"),
    Constant(0x2, "prefer"),
    Constant(0x4, "trust"),
    Constant(0x8, "require")
]

# Authdata mode enum
AUTHDATA_MODE_ENUMS = [
    Constant(0, "none"),
    Constant(1, "symmetric key"),
    Constant(2, "NTS")
]

# Authdata keytype enum
AUTHDATA_KEYTYPE_ENUMS = [
    Constant(1, "MD5"),
    Constant(2, "SHA1"),
    Constant(3, "SHA256"),
    Constant(4, "SHA384"),
    Constant(5, "SHA512"),
    Constant(6, "SHA3-224"),
    Constant(7, "SHA3-256"),
    Constant(8, "SHA3-384"),
    Constant(9, "SHA3-512"),
    Constant(10, "TIGER"),
    Constant(11, "WHIRLPOOL"),
    Constant(13, "AES128"),
    Constant(14, "AES256"),
    Constant(15, "AEAD-AES-SIV-CMAC-256"),
    Constant(30, "AEAD-AES-128-GCM-SIV")
]

# NTP mode enum
NTP_MODE_ENUMS = [
    Constant(1, "active symmetric"),
    Constant(2, "passive symmetric"),
    Constant(4, "server")
]

# NTP timestamping enum
NTP_TIMESTAMPING_ENUMS = [
    Constant(ord('D'), "daemon"),
    Constant(ord('K'), "kernel"),
    Constant(ord('H'), "hardware")
]

# NTP flags
NTP_FLAGS = [
    Constant(0x200, "test1"),
    Constant(0x100, "test2"),
    Constant(0x80, "test3"),
    Constant(0x40, "test5"),
    Constant(0x20, "test6"),
    Constant(0x10, "test7"),
    Constant(0x8, "testA"),
    Constant(0x4, "testC"),
    Constant(0x2, "testB"),
    Constant(0x1, "testD"),
    Constant(0x4000, "interleaved"),
    Constant(0x8000, "authenticated")
]

# Smoothing flags
SMOOTHING_FLAGS = [
    Constant(0x1, "active"),
    Constant(0x2, "leaponly")
]

# Field definitions for all reports
TRACKING_REPORT_FIELDS = [
    Field("reference ID", FieldType.UINT32, ChronyFieldContent.REFERENCE_ID),
    Field("address", FieldType.ADDRESS, ChronyFieldContent.ADDRESS),
    Field("stratum", FieldType.UINT16, ChronyFieldContent.COUNT),
    Field("leap status", FieldType.UINT16, ChronyFieldContent.ENUM, LEAP_ENUMS),
    Field("reference time", FieldType.TIMESPEC, ChronyFieldContent.TIME),
    Field("current correction", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("last offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("RMS offset", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("frequency offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_PPM),
    Field("residual frequency", FieldType.FLOAT, ChronyFieldContent.OFFSET_PPM),
    Field("skew", FieldType.FLOAT, ChronyFieldContent.MEASURE_PPM),
    Field("root delay", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("root dispersion", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("last update interval", FieldType.FLOAT, ChronyFieldContent.INTERVAL_SECONDS)
]

NUM_SOURCES_FIELDS = [
    Field("sources", FieldType.UINT32, ChronyFieldContent.COUNT)
]

REQUEST_BY_INDEX_FIELDS = [
    Field("index", FieldType.UINT32, ChronyFieldContent.INDEX)
]

SOURCES_REPORT_FIELDS = [
    Field("address\0reference ID", FieldType.ADDRESS_OR_UINT32_IN_ADDRESS, ChronyFieldContent.NONE),
    Field("poll", FieldType.INT16, ChronyFieldContent.INTERVAL_LOG2_SECONDS),
    Field("stratum", FieldType.UINT16, ChronyFieldContent.COUNT),
    Field("state", FieldType.UINT16, ChronyFieldContent.ENUM, SOURCES_STATE_ENUMS),
    Field("mode", FieldType.UINT16, ChronyFieldContent.ENUM, SOURCES_MODE_ENUMS),
    Field("flags", FieldType.UINT16, ChronyFieldContent.NONE),
    Field("reachability", FieldType.UINT16, ChronyFieldContent.BITS),
    Field("last sample ago", FieldType.UINT32, ChronyFieldContent.INTERVAL_SECONDS),
    Field("original last sample offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("adjusted last sample offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("last sample error", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS)
]

SOURCESTATS_REPORT_FIELDS = [
    Field("reference ID", FieldType.UINT32, ChronyFieldContent.REFERENCE_ID),
    Field("address", FieldType.ADDRESS, ChronyFieldContent.ADDRESS),
    Field("samples", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("runs", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("span", FieldType.UINT32, ChronyFieldContent.INTERVAL_SECONDS),
    Field("standard deviation", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("residual frequency", FieldType.FLOAT, ChronyFieldContent.OFFSET_PPM),
    Field("skew", FieldType.FLOAT, ChronyFieldContent.MEASURE_PPM),
    Field("offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("offset error", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS)
]

SELECTDATA_REPORT_FIELDS = [
    Field("reference ID", FieldType.UINT32, ChronyFieldContent.REFERENCE_ID),
    Field("address", FieldType.ADDRESS, ChronyFieldContent.ADDRESS),
    Field("state", FieldType.UINT8, ChronyFieldContent.ENUM, SELECTDATA_STATE_ENUMS),
    Field("authentication", FieldType.UINT8, ChronyFieldContent.BOOLEAN),
    Field("leap status", FieldType.UINT8, ChronyFieldContent.ENUM, LEAP_ENUMS),
    Field("reserved #1", FieldType.UINT8, ChronyFieldContent.NONE),
    Field("configured options", FieldType.UINT16, ChronyFieldContent.FLAGS, SELECTDATA_OPTION_FLAGS),
    Field("effective options", FieldType.UINT16, ChronyFieldContent.FLAGS, SELECTDATA_OPTION_FLAGS),
    Field("last sample ago", FieldType.UINT32, ChronyFieldContent.INTERVAL_SECONDS),
    Field("score", FieldType.FLOAT, ChronyFieldContent.RATIO),
    Field("low limit", FieldType.FLOAT, ChronyFieldContent.INTERVAL_SECONDS),
    Field("high limit", FieldType.FLOAT, ChronyFieldContent.INTERVAL_SECONDS)
]

ACTIVITY_REPORT_FIELDS = [
    Field("online sources", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("offline sources", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("burst online-return sources", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("burst offline-return sources", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("unresolved sources", FieldType.UINT32, ChronyFieldContent.COUNT)
]

REQUEST_BY_ADDRESS_FIELDS = [
    Field("address", FieldType.ADDRESS, ChronyFieldContent.ADDRESS)
]

AUTHDATA_REPORT_FIELDS = [
    Field("mode", FieldType.UINT16, ChronyFieldContent.ENUM, AUTHDATA_MODE_ENUMS),
    Field("key type", FieldType.UINT16, ChronyFieldContent.ENUM, AUTHDATA_KEYTYPE_ENUMS),
    Field("key ID", FieldType.UINT32, ChronyFieldContent.INDEX),
    Field("key length", FieldType.UINT16, ChronyFieldContent.LENGTH_BITS),
    Field("key establishment attempts", FieldType.UINT16, ChronyFieldContent.COUNT),
    Field("last key establishment ago", FieldType.UINT32, ChronyFieldContent.INTERVAL_SECONDS),
    Field("cookies", FieldType.UINT16, ChronyFieldContent.COUNT),
    Field("cookie length", FieldType.UINT16, ChronyFieldContent.LENGTH_BYTES),
    Field("NAK", FieldType.UINT16, ChronyFieldContent.BOOLEAN),
    Field("reserved #1", FieldType.UINT16, ChronyFieldContent.NONE)
]

NTPDATA_REPORT_FIELDS = [
    Field("remote address", FieldType.ADDRESS, ChronyFieldContent.ADDRESS),
    Field("local address", FieldType.ADDRESS, ChronyFieldContent.ADDRESS),
    Field("remote port", FieldType.UINT16, ChronyFieldContent.PORT),
    Field("leap status", FieldType.UINT8, ChronyFieldContent.ENUM, LEAP_ENUMS),
    Field("version", FieldType.UINT8, ChronyFieldContent.COUNT),
    Field("mode", FieldType.UINT8, ChronyFieldContent.ENUM, NTP_MODE_ENUMS),
    Field("stratum", FieldType.UINT8, ChronyFieldContent.COUNT),
    Field("poll", FieldType.INT8, ChronyFieldContent.INTERVAL_LOG2_SECONDS),
    Field("precision", FieldType.INT8, ChronyFieldContent.INTERVAL_LOG2_SECONDS),
    Field("root delay", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("root dispersion", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("reference ID", FieldType.UINT32, ChronyFieldContent.REFERENCE_ID),
    Field("reference time", FieldType.TIMESPEC, ChronyFieldContent.TIME),
    Field("offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("peer delay", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("peer dispersion", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("response time", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("jitter asymmetry", FieldType.FLOAT, ChronyFieldContent.RATIO),
    Field("flags", FieldType.UINT16, ChronyFieldContent.FLAGS, NTP_FLAGS),
    Field("transmit timestamping", FieldType.UINT8, ChronyFieldContent.ENUM, NTP_TIMESTAMPING_ENUMS),
    Field("receive timestamping", FieldType.UINT8, ChronyFieldContent.ENUM, NTP_TIMESTAMPING_ENUMS),
    Field("transmitted messages", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received messages", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received valid messages", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received good messages", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("reserved #1", FieldType.UINT32, ChronyFieldContent.NONE),
    Field("reserved #2", FieldType.UINT32, ChronyFieldContent.NONE),
    Field("reserved #3", FieldType.UINT32, ChronyFieldContent.NONE)
]

NTPDATA2_REPORT_FIELDS = [
    Field("remote address", FieldType.ADDRESS, ChronyFieldContent.ADDRESS),
    Field("local address", FieldType.ADDRESS, ChronyFieldContent.ADDRESS),
    Field("remote port", FieldType.UINT16, ChronyFieldContent.PORT),
    Field("leap status", FieldType.UINT8, ChronyFieldContent.ENUM, LEAP_ENUMS),
    Field("version", FieldType.UINT8, ChronyFieldContent.COUNT),
    Field("mode", FieldType.UINT8, ChronyFieldContent.ENUM, NTP_MODE_ENUMS),
    Field("stratum", FieldType.UINT8, ChronyFieldContent.COUNT),
    Field("poll", FieldType.INT8, ChronyFieldContent.INTERVAL_LOG2_SECONDS),
    Field("precision", FieldType.INT8, ChronyFieldContent.INTERVAL_LOG2_SECONDS),
    Field("root delay", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("root dispersion", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("reference ID", FieldType.UINT32, ChronyFieldContent.REFERENCE_ID),
    Field("reference time", FieldType.TIMESPEC, ChronyFieldContent.TIME),
    Field("offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("peer delay", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("peer dispersion", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("response time", FieldType.FLOAT, ChronyFieldContent.MEASURE_SECONDS),
    Field("jitter asymmetry", FieldType.FLOAT, ChronyFieldContent.RATIO),
    Field("flags", FieldType.UINT16, ChronyFieldContent.FLAGS, NTP_FLAGS),
    Field("transmit timestamping", FieldType.UINT8, ChronyFieldContent.ENUM, NTP_TIMESTAMPING_ENUMS),
    Field("receive timestamping", FieldType.UINT8, ChronyFieldContent.ENUM, NTP_TIMESTAMPING_ENUMS),
    Field("transmitted messages", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received messages", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received valid messages", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received good messages", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("kernel transmit timestamps", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("kernel receive timestamps", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("hardware transmit timestamps", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("hardware receive timestamps", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("reserved #1", FieldType.UINT32, ChronyFieldContent.NONE),
    Field("reserved #2", FieldType.UINT32, ChronyFieldContent.NONE),
    Field("reserved #3", FieldType.UINT32, ChronyFieldContent.NONE),
    Field("reserved #4", FieldType.UINT32, ChronyFieldContent.NONE)
]

SERVERSTATS_REPORT_FIELDS = [
    Field("received NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received command requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped command requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped client log records", FieldType.UINT32, ChronyFieldContent.COUNT)
]

SERVERSTATS2_REPORT_FIELDS = [
    Field("received NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("accepted NTS-KE connections", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received command requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped NTS-KE connections", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped command requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped client log records", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received authenticated NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT)
]

SERVERSTATS3_REPORT_FIELDS = [
    Field("received NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("accepted NTS-KE connections", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received command requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped NTS-KE connections", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped command requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("dropped client log records", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received authenticated NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("received interleaved NTP requests", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("held NTP timestamps", FieldType.UINT32, ChronyFieldContent.COUNT),
    Field("NTP timestamp span", FieldType.UINT32, ChronyFieldContent.INTERVAL_SECONDS)
]

SERVERSTATS4_REPORT_FIELDS = [
    Field("received NTP requests", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("accepted NTS-KE connections", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("received command requests", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("dropped NTP requests", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("dropped NTS-KE connections", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("dropped command requests", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("dropped client log records", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("received authenticated NTP requests", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("received interleaved NTP requests", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("held NTP timestamps", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("NTP timestamp span", FieldType.UINT64, ChronyFieldContent.INTERVAL_SECONDS),
    Field("served daemon RX timestamps", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("served daemon TX timestamps", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("served kernel RX timestamps", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("served kernel TX timestamps", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("served hardware RX timestamps", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("served hardware TX timestamps", FieldType.UINT64, ChronyFieldContent.COUNT),
    Field("reserved #1", FieldType.UINT64, ChronyFieldContent.NONE),
    Field("reserved #2", FieldType.UINT64, ChronyFieldContent.NONE),
    Field("reserved #3", FieldType.UINT64, ChronyFieldContent.NONE),
    Field("reserved #4", FieldType.UINT64, ChronyFieldContent.NONE)
]

RTCDATA_REPORT_FIELDS = [
    Field("reference time", FieldType.TIMESPEC, ChronyFieldContent.TIME),
    Field("samples", FieldType.UINT16, ChronyFieldContent.COUNT),
    Field("runs", FieldType.UINT16, ChronyFieldContent.COUNT),
    Field("span", FieldType.UINT32, ChronyFieldContent.INTERVAL_SECONDS),
    Field("offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("frequency offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_PPM)
]

SMOOTHING_REPORT_FIELDS = [
    Field("flags", FieldType.UINT32, ChronyFieldContent.FLAGS, SMOOTHING_FLAGS),
    Field("offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_SECONDS),
    Field("frequency offset", FieldType.FLOAT, ChronyFieldContent.OFFSET_PPM),
    Field("wander", FieldType.FLOAT, ChronyFieldContent.OFFSET_PPM_PER_SECOND),
    Field("last update ago", FieldType.FLOAT, ChronyFieldContent.INTERVAL_SECONDS),
    Field("remaining time", FieldType.FLOAT, ChronyFieldContent.INTERVAL_SECONDS)
]

# Define all reports
REPORTS = [
    Report(
        name="tracking",
        record_requests=[Request(33)],
        record_responses=[Response(5, TRACKING_REPORT_FIELDS)]
    ),
    Report(
        name="sources",
        count_requests=[Request(14)],
        count_responses=[Response(2, NUM_SOURCES_FIELDS)],
        record_requests=[Request(15, REQUEST_BY_INDEX_FIELDS)],
        record_responses=[Response(3, SOURCES_REPORT_FIELDS)]
    ),
    Report(
        name="sourcestats",
        count_requests=[Request(14)],
        count_responses=[Response(2, NUM_SOURCES_FIELDS)],
        record_requests=[Request(34, REQUEST_BY_INDEX_FIELDS)],
        record_responses=[Response(6, SOURCESTATS_REPORT_FIELDS)]
    ),
    Report(
        name="selectdata",
        count_requests=[Request(14)],
        count_responses=[Response(2, NUM_SOURCES_FIELDS)],
        record_requests=[Request(69, REQUEST_BY_INDEX_FIELDS)],
        record_responses=[Response(23, SELECTDATA_REPORT_FIELDS)]
    ),
    Report(
        name="activity",
        record_requests=[Request(44)],
        record_responses=[Response(12, ACTIVITY_REPORT_FIELDS)]
    ),
    Report(
        name="authdata",
        count_requests=[Request(14)],
        count_responses=[Response(2, NUM_SOURCES_FIELDS)],
        record_requests=[Request(67, REQUEST_BY_ADDRESS_FIELDS)],
        record_responses=[Response(20, AUTHDATA_REPORT_FIELDS)]
    ),
    Report(
        name="ntpdata",
        count_requests=[Request(14)],
        count_responses=[Response(2, NUM_SOURCES_FIELDS)],
        record_requests=[Request(57, REQUEST_BY_ADDRESS_FIELDS)],
        record_responses=[
            Response(16, NTPDATA_REPORT_FIELDS),
            Response(26, NTPDATA2_REPORT_FIELDS)
        ]
    ),
    Report(
        name="serverstats",
        record_requests=[Request(54)],
        record_responses=[
            Response(14, SERVERSTATS_REPORT_FIELDS),
            Response(22, SERVERSTATS2_REPORT_FIELDS),
            Response(24, SERVERSTATS3_REPORT_FIELDS),
            Response(25, SERVERSTATS4_REPORT_FIELDS)
        ]
    ),
    Report(
        name="rtcdata",
        record_requests=[Request(35)],
        record_responses=[Response(7, RTCDATA_REPORT_FIELDS)]
    ),
    Report(
        name="smoothing",
        record_requests=[Request(51)],
        record_responses=[Response(13, SMOOTHING_REPORT_FIELDS)]
    )
]

# Helper functions

def get_field_len(field_type: FieldType) -> int:
    """Get the length of a field based on its type."""
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
    """Get the offset of a field in a message based on its index."""
    if not fields or field_index < 0:
        return 0
    
    offset = 0
    for i in range(field_index):
        offset += get_field_len(fields[i].type)
    return offset

def get_constant_name(constants: List[Constant], value: int) -> Optional[str]:
    """Get the name of a constant given its value."""
    if not constants:
        return None
    
    for constant in constants:
        if constant.value == value:
            return constant.name
    
    return None

def get_report_index(name: str) -> int:
    """Get the index of a report given its name."""
    for i, report in enumerate(REPORTS):
        if report.name == name:
            return i
    return -1

def get_report(report_index: int) -> Optional[Report]:
    """Get a report given its index."""
    if report_index < 0 or report_index >= len(REPORTS):
        return None
    return REPORTS[report_index]
