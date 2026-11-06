"""Settings endpoints."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import settings_service

router = APIRouter(prefix="/settings", tags=["settings"])


class SettingsUpdate(BaseModel):
    updates: dict[str, str]


@router.get("/")
async def get_settings(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    return await settings_service.get_all(db)


@router.put("/")
async def update_settings(
    payload: SettingsUpdate, db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    return await settings_service.set_many(db, payload.updates)
