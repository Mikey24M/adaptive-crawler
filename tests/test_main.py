from fastapi.testclient import TestClient

from crawler.main import app


def test_root_exposes_predictor_metadata() -> None:
    response = TestClient(app).get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "nfl-game-predictor"
    assert payload["sport"] == "nfl"
    assert payload["features"]["injury_adjustments"] is True


def test_predict_endpoint_returns_prediction() -> None:
    response = TestClient(app).post(
        "/predict",
        json={
            "home_team": {
                "name": "Buffalo Bills",
                "overall_rating": 92,
                "offense_rating": 91,
                "defense_rating": 87,
                "quarterback_rating": 94,
                "recent_form": 4,
                "rest_days": 7,
                "travel_miles": 0,
                "key_players": [
                    {
                        "name": "Josh Allen",
                        "position": "QB",
                        "impact_rating": 10,
                    }
                ],
                "injuries": [],
            },
            "away_team": {
                "name": "Miami Dolphins",
                "overall_rating": 88,
                "offense_rating": 89,
                "defense_rating": 80,
                "quarterback_rating": 84,
                "recent_form": 1,
                "rest_days": 6,
                "travel_miles": 1200,
                "key_players": [],
                "injuries": [
                    {
                        "player_name": "Starting LT",
                        "position": "OL",
                        "status": "out",
                        "impact_rating": 7,
                    }
                ],
            },
            "context": {
                "week": 9,
                "divisional_game": True,
                "neutral_site": False,
                "weather": "wind",
                "playoff_urgency_home": 4,
                "playoff_urgency_away": 3,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["predicted_winner"] == "Buffalo Bills"
    assert payload["home_win_probability"] > payload["away_win_probability"]
    assert payload["factors"]
