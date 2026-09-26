# retail_dummyjson_data_pipeline

End-to-end data engineering pipeline for **retail/e-commerce analytics**, ingesting the free
[DummyJSON](https://dummyjson.com) API into **Google BigQuery** and transforming it with **dbt**.

## Architecture

```
DummyJSON API
    ↓  (Python ingestion: httpx + polars)
raw → bronze → silver (local Parquet staging)
    ↓  (load)
BigQuery (warehouse)
    ↓  (dbt)
staging → intermediate → marts
```

## Stack

| Layer | Tool |
|---|---|
| Ingestion | Python 3.11, httpx, polars, pyarrow |
| Warehouse | Google BigQuery (free tier) |
| Transformation | dbt-core + dbt-bigquery |
| Data quality | dbt tests (elementary later) |
| Orchestration | Prefect (later) |
| Containerisation | Docker (later) |
| CI/CD | GitHub Actions (later) |
| IaC | Terraform (later) |

## Repository structure

- `src/retail_dummyjson_pipeline/` — Python ingestion code
- `tests/` — pytest suite
- `dbt/` — dbt project (staging / intermediate / marts)
- `data/{raw,bronze,silver,gold}/` — local data staging (gitignored)
- `scripts/` — helper scripts
- `docs/` — documentation
- `infrastructure/` — Terraform (later)
- `docker/` — container configs (later)
- `.github/workflows/` — CI/CD (later)

## Local setup

```powershell
uv sync                 # create .venv and install dependencies
uv run retail-ingest    # pull DummyJSON data into data/raw/
uv run pytest           # run tests
uv run ruff check .     # lint
uv run mypy src         # type-check
```

## Status

Scaffolding in progress — environment and repository foundation only.
