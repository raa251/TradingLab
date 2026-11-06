"""Dataset ORM model – tracks imported market data series."""
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    symbol: Mapped[str] = mapped_column(String(50), nullable=False)
    timeframe: Mapped[str | None] = mapped_column(String(20))  # M1, H1, D1, TICK …
    source: Mapped[str | None] = mapped_column(String(100))    # MetaTrader, manual …
    data_format: Mapped[str] = mapped_column(String(10), nullable=False)  # OHLCV | TICK
    start_time: Mapped[datetime | None] = mapped_column(DateTime)
    end_time: Mapped[datetime | None] = mapped_column(DateTime)
    row_count: Mapped[int | None] = mapped_column(Integer)
    file_path: Mapped[str | None] = mapped_column(Text)        # relative to market_data_dir
    file_size_bytes: Mapped[int | None] = mapped_column(Integer)
    timezone_orig: Mapped[str | None] = mapped_column(String(50))
    import_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="importing"
    )  # importing | ready | error | partial
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
