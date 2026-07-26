# API Design

## Purpose

Define a small, read-focused HTTP API for the frontend. The API serves persisted
data; pipeline and training commands remain out of band.

## Conventions

- Base path: `/api/v1`
- JSON request and response bodies
- UTC ISO 8601 timestamps
- Stable, explicit response schemas defined with Pydantic
- Pagination for collection endpoints before large datasets are exposed
- A consistent error body: `code`, `message`, and optional `details`

## Initial endpoints

### `GET /health`

Returns service and database readiness. It is for local orchestration and
monitoring, not product data.

### `GET /api/v1/games`

Lists games, filtered by `season`, `week`, `game_type`, or `date`. The initial
response includes only public game identity and final score where available.

### `GET /api/v1/games/{source_game_id}`

Returns one game and its stored final score or scheduled state.

### `GET /api/v1/predictions`

Lists the latest eligible prediction for games matching supported filters.
Default behavior must be documented explicitly before implementation.

### `GET /api/v1/predictions/{source_game_id}`

Returns the current selected model prediction for one game, including model
version and generated timestamp. Return `404` if the game does not exist and
`409` or a documented empty response if the game exists but has no prediction.

## Prediction response contract

```json
{
  "game_id": "2025_01_DAL_PHI",
  "season": 2025,
  "week": 1,
  "gameday": "2025-09-04",
  "away_team": "DAL",
  "home_team": "PHI",
  "home_win_probability": 0.62,
  "predicted_home_score": 24.1,
  "predicted_away_score": 20.3,
  "predicted_point_differential": 3.8,
  "confidence": null,
  "model_version": "baseline-v1",
  "generated_at": "2025-09-01T12:00:00Z"
}
```

The values above are illustrative. `confidence` remains `null` until its
statistical definition is implemented and documented.

## Non-goals

Authentication, write endpoints, user preferences, background-job triggers,
and prediction generation through HTTP are outside V1's first vertical slice.
