# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Span"]


class Span(BaseModel):
    id: str

    account_id: str

    created_by_user_id: str

    name: str

    start_timestamp: datetime

    trace_id: str
    """id for grouping traces together, uuid is recommended"""

    data: Optional[Dict[str, object]] = None

    end_timestamp: Optional[datetime] = None

    input: Optional[Dict[str, object]] = None

    object: Optional[Literal["span"]] = None

    output: Optional[Dict[str, builtins.object]] = None

    parent_id: Optional[str] = None
    """Reference to a parent span_id"""
