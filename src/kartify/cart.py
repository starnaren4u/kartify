from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class Item:
    name: str
    price: Decimal

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("price must be non-negative")


@dataclass
class Cart:
    _lines: dict[str, tuple[Item, int]] = field(default_factory=dict)

    def add(self, item: Item, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        _, current = self._lines.get(item.name, (item, 0))
        self._lines[item.name] = (item, current + quantity)

    def remove(self, name: str, quantity: int | None = None) -> None:
        if name not in self._lines:
            raise KeyError(name)
        item, current = self._lines[name]
        if quantity is None or quantity >= current:
            del self._lines[name]
        else:
            self._lines[name] = (item, current - quantity)

    def quantity(self, name: str) -> int:
        return self._lines.get(name, (None, 0))[1]

    @property
    def total(self) -> Decimal:
        return sum(
            (item.price * qty for item, qty in self._lines.values()), Decimal("0")
        )

    def __len__(self) -> int:
        return sum(qty for _, qty in self._lines.values())

    def __iter__(self):
        return iter(self._lines.values())
