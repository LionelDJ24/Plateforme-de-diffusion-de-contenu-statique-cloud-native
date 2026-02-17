def test_healthz(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, dict)
    assert data.get("status") == "ok"
    assert "ts" in data


def test_readyz(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, dict)
    assert data.get("status") == "ready"
