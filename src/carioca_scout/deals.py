"""deals.json export (REQ alerting#3 + dashboard contract).

deals.json is the ONLY contract between backend and frontend.
Its shape is a spec (openspec/specs/dashboard/spec.md) — if you change
a field name here you must change the spec and app.js in the same change.

Shape:
{
  "generated_at": "2026-07-12T09:00:00",
  "deals": [
    {
      "origin": "GIG", "dest": "POA", "travel_date": "2026-11-20",
      "holiday": "Consciência Negra",
      "price_brl": 380.0, "baseline_brl": 520.0,
      "drop_pct": 26.9,
      "trend": [520.0, 515.0, ...]     # last N daily minimums, for sparkline
    }
  ]
}
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Deal:
    origin: str
    dest: str
    travel_date: str
    holiday: str
    price_brl: float
    baseline_brl: float
    drop_pct: float
    trend: list[float]


def build_deal(*, origin: str, dest: str, travel_date: str, holiday: str,
               price: float, baseline: float, trend: list[float]) -> Deal:
    drop_pct = round((baseline - price) / baseline * 100, 1)
    return Deal(origin, dest, travel_date, holiday,
                round(price, 2), round(baseline, 2), drop_pct, trend[-14:])


def export_deals(deals: list[Deal], path: Path,
                 now: datetime | None = None) -> None:
    payload = {
        "generated_at": (now or datetime.now()).isoformat(timespec="seconds"),
        "deals": [asdict(d) for d in sorted(
            deals, key=lambda d: d.drop_pct, reverse=True)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                    encoding="utf-8")
