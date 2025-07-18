#!/usr/bin/env python3
# /********************************************************************************
# * Copyright (c) 2025 Contributors to the Eclipse Foundation
# *
# * See the NOTICE file(s) distributed with this work for additional
# * information regarding copyright ownership.
# *
# * This program and the accompanying materials are made available under the
# * terms of the Apache License 2.0 which is available at
# * http://www.apache.org/licenses/LICENSE-2.0
# *
# * SPDX-License-Identifier: Apache-2.0
# ********************************************************************************/
"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*******************************************************************************
Copyright (c) 2024 Contributors to the Eclipse Foundation

See the NOTICE file(s) distributed with this work for additional
information regarding copyright ownership.

This program and the accompanying materials are made available under the
terms of the Apache License 2.0 which is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0
******************************************************************************

Please do not add optional fields due to older proto3 versions limitations
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _FilterError:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _FilterErrorEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_FilterError.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    FILTER_ERROR_CODE_UNSPECIFIED: _FilterError.ValueType  # 0
    FILTER_ERROR_CODE_UNKNOWN_SINGAL_ID: _FilterError.ValueType  # 1

class FilterError(_FilterError, metaclass=_FilterErrorEnumTypeWrapper): ...

FILTER_ERROR_CODE_UNSPECIFIED: FilterError.ValueType  # 0
FILTER_ERROR_CODE_UNKNOWN_SINGAL_ID: FilterError.ValueType  # 1
global___FilterError = FilterError

class _ProviderError:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ProviderErrorEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ProviderError.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CODE_UNSPECIFIED: _ProviderError.ValueType  # 0
    CODE_NETWORK_ERROR: _ProviderError.ValueType  # 1
    CODE_OVERLOAD: _ProviderError.ValueType  # 2

class ProviderError(_ProviderError, metaclass=_ProviderErrorEnumTypeWrapper):
    """Could be extended in the future with more errors"""

CODE_UNSPECIFIED: ProviderError.ValueType  # 0
CODE_NETWORK_ERROR: ProviderError.ValueType  # 1
CODE_OVERLOAD: ProviderError.ValueType  # 2
global___ProviderError = ProviderError

class _ErrorCode:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ErrorCodeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ErrorCode.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    ERROR_CODE_UNSPECIFIED: _ErrorCode.ValueType  # 0
    """Default value, never to be explicitly set,"""
    ERROR_CODE_OK: _ErrorCode.ValueType  # 1
    ERROR_CODE_INVALID_ARGUMENT: _ErrorCode.ValueType  # 2
    ERROR_CODE_NOT_FOUND: _ErrorCode.ValueType  # 3
    ERROR_CODE_PERMISSION_DENIED: _ErrorCode.ValueType  # 4

class ErrorCode(_ErrorCode, metaclass=_ErrorCodeEnumTypeWrapper): ...

ERROR_CODE_UNSPECIFIED: ErrorCode.ValueType  # 0
"""Default value, never to be explicitly set,"""
ERROR_CODE_OK: ErrorCode.ValueType  # 1
ERROR_CODE_INVALID_ARGUMENT: ErrorCode.ValueType  # 2
ERROR_CODE_NOT_FOUND: ErrorCode.ValueType  # 3
ERROR_CODE_PERMISSION_DENIED: ErrorCode.ValueType  # 4
global___ErrorCode = ErrorCode

class _DataType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _DataTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_DataType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    DATA_TYPE_UNSPECIFIED: _DataType.ValueType  # 0
    DATA_TYPE_STRING: _DataType.ValueType  # 1
    DATA_TYPE_BOOLEAN: _DataType.ValueType  # 2
    DATA_TYPE_INT8: _DataType.ValueType  # 3
    DATA_TYPE_INT16: _DataType.ValueType  # 4
    DATA_TYPE_INT32: _DataType.ValueType  # 5
    DATA_TYPE_INT64: _DataType.ValueType  # 6
    DATA_TYPE_UINT8: _DataType.ValueType  # 7
    DATA_TYPE_UINT16: _DataType.ValueType  # 8
    DATA_TYPE_UINT32: _DataType.ValueType  # 9
    DATA_TYPE_UINT64: _DataType.ValueType  # 10
    DATA_TYPE_FLOAT: _DataType.ValueType  # 11
    DATA_TYPE_DOUBLE: _DataType.ValueType  # 12
    DATA_TYPE_TIMESTAMP: _DataType.ValueType  # 13
    DATA_TYPE_STRING_ARRAY: _DataType.ValueType  # 20
    DATA_TYPE_BOOLEAN_ARRAY: _DataType.ValueType  # 21
    DATA_TYPE_INT8_ARRAY: _DataType.ValueType  # 22
    DATA_TYPE_INT16_ARRAY: _DataType.ValueType  # 23
    DATA_TYPE_INT32_ARRAY: _DataType.ValueType  # 24
    DATA_TYPE_INT64_ARRAY: _DataType.ValueType  # 25
    DATA_TYPE_UINT8_ARRAY: _DataType.ValueType  # 26
    DATA_TYPE_UINT16_ARRAY: _DataType.ValueType  # 27
    DATA_TYPE_UINT32_ARRAY: _DataType.ValueType  # 28
    DATA_TYPE_UINT64_ARRAY: _DataType.ValueType  # 29
    DATA_TYPE_FLOAT_ARRAY: _DataType.ValueType  # 30
    DATA_TYPE_DOUBLE_ARRAY: _DataType.ValueType  # 31
    DATA_TYPE_TIMESTAMP_ARRAY: _DataType.ValueType  # 32

class DataType(_DataType, metaclass=_DataTypeEnumTypeWrapper):
    """VSS Data type of a signal

    Protobuf doesn't support int8, int16, uint8 or uint16.
    These are mapped to int32 and uint32 respectively.
    """

DATA_TYPE_UNSPECIFIED: DataType.ValueType  # 0
DATA_TYPE_STRING: DataType.ValueType  # 1
DATA_TYPE_BOOLEAN: DataType.ValueType  # 2
DATA_TYPE_INT8: DataType.ValueType  # 3
DATA_TYPE_INT16: DataType.ValueType  # 4
DATA_TYPE_INT32: DataType.ValueType  # 5
DATA_TYPE_INT64: DataType.ValueType  # 6
DATA_TYPE_UINT8: DataType.ValueType  # 7
DATA_TYPE_UINT16: DataType.ValueType  # 8
DATA_TYPE_UINT32: DataType.ValueType  # 9
DATA_TYPE_UINT64: DataType.ValueType  # 10
DATA_TYPE_FLOAT: DataType.ValueType  # 11
DATA_TYPE_DOUBLE: DataType.ValueType  # 12
DATA_TYPE_TIMESTAMP: DataType.ValueType  # 13
DATA_TYPE_STRING_ARRAY: DataType.ValueType  # 20
DATA_TYPE_BOOLEAN_ARRAY: DataType.ValueType  # 21
DATA_TYPE_INT8_ARRAY: DataType.ValueType  # 22
DATA_TYPE_INT16_ARRAY: DataType.ValueType  # 23
DATA_TYPE_INT32_ARRAY: DataType.ValueType  # 24
DATA_TYPE_INT64_ARRAY: DataType.ValueType  # 25
DATA_TYPE_UINT8_ARRAY: DataType.ValueType  # 26
DATA_TYPE_UINT16_ARRAY: DataType.ValueType  # 27
DATA_TYPE_UINT32_ARRAY: DataType.ValueType  # 28
DATA_TYPE_UINT64_ARRAY: DataType.ValueType  # 29
DATA_TYPE_FLOAT_ARRAY: DataType.ValueType  # 30
DATA_TYPE_DOUBLE_ARRAY: DataType.ValueType  # 31
DATA_TYPE_TIMESTAMP_ARRAY: DataType.ValueType  # 32
global___DataType = DataType

class _EntryType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _EntryTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_EntryType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    ENTRY_TYPE_UNSPECIFIED: _EntryType.ValueType  # 0
    ENTRY_TYPE_ATTRIBUTE: _EntryType.ValueType  # 1
    ENTRY_TYPE_SENSOR: _EntryType.ValueType  # 2
    ENTRY_TYPE_ACTUATOR: _EntryType.ValueType  # 3

class EntryType(_EntryType, metaclass=_EntryTypeEnumTypeWrapper):
    """Entry type"""

ENTRY_TYPE_UNSPECIFIED: EntryType.ValueType  # 0
ENTRY_TYPE_ATTRIBUTE: EntryType.ValueType  # 1
ENTRY_TYPE_SENSOR: EntryType.ValueType  # 2
ENTRY_TYPE_ACTUATOR: EntryType.ValueType  # 3
global___EntryType = EntryType

@typing.final
class Datapoint(google.protobuf.message.Message):
    """A Datapoint represents a timestamped value.
    The 'value' field can be explicitly 'None', meaning the Datapoint exists but no value is present.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TIMESTAMP_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    @property
    def timestamp(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """The timestamp of the datapoint."""

    @property
    def value(self) -> global___Value:
        """The value associated with the timestamp. If no value is present, this field can be 'None'."""

    def __init__(
        self,
        *,
        timestamp: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        value: global___Value | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["timestamp", b"timestamp", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["timestamp", b"timestamp", "value", b"value"]) -> None: ...

global___Datapoint = Datapoint

@typing.final
class Value(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STRING_FIELD_NUMBER: builtins.int
    BOOL_FIELD_NUMBER: builtins.int
    INT32_FIELD_NUMBER: builtins.int
    INT64_FIELD_NUMBER: builtins.int
    UINT32_FIELD_NUMBER: builtins.int
    UINT64_FIELD_NUMBER: builtins.int
    FLOAT_FIELD_NUMBER: builtins.int
    DOUBLE_FIELD_NUMBER: builtins.int
    STRING_ARRAY_FIELD_NUMBER: builtins.int
    BOOL_ARRAY_FIELD_NUMBER: builtins.int
    INT32_ARRAY_FIELD_NUMBER: builtins.int
    INT64_ARRAY_FIELD_NUMBER: builtins.int
    UINT32_ARRAY_FIELD_NUMBER: builtins.int
    UINT64_ARRAY_FIELD_NUMBER: builtins.int
    FLOAT_ARRAY_FIELD_NUMBER: builtins.int
    DOUBLE_ARRAY_FIELD_NUMBER: builtins.int
    string: builtins.str
    bool: builtins.bool
    int32: builtins.int
    int64: builtins.int
    uint32: builtins.int
    uint64: builtins.int
    float: builtins.float
    double: builtins.float
    @property
    def string_array(self) -> global___StringArray: ...
    @property
    def bool_array(self) -> global___BoolArray: ...
    @property
    def int32_array(self) -> global___Int32Array: ...
    @property
    def int64_array(self) -> global___Int64Array: ...
    @property
    def uint32_array(self) -> global___Uint32Array: ...
    @property
    def uint64_array(self) -> global___Uint64Array: ...
    @property
    def float_array(self) -> global___FloatArray: ...
    @property
    def double_array(self) -> global___DoubleArray: ...
    def __init__(
        self,
        *,
        string: builtins.str = ...,
        bool: builtins.bool = ...,
        int32: builtins.int = ...,
        int64: builtins.int = ...,
        uint32: builtins.int = ...,
        uint64: builtins.int = ...,
        float: builtins.float = ...,
        double: builtins.float = ...,
        string_array: global___StringArray | None = ...,
        bool_array: global___BoolArray | None = ...,
        int32_array: global___Int32Array | None = ...,
        int64_array: global___Int64Array | None = ...,
        uint32_array: global___Uint32Array | None = ...,
        uint64_array: global___Uint64Array | None = ...,
        float_array: global___FloatArray | None = ...,
        double_array: global___DoubleArray | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["bool", b"bool", "bool_array", b"bool_array", "double", b"double", "double_array", b"double_array", "float", b"float", "float_array", b"float_array", "int32", b"int32", "int32_array", b"int32_array", "int64", b"int64", "int64_array", b"int64_array", "string", b"string", "string_array", b"string_array", "typed_value", b"typed_value", "uint32", b"uint32", "uint32_array", b"uint32_array", "uint64", b"uint64", "uint64_array", b"uint64_array"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["bool", b"bool", "bool_array", b"bool_array", "double", b"double", "double_array", b"double_array", "float", b"float", "float_array", b"float_array", "int32", b"int32", "int32_array", b"int32_array", "int64", b"int64", "int64_array", b"int64_array", "string", b"string", "string_array", b"string_array", "typed_value", b"typed_value", "uint32", b"uint32", "uint32_array", b"uint32_array", "uint64", b"uint64", "uint64_array", b"uint64_array"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["typed_value", b"typed_value"]) -> typing.Literal["string", "bool", "int32", "int64", "uint32", "uint64", "float", "double", "string_array", "bool_array", "int32_array", "int64_array", "uint32_array", "uint64_array", "float_array", "double_array"] | None: ...

global___Value = Value

@typing.final
class SampleInterval(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INTERVAL_MS_FIELD_NUMBER: builtins.int
    interval_ms: builtins.int
    def __init__(
        self,
        *,
        interval_ms: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["interval_ms", b"interval_ms"]) -> None: ...

global___SampleInterval = SampleInterval

@typing.final
class Filter(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DURATION_MS_FIELD_NUMBER: builtins.int
    MIN_SAMPLE_INTERVAL_FIELD_NUMBER: builtins.int
    duration_ms: builtins.int
    """Duration of the active call. If it is not set, call will last for ever."""
    @property
    def min_sample_interval(self) -> global___SampleInterval:
        """Min desired sample update interval."""

    def __init__(
        self,
        *,
        duration_ms: builtins.int = ...,
        min_sample_interval: global___SampleInterval | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["min_sample_interval", b"min_sample_interval"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["duration_ms", b"duration_ms", "min_sample_interval", b"min_sample_interval"]) -> None: ...

global___Filter = Filter

@typing.final
class SignalID(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    id: builtins.int
    """Numeric identifier to the signal
    As of today Databroker assigns arbitrary unique numbers to each registered signal
    at startup, meaning that identifiers may change after restarting Databroker.
    A mechanism for static identifiers may be introduced in the future.
    """
    path: builtins.str
    """Full VSS-style path to a specific signal, like "Vehicle.Speed"
    Wildcards and paths to branches are not supported.
    The given path must be known by the Databroker.
    """
    def __init__(
        self,
        *,
        id: builtins.int = ...,
        path: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["id", b"id", "path", b"path", "signal", b"signal"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["id", b"id", "path", b"path", "signal", b"signal"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["signal", b"signal"]) -> typing.Literal["id", "path"] | None: ...

global___SignalID = SignalID

@typing.final
class Error(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    code: global___ErrorCode.ValueType
    message: builtins.str
    def __init__(
        self,
        *,
        code: global___ErrorCode.ValueType = ...,
        message: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["code", b"code", "message", b"message"]) -> None: ...

global___Error = Error

@typing.final
class Metadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PATH_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    DATA_TYPE_FIELD_NUMBER: builtins.int
    ENTRY_TYPE_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    COMMENT_FIELD_NUMBER: builtins.int
    DEPRECATION_FIELD_NUMBER: builtins.int
    UNIT_FIELD_NUMBER: builtins.int
    ALLOWED_VALUES_FIELD_NUMBER: builtins.int
    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    MIN_SAMPLE_INTERVAL_FIELD_NUMBER: builtins.int
    path: builtins.str
    """Full dot notated path for the signal"""
    id: builtins.int
    """ID field"""
    data_type: global___DataType.ValueType
    """Data type
    The VSS data type of the entry (i.e. the value, min, max etc).

    NOTE: protobuf doesn't have int8, int16, uint8 or uint16 which means
    that these values must be serialized as int32 and uint32 respectively.
    """
    entry_type: global___EntryType.ValueType
    """Entry type"""
    description: builtins.str
    """Description
    Describes the meaning and content of the entry.
    """
    comment: builtins.str
    """Comment
    A comment can be used to provide additional informal information
    on a entry.
    """
    deprecation: builtins.str
    """Deprecation
    Whether this entry is deprecated. Can contain recommendations of what
    to use instead.
    """
    unit: builtins.str
    """Unit
    The unit of measurement
    """
    @property
    def allowed_values(self) -> global___Value:
        """Value restrictions checked/enforced by Databroker
        Must be of array type
        """

    @property
    def min(self) -> global___Value: ...
    @property
    def max(self) -> global___Value: ...
    @property
    def min_sample_interval(self) -> global___SampleInterval:
        """Minimum sample interval at which its provider can publish the signal value"""

    def __init__(
        self,
        *,
        path: builtins.str = ...,
        id: builtins.int = ...,
        data_type: global___DataType.ValueType = ...,
        entry_type: global___EntryType.ValueType = ...,
        description: builtins.str = ...,
        comment: builtins.str = ...,
        deprecation: builtins.str = ...,
        unit: builtins.str = ...,
        allowed_values: global___Value | None = ...,
        min: global___Value | None = ...,
        max: global___Value | None = ...,
        min_sample_interval: global___SampleInterval | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["allowed_values", b"allowed_values", "max", b"max", "min", b"min", "min_sample_interval", b"min_sample_interval"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["allowed_values", b"allowed_values", "comment", b"comment", "data_type", b"data_type", "deprecation", b"deprecation", "description", b"description", "entry_type", b"entry_type", "id", b"id", "max", b"max", "min", b"min", "min_sample_interval", b"min_sample_interval", "path", b"path", "unit", b"unit"]) -> None: ...

global___Metadata = Metadata

@typing.final
class StringArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["values", b"values"]) -> None: ...

global___StringArray = StringArray

@typing.final
class BoolArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bool]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.bool] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["values", b"values"]) -> None: ...

global___BoolArray = BoolArray

@typing.final
class Int32Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["values", b"values"]) -> None: ...

global___Int32Array = Int32Array

@typing.final
class Int64Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["values", b"values"]) -> None: ...

global___Int64Array = Int64Array

@typing.final
class Uint32Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["values", b"values"]) -> None: ...

global___Uint32Array = Uint32Array

@typing.final
class Uint64Array(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["values", b"values"]) -> None: ...

global___Uint64Array = Uint64Array

@typing.final
class FloatArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.float] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["values", b"values"]) -> None: ...

global___FloatArray = FloatArray

@typing.final
class DoubleArray(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    VALUES_FIELD_NUMBER: builtins.int
    @property
    def values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(
        self,
        *,
        values: collections.abc.Iterable[builtins.float] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["values", b"values"]) -> None: ...

global___DoubleArray = DoubleArray
