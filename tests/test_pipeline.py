"""Integration test: one full 'cron day' in memory.

No network, no real clock, no git — every port is a fake. This is the
payoff of the Protocol-based design: the WHOLE daily run is testable.
"""

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from carioca_scout.config import ScoutConfig
from carioca_scout.holidays import StaticCalendarProvider
from carioca_scout.pipeline import daily_run
from carioca_scout.prices import FakePriceProvider

# Consciência Negra 2026 — Friday -> window starts on the holiday itself
HOLIDAY = date(2026, 11, 20)
CAL = StaticCalendarProvider(json.dumps([
    {"date": "2026-11-20", "name": "Consciência Negra",
     "scope": "BR-RJ-state"},
]))


@pytest.fixture
def cfg(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # docs/deals.json lands in tmp
    return ScoutConfig(
        origins=("GIG",), destinations=("POA",), data_dir=tmp_path / "data")


def seed_history(cfg, days=10, price=400.0):
    """Simulate `days` previous cron runs at a stable price."""
    provider = FakePriceProvider({("GIG", "POA", HOLIDAY): price})
    start = date(2026, 7, 1)
    for i in range(days):
        daily_run(cfg=cfg, calendar=CAL, prices=provider,
                  today=start + timedelta(days=i))


class TestDailyRun:
    def test_stable_prices_produce_no_deals(self, cfg):
        seed_history(cfg, days=10, price=400.0)
        provider = FakePriceProvider({("GIG", "POA", HOLIDAY): 400.0})
        deals = daily_run(cfg=cfg, calendar=CAL, prices=provider,
                          today=date(2026, 7, 11))
        assert deals == []

    def test_25_percent_crash_produces_a_deal(self, cfg):
        seed_history(cfg, days=10, price=400.0)
        provider = FakePriceProvider({("GIG", "POA", HOLIDAY): 300.0})
        deals = daily_run(cfg=cfg, calendar=CAL, prices=provider,
                          today=date(2026, 7, 11))
        assert len(deals) == 1
        assert deals[0].drop_pct == 25.0
        assert deals[0].holiday == "Consciência Negra"

        # ...and the payload the dashboard reads was actually written
        payload = json.loads(Path("docs/deals.json").read_text())
        assert payload["deals"][0]["dest"] == "POA"

    def test_cold_start_never_alerts_even_on_crash(self, cfg):
        """Day 1 of monitoring + a huge drop = still silence (REQ alerting#4)."""
        provider = FakePriceProvider({("GIG", "POA", HOLIDAY): 100.0})
        deals = daily_run(cfg=cfg, calendar=CAL, prices=provider,
                          today=date(2026, 7, 1))
        assert deals == []

    def test_provider_returning_none_is_not_an_error(self, cfg):
        provider = FakePriceProvider({})  # airline site down, no quotes
        deals = daily_run(cfg=cfg, calendar=CAL, prices=provider,
                          today=date(2026, 7, 1))
        assert deals == []

    def test_past_holidays_are_skipped(self, cfg):
        provider = FakePriceProvider({("GIG", "POA", HOLIDAY): 400.0})
        deals = daily_run(cfg=cfg, calendar=CAL, prices=provider,
                          today=date(2026, 12, 25))  # after the holiday
        assert deals == []
