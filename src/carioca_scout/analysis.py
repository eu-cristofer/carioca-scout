"""Analytical core: moving average, price delta and the 25% trigger.

This module is PURE — no I/O, no dates from the wall clock, no network.
That is a deliberate design decision (see openspec/specs/alerting/spec.md):
pure functions are trivially testable, which is what makes TDD cheap here.

All functions raise ValueError on invalid input rather than guessing.
"""

from __future__ import annotations

from collections.abc import Sequence


def moving_average(prices: Sequence[float], window: int = 30) -> float:
    """Mean of the last `window` observations (or all, if fewer).

    REQ alerting#2: the baseline is the moving average of the LAST 30
    daily minimum prices. With fewer than `window` points we average what
    we have — but callers should check `has_enough_history` before
    trusting the trigger (REQ alerting#4: no alerts on cold start).
    """
    if window <= 0:
        raise ValueError(f"window must be positive, got {window}")
    if not prices:
        raise ValueError("cannot average an empty price series")
    if any(p <= 0 for p in prices):
        raise ValueError("prices must be positive")
    tail = prices[-window:]
    return sum(tail) / len(tail)


def price_delta(current: float, baseline: float) -> float:
    """Relative variation of `current` vs `baseline`.

    Negative = price dropped. -0.25 means a 25% drop.
    """
    if baseline <= 0:
        raise ValueError(f"baseline must be positive, got {baseline}")
    if current <= 0:
        raise ValueError(f"current price must be positive, got {current}")
    return (current - baseline) / baseline


def is_deal(current: float, history: Sequence[float], *,
            threshold: float = 0.25, window: int = 30) -> bool:
    """True iff `current` is at least `threshold` below the moving average.

    REQ alerting#1: fire ONLY on drops of >= 25% vs the 30-day moving
    average. Exactly 25% counts (>=, not >) — this edge is pinned by
    tests/test_analysis.py::test_exactly_25_percent_drop_fires.
    """
    if not 0 < threshold < 1:
        raise ValueError(f"threshold must be in (0, 1), got {threshold}")
    baseline = moving_average(history, window)
    return price_delta(current, baseline) <= -threshold


def has_enough_history(history: Sequence[float], minimum: int = 7) -> bool:
    """Guard against cold-start false alerts (REQ alerting#4).

    With fewer than `minimum` observations the moving average is too
    noisy to act on; the pipeline records the price but never alerts.
    """
    return len(history) >= minimum
