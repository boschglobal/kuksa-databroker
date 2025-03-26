#!/usr/bin/env python3
import grpc
import time
import os
import sys
import threading
import queue
import pytest
import logging

from pytest_bdd import given, when, then,parsers

from gen_proto.kuksa.val.v2 import val_pb2_grpc;
from gen_proto.kuksa.val.v2 import val_pb2;
from gen_proto.kuksa.val.v2 import types_pb2;

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ProviderValV2:
    def __init__(self,pytestconfig):
        """
        Initializes the gRPC channel, stub, and internal data structures.
        """
        self.pytestconfig=pytestconfig
        #self.address = f"{host}:{port}"
        #if secure:
        #    # Configure secure credentials as needed.
        #    credentials = grpc.ssl_channel_credentials()
        #    self.channel = grpc.secure_channel(self.address, credentials)
        #else:
        self.channel = grpc.insecure_channel(self.pytestconfig.getini('grpc_base_url'))
        self.stub = val_pb2_grpc.VALStub(self.channel)

        # For the bidirectional stream
        self._request_queue = queue.Queue()
        self._response_queue = queue.Queue()
        self._shutdown = False
        # Default frequency (iterations per second) for checking/sending messages.
        self._frequency = 1000.0
        self._send_interval = 1.0 / self._frequency

        # Thread for handling the streaming call.
        self._stream_thread = None

        # Map for storing metadata by int id.
        self.metadata_map = {}
        self.start_stream()

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

    def set_frequency(self, frequency):
        """
        Adjusts the frequency (iterations per second) at which the stream loop
        checks for new messages.
        :param frequency: New frequency in Hz (iterations per second).
        """
        if frequency <= 0:
            raise ValueError("Frequency must be positive.")
        self._frequency = frequency
        self._send_interval = 1.0 / frequency
        print(f"Frequency set to {frequency} Hz.")

    def _get_queued_message(self):
        """
        Get queued message
        """
        while not self._shutdown:
            try:
                # Wait for a message from the queue.
                message = self._request_queue.get(timeout=self._send_interval)
                yield message
            except queue.Empty:
                # No message available in the interval; continue waiting.
                continue

    def _stream_loop(self):
        """
        Runs the bidirectional streaming call in a loop. Sends messages from the queue
        and processes responses.
        """
        try:
            stream = self.stub.OpenProviderStream(self._get_queued_message())
            for response in stream:
                # Process responses from the server.
                if response.HasField("provide_actuation_response"):
                    print("Received ProvideActuationResponse")
                elif response.HasField("publish_values_response"):
                    print("Received PublishValuesResponse")
                elif response.HasField("provide_signal_response"):
                    self._response_queue.put(response)
                    #print("Received ProvideSignalResponse {}", response)
                elif response.HasField("batch_actuate_stream_request"):
                    self._response_queue.put(response)
                elif response.HasField("update_filter_request"):
                    self._response_queue.put(response)
                elif response.HasField("get_provider_value_request"):
                    print("before queue size: ", self._response_queue.qsize())
                    self._response_queue.put(response)
                    print("queue size: ", self._response_queue.qsize())
                    print("response: ", response)
                else:
                    print("Received unknown response:", response)
                # Check shutdown flag between responses.
                if self._shutdown:
                    break
        except grpc.RpcError as e:
            print(f"OpenProviderStream RPC failed: {e.code()} - {e.details()}")

    def start_stream(self):
        if self._stream_thread and self._stream_thread.is_alive():
            return
        self._shutdown = False
        self._stream_thread = threading.Thread(target=self._stream_loop, daemon=True)
        self._stream_thread.start()

    def shutdown(self):
        self._shutdown = True
        if self._stream_thread:
            self._stream_thread.join()
        self.disconnect()
    # --- Methods for sending various types of messages through the same stream ---

    def send_provide_actuation(self, actuator_identifiers):
        req = val_pb2.ProvideActuationRequest(
            actuator_identifiers=actuator_identifiers
        )
        msg = val_pb2.OpenProviderStreamRequest(provide_actuation_request=req)
        self._request_queue.put(msg)

    def send_publish_values(self, request_id, data_points):
        req = val_pb2.PublishValuesRequest(
            request_id=request_id,
            data_points=data_points
        )
        msg = val_pb2.OpenProviderStreamRequest(publish_values_request=req)
        self._request_queue.put(msg)

    def send_provide_signal(self, signals_sample_intervals):
        req = val_pb2.ProvideSignalRequest(
            signals_sample_intervals=signals_sample_intervals
        )
        msg = val_pb2.OpenProviderStreamRequest(provide_signal_request=req)
        self._request_queue.put(msg)

    def send_provider_error_indication(self, provider_error):
        req = val_pb2.ProviderErrorIndication(
            provider_error=provider_error
        )
        msg = val_pb2.OpenProviderStreamRequest(provider_error_indication=req)
        self._request_queue.put(msg)

    def send_provider_get_value_response(self):

        datapoint_value = types_pb2.Value(
            float=2.0  # Directly set the float field (not FLOAT_FIELD_NUMBER)
        )
        datapoint = types_pb2.Datapoint(value=datapoint_value)

        # Use a dictionary for the map<int32, Datapoint> field
        req = val_pb2.GetProviderValueResponse(
            request_id=123,  # Don't forget the required uint32 request_id
            entries={
                882: datapoint  # Key must be int32, value must be a Datapoint instance
            }
        )
        msg = val_pb2.OpenProviderStreamRequest(get_provider_value_response=req)
        self._request_queue.put(msg)
    # --- Methods for receiving various types of request through the same stream ---

    def received_provide_actuation_response(self, request):
        response = self._response_queue.get()
        if response.HasField("provide_actuation_response"):
            return response
        else:
            None

    def received_publish_values_response(self, request):
        response = self._response_queue.get()
        if response.HasField("publish_values_response"):
            return response
        else:
            None

    def received_provide_signal_response(self, request):
        response = self._response_queue.get()
        if response.HasField("provide_signal_response"):
            return response
        else:
            None

    def received_batch_actuate_stream_request(self, request):
        response = self._response_queue.get()
        if response.HasField("batch_actuate_stream_request"):
            return response
        else:
            None

    def received_update_filter_request(self, request):
        response = self._response_queue.get()
        if response.HasField("update_filter_request"):
            return response
        else:
            None

    def received_get_provider_value_request(self):
        print("received_get_provider_value_request queue size: ", self._response_queue.qsize())
        response = self._response_queue.get()
        print(response)
        response = self._response_queue.get()

        if response.HasField("get_provider_value_request"):
            return response
        else:
            None

@pytest.fixture
def connected_provider(request,pytestconfig):
    connected_provider = ProviderValV2(pytestconfig)
    def cleanup():
        connected_provider.disconnect()
    request.addfinalizer(cleanup)
    return connected_provider

@given("the Provider connected via gRPC")
def grpc_kuksa_provider_via_grpc(connected_provider):
    metadata = connected_provider.list_metadata(root_branch="Vehicle.*")
    #if metadata is not None:
    #    for key, meta in metadata.items():
    #        print(f"  ID: {key}, Metadata: {meta}")

@when(parsers.parse('Provider claims the signal "{path}"'))
def claim_signal(connected_provider, path):
    sample_intervals = {882: types_pb2.SampleInterval(interval_ms=10)}
    connected_provider.send_provide_signal(signals_sample_intervals=sample_intervals)

@when(parsers.parse('Provider disconnects'))
def disconnect(connected_provider):
    time.sleep(2)
    connected_provider.disconnect()

@then(parsers.parse('Provider should receive a valid read request for path "{path}"'))
def receive_get_value_request(connected_provider, path):
    time.sleep(3) # sleep to wait to receiver the response
    response = connected_provider.received_get_provider_value_request()
    print("RESPONSE ", response)
    assert response.get_provider_value_request.signal_ids[0]==882
    connected_provider.disconnect()

@then(parsers.parse('Provider should send valid value for path "{path}"'))
def provider_send_response(connected_provider, path):
    logger.debug("\n\n\n\provider_send_response(connected_provider\n\n\n")
    print("def provider_send_response(connected_provider, path):", path, "\n\n\n")
    connected_provider.send_provider_get_value_response()


# Example usage:
def main():
    class DummyConfig:
        def getini(self, key):
            # Replace with your actual gRPC base URL.
            return "localhost:55555"

    dummy_config = DummyConfig()
    provider = ProviderValV2(dummy_config)

    # Retrieve and store metadata.
    #metadata = client.list_metadata(root_branch="Vehicle")
    #if metadata is not None:
        #print("Stored metadata (by id):")
        #for key, meta in metadata.items():
            #print(f"  ID: {key}, Metadata: {meta}")

    # Step 2: Start the bidirectional stream
    #provider.start_stream()

    # Step 3: Set frequency to 2 Hz (2 messages per second)
    provider.set_frequency(2.0)

    # Step 4: Send ProvideActuationRequest
    #client.send_provide_actuation(actuator_identifiers=["example_actuator_1", "example_actuator_2"])

    # Step 5: Send PublishValuesRequest
    #datapoint = val_pb2.Datapoint()
    #datapoint.value_str = "sensor_value"
    #client.send_publish_values(request_id=1, data_points={1001: datapoint})

    # Step 6: Send BatchActuateStreamResponse
    #signal_id = val_pb2.SignalId(name="test_signal")
    #error = val_pb2.Error(code=0, message="No error")
    #client.send_batch_actuate_stream_response(signal_id=signal_id, error=error)

    # Step 7: Send ProvideSignalRequest
    sample_intervals = {882: types_pb2.SampleInterval(interval_ms=10)}
    provider.send_provide_signal(signals_sample_intervals=sample_intervals)

    # Step 8: Send UpdateFilterResponse
    #filter_error = val_pb2.Error(code=1, message="Filter updated successfully")
    #client.send_update_filter_response(request_id=2, filter_error=filter_error)

    # Step 9: Send GetProviderValueResponse
    #response_value = val_pb2.GetValueResponse()
    #response_value.value.value_str = "retrieved_value"
    time.sleep(10)

    provider.send_provider_get_value_response()

    # Step 10: Send ProviderErrorIndication
    #provider_error = val_pb2.ProviderError(code=2, message="Sample error occurred")
    #client.send_provider_error_indication(provider_error=provider_error)

    # Step 11: Let the stream run for a while
    time.sleep(1)

    provider.disconnect()
    # Step 12: Shutdown the stream
    # client.shutdown()

if __name__ == "__main__":
    main()
