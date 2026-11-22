from __future__ import annotations

import hashlib
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterator
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .bars import BarTimestampSemantics, MarketBar


REQUIRED_COLUMNS = ("Data", "Abertura", "Máxima", "Mínima", "Fechamento", "Contador de Candles")


def iter_profit_one_xlsx(
    path: str | Path,
    *,
    source_id: str,
    dataset_id: str,
    instrument_id: str,
    timezone_name: str,
    timestamp_semantics: BarTimestampSemantics = BarTimestampSemantics.UNKNOWN,
    sheet_name: str | None = None,
) -> Iterator[MarketBar]:
    """Read the OHLC/counter columns from a local Profit One workbook.

    The caller must supply the source timezone explicitly. The adapter does not
    infer that timestamps represent bar opens or closes and does not infer
    trade_count or volume from OHLC, elapsed time, or the candle counter.
    Indicator columns are deliberately ignored.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    if not all((source_id.strip(), dataset_id.strip(), instrument_id.strip(), timezone_name.strip())):
        raise ValueError("source_id, dataset_id, instrument_id and timezone_name are required")
    try:
        source_zone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"unknown IANA timezone: {timezone_name}") from exc

    try:
        from openpyxl import load_workbook
    except ImportError as exc:
        raise RuntimeError("XLSX support requires the optional dependency: pip install '.[excel]'") from exc

    raw_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
    workbook = load_workbook(file_path, read_only=True, data_only=True)
    try:
        if sheet_name is None:
            worksheet = workbook.active
        elif sheet_name in workbook.sheetnames:
            worksheet = workbook[sheet_name]
        else:
            raise ValueError(f"worksheet not found: {sheet_name}")

        rows = worksheet.iter_rows(values_only=True)
        header = next(rows, None)
        if header is None:
            raise ValueError("worksheet is empty")
        positions = {str(value).strip(): index for index, value in enumerate(header) if value is not None}
        missing = [name for name in REQUIRED_COLUMNS if name not in positions]
        if missing:
            raise ValueError(f"missing required columns: {missing}")

        parsed: list[tuple[datetime, int, Decimal, Decimal, Decimal, Decimal, str]] = []
        for row_number, row in enumerate(rows, start=2):
            if not row or all(value is None for value in row):
                continue
            try:
                raw_timestamp = row[positions["Data"]]
                if not isinstance(raw_timestamp, datetime):
                    raise ValueError("Data must be an Excel datetime value")
                if raw_timestamp.tzinfo is None or raw_timestamp.utcoffset() is None:
                    timestamp = raw_timestamp.replace(tzinfo=source_zone)
                else:
                    timestamp = raw_timestamp
                counter_value = row[positions["Contador de Candles"]]
                counter_decimal = Decimal(str(counter_value))
                if counter_decimal != counter_decimal.to_integral_value():
                    raise ValueError("Contador de Candles must be an integer")
                source_counter = int(counter_decimal)

                def decimal_value(column: str) -> Decimal:
                    value = row[positions[column]]
                    if value is None:
                        raise ValueError(f"{column} is empty")
                    return Decimal(str(value))

                open_value = decimal_value("Abertura")
                high_value = decimal_value("Máxima")
                low_value = decimal_value("Mínima")
                close_value = decimal_value("Fechamento")
                precision = "MINUTE" if timestamp.second == 0 and timestamp.microsecond == 0 else "SECOND_OR_BETTER"
                parsed.append((
                    timestamp, source_counter, open_value, high_value, low_value, close_value, precision
                ))
            except (ValueError, InvalidOperation, TypeError, IndexError) as exc:
                raise ValueError(f"invalid workbook record at row {row_number}: {exc}") from exc
    finally:
        workbook.close()

    # The workbook may be exported newest-first. Sort chronologically and use
    # the source candle counter to preserve order when timestamps share a minute.
    parsed.sort(key=lambda item: (item[0], item[1]))
    for bar_index, item in enumerate(parsed, start=1):
        timestamp, source_counter, open_value, high_value, low_value, close_value, precision = item
        yield MarketBar(
            source_id=source_id,
            dataset_id=dataset_id,
            instrument_id=instrument_id,
            bar_index=bar_index,
            source_counter=source_counter,
            bar_timestamp=timestamp,
            timestamp_semantics=timestamp_semantics,
            open=open_value,
            high=high_value,
            low=low_value,
            close=close_value,
            trade_count=None,
            volume=None,
            financial_volume=None,
            source_timezone=timezone_name,
            timestamp_precision=precision,
            raw_sha256=raw_hash,
        )
