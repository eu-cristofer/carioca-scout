"""Local temporal store: price_history.json.

Schema (versioned so future migrations are possible):
{
  "schema_version": 1,
  "routes": {
    "GIG-POA:2026-11-20": {           # route key = origin-dest:travel_date
      "observations": [
        {"observed_on": "2026-07-12", "min_price_brl": 512.30}
      ]
    }
  }
}

One record per route per calendar day — the DAILY MINIMUM
(REQ price-monitoring#5). Re-running the pipeline on the same day
overwrites that day's observation with the lower of the two.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class Observation:
    observed_on: date
    min_price_brl: float


def route_key(origin: str, dest: str, travel_date: date) -> str:
    return f"{origin}-{dest}:{travel_date.isoformat()}"


class PriceHistory:
    def __init__(self, path: Path):
        self.path = path
        self._data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if raw.get("schema_version") != SCHEMA_VERSION:
                raise ValueError(
                    f"unsupported schema_version {raw.get('schema_version')!r} "
                    f"in {self.path} (expected {SCHEMA_VERSION})"
                )
            return raw
        return {"schema_version": SCHEMA_VERSION, "routes": {}}

    def record(self, origin: str, dest: str, travel_date: date,
               observed_on: date, price_brl: float) -> None:
        """Record today's minimum. Idempotent per (route, observed_on):
        keeps the LOWEST price seen that day (REQ price-monitoring#5)."""
        if price_brl <= 0:
            raise ValueError(f"price must be positive, got {price_brl}")
        key = route_key(origin, dest, travel_date)
        route = self._data["routes"].setdefault(key, {"observations": []})
        day = observed_on.isoformat()
        for obs in route["observations"]:
            if obs["observed_on"] == day:
                obs["min_price_brl"] = min(obs["min_price_brl"], price_brl)
                return
        route["observations"].append(
            {"observed_on": day, "min_price_brl": price_brl}
        )

    def series(self, origin: str, dest: str, travel_date: date) -> list[float]:
        """Chronological daily-minimum series for one route."""
        key = route_key(origin, dest, travel_date)
        route = self._data["routes"].get(key, {"observations": []})
        ordered = sorted(route["observations"], key=lambda o: o["observed_on"])
        return [o["min_price_brl"] for o in ordered]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
