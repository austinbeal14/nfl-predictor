# Data Source Selection

## Status

- Status: Accepted
- Owner: Austin Beal
- Date: 2026-07-26
- Review trigger: Before adding live data, player predictions, or a public deployment

## Purpose

Select the primary source of historical NFL game data for Version 1 of
GridironIQ.

V1 predicts NFL game outcomes. It does not include player predictions, fantasy
projections, betting advice, or real-time predictions.

## Decision Summary

**Decision:** Use nflverse game and schedule data as the primary V1 source.

**Why:** It provides the required historical game fields in public,
machine-readable files that can be downloaded from Python without an API key or
paid subscription. Its published data dictionary also makes the schema easier
to validate and document.

**Primary tradeoff:** nflverse is a community-maintained data release rather
than a contractual commercial API. It is therefore suitable for V1 historical
data, but not yet a guarantee of production-grade live-data availability.

## V1 Data Requirements

The selected source must provide historical data for completed NFL games.

| Field | Why it is needed | Required? |
| --- | --- | --- |
| `game_id` | Prevent duplicate imports and join related data later | Yes |
| `season` | Partition training and evaluation data by season | Yes |
| `week` and `gameday` | Order games without using future information | Yes |
| `game_type` | Separate regular season and postseason games | Yes |
| `home_team` | Identify the designated home competitor | Yes |
| `away_team` | Identify the designated away competitor | Yes |
| `home_score` | Training label and score-difference calculation | Yes |
| `away_score` | Training label and score-difference calculation | Yes |

The schedule dataset documents these fields. `game_id` is the primary game
identifier; `game_type` distinguishes regular season (`REG`) from postseason
games; and unplayed games have missing score fields.

### Deferred fields

Weather, stadium, betting lines, injuries, rosters, and player statistics are
not required for the first ingestion pipeline. They may become features in a
later iteration after the base game dataset is validated.

## Source Evaluation Criteria

| Criterion | Importance | Evaluation |
| --- | ---: | --- |
| Data completeness | High | Contains every required V1 field |
| Reliability | High | Has documented, repeatable access |
| Terms and license | High | Permits portfolio use with required attribution |
| Cost | High | Free for local development |
| Historical coverage | High | Supports a multi-season training set |
| Data format | Medium | CSV or Parquet can be read from Python |
| Update cadence | Medium | Refreshes during an NFL season |
| Documentation | Medium | Provides a data dictionary and access guidance |
| Enrichment potential | Low | Can later support team-level feature engineering |

## Candidate Sources

### Candidate 1: nflverse game and schedule data

- Access method: Public CSV or Parquet data releases retrieved over HTTPS. This
  is file-based data access, not a traditional REST API.
- Cost: Free.
- Historical coverage: Use 2006 through the latest completed season for the
  initial training dataset. Verify exact coverage during exploration before
  expanding the range.
- Update cadence: nflverse documents game/schedule updates every five minutes
  during the season.
- License: nflverse-data is published under CC BY 4.0. Preserve attribution in
  project documentation and confirm the license for each additional dataset.
- Strengths:
  - Includes the V1 game identifiers, schedule, teams, game type, and scores.
  - Uses machine-readable formats compatible with Polars.
  - Does not require an API key or paid plan.
  - Includes a published data dictionary and future datasets for enrichment.
- Limitations:
  - Community-maintained rather than governed by a commercial SLA.
  - Schema or release locations can change; the ETL must validate inputs.
  - Does not by itself provide a contractual real-time data feed.
- V1 fit: Good.

### Candidate 2: Sportradar NFL API

- Access method: Authenticated REST API.
- Cost: Commercial; trial access requires an API key and must be evaluated
  separately.
- Historical coverage: Vendor-dependent; verify against the subscribed product.
- Strengths:
  - Supported API contract appropriate for a later production integration.
  - NFL schedule endpoints are documented.
- Limitations:
  - Adds credentials, quotas, vendor dependency, and likely cost.
  - Does not meet the V1 no-paid-services constraint as the primary source.
- V1 fit: Partial; revisit for future live or commercial deployment needs.

### Candidate 3: SportsDataIO NFL API

- Access method: Authenticated REST API returning JSON or XML.
- Cost: Commercial for real production data.
- Historical coverage: Available through paid products; verify before use.
- Strengths:
  - Provides a conventional vendor API for evaluating an integration design.
- Limitations:
  - Its free trial uses scrambled data, so it cannot train or validate a real
    prediction model.
  - Adds credentials, quotas, and cost that V1 does not need.
- V1 fit: Poor as the primary V1 data source; a future comparison option only.

## Comparison

| Criterion | nflverse | Sportradar | SportsDataIO |
| --- | --- | --- | --- |
| Required V1 fields | Yes | Verify by product | Verify by product |
| Free real historical data | Yes | Trial-dependent | No; trial data is scrambled |
| Automated access | Yes, HTTPS files | Yes, authenticated API | Yes, authenticated API |
| API key required | No | Yes | Yes |
| Published schema documentation | Yes | Yes | Yes |
| Fits V1 constraints | Yes | No | No |

## Chosen Source

### Rationale

nflverse wins because it meets all V1 hard constraints: free access, real
historical game data, automated retrieval, and a documented schema. The project
does not yet need live updates, a vendor SLA, or paid API features. Starting
with files also keeps the initial ETL focused on the fundamentals: download,
validate, transform, store, and reproduce a dataset.

### Access and ingestion assumptions

- Data format: Prefer Parquet for local analytical processing; use CSV only
  when inspecting data manually or when a release does not provide Parquet.
- Retrieval method: Download the selected public release URL over HTTPS with
  `httpx`; read the file with Polars.
- Initial historical range: 2006–2025. Do not include 2026 in model training
  until its games are complete and the data-quality checks pass.
- Refresh cadence: No recurring refresh is needed until an in-season product
  feature is planned. When added, retrieve on a scheduled cadence and process
  only completed games.
- Raw-data storage: Store original downloaded files outside the transformed
  database, with the source URL, download timestamp, and checksum recorded.
- Dependency decision: Do not start with an nflverse Python wrapper. Direct
  file retrieval makes the source boundary and ETL behavior explicit. Revisit
  `nflreadpy` only if it reduces verified maintenance without hiding needed
  pipeline behavior.

### Data-quality rules to verify

1. `game_id` is unique in the selected dataset.
2. Completed regular-season games have both scores populated.
3. `home_team` and `away_team` are populated and use a consistent code system.
4. `game_type` equals `REG` for the initial V1 training population.
5. A game date and week exist and can order games within a season.
6. Ties, neutral-site games, postponed games, and games without final scores
   have explicit, documented handling.
7. The data contains no games dated after the intended training cutoff.

## Rejected Alternatives

### Scraping Pro-Football-Reference, ESPN, or NFL web pages

Rejected because web pages and undocumented endpoints are not stable ingestion
contracts. They can change without notice and introduce scraping, rate-limit,
and terms-of-use risk.

Reconsider only when a specific field is unavailable from documented sources,
the site's terms permit the intended automation, and the source is isolated
behind an adapter with a fallback.

### Kaggle or other one-off datasets

Rejected because they are useful for exploration but do not provide a controlled
refresh process or consistent provenance for a production-style data platform.

Reconsider only as a static, clearly attributed supplemental dataset.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Source schema changes | ETL can break | Validate expected columns and types before loading |
| Historical corrections | Features or labels can change | Preserve raw files and record source version/checksum |
| Source becomes unavailable | Refreshes fail | Keep the source adapter small and document commercial fallbacks |
| Attribution omitted | License noncompliance | Keep source and CC BY attribution in project documentation |
| Future-data leakage | Invalid model evaluation | Split training and evaluation chronologically and enforce cutoff checks |

## Open Questions

- What exact public release URL and Parquet layout will the ingestion job use?
- Should the initial baseline use only regular-season games or include postseason
  games as a separate evaluation set?
- What data-retention policy should apply once raw downloads are stored locally?
- Which team-level, pre-game features should be added after the base dataset is
  stable?

## References

- [nflverse overview](https://github.com/nflverse)
- [nflverse schedule loader documentation](https://nflreadr.nflverse.com/reference/load_schedules.html)
- [nflverse schedule data dictionary](https://nflreadr.nflverse.com/articles/dictionary_schedules.html)
- [nflverse data update schedule](https://nflreadr.nflverse.com/articles/nflverse_data_schedule.html)
- [Sportradar NFL API overview](https://developer.sportradar.com/football/docs/nfl-ig-api-basics)
- [SportsDataIO API access documentation](https://sportsdata.io/developers/apis)

## Next Step

Create `docs/data-exploration.md` and inspect a small nflverse schedule sample
before writing ETL code. Record the exact URL, fields observed, types, null
counts, duplicate `game_id` count, date range, and any data-quality exceptions.
