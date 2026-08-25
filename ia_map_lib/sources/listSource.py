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


from collections.abc import Iterable

from ia_map_lib.records import Record
from ia_map_lib.sources.dataSource import DataSource


class ListSource(DataSource):
    """
        A Data Source backed by a list, intended for test and development purposes only
    """

    def __init__(self, data=None):
        """
        Creates a new list source backed by the given list
        :param data: List of records
        """
        super().__init__("List")
        if data is None:
            data = []
        self.list = data
        self.index = -1

    def data(self) -> Iterable[Record]:
        return self

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        self.index += 1
        if self.index >= len(self.list):
            raise StopIteration
        return self.list[self.index]

    def close(self) -> None:
        self.index = -1

    def __str__(self):
        return f"In-Memory List({len(self.list)} records)"
