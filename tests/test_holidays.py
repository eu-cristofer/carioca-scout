import json
from datetime import date

from carioca_scout.holidays import (
    Holiday,
    StaticCalendarProvider,
    derive_window,
    travel_windows,
)


def h(iso: str, name: str = "Feriado") -> Holiday:
    return Holiday(on=date.fromisoformat(iso), name=name, scope="BR-RJ-state")


class TestBridgeDerivation:
    """The 'emenda' rules — pinned exhaustively by weekday."""

    def test_tuesday_holiday_bridges_monday(self):
        # 2026-04-21 (Tiradentes) is a Tuesday
        w = derive_window(h("2026-04-21"))
        assert (w.start, w.end, w.has_bridge) == (
            date(2026, 4, 18), date(2026, 4, 21), True)

    def test_thursday_holiday_bridges_friday(self):
        # 2026-06-04 (Corpus Christi) is a Thursday
        w = derive_window(h("2026-06-04"))
        assert (w.start, w.end, w.has_bridge) == (
            date(2026, 6, 4), date(2026, 6, 7), True)

    def test_monday_holiday_is_natural_long_weekend(self):
        w = derive_window(h("2026-10-12"))  # Monday
        assert (w.start, w.has_bridge) == (date(2026, 10, 10), False)

    def test_friday_holiday_is_natural_long_weekend(self):
        w = derive_window(h("2026-11-20"))  # Consciência Negra, Friday
        assert (w.end, w.has_bridge) == (date(2026, 11, 22), False)

    def test_wednesday_holiday_has_no_bridge(self):
        w = derive_window(h("2026-01-21"))  # Wednesday
        assert (w.start, w.end, w.has_bridge) == (
            date(2026, 1, 21), date(2026, 1, 21), False)


class TestStaticProvider:
    PAYLOAD = json.dumps([
        {"date": "2026-01-20", "name": "São Sebastião",
         "scope": "BR-RJ-rio-municipal"},
        {"date": "2026-04-23", "name": "São Jorge", "scope": "BR-RJ-state"},
        {"date": "2027-01-20", "name": "São Sebastião",
         "scope": "BR-RJ-rio-municipal"},
    ])

    def test_filters_by_year_and_sorts(self):
        provider = StaticCalendarProvider(self.PAYLOAD)
        names = [x.on for x in provider.holidays(2026)]
        assert names == [date(2026, 1, 20), date(2026, 4, 23)]

    def test_travel_windows_pipeline(self):
        provider = StaticCalendarProvider(self.PAYLOAD)
        windows = travel_windows(provider, 2026)
        assert len(windows) == 2
        # São Jorge 2026-04-23 is a Thursday -> Friday bridge
        assert windows[1].has_bridge is True
