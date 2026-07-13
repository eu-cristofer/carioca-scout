"""Price collection (REQ price-monitoring spec).

Same pattern as holidays.py: the flaky, slow, rate-limited outside world
(flight-price API or scraper) sits behind a Protocol. Tests use
`FakePriceProvider`; production wires a real adapter in scripts/run_daily.py.

IMPORTANT: any real scraper adapter must follow the rules in
.opencode/skills/scraper-etiquette/SKILL.md (robots.txt, backoff, no
credential-gated pages). That skill exists precisely so the agent never
"helpfully" writes an abusive scraper.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class Quote:
    origin: str
    dest: str
    travel_date: date
    price_brl: float
    source: str


class PriceProvider(Protocol):
    def cheapest(self, origin: str, dest: str, travel_date: date) -> Quote | None:
        """Cheapest fare found today for one route/date, or None if
        the source had no availability. Must NOT raise on 'no results'."""
        ...


class FakePriceProvider:
    """Deterministic double for tests: returns scripted quotes."""

    def __init__(self, quotes: dict[tuple[str, str, date], float]):
        self._quotes = quotes

    def cheapest(self, origin: str, dest: str, travel_date: date) -> Quote | None:
        key = (origin, dest, travel_date)
        if key not in self._quotes:
            return None
        return Quote(origin, dest, travel_date, self._quotes[key], source="fake")
