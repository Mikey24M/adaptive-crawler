"""Shared models for the NFL game predictor."""

from dataclasses import dataclass, field as dataclass_field
from enum import StrEnum

from pydantic import BaseModel, Field


@dataclass(slots=True)
class CrawlRequest:
    """Represents a single crawl candidate."""

    url: str
    depth: int = 0
    discovered_from: str | None = None


@dataclass(slots=True)
class FetchResult:
    """Represents the outcome of a fetch operation."""

    url: str
    final_url: str
    status_code: int | None
    content_type: str | None
    content: str | None
    error: str | None = None


@dataclass(slots=True)
class PageMetadata:
    """Structured page metadata extracted from a document."""

    url: str
    status_code: int | None
    title: str | None = None
    description: str | None = None
    canonical_url: str | None = None

    headings: list[str] = dataclass_field(default_factory=list)
    internal_links: list[str] = dataclass_field(default_factory=list)
    external_links: list[str] = dataclass_field(default_factory=list)
    images: list[str] = dataclass_field(default_factory=list)


class PlayerStatus(StrEnum):
    """Supported NFL player availability states."""

    ACTIVE = "active"
    QUESTIONABLE = "questionable"
    DOUBTFUL = "doubtful"
    OUT = "out"
    INJURED_RESERVE = "injured_reserve"


class WeatherOutlook(StrEnum):
    """Simplified game-day weather conditions."""

    INDOOR = "indoor"
    CLEAR = "clear"
    RAIN = "rain"
    SNOW = "snow"
    WIND = "wind"


class KeyPlayer(BaseModel):
    """A notable player expected to influence the matchup."""

    name: str
    position: str
    impact_rating: float = Field(ge=0, le=10)


class InjuryReport(BaseModel):
    """A player availability item that can lower a team's outlook."""

    player_name: str
    position: str
    status: PlayerStatus
    impact_rating: float = Field(ge=0, le=10)


class TeamProfile(BaseModel):
    """Predictor inputs for one NFL team."""

    name: str
    overall_rating: float = Field(ge=0, le=100)
    offense_rating: float = Field(ge=0, le=100)
    defense_rating: float = Field(ge=0, le=100)
    quarterback_rating: float = Field(ge=0, le=100)
    recent_form: float = Field(default=0, ge=-10, le=10)
    rest_days: int = Field(default=7, ge=0, le=21)
    travel_miles: int = Field(default=0, ge=0, le=5000)
    key_players: list[KeyPlayer] = Field(default_factory=list)
    injuries: list[InjuryReport] = Field(default_factory=list)


class GameContext(BaseModel):
    """Game-level conditions that shape a prediction."""

    week: int = Field(ge=1, le=23)
    divisional_game: bool = False
    neutral_site: bool = False
    weather: WeatherOutlook = WeatherOutlook.CLEAR
    playoff_urgency_home: float = Field(default=0, ge=0, le=5)
    playoff_urgency_away: float = Field(default=0, ge=0, le=5)


class GamePredictionRequest(BaseModel):
    """Top-level prediction request."""

    home_team: TeamProfile
    away_team: TeamProfile
    context: GameContext


class FactorImpact(BaseModel):
    """One factor that meaningfully shifted the game outlook."""

    team: str
    category: str
    score_delta: float
    explanation: str


class GamePredictionResponse(BaseModel):
    """Prediction output returned by the API."""

    predicted_winner: str
    home_win_probability: float = Field(ge=0, le=1)
    away_win_probability: float = Field(ge=0, le=1)
    projected_margin: float
    confidence_tier: str
    factors: list[FactorImpact]
    summary: str
