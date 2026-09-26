"""Minimal HTTP client for the DummyJSON API."""

from __future__ import annotations

from collections.abc import Mapping

import httpx

DUMMYJSON_BASE_URL = "https://dummyjson.com"


class DummyJsonClient:
    """A thin client around the DummyJSON REST API.

    Intentionally minimal for now; the ingestion logic will be added once the
    pipeline work begins (after environment/repository setup is complete).
    """

    def __init__(self, base_url: str = DUMMYJSON_BASE_URL, timeout: float = 30.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(
        self,
        path: str,
        params: Mapping[str, str | int | float | bool | None] | None = None,
    ) -> httpx.Response:
        """Perform a GET request against the API."""
        with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
            return client.get(path, params=params)
