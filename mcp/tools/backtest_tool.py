"""MCP tool wrapper — backtest runner."""
from apps.fincept_aiops.backtest_runner import BacktestRunner

_runner = BacktestRunner()


def run_backtest(signal: dict, price_series: list, initial_equity: float = 10_000.0) -> dict:
    return _runner.run(signal, price_series, initial_equity)
