from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Protocol

import yaml
from azure.storage.blob import BlobServiceClient


class StorageClient(Protocol):
    def read_text(self, container: str, blob_name: str) -> str: ...
    def exists(self, container: str, blob_name: str) -> bool: ...


@dataclass(frozen=True)
class Parsers:
    def parse(self, filename: str, raw: str) -> Any:
        if not raw or not raw.strip():
            return {"items": []}

        lower = filename.lower()

        if lower.endswith(".json"):
            return json.loads(raw)

        if lower.endswith((".yaml", ".yml")):
            return yaml.safe_load(raw)

        try:
            return yaml.safe_load(raw)
        except Exception:
            return json.loads(raw)


def load_parsers() -> Parsers:
    return Parsers()


class AzureBlobStorage:
    def __init__(self, blob_service: BlobServiceClient) -> None:
        self._svc = blob_service

    @staticmethod
    def from_env() -> "AzureBlobStorage":
        conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not conn:
            raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING not defined")
        service = BlobServiceClient.from_connection_string(conn)
        return AzureBlobStorage(service)

    def read_text(self, container: str, blob_name: str) -> str:
        client = self._svc.get_blob_client(container=container, blob=blob_name)
        stream = client.download_blob()
        data = stream.readall()
        return data.decode("utf-8")

    def exists(self, container: str, blob_name: str) -> bool:
        client = self._svc.get_blob_client(container=container, blob=blob_name)
        return client.exists()
