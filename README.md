# NFL Game Predictor

This repository now exposes a minimal FastAPI-based NFL game predictor. It accepts
team strength, schedule context, player availability, and injuries, then returns a
winner, win probabilities, a projected margin, and the biggest matchup factors.

## Repository Layout

```text
adaptive-crawler/
├── crawler/
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   └── predictor.py
├── docs/
│   └── architecture.md
├── tests/
├── .env.example
├── pyproject.toml
└── requirements.txt
```

## System Architecture Overview

The current codebase establishes the foundation for four core layers:

1. **Prediction API** via FastAPI.
2. **Scoring engine** for roster, injuries, and schedule effects.
3. **Configuration** through environment-driven weights.
4. **Extension points** for future real data sources and model upgrades.

See `/home/runner/work/adaptive-crawler/adaptive-crawler/docs/architecture.md` for the
prediction architecture and future data-ingestion direction.

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

4. Start the API:

   ```bash
   uvicorn crawler.main:app --reload
   ```

5. Run quality checks:

   ```bash
   ruff check .
   black --check .
   pytest
   ```

## Example Prediction Request

```json
{
  "home_team": {
    "name": "Detroit Lions",
    "overall_rating": 91,
    "offense_rating": 93,
    "defense_rating": 84,
    "quarterback_rating": 90,
    "recent_form": 5,
    "rest_days": 7,
    "travel_miles": 0,
    "key_players": [
      { "name": "Amon-Ra St. Brown", "position": "WR", "impact_rating": 8.5 }
    ],
    "injuries": []
  },
  "away_team": {
    "name": "Green Bay Packers",
    "overall_rating": 88,
    "offense_rating": 87,
    "defense_rating": 85,
    "quarterback_rating": 86,
    "recent_form": 2,
    "rest_days": 6,
    "travel_miles": 320,
    "key_players": [],
    "injuries": [
      {
        "player_name": "Starting Left Tackle",
        "position": "OL",
        "status": "questionable",
        "impact_rating": 7
      }
    ]
  },
  "context": {
    "week": 10,
    "divisional_game": true,
    "neutral_site": false,
    "weather": "wind",
    "playoff_urgency_home": 4,
    "playoff_urgency_away": 3
  }
}
```

## Current Status

This repository intentionally includes a lightweight heuristic model rather than a
historical machine-learning pipeline. It is ready to accept schedule, roster, and
injury inputs now, and it can be extended later with live NFL data sources.
