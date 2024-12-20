## Supported protocols

This file contains an overview what the KUKSA Server and databroker each supports. It focuses on gRPC and VISS support and also what feeders are supported.

| Protocol                 | KUKSA server | KUKSA databroker |
| ------------------------ | :----------: | :--------------: |
| VISS V1                  |      -       |        -         |
| VISS V2                  |     x/-      |       x/-        |
| gRPC (kuksa)             |      x       |        -         |
| gRPC (kuksa.val.v2)      |      -       |        x         |
| gRPC (kuksa.val.v1)      |      -       |        x         |
| gRPC (sdv.databroker.v1) |      -       |        x         |

x = supported; x/- = partially supported; - = not supported

### VISSv2 support (websocket transport)

| Feature                   |  KUKSA server   | KUKSA databroker |
| ------------------------- | :-------------: | :--------------: |
| Read                      |                 |                  |
| - Authorized Read         | x<sup>1,2</sup> |        x         |
| - Search Read             |        -        |        -         |
| - History Read            |        -        |        -         |
| - Static Metadata Read    |        -        |        x         |
| - Dynamic Metadata Read   |        -        |        -         |
| Update                    |                 |                  |
| - Authorized Update       | x<sup>1,2</sup> |        x         |
| Subscribe                 |                 |                  |
| - Authorized Subscribe    | x<sup>1,2</sup> |        x         |
| - Curve Logging Subscribe |        -        |        -         |
| - Range Subscribe         |        -        |        -         |
| - Change Subscribe        |        -        |        -         |
| Unsubscribe               |        x        |        x         |
| Subscription              |        x        |        x         |
| Error messages            |        x        |        x         |
| Timestamps                |        x        |        x         |

x = supported

x<sup>1</sup> Authorization is done using a non-standard standalone call which is incompatible with standards compliant clients.

x<sup>2</sup> Relies on the non-standard `attribute` values which doesn't work with standards compliant clients.

For a more detailed view of the supported JSON-schemas [click here](https://github.com/eclipse/kuksa.val/blob/master/kuksa-val-server/include/VSSRequestJsonSchema.hpp)

### sdv.databroker.v1 in KUKSA Databroker

To enable the legacy `sdv.databroker.v1` API you must start Databroker with the `--enable-databroker-v1` argument.

### VISSv2 in KUKSA Databroker

KUKSA databroker aims to provide a standards compliant implementation of VISSv2 (using the websocket transport).

It supports authorization using the access token format specified in [authorization.md](../authorization.md).

VISSv2 support in databroker is included by building it with the `viss` feature flag.

```shell
$ cargo build --features viss
```

The `enable-viss` flag must be provided at startup in order to enable the VISSv2 websocket interface.

```shell
$ databroker --enable-viss
```

The arguments `--viss-address` and `--viss-port` can be used if you want to use a different address or port than default for VISS.
If not specified, the address `127.0.0.1` will be used unless otherwise specified with `--address`, and the port 8090 will be used.

Using kuksa-client, the VISSv2 interface of databroker is available using the `ws` protocol in the uri, i.e.:

```shell
$ kuksa-client ws://127.0.0.1:8090
```

TLS is currently not supported.

### KUKSA databroker gRPC API

The VISS Standard is not applicable for gRPC protocols. Here is an overview what the gRPC API in KUKSA databroker is capable of:

- Read: Reading VSS datapoints
  - Reading value for actuators (for kuksa.val.v1 current or target values)
  - Reading some metadata information from VSS datapoints
- Write: Writing VSS datapoints
  - Writing sensor values
  - Writing value for actuators (for kuksa.val.v1 current or target value)
  - Soon: Writing some metadata information from VSS datapoints
- Subscription: Subscribing VSS datapoints
  - Subscribing sensor values
  - Subscribing value for actuators (for kuksa.val.v1 current or target value)
