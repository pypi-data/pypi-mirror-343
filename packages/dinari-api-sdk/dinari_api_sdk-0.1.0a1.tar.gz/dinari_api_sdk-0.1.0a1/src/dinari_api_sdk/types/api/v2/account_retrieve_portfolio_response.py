# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ...._models import BaseModel

__all__ = ["AccountRetrievePortfolioResponse", "Asset"]


class Asset(BaseModel):
    amount: float
    """Total amount of the stock"""

    market_value: float
    """Total market value of the stock"""

    stock_id: str
    """ID of Stock"""


class AccountRetrievePortfolioResponse(BaseModel):
    assets: List[Asset]
    """Stock Balance details for all owned stocks"""
