# Data Exploration Plan

## Purpose

Validate the nflverse schedule dataset before implementing ingestion or a
database schema. This document records observations from actual downloaded data;
it is not a substitute for the source data dictionary.

## Source under evaluation

- Provider: nflverse
- Dataset: Game and schedule data
- Access: Public CSV or Parquet release over HTTPS
- Initial sample: 2023, 2024, and 2025 completed seasons

## Schema findings from the source data dictionary

The dataset provides `game_id`, `season`, `game_type`, `week`, `gameday`,
`home_team`, `away_team`, `home_score`, `away_score`, `location`, and
`overtime`. These fields satisfy the initial game-record requirements.

`result` and `total` are calculated from final scores and are labels or derived
post-game values, not model features. Betting fields such as `spread_line` and
moneylines are excluded from V1 features. Weather, roof, surface, coach, and
starting-quarterback fields are deferred until their pre-game availability is
verified.

## Exploration procedure

For a downloaded sample, record the following results.

| Check | Expected result | Observed result | Pass? |
| --- | --- | --- | --- |
| File URL, format, and download date | Recorded | [Fill after download] | [ ] |
| Date range | Includes 2023–2025 | [Fill] | [ ] |
| `game_id` duplicates | Zero | [Fill] | [ ] |
| Required column names and types | Present and usable | [Fill] | [ ] |
| `game_type` values | Includes `REG`; postseason values documented | [Fill] | [ ] |
| Missing scores for completed games | Zero | [Fill] | [ ] |
| Missing team identifiers | Zero | [Fill] | [ ] |
| Regular-season games per season | Plausible NFL totals | [Fill] | [ ] |
| Tie, neutral-site, and unplayed-game representation | Explicit and documented | [Fill] | [ ] |

## Acceptance decision

The dataset passes this exploration when all required fields are present,
`game_id` is unique, completed regular-season games have final scores, and the
observed values support the stated transformations. Record exceptions below.

### Exceptions and decisions

- [Add each observed exception, its handling rule, and rationale.]

## Follow-on implementation contract

The first ingestion job must reject a load when required columns are missing,
when a completed regular-season game lacks a score, or when duplicate source
game identifiers are found. It must report the failed validation clearly.
