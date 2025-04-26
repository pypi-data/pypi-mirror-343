# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SpanUpdateParams"]


class SpanUpdateParams(TypedDict, total=False):
    data: Dict[str, object]

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    name: str

    output: Dict[str, object]
