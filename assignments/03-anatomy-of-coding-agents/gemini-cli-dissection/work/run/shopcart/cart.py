"""Shopping cart."""
from __future__ import annotations

from .catalog import price_of
from .pricing import final_total, validate_code


class Cart:
    def __init__(self) -> None:
        self.items: dict[str, int] = {}  # sku -> quantity
        self.discount_code: str | None = None

    def add_item(self, sku: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        price_of(sku)  # raises on unknown SKU
        self.items[sku] = self.items.get(sku, 0) + quantity

    def remove_item(self, sku: str, quantity: int = 1) -> None:
        if sku not in self.items:
            raise KeyError(sku)
        remaining = self.items[sku] - quantity
        if remaining > 0:
            self.items[sku] = remaining
        else:
            del self.items[sku]

    def apply_code(self, code: str) -> None:
        validate_code(code)
        self.discount_code = code

    def subtotal(self) -> int:
        return sum(price_of(sku) * qty for sku, qty in self.items.items())

    def total(self) -> int:
        return final_total(self.subtotal(), self.discount_code)
