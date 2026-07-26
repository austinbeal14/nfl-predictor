# Database Design

## Purpose

Define the minimal PostgreSQL model needed to ingest games, create reproducible
features, train models, and serve persisted predictions. The schema should grow
through Alembic migrations, not manual database changes.

## Conventions

- Use `uuid` primary keys for internal entities and preserve external IDs in
  unique columns.
- Store timestamps as `timestamptz` in UTC.
- Use `created_at` and `updated_at` on mutable application tables.
- Use database constraints for identity, required relationships, and allowed
  states; do not rely only on application validation.
- Preserve source metadata so every record can be traced to a load run.

## Initial entities

```text
source_loads 1--* games 1--* team_game_features
feature_sets 1--* team_game_features
model_runs 1--* predictions
games 1--* predictions
```

### `source_loads`

Records one source retrieval and validation attempt.

| Column | Notes |
| --- | --- |
| `id` | Internal UUID primary key |
| `source_name` | Initially `nflverse` |
| `source_url` | Exact downloaded URL |
| `source_checksum` | File hash for reproducibility |
| `retrieved_at` | Retrieval timestamp |
| `status` | `started`, `succeeded`, or `failed` |
| `row_count` | Source row count after parsing |
| `validation_summary` | Structured validation result |

### `games`

Stores source game records; it is not a prediction table.

| Column | Notes |
| --- | --- |
| `id` | Internal UUID primary key |
| `source_game_id` | Unique nflverse `game_id` |
| `season`, `week`, `game_type`, `gameday` | Game calendar identity |
| `home_team_code`, `away_team_code` | Source team codes |
| `home_score`, `away_score` | Nullable until completed |
| `location`, `overtime` | Source game context |
| `source_load_id` | Foreign key to `source_loads` |

Constraint: unique `source_game_id`. For V1 training, select only games where
`game_type = 'REG'` and both scores are present.

### `feature_sets`

Defines an immutable, named feature specification.

| Column | Notes |
| --- | --- |
| `id` | UUID primary key |
| `name`, `version` | Unique human-readable identity |
| `definition` | JSON description of columns and computation rules |
| `cutoff_policy` | Statement of the no-future-data rule |

### `team_game_features`

Stores a feature snapshot for one team before one game. A game has two rows,
one per participant.

| Column | Notes |
| --- | --- |
| `id` | UUID primary key |
| `game_id`, `feature_set_id` | Foreign keys |
| `team_code`, `opponent_team_code` | Feature perspective |
| `is_home` | Home/away context |
| `as_of_at` | Latest time represented by the features |
| `values` | JSON feature payload initially; normalize only proven query fields |

Constraint: unique (`game_id`, `feature_set_id`, `team_code`).

### `model_runs`

Records a reproducible training run.

| Column | Notes |
| --- | --- |
| `id` | UUID primary key |
| `model_name`, `model_version` | Model identity |
| `feature_set_id` | Feature specification used |
| `training_data_cutoff` | Latest game date included in training |
| `parameters`, `metrics` | JSON artifacts of the run |
| `artifact_uri`, `artifact_checksum` | Stored model location and integrity |
| `status` | `running`, `succeeded`, or `failed` |

### `predictions`

Persists output from a completed model run for one game.

| Column | Notes |
| --- | --- |
| `id` | UUID primary key |
| `game_id`, `model_run_id` | Foreign keys |
| `generated_at` | Prediction generation time |
| `home_win_probability` | Decimal in [0, 1] |
| `predicted_home_score`, `predicted_away_score` | Model outputs |
| `predicted_point_differential` | Derived output stored for API efficiency |
| `confidence` | Defined only after calibration work |
| `explanation` | Optional JSON summary |

Constraint: unique (`game_id`, `model_run_id`).

## Deferred entities

Teams, venues, coaches, injuries, player statistics, odds, and user accounts
are not required for the first vertical slice. Add them only when a concrete
feature or product workflow needs them.
