# Task

## 1. Fix the failing tests
`python -m pytest` currently fails. Make the whole suite pass by fixing the code in
`shopcart/`. The existing tests describe the intended behavior — do not edit them for
this step.

## 2. Add shipping to cart totals
- Orders pay a flat **$5.99** shipping fee (`599` cents).
- Shipping is **free** when the subtotal *after discount, before tax* is **$50.00 or more**.
- An empty cart pays no shipping.
- Shipping is **not taxed**: `total = tax(discounted subtotal) + shipping`.
- Put the shipping rule in `shopcart/pricing.py` and use it from `Cart.total()`.

Some existing tests check `Cart.total()` with values from before shipping existed. You may
update those expected values — and only those — and note why in a comment.

## 3. Test it
Add tests covering the shipping rules (including the free-shipping threshold), then run
the full suite and confirm it passes.
