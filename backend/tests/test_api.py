def _assert_items(resp):
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, dict)
    assert "items" in data
    assert isinstance(data["items"], list)


def test_events(client):
    resp = client.get("/api/events")
    _assert_items(resp)


def test_news(client):
    resp = client.get("/api/news")
    _assert_items(resp)


def test_faq(client):
    resp = client.get("/api/faq")
    _assert_items(resp)
