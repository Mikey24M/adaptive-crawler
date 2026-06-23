"""Minimal structured metadata extraction."""

from html.parser import HTMLParser

from crawler.models import FetchResult, PageMetadata


class MetadataHTMLParser(HTMLParser):
    """Extract starter metadata from HTML documents."""

    def __init__(self) -> None:
        super().__init__()
        self.title: str | None = None
        self.description: str | None = None
        self.canonical_url: str | None = None
        self._inside_title = False
        self._title_chunks: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attr_map = {key.lower(): value for key, value in attrs}

        if tag.lower() == "title":
            self._inside_title = True
        elif (
            tag.lower() == "meta" and attr_map.get("name", "").lower() == "description"
        ):
            self.description = attr_map.get("content")
        elif tag.lower() == "link" and attr_map.get("rel", "").lower() == "canonical":
            self.canonical_url = attr_map.get("href")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._inside_title = False
            title = "".join(self._title_chunks).strip()
            self.title = title or None

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self._title_chunks.append(data)


def extract_page_metadata(fetch_result: FetchResult) -> PageMetadata:
    """Extract starter metadata fields from a fetch result."""

    parser = MetadataHTMLParser()
    if fetch_result.content:
        parser.feed(fetch_result.content)

    return PageMetadata(
        url=fetch_result.final_url,
        status_code=fetch_result.status_code,
        title=parser.title,
        description=parser.description,
        canonical_url=parser.canonical_url,
    )
