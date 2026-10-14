# shopcart

A tiny shopping-cart library: a product catalog, discount codes, tax, and cart totals.

```bash
pip install -r requirements.txt
python -m pytest -q
```

Layout:
- `shopcart/catalog.py` — products and prices
- `shopcart/pricing.py` — discounts, tax, totals
- `shopcart/cart.py` — the `Cart` class
- `tests/` — pytest suite
