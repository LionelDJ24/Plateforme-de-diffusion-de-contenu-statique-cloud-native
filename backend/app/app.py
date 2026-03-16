from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Optional

from flask import Flask, jsonify, render_template

from .cache import TTLCache
from .storage import AzureBlobStorage, StorageClient, load_parsers

DEFAULT_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))


@dataclass(frozen=True)
class AppConfig:
    container_name: str
    events_blob: str
    news_blob: str
    faq_blob: str
    ready_check_mode: str


def _load_config() -> AppConfig:
    return AppConfig(
        container_name=os.getenv("BLOB_CONTAINER", "content"),
        events_blob=os.getenv("BLOB_EVENTS", "events.json"),
        news_blob=os.getenv("BLOB_NEWS", "news.yaml"),
        faq_blob=os.getenv("BLOB_FAQ", "faq.json"),
        ready_check_mode=os.getenv("READY_CHECK_MODE", "basic"),
    )


def create_app(storage_client: Optional[StorageClient] = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    cfg = _load_config()
    cache = TTLCache(default_ttl_seconds=DEFAULT_TTL_SECONDS)
    parsers = load_parsers()

    if storage_client is None:
        storage_client = AzureBlobStorage.from_env()

    def fetch_items(blob_name: str) -> list[dict[str, Any]]:
        cache_key = f"blob:{cfg.container_name}:{blob_name}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            raw = storage_client.read_text(cfg.container_name, blob_name)
            parsed = parsers.parse(blob_name, raw)

            if isinstance(parsed, list):
                items = parsed
            elif isinstance(parsed, dict):
                items = parsed.get("items", [])
                if not isinstance(items, list):
                    items = [items]
            else:
                items = []

            cache.set(cache_key, items)
            return items

        except Exception:
            return []

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            events=fetch_items(cfg.events_blob),
            news=fetch_items(cfg.news_blob),
            faq=fetch_items(cfg.faq_blob),
            ttl=DEFAULT_TTL_SECONDS,
        )

    @app.get("/api/events")
    def api_events():
        return jsonify({"items": fetch_items(cfg.events_blob)})

    @app.get("/api/news")
    def api_news():
        return jsonify({"items": fetch_items(cfg.news_blob)})

    @app.get("/api/faq")
    def api_faq():
        return jsonify({"items": fetch_items(cfg.faq_blob)})

    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok", "ts": int(time.time())}), 200

    @app.get("/readyz")
    def readyz():
        if cfg.ready_check_mode == "storage":
            try:
                storage_client.exists(cfg.container_name, cfg.events_blob)
            except Exception:
                return jsonify({"status": "not_ready"}), 503

        return jsonify({"status": "ready"}), 200

    return app
