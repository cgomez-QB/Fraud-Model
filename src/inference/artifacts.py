# src/fraud/inference/artifacts.py
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd

_ARTIFACTS: Optional["Artifacts"] = None


@dataclass(frozen=True)
class Artifacts:
    """
    Artefactos precalculados en entrenamiento para scoring online.
    """
    shrinkage: Dict[str, Dict[str, float]]  # feature_name -> category_value -> shrinkage


def _load_json(name: str) :
    base = Path(__file__).resolve().parent
    return json.loads((base / name).read_text(encoding="utf-8"))

def _load_csv(paht_name):
    #base = Path(__file__).resolve().parent
    df = pd.read_csv(paht_name)
    col1,col2 = df.columns.tolist()[0], df.columns.tolist()[1]
    return dict(zip(df[col1],df[col2]))


def get_artifacts(var, default_value=None):
    """
    Carga y cachea todos los artefactos (cold start) y los reutiliza en warm invocations.
    """
    global _ARTIFACTS
    if _ARTIFACTS is None:
        shrinkage = _load_csv(f"../data/datos/{var}.csv")
        _ARTIFACTS = Artifacts(shrinkage=shrinkage)
        
    return _ARTIFACTS