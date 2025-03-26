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

import grpc
import time
import os
import sys
import threading
import queue
import pytest
import logging

from pytest_bdd import given, when, then,parsers

import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import gen_proto;

from gen_proto.kuksa.val.v2 import val_pb2_grpc;
from gen_proto.kuksa.val.v2 import val_pb2;
from gen_proto.kuksa.val.v2 import types_pb2;

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
# logger = logging.getLogger(__name__)

class KuksaValV2Client:

    def __init__(self, pytestconfig):
        self.pytestconfig = pytestconfig
        self._request_queue = queue.Queue()
        self._response_queue = queue.Queue()
        self._client_is_connected = False
        self.metadata_map = {}

    def is_connected(self)-> bool:
        return self._client_is_connected

    def connect(self):
        self._client_is_connected = True
        self.channel = grpc.insecure_channel(self.pytestconfig.getini('grpc_base_url'))
        self.stub = val_pb2_grpc.VALStub(self.channel)

    def disconnect(self):
        if self.channel:
            self.channel.close()
            time.sleep(2)

    def list_metadata(self, root_branch="Vehicle"):
        request = val_pb2.ListMetadataRequest(root=root_branch)
        try:
            response = self.stub.ListMetadata(request)
            for metadata in response.metadata:
                # Assume metadata.id is an int field.
                self.metadata_map[int(metadata.id)] = metadata
            return self.metadata_map
        except grpc.RpcError as e:
            print(f"ListMetadata RPC failed: {e.code()} - {e.details()}")
            return None

    def get_value(self, path):
        request = val_pb2.GetValueRequest(signal_id=types_pb2.SignalID(path=path))
        try:
            response = self.stub.GetValue(request)
            self._response_queue.put(response)
        except grpc.RpcError as e:
            print(f"Get value RPC failed: {e.code()} - {e.details()}")
            return None

    def get_last_response(self):
        return self._response_queue.get()

@pytest.fixture
def connected_client(pytestconfig):
    connected_client = KuksaValV2Client(pytestconfig)
    return connected_client

@when(parsers.parse('KuksaValV2 client disconnects'))
def disconnect(connected_client):
    time.sleep(2)
    connected_client.disconnect()

@given("the Kuksa val v2 client is connected via gRPC")
def connect(connected_client):
    #logger.debug("Connecting via gRPC")
    connected_client.connect()
    connected_client.list_metadata()

@when(parsers.parse('I send a read request with path "{path}"'))
def send_read_data_point(connected_client, path):
    connected_client.get_value(path)

@then(parsers.parse('I should receive a valid read response for path "{path}"'))
def receive_valid_get_response(connected_client, path):
    response = connected_client.get_last_response()
    print("RESPONSE ", response)



# # Entry point for manual testing (if needed)
if __name__ == "__main__":
    def main():
        # Create a dummy pytestconfig object with a getini method for testing.
        class DummyConfig:
            def getini(self, key):
                # Replace with your actual gRPC base URL.
                return "localhost:55555"

        dummy_config = DummyConfig()
        client = KuksaValV2Client(dummy_config)
        client.connect()
        #metadata = client.list_metadata()
        #print("Metadata:", metadata)
        # Assume there's a valid path to test
        client.get_value("Vehicle.Speed")
        response = client.get_last_response()
        print("Response: " , response)
        client.disconnect()
        #response = await client.get_last_response()
        #print("Response:", response)
        #await client.disconnect()

    main()
