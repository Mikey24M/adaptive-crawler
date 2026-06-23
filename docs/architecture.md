# Architecture Overview

## Goals

Adaptive Crawler is being shaped as a horizontally scalable platform for crawling
public websites from seed URLs, extracting structured metadata, and managing work
across distributed workers.

## Current Foundation

The current starter implementation provides:

- a centralized settings model in `crawler.config`
- a minimal FastAPI application in `crawler.main`
- a small HTTP-first fetcher in `crawler.fetcher`
- structured metadata parsing in `crawler.parser`
- URL normalization helpers in `crawler.urls`
- basic data models in `crawler.models`

## Target System Design

```text
             +------------------+
             |   FastAPI API    |
             | crawl requests   |
             | health/status    |
             +---------+--------+
                       |
                       v
             +------------------+
             | Crawl Orchestrator|
             | limits/policies   |
             +---------+--------+
                       |
          +------------+-------------+
          |                          |
          v                          v
+-------------------+      +--------------------+
| Redis Crawl Queue |      | PostgreSQL Storage |
| pending / retries |      | pages / metadata   |
+---------+---------+      +----------+---------+
          |                           |
          v                           |
 +-------------------+                |
 | Distributed Worker|----------------+
 | fetch / parse     |
 | normalize / dedup |
 +---------+---------+
           |
           v
 +-------------------+
 | Playwright Fallback|
 | JS rendering path  |
 +-------------------+
```

## Component Responsibilities

### API Layer

- Accept crawl requests from operators or upstream systems.
- Expose health and readiness endpoints.
- Surface crawl status and metrics in future iterations.

### Orchestration Layer

- Apply crawl depth, page, and domain policies.
- Respect `robots.txt`.
- Coordinate retries and backoff.
- Route HTTP-first requests to browser rendering only when needed.

### Worker Layer

- Fetch pages with `httpx`.
- Parse structured metadata.
- Normalize and deduplicate URLs.
- Emit new crawl candidates back to the queue.

### Data Layer

- Redis for distributed queueing and worker coordination.
- PostgreSQL for crawl results, metadata, and crawl state snapshots.

### Observability Layer

- Prometheus metrics for queue depth, latency, and success rates.
- Grafana dashboards for cluster visibility.

## Local Development Flow

For now, the local development loop is intentionally small:

1. configure environment values with `.env`
2. run the FastAPI service locally
3. iterate on fetching/parsing utilities
4. validate with Ruff, Black, and Pytest

## Future Kubernetes Architecture

The expected Kubernetes deployment shape is:

- **API Deployment** for FastAPI ingress-facing services
- **Worker Deployment** for scalable crawl workers
- **Redis StatefulSet or managed Redis** for crawl frontier storage
- **PostgreSQL StatefulSet or managed PostgreSQL** for durable metadata storage
- **ConfigMaps and Secrets** for crawler settings
- **HorizontalPodAutoscaler** for worker pools based on queue depth and CPU
- **Prometheus + Grafana** stack for monitoring

## Roadmap

1. implement crawl frontier logic
2. add robots parsing and policy enforcement
3. connect Redis and PostgreSQL adapters
4. add Playwright fallback workflow
5. introduce Docker images and Compose-based local services
6. add Kubernetes manifests or Helm charts
