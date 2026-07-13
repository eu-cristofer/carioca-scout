#!/usr/bin/env python3
"""Cron entrypoint — the ONLY place where real adapters are wired.

Everything imported here is already covered by tests through fakes;
this file only does composition + logging, so it stays thin on purpose.
"""

import logging
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from carioca_scout.config import DEFAULT
from carioca_scout.holidays import StaticCalendarProvider
from carioca_scout.pipeline import daily_run, publish

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(),
              logging.FileHandler("carioca_scout.log")],
)
log = logging.getLogger("carioca-scout")

REPO_DIR = Path(__file__).resolve().parent.parent


def load_calendar():
    """Production would call the AI endpoint here and cache the JSON;
    on failure we fall back to the last cached calendar
    (REQ holiday-calendar#3). The sample repo ships only the fallback."""
    cache = REPO_DIR / "data" / "holidays_cache.json"
    if not cache.exists():
        log.warning("no holiday cache found — seeding with sample calendar")
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(SAMPLE_CALENDAR, encoding="utf-8")
    return StaticCalendarProvider(cache.read_text(encoding="utf-8"))


SAMPLE_CALENDAR = """[
  {"date": "2026-11-20", "name": "Consciência Negra", "scope": "BR-RJ-state"},
  {"date": "2027-01-20", "name": "São Sebastião", "scope": "BR-RJ-rio-municipal"},
  {"date": "2027-04-23", "name": "São Jorge", "scope": "BR-RJ-state"}
]"""


def load_price_provider():
    """Swap in a real PriceProvider adapter here.
    Read .opencode/skills/scraper-etiquette/SKILL.md BEFORE writing it."""
    from carioca_scout.prices import FakePriceProvider
    log.warning("using FakePriceProvider — wire a real adapter for production")
    return FakePriceProvider({})


def main() -> int:
    today = date.today()
    log.info("daily run starting for %s", today)
    deals = daily_run(cfg=DEFAULT, calendar=load_calendar(),
                      prices=load_price_provider(), today=today)
    log.info("found %d deal(s)", len(deals))
    try:
        publish(DEFAULT.deals_path, REPO_DIR)
        log.info("deals.json committed and pushed")
    except Exception:
        log.exception("publish failed — deals.json is still on disk")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
