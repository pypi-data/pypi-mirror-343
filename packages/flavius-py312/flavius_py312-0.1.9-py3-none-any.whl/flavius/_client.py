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

from datetime import date, datetime, time
import requests
from typing import List, Union, Tuple
from .utils.json import Record, parse
from .utils.utils import DataType, TimeStamp


class ClientImpl:
    """Internal implementation of the Flavius client"""

    def __init__(self, host: str = "localhost", port: int = 30000, timeout: int | None = None):
        self._host = host
        self._port = port
        self._api_header = {"Content-Type": "application/json"}
        self._timeout = timeout

    def _get_api_url(self) -> str:
        return f"http://{self._host}:{self._port}/v1/cypher"

    def verify_connectivity(self) -> None:
        health_url = f"http://{self._host}:{self._port}/health"
        rsp = requests.get(health_url, timeout=self._timeout)
        assert rsp.status_code == 200, f"Failed to connect to Flavius: {rsp.text}"

    def close(self) -> None:
        pass

    def create_namespace(self, namespace: str) -> None:
        create_ns = {
            "statement": f"CREATE NAMESPACE {namespace}",
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=create_ns,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert (
            rsp.status_code == 200
        ), f"Failed to create namespace {namespace}: {rsp.text}"
        assert (
            rsp.json()["code"] == 0
        ), f"Failed to create namespace {namespace}: {rsp.json()}"

    def drop_namespace(self, namespace: str) -> None:
        drop_ns = {
            "statement": f"DROP NAMESPACE {namespace}",
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=drop_ns,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert (
            rsp.status_code == 200
        ), f"Failed to drop namespace {namespace}: {rsp.text}"
        assert (
            rsp.json()["code"] == 0
        ), f"Failed to drop namespace {namespace}: {rsp.json()}"

    def list_namespace(self) -> List[str]:
        payload = {
            "statement": "LIST NAMESPACE",
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=payload,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert rsp.status_code == 200, f"Failed to list namespace: {rsp.text}"
        assert rsp.json()["code"] == 0, f"Failed to list namespace: {rsp.json()}"
        return rsp.json()["data"]["entries"]

    def create_graph(self, graph: str, namespace: str) -> None:
        create_graph = {
            "statement": f"CREATE GRAPH {graph}",
            "namespace": namespace,
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=create_graph,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert rsp.status_code == 200, f"Failed to create graph {graph}: {rsp.text}"
        assert rsp.json()["code"] == 0, f"Failed to create graph {graph}: {rsp.json()}"

    def drop_graph(self, graph: str, namespace: str) -> None:
        drop_graph = {
            "statement": f"DROP GRAPH {graph}",
            "namespace": namespace,
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=drop_graph,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert rsp.status_code == 200, f"Failed to drop graph {graph}: {rsp.text}"
        assert rsp.json()["code"] == 0, f"Failed to drop graph {graph}: {rsp.json()}"

    def list_graph(self, namespace: str) -> List[str]:
        payload = {
            "statement": "LIST GRAPH",
            "namespace": namespace,
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=payload,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert rsp.status_code == 200, f"Failed to list graph: {rsp.text}"
        assert rsp.json()["code"] == 0, f"Failed to list graph: {rsp.json()}"
        return rsp.json()["data"]["entries"]

    def create_vertex_table(
        self,
        table: str,
        columns: List[Union[Tuple[str, DataType], Tuple[str, DataType, bool]]],
        primary_key: Union[str, List[str]],
        namespace: str,
        graph: str,
    ) -> None:
        # Build column definitions
        cols = []
        for col in columns:
            if len(col) == 2:
                name, dtype = col
                cols.append(f"{name} {dtype.value}")
            else:
                name, dtype, nullable = col
                nullable_str = "NULL" if nullable else "NOT NULL"
                cols.append(f"{name} {dtype.value} {nullable_str}")

        # Build primary key
        if isinstance(primary_key, list):
            pk = f"({', '.join(primary_key)})"
        else:
            pk = primary_key

        properties = f"({', '.join(cols)}) PRIMARY KEY {pk}"
        create_vtable = {
            "statement": f"CREATE VERTEX {table} {properties}",
            "namespace": namespace,
            "graph": graph,
            "timeout": self._timeout,
            "parameters": {},
        }

        rsp = requests.post(
            self._get_api_url(),
            json=create_vtable,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert (
            rsp.status_code == 200
        ), f"Failed to create vertex table {table}: {rsp.text}"
        assert (
            rsp.json()["code"] == 0
        ), f"Failed to create vertex table {table}: {rsp.json()}"

    def drop_vertex_table(self, table: str, namespace: str, graph: str) -> None:
        drop_vtable = {
            "statement": f"DROP VERTEX {table}",
            "namespace": namespace,
            "graph": graph,
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=drop_vtable,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert (
            rsp.status_code == 200
        ), f"Failed to drop vertex table {table}: {rsp.text}"
        assert (
            rsp.json()["code"] == 0
        ), f"Failed to drop vertex table {table}: {rsp.json()}"

    def list_vertex(self, namespace: str, graph: str) -> List[str]:
        payload = {
            "statement": "LIST VERTEX",
            "namespace": namespace,
            "graph": graph,
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=payload,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert rsp.status_code == 200, f"Failed to list vertex: {rsp.text}"
        assert rsp.json()["code"] == 0, f"Failed to list vertex: {rsp.json()}"
        return rsp.json()["data"]["entries"]

    def create_edge_table(
        self,
        table: str,
        source_vertex: str,
        target_vertex: str,
        columns: List[Union[Tuple[str, DataType], Tuple[str, DataType, bool]]],
        directed: bool,
        namespace: str,
        graph: str,
        reverse_edge: str = None,
    ) -> None:
        # Build column definitions
        cols = []
        for col in columns:
            if len(col) == 2:
                name, dtype = col
                cols.append(f"{name} {dtype.value}")
            else:
                name, dtype, nullable = col
                nullable_str = "NULL" if nullable else "NOT NULL"
                cols.append(f"{name} {dtype.value} {nullable_str}")

        direction = "DIRECTED" if directed else "UNDIRECTED"
        properties = f"(FROM {source_vertex} TO {target_vertex}"
        if cols:
            properties += f", {', '.join(cols)}"
        properties += ")"

        if reverse_edge:
            properties += f" WITH REVERSE EDGE {reverse_edge}"

        create_etable = {
            "statement": f"CREATE {direction} EDGE {table} {properties}",
            "namespace": namespace,
            "graph": graph,
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=create_etable,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert (
            rsp.status_code == 200
        ), f"Failed to create edge table {table}: {rsp.text}"
        assert (
            rsp.json()["code"] == 0
        ), f"Failed to create edge table {table}: {rsp.json()}"

    def drop_edge_table(self, table: str, namespace: str, graph: str) -> None:
        drop_etable = {
            "statement": f"DROP EDGE {table}",
            "namespace": namespace,
            "graph": graph,
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=drop_etable,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert rsp.status_code == 200, f"Failed to drop edge table {table}: {rsp.text}"
        assert (
            rsp.json()["code"] == 0
        ), f"Failed to drop edge table {table}: {rsp.json()}"

    def list_edge(self, namespace: str, graph: str) -> List[str]:
        payload = {
            "statement": "LIST EDGE",
            "namespace": namespace,
            "graph": graph,
            "timeout": self._timeout,
            "parameters": {},
        }
        rsp = requests.post(
            self._get_api_url(),
            json=payload,
            headers=self._api_header,
            timeout=self._timeout,
        )
        assert rsp.status_code == 200, f"Failed to list edge: {rsp.text}"
        assert rsp.json()["code"] == 0, f"Failed to list edge: {rsp.json()}"
        return rsp.json()["data"]["entries"]

    def execute_query(
        self,
        query: str,
        namespace: str,
        graph: str,
        parameters: dict = None,
        timeout: int | None = None,
    ) -> Tuple[List[Record], List[str]] | None:
        def process_param_value(value):
            if isinstance(value, list):
                value = [process_param_value(v) for v in value]
                return f"ARRAY[{', '.join(value)}]"
            elif isinstance(value, str):
                return f"'{value}'"
            elif isinstance(value, dict):
                items = []
                for k, v in value.items():
                    items.append(f"{k}: {process_param_value(v)}")
                return "{ " + ", ".join(items) + " }"
            elif isinstance(value, datetime):
                return f"CAST ('{value.strftime('%Y-%m-%d %H:%M:%S.%f')}' AS DATETIME)"
            elif isinstance(value, date):
                return f"CAST ('{value.strftime('%Y-%m-%d')}' AS DATE)"
            elif isinstance(value, time):
                return f"CAST ('{value.strftime('%H:%M:%S.%f')}' AS TIME)"
            elif isinstance(value, TimeStamp):
                return f"CAST ('{value}' AS TIMESTAMP)"
            else:
                return str(value)

        processed_parameters = {}
        if parameters:
            for key, value in parameters.items():
                processed_parameters[key] = process_param_value(value)

        if timeout is None:
            timeout = self._timeout

        payload = {
            "statement": query,
            "namespace": namespace,
            "graph": graph,
            "parameters": processed_parameters,
            "timeout": timeout,
        }
        rsp = requests.post(
            self._get_api_url(),
            json=payload,
            headers=self._api_header,
            timeout=timeout,
        )

        assert rsp.status_code == 200, f"Failed to execute query: {rsp.text}"
        assert rsp.json()["code"] == 0, f"Failed to execute query: {rsp.json()}"

        return parse(rsp.json()["data"])
