"""Minimal HTTP client for the DummyJSON API."""

from __future__ import annotations

from collections.abc import Mapping

import httpx

DUMMYJSON_BASE_URL = "https://dummyjson.com"


class DummyJsonClient:
    """A thin client around the DummyJSON REST API."""

    def __init__(
        self,
        base_url: str = DUMMYJSON_BASE_URL,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout, transport=transport)

    def get(
        self,
        path: str,
        params: Mapping[str, str | int | float | bool | None] | None = None,
    ) -> httpx.Response:
        """Perform a GET request against the API."""
        return self._client.get(path, params=params)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()
