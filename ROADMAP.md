# Fincept AI Ops — ROADMAP

> Research-first, supervised paper trading system | FastAPI + N8N + MCP

**Status:** Production-Ready (v1.0) | **Audit Score:** 8.4/10
**Last Updated:** 2026-06-15

---

## ✅ Completed (v1.0)

- [x] FastAPI core with `/health`, `/backtest`, `/audit` endpoints
- [x] N8N workflow integration (5 active connectors)
- [x] MCP gateway with tool definitions (`mcp/tools/`)
- [x] BaseAgent abstract class (`agents/__init__.py`)
- [x] Docker build + smoke test in CI
- [x] CodeQL security analysis
- [x] Multi-Python CI matrix (3.11, 3.12)
- [x] Paper trading loop (supervised, human-in-the-loop)

---

## 🔄 In Progress (v1.1)

- [ ] **N8N workflow JSON scaffolding** (`workflows/` directory) — Issue #16
- [ ] **Live data connector** — replace stub provider with real market feed
- [ ] **Strategy registry** — persistent storage for backtest strategies
- [ ] **Slack notifications** — trade alerts via zxai workspace

---

## 🗓️ Upcoming (v1.2 — Q3 2026)

- [ ] **quant-mind integration** — use QuantMind as the knowledge extraction layer
- [ ] **memory-core-mcp bridge** — store agent memory in Oracle ADB 23ai
- [ ] **Multi-agent orchestration** — Hermes execution layer integration
- [ ] **Risk dashboard** — Grafana / Metabase visualization
- [ ] **MiCA compliance layer** — for EU regulatory reporting (synergy: A-Identity-Z)

---

## 🔮 Future Vision (v2.0)

- [ ] **Chainlingo integration** — whitepaper localization for portfolio assets
- [ ] **PromptLedger** — prompt version control for all LLM calls
- [ ] **Live trading mode** — with strict circuit breakers and approval gates
- [ ] **Mobile alerts** — WhatsApp / Telegram via zxai webhook

---

## Architecture

```
FastAPI (API layer)
    ↓
BaseAgent (orchestration)
    ↓
MCP Tools ←→ N8N Workflows
    ↓
Market Data Provider (stub → live)
    ↓
Audit Log (JSONL) + State (filesystem)
```

> Synergy map: fincept-ai-ops ↔ quant-mind ↔ memory-core-mcp ↔ A-Identity-Z
