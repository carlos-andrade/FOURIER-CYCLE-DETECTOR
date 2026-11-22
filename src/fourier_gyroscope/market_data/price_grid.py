from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable

from .bars import MarketBar


OHLC_FIELDS = ("open", "high", "low", "close")


@dataclass(frozen=True)
class PriceGridSessionAudit:
    """Observed conformity to a caller-supplied candidate price increment."""

    session_date: date
    candidate_increment: Decimal
    bar_count: int
    bars_with_nonconforming_prices: int
    nonconforming_price_fields: int
    price_field_count: int
    field_counts: tuple[tuple[str, int], ...]

    @property
    def nonconforming_bar_ratio(self) -> Decimal:
        if self.bar_count == 0:
            return Decimal("0")
        return Decimal(self.bars_with_nonconforming_prices) / Decimal(self.bar_count)


def audit_candidate_price_grid(
    bars: Iterable[MarketBar],
    *,
    candidate_increment: Decimal,
) -> tuple[PriceGridSessionAudit, ...]:
    """Audit OHLC values against a candidate increment, grouped by local session date.

    This is a descriptive diagnostic only. The increment is supplied by the
    caller and is not validated against an exchange contract or instrument
    master. Source prices are never rounded, rescaled, or modified.

    Pass bars from one instrument/dataset and with timestamps normalized to
    the intended market timezone. The timestamp's calendar date defines the
    session bucket; overnight-session calendars require an explicit upstream
    session-date mapping and are not inferred here.
    """
    if not isinstance(candidate_increment, Decimal) or candidate_increment <= 0:
        raise ValueError("candidate_increment must be a positive Decimal")

    grouped: dict[date, list[MarketBar]] = defaultdict(list)
    for bar in bars:
        grouped[bar.bar_timestamp.date()].append(bar)

    audits: list[PriceGridSessionAudit] = []
    for session_date, session_bars in sorted(grouped.items()):
        field_counts = {field: 0 for field in OHLC_FIELDS}
        affected_bars = 0
        affected_fields = 0

        for bar in session_bars:
            bar_affected = False
            for field in OHLC_FIELDS:
                value = getattr(bar, field)
                if value % candidate_increment != 0:
                    field_counts[field] += 1
                    affected_fields += 1
                    bar_affected = True
            if bar_affected:
                affected_bars += 1

        audits.append(
            PriceGridSessionAudit(
                session_date=session_date,
                candidate_increment=candidate_increment,
                bar_count=len(session_bars),
                bars_with_nonconforming_prices=affected_bars,
                nonconforming_price_fields=affected_fields,
                price_field_count=len(session_bars) * len(OHLC_FIELDS),
                field_counts=tuple((field, field_counts[field]) for field in OHLC_FIELDS),
            )
        )

    return tuple(audits)
