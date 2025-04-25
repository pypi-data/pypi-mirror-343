# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["AccountRetrieveCashResponse"]


class AccountRetrieveCashResponse(BaseModel):
    amount: float
    """Total amount of cash and cash equivalents"""

    currency: str
    """Currency (e.g. USD)"""
