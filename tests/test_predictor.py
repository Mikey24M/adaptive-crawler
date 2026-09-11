from crawler.config import Settings
from crawler.models import (
    GameContext,
    GamePredictionRequest,
    InjuryReport,
    PlayerStatus,
    TeamProfile,
    WeatherOutlook,
)
from crawler.predictor import predict_game


def test_predict_game_penalizes_injuries_and_travel() -> None:
    prediction = predict_game(
        GamePredictionRequest(
            home_team=TeamProfile(
                name="San Francisco 49ers",
                overall_rating=90,
                offense_rating=89,
                defense_rating=90,
                quarterback_rating=85,
                recent_form=3,
                rest_days=8,
                travel_miles=0,
            ),
            away_team=TeamProfile(
                name="Seattle Seahawks",
                overall_rating=88,
                offense_rating=85,
                defense_rating=82,
                quarterback_rating=83,
                recent_form=1,
                rest_days=6,
                travel_miles=800,
                injuries=[
                    InjuryReport(
                        player_name="Edge Rusher",
                        position="DL",
                        status=PlayerStatus.OUT,
                        impact_rating=8,
                    )
                ],
            ),
            context=GameContext(
                week=13,
                divisional_game=True,
                weather=WeatherOutlook.RAIN,
                playoff_urgency_home=4,
                playoff_urgency_away=2,
            ),
        ),
        Settings(_env_file=None),
    )

    assert prediction.predicted_winner == "San Francisco 49ers"
    assert prediction.home_win_probability > 0.5
    assert any(factor.category == "injuries" for factor in prediction.factors)
    assert "San Francisco 49ers" in prediction.summary


def test_predict_game_can_pick_away_team() -> None:
    prediction = predict_game(
        GamePredictionRequest(
            home_team=TeamProfile(
                name="New York Giants",
                overall_rating=72,
                offense_rating=68,
                defense_rating=70,
                quarterback_rating=66,
                recent_form=-2,
                rest_days=5,
                travel_miles=0,
            ),
            away_team=TeamProfile(
                name="Philadelphia Eagles",
                overall_rating=94,
                offense_rating=92,
                defense_rating=88,
                quarterback_rating=90,
                recent_form=6,
                rest_days=7,
                travel_miles=95,
            ),
            context=GameContext(
                week=16,
                divisional_game=False,
                weather=WeatherOutlook.CLEAR,
                playoff_urgency_home=1,
                playoff_urgency_away=5,
            ),
        ),
        Settings(_env_file=None),
    )

    assert prediction.predicted_winner == "Philadelphia Eagles"
    assert prediction.away_win_probability > prediction.home_win_probability
    assert prediction.projected_margin > 0
