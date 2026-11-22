from __future__ import annotations
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterator, Mapping
from .models import AggressorSource, TradeEvent

REQUIRED_COLUMNS = {'instrument_id', 'event_at', 'price', 'quantity'}


def iter_trade_csv(path: str | Path, *, source_id: str, dataset_id: str, delimiter: str = ',', column_map: Mapping[str, str] | None = None, timestamp_format: str | None = None) -> Iterator[TradeEvent]:
    mapping = {'instrument_id':'instrument_id','event_at':'event_at','price':'price','quantity':'quantity','official_event_id':'official_event_id','sequence_number':'sequence_number','stream_id':'stream_id','channel_id':'channel_id','aggressor_side':'aggressor_side'}
    if column_map:
        mapping.update(column_map)
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    with file_path.open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        if not reader.fieldnames:
            raise ValueError('CSV header is missing')
        missing = {mapping[key] for key in REQUIRED_COLUMNS} - set(reader.fieldnames)
        if missing:
            raise ValueError(f'missing required CSV columns: {sorted(missing)}')
        for line_number, row in enumerate(reader, start=2):
            try:
                raw_time = (row.get(mapping['event_at']) or '').strip()
                timestamp = datetime.strptime(raw_time, timestamp_format) if timestamp_format else datetime.fromisoformat(raw_time.replace('Z', '+00:00'))
                if timestamp.tzinfo is None or timestamp.utcoffset() is None:
                    raise ValueError('timestamp requires explicit UTC offset; timezone is never guessed')
                price = Decimal((row.get(mapping['price']) or '').strip())
                quantity = Decimal((row.get(mapping['quantity']) or '').strip())
                seq = (row.get(mapping['sequence_number']) or '').strip()
                side = (row.get(mapping['aggressor_side']) or '').strip().upper()
                kwargs = {}
                if side in {'BUY','SELL'}:
                    kwargs.update(aggressor_source=AggressorSource.OBSERVED, aggressor_side=side)
                yield TradeEvent(source_id=source_id, dataset_id=dataset_id, instrument_id=(row.get(mapping['instrument_id']) or '').strip(), event_at=timestamp, price=price, quantity=quantity, official_event_id=(row.get(mapping['official_event_id']) or '').strip() or None, sequence_number=int(seq) if seq else None, stream_id=(row.get(mapping['stream_id']) or '').strip() or None, channel_id=(row.get(mapping['channel_id']) or '').strip() or None, **kwargs)
            except (ValueError, InvalidOperation, TypeError) as exc:
                raise ValueError(f'invalid trade record at CSV line {line_number}: {exc}') from exc
