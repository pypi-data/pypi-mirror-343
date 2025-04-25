from __future__ import annotations

from decimal import Decimal
from typing import Protocol


class Taxable(Protocol):
    tax_name: str
    tax_rate: Decimal
    tax_value: Decimal
    gross_value: Decimal
    description: str | None


def get_tax_category(item: Taxable) -> str | None:
    # We store the tax category in the tax_name field of the item
    # N1 is used for hotel services, N2.2 for donations

    tax_name = item.tax_name.upper()

    if tax_name in ("N1", "N2.2"):
        return tax_name

    # Returning None is excpected, the tax category is
    # only used when the tax rate is 0.00, and in that case
    # we do have a validation

    # # but we also check if the item price is 10.00 for donations
    if item.tax_value == Decimal("0.00"):
        if item.gross_value == Decimal("10.00"):
            return "N2.2"

        if (
            item.description
            and "python italia association membership" in item.description.lower()
        ):
            return "N2.2"

        if item.description and "hotel" in item.description.lower():
            return "N1"

    return None
