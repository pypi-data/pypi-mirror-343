# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import date
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["KYCDataParam"]


class KYCDataParam(TypedDict, total=False):
    country_code: Required[str]
    """
    ISO 3166-1 alpha 2 country code of citizenship or the country the organization
    is based out of.
    """

    last_name: Required[str]
    """Last name of the person"""

    address_city: str
    """City of address. Not all international addresses use this attribute."""

    address_postal_code: str
    """ZIP or postal code of residence address.

    Not all international addresses use this attribute.
    """

    address_street_1: str
    """Street name of address."""

    address_street_2: str
    """Extension of address, usually apartment or suite number."""

    address_subdivision: str
    """State or subdivision of address.

    In the US, this should be the unabbreviated name. Not all international
    addresses use this attribute.
    """

    birth_date: Annotated[Union[str, date], PropertyInfo(format="iso8601")]
    """Birth date of the individual"""

    email: Optional[str]
    """Email address"""

    first_name: Optional[str]
    """First name of the person, or name of the organization"""

    middle_name: Optional[str]
    """Middle name of the user"""

    tax_id_number: str
    """ID number of the official tax document of the country the entity belongs to"""
