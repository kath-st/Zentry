from pathlib import Path
import pandas as pd

class EventsExcelRepo:
    def __init__(self, storage_dir: str | Path = "storage"):
        self.events_xlsx = Path(storage_dir) / "events.xlsx"

    def _read(self, sheet: str) -> pd.DataFrame:
        return pd.read_excel(self.events_xlsx, sheet_name=sheet, dtype=str)

    def get_zone_stock(self, event_id: int, zone_id: str) -> int:
        df = self._read("Stock")
        row = df[(df["event_id"] == str(event_id)) & (df["zone_id"] == zone_id)]
        if row.empty:
            raise KeyError(f"Stock not found for ({event_id},{zone_id})")
        return int(row.iloc[0]["available"])

    def get_zone_price(self, event_id: int, zone_id: str, stage: str | None = None) -> float:
        df = self._read("Prices")
        sel = df[(df["event_id"] == str(event_id)) & (df["zone_id"] == zone_id)]
        if stage:
            sel = sel[sel["stage"] == stage]
        if sel.empty and not stage:
            pref = df[(df["event_id"] == str(event_id)) & (df["zone_id"] == zone_id) & (df["stage"] == "regular")]
            sel = pref if not pref.empty else df[(df["event_id"] == str(event_id)) & (df["zone_id"] == zone_id) & (df["stage"] == "preventa")]
        if sel.empty:
            raise KeyError(f"Price not found for ({event_id},{zone_id},{stage})")
        return float(sel.iloc[0]["price"])

__all__ = ["EventsExcelRepo"]
