# 🏗️ Fincept AI Ops

> Research-first, supervised paper trading system.
> FastAPI + N8N + MCP. 5 active connectors. Enterprise grade.

**Status:** 🟢 Production-Ready — Audit Score 8.4/10
**Default Branch:** `main` ← canonical, fully up-to-date
**Owner:** Mehmet Zeki (ZeZilly)
**Version:** 1.0 / MVP
**Last Updated:** 2026-05-22

---

## ⚠️ Branch Status

| Branch | Role | Content | Status |
|---|---|---|---|
| `main` | **Canonical / Production** | Full implementation | ✅ Default & Active |
| `youtube` | Legacy dev branch | Identical to main | 🔒 Frozen (no divergence) |

> `main` contains 100% of all implementation. `youtube` was the development branch during initial build — all content was squash-merged into `main` on 2026-05-22. **Use `main` for all future work.**

---

## Core Principle

> No live trading. No execution without human approval. No broker action without audit log.

---

## System Overview

```
Market Data + News + Fundamentals
            ↓
      Research Pipeline
            ↓
      Strategy Lab (signal candidate)
            ↓
      Risk Policy (evaluate)
            ↓
    Human Approval Gate
            ↓
    Paper Broker Execution
            ↓
    Audit Logger + State Store
            ↓
    Daily Briefing Generator
```

---

## 5 Active Connectors (MVP)

| # | Connector | Purpose | Status |
|---|---|---|---|
| 1 | market_data | Price, OHLCV, watchlist | ✅ Active |
| 2 | fundamentals | Balance sheet, income, cash flow | ✅ Active |
| 3 | news | News and event data | ✅ Active |
| 4 | backtest | Signal test and performance | ✅ Active |
| 5 | broker_sandbox | Paper order execution | ✅ Active |

All other connectors are **disabled** in MVP.

---

## What's Implemented (v1.0)

### Agent Layer
- `risk_guard` — Portfolio-context-enriched risk evaluation
- `execution_ops` — Dual-gate: risk check + human approval before execution

### MCP Server
- `mcp/server.py` — Full StdIO MCP server with 7 tools
- `mcp/tools/market_data.py`
- `mcp/tools/research_execution.py`

### API & Middleware
- FastAPI app with rate limiting + request size limits
- CORS env-driven configuration
- Tenacity retry decorator on connectors
- Env-configurable risk limits (`risk_policy.py`)

### Infrastructure
- `Dockerfile` — Production-ready with healthcheck
- `docker-compose.yml` — API + MCP services
- `.github/workflows/ci.yml` — Test matrix (Python 3.11 / 3.12 + Docker build)

### Tests (17 cases)
- `test_risk_guard_agent.py` (4)
- `test_execution_ops_agent.py` (4)
- `test_security_middleware.py` (3)
- `test_mcp_server.py` (6)

---

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn apps.fincept_aiops.app:app --reload --port 8000
pytest -q
```

---

## Startup Sequence

1. Create storage dirs
2. Start FastAPI app (port 8000)
3. Start MCP server (`python mcp/server.py`)
4. Import N8N workflows
5. Run smoke tests (`pytest -q`)
6. Activate paper flows

---

## Hard Limits

- ❌ No live trading
- ❌ No prompt-based risk override
- ❌ No broker action without audit
- ❌ Max 6 agents
- ❌ Max 5 active connectors
- ❌ Max 1 risk policy source

---

## Realization Scope

| Phase | Scope | Decision |
|---|---|---|
| 1 | Research + briefing + paper broker | ✅ MVP |
| 2 | Backtest + screening + approval gate | ✅ MVP+ |
| 3 | Sandboxed broker integration | ⏳ Pilot |
| 4 | Live trading | ❌ No-Go |
| 5 | Multi-broker, full automation | 💤 V2 |

---

## Docs

See [`docs/`](./docs/) for full architecture, API contracts, deployment guide, ops playbook, and decision matrix.
