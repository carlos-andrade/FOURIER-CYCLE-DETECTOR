from datetime import datetime, timezone
from decimal import Decimal
import pytest
from fourier_gyroscope.market_data.models import AggressorSource, InstrumentIdentity, TradeEvent
from fourier_gyroscope.market_data.sequence import audit_sequence

def event(**changes):
    values = dict(source_id='LOCAL', dataset_id='FIXTURE', instrument_id='WINFUT_TEST', event_at=datetime(2026, 1, 1, tzinfo=timezone.utc), price=Decimal('130000'), quantity=Decimal('1'))
    values.update(changes)
    return TradeEvent(**values)

def test_event_requires_timezone_aware_timestamp():
    with pytest.raises(ValueError): event(event_at=datetime(2026, 1, 1))

def test_observed_aggressor_requires_explicit_side():
    with pytest.raises(ValueError): event(aggressor_source=AggressorSource.OBSERVED)

def test_proxy_requires_method():
    with pytest.raises(ValueError): event(aggressor_source=AggressorSource.PROXY, aggressor_side='BUY')

def test_unknown_cannot_carry_side():
    with pytest.raises(ValueError): event(aggressor_side='BUY')

def test_instrument_requires_source_identity():
    with pytest.raises(ValueError): InstrumentIdentity('', 'B3')

def test_sequence_detects_gap():
    result = audit_sequence([10, 11, 13], source_id='P', stream_id='S', channel_id='C', sequence_scope='session')
    assert result.missing_sequence_count == 1 and not result.synchronized

def test_sequence_detects_duplicate_and_out_of_order():
    result = audit_sequence([1, 3, 2, 2], source_id='P', stream_id='S', channel_id='C', sequence_scope='session')
    assert result.duplicate_count == 1 and result.out_of_order_count == 1 and not result.synchronized

def test_contiguous_sequence_passes():
    result = audit_sequence([101, 102, 103], source_id='P', stream_id='S', channel_id='C', sequence_scope='session')
    assert result.synchronized and result.missing_sequence_count == 0

def test_unknown_aggressor_is_explicit():
    item = event()
    assert item.aggressor_source == AggressorSource.UNKNOWN and item.aggressor_side is None
