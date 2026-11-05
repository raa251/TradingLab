# TradingLab – Technical Plan & Architecture Decisions

## 1. Architecture Decisions

### 1.1 Frontend: React + TypeScript + Vite
- **Chosen**: React 18, TypeScript 5, Vite 5
- **Charts**: TradingView Lightweight Charts v4 – best-in-class performance for financial charts, free, MIT-licensed
- **State**: Zustand – minimal boilerplate, async-friendly, devtools support
- **Styling**: Tailwind CSS + shadcn/ui components – dark mode first, accessible
- **Alternative considered**: Electron + React (rejected: larger bundle, no Rust safety)

### 1.2 Backend: Python + FastAPI
- **Chosen**: Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic, PyArrow, pandas
- **Package manager**: uv (fast, lockfile-based)
- **Alternative considered**: Node.js backend (rejected: pandas/numpy ecosystem advantage for data processing)

### 1.3 Database: SQLite + Parquet
- **SQLite**: All metadata, configs, backtests, trades, drawings – single file, zero ops
- **Parquet**: OHLCV and tick market data, partitioned by `symbol/YYYY/MM/` – efficient columnar reads
- **Separation**: Market data files are referenced by path in SQLite, never stored as BLOBs
- **Migration**: Alembic manages schema versions

### 1.4 Desktop Packaging: Tauri (Phase 10)
- **Plan**: Tauri 2.0 wraps the React frontend; Python backend starts as a sidecar process
- **Alternative**: Electron (rejected: 100MB+ overhead vs Tauri ~5MB)
- **Risk**: Python sidecar bundling is complex – deferred to Phase 10

### 1.5 Local-only operation
- Backend binds to `127.0.0.1:8000` only (no `0.0.0.0`)
- No telemetry, no cloud dependencies
- Data directory: `~/.tradinglab/data` (configurable via env var)

---

## 2. Data Model

### 2.1 Core entities (SQLite)

#### `datasets`
Tracks imported market data series.
```
id              UUID PK
name            TEXT NOT NULL
symbol          TEXT NOT NULL
timeframe       TEXT              -- e.g. "M1", "H1", "D1", "TICK"
source          TEXT              -- e.g. "MetaTrader", "manual"
data_format     TEXT NOT NULL     -- "OHLCV" | "TICK"
start_time      DATETIME NOT NULL (UTC)
end_time        DATETIME NOT NULL (UTC)
row_count       INTEGER
file_path       TEXT NOT NULL     -- relative path to Parquet file(s)
file_size_bytes INTEGER
timezone_orig   TEXT              -- original timezone of source data
import_status   TEXT NOT NULL     -- "importing" | "ready" | "error" | "partial"
created_at      DATETIME NOT NULL
updated_at      DATETIME NOT NULL
```

#### `import_jobs`
Tracks each import attempt for audit and recovery.
```
id              UUID PK
dataset_id      UUID FK → datasets
source_file     TEXT
rows_imported   INTEGER
rows_skipped    INTEGER
rows_error      INTEGER
status          TEXT    -- "running" | "done" | "failed" | "aborted"
error_log       TEXT
started_at      DATETIME
finished_at     DATETIME
engine_version  TEXT
```

#### `backtests`
One row per backtest run.
```
id              UUID PK
name            TEXT NOT NULL
description     TEXT
dataset_id      UUID FK → datasets (nullable – dataset may be deleted)
symbol          TEXT
timeframe       TEXT
start_time      DATETIME
end_time        DATETIME
replay_cursor   DATETIME          -- current replay position
status          TEXT    -- "new" | "running" | "paused" | "finished"
settings        JSON              -- risk %, commission, spread, slippage
stats_cache     JSON              -- cached computed stats
engine_version  TEXT
created_at      DATETIME
updated_at      DATETIME
```

#### `trades`
Executed trades within a backtest.
```
id              UUID PK
backtest_id     UUID FK → backtests
direction       TEXT    -- "LONG" | "SHORT"
entry_time      DATETIME
entry_price     REAL
sl_price        REAL
tp_price        REAL
close_time      DATETIME
close_price     REAL
close_reason    TEXT    -- "TP" | "SL" | "MANUAL"
size            REAL
commission      REAL
swap            REAL
pnl_points      REAL
pnl_money       REAL
pnl_r           REAL    -- R-multiple
max_adverse_exc REAL    -- MAE in points
max_fav_exc     REAL    -- MFE in points
tags            TEXT    -- JSON array of strings
notes           TEXT
created_at      DATETIME
```

#### `drawings`
Visual drawings on the chart (not trades).
```
id              UUID PK
backtest_id     UUID FK → backtests
type            TEXT    -- "RECT" | "LONG_POS" | "SHORT_POS" | "HLINE" | "TREND"
data            JSON    -- type-specific shape data
visible         BOOLEAN DEFAULT 1
created_at      DATETIME
updated_at      DATETIME
```

#### `settings`
Key/value store for application settings.
```
key             TEXT PK
value           TEXT
updated_at      DATETIME
```

### 2.2 Parquet file layout

```
data/market_data/
└── {dataset_id}/
    ├── _meta.json          -- symbol, timeframe, tz, row_count
    ├── ohlcv/
    │   └── YYYY-MM/
    │       └── data.parquet
    └── tick/
        └── YYYY-MM/
            └── data.parquet
```

OHLCV columns: `time (int64 UTC ns), open, high, low, close, volume, tick_volume`
Tick columns: `time (int64 UTC ns), bid, ask, last, volume`

---

## 3. API Endpoints (Phase 1 skeleton)

```
GET  /health
GET  /api/v1/datasets
POST /api/v1/datasets/import
GET  /api/v1/datasets/{id}
DELETE /api/v1/datasets/{id}
GET  /api/v1/datasets/{id}/ohlcv?from=&to=&limit=
GET  /api/v1/backtests
POST /api/v1/backtests
GET  /api/v1/backtests/{id}
PUT  /api/v1/backtests/{id}
DELETE /api/v1/backtests/{id}
GET  /api/v1/backtests/{id}/trades
POST /api/v1/backtests/{id}/trades
GET  /api/v1/backtests/{id}/drawings
POST /api/v1/backtests/{id}/drawings
GET  /api/v1/backtests/{id}/stats
GET  /api/v1/settings
PUT  /api/v1/settings
```

---

## 4. Technical Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Large Parquet files slow to query | Medium | Partition by month, use PyArrow predicates |
| SL+TP hit same candle ambiguity | High | Document rule: SL takes priority on OHLCV; tick data resolves if available |
| Tauri Python sidecar bundling | High | Defer to Phase 10; dev mode runs both separately |
| Cross-platform path handling | Medium | Use `pathlib.Path` everywhere, never hardcode separators |
| Browser memory with large datasets | Medium | Virtual windowing, never load full dataset into JS |
| Import of duplicate data | Medium | Hash-based dedup check before writing |

---

## 5. Acceptance Criteria – Phase 1

- [ ] `npm run dev` starts frontend at localhost:5173
- [ ] `uv run uvicorn ...` starts backend at localhost:8000
- [ ] `GET /health` returns 200
- [ ] SQLite DB created on first backend start
- [ ] Alembic migration applies cleanly
- [ ] Frontend renders main layout with navigation
- [ ] All lint checks pass (ESLint, Ruff, mypy)
- [ ] All tests pass (Vitest, pytest)
- [ ] Git commit on main branch, pushed to remote
