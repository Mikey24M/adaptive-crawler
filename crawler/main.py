"""FastAPI entrypoint for the NFL predictor service."""

from fastapi import FastAPI

from crawler.config import get_settings
from crawler.models import GamePredictionRequest, GamePredictionResponse
from crawler.predictor import predict_game


def create_app() -> FastAPI:
    """Create the FastAPI application."""

    settings = get_settings()
    app = FastAPI(
        title="NFL Game Predictor",
        version="0.1.0",
        description=(
            "Predict NFL games from team strength, player availability, "
            "injuries, and schedule context."
        ),
    )

    @app.get("/")
    def root() -> dict[str, object]:
        return {
            "service": "nfl-game-predictor",
            "status": "ready",
            "sport": "nfl",
            "features": {
                "prediction_api": True,
                "schedule_context": True,
                "player_inputs": True,
                "injury_adjustments": True,
                "factor_breakdown": True,
            },
            "model_tuning": {
                "home_field_edge": settings.home_field_edge,
                "rest_day_edge_per_day": settings.rest_day_edge_per_day,
                "injury_edge_multiplier": settings.injury_edge_multiplier,
            },
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/predict", response_model=GamePredictionResponse)
    def predict(payload: GamePredictionRequest) -> GamePredictionResponse:
        return predict_game(payload, settings)

    return app


app = create_app()
