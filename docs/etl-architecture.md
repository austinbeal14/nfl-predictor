# ETL Architecture

## Goal

Load nflverse schedule data into PostgreSQL safely, repeatably, and with enough
metadata to reproduce or audit every load.

## Pipeline

```text
extract -> save raw snapshot -> parse -> validate -> transform -> load -> report
```

### Extract

- Retrieve a configured nflverse release URL over HTTPS.
- Set a request timeout and identify the source in logs.
- Never embed URLs, credentials, or dates in application logic; use typed
  configuration.

### Save raw snapshot

- Save the unmodified source file before transformation.
- Record source URL, retrieval time, file size, and SHA-256 checksum in
  `source_loads`.
- Do not edit raw files after saving them.

### Parse and validate

Parse with Polars. Validate before a database transaction begins:

- Required columns exist.
- Types can be converted to the project contract.
- `game_id` is non-null and unique in the source file.
- Completed regular-season games contain both final scores.
- Team codes, dates, and `game_type` values are valid.
- A load cannot unexpectedly overwrite a game with incompatible identity data.

### Transform

- Rename source columns only at the adapter boundary.
- Normalize dates, team codes, nullable values, and game type values.
- Retain source values rather than calculating model features in this step.
- Treat a neutral-site game explicitly; a designated `home_team` is not always
  a physical home-field advantage.

### Load

- Create a `source_loads` row with `started` status.
- Upsert games by `source_game_id` in one transaction.
- Mark the load `succeeded` only after all game rows commit.
- On failure, roll back game writes and record the error summary.

## Idempotency

Running the same file twice must not create duplicate games. The preferred
behavior is an upsert that updates source fields only when the new source data
is newer or differs in an expected, auditable way.

## Initial commands

The first implementation should expose separate commands:

- `download-schedules` — retrieve and save a source snapshot
- `validate-schedules` — validate a local snapshot without database writes
- `load-schedules` — load a validated snapshot

Do not combine these into one opaque command until each stage is understood and
tested.

## Observability

Each run must log an ID, source URL, checksum, parsed row count, loaded row
count, validation failures, and elapsed duration. The command exit status must
be non-zero on failure.
