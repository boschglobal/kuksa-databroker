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


import time
import grpc
import asyncio
import os
import sys
import pytest
import logging

from pytest_bdd import given, when, then, parsers

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import gen_proto  # Assuming this sets up your generated proto modules

from gen_proto.kuksa.val.v2 import val_pb2_grpc
from gen_proto.kuksa.val.v2 import val_pb2
from gen_proto.kuksa.val.v2 import types_pb2

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class AsyncKuksaValV2Client:
    def __init__(self, pytestconfig):
        self.pytestconfig = pytestconfig
        self._response_queue = asyncio.Queue()
        self._client_is_connected = False
        self.metadata_map = {}

    def is_connected(self) -> bool:
        return self._client_is_connected

    async def connect(self):
        self._client_is_connected = True
        # Create an asynchronous insecure channel
        self.channel = grpc.aio.insecure_channel(self.pytestconfig.getini('grpc_base_url'))
        self.stub = val_pb2_grpc.VALStub(self.channel)

    async def disconnect(self):
        if self.channel:
            await self.channel.close()
            # Simulate a short delay after disconnecting
            await asyncio.sleep(2)

    async def list_metadata(self, root_branch="Vehicle"):
        request = val_pb2.ListMetadataRequest(root=root_branch)
        try:
            # Await the asynchronous RPC call
            response = await self.stub.ListMetadata(request)
            for metadata in response.metadata:
                # Assume metadata.id is an int field.
                self.metadata_map[int(metadata.id)] = metadata
            return self.metadata_map
        except grpc.aio.AioRpcError as e:
            print(f"ListMetadata RPC failed: {e.code()} - {e.details()}")
            return None

    async def get_value(self, path):
        request = val_pb2.GetValueRequest(signal_id=types_pb2.SignalID(path=path))
        try:
            response = await self.stub.GetValue(request)
            await self._response_queue.put(response)
        except grpc.aio.AioRpcError as e:
            print(f"GetValue RPC failed: {e.code()} - {e.details()}")
            return None

    async def get_last_response(self):
        return await self._response_queue.get()


# Async pytest fixture that connects the client before tests and disconnects after.
@pytest.fixture
async def connected_client(pytestconfig):
    client = AsyncKuksaValV2Client(pytestconfig)
    await client.connect()
    print("AsyncKuksaValV2Client")
    await client.list_metadata()
    yield client

@given("the Kuksa val v2 client is connected via gRPC")
async def connect(connected_client):
    # The connection is already established by the fixture.
    pass


@pytest.mark.asyncio
@when(parsers.parse('I send a read request with path "{path}"'))
async def send_read_data_point(path):
    asyncio.run(_send_read_data_point(path))  # Wrap async function in `asyncio.run()`

async def _send_read_data_point(path):
    print("send test\n\n\n\n\n\n\n")
    class DummyConfig:
        def getini(self, key):
            return "localhost:55555"  # Replace with actual gRPC URL

    dummy_config = DummyConfig()
    client = AsyncKuksaValV2Client(dummy_config)
    await client.connect()
    await client.get_value(path)  #

@then(parsers.parse('I should receive a valid read response for path "{path}"'))
async def receive_valid_get_response(connected_client, path):
    response = await connected_client.get_last_response()
    print("RESPONSE", response)


# Entry point for manual testing (if needed)
if __name__ == "__main__":
    async def main():
        # Create a dummy pytestconfig object with a getini method for testing.
        class DummyConfig:
            def getini(self, key):
                # Replace with your actual gRPC base URL.
                return "localhost:55555"

        dummy_config = DummyConfig()
        client = AsyncKuksaValV2Client(dummy_config)
        await client.connect()
        metadata = await client.list_metadata()
        #print("Metadata:", metadata)
        # Assume there's a valid path to test
        await client.get_value("Vehicle.Speed")
        response = await client.get_last_response()
        print("Response:", response)
        await client.disconnect()

    asyncio.run(main())
