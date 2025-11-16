import pandas as pd
from pathlib import Path

STAGES = {"preventa","regular","ultima"}
STATUSES = {"pending","confirmed","released"}

def test_events_file_integrity():
    p = Path("storage") / "events.xlsx"
    assert p.exists(), "events.xlsx no encontrado en /storage"
    ev = pd.read_excel(p, sheet_name="Events", dtype=str)
    zn = pd.read_excel(p, sheet_name="Zones", dtype=str)
    pr = pd.read_excel(p, sheet_name="Prices", dtype=str)
    st = pd.read_excel(p, sheet_name="Stock", dtype=str)

    # IDs únicos en Events
    assert ev["id"].is_unique, "Events.id debe ser único"

    # (event_id, zone_id) único en Zones y Stock
    assert not zn.duplicated(subset=["event_id","zone_id"]).any(), "Zones tiene duplicados (event_id,zone_id)"
    assert not st.duplicated(subset=["event_id","zone_id"]).any(), "Stock tiene duplicados (event_id,zone_id)"

    # Cada zone en Prices/Stock existe en Zones
    pairs = set(map(tuple, zn[["event_id","zone_id"]].values))
    for df, name in [(pr,"Prices"), (st,"Stock")]:
        for row in df[["event_id","zone_id"]].itertuples(index=False):
            assert tuple(row) in pairs, f"{name} contiene zona inexistente {row}"

    # Stages permitidos
    assert set(pr["stage"].unique()).issubset(STAGES), "Hay stages no permitidos en Prices"

def test_reservations_file_integrity():
    p = Path("storage") / "reservations.xlsx"
    assert p.exists(), "reservations.xlsx no encontrado en /storage"
    rs = pd.read_excel(p, sheet_name="Reservations", dtype=str)

    # status permitido
    if not rs.empty:
        assert set(rs["status"].unique()).issubset({"pending","confirmed","released"}), "status inválido en Reservations"
