# API Reference

This document provides a comprehensive reference of all classes, methods, and properties available in the Python libchrony library.

## Table of Contents

- [Exceptions](#exceptions)
- [Data Structures](#data-structures)
- [Connection Functions](#connection-functions)
- [Chrony Class](#chrony-class)
- [Record Class](#record-class)
- [Report Class](#report-class)
- [FieldValue Class](#fieldvalue-class)
- [Direct API Functions](#direct-api-functions)
- [Enumeration Types](#enumeration-types)

## Exceptions

### `ChronyException`

Base exception for all chrony-related errors.

```python
class ChronyException(Exception)
```

**Attributes:**
- `error_code`: The error code (ChronyError enum value)
- `message`: Descriptive error message

### `ConnectionError`

Exception raised for connection-related errors.

```python
class ConnectionError(ChronyException)
```

### `RequestError`

Exception raised for request-related errors.

```python
class RequestError(ChronyException)
```

### `ResponseError`

Exception raised for response-related errors.

```python
class ResponseError(ChronyException)
```

### `AuthorizationError`

Exception raised for authorization-related errors.

```python
class AuthorizationError(ChronyException)
```

## Data Structures

### `TimeSpec`

Represents a timespec structure (seconds and nanoseconds).

```python
@dataclass
class TimeSpec:
    tv_sec: int = 0
    tv_nsec: int = 0
```

### `Constant`

Represents an enumeration or flag constant.

```python
@dataclass
class Constant:
    value: int
    name: str
```

### `Field`

Represents a field definition in a report.

```python
@dataclass
class Field:
    name: str
    type: FieldType
    content: ChronyFieldContent
    constants: Optional[List[Constant]] = None
```

## Connection Functions

### `connect(address=None)`

Creates a context manager for connecting to chronyd.

```python
@contextmanager
def connect(address: Optional[str] = None) -> Generator[Chrony, None, None]
```

**Parameters:**
- `address` (str, optional): Address of chronyd (Unix socket path or IP:port). If None, will try default connections.

**Returns:**
- A context manager that yields a `Chrony` object.

**Raises:**
- `ConnectionError`: If connection to chronyd fails.

**Example:**
```python
with libchrony.connect() as chrony:
    tracking = chrony.get_tracking()
```

## Chrony Class

The main interface class for interacting with chronyd.

```python
class Chrony:
    def __init__(self, address: Optional[str] = None)
    def close(self) -> None
    def get_available_reports(self) -> List[str]
    def get_record_count(self, report_name: str) -> int
    def get_record(self, report_name: str, record_index: int = 0) -> Record
    def get_report(self, report_name: str) -> Report
    def iter_records(self, report_name: str) -> Generator[Record, None, None]
    def get_tracking(self) -> Record
    def get_sources(self) -> Report
    def get_sourcestats(self) -> Report
    def get_serverstats(self) -> Record
    def get_activity(self) -> Record
    def get_selectdata(self) -> Report
    def get_rtcdata(self) -> Record
    def get_smoothing(self) -> Record
    def get_all_reports(self) -> Dict[str, Union[Report, Record]]
```

### `__init__(address=None)`

Initializes a new connection to chronyd.

**Parameters:**
- `address` (str, optional): Address of chronyd (Unix socket path or IP:port). If None, will try default connections.

**Raises:**
- `ConnectionError`: If connection to chronyd fails.

### `close()`

Closes the connection to chronyd.

### `get_available_reports()`

Gets a list of all available reports.

**Returns:**
- List of report names.

### `get_record_count(report_name)`

Gets the number of records in a report.

**Parameters:**
- `report_name` (str): Name of the report.

**Returns:**
- Number of records.

**Raises:**
- `RequestError`: If the request fails.
- `ResponseError`: If receiving or processing the response fails.

### `get_record(report_name, record_index=0)`

Gets a single record from a report.

**Parameters:**
- `report_name` (str): Name of the report.
- `record_index` (int, optional): Index of the record. Default is 0.

**Returns:**
- `Record` object containing the requested record.

**Raises:**
- `RequestError`: If the request fails.
- `ResponseError`: If receiving or processing the response fails.

### `get_report(report_name)`

Gets all records from a report.

**Parameters:**
- `report_name` (str): Name of the report.

**Returns:**
- `Report` object containing all records.

**Raises:**
- `RequestError`: If the request fails.
- `ResponseError`: If receiving or processing the response fails.

### `iter_records(report_name)`

Iterates over all records in a report.

**Parameters:**
- `report_name` (str): Name of the report.

**Yields:**
- `Record` objects for each record in the report.

**Raises:**
- `RequestError`: If the request fails.
- `ResponseError`: If receiving or processing the response fails.

### `get_tracking()`

Gets the tracking report (current synchronization state).

**Returns:**
- `Record` object containing the tracking report.

### `get_sources()`

Gets the sources report (time sources).

**Returns:**
- `Report` object containing all source records.

### `get_sourcestats()`

Gets the sourcestats report (statistics for time sources).

**Returns:**
- `Report` object containing all sourcestats records.

### `get_serverstats()`

Gets the serverstats report (server statistics).

**Returns:**
- `Record` object containing the server statistics.

### `get_activity()`

Gets the activity report (source activity statistics).

**Returns:**
- `Record` object containing activity statistics.

### `get_selectdata()`

Gets the selectdata report (source selection data).

**Returns:**
- `Report` object containing all selectdata records.

### `get_rtcdata()`

Gets the rtcdata report (real-time clock data).

**Returns:**
- `Record` object containing RTC data.

### `get_smoothing()`

Gets the smoothing report (clock smoothing parameters).

**Returns:**
- `Record` object containing smoothing parameters.

### `get_all_reports()`

Gets all available reports.

**Returns:**
- Dictionary mapping report names to `Report` or `Record` objects.

## Record Class

Represents a record from a chrony report.

```python
@dataclass
class Record:
    report_name: str
    index: int
    fields: List[FieldValue] = field(default_factory=list)
    
    def __getitem__(self, key: Union[int, str]) -> FieldValue
    def __iter__(self) -> Iterator[FieldValue]
    def __len__(self) -> int
    def as_dict(self) -> Dict[str, Any]
```

### `__getitem__(key)`

Gets a field by index or name.

**Parameters:**
- `key` (int or str): Index or name of the field.

**Returns:**
- `FieldValue` object.

**Raises:**
- `IndexError`: If the index is out of range.
- `KeyError`: If the field name is not found.

### `__iter__()`

Iterates over fields.

**Returns:**
- Iterator over `FieldValue` objects.

### `__len__()`

Gets the number of fields.

**Returns:**
- Number of fields in the record.

### `as_dict()`

Converts the record to a dictionary.

**Returns:**
- Dictionary mapping field names to values.

## Report Class

Represents a chrony report with multiple records.

```python
@dataclass
class Report:
    name: str
    records: List[Record] = field(default_factory=list)
    
    def __getitem__(self, key: int) -> Record
    def __iter__(self) -> Iterator[Record]
    def __len__(self) -> int
```

### `__getitem__(key)`

Gets a record by index.

**Parameters:**
- `key` (int): Index of the record.

**Returns:**
- `Record` object.

**Raises:**
- `IndexError`: If the index is out of range.

### `__iter__()`

Iterates over records.

**Returns:**
- Iterator over `Record` objects.

### `__len__()`

Gets the number of records.

**Returns:**
- Number of records in the report.

## FieldValue Class

Represents a field value with metadata.

```python
@dataclass
class FieldValue:
    name: str
    value: Any
    type: ChronyFieldType
    content: ChronyFieldContent
    
    def __str__(self) -> str
    @property
    def unit(self) -> Optional[str]
```

### `__str__()`

Gets a string representation of the value.

**Returns:**
- String representation of the field value.

### `unit`

Property that returns the unit for the field content.

**Returns:**
- Unit string or None if the field doesn't have a unit.

## Direct API Functions

These functions match the original C API and are available in the `client` module.

### Socket Functions

```python
def chrony_open_socket(address: Optional[str] = None) -> Optional[socket.socket]
def chrony_close_socket(sock: socket.socket) -> None
```

### Session Management

```python
def chrony_init_session(sock_or_fd: Union[socket.socket, int]) -> Tuple[ChronyError, Optional[ChronySession]]
def chrony_deinit_session(session: ChronySession) -> None
def chrony_get_fd(session: ChronySession) -> int
def chrony_needs_response(session: ChronySession) -> bool
def chrony_process_response(session: ChronySession) -> ChronyError
```

### Report Functions

```python
def chrony_get_number_supported_reports() -> int
def chrony_get_report_name(report: int) -> Optional[str]
def chrony_request_report_number_records(session: ChronySession, report_name: str) -> ChronyError
def chrony_get_report_number_records(session: ChronySession) -> int
def chrony_request_record(session: ChronySession, report_name: str, record: int) -> ChronyError
```

### Field Access Functions

```python
def chrony_get_record_number_fields(session: ChronySession) -> int
def chrony_get_field_name(session: ChronySession, field: int) -> Optional[str]
def chrony_get_field_index(session: ChronySession, name: str) -> int
def chrony_get_field_type(session: ChronySession, field: int) -> ChronyFieldType
def chrony_get_field_content(session: ChronySession, field: int) -> ChronyFieldContent
def chrony_get_field_uinteger(session: ChronySession, field: int) -> int
def chrony_get_field_integer(session: ChronySession, field: int) -> int
def chrony_get_field_float(session: ChronySession, field: int) -> float
def chrony_get_field_timespec(session: ChronySession, field: int) -> TimeSpec
def chrony_get_field_string(session: ChronySession, field: int) -> Optional[str]
def chrony_get_field_constant_name(session: ChronySession, field: int, value: int) -> Optional[str]
```

### Error Handling

```python
def chrony_get_error_string(error: ChronyError) -> str
```

## Enumeration Types

### `ChronyError`

```python
class ChronyError(IntEnum):
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
```

### `ChronyFieldType`

```python
class ChronyFieldType(IntEnum):
    NONE = 0
    UINTEGER = 1
    INTEGER = 2
    FLOAT = 3
    TIMESPEC = 4
    STRING = 5
```

### `ChronyFieldContent`

```python
class ChronyFieldContent(IntEnum):
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
```

### `SessionState`

```python
class SessionState(IntEnum):
    IDLE = 0
    REQUEST_SENT = 1
    RESPONSE_RECEIVED = 2
    RESPONSE_ACCEPTED = 3
```

### Internal Field Types

```python
class FieldType(IntEnum):
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
    ADDRESS_OR_UINT32_IN_ADDRESS = 11
```

### License

LGPL V2.1 or later
