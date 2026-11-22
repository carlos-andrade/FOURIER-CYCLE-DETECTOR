from __future__ import annotations
from collections.abc import Iterable
from dataclasses import dataclass

@dataclass(frozen=True)
class SequenceContinuity:
    source_id: str
    stream_id: str
    channel_id: str
    sequence_scope: str
    first_sequence: int
    last_sequence: int
    observed_count: int
    duplicate_count: int
    out_of_order_count: int
    missing_sequence_count: int
    synchronized: bool


def audit_sequence(sequence_numbers: Iterable[int], *, source_id: str, stream_id: str, channel_id: str, sequence_scope: str) -> SequenceContinuity:
    values = list(sequence_numbers)
    if not values:
        raise ValueError('at least one sequence number is required')
    if not all(isinstance(v, int) and v >= 0 for v in values):
        raise ValueError('sequence numbers must be non-negative integers')
    if not all((source_id, stream_id, channel_id, sequence_scope)):
        raise ValueError('source, stream, channel and scope are required')
    seen = set()
    duplicates = 0
    out_of_order = 0
    for index, value in enumerate(values):
        if value in seen:
            duplicates += 1
        if index and value < values[index - 1]:
            out_of_order += 1
        seen.add(value)
    first, last = min(values), max(values)
    missing = max(0, last - first + 1 - len(seen))
    return SequenceContinuity(source_id, stream_id, channel_id, sequence_scope, first, last, len(values), duplicates, out_of_order, missing, not (duplicates or out_of_order or missing))
