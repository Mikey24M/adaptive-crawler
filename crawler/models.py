"""Shared starter models for crawling workflows."""

from dataclasses import dataclass, field


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

    headings: list[str] = field(default_factory=list)
    internal_links: list[str] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
