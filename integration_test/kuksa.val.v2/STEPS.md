# Step Definitions

The steps in the test scenarios follow the following Gherkin syntax:

## Parameters

> _VSS Path_: A VSS data point path in the "`Vehicle.Branch.Leaf`" syntax.

## Given

> Given the databroker server is running

The client will test that the databroker server is up and running.

> Given the Kuksa val v2 client is connected via gRPC

The client will connect to databroker server using the gRPC channel.

> Given the Provider connected via gRPC

The provider kuksa val v2 will connect to the Databroker using gRPC.

## When

> When I send a read request with path "_VSS Path_"

Get a value of a data pointo once.

> When Provider claims the signal "_VSS Path_"

  Provider will provide the values for the claimed signal

> When KuksaValV2 client disconnects

  Kuska clien disconnects

> When Provider claims the signal "_VSS Path_"

  Provider will provide the values for the claimed signal

> When Provider disconnects

  Provider disconnects

## Then

> Then I should receive a valid response

Validate the server response to be a successful response, e.g. no error.

> Then I should receive a valid read response for path "_VSS Path_"

Server response is valid and a response to a read request.

> Then Provider should receive a valid read request for path "_VSS Path_"

Provider should receive a request path from databroker

> Then Provider should send valid value for path "_VSS Path_"

Provider should send a valie value for the path