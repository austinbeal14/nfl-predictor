# GridironIQ

GridironIQ is a portfolio-quality NFL analytics and game-prediction platform.
Version 1 predicts completed and upcoming regular-season game outcomes using
historical team and game data.

This repository is intentionally being built as an end-to-end software product:
data ingestion, validation, storage, feature generation, model evaluation, API,
and user interface. It is not a single notebook or a one-off model.

## V1 scope

- Win probability
- Predicted home and away scores
- Predicted point differential
- Model performance and prediction explanations

V1 excludes player predictions, fantasy projections, betting advice, LLMs,
chatbots, and real-time in-game predictions.

## Documentation

- [Product vision](docs/vision.md)
- [Project context and working principles](docs/context.md)
- [Architecture](docs/architecture.md)
- [Data-source decision](docs/data-sources.md)
- [Data exploration plan](docs/data-exploration.md)
- [Database design](docs/database-design.md)
- [ETL architecture](docs/etl-architecture.md)
- [Modeling plan](docs/modeling-plan.md)
- [API design](docs/api-design.md)
- [Engineering workflow](docs/engineering-workflow.md)
- [Delivery plan](docs/delivery-plan.md)

## Status

Documentation and design are complete enough to begin the repository scaffold.
The first implementation milestone is defined in the delivery plan.
