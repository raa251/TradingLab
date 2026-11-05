# TradingLab

A cross-platform (Windows & macOS) manual backtesting application for historical financial market data.

## Overview

TradingLab lets traders replay historical candlestick data, draw trade setups, execute manual trades, and analyze the results with comprehensive statistics. The UI is inspired by TradingView, but focused exclusively on manual backtesting workflows.

## Architecture

```
tradinglab/
├── frontend/          # React + TypeScript + Vite
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── store/
│       └── lib/
├── backend/           # Python + FastAPI
│   ├── app/
│   │   ├── api/       # REST endpoints
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── services/  # Business logic
│   │   ├── importer/  # Data import pipeline
│   │   └── backtest/  # Backtest engine
│   ├── migrations/    # Alembic DB migrations
│   └── tests/
├── data/              # Local data directory (gitignored)
│   ├── db/            # SQLite database
│   └── market_data/   # Parquet files for OHLCV / tick data
└── docs/              # Additional documentation
```

## Technology Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend | React 18 + TypeScript + Vite | Fast HMR, type safety, ecosystem |
| Charts | Lightweight Charts (TradingView) | Performance, candlestick support |
| State | Zustand | Lightweight, easy async |
| Styling | Tailwind CSS + shadcn/ui | Rapid UI, dark mode built-in |
| Backend | Python 3.11 + FastAPI | Async, Pydantic validation, pandas |
| Database | SQLite + SQLAlchemy + Alembic | Zero-setup, file-based, migrations |
| Market data | Apache Parquet (via PyArrow) | Columnar, compressed, fast queries |
| Packaging | Tauri (Phase 10) | Rust shell, small bundle, cross-platform |

## Quick Start (Development)

### Prerequisites
- Node.js 20+
- Python 3.11+
- uv (Python package manager)

### Backend
```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The app opens at http://localhost:5173 and talks to the backend at http://localhost:8000.

## Data Storage

- **SQLite** (`data/db/tradinglab.db`): Metadata, backtests, trades, drawings, settings
- **Parquet** (`data/market_data/`): OHLCV and tick data, partitioned by symbol/date

The data directory is configurable via `TRADINGLAB_DATA_DIR` environment variable and defaults to `~/.tradinglab/data`.

## Development Phases

| Phase | Description | Status |
|---|---|---|
| 0 | Analysis & Planning | ✅ Done |
| 1 | Project foundation | 🔄 In Progress |
| 2 | Local persistence | ⏳ Pending |
| 3 | Data import | ⏳ Pending |
| 4 | Chart interface | ⏳ Pending |
| 5 | Drawing tools | ⏳ Pending |
| 6 | Manual backtest | ⏳ Pending |
| 7 | Tick data | ⏳ Pending |
| 8 | Statistics | ⏳ Pending |
| 9 | Backtest management | ⏳ Pending |
| 10 | Desktop packages | ⏳ Pending |
| 11 | Stabilization | ⏳ Pending |

## License

Private – all rights reserved.
