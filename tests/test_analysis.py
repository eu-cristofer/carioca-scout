"""RED first: these tests were written BEFORE analysis.py existed.

Each test name states a business rule. If a test breaks, the failure
message should tell you which requirement you violated.
"""

import pytest

from carioca_scout.analysis import (
    has_enough_history,
    is_deal,
    moving_average,
    price_delta,
)


class TestMovingAverage:
    def test_simple_mean(self):
        assert moving_average([100, 200, 300], window=3) == 200

    def test_uses_only_last_window_points(self):
        # 30-day window over 40 points must ignore the first 10
        prices = [1000.0] * 10 + [500.0] * 30
        assert moving_average(prices, window=30) == 500.0

    def test_fewer_points_than_window_averages_what_exists(self):
        assert moving_average([100, 300], window=30) == 200

    def test_empty_series_raises(self):
        with pytest.raises(ValueError, match="empty"):
            moving_average([], window=30)

    def test_non_positive_price_raises(self):
        with pytest.raises(ValueError, match="positive"):
            moving_average([100, 0, 300], window=30)

    def test_non_positive_window_raises(self):
        with pytest.raises(ValueError, match="window"):
            moving_average([100], window=0)


class TestPriceDelta:
    def test_drop_is_negative(self):
        assert price_delta(current=75, baseline=100) == pytest.approx(-0.25)

    def test_rise_is_positive(self):
        assert price_delta(current=110, baseline=100) == pytest.approx(0.10)

    def test_zero_baseline_raises(self):
        with pytest.raises(ValueError):
            price_delta(current=100, baseline=0)


class TestTrigger:
    """REQ alerting#1 — fire ONLY on drops >= 25% vs 30-day average."""

    HISTORY = [400.0] * 30  # stable baseline of R$400

    def test_exactly_25_percent_drop_fires(self):
        # 400 * 0.75 = 300 — the boundary itself must alert (>=)
        assert is_deal(300.0, self.HISTORY) is True

    def test_26_percent_drop_fires(self):
        assert is_deal(296.0, self.HISTORY) is True

    def test_24_percent_drop_does_not_fire(self):
        assert is_deal(304.0, self.HISTORY) is False

    def test_price_rise_does_not_fire(self):
        assert is_deal(500.0, self.HISTORY) is False

    def test_invalid_threshold_raises(self):
        with pytest.raises(ValueError, match="threshold"):
            is_deal(300.0, self.HISTORY, threshold=1.5)


class TestColdStartGuard:
    """REQ alerting#4 — never alert with too little history."""

    def test_six_days_is_not_enough(self):
        assert has_enough_history([100.0] * 6) is False

    def test_seven_days_is_enough(self):
        assert has_enough_history([100.0] * 7) is True
