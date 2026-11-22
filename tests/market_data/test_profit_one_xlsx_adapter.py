from datetime import datetime
from decimal import Decimal

import pytest
from openpyxl import Workbook

from fourier_gyroscope.market_data.bars import BarTimestampSemantics, MarketBar
from fourier_gyroscope.market_data.xlsx_adapter import iter_profit_one_xlsx


def make_bar(**changes):
    values = dict(
        source_id="PROFIT_ONE",
        dataset_id="FIXTURE",
        instrument_id="WINFUT_TEST",
        bar_index=1,
        source_counter=1,
        bar_timestamp=datetime(2026, 1, 1, 9, 0).astimezone(),
        timestamp_semantics=BarTimestampSemantics.UNKNOWN,
        open=Decimal("100"),
        high=Decimal("105"),
        low=Decimal("95"),
        close=Decimal("102"),
    )
    values.update(changes)
    return MarketBar(**values)


def test_market_bar_rejects_naive_timestamp():
    with pytest.raises(ValueError, match="timezone-aware"):
        make_bar(bar_timestamp=datetime(2026, 1, 1, 9, 0))


def test_market_bar_rejects_incoherent_ohlc():
    with pytest.raises(ValueError, match="high"):
        make_bar(high=Decimal("101"))


def test_market_bar_does_not_infer_trade_count_or_volume():
    item = make_bar()
    assert item.trade_count is None
    assert item.volume is None
    assert item.timestamp_semantics is BarTimestampSemantics.UNKNOWN


def test_profit_one_xlsx_adapter_sorts_bars_and_preserves_missing_trade_count(tmp_path):
    path = tmp_path / "sample.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Data", "Abertura", "Máxima", "Mínima", "Fechamento", "Contador de Candles", "INDICADOR"])
    sheet.append([datetime(2026, 1, 1, 9, 2), 102, 106, 100, 105, 2, 999])
    sheet.append([datetime(2026, 1, 1, 9, 0), 100, 104, 98, 102, 1, 888])
    workbook.save(path)

    bars = list(iter_profit_one_xlsx(
        path,
        source_id="PROFIT_ONE",
        dataset_id="FIXTURE",
        instrument_id="WINFUT_TEST",
        timezone_name="America/Sao_Paulo",
    ))

    assert [bar.bar_index for bar in bars] == [1, 2]
    assert [bar.source_counter for bar in bars] == [1, 2]
    assert bars[0].bar_timestamp.hour == 9
    assert bars[0].bar_timestamp.minute == 0
    assert all(bar.trade_count is None and bar.volume is None for bar in bars)
    assert all(bar.raw_sha256 and len(bar.raw_sha256) == 64 for bar in bars)


def test_profit_one_xlsx_adapter_requires_explicit_timezone(tmp_path):
    path = tmp_path / "sample.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Data", "Abertura", "Máxima", "Mínima", "Fechamento", "Contador de Candles"])
    sheet.append([datetime(2026, 1, 1, 9, 0), 100, 105, 95, 102, 1])
    workbook.save(path)

    with pytest.raises(ValueError, match="timezone_name"):
        list(iter_profit_one_xlsx(
            path,
            source_id="PROFIT_ONE",
            dataset_id="FIXTURE",
            instrument_id="WINFUT_TEST",
            timezone_name="",
        ))
