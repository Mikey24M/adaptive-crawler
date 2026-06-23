import pytest

from crawler.urls import is_same_domain, normalize_url


def test_normalize_url_removes_fragments_and_default_ports() -> None:
    normalized = normalize_url("HTTPS://Example.com:443/path?b=2&a=1#section")

    assert normalized == "https://example.com/path?a=1&b=2"


def test_normalize_url_requires_absolute_urls() -> None:
    with pytest.raises(ValueError):
        normalize_url("/relative/path")


def test_is_same_domain_checks_hostnames() -> None:
    assert is_same_domain("https://example.com/about", "https://example.com")
    assert not is_same_domain("https://blog.example.com", "https://example.com")
