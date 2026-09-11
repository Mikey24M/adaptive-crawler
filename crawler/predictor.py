"""Heuristic NFL game prediction engine."""

from __future__ import annotations

from math import exp

from crawler.config import Settings
from crawler.models import (
    FactorImpact,
    GamePredictionRequest,
    GamePredictionResponse,
    PlayerStatus,
    TeamProfile,
    WeatherOutlook,
)

STATUS_WEIGHTS = {
    PlayerStatus.ACTIVE: 0.0,
    PlayerStatus.QUESTIONABLE: 0.35,
    PlayerStatus.DOUBTFUL: 0.7,
    PlayerStatus.OUT: 1.0,
    PlayerStatus.INJURED_RESERVE: 1.1,
}


def predict_game(
    request: GamePredictionRequest,
    settings: Settings,
) -> GamePredictionResponse:
    """Score an NFL matchup from roster, injury, and schedule context."""

    home = request.home_team
    away = request.away_team
    context = request.context

    factor_deltas = {
        "roster_strength": _roster_strength_delta(home, away),
        "quarterback": 0.16 * (home.quarterback_rating - away.quarterback_rating),
        "recent_form": 1.4 * (home.recent_form - away.recent_form),
        "key_players": settings.key_player_edge_multiplier
        * (_key_player_value(home) - _key_player_value(away)),
        "injuries": settings.injury_edge_multiplier
        * (_injury_burden(away) - _injury_burden(home)),
        "rest": settings.rest_day_edge_per_day * (home.rest_days - away.rest_days),
        "travel": settings.travel_penalty_per_500_miles
        * ((away.travel_miles - home.travel_miles) / 500),
        "venue": 0.0 if context.neutral_site else settings.home_field_edge,
        "weather": _weather_delta(home, away, context.weather),
        "playoff_urgency": 0.35
        * (context.playoff_urgency_home - context.playoff_urgency_away),
    }

    total_delta = sum(factor_deltas.values())
    if context.divisional_game:
        total_delta *= 0.92

    home_win_probability = 1 / (1 + exp(-total_delta / settings.confidence_smoothing))
    away_win_probability = 1 - home_win_probability
    predicted_winner = home.name if total_delta >= 0 else away.name
    confidence_tier = _confidence_tier(abs(home_win_probability - 0.5))
    projected_margin = round(total_delta * 0.75, 1)
    if predicted_winner == away.name:
        projected_margin = abs(projected_margin)

    factors = _build_factor_impacts(home, away, factor_deltas, context.divisional_game)
    summary = _build_summary(predicted_winner, factors, context.divisional_game)

    return GamePredictionResponse(
        predicted_winner=predicted_winner,
        home_win_probability=round(home_win_probability, 3),
        away_win_probability=round(away_win_probability, 3),
        projected_margin=projected_margin,
        confidence_tier=confidence_tier,
        factors=factors,
        summary=summary,
    )


def _roster_strength_delta(home: TeamProfile, away: TeamProfile) -> float:
    return (
        0.32 * (home.overall_rating - away.overall_rating)
        + 0.22 * (home.offense_rating - away.offense_rating)
        + 0.22 * (home.defense_rating - away.defense_rating)
    )


def _key_player_value(team: TeamProfile) -> float:
    return sum(player.impact_rating for player in team.key_players)


def _injury_burden(team: TeamProfile) -> float:
    return sum(
        injury.impact_rating * STATUS_WEIGHTS[injury.status] for injury in team.injuries
    )


def _weather_delta(
    home: TeamProfile,
    away: TeamProfile,
    weather: WeatherOutlook,
) -> float:
    if weather in {WeatherOutlook.INDOOR, WeatherOutlook.CLEAR}:
        return 0.0

    balance_delta = (home.defense_rating - home.offense_rating) - (
        away.defense_rating - away.offense_rating
    )
    multiplier = 0.04 if weather == WeatherOutlook.RAIN else 0.06
    if weather == WeatherOutlook.SNOW:
        multiplier = 0.08
    return balance_delta * multiplier


def _confidence_tier(probability_edge: float) -> str:
    if probability_edge >= 0.22:
        return "high"
    if probability_edge >= 0.12:
        return "medium"
    return "low"


def _build_factor_impacts(
    home: TeamProfile,
    away: TeamProfile,
    factor_deltas: dict[str, float],
    divisional_game: bool,
) -> list[FactorImpact]:
    explanations = {
        "roster_strength": (
            "overall roster strength, offense, and defense grades",
            "overall roster strength, offense, and defense grades",
        ),
        "quarterback": (
            "quarterback play gives the home side a cleaner path to efficient drives",
            "quarterback play gives the away side a cleaner path to efficient drives",
        ),
        "recent_form": (
            "recent form points toward the home side carrying better momentum",
            "recent form points toward the away side carrying better momentum",
        ),
        "key_players": (
            "star-player availability adds more top-end playmaking for the home side",
            "star-player availability adds more top-end playmaking for the away side",
        ),
        "injuries": (
            "the home roster is healthier in the most important spots",
            "the away roster is healthier in the most important spots",
        ),
        "rest": (
            "the home side has the better rest and recovery setup",
            "the away side has the better rest and recovery setup",
        ),
        "travel": (
            "travel demands are lighter for the home side",
            "travel demands are lighter for the away side",
        ),
        "venue": (
            "home-field advantage is working for the host team",
            "neutral-site conditions would remove this edge",
        ),
        "weather": (
            "the expected weather favors the home team's balance",
            "the expected weather favors the away team's balance",
        ),
        "playoff_urgency": (
            "the home side has the stronger late-season urgency signal",
            "the away side has the stronger late-season urgency signal",
        ),
    }

    factors: list[FactorImpact] = []
    for category, delta in factor_deltas.items():
        if abs(delta) < 0.05:
            continue

        team = home.name if delta > 0 else away.name
        winning_explanation = explanations[category][0 if delta > 0 else 1]
        factors.append(
            FactorImpact(
                team=team,
                category=category,
                score_delta=round(abs(delta), 2),
                explanation=winning_explanation,
            )
        )

    if divisional_game:
        factors.append(
            FactorImpact(
                team="matchup",
                category="divisional_familiarity",
                score_delta=0.08,
                explanation=(
                    "divisional opponents usually compress outcomes and "
                    "lower certainty"
                ),
            )
        )

    return sorted(factors, key=lambda factor: factor.score_delta, reverse=True)


def _build_summary(
    predicted_winner: str,
    factors: list[FactorImpact],
    divisional_game: bool,
) -> str:
    top_factors = [
        factor.explanation for factor in factors if factor.team != "matchup"
    ][:3]
    if top_factors:
        summary = (
            f"{predicted_winner} gets the edge because " + ", ".join(top_factors) + "."
        )
    else:
        summary = (
            f"{predicted_winner} has the slimmest edge in an otherwise " "even matchup."
        )
    if divisional_game:
        summary += " Divisional familiarity trims the confidence a bit."
    return summary
