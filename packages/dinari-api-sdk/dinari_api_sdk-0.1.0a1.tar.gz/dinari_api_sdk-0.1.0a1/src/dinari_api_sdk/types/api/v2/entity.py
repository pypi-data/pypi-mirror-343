# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["Entity"]


class Entity(BaseModel):
    id: str
    """Unique identifier for the entity"""

    entity_type: Literal["INDIVIDUAL", "ORGANIZATION"]
    """Type of entity"""

    is_kyc_complete: bool
    """Indicates if Entity completed KYC"""

    name: Optional[str] = None
    """Name of Entity"""

    nationality: Optional[str] = None
    """Nationality of the entity"""
