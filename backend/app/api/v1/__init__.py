from fastapi import APIRouter

from app.api.v1 import backtests, datasets, health

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(datasets.router)
router.include_router(backtests.router)
