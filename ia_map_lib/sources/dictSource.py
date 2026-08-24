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


class DictionarySource(DataSource):
    """
    A Data Source backed by a dictionary, intended for test and development purposes only
    """

    def __init__(self, data=None):
        """
        Creates a new source backed by the given dictionary
        :param data: Dictionary
        """
        super().__init__("Dictionary")
        if data is None:
            data = {}
        self.dictionary = data
        self.iterator = None

    def data(self) -> Iterable[Record]:
        return self

    def __iter__(self):
        self.iterator = self.dictionary.copy()
        return self

    def __next__(self):
        if self.iterator is None:
            raise StopIteration
        try:
            key, value = self.iterator.popitem()
            return Record(None, key, value, None)
        except KeyError:
            self.iterator = None
            raise StopIteration from None

    def close(self) -> None:
        self.iterator = None

    def __str__(self):
        return f"In-Memory Dictionary({len(self.dictionary)} items)"
