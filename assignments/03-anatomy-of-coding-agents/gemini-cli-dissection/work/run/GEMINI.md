# Project context

- Python 3.10+ library; no third-party runtime dependencies.
- All money is integer **cents**. Never use floats for stored amounts.
- Run tests with `python -m pytest -q` from the repository root.
- Keep functions small; pricing rules live in `shopcart/pricing.py`, cart state in `shopcart/cart.py`.
