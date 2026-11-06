"""Backtest CRUD API tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_backtests_empty(client: AsyncClient):
    resp = await client.get("/api/v1/backtests/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_create_backtest(client: AsyncClient):
    resp = await client.post(
        "/api/v1/backtests/",
        json={"name": "Test BT 1", "description": "My first backtest", "symbol": "EURUSD"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Test BT 1"
    assert "id" in data
    assert data["status"] == "new"


@pytest.mark.asyncio
async def test_get_backtest(client: AsyncClient):
    create_resp = await client.post("/api/v1/backtests/", json={"name": "BT Get Test"})
    bt_id = create_resp.json()["id"]

    resp = await client.get(f"/api/v1/backtests/{bt_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == bt_id
    assert resp.json()["name"] == "BT Get Test"


@pytest.mark.asyncio
async def test_get_backtest_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/backtests/nonexistent-id")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_list_backtests_after_create(client: AsyncClient):
    await client.post("/api/v1/backtests/", json={"name": "BT A"})
    await client.post("/api/v1/backtests/", json={"name": "BT B"})
    resp = await client.get("/api/v1/backtests/")
    assert len(resp.json()) == 2
