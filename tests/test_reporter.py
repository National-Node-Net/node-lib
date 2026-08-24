# SPDX-License-Identifier: Apache-2.0
# Originally developed by Telicent Ltd.; subsequently adapted, enhanced, and maintained by the National Digital Twin Programme.


# Copyright (c) Telicent Ltd.

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


import json
import time
import unittest

from ia_map_lib.reporter import Reporter
from ia_map_lib.sinks.listSink import ListSink
from ia_map_lib.status import Status
from tests.test_records import RecordVerifier


class TestReporter(RecordVerifier):
    # Need to break this up and add more but should do for now
    def test_reporter_01(self):
        reporter_sink = ListSink()
        reporter = Reporter(
            action_name="Test", target_name="destination", source_name="source", action="mapper", sink=reporter_sink
        )
        received = json.loads(reporter.sink.get().pop().value)
        self.assertEqual(received["name"], "Test")
        self.assertEqual(received["component_type"], "mapper")
        self.assertEqual(received["status"], "STARTED")
        self.assertEqual(received["input"]["name"], "source")
        self.assertEqual(received["output"]["name"], "destination")
        reporter.run()
        time.sleep(2)
        received = json.loads(reporter.sink.get().pop().value)
        self.assertEqual(received["name"], "Test")
        self.assertEqual(received["status"], "RUNNING")
        time.sleep(2)
        reporter.set_status(Status.COMPLETED)
        reporter.stop_heartbeat()
        received = json.loads(reporter.sink.get().pop().value)
        self.assertEqual(received["name"], "Test")
        self.assertEqual(received["status"], "COMPLETED")
        reporter.set_status(Status.ERRORING)
        reporter.send_heartbeat()
        received = json.loads(reporter.sink.get().pop().value)
        self.assertEqual(received["name"], "Test")
        self.assertEqual(received["status"], "ERRORING")

    def test_reporter_no_termination_hang(self):
        reporter_sink = ListSink()
        start = time.perf_counter()
        reporter = Reporter(action_name="Test", target_name="destination", source_name="source", action="mapper",
                            heartbeat_time=5, sink=reporter_sink)
        reporter.run()
        time.sleep(1)
        reporter.stop_heartbeat()
        elapsed = time.perf_counter() - start
        self.assertTrue(elapsed < 5, "Expected reporter to terminate immediately")


if __name__ == '__main__':
    unittest.main()
