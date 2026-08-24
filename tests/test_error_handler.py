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

import json
from collections.abc import Iterable
from unittest import TestCase, mock

from ia_map_lib import AutomaticAdapter, Mapper, Projector, Record
from ia_map_lib.errors import ErrorHandler, ErrorLevel
from ia_map_lib.sinks.listSink import ListSink
from ia_map_lib.sources.listSource import ListSource


class FakeErrorHandler(ErrorHandler):

    def __init__(self):
        super().__init__('test-id')
        self.errors = []
        self.closed = False

    def __send_record__(self, record):
        self.errors.append(record)

    def close(self):
        self.closed = True


def fake_adapter_function() -> Iterable[Record]:
    raise Exception('Test Exception')


def fake_mapper_function(record: Record) -> Record | list[Record] | None:
    raise Exception('Test Exception')


def fake_projector_function(record: Record) -> None:
    raise Exception('Test Exception')


class ErrorHandlerTestCaseStub(TestCase):

    def setUp(self) -> None:
        self.error_handler = FakeErrorHandler()

    def tearDown(self) -> None:
        del self.error_handler


class ErrorHandlerTestCase(ErrorHandlerTestCaseStub):

    def test_send_exception(self):
        try:
            raise Exception('Test Exception')
        except Exception as e:
            self.error_handler.send_exception(e)

        self.assertEqual(1, len(self.error_handler.errors))
        error_record = self.error_handler.errors[0]
        self.assertEqual(error_record.headers, [('Content-Type', b'application/json')])
        record_json = json.loads(error_record.value)
        self.assertEqual(record_json['error_message'], 'Test Exception')
        self.assertEqual(record_json['id'], 'test-id')
        self.assertEqual(record_json['error_type'], 'Exception')
        self.assertEqual(record_json['level'], ErrorLevel.ERROR.name)

    def test_send_error(self):
        self.error_handler.send_error('Test Error', 'TestType', ErrorLevel.WARNING)
        self.assertEqual(1, len(self.error_handler.errors))

        error_record = self.error_handler.errors[0]
        self.assertEqual(error_record.headers, [('Content-Type', b'application/json')])

        record_json = json.loads(error_record.value)
        self.assertEqual(record_json['error_message'], 'Test Error')
        self.assertEqual(record_json['id'], 'test-id')
        self.assertEqual(record_json['error_type'], 'TestType')
        self.assertEqual(record_json['level'], ErrorLevel.WARNING.name)


class ErrorHandlerUseCaseTestCase(ErrorHandlerTestCaseStub):

    @mock.patch('ia_map_lib.errors.ErrorHandler.send_exception')
    def test_adaptor_error_handler(self, mocked_send_exception):
        adapter = AutomaticAdapter(
            adapter_function=fake_adapter_function,
            target=ListSink(), name='test-name', error_handler=self.error_handler,
            has_reporter=False, has_data_catalog=False,
        )
        try:
            adapter.run()
        except Exception:
            pass

        self.assertEqual(1, mocked_send_exception.call_count)

    @mock.patch('ia_map_lib.errors.ErrorHandler.send_exception')
    def test_mapper_error_handler(self, mocked_send_exception):
        mapper = Mapper(
            map_function=fake_mapper_function, source=ListSource(['one', 'two']),
            target=ListSink(), name='test-name', error_handler=self.error_handler,
            has_reporter=False,
        )
        try:
            mapper.run()
        except Exception:
            pass

        self.assertEqual(1, mocked_send_exception.call_count)

    @mock.patch('ia_map_lib.errors.ErrorHandler.send_exception')
    def test_projector_error_handler(self, mocked_send_exception):
        projector = Projector(
            projector_function=fake_projector_function, source=ListSource(['one', 'two']),
            target=ListSink(), name='test-name', error_handler=self.error_handler,
            has_reporter=False, target_store='Test'
        )
        try:
            projector.run()
        except Exception:
            pass

        self.assertEqual(1, mocked_send_exception.call_count)
