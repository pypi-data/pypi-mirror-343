# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import date
from typing_extensions import TypeAlias

from ...._models import BaseModel

__all__ = ["AccountRetrieveInterestPaymentsResponse", "AccountRetrieveInterestPaymentsResponseItem"]


class AccountRetrieveInterestPaymentsResponseItem(BaseModel):
    amount: float
    """Amount of interest paid"""

    currency: str
    """Type of currency (e.g. USD)"""

    payment_date: date
    """Date of interest payment. In US Eastern time zone"""


AccountRetrieveInterestPaymentsResponse: TypeAlias = List[AccountRetrieveInterestPaymentsResponseItem]
