# Architecture Overview

## Goals

The application is being shaped as an NFL game prediction service that blends
schedule context, player quality, injuries, and team-level ratings into a single
game outlook.

## Current Foundation

The current starter implementation provides:

- a centralized settings model in `crawler.config`
- a prediction API in `crawler.main`
- request and response schemas in `crawler.models`
- a heuristic scoring engine in `crawler.predictor`

## Target System Design

```text
             +----------------------+
             |     FastAPI API      |
             | /predict /health     |
             +----------+-----------+
                        |
                        v
             +----------------------+
             |   Prediction Engine  |
             | weighted heuristics   |
             +----------+-----------+
                        |
        +---------------+----------------+
        |               |                |
        v               v                v
+---------------+ +--------------+ +----------------+
| Team Ratings  | | Injuries     | | Schedule/Game  |
| overall/off/d | | status/impact| | week/rest/trip |
+-------+-------+ +------+-------+ +--------+-------+
        \                |                 /
         \               |                /
          \              v               /
           +----------------------------+
           | Factor Breakdown + Output  |
           | winner/probability/margin  |
           +----------------------------+
```

## Component Responsibilities

### API Layer

- Accept a home team, away team, and matchup context.
- Expose health and readiness endpoints.
- Return a prediction plus factor-level explanations.

### Orchestration Layer

- Combine roster grades, injuries, rest, travel, and game context.
- Apply configurable weights from environment settings.
- Compress certainty slightly for divisional games.

### Worker Layer

- Evaluate base team strength.
- Add key-player bonuses and injury penalties.
- Adjust for weather, venue, urgency, and travel.

### Data Layer

- Team, injury, and schedule inputs are request-driven today.
- Future versions can ingest external NFL data feeds and historical results.

### Observability Layer

- Future versions can track prediction accuracy, calibration, and input freshness.

## Local Development Flow

For now, the local development loop is intentionally small:

1. configure environment values with `.env`
2. run the FastAPI service locally
3. send prediction payloads to `/predict`
4. validate with Ruff, Black, and Pytest

## Future Data and Model Architecture

The next useful extensions are:

- **Schedule ingestion** from a maintained NFL schedule feed
- **Roster and injury ingestion** from authoritative team or league sources
- **Historical results store** for backtesting and calibration
- **Model evaluation jobs** for weekly retraining or weight tuning
- **Prediction monitoring** for drift, confidence, and accuracy

## Roadmap

1. add live schedule, roster, and injury ingestion
2. store historical game outcomes for calibration
3. replace heuristic weights with data-driven training
4. add richer matchup inputs such as trenches, weather severity, and coaching
5. track weekly model performance over the season
