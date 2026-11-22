from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class BarTimestampSemantics(str, Enum):
    OPEN_TIME = "OPEN_TIME"
    CLOSE_TIME = "CLOSE_TIME"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class MarketBar:
    source_id: str
    dataset_id: str
    instrument_id: str
    bar_index: int
    source_counter: Optional[int]
    bar_timestamp: datetime
    timestamp_semantics: BarTimestampSemantics
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    trade_count: Optional[int] = None
    volume: Optional[Decimal] = None
    financial_volume: Optional[Decimal] = None
    source_timezone: Optional[str] = None
    timestamp_precision: str = "UNKNOWN"
    raw_sha256: Optional[str] = None
    parser_version: str = "0.1.0"

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.dataset_id.strip() or not self.instrument_id.strip():
            raise ValueError("source_id, dataset_id and instrument_id are required")
        if self.bar_index < 1:
            raise ValueError("bar_index must be positive")
        if self.source_counter is not None and self.source_counter < 1:
            raise ValueError("source_counter must be positive")
        if self.bar_timestamp.tzinfo is None or self.bar_timestamp.utcoffset() is None:
            raise ValueError("bar_timestamp must be timezone-aware; timezone is never guessed")
        if any(value <= 0 for value in (self.open, self.high, self.low, self.close)):
            raise ValueError("OHLC values must be positive")
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("high must be >= open, close and low")
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("low must be <= open, close and high")
        if self.trade_count is not None and self.trade_count < 1:
            raise ValueError("trade_count must be positive when supplied")
        if self.volume is not None and self.volume <= 0:
            raise ValueError("volume must be positive when supplied")
        if self.financial_volume is not None and self.financial_volume <= 0:
            raise ValueError("financial_volume must be positive when supplied")
        if self.raw_sha256 is not None and (
            len(self.raw_sha256) != 64
            or any(char not in "0123456789abcdefABCDEF" for char in self.raw_sha256)
        ):
            raise ValueError("raw_sha256 must be 64-character hexadecimal")
