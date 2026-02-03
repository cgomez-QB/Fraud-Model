from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


@dataclass(frozen=True)
class Artifacts:
    # feature_name -> category_value -> shrinkage
    shrinkage: Dict[str, Dict[str, float]]


_ARTIFACTS: Optional[Artifacts] = None


def _data_artifacts_dir():
    # Ajusta esto a donde realmente empaquetes los CSV para Lambda.
    # Recomendación: meterlos dentro de src/inference/artifacts_data/
    
    return Path(__file__).resolve().parent.parent / "data/datos"


def _load_csv_map(path: Path) -> Dict[str, float]:
    """
    Lee un CSV de dos columnas: categoria, shrinkage
    y devuelve dict[categoria] = shrinkage
    """
    mapping: Dict[str, float] = {}
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)  # asume cabecera
        for row in reader:
            if not row:
                continue
            key = str(row[0]).strip()
            val = row[1]
            mapping[key] = val
    return mapping


def load_artifacts():
    """
    Carga todos los shrinkage maps una sola vez (cold start) y los cachea.
    """
    global _ARTIFACTS
    if _ARTIFACTS is None:
        base = _data_artifacts_dir()

        files = {
            "bank_name": base / "bank_name_shrinkage.csv",
            "tramo_amount_2": base / "tramo_amount_2_shrinkage.csv",
            "tramo_days": base / "tramo_days_shrinkage.csv",
            "ip_asn_org": base / "ip_asn_flag.csv",
            "ip_asn_flag": base / "ip_asn_flag_shrinkage.csv",
            "ip_city": base / "ip_city_flag.csv",
            "ip_city_flag": base / "ip_city_flag_shrinkage.csv",
            "os_family": base / "os_family_shrinkage.csv",
            "tramo_platforms": base / "tramo_platforms_shrinkage.csv",
            "tramo_platforms_network_tools": base / "tramo_platforms_network_tools_shrinkage.csv",
            "tramo_good_behavioral_apps": base / "tramo_good_behavioral_apps_shrinkage.csv",
            "tramo_platforms_comercial": base / "tramo_platforms_comercial_shrinkage.csv",

        }

        shrinkage: Dict[str, Dict[str, float]] = {
            feature: _load_csv_map(path) for feature, path in files.items()
        }
        _ARTIFACTS = Artifacts(shrinkage=shrinkage)

    return _ARTIFACTS


def get_shrinkage(feature: str, key: str, default: float = 1.0):
    art = load_artifacts()
    return float(art.shrinkage.get(feature, {}).get(key, default))

def get_ip_flag(feature, key, default="NORMAL"):
    art = load_artifacts()
    return art.shrinkage.get(feature, {}).get(key, default)