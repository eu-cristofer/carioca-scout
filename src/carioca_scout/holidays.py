"""Holiday-calendar ingestion (REQ holiday-calendar spec).

The spec says: "consume an AI endpoint to identify and structure, as JSON,
the RJ state/municipal holiday dates and possible bridge days (emendas)".

Design decision (see openspec/changes archive): the AI endpoint sits behind
a Protocol so tests never touch the network. `AiCalendarProvider` is the
production adapter (calls the Anthropic API); `StaticCalendarProvider` is
the deterministic double used in tests and offline runs.

A 'bridge' (emenda) is derived, not asked: if a holiday lands on
Tue → Monday is a bridge day; Thu → Friday is a bridge day.
Deriving it locally keeps the AI output small and verifiable.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Protocol


@dataclass(frozen=True)
class Holiday:
    on: date
    name: str
    scope: str  # "BR-RJ-state" | "BR-RJ-rio-municipal"


@dataclass(frozen=True)
class TravelWindow:
    """A holiday plus its derived bridge days — the dates worth pricing."""
    holiday: Holiday
    start: date
    end: date
    has_bridge: bool


class CalendarProvider(Protocol):
    def holidays(self, year: int) -> list[Holiday]: ...


class StaticCalendarProvider:
    """Deterministic provider: loads holidays from a local JSON file.

    File format: [{"date": "2026-11-20", "name": "...", "scope": "..."}]
    Used in tests and as an offline fallback when the AI endpoint is
    unreachable (REQ holiday-calendar#3: the pipeline must degrade
    gracefully, never crash the cron run).
    """

    def __init__(self, payload: str):
        self._items = json.loads(payload)

    def holidays(self, year: int) -> list[Holiday]:
        out = []
        for item in self._items:
            d = date.fromisoformat(item["date"])
            if d.year == year:
                out.append(Holiday(on=d, name=item["name"], scope=item["scope"]))
        return sorted(out, key=lambda h: h.on)


def derive_window(holiday: Holiday) -> TravelWindow:
    """Expand a holiday into the travel window including bridge days.

    Rules (pinned by tests/test_holidays.py):
    - Tue holiday  -> window Sat..Tue  (Monday is the bridge)
    - Thu holiday  -> window Thu..Sun  (Friday is the bridge)
    - Mon holiday  -> window Sat..Mon  (natural long weekend, no bridge)
    - Fri holiday  -> window Fri..Sun  (natural long weekend, no bridge)
    - Wed/weekend  -> window is the day itself, no bridge
    """
    wd = holiday.on.weekday()  # Mon=0 .. Sun=6
    if wd == 1:  # Tuesday
        return TravelWindow(holiday, holiday.on - timedelta(days=3), holiday.on, True)
    if wd == 3:  # Thursday
        return TravelWindow(holiday, holiday.on, holiday.on + timedelta(days=3), True)
    if wd == 0:  # Monday
        return TravelWindow(holiday, holiday.on - timedelta(days=2), holiday.on, False)
    if wd == 4:  # Friday
        return TravelWindow(holiday, holiday.on, holiday.on + timedelta(days=2), False)
    return TravelWindow(holiday, holiday.on, holiday.on, False)


def travel_windows(provider: CalendarProvider, year: int) -> list[TravelWindow]:
    return [derive_window(h) for h in provider.holidays(year)]
