"""Settings API tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_settings_returns_defaults(client: AsyncClient):
    resp = await client.get("/api/v1/settings/")
    assert resp.status_code == 200
    data = resp.json()
    assert "theme" in data
    assert data["theme"] == "dark"
    assert "default_risk_pct" in data


@pytest.mark.asyncio
async def test_update_setting(client: AsyncClient):
    resp = await client.put(
        "/api/v1/settings/",
        json={"updates": {"theme": "light", "replay_speed": "2.0"}},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["theme"] == "light"
    assert data["replay_speed"] == "2.0"


@pytest.mark.asyncio
async def test_updated_setting_persists(client: AsyncClient):
    await client.put("/api/v1/settings/", json={"updates": {"theme": "custom"}})
    resp = await client.get("/api/v1/settings/")
    assert resp.json()["theme"] == "custom"
