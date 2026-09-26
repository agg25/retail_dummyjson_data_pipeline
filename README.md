# retail_dummyjson_data_pipeline

[![CI](https://github.com/agg25/retail_dummyjson_data_pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/agg25/retail_dummyjson_data_pipeline/actions)

An end-to-end data engineering project I built to practice the whole flow: pulling data
from an API, landing it in a warehouse, transforming it with dbt, adding tests, and wiring
up CI.

The data comes from [DummyJSON](https://dummyjson.com) — a free fake e-commerce API (no
key needed) with realistic products, carts and users. It loads into **Google BigQuery**
(free tier) and gets modelled with **dbt**.

## Pipeline

```
DummyJSON API
    -> Parquet files (local raw layer)
    -> BigQuery (raw_* tables)
    -> dbt staging -> intermediate -> marts
```

## Why these choices

- **DummyJSON** — free, no auth, and the data actually looks like an e-commerce store.
- **BigQuery** — free tier, nothing to host myself, and dbt has a solid adapter for it.
- **Prefect** — Python-native orchestration, runs locally without needing Docker.
- **uv** — quick, reproducible Python env and dependency management.

## Tech

Python 3.11, uv, httpx, polars, pyarrow, Google BigQuery, dbt-bigquery, Prefect, pytest,
ruff, mypy, GitHub Actions.

## Quick start

```powershell
uv sync                    # create the venv + install dependencies
uv run retail-orchestrate  # run the whole pipeline (Prefect)
```

Individual steps, in case you want to run them by hand:

```powershell
uv run retail-ingest     # 1. DummyJSON -> data/raw/*.parquet
uv run retail-load-bq    # 2. Parquet -> BigQuery raw tables
uv run dbt run --project-dir dbt --profiles-dir dbt    # 3. build the models
uv run dbt test --project-dir dbt --profiles-dir dbt   # 4. run the tests
uv run dbt docs generate --project-dir dbt --profiles-dir dbt  # 5. lineage docs
```

## Layout

- `src/retail_dummyjson_pipeline/` — ingestion, BigQuery loader, Prefect flow
- `dbt/models/` — staging / intermediate / marts
- `tests/` — pytest suite
- `data/raw/` — local Parquet staging (gitignored)
- `.github/workflows/` — CI

## Notes / gotchas

- `dbt/profiles.yml` is gitignored. Create it yourself before running dbt:
  ```yaml
  retail_dummyjson:
    target: dev
    outputs:
      dev:
        type: bigquery
        method: oauth
        project: <your-gcp-project-id>
        dataset: retail_dummyjson
        threads: 1
        location: US
  ```
- The GCP project id is also in `dbt/models/staging/sources.yml`. It's just an identifier
  (not a secret), but swap in your own if you clone the repo.

## Things I'd still like to add

- Docker / containerisation
- A scheduled Prefect deployment
- Terraform for the GCP setup
- dbt elementary for data observability

