"""Tests for the ingestion module using a mocked HTTP transport."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import httpx
import polars as pl

from retail_dummyjson_pipeline.api_client import DummyJsonClient
from retail_dummyjson_pipeline.ingest import fetch_all, run_ingestion


def _make_client(handler: Callable[[httpx.Request], httpx.Response]) -> DummyJsonClient:
    return DummyJsonClient(transport=httpx.MockTransport(handler))


def test_fetch_all_paginates() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        skip = int(request.url.params["skip"])
        if skip == 0:
            return httpx.Response(200, json={"products": [{"id": 1}, {"id": 2}], "total": 3})
        return httpx.Response(200, json={"products": [{"id": 3}], "total": 3})

    client = _make_client(handler)
    items = fetch_all(client, "/products", "products", page_size=2)
    assert [item["id"] for item in items] == [1, 2, 3]


def test_run_ingestion_writes_parquet(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == "/products":
            return httpx.Response(
                200, json={"products": [{"id": 1, "title": "Widget"}], "total": 1}
            )
        if path == "/users":
            return httpx.Response(
                200, json={"users": [{"id": 1, "firstName": "Ada"}], "total": 1}
            )
        if path == "/carts":
            return httpx.Response(
                200,
                json={
                    "carts": [
                        {
                            "id": 100,
                            "userId": 1,
                            "total": 9.99,
                            "products": [
                                {"id": 1, "title": "Widget", "price": 9.99, "quantity": 1}
                            ],
                        }
                    ],
                    "total": 1,
                },
            )
        return httpx.Response(404)

    client = _make_client(handler)
    results = run_ingestion(out_dir=tmp_path, client=client)

    products = pl.read_parquet(results["products"])
    assert products.shape[0] == 1
    assert products["title"][0] == "Widget"

    carts = pl.read_parquet(results["carts"])
    assert carts["id"][0] == 100

    cart_items = pl.read_parquet(results["cart_items"])
    assert cart_items.shape[0] == 1
    assert cart_items["product_id"][0] == 1
