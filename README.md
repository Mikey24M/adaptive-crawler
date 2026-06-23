# Adaptive Crawler

Adaptive Crawler is the starter foundation for an adaptive, distributed web crawling
platform. The repository is intentionally minimal today, but it is structured to
grow into a production-grade system with:

- HTTP-first crawling via `httpx`
- Browser-rendering fallback via Playwright
- URL normalization and deduplication
- `robots.txt` compliance
- Crawl depth and page limits
- Structured metadata extraction
- Distributed queues backed by Redis
- PostgreSQL persistence
- FastAPI control APIs
- Docker and Kubernetes deployment targets
- Prometheus and Grafana monitoring

## Repository Layout

```text
adaptive-crawler/
├── crawler/
│   ├── __init__.py
│   ├── config.py
│   ├── fetcher.py
│   ├── main.py
│   ├── models.py
│   ├── parser.py
│   └── urls.py
├── docs/
│   └── architecture.md
├── tests/
├── .env.example
├── pyproject.toml
└── requirements.txt
```

## System Architecture Overview

The current codebase establishes the foundation for four core layers:

1. **API and orchestration** via FastAPI.
2. **Crawler runtime** for fetch, parse, and URL policy decisions.
3. **Configuration** through environment-driven settings.
4. **Future distributed services** for queueing, storage, rendering, and monitoring.

See `/home/runner/work/adaptive-crawler/adaptive-crawler/docs/architecture.md` for the
full architecture and future Kubernetes deployment plan.

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

4. Start the API:

   ```bash
   uvicorn crawler.main:app --reload
   ```

5. Run quality checks:

   ```bash
   ruff check .
   black --check .
   pytest
   ```

## Development Roadmap

- **Phase 1:** foundation, configuration, and local developer tooling
- **Phase 2:** HTTP crawling, parsing, and crawl frontier management
- **Phase 3:** robots, deduplication, and crawl policy enforcement
- **Phase 4:** Redis queues, PostgreSQL storage, and worker coordination
- **Phase 5:** Playwright rendering fallback and richer extraction
- **Phase 6:** Docker, Kubernetes, and observability

## Current Status

This repository intentionally includes only starter implementations and TODO-ready
extension points. The current modules are safe to build on, but they do not yet
represent a full distributed crawler.
