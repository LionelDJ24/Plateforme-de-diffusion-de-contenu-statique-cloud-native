import pytest

from app import create_app


class FakeStorage:
    def __init__(self, data):
        self.data = data

    def read_text(self, container: str, blob_name: str) -> str:
        return self.data.get((container, blob_name), '{"items": []}')

    def exists(self, container: str, blob_name: str) -> bool:
        return (container, blob_name) in self.data


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("BLOB_CONTAINER", "content")
    monkeypatch.setenv("BLOB_EVENTS", "events.json")
    monkeypatch.setenv("BLOB_NEWS", "news.yaml")
    monkeypatch.setenv("BLOB_FAQ", "faq.json")
    monkeypatch.setenv("CACHE_TTL_SECONDS", "60")
    monkeypatch.setenv("READY_CHECK_MODE", "basic")

    data = {
        ("content", "events.json"): '{"items":[{"title":"Demo","date":"2026-02-16"}]}',
        ("content", "news.yaml"): "items:\n  - title: News1\n    date: 2026-02-16\n",
        ("content", "faq.json"): '{"items":[{"q":"Q1","a":"A1"}]}',
    }

    app = create_app(storage_client=FakeStorage(data))
    app.config.update(TESTING=True)

    with app.test_client() as client:
        yield client
