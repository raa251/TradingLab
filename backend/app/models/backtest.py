"""Backtest, Trade, Drawing ORM models."""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Backtest(Base):
    __tablename__ = "backtests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    dataset_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("datasets.id", ondelete="SET NULL")
    )
    symbol: Mapped[str | None] = mapped_column(String(50))
    timeframe: Mapped[str | None] = mapped_column(String(20))
    start_time: Mapped[datetime | None] = mapped_column(DateTime)
    end_time: Mapped[datetime | None] = mapped_column(DateTime)
    replay_cursor: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="new")
    # JSON: { commission_per_lot, spread_points, slippage_points, risk_per_trade_pct }
    settings_json: Mapped[str | None] = mapped_column(Text)
    stats_cache_json: Mapped[str | None] = mapped_column(Text)
    engine_version: Mapped[str | None] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    trades: Mapped[list["Trade"]] = relationship(
        "Trade", back_populates="backtest", cascade="all, delete-orphan"
    )
    drawings: Mapped[list["Drawing"]] = relationship(
        "Drawing", back_populates="backtest", cascade="all, delete-orphan"
    )


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    backtest_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("backtests.id", ondelete="CASCADE"), nullable=False
    )
    direction: Mapped[str] = mapped_column(String(5), nullable=False)   # LONG | SHORT
    entry_time: Mapped[datetime | None] = mapped_column(DateTime)
    entry_price: Mapped[float | None] = mapped_column(Float)
    sl_price: Mapped[float | None] = mapped_column(Float)
    tp_price: Mapped[float | None] = mapped_column(Float)
    close_time: Mapped[datetime | None] = mapped_column(DateTime)
    close_price: Mapped[float | None] = mapped_column(Float)
    close_reason: Mapped[str | None] = mapped_column(String(10))        # TP | SL | MANUAL
    size: Mapped[float | None] = mapped_column(Float)
    commission: Mapped[float] = mapped_column(Float, default=0.0)
    swap: Mapped[float] = mapped_column(Float, default=0.0)
    pnl_points: Mapped[float | None] = mapped_column(Float)
    pnl_money: Mapped[float | None] = mapped_column(Float)
    pnl_r: Mapped[float | None] = mapped_column(Float)
    max_adverse_exc: Mapped[float | None] = mapped_column(Float)
    max_fav_exc: Mapped[float | None] = mapped_column(Float)
    tags_json: Mapped[str | None] = mapped_column(Text)                 # JSON array
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    backtest: Mapped["Backtest"] = relationship("Backtest", back_populates="trades")


class Drawing(Base):
    __tablename__ = "drawings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    backtest_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("backtests.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # RECT | LONG_POS | SHORT_POS
    data_json: Mapped[str | None] = mapped_column(Text)                 # shape-specific JSON
    visible: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    backtest: Mapped["Backtest"] = relationship("Backtest", back_populates="drawings")


class AppSetting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
