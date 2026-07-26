# Delivery Plan

## Milestone 0: Repository scaffold

Create the target directories, Python project configuration, frontend project,
Docker Compose PostgreSQL service, environment example, formatting/linting,
and a minimal CI workflow. Verify a clean checkout can run the quality gates.

**Done when:** the repository has a repeatable local setup and a passing health
check from the backend to PostgreSQL.

## Milestone 1: Schedule ingestion vertical slice

Implement source download, raw snapshot metadata, validation, and idempotent
loading of a small schedule fixture and then real historical nflverse data.

**Done when:** a command can load 2023–2025 regular-season games, rerun without
duplicates, reject an invalid fixture, and report its load metadata.

## Milestone 2: Game read API

Implement the game schema, migration, and read-only game endpoints.

**Done when:** API tests prove filtering and not-found behavior, and the API
returns games loaded in Milestone 1.

## Milestone 3: Baseline feature and model pipeline

Create strictly pre-game rolling team features, a chronological train/test
split, a simple baseline model, evaluation metrics, and stored model metadata.

**Done when:** the training run is reproducible, uses no future information,
and outputs documented performance metrics against a held-out future season.

## Milestone 4: Persisted predictions and API

Generate and store predictions from a successful model run, then expose them
through the prediction endpoint.

**Done when:** every API prediction identifies its model version and generated
time, and endpoint tests pass.

## Milestone 5: Web experience

Build a minimal Next.js interface for selecting a week, viewing games, and
viewing prediction details and model performance.

**Done when:** the frontend consumes the documented API contract without mock
data in the main workflow.

## Milestone 6: Operational polish

Add CI, containerized local startup, structured logging, documentation updates,
and an architecture walkthrough suitable for the portfolio README.

## Explicit sequencing rule

Do not start ML training before Milestone 1 is complete and its data-quality
checks are trusted. Do not start frontend work before a real API contract exists.
