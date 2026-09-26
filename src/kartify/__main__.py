from decimal import Decimal

from kartify import Cart, Item


def main() -> None:
    cart = Cart()
    cart.add(Item("apple", Decimal("0.50")), 4)
    cart.add(Item("bread", Decimal("2.25")))
    cart.add(Item("milk", Decimal("1.99")), 2)

    for item, qty in cart:
        print(f"{item.name:<10} {qty:>3} x {item.price:>6}")
    print(f"{'Total':<10} {len(cart):>3} items  {cart.total:>6}")


if __name__ == "__main__":
    main()
