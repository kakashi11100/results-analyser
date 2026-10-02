"""Refresh rotation, reuse detection, and type confusion."""

from __future__ import annotations

from tests.conftest import auth_header


def _login(client, username="admin", password="supersecret"):
    r = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": password},
    )
    assert r.status_code == 200, r.text
    return r.json()


def test_refresh_rotates_tokens(client, admin_user):
    first = _login(client)
    r = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": first["refresh_token"]},
    )
    assert r.status_code == 200, r.text
    second = r.json()
    assert second["access_token"]
    assert second["refresh_token"]
    assert second["refresh_token"] != first["refresh_token"]

    # New access token works.
    r = client.get("/api/v1/auth/me", headers=auth_header(second["access_token"]))
    assert r.status_code == 200


def test_reusing_old_refresh_revokes_whole_family(client, admin_user):
    first = _login(client)
    rotated = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": first["refresh_token"]},
    ).json()

    # Reuse the first token → 401 and family revoked.
    r = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": first["refresh_token"]},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "UNAUTHORIZED"

    # The rotated token must now also be dead.
    r = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": rotated["refresh_token"]},
    )
    assert r.status_code == 401


def test_access_token_rejected_as_refresh(client, admin_user, admin_token):
    r = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": admin_token},
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "UNAUTHORIZED"


def test_logout_revokes_refresh_token(client, admin_user):
    first = _login(client)
    r = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": first["refresh_token"]},
    )
    assert r.status_code == 204

    r = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": first["refresh_token"]},
    )
    assert r.status_code == 401


def test_logout_unknown_token_still_204(client):
    r = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": "not-a-real-token"},
    )
    assert r.status_code == 204