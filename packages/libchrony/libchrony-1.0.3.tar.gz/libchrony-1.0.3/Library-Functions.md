# LibChrony Python Library Functions

This documentation covers the functions available in the Python port of libchrony. The library provides two interfaces:

1. **Direct API** - Functions in `client.py` that closely mirror the original C API
2. **Pythonic API** - An object-oriented interface in `libchrony.py` with modern Python features

# Version

Version 1.0

## Direct API Functions (client.py)

These functions match the original C API and provide a familiar interface for users transitioning from the C library.

### Connection Management

#### `chrony_open_socket(address=None)`

Opens a socket connection to chronyd.

**Parameters:**
- `address` (str, optional): Address of the chronyd socket. If it starts with '/', it is interpreted as a Unix domain socket path. Otherwise, it is treated as an IPv4 or IPv6 address, optionally with a port number (default is 323). If None or empty, the function tries to connect to `/var/run/chrony/chronyd.sock`, then `127.0.0.1`, and finally `::1`.

**Returns:**
- A socket object connected to chronyd, or None if connection fails.

**Example:**
```python
import chrony_socket
sock = chrony_socket.chrony_open_socket("/var/run/chrony/chronyd.sock")
```

#### `chrony_close_socket(sock)`

Closes a chronyd socket connection.

**Parameters:**
- `sock` (socket): Socket returned by `chrony_open_socket()`.

**Example:**
```python
chrony_socket.chrony_close_socket(sock)
```

#### `chrony_init_session(sock_or_fd)`

Creates a new client-server session.

**Parameters:**
- `sock_or_fd` (socket or int): Socket object or file descriptor returned by `chrony_open_socket()`.

**Returns:**
- A tuple of (ChronyError, session) where session is a ChronySession object or None if initialization failed.

**Example:**
```python
result, session = client.chrony_init_session(sock)
if result == ChronyError.OK:
    # Use session
```

#### `chrony_deinit_session(session)`

Destroys a session.

**Parameters:**
- `session` (ChronySession): Session to destroy.

**Example:**
```python
client.chrony_deinit_session(session)
```

#### `chrony_get_fd(session)`

Gets the socket file descriptor used by the session.

**Parameters:**
- `session` (ChronySession): Session object.

**Returns:**
- The socket file descriptor.

**Example:**
```python
fd = client.chrony_get_fd(session)
```

### Communication Functions

#### `chrony_needs_response(session)`

Checks if the session is waiting for a server response.

**Parameters:**
- `session` (ChronySession): Session object.

**Returns:**
- True if waiting for a response, False otherwise.

**Example:**
```python
if client.chrony_needs_response(session):
    # Need to process response
```

#### `chrony_process_response(session)`

Processes a server response. This function should be called only when `chrony_needs_response()` returns True.

**Parameters:**
- `session` (ChronySession): Session object.

**Returns:**
- Error code (ChronyError.OK on success).

**Example:**
```python
error = client.chrony_process_response(session)
```

### Report Management

#### `chrony_get_number_supported_reports()`

Gets the number of reports supported by the client.

**Returns:**
- Number of supported reports.

**Example:**
```python
num_reports = client.chrony_get_number_supported_reports()
```

#### `chrony_get_report_name(report)`

Gets the name of a report supported by the client.

**Parameters:**
- `report` (int): Index of the report (starting at 0).

**Returns:**
- Name of the report (e.g., "sources", "tracking").

**Example:**
```python
report_name = client.chrony_get_report_name(0)
```

#### `chrony_request_report_number_records(session, report_name)`

Sends a request to get the number of records for a report.

**Parameters:**
- `session` (ChronySession): Session object.
- `report_name` (str): Name of the report.

**Returns:**
- Error code (ChronyError.OK on success).

**Example:**
```python
error = client.chrony_request_report_number_records(session, "sources")
```

#### `chrony_get_report_number_records(session)`

Gets the number of records available for the requested report.

**Parameters:**
- `session` (ChronySession): Session object.

**Returns:**
- Number of records.

**Example:**
```python
num_records = client.chrony_get_report_number_records(session)
```

#### `chrony_request_record(session, report_name, record)`

Sends a request to get a record of a report.

**Parameters:**
- `session` (ChronySession): Session object.
- `report_name` (str): Name of the report.
- `record` (int): Index of the record (starting at 0).

**Returns:**
- Error code (ChronyError.OK on success).

**Example:**
```python
error = client.chrony_request_record(session, "tracking", 0)
```

### Field Access

#### `chrony_get_record_number_fields(session)`

Gets the number of fields in the requested record.

**Parameters:**
- `session` (ChronySession): Session object.

**Returns:**
- Number of fields.

**Example:**
```python
num_fields = client.chrony_get_record_number_fields(session)
```

#### `chrony_get_field_name(session, field)`

Gets the name of a field in the requested record.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).

**Returns:**
- Name of the field, or None if the index is not valid.

**Example:**
```python
field_name = client.chrony_get_field_name(session, 0)
```

#### `chrony_get_field_index(session, name)`

Gets the index of a field given by its name.

**Parameters:**
- `session` (ChronySession): Session object.
- `name` (str): Name of the field.

**Returns:**
- Index of the field, or -1 if not found.

**Example:**
```python
field_index = client.chrony_get_field_index(session, "stratum")
```

#### `chrony_get_field_type(session, field)`

Gets the type of a field.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).

**Returns:**
- Type of the field (a value from the ChronyFieldType enum).

**Example:**
```python
field_type = client.chrony_get_field_type(session, 0)
```

#### `chrony_get_field_content(session, field)`

Gets the content type of a field.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).

**Returns:**
- Content type of the field (a value from the ChronyFieldContent enum).

**Example:**
```python
field_content = client.chrony_get_field_content(session, 0)
```

#### `chrony_get_field_uinteger(session, field)`

Gets the value of an unsigned integer field.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).

**Returns:**
- Value of the field as int.

**Example:**
```python
value = client.chrony_get_field_uinteger(session, 0)
```

#### `chrony_get_field_integer(session, field)`

Gets the value of a signed integer field.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).

**Returns:**
- Value of the field as int.

**Example:**
```python
value = client.chrony_get_field_integer(session, 0)
```

#### `chrony_get_field_float(session, field)`

Gets the value of a floating-point field.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).

**Returns:**
- Value of the field as float.

**Example:**
```python
value = client.chrony_get_field_float(session, 0)
```

#### `chrony_get_field_timespec(session, field)`

Gets the value of a timespec field.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).

**Returns:**
- Value of the field as TimeSpec object.

**Example:**
```python
timespec = client.chrony_get_field_timespec(session, 0)
```

#### `chrony_get_field_string(session, field)`

Gets the value of a string field.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).

**Returns:**
- Value of the field as str, or None if not a string field.

**Example:**
```python
string_value = client.chrony_get_field_string(session, 0)
```

#### `chrony_get_field_constant_name(session, field, value)`

Gets the name of a constant value for a field.

**Parameters:**
- `session` (ChronySession): Session object.
- `field` (int): Index of the field in the record (starting at 0).
- `value` (int): Value to look up.

**Returns:**
- Name of the constant, or None if not found.

**Example:**
```python
const_name = client.chrony_get_field_constant_name(session, 0, 1)
```

### Error Handling

#### `chrony_get_error_string(error)`

Gets a string describing a libchrony error code.

**Parameters:**
- `error` (ChronyError): Error code.

**Returns:**
- Description of the error.

**Example:**
```python
error_description = client.chrony_get_error_string(ChronyError.UNAUTHORIZED)
```

## Pythonic API Functions (libchrony.py)

These functions provide an object-oriented interface with modern Python features like context managers, iterators, and exceptions.

### Connection Management

#### `connect(address=None)`

Context manager for connecting to chronyd.

**Parameters:**
- `address` (str, optional): Address of chronyd (Unix socket path or IP:port). If None, will try default connections.

**Returns:**
- A context manager that yields a Chrony object.

**Example:**
```python
import libchrony

with libchrony.connect() as chrony:
    # Use chrony object
    tracking = chrony.get_tracking()
```

### Chrony Class

#### `Chrony(address=None)`

Creates a new connection to chronyd.

**Parameters:**
- `address` (str, optional): Address of chronyd (Unix socket path or IP:port). If None, will try default connections.

**Raises:**
- `ConnectionError`: If connection to chronyd fails.

**Example:**
```python
chrony = libchrony.Chrony("/var/run/chrony/chronyd.sock")
try:
    # Use chrony object
finally:
    chrony.close()
```

#### `close()`

Closes the connection to chronyd.

**Example:**
```python
chrony.close()
```

### Report Functions

#### `get_available_reports()`

Gets a list of all available reports.

**Returns:**
- List of report names.

**Example:**
```python
reports = chrony.get_available_reports()
```

#### `get_record_count(report_name)`

Gets the number of records in a report.

**Parameters:**
- `report_name` (str): Name of the report.

**Returns:**
- Number of records.

**Raises:**
- `RequestError`: If the request fails.
- `ResponseError`: If receiving or processing the response fails.

**Example:**
```python
count = chrony.get_record_count("sources")
```

#### `get_record(report_name, record_index=0)`

Gets a single record from a report.

**Parameters:**
- `report_name` (str): Name of the report.
- `record_index` (int, optional): Index of the record. Default is 0.

**Returns:**
- `Record` object containing the requested record.

**Raises:**
- `RequestError`: If the request fails.
- `ResponseError`: If receiving or processing the response fails.

**Example:**
```python
tracking = chrony.get_record("tracking")
```

#### `get_report(report_name)`

Gets all records from a report.

**Parameters:**
- `report_name` (str): Name of the report.

**Returns:**
- `Report` object containing all records.

**Raises:**
- `RequestError`: If the request fails.
- `ResponseError`: If receiving or processing the response fails.

**Example:**
```python
sources = chrony.get_report("sources")
```

#### `iter_records(report_name)`

Iterates over all records in a report.

**Parameters:**
- `report_name` (str): Name of the report.

**Yields:**
- `Record` objects for each record in the report.

**Raises:**
- `RequestError`: If the request fails.
- `ResponseError`: If receiving or processing the response fails.

**Example:**
```python
for source in chrony.iter_records("sources"):
    print(source["address"])
```

### Convenience Methods for Common Reports

#### `get_tracking()`

Gets the tracking report (current synchronization state).

**Returns:**
- `Record` object containing the tracking report.

**Example:**
```python
tracking = chrony.get_tracking()
print(f"Reference ID: {tracking['reference ID'].value}")
```

#### `get_sources()`

Gets the sources report (time sources).

**Returns:**
- `Report` object containing all source records.

**Example:**
```python
sources = chrony.get_sources()
for source in sources:
    print(f"Source: {source['address'].value}")
```

#### `get_sourcestats()`

Gets the sourcestats report (statistics for time sources).

**Returns:**
- `Report` object containing all sourcestats records.

**Example:**
```python
sourcestats = chrony.get_sourcestats()
```

#### `get_serverstats()`

Gets the serverstats report (server statistics).

**Returns:**
- `Record` object containing the server statistics.

**Example:**
```python
serverstats = chrony.get_serverstats()
```

#### `get_activity()`

Gets the activity report (source activity statistics).

**Returns:**
- `Record` object containing activity statistics.

**Example:**
```python
activity = chrony.get_activity()
print(f"Online sources: {activity['online sources'].value}")
```

#### `get_selectdata()`

Gets the selectdata report (source selection data).

**Returns:**
- `Report` object containing all selectdata records.

**Example:**
```python
selectdata = chrony.get_selectdata()
```

#### `get_rtcdata()`

Gets the rtcdata report (real-time clock data).

**Returns:**
- `Record` object containing RTC data.

**Example:**
```python
rtcdata = chrony.get_rtcdata()
```

#### `get_smoothing()`

Gets the smoothing report (clock smoothing parameters).

**Returns:**
- `Record` object containing smoothing parameters.

**Example:**
```python
smoothing = chrony.get_smoothing()
```

#### `get_all_reports()`

Gets all available reports.

**Returns:**
- Dictionary mapping report names to `Report` or `Record` objects.

**Example:**
```python
all_reports = chrony.get_all_reports()
tracking = all_reports["tracking"]
```

### Data Classes

#### `Record`

Represents a record from a chrony report.

**Attributes:**
- `report_name` (str): Name of the report.
- `index` (int): Index of the record.
- `fields` (List[FieldValue]): List of field values.

**Methods:**
- `__getitem__(key)`: Get a field by index or name.
- `__iter__()`: Iterate over fields.
- `__len__()`: Get the number of fields.
- `as_dict()`: Convert the record to a dictionary.

**Example:**
```python
tracking = chrony.get_tracking()
ref_id = tracking["reference ID"]
print(f"Reference ID: {ref_id.value}")
```

#### `Report`

Represents a chrony report with multiple records.

**Attributes:**
- `name` (str): Name of the report.
- `records` (List[Record]): List of records.

**Methods:**
- `__getitem__(key)`: Get a record by index.
- `__iter__()`: Iterate over records.
- `__len__()`: Get the number of records.

**Example:**
```python
sources = chrony.get_sources()
for i, source in enumerate(sources):
    print(f"Source {i}: {source['address'].value}")
```

#### `FieldValue`

Represents a field value with metadata.

**Attributes:**
- `name` (str): Name of the field.
- `value` (Any): Value of the field.
- `type` (ChronyFieldType): Type of the field.
- `content` (ChronyFieldContent): Content type of the field.

**Methods:**
- `__str__()`: Get a string representation of the value.
- `unit` (property): Get the unit for the field content.

**Example:**
```python
offset = tracking["current correction"]
print(f"Current correction: {offset.value} {offset.unit}")
```

### Exceptions

#### `ChronyException`

Base exception for all chrony-related errors.

#### `ConnectionError`

Exception raised for connection-related errors.

#### `RequestError`

Exception raised for request-related errors.

#### `ResponseError`

Exception raised for response-related errors.

#### `AuthorizationError`

Exception raised for authorization-related errors.

## Complete Example

```python
import libchrony

try:
    with libchrony.connect() as chrony:
        # Get tracking information
        tracking = chrony.get_tracking()
        print(f"Reference ID: {tracking['reference ID'].value}")
        print(f"Stratum: {tracking['stratum'].value}")
        
        # Get sources information
        sources = chrony.get_sources()
        print(f"Number of sources: {len(sources)}")
        
        for i, source in enumerate(sources):
            print(f"Source {i+1}:")
            print(f"  Address: {source['address'].value}")
            print(f"  State: {source['state'].value}")
            print(f"  Stratum: {source['stratum'].value}")
        
        # Get activity information
        activity = chrony.get_activity()
        print(f"Online sources: {activity['online sources'].value}")
        print(f"Offline sources: {activity['offline sources'].value}")

except libchrony.ConnectionError as e:
    print(f"Connection error: {e}")
except libchrony.ChronyException as e:
    print(f"Chrony error: {e}")
```
