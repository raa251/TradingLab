"""Dataset endpoints – skeleton for Phase 1."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.dataset import Dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("/")
async def list_datasets(db: AsyncSession = Depends(get_db)) -> list[dict]:
    result = await db.execute(select(Dataset).order_by(Dataset.created_at.desc()))
    datasets = result.scalars().all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "symbol": d.symbol,
            "timeframe": d.timeframe,
            "data_format": d.data_format,
            "import_status": d.import_status,
            "row_count": d.row_count,
            "start_time": d.start_time,
            "end_time": d.end_time,
            "file_size_bytes": d.file_size_bytes,
            "created_at": d.created_at,
        }
        for d in datasets
    ]
