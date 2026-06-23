"""HTTP-first page fetching utilities."""

import httpx

from crawler.config import Settings
from crawler.models import FetchResult


async def fetch_url(url: str, settings: Settings) -> FetchResult:
    """Fetch a page over HTTP.

    TODO: add retry backoff, robots-aware scheduling, and Playwright fallback for
    JavaScript-heavy pages that cannot be handled through the HTTP path alone.
    """

    timeout = httpx.Timeout(settings.request_timeout)
    headers = {"User-Agent": "adaptive-crawler/0.1"}

    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            headers=headers,
            timeout=timeout,
        ) as client:
            response = await client.get(url)
    except httpx.HTTPError as exc:
        return FetchResult(
            url=url,
            final_url=url,
            status_code=None,
            content_type=None,
            content=None,
            error=str(exc),
        )

    return FetchResult(
        url=url,
        final_url=str(response.url),
        status_code=response.status_code,
        content_type=response.headers.get("content-type"),
        content=response.text,
    )
