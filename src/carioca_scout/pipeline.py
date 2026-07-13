"""Daily pipeline: calendar -> prices -> history -> analysis -> deals.

Kept as one readable function so the whole business flow is visible in
a single screen. Every dependency is injected (providers, clock, paths),
so the integration test in tests/test_pipeline.py runs the ENTIRE daily
run in memory, with zero network and zero real dates.
"""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

from .analysis import has_enough_history, is_deal, moving_average
from .config import ScoutConfig
from .deals import Deal, build_deal, export_deals
from .history import PriceHistory
from .holidays import CalendarProvider, travel_windows
from .prices import PriceProvider


def daily_run(*, cfg: ScoutConfig, calendar: CalendarProvider,
              prices: PriceProvider, today: date) -> list[Deal]:
    """One cron tick. Returns the deals found (already exported)."""
    history = PriceHistory(cfg.history_path)
    deals: list[Deal] = []

    windows = []
    for year in (today.year, today.year + 1):  # 12-month coverage window
        windows.extend(travel_windows(calendar, year))
    windows = [w for w in windows if today <= w.start]

    for window in windows:
        for origin in cfg.origins:
            for dest in cfg.destinations:
                quote = prices.cheapest(origin, dest, window.start)
                if quote is None:
                    continue  # REQ: absence of data is not an error
                history.record(origin, dest, window.start,
                               today, quote.price_brl)
                series = history.series(origin, dest, window.start)
                past = series[:-1]  # baseline excludes today's point
                if not has_enough_history(past):
                    continue  # REQ alerting#4: no cold-start alerts
                if is_deal(quote.price_brl, past,
                           threshold=cfg.drop_threshold,
                           window=cfg.moving_average_days):
                    baseline = moving_average(past, cfg.moving_average_days)
                    deals.append(build_deal(
                        origin=origin, dest=dest,
                        travel_date=window.start.isoformat(),
                        holiday=window.holiday.name,
                        price=quote.price_brl, baseline=baseline,
                        trend=series))

    history.save()
    export_deals(deals, cfg.deals_path)
    return deals


def publish(deals_path: Path, repo_dir: Path) -> None:
    """Commit and push deals.json (REQ ci-cd). Isolated so tests never
    run git; scripts/run_daily.py is the only caller in production."""
    subprocess.run(["git", "add", str(deals_path)], cwd=repo_dir, check=True)
    result = subprocess.run(
        ["git", "commit", "-m", "chore(data): daily deals refresh"],
        cwd=repo_dir)
    if result.returncode == 0:  # nothing-to-commit is fine, skip push
        subprocess.run(["git", "push"], cwd=repo_dir, check=True)
