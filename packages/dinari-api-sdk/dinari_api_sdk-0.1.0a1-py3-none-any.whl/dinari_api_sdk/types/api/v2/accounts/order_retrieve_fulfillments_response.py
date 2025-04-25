# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .order_fulfillment import OrderFulfillment

__all__ = ["OrderRetrieveFulfillmentsResponse"]

OrderRetrieveFulfillmentsResponse: TypeAlias = List[OrderFulfillment]
