from dataclasses import dataclass

class StockError(Exception): ...
class HoldExpired(Exception): ...
class LimitExceeded(Exception): ...

@dataclass(frozen=True)
class CartItem:
    event_id: int
    zone_id: str
    qty: int
    unit_price: float
    reservation_id: str | None = None

@dataclass
class Cart:
    user_id: str
    items: list[CartItem]

    def total_qty(self):
        return sum(i.qty for i in self.items)

    def total_amount(self):
        return sum(i.qty * i.unit_price for i in self.items)
