def test_bad_request_returns_standard_envelope(client):
    resp = client.post("/api/v1/auth/users", json={"username": "x"})
    assert resp.status_code == 422
    body = resp.json()
    assert "error" in body
    err = body["error"]
    assert err["code"] == "validation_failed"
    assert isinstance(err["message"], str)
    assert isinstance(err["details"], list)
    assert isinstance(err["request_id"], str)
    assert resp.headers["X-Request-ID"] == err["request_id"]
