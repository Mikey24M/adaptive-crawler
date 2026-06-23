"""URL normalization and policy helpers."""

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def normalize_url(url: str) -> str:
    """Normalize absolute URLs for deduplication."""

    parts = urlsplit(url.strip())
    if not parts.scheme or not parts.netloc:
        msg = f"Expected an absolute URL, got: {url!r}"
        raise ValueError(msg)

    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    if scheme == "http" and netloc.endswith(":80"):
        netloc = netloc[:-3]
    if scheme == "https" and netloc.endswith(":443"):
        netloc = netloc[:-4]

    path = parts.path or "/"
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))

    return urlunsplit((scheme, netloc, path, query, ""))


def is_same_domain(candidate_url: str, seed_url: str) -> bool:
    """Return whether two URLs share the same hostname."""

    return urlsplit(candidate_url).hostname == urlsplit(seed_url).hostname
