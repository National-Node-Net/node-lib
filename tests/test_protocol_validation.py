# SPDX-License-Identifier: Apache-2.0
# Originally developed by Telicent Ltd.; subsequently adapted, enhanced, and maintained by the National Digital Twin Programme.


# Copyright (c) Telicent Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Modifications made by the National Digital Twin Programme (NDTP)
# © Crown Copyright 2026. This work has been developed by the National Digital Twin Programme
# and is legally attributed to the UK's Department for Business, Innovation, Science and Trade (BIST) as the governing entity.


from __future__ import annotations

import unittest
from typing import Any, Protocol, runtime_checkable

from ia_map_lib.sources import DeserializerFunction
from ia_map_lib.utils import validate_callable_protocol


def not_a_deserializer(a: int, b: int) -> int:
    return a + b


def nearly_a_deserializer(data: int) -> int:
    return data


def a_deserializer(data: bytes | None) -> Any:
    return data


def kwargs_deserializer(data: bytes | None, **kwargs) -> Any:
    return data


def not_an_adder(a: int, b: int, c: bool) -> int:
    if c:
        return a * b
    else:
        return int(a / b)


@runtime_checkable
class Adder(Protocol):
    def __call__(self, x: int, y: int) -> int:
        pass # This function is intentionally left empty as part of the test setup.


class UsableAdder(Adder):
    def __call__(self, x: int, y: int) -> int:
        return x + y


class TestProtocolValidation(unittest.TestCase):

    def test_protocol_validation_no_function(self) -> None:
        with self.assertRaisesRegex(ValueError, expected_regex=".* cannot be None"):
            validate_callable_protocol(None, DeserializerFunction)

    def test_protocol_validation_no_protocol(self) -> None:
        with self.assertRaisesRegex(ValueError, expected_regex=".* cannot be None"):
            validate_callable_protocol(a_deserializer, None)

    def test_protocol_validation_not_a_function(self) -> None:
        value = 45678
        with self.assertRaisesRegex(TypeError, expected_regex=".* not a function.*"):
            validate_callable_protocol(value, DeserializerFunction)

    def test_protocol_validation_wrong_parameter_type(self) -> None:
        with self.assertRaisesRegex(TypeError, expected_regex="Wrong parameter type.*.*bytes.*int.*"):
            validate_callable_protocol(not_a_deserializer, DeserializerFunction)

    def test_protocol_validation_good(self) -> None:
        validate_callable_protocol(a_deserializer, DeserializerFunction)

    def test_protocol_validation_multiple_arguments(self) -> None:
        validate_callable_protocol(not_a_deserializer, Adder)

    def test_protocol_validation_multiple_arguments_class(self) -> None:
        validate_callable_protocol(UsableAdder, Adder)

    def test_protocol_validation_multiple_arguments_missing(self) -> None:
        with self.assertRaisesRegex(TypeError, expected_regex=".*missing required parameter y.*"):
            validate_callable_protocol(nearly_a_deserializer, Adder)

    def test_protocol_validation_extra_parameters(self) -> None:
        with self.assertRaisesRegex(TypeError, expected_regex="Wrong number of parameters.*expected 2 but.* has 3"):
            validate_callable_protocol(not_an_adder, Adder)

    def test_protocol_validation_kwargs(self) -> None:
        validate_callable_protocol(kwargs_deserializer, DeserializerFunction)


if __name__ == '__main__':
    unittest.main()
