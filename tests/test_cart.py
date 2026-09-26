import unittest
from decimal import Decimal

from kartify import Cart, Item

APPLE = Item("apple", Decimal("0.50"))
BREAD = Item("bread", Decimal("2.25"))


class CartTests(unittest.TestCase):
    def test_empty_cart(self):
        cart = Cart()
        self.assertEqual(len(cart), 0)
        self.assertEqual(cart.total, Decimal("0"))

    def test_add_accumulates_quantity(self):
        cart = Cart()
        cart.add(APPLE, 2)
        cart.add(APPLE, 3)
        self.assertEqual(cart.quantity("apple"), 5)

    def test_total(self):
        cart = Cart()
        cart.add(APPLE, 4)
        cart.add(BREAD)
        self.assertEqual(cart.total, Decimal("4.25"))

    def test_remove_partial_and_full(self):
        cart = Cart()
        cart.add(APPLE, 3)
        cart.remove("apple", 1)
        self.assertEqual(cart.quantity("apple"), 2)
        cart.remove("apple")
        self.assertEqual(cart.quantity("apple"), 0)

    def test_remove_missing_raises(self):
        with self.assertRaises(KeyError):
            Cart().remove("ghost")

    def test_invalid_values(self):
        with self.assertRaises(ValueError):
            Item("bad", Decimal("-1"))
        with self.assertRaises(ValueError):
            Cart().add(APPLE, 0)


if __name__ == "__main__":
    unittest.main()
