#
# https://w3c.github.io/automotive/spec/VISSv2_Core.html#read
#

Feature: VISS v2 Compliance Testing - Basic

  Background:
    Given the Provider connected via gRPC

  # 5.1.2 Read request
  # The VISS server must support read requests to retrieve data from a valid path.
  @MustHave
  Scenario: Read a valid data path in kuksavalv2
    When Provider claims the signal "Vehicle.Speed"
    When I send a read request with path "Vehicle.Speed"
    Then Provider should receive a valid read request for path "Vehicle.Speed"
    When Provider disconnects
    When KuksaValV2 client disconnects