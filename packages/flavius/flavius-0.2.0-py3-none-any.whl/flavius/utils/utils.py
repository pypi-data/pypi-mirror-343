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

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

class Record:
    """
    A wrapper class for query result records that supports attribute-style data access
    """

    def __init__(self, schema: List[str], values: List[Any]):
        self._schema = schema
        self._values = values
        self._data = dict(zip(schema, values))

    def __getitem__(self, key: str) -> Any:
        """Support record['key'] style access"""
        return self._data[key]

    def __str__(self) -> str:
        return str(self._data)

    def get(self, key: str, default: Any = None) -> Any:
        """Safely get a value with a default"""
        return self._data.get(key, default)

    def keys(self) -> List[str]:
        """Return all field names"""
        return self._schema

    def values(self) -> List[Any]:
        """Return all values"""
        return self._values

    def items(self) -> Dict[str, Any]:
        """Return a dictionary of field names and values"""
        return self._data

class DataType(Enum):
    """Data types supported by Flavius"""

    BOOL = "BOOL"
    BIGINT = "BIGINT"
    DOUBLE = "DOUBLE"
    VARCHAR = "VARCHAR"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"


class TimeStamp:
    def __init__(self, dt: datetime):
        self._dt = dt

    def __str__(self) -> str:
        if self._dt.tzinfo is None:
            return self._dt.strftime("%Y-%m-%d %H:%M:%S.%f+00:00")
        else:
            return self._dt.strftime("%Y-%m-%d %H:%M:%S.%f%z")
