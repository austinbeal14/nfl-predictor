# Architecture

## Decision

GridironIQ V1 will be a modular monorepo with a batch-oriented data and model
pipeline. The web application reads predictions from an API; it does not train
models or access raw data directly.

## Components

```text
nflverse files
    -> ingestion and validation
    -> PostgreSQL operational store + versioned raw files
    -> feature generation
    -> model training and evaluation
    -> persisted model artifacts and predictions
    -> FastAPI
    -> Next.js web application
```

### Responsibilities

| Component | Responsibility | Must not do |
| --- | --- | --- |
| ETL | Retrieve, validate, and load source data | Train or serve models |
| PostgreSQL | Store normalized application and pipeline data | Perform exploratory analytics at scale |
| DuckDB | Local analytical queries during development and training | Become a second production source of truth |
| ML package | Build features, train, evaluate, and generate predictions | Fetch external data directly |
| FastAPI | Expose stable read APIs and operational endpoints | Run long training jobs in a request |
| Next.js | Render product workflows | Contain model or business rules |

## Runtime modes

1. **Local development:** Docker Compose runs PostgreSQL and supporting
   services. Python and frontend commands may initially run on the host for
   rapid iteration.
2. **Batch jobs:** Ingestion, feature generation, training, and prediction
   generation are explicit commands. They are idempotent and produce logs.
3. **Application serving:** The API only reads persisted data and model output.

## Core principles

- Use one source of truth per concern: PostgreSQL for application data,
  versioned files for raw source snapshots, and a registered artifact for a
  trained model.
- Keep external-provider code behind a small source adapter.
- Make time explicit. A feature for a game may use only data known before that
  game's kickoff.
- Start as a modular monolith. Do not introduce queues, microservices, or a
  model-serving platform in V1.

## Target repository layout

```text
backend/       FastAPI application and API tests
etl/           source adapters, validation, and load jobs
ml/            feature, training, evaluation, and prediction modules
database/      migrations and database documentation
frontend/      Next.js application
infra/         Docker and Docker Compose configuration
scripts/       developer commands that compose project modules
tests/         cross-package integration tests
docs/          decisions, contracts, and operating guides
```
