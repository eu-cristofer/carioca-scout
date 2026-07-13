from datetime import date

import pytest

from carioca_scout.history import PriceHistory, SCHEMA_VERSION


@pytest.fixture
def store(tmp_path):
    return PriceHistory(tmp_path / "price_history.json")


D_TRAVEL = date(2026, 11, 20)


class TestRecordAndSeries:
    def test_records_daily_minimum(self, store):
        store.record("GIG", "POA", D_TRAVEL, date(2026, 7, 1), 500.0)
        assert store.series("GIG", "POA", D_TRAVEL) == [500.0]

    def test_same_day_rerun_keeps_lowest_price(self, store):
        """REQ price-monitoring#5: one record per day = the MINIMUM."""
        store.record("GIG", "POA", D_TRAVEL, date(2026, 7, 1), 500.0)
        store.record("GIG", "POA", D_TRAVEL, date(2026, 7, 1), 480.0)
        store.record("GIG", "POA", D_TRAVEL, date(2026, 7, 1), 999.0)
        assert store.series("GIG", "POA", D_TRAVEL) == [480.0]

    def test_series_is_chronological_even_if_recorded_out_of_order(self, store):
        store.record("GIG", "POA", D_TRAVEL, date(2026, 7, 2), 490.0)
        store.record("GIG", "POA", D_TRAVEL, date(2026, 7, 1), 500.0)
        assert store.series("GIG", "POA", D_TRAVEL) == [500.0, 490.0]

    def test_routes_are_isolated(self, store):
        store.record("GIG", "POA", D_TRAVEL, date(2026, 7, 1), 500.0)
        store.record("SDU", "FLN", D_TRAVEL, date(2026, 7, 1), 700.0)
        assert store.series("SDU", "FLN", D_TRAVEL) == [700.0]

    def test_non_positive_price_rejected(self, store):
        with pytest.raises(ValueError):
            store.record("GIG", "POA", D_TRAVEL, date(2026, 7, 1), -10.0)


class TestPersistence:
    def test_roundtrip(self, tmp_path):
        path = tmp_path / "price_history.json"
        a = PriceHistory(path)
        a.record("GIG", "NYC", D_TRAVEL, date(2026, 7, 1), 3200.0)
        a.save()

        b = PriceHistory(path)
        assert b.series("GIG", "NYC", D_TRAVEL) == [3200.0]

    def test_unknown_schema_version_refuses_to_load(self, tmp_path):
        path = tmp_path / "price_history.json"
        path.write_text('{"schema_version": 99, "routes": {}}')
        with pytest.raises(ValueError, match="schema_version"):
            PriceHistory(path)

    def test_current_schema_version_is_pinned(self):
        # If you bump this, write a migration first.
        assert SCHEMA_VERSION == 1
