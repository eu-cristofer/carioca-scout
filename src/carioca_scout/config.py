"""Business-rule configuration for CariocaScout.

Every number here traces back to a requirement in openspec/specs/.
Keep rules as data (editable, testable) — never bury them in logic.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ScoutConfig:
    # REQ: price-monitoring #1 — origin airports
    origins: tuple[str, ...] = ("GIG", "SDU")

    # REQ: price-monitoring #2 — monitored destinations
    destinations: tuple[str, ...] = ("POA", "FLN", "NYC", "FLR")

    # REQ: alerting #1 — trigger only on a drop of >= 25% vs 30-day moving average
    drop_threshold: float = 0.25
    moving_average_days: int = 30

    # REQ: price-monitoring #4 — coverage window of 12 months ahead
    coverage_months: int = 12

    # REQ: holiday-calendar #1 — RJ state + municipal holidays (and bridge days)
    holiday_scope: tuple[str, ...] = ("BR-RJ-state", "BR-RJ-rio-municipal")

    # Storage paths (overridable in tests)
    data_dir: Path = field(default_factory=lambda: Path("data"))

    @property
    def history_path(self) -> Path:
        return self.data_dir / "price_history.json"

    @property
    def deals_path(self) -> Path:
        # docs/ so GitHub Pages serves it directly
        return Path("docs") / "deals.json"


DEFAULT = ScoutConfig()
