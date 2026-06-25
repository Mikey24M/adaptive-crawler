"""HTTP-first page fetching utilities."""

import httpx

from crawler.config import Settings
from crawler.models import FetchResult


async def fetch_url(url: str, settings: Settings) -> FetchResult:
    """Fetch a page over HTTP.
    MVP version:
    - follows redirects
    - returns status codes, final url, content type, and text content
    - handles network errors

    Future TODO:
    - add retry backoff
    - robot aware scheduling
    - playwright fallbacks for javascript 
    """

    timeout = httpx.Timeout(settings.request_timeout)
    headers = {
        "User-Agent": settings.user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            headers=headers,
            timeout=timeout,
        ) as client:
            response = await client.get(url)

        content_type = response.headers.get("content-type", "")

        if not (
            "text/html" in content_type
            or "application/xhtml+xml" in content_type
        ):
            return FetchResult(
                url=url,
                final_url=str(response.url),
                status_code=response.status_code,
                content_type=content_type,
                content=None,
                error=f"Unsupported content type: {content_type}",
        )

        return FetchResult(
            url=url,
            final_url=str(response.url),
            status_code=response.status_code,
            content_type=content_type,
            content=response.text,
            error=None,
        )

    except httpx.TimeoutException as exc:
        return FetchResult(
            url=url,
            final_url=url,
            status_code=None,
            content_type=None,
            content=None,
            error=f"Timeout: {exc}",
        )

    except httpx.HTTPError as exc:
        return FetchResult(
            url=url,
            final_url=url,
            status_code=None,
            content_type=None,
            content=None,
            error=str(exc),
        )
