"""Product catalog. Prices are stored in integer cents to avoid float rounding."""
from __future__ import annotations

PRODUCTS = {
    "MUG": {"name": "Coffee mug", "price_cents": 1200},
    "TEE": {"name": "T-shirt", "price_cents": 2000},
    "CAP": {"name": "Baseball cap", "price_cents": 1500},
    "STICKER": {"name": "Sticker pack", "price_cents": 300},
}


def price_of(sku: str) -> int:
    """Return the unit price of a SKU in cents."""
    try:
        return PRODUCTS[sku]["price_cents"]
    except KeyError:
        raise ValueError(f"unknown SKU: {sku}") from None
