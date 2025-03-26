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

from pytest_bdd import scenarios
from test_steps.async_v2_grpc_client import *  # Import step definitions
from provider import *  # Import provider definition
import os

# Point to the feature file
scenarios("../features/kuksa_val_v2_basic.feature")
