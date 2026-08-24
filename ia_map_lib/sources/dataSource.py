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

from collections.abc import Iterable

from ia_map_lib.records import Record


class DataSource:
    """Represents a source from which data can be read"""
    def __init__(self, source_name: str = None):
        if source_name is None:
            raise TypeError("DataSource must be provided a source name")
        self.__source = source_name

    def data(self) -> Iterable[Record]:
        """Provides an iterable over the data"""
        raise NotImplementedError

    def remaining(self) -> int | None:
        """
        Returns the remaining number of records

        This may be None if this is unknown.  The return value may also change over time both as records are consumed
        from the data source and if the data source is actively receiving new records.
        """
        return None

    def get_source_name(self):
        return self.__source

    def close(self) -> None:
        """Closes the data source, allowing it to release any resources it may be holding open"""
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
