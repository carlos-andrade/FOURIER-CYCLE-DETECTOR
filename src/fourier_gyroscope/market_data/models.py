from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

class AggressorSource(str, Enum):
    OBSERVED = 'OBSERVED'
    PROXY = 'PROXY'
    UNKNOWN = 'UNKNOWN'

class FeedGranularity(str, Enum):
    TRADE = 'TRADE'
    MBO = 'MBO'
    MBP = 'MBP'
    TOB = 'TOB'
    CONFLATED = 'CONFLATED'
    DAILY_BAR = 'DAILY_BAR'

@dataclass(frozen=True)
class InstrumentIdentity:
    instrument_id: str
    source_id: str
    symbol: Optional[str] = None
    contract_code: Optional[str] = None
    expiry_date: Optional[date] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
    tick_size: Optional[Decimal] = None
    multiplier: Optional[Decimal] = None
    currency: Optional[str] = None

    def __post_init__(self):
        if not self.instrument_id.strip() or not self.source_id.strip():
            raise ValueError('instrument_id and source_id are required')
        if self.tick_size is not None and self.tick_size <= 0:
            raise ValueError('tick_size must be positive')
        if self.multiplier is not None and self.multiplier <= 0:
            raise ValueError('multiplier must be positive')
        if self.valid_from and self.valid_to and self.valid_to <= self.valid_from:
            raise ValueError('valid_to must be later than valid_from')

@dataclass(frozen=True)
class TradeEvent:
    source_id: str
    dataset_id: str
    instrument_id: str
    event_at: datetime
    price: Decimal
    quantity: Decimal
    granularity: FeedGranularity = FeedGranularity.TRADE
    official_event_id: Optional[str] = None
    technical_fingerprint: Optional[str] = None
    sequence_number: Optional[int] = None
    stream_id: Optional[str] = None
    channel_id: Optional[str] = None
    source_timezone: Optional[str] = None
    time_precision: str = 'UNKNOWN'
    received_at: Optional[datetime] = None
    information_available_at: Optional[datetime] = None
    aggressor_source: AggressorSource = AggressorSource.UNKNOWN
    aggressor_side: Optional[str] = None
    aggressor_method: Optional[str] = None
    raw_sha256: Optional[str] = None
    parser_version: Optional[str] = None

    def __post_init__(self):
        if not self.source_id.strip() or not self.dataset_id.strip() or not self.instrument_id.strip():
            raise ValueError('source_id, dataset_id and instrument_id are required')
        for name, value in [('event_at', self.event_at), ('received_at', self.received_at), ('information_available_at', self.information_available_at)]:
            if value is not None and (value.tzinfo is None or value.utcoffset() is None):
                raise ValueError(f'{name} must be timezone-aware')
        if self.price <= 0 or self.quantity <= 0:
            raise ValueError('price and quantity must be positive')
        if self.sequence_number is not None and self.sequence_number < 0:
            raise ValueError('sequence_number must be non-negative')
        if self.aggressor_source == AggressorSource.OBSERVED and self.aggressor_side not in {'BUY', 'SELL'}:
            raise ValueError('OBSERVED aggressor requires explicit BUY or SELL')
        if self.aggressor_source == AggressorSource.PROXY and (self.aggressor_side not in {'BUY', 'SELL'} or not self.aggressor_method):
            raise ValueError('PROXY aggressor requires side and method')
        if self.aggressor_source == AggressorSource.UNKNOWN and self.aggressor_side is not None:
            raise ValueError('UNKNOWN aggressor must not carry a side')
        if self.raw_sha256 is not None and (len(self.raw_sha256) != 64 or any(c not in '0123456789abcdefABCDEF' for c in self.raw_sha256)):
            raise ValueError('raw_sha256 must be 64-character hexadecimal')
