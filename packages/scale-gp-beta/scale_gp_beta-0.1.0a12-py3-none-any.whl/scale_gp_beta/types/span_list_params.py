# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["SpanListParams"]


class SpanListParams(TypedDict, total=False):
    ending_before: Optional[str]

    from_ts: int
    """The starting (oldest) timestamp window in seconds."""

    limit: int

    parents_only: Optional[bool]

    starting_after: Optional[str]

    to_ts: int
    """The ending (most recent) timestamp in seconds."""

    trace_id: Optional[str]
