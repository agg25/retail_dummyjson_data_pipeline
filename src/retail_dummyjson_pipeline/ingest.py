"""Ingestion of DummyJSON data into the local raw layer (Parquet files)."""

from __future__ import annotations

import os
from pathlib import Path

import polars as pl

from retail_dummyjson_pipeline.api_client import DUMMYJSON_BASE_URL, DummyJsonClient

DEFAULT_RAW_DIR = "data/raw"


def fetch_all(
    client: DummyJsonClient,
    path: str,
    item_key: str,
    page_size: int = 100,
) -> list[dict]:
    """Fetch every record from a paginated DummyJSON endpoint."""
    items: list[dict] = []
    skip = 0
    while True:
        response = client.get(path, params={"limit": page_size, "skip": skip})
        response.raise_for_status()
        payload = response.json()
        batch: list[dict] = payload.get(item_key, [])
        if not batch:
            break
        items.extend(batch)
        if len(items) >= int(payload.get("total", 0)):
            break
        skip += page_size
    return items


def ingest_products(client: DummyJsonClient, out_dir: Path) -> Path:
    """Land the full product catalog as Parquet."""
    out_path = out_dir / "products.parquet"
    pl.DataFrame(fetch_all(client, "/products", "products")).write_parquet(out_path)
    return out_path


def ingest_users(client: DummyJsonClient, out_dir: Path) -> Path:
    """Land all users as Parquet."""
    out_path = out_dir / "users.parquet"
    pl.DataFrame(fetch_all(client, "/users", "users")).write_parquet(out_path)
    return out_path


def ingest_carts(client: DummyJsonClient, out_dir: Path) -> tuple[Path, Path]:
    """Land carts (header) and cart line items (exploded) as Parquet."""
    carts = fetch_all(client, "/carts", "carts")

    cart_rows: list[dict] = []
    item_rows: list[dict] = []
    for cart in carts:
        cart_rows.append({key: value for key, value in cart.items() if key != "products"})
        for product in cart.get("products", []):
            row: dict = {"cart_id": cart["id"], "user_id": cart.get("userId")}
            for key, value in product.items():
                row["product_id" if key == "id" else key] = value
            item_rows.append(row)

    cart_path = out_dir / "carts.parquet"
    pl.DataFrame(cart_rows).write_parquet(cart_path)
    items_path = out_dir / "cart_items.parquet"
    pl.DataFrame(item_rows).write_parquet(items_path)
    return cart_path, items_path


def run_ingestion(
    out_dir: Path,
    client: DummyJsonClient | None = None,
    base_url: str = DUMMYJSON_BASE_URL,
) -> dict[str, Path]:
    """Run the full ingestion and return the paths written, keyed by entity."""
    out_dir.mkdir(parents=True, exist_ok=True)
    owns_client = client is None
    if client is None:
        client = DummyJsonClient(base_url=base_url)
    try:
        products_path = ingest_products(client, out_dir)
        users_path = ingest_users(client, out_dir)
        carts_path, cart_items_path = ingest_carts(client, out_dir)
        return {
            "products": products_path,
            "users": users_path,
            "carts": carts_path,
            "cart_items": cart_items_path,
        }
    finally:
        if owns_client:
            client.close()


def main() -> None:
    """CLI entry point: pull DummyJSON data into the local raw layer."""
    from dotenv import load_dotenv

    load_dotenv()
    base_url = os.getenv("DUMMYJSON_BASE_URL", DUMMYJSON_BASE_URL)
    out_dir = Path(os.getenv("RAW_DATA_DIR", DEFAULT_RAW_DIR))
    for entity, path in run_ingestion(out_dir=out_dir, base_url=base_url).items():
        print(f"[{entity}] {path}")


if __name__ == "__main__":
    main()
