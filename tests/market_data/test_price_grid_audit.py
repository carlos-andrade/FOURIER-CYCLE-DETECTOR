from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from fourier_gyroscope.market_data import BarTimestampSemantics, MarketBar
from fourier_gyroscope.market_data.price_grid import audit_candidate_price_grid


def make_bar(day: int, counter: int, *, open_price: str, high: str, low: str, close: str):
    return MarketBar(
        source_id="FIXTURE",
        dataset_id="GRID_AUDIT",
        instrument_id="TEST_INSTRUMENT",
        bar_index=counter,
        source_counter=counter,
        bar_timestamp=datetime(2026, 10, day, 10, counter, tzinfo=ZoneInfo("America/Sao_Paulo")),
        timestamp_semantics=BarTimestampSemantics.UNKNOWN,
        open=Decimal(open_price),
        high=Decimal(high),
        low=Decimal(low),
        close=Decimal(close),
    )


def test_candidate_grid_audit_groups_by_local_date_and_counts_fields():
    bars = [
        make_bar(13, 1, open_price="100.1", high="105.2", low="95.3", close="102.4"),
        make_bar(13, 2, open_price="100", high="105", low="95", close="100"),
        make_bar(14, 1, open_price="100", high="105", low="95", close="100"),
    ]

    result = audit_candidate_price_grid(bars, candidate_increment=Decimal("5"))

    assert len(result) == 2
    assert result[0].session_date.isoformat() == "2026-10-13"
    assert result[0].bar_count == 2
    assert result[0].bars_with_nonconforming_prices == 1
    assert result[0].nonconforming_price_fields == 4
    assert result[0].price_field_count == 8
    assert result[0].field_counts == (("open", 1), ("high", 1), ("low", 1), ("close", 1))
    assert result[0].nonconforming_bar_ratio == Decimal("0.5")
    assert result[1].session_date.isoformat() == "2026-10-14"
    assert result[1].bars_with_nonconforming_prices == 0


def test_candidate_grid_audit_does_not_mutate_source_prices():
    bar = make_bar(13, 1, open_price="100.1", high="105.2", low="95.3", close="102.4")
    original = (bar.open, bar.high, bar.low, bar.close)

    audit_candidate_price_grid([bar], candidate_increment=Decimal("5"))

    assert (bar.open, bar.high, bar.low, bar.close) == original


@pytest.mark.parametrize("increment", [Decimal("0"), Decimal("-1")])
def test_candidate_grid_audit_rejects_non_positive_increment(increment):
    with pytest.raises(ValueError, match="positive Decimal"):
        audit_candidate_price_grid([], candidate_increment=increment)


def test_candidate_grid_audit_requires_decimal_increment():
    with pytest.raises(ValueError, match="positive Decimal"):
        audit_candidate_price_grid([], candidate_increment=5)
