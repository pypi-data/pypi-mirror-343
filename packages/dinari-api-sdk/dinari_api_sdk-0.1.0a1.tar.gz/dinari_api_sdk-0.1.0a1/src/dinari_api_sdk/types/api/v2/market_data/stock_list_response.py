# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ....._models import BaseModel

__all__ = ["StockListResponse", "StockListResponseItem"]


class StockListResponseItem(BaseModel):
    id: str
    """Unique identifier for the stock"""

    is_fractionable: bool
    """Whether the stock allows for fractional trading.

    If it is not fractionable, Dinari only supports limit orders for the stock.
    """

    name: str
    """Stock Name"""

    symbol: str
    """Ticker symbol of the stock"""

    cik: Optional[str] = None
    """SEC Central Index Key.

    Refer to
    [this link](https://www.sec.gov/submit-filings/filer-support-resources/how-do-i-guides/understand-utilize-edgar-ciks-passphrases-access-codes)
    """

    composite_figi: Optional[str] = None
    """Composite FIGI ID. Refer to [this link](https://www.openfigi.com/about/figi)"""

    cusip: Optional[str] = None
    """CUSIP ID. Refer to [this link](https://www.cusip.com/identifiers.html)"""

    description: Optional[str] = None
    """Description of the company and what they do/offer."""

    display_name: Optional[str] = None
    """Name of Stock for application display"""

    logo_url: Optional[str] = None
    """The URL of the logo of the stock. The preferred format is svg."""


StockListResponse: TypeAlias = List[StockListResponseItem]
