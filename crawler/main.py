"""FastAPI entrypoint for the crawler foundation."""

from fastapi import FastAPI

from crawler.config import get_settings


def create_app() -> FastAPI:
    """Create the FastAPI application."""

    settings = get_settings()
    app = FastAPI(
        title="Adaptive Crawler",
        version="0.1.0",
        description="Starter control plane for an adaptive distributed crawler.",
    )

    @app.get("/")
    def root() -> dict[str, object]:
        return {
            "service": "adaptive-crawler",
            "status": "ready",
            "limits": {
                "max_pages": settings.max_pages,
                "max_depth": settings.max_depth,
            },
            "features": {
                "http_fetching": True,
                "browser_fallback": "planned",
                "distributed_queue": "planned",
            },
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
