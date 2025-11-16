from abc import ABC, abstractmethod

class EventService(ABC):
    @abstractmethod
    def get_zone_stock(self, event_id: int, zone_id: str) -> int: ...

    @abstractmethod
    def get_zone_price(self, event_id: int, zone_id: str, stage: str | None) -> float: ...

    @abstractmethod
    def ensure_purchase_limit(self, user_id: str, event_id: int, zone_id: str, requested_qty: int) -> None: ...
