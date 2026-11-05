"""Backtest endpoints – skeleton for Phase 1."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.backtest import Backtest

router = APIRouter(prefix="/backtests", tags=["backtests"])


class BacktestCreate(BaseModel):
    name: str
    description: str | None = None
    dataset_id: str | None = None
    symbol: str | None = None
    timeframe: str | None = None


@router.get("/")
async def list_backtests(db: AsyncSession = Depends(get_db)) -> list[dict]:
    result = await db.execute(select(Backtest).order_by(Backtest.updated_at.desc()))
    backtests = result.scalars().all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "symbol": b.symbol,
            "timeframe": b.timeframe,
            "status": b.status,
            "created_at": b.created_at,
            "updated_at": b.updated_at,
        }
        for b in backtests
    ]


@router.post("/", status_code=201)
async def create_backtest(payload: BacktestCreate, db: AsyncSession = Depends(get_db)) -> dict:
    bt = Backtest(
        name=payload.name,
        description=payload.description,
        dataset_id=payload.dataset_id,
        symbol=payload.symbol,
        timeframe=payload.timeframe,
    )
    db.add(bt)
    await db.commit()
    await db.refresh(bt)
    return {"id": bt.id, "name": bt.name, "status": bt.status}


@router.get("/{backtest_id}")
async def get_backtest(backtest_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Backtest).where(Backtest.id == backtest_id))
    bt = result.scalar_one_or_none()
    if bt is None:
        raise HTTPException(status_code=404, detail="Backtest not found")
    return {
        "id": bt.id,
        "name": bt.name,
        "description": bt.description,
        "dataset_id": bt.dataset_id,
        "symbol": bt.symbol,
        "timeframe": bt.timeframe,
        "status": bt.status,
        "replay_cursor": bt.replay_cursor,
        "created_at": bt.created_at,
        "updated_at": bt.updated_at,
    }
