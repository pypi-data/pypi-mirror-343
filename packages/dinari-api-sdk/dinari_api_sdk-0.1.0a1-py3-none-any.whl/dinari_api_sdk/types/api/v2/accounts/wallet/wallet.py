# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ......_models import BaseModel

__all__ = ["Wallet"]


class Wallet(BaseModel):
    address: str
    """Address of the wallet"""

    is_aml_flagged: bool
    """Indicates whether the wallet is flagged for AML violations"""

    is_managed_wallet: bool
    """Indicates whether the wallet is a Dinari-managed wallet"""
