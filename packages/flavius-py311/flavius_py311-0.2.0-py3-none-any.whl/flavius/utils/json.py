# Copyright 2025 Kasma
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
# See the License for the specific language governing permissions and
# limitations under the License.

import dateutil.parser
from typing import Any, List, Tuple
from .utils import Record


def parse_column_schema(columns: List[dict]) -> dict:
    column_types = {}
    for col in columns:
        name = col["name"]
        kind = col["data_type"]["kind"]
        if kind in ["Struct", "Vertex", "Edge"]:
            column_types[name] = {}
            for field in col["data_type"]["fields"]:
                field_name = field["name"]
                column_types[name][field_name] = field["data_type"]["kind"]
        else:
            column_types[name] = kind
    return column_types


def convert_value(value: Any, data_type: dict | str) -> Any:
    if isinstance(data_type, dict):
        for field, field_type in data_type.items():
            value[field] = convert_value(value[field], field_type)
    elif data_type == "Date":
        value = dateutil.parser.parse(value).date()
    elif data_type == "Time":
        value = dateutil.parser.parse(value).time()
    elif data_type in ["DateTime", "Timestamp"]:
        value = dateutil.parser.parse(value)
    return value


def parse(data: dict) -> Tuple[List[Record], List[str]] | None:
    if data["kind"] != "Query":
        return None

    column_types = parse_column_schema(data["schema"]["columns"])
    keys = [col["name"] for col in data["schema"]["columns"]]

    records = []
    for row in data["rows"]:
        values = [convert_value(row[key], column_types[key]) for key in keys]
        records.append(Record(keys, values))

    return records, keys
