"""Load local raw Parquet files into BigQuery raw tables."""

from __future__ import annotations

import json
import os
from pathlib import Path

import polars as pl
from google.cloud import bigquery

DEFAULT_PROJECT = "retail-pipeline-509804"
DEFAULT_DATASET = "retail_dummyjson"
RAW_TABLES = {
    "products.parquet": "raw_products",
    "users.parquet": "raw_users",
    "carts.parquet": "raw_carts",
    "cart_items.parquet": "raw_cart_items",
}


def _flatten_for_bigquery(df: pl.DataFrame):
    """Convert nested columns (lists/dicts) to JSON strings for BigQuery."""
    pandas_df = df.to_pandas()
    for column in pandas_df.columns:
        non_null = pandas_df[column].dropna()
        if len(non_null) and isinstance(non_null.iloc[0], (list, dict)):
            pandas_df[column] = pandas_df[column].map(
                lambda v: json.dumps(v) if isinstance(v, (list, dict)) else v
            )
    return pandas_df


def _load_table(
    client: bigquery.Client,
    project: str,
    dataset_id: str,
    table_id: str,
    df: pl.DataFrame,
) -> None:
    pandas_df = _flatten_for_bigquery(df)
    table_ref = f"{project}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(pandas_df, table_ref, job_config=job_config)
    job.result()
    print(f"Loaded {table_id}: {len(pandas_df)} rows")


def main() -> None:
    """CLI entry point: load the local raw layer into BigQuery."""
    from dotenv import load_dotenv

    load_dotenv()
    project = os.getenv("GCP_PROJECT_ID", DEFAULT_PROJECT)
    dataset_id = os.getenv("BIGQUERY_DATASET", DEFAULT_DATASET)
    raw_dir = Path(os.getenv("RAW_DATA_DIR", "data/raw"))

    client = bigquery.Client(project=project)

    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    try:
        client.get_dataset(dataset_ref)
    except Exception:
        client.create_dataset(dataset_ref)
        print(f"Created dataset {project}.{dataset_id}")

    for filename, table_id in RAW_TABLES.items():
        path = raw_dir / filename
        if not path.exists():
            print(f"SKIPPED {table_id}: {path} not found (run `uv run retail-ingest` first)")
            continue
        _load_table(client, project, dataset_id, table_id, pl.read_parquet(path))


if __name__ == "__main__":
    main()
