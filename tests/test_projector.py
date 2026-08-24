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

from ia_map_lib import Projector, Record, RecordProjector
from ia_map_lib.sources.listSource import ListSource
from tests.test_records import RecordVerifier


def __noop_projector__(record: Record) -> None:
    pass # This function is intentionally left empty as part of the test setup.


def __fail_projector__(record: Record) -> None:
    raise ValueError("Can't project this record")


def __args_projector__(record: Record, **kwargs) -> None:
    print(kwargs["test"])


class CollectingProjector(RecordProjector):
    def __init__(self):
        self.data: list[Record] = []

    def __call__(self, record: Record) -> None:
        self.data.append(record)

    def get(self) -> list[Record]:
        return self.data


class TestProjector(RecordVerifier):

    def test_bad_projector_01(self):
        with self.assertRaisesRegex(TypeError, expected_regex=".*required positional argument.*projector_function.*"):
            Projector(source=ListSource(), target_store="Test", has_reporter=False, has_error_handler=False)

    def test_bad_projector_02(self):
        with self.assertRaisesRegex(ValueError, expected_regex=".*cannot be None"):
            Projector(source=ListSource(), target_store="Test", projector_function=None,
                      has_reporter=False, has_error_handler=False)

    def test_projector_01(self):
        source = ListSource(self.__generate_records__(10))
        projector = Projector(source=source, target_store="Test", projector_function=__noop_projector__,
                              has_reporter=False, has_error_handler=False)
        projector.run()

    def test_projector_02(self):
        source = ListSource(self.__generate_records__(10))
        projector = Projector(source=source, target_store="Test", projector_function=__noop_projector__,
                              text_colour=None, has_reporter=False, has_error_handler=False)
        projector.run()

    def test_projector_03(self):
        source = ListSource(self.__generate_records__(10))
        projector = Projector(source=source, target_store="Test", projector_function=__fail_projector__,
                              has_reporter=False, has_error_handler=False)
        with self.assertRaisesRegex(ValueError, expected_regex="Can't project this record"):
            projector.run()

    def test_projector_04(self):
        source = ListSource(self.__generate_records__(10))
        collector = CollectingProjector()
        projector = Projector(source=source, target_store="Test", projector_function=collector,
                              has_reporter=False, has_error_handler=False)
        projector.run()

        self.assertEqual(len(collector.get()), 10)
        self.assertEqual(collector.get(), source.list)

    def test_projector_args(self):
        source = ListSource(self.__generate_records__(10))
        projector = Projector(source=source, target_store="Test", projector_function=__args_projector__,
                              test="foo", has_error_handler=False, has_reporter=False,)
        projector.run()


if __name__ == '__main__':
    unittest.main()
