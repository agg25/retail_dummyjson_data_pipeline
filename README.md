# retail_dummyjson_data_pipeline

[![CI](https://github.com/agg25/retail_dummyjson_data_pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/agg25/retail_dummyjson_data_pipeline/actions)

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
uv run pytest           # run tests
uv run ruff check .     # lint
uv run mypy src         # type-check
```

## Running the pipeline

```powershell
uv run retail-ingest     # 1. DummyJSON API -> data/raw/*.parquet
uv run retail-load-bq    # 2. Parquet -> BigQuery raw_* tables
uv run dbt run --project-dir dbt --profiles-dir dbt      # 3. build staging/intermediate/marts
uv run dbt test --project-dir dbt --profiles-dir dbt     # 4. run data quality tests
uv run dbt docs generate --project-dir dbt --profiles-dir dbt  # 5. generate lineage docs
```

> **Note:** `dbt/profiles.yml` is gitignored (personal config). Create it manually
> before running dbt:
> ```yaml
> retail_dummyjson:
>   target: dev
>   outputs:
>     dev:
>       type: bigquery
>       method: oauth
>       project: <your-gcp-project-id>
>       dataset: retail_dummyjson
>       threads: 1
>       location: US
> ```

## Status

Scaffolding in progress — environment and repository foundation only.
