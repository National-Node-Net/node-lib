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

import os
from unittest import TestCase, mock

from ia_map_lib import Record, RecordUtils
from ia_map_lib.mapper import Mapper
from ia_map_lib.sinks.listSink import ListSink
from ia_map_lib.sources.listSource import ListSource


def __map_function_no_headers__(record: Record, **map_args) -> Record | list[Record] | None:
    headers = {
        'New-Header': 'New Header'
    }
    return Record(RecordUtils.to_headers(headers), None, None, None)


def __map_function_set_new_label__(record: Record, **map_args) -> Record | list[Record] | None:
    headers = {
        'Security-Label': 'NewLabel'
    }
    return Record(RecordUtils.to_headers(headers), None, None, None)


class PersistentSecurityHeadersTestCase(TestCase):

    def test_output_record_has_same_labels_as_input_record(self):
        headers = {
            'Security-Label': 'TestLabel'
        }
        record = Record(headers=RecordUtils.to_headers(headers), key=None, value=None, raw=None)
        source = ListSource([record])
        sink = ListSink()
        mapper = Mapper(
            source=source, target=sink, map_function=__map_function_no_headers__,
            has_reporter=False, has_error_handler=False
        )
        mapper.run()
        output_record = sink.get()[0]
        output_security_label = RecordUtils.get_last_header(output_record, 'Security-Label')
        self.assertEqual(output_security_label, headers['Security-Label'])

    def test_can_override_label(self):
        headers = {
            'Security-Label': 'TestLabel'
        }
        record = Record(headers=RecordUtils.to_headers(headers), key=None, value=None, raw=None)
        source = ListSource([record])
        sink = ListSink()
        mapper = Mapper(
            source=source, target=sink, map_function=__map_function_set_new_label__,
            has_reporter=False, has_error_handler=False
        )
        mapper.run()
        output_record = sink.get()[0]
        output_security_label = list(RecordUtils.get_headers(output_record, 'Security-Label'))
        self.assertEqual(len(output_security_label), 1)
        self.assertEqual('NewLabel', output_security_label[0])

    def test_nothing_happens_with_no_label(self):
        record = Record(headers=None, key=None, value=None, raw=None)
        source = ListSource([record])
        sink = ListSink()
        mapper = Mapper(
            source=source, target=sink, map_function=__map_function_no_headers__,
            has_reporter=False, has_error_handler=False
        )
        mapper.run()
        output_record = sink.get()[0]
        self.assertFalse(RecordUtils.has_header(output_record, 'Security-Label'))

    @mock.patch.dict(os.environ, {"DISABLE_PERSISTENT_HEADERS": "1"})
    def test_persistence_can_be_disabled(self):
        headers = {
            'Security-Label': 'TestLabel'
        }
        record = Record(headers=RecordUtils.to_headers(headers), key=None, value=None, raw=None)
        source = ListSource([record])
        sink = ListSink()
        mapper = Mapper(
            source=source, target=sink, map_function=__map_function_no_headers__,
            has_reporter=False, has_error_handler=False
        )
        mapper.run()
        output_record = sink.get()[0]
        self.assertFalse(RecordUtils.has_header(output_record, 'Security-Label'))
