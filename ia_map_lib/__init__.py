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


from ia_map_lib.adapter import Adapter, AutomaticAdapter
from ia_map_lib.datasets import DCATDataSet, SimpleDataSet
from ia_map_lib.mapper import Mapper
from ia_map_lib.projector import Projector
from ia_map_lib.records import Record, RecordAdapter, RecordMapper, RecordProjector, RecordUtils



__all__ = [
    'Adapter',
    'AutomaticAdapter',
    'DCATDataSet',
    'Mapper',
    'Projector',
    'Record',
    'RecordMapper',
    'RecordProjector',
    'RecordAdapter',
    'RecordUtils',
    'SimpleDataSet',
]
