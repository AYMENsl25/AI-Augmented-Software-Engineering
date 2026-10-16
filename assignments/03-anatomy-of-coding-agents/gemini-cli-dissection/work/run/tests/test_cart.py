import pytest

from shopcart import Cart


def test_empty_cart_total_is_zero():
    assert Cart().total() == 0


def test_add_single_item():
    cart = Cart()
    cart.add_item("MUG")
    assert cart.items == {"MUG": 1}
    assert cart.subtotal() == 1200


def test_add_same_item_twice_increments_quantity():
    cart = Cart()
    cart.add_item("MUG")
    cart.add_item("MUG", 2)
    assert cart.items == {"MUG": 3}


def test_remove_item_decrements_then_deletes():
    cart = Cart()
    cart.add_item("CAP", 2)
    cart.remove_item("CAP")
    assert cart.items == {"CAP": 1}
    cart.remove_item("CAP")
    assert cart.items == {}


def test_unknown_sku_raises():
    with pytest.raises(ValueError):
        Cart().add_item("NOPE")


def test_invalid_code_raises():
    with pytest.raises(ValueError):
        Cart().apply_code("FREESTUFF")


def test_total_includes_tax():
    cart = Cart()
    cart.add_item("TEE")
    assert cart.total() == 2759  # 2000 + 8% tax ($160) + $5.99 shipping (599 cents)


def test_percent_discount():
    cart = Cart()
    cart.add_item("MUG", 2)
    cart.apply_code("SAVE10")
    assert cart.total() == 2932  # ((2400 - 10%) + 8% tax) + $5.99 shipping (599 cents)


def test_fixed_discount_applied_before_tax():
    cart = Cart()
    cart.add_item("TEE")
    cart.add_item("TEE")
    cart.apply_code("TENOFF")
    assert cart.total() == 3839  # ((4000 - 1000) + 8% tax) + $5.99 shipping (599 cents)


def test_shipping_fee_applied_below_threshold():
    cart = Cart()
    cart.add_item("CAP", 3)  # subtotal 4500 (< 5000)
    # discounted: 4500, taxed: 4860, shipping: 599 -> total: 5459
    assert cart.total() == 5459


def test_free_shipping_at_or_above_threshold():
    cart = Cart()
    cart.add_item("TEE", 3)  # subtotal 6000 (>= 5000)
    # discounted: 6000, taxed: 6480, shipping: 0 -> total: 6480
    assert cart.total() == 6480


def test_free_shipping_with_discount():
    cart = Cart()
    cart.add_item("TEE", 3)  # subtotal 6000
    cart.apply_code("SAVE10")  # discounted: 5400 (>= 5000, still free shipping)
    # taxed: 5832, shipping: 0 -> total: 5832
    assert cart.total() == 5832


def test_free_shipping_at_exact_threshold():
    cart = Cart()
    cart.add_item("TEE")
    cart.add_item("CAP", 2)  # 2000 + 3000 = 5000 cents
    assert cart.total() == 5400  # 5000 + 8% tax; no shipping


def test_discount_can_move_order_below_free_shipping_threshold():
    cart = Cart()
    cart.add_item("TEE", 3)  # 6000 cents before discount
    cart.apply_code("SAVE25")  # 4500 cents after discount
    assert cart.total() == 5459  # 4500 + 8% tax + 599 shipping


def test_shipping_not_taxed():
    cart = Cart()
    cart.add_item("MUG")  # subtotal 1200 (< 5000)
    # If shipping (599) were taxed at 8%, shipping tax would be 47.92 (48).
    # Without tax on shipping: taxed subtotal (1296) + shipping (599) = 1895.
    assert cart.total() == 1895
