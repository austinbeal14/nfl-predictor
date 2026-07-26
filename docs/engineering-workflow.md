# Engineering Workflow

## Development rules

- Work in small vertical slices with a runnable state after each slice.
- Write a failing test for behavior when practical, then implement the smallest
  change that makes it pass.
- Keep functions and modules single-purpose; avoid shared utility modules until
  duplication is real.
- Use type hints for public Python interfaces and strict schemas at system
  boundaries.
- Commit coherent changes with imperative messages.

## Quality gates

Before merging a feature, run the relevant formatter, linter, type checker,
unit tests, and integration tests. CI should run the same commands from the
start, even while the project is small.

## Testing strategy

| Test level | Purpose | Example |
| --- | --- | --- |
| Unit | Isolated logic | Score-label derivation and source validation |
| Integration | Real boundaries | Load a fixture into PostgreSQL |
| API | HTTP contract | Prediction endpoint response and error behavior |
| End-to-end | Critical user flow | Ingest fixture -> serve game -> display prediction |

Use small, checked-in fixture files for tests. Do not make normal tests depend
on an external nflverse download.

## Configuration and secrets

- Keep local configuration in `.env`, excluded from Git.
- Commit a `.env.example` containing variable names and safe placeholders.
- Validate required configuration at startup.
- Never commit API keys, database passwords, downloaded raw data, or model
artifacts unless a later explicit decision changes that policy.

## Definition of done

A task is done when its intended behavior is implemented, tested, documented
where it changes a contract, formatted, and usable through the documented local
workflow.
