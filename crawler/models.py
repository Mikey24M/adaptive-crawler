"""Shared starter models for crawling workflows."""

from dataclasses import dataclass


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
