# Modeling Plan

## Purpose

Define the first model workflow without prematurely selecting complex models or
features. The purpose of V1 modeling is to establish a trustworthy benchmark,
not to maximize a leaderboard score.

## Prediction targets

The first model pipeline produces three related outputs:

1. Home-team win probability
2. Home-team score and away-team score
3. Home-team point differential

Point differential can be predicted directly or calculated from predicted
scores. The implementation must document which approach is used and evaluate
the outputs separately.

## Training population

- Include completed regular-season (`REG`) games only for the first baseline.
- Begin with seasons 2006–2025, subject to the data-exploration result.
- Exclude games with missing scores or invalid source identities.
- Keep the 2025 season as an initial holdout evaluation season; do not shuffle
  games across time.

## Feature policy

Every feature must be known before the target game's kickoff. This rule is more
important than feature count.

### First feature set

Start with simple rolling, team-level features calculated only from prior
completed games:

- Rolling win percentage
- Rolling average points scored
- Rolling average points allowed
- Rolling average point differential
- Number of prior games in the season
- Home/away indicator
- Division-game indicator, after source validity is verified

Use a fixed lookback window and define its behavior when fewer than that many
prior games exist. The feature set version must capture this choice.

### Excluded initially

- Final score-derived columns (`result`, `total`)
- Betting lines and odds
- Any field that is only known after kickoff or after the game
- Player-level data, injuries, and starting quarterbacks
- Manual rankings, subjective power ratings, or outside predictions

## Baselines

Implement and evaluate simple baselines before a machine-learning model:

1. Home-team-always-wins probability baseline
2. Historical league home-win-rate baseline
3. Team rolling-win-rate baseline

The first learned model should be an interpretable scikit-learn model. Choose a
logistic-regression classifier for win probability and a regularized linear
regression model for score or point differential. Do not introduce XGBoost or
SHAP until these baselines and data-leakage checks are working.

## Evaluation

| Output | Primary metrics | Secondary checks |
| --- | --- | --- |
| Win probability | Log loss and Brier score | Calibration curve, accuracy |
| Score prediction | MAE and RMSE | Error by home/away team |
| Point differential | MAE and RMSE | Error distribution |

Use a chronological split: train on seasons through 2024, tune only within
earlier historical periods, and evaluate once on 2025. If cross-validation is
added, use time-based folds rather than random folds.

## Reproducibility requirements

Each model run must record the feature-set version, training data cutoff,
training and evaluation row counts, parameters, random seed, metrics, artifact
checksum, and code revision when available.

## Confidence definition

Do not expose a confidence value until it has a written statistical definition.
The likely V1 definition is calibrated probability confidence: the distance of
the calibrated win probability from 0.5, accompanied by calibration metrics.
This must not be presented as a guarantee of correctness.
