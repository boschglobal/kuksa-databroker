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
Copyright (c) 2022 Contributors to the Eclipse Foundation

See the NOTICE file(s) distributed with this work for additional
information regarding copyright ownership.

This program and the accompanying materials are made available under the
terms of the Apache License 2.0 which is available at
http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0
******************************************************************************
"""

import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import kuksa.val.v1.types_pb2
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class EntryRequest(google.protobuf.message.Message):
    """Define which data we want"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PATH_FIELD_NUMBER: builtins.int
    VIEW_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    path: builtins.str
    view: kuksa.val.v1.types_pb2.View.ValueType
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[kuksa.val.v1.types_pb2.Field.ValueType]: ...
    def __init__(
        self,
        *,
        path: builtins.str = ...,
        view: kuksa.val.v1.types_pb2.View.ValueType = ...,
        fields: collections.abc.Iterable[kuksa.val.v1.types_pb2.Field.ValueType] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["fields", b"fields", "path", b"path", "view", b"view"]) -> None: ...

global___EntryRequest = EntryRequest

@typing.final
class GetRequest(google.protobuf.message.Message):
    """Request a set of entries."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ENTRIES_FIELD_NUMBER: builtins.int
    @property
    def entries(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___EntryRequest]: ...
    def __init__(
        self,
        *,
        entries: collections.abc.Iterable[global___EntryRequest] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["entries", b"entries"]) -> None: ...

global___GetRequest = GetRequest

@typing.final
class GetResponse(google.protobuf.message.Message):
    """Global errors are specified in `error`.
    Errors for individual entries are specified in `errors`.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ENTRIES_FIELD_NUMBER: builtins.int
    ERRORS_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    @property
    def entries(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[kuksa.val.v1.types_pb2.DataEntry]: ...
    @property
    def errors(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[kuksa.val.v1.types_pb2.DataEntryError]: ...
    @property
    def error(self) -> kuksa.val.v1.types_pb2.Error: ...
    def __init__(
        self,
        *,
        entries: collections.abc.Iterable[kuksa.val.v1.types_pb2.DataEntry] | None = ...,
        errors: collections.abc.Iterable[kuksa.val.v1.types_pb2.DataEntryError] | None = ...,
        error: kuksa.val.v1.types_pb2.Error | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["error", b"error"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["entries", b"entries", "error", b"error", "errors", b"errors"]) -> None: ...

global___GetResponse = GetResponse

@typing.final
class EntryUpdate(google.protobuf.message.Message):
    """Define the data we want to set"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ENTRY_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    @property
    def entry(self) -> kuksa.val.v1.types_pb2.DataEntry: ...
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[kuksa.val.v1.types_pb2.Field.ValueType]: ...
    def __init__(
        self,
        *,
        entry: kuksa.val.v1.types_pb2.DataEntry | None = ...,
        fields: collections.abc.Iterable[kuksa.val.v1.types_pb2.Field.ValueType] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["entry", b"entry"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["entry", b"entry", "fields", b"fields"]) -> None: ...

global___EntryUpdate = EntryUpdate

@typing.final
class SetRequest(google.protobuf.message.Message):
    """A list of entries to be updated"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UPDATES_FIELD_NUMBER: builtins.int
    @property
    def updates(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___EntryUpdate]: ...
    def __init__(
        self,
        *,
        updates: collections.abc.Iterable[global___EntryUpdate] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["updates", b"updates"]) -> None: ...

global___SetRequest = SetRequest

@typing.final
class SetResponse(google.protobuf.message.Message):
    """Global errors are specified in `error`.
    Errors for individual entries are specified in `errors`.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ERROR_FIELD_NUMBER: builtins.int
    ERRORS_FIELD_NUMBER: builtins.int
    @property
    def error(self) -> kuksa.val.v1.types_pb2.Error: ...
    @property
    def errors(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[kuksa.val.v1.types_pb2.DataEntryError]: ...
    def __init__(
        self,
        *,
        error: kuksa.val.v1.types_pb2.Error | None = ...,
        errors: collections.abc.Iterable[kuksa.val.v1.types_pb2.DataEntryError] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["error", b"error"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["error", b"error", "errors", b"errors"]) -> None: ...

global___SetResponse = SetResponse

@typing.final
class StreamedUpdateRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UPDATES_FIELD_NUMBER: builtins.int
    @property
    def updates(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___EntryUpdate]: ...
    def __init__(
        self,
        *,
        updates: collections.abc.Iterable[global___EntryUpdate] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["updates", b"updates"]) -> None: ...

global___StreamedUpdateRequest = StreamedUpdateRequest

@typing.final
class StreamedUpdateResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ERROR_FIELD_NUMBER: builtins.int
    ERRORS_FIELD_NUMBER: builtins.int
    @property
    def error(self) -> kuksa.val.v1.types_pb2.Error: ...
    @property
    def errors(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[kuksa.val.v1.types_pb2.DataEntryError]: ...
    def __init__(
        self,
        *,
        error: kuksa.val.v1.types_pb2.Error | None = ...,
        errors: collections.abc.Iterable[kuksa.val.v1.types_pb2.DataEntryError] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["error", b"error"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["error", b"error", "errors", b"errors"]) -> None: ...

global___StreamedUpdateResponse = StreamedUpdateResponse

@typing.final
class SubscribeEntry(google.protobuf.message.Message):
    """Define what to subscribe to"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PATH_FIELD_NUMBER: builtins.int
    VIEW_FIELD_NUMBER: builtins.int
    FIELDS_FIELD_NUMBER: builtins.int
    path: builtins.str
    view: kuksa.val.v1.types_pb2.View.ValueType
    @property
    def fields(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[kuksa.val.v1.types_pb2.Field.ValueType]: ...
    def __init__(
        self,
        *,
        path: builtins.str = ...,
        view: kuksa.val.v1.types_pb2.View.ValueType = ...,
        fields: collections.abc.Iterable[kuksa.val.v1.types_pb2.Field.ValueType] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["fields", b"fields", "path", b"path", "view", b"view"]) -> None: ...

global___SubscribeEntry = SubscribeEntry

@typing.final
class SubscribeRequest(google.protobuf.message.Message):
    """Subscribe to changes in datapoints."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ENTRIES_FIELD_NUMBER: builtins.int
    @property
    def entries(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SubscribeEntry]: ...
    def __init__(
        self,
        *,
        entries: collections.abc.Iterable[global___SubscribeEntry] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["entries", b"entries"]) -> None: ...

global___SubscribeRequest = SubscribeRequest

@typing.final
class SubscribeResponse(google.protobuf.message.Message):
    """A subscription response"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UPDATES_FIELD_NUMBER: builtins.int
    @property
    def updates(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___EntryUpdate]: ...
    def __init__(
        self,
        *,
        updates: collections.abc.Iterable[global___EntryUpdate] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["updates", b"updates"]) -> None: ...

global___SubscribeResponse = SubscribeResponse

@typing.final
class GetServerInfoRequest(google.protobuf.message.Message):
    """Nothing yet"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___GetServerInfoRequest = GetServerInfoRequest

@typing.final
class GetServerInfoResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    VERSION_FIELD_NUMBER: builtins.int
    name: builtins.str
    version: builtins.str
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        version: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["name", b"name", "version", b"version"]) -> None: ...

global___GetServerInfoResponse = GetServerInfoResponse
