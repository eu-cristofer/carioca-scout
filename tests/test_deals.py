import json
from datetime import datetime

from carioca_scout.deals import build_deal, export_deals


def make(dest="POA", price=300.0, baseline=400.0, trend=None):
    return build_deal(origin="GIG", dest=dest, travel_date="2026-11-20",
                      holiday="Consciência Negra", price=price,
                      baseline=baseline, trend=trend or [400.0, 390.0, 300.0])


class TestBuildDeal:
    def test_drop_pct_is_positive_percentage(self):
        assert make(price=300.0, baseline=400.0).drop_pct == 25.0

    def test_trend_is_capped_at_14_points_for_sparkline(self):
        deal = make(trend=[float(i) for i in range(1, 31)])
        assert len(deal.trend) == 14
        assert deal.trend[-1] == 30.0  # keeps the most recent points

    def test_money_is_rounded_to_cents(self):
        deal = make(price=299.999, baseline=400.001)
        assert deal.price_brl == 300.0
        assert deal.baseline_brl == 400.0


class TestExport:
    def test_payload_contract_for_dashboard(self, tmp_path):
        """This test IS the frontend contract. Change it consciously."""
        path = tmp_path / "deals.json"
        export_deals([make()], path, now=datetime(2026, 7, 12, 9, 0, 0))
        payload = json.loads(path.read_text(encoding="utf-8"))

        assert payload["generated_at"] == "2026-07-12T09:00:00"
        deal = payload["deals"][0]
        assert set(deal) == {"origin", "dest", "travel_date", "holiday",
                             "price_brl", "baseline_brl", "drop_pct", "trend"}

    def test_deals_sorted_by_biggest_drop_first(self, tmp_path):
        path = tmp_path / "deals.json"
        small = make(dest="POA", price=300.0, baseline=400.0)   # 25%
        big = make(dest="FLN", price=200.0, baseline=400.0)     # 50%
        export_deals([small, big], path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert [d["dest"] for d in payload["deals"]] == ["FLN", "POA"]

    def test_empty_deals_still_writes_valid_payload(self, tmp_path):
        path = tmp_path / "deals.json"
        export_deals([], path)
        assert json.loads(path.read_text(encoding="utf-8"))["deals"] == []
