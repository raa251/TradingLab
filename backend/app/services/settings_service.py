"""Application settings service – persists key/value pairs in SQLite."""
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.backtest import AppSetting

# Default settings applied on first start
DEFAULTS: dict[str, str] = {
    "theme": "dark",
    "default_risk_pct": "1.0",
    "default_commission": "0.0",
    "default_spread_points": "0.0",
    "default_slippage_points": "0.0",
    "replay_speed": "1.0",
    "data_dir": "",  # empty = use config default (~/.tradinglab/data)
}


async def get_all(db: AsyncSession) -> dict[str, str]:
    result = await db.execute(select(AppSetting))
    rows = result.scalars().all()
    merged = dict(DEFAULTS)
    for row in rows:
        if row.value is not None:
            merged[row.key] = row.value
    return merged


async def get(db: AsyncSession, key: str) -> str | None:
    result = await db.execute(select(AppSetting).where(AppSetting.key == key))
    row = result.scalar_one_or_none()
    if row is None:
        return DEFAULTS.get(key)
    return row.value


async def set_many(db: AsyncSession, updates: dict[str, str]) -> dict[str, str]:
    for key, value in updates.items():
        result = await db.execute(select(AppSetting).where(AppSetting.key == key))
        row = result.scalar_one_or_none()
        if row is None:
            db.add(AppSetting(key=key, value=value, updated_at=datetime.now(UTC)))
        else:
            row.value = value
            row.updated_at = datetime.now(UTC)
    await db.commit()
    return await get_all(db)


async def ensure_defaults(db: AsyncSession) -> None:
    """Write missing default keys on first startup."""
    existing = await get_all(db)
    missing = {k: v for k, v in DEFAULTS.items() if k not in existing or existing[k] == v}
    if missing:
        # Only insert truly missing rows (not already in DB)
        result = await db.execute(select(AppSetting.key))
        db_keys = set(result.scalars().all())
        to_insert = {k: v for k, v in DEFAULTS.items() if k not in db_keys}
        for key, value in to_insert.items():
            db.add(AppSetting(key=key, value=value))
        if to_insert:
            await db.commit()
