"""Prefect orchestration for the retail data pipeline."""

from __future__ import annotations

import subprocess
from pathlib import Path

from prefect import flow, task

from retail_dummyjson_pipeline.ingest import run_ingestion
from retail_dummyjson_pipeline.load_bigquery import load_raw_layer

DEFAULT_PROJECT = "retail-pipeline-509804"
DEFAULT_DATASET = "retail_dummyjson"
RAW_DIR = Path("data/raw")


@task
def ingest() -> None:
    """Pull DummyJSON data into the local raw layer."""
    run_ingestion(out_dir=RAW_DIR)


@task
def load_to_bigquery(project: str, dataset: str) -> None:
    """Load the raw Parquet files into BigQuery."""
    load_raw_layer(project, dataset, RAW_DIR)


@task
def dbt_run() -> None:
    """Build dbt staging/intermediate/marts models."""
    subprocess.run(
        ["uv", "run", "dbt", "run", "--project-dir", "dbt", "--profiles-dir", "dbt"],
        check=True,
    )


@task
def dbt_test() -> None:
    """Run dbt data-quality tests."""
    subprocess.run(
        ["uv", "run", "dbt", "test", "--project-dir", "dbt", "--profiles-dir", "dbt"],
        check=True,
    )


@flow(name="retail-dummyjson-pipeline")
def retail_pipeline(project: str = DEFAULT_PROJECT, dataset: str = DEFAULT_DATASET) -> None:
    """Orchestrate the full pipeline: ingest -> load -> dbt run -> dbt test."""
    ingest()
    load_to_bigquery(project, dataset)
    dbt_run()
    dbt_test()


if __name__ == "__main__":
    retail_pipeline()
