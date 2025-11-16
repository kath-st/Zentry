from pathlib import Path
from datetime import datetime, timedelta, timezone
import pandas as pd

ISO = "%Y-%m-%dT%H:%M:%S%z"

class ReservationsExcelRepo:
    def __init__(self, storage_dir: str | Path = "storage"):
        self.path = Path(storage_dir) / "reservations.xlsx"
        self.sheet = "Reservations"

    def _read(self) -> pd.DataFrame:
        return pd.read_excel(self.path, sheet_name=self.sheet, dtype=str)

    def _write(self, df: pd.DataFrame):
        with pd.ExcelWriter(self.path, engine="openpyxl", mode="w") as w:
            df.to_excel(w, sheet_name=self.sheet, index=False)

    def hold(self, reservation_id: str, event_id: int, zone_id: str, qty: int, user_id: str, ttl_minutes: int):
        now = datetime.now(timezone.utc).astimezone()
        created_at = now.strftime(ISO)
        expiry_at = (now + timedelta(minutes=ttl_minutes)).strftime(ISO)
        df = self._read()
        new_row = {
            "reservation_id": reservation_id,
            "event_id": str(event_id),
            "zone_id": zone_id,
            "qty": str(qty),
            "user_id": user_id,
            "created_at": created_at,
            "expiry_at": expiry_at,
            "status": "pending",
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self._write(df)

    def update_status(self, reservation_id: str, status: str):
        df = self._read()
        idx = df.index[df["reservation_id"] == reservation_id]
        if len(idx) == 0:
            raise KeyError(f"Reservation {reservation_id} not found")
        df.loc[idx, "status"] = status
        self._write(df)

    def release(self, reservation_id: str): self.update_status(reservation_id, "released")
    def confirm(self, reservation_id: str): self.update_status(reservation_id, "confirmed")

    def is_expired(self, reservation_id: str) -> bool:
        df = self._read()
        row = df[df["reservation_id"] == reservation_id]
        if row.empty:
            raise KeyError(f"Reservation {reservation_id} not found")
        exp = datetime.strptime(row.iloc[0]["expiry_at"], ISO)
        now = datetime.now(exp.tzinfo)
        return exp < now

__all__ = ["ReservationsExcelRepo"]
