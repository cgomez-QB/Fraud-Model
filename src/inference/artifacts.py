from __future__ import annotations
import csv
import joblib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
import numpy as np
import pandas as pd

@dataclass(frozen=True)
class Artifacts:
  # feature_name -> category_value -> shrinkage
  shrinkage: Dict[str, Dict[str, float]]

  # Modelos ML
  last_attempt_model: Optional[object] = None
  last_attempt_artifacts: Optional[Dict] = None

  # DataFrame con los intentos todos los intentos previos fallidos
  df_attempts: Optional[pd.DataFrame] = None

  # DataFrame para la similitud entre emails
  df_block_bad_emails: Optional[pd.DataFrame] = None


_ARTIFACTS: Optional[Artifacts] = None


def _data_artifacts_dir():
  """Directorio de CSVs de shrinkage"""
  return Path(__file__).resolve().parent.parent / "data/datos"


def _models_dir():
  """Directorio de modelos .pkl"""
  return Path(__file__).resolve().parent.parent / "data/models"


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


def _load_last_attempt_model():
  """Carga el modelo XGB y sus artefactos para last_attempt"""
  models_path = _models_dir()
  
  try:
      model_path = models_path / "last_attempt_xgb_model.pkl"
      artifacts_path = models_path / "last_attempt_artifacts.pkl"
      
      if not model_path.exists() or not artifacts_path.exists():
        #   print(f"⚠️  Modelo de last_attempt no encontrado en {models_path}")
          return None, None
      
    #   print("📦 Cargando modelo last_attempt XGB...")
      model = joblib.load(model_path)
      artifacts = joblib.load(artifacts_path)
    #   print("✅ Modelo last_attempt cargado correctamente")
      
      return model, artifacts
      
  except Exception as e:
    #   print(f"❌ Error cargando modelo last_attempt: {e}")
      return None, None


def _load_bad_emails_blocks():
  """Carga del DataFrame con la lista de emails y sus respectivos blockes"""
  previous_path = _data_artifacts_dir()
  previous_path = previous_path / "df_bad_emails.csv"

  try:
    return pd.read_csv(previous_path)

  except Exception as e:
    # print(f"❌ Error cargando el DataFrame de bad Emails blocks: {e}")
    return None


def _load_dataframe_previous_attemtps():
  """Carga el df con todos los intentos previos fallidos de todos los usuarios new"""
  previous_path = _data_artifacts_dir()
  previous_path = previous_path / "df_attempts.csv"

  # En caso de no existir el archivo csv devolvemos un None
  try:
    return pd.csv_read(previous_path)

  except Exception as e:
    #   print(f"❌ Error cargando el DataFrame de bad Emails blocks: {e}")
    return None


def load_artifacts():
  """
  Carga todos los shrinkage maps y modelos una sola vez (cold start) y los cachea.
  """
  global _ARTIFACTS
  if _ARTIFACTS is None:
      
      # Cargar CSVs de shrinkage (tu código existente)
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
          "tramo_num_attempts": base / "tramo_num_attempts.csv",
          "tramo_days_last_attempt": base / "tramo_days_last_attempt.csv",
          "req_ip_bin": base /"req_ip_bin.csv",
          "last_attempt": base / "last_attempt_shrinkage.csv",
          "hour_loan": base / "hour_loan_flag.csv",
          "hour_loan_flag": base / "hour_loan_flag_shrinkage.csv",
          "day_week_flag": base / "day_week_flag_shrinkage.csv",
          "day_hour_loan": base / "day_hour_loan_flag.csv",
          "day_hour_loan_flag": base / "day_hour_loan_flag_shrinkage.csv",
          "device_browser_ver": base / "device_browser_ver.csv",
          "device_browser_ver_flag": base / "device_browser_ver_flag.csv",
      }
      shrinkage: Dict[str, Dict[str, float]] = {
          feature: _load_csv_map(path) for feature, path in files.items()
      }
      
      # Cargar modelos ML
      last_attempt_model, last_attempt_artifacts = _load_last_attempt_model()

      # Cargamos todos los intentos previos fallidos de creditos
      df_attempts = _load_dataframe_previous_attemtps()

      # Cargamos los bad emails para poder hacer la compartiva de similitud
      df_block_bad_emails = _load_bad_emails_blocks()
      
      _ARTIFACTS = Artifacts(
          shrinkage=shrinkage,
          last_attempt_model=last_attempt_model,
          last_attempt_artifacts=last_attempt_artifacts,
          df_attempts = df_attempts,
          df_block_bad_emails = df_block_bad_emails,
      )
      
    #   print("✅ Todos los artifacts cargados correctamente")
  return _ARTIFACTS


def get_shrinkage(feature: str, key: str, default: float = 1.0):
  """Obtiene valor de shrinkage para una feature categórica"""
  art = load_artifacts()
  return float(art.shrinkage.get(feature, {}).get(key, default))


def get_var_flag(feature, key, default="NORMAL"):
  """Obtiene flag dela variable pasada"""
  art = load_artifacts()
  return art.shrinkage.get(feature, {}).get(key, default)


def get_previous_attempts():
    """ Obtenemos el DataFrame con los inentos anteriores fallidos"""
    art = load_artifacts()
    return art.df_attempts


def get_bad_emails_blocks():
  """Obtenemos el Dataframe con los blocke de rpefijo y sufijos para calcular la similitud de emails"""
  art = load_artifacts()
  return art.df_block_bad_emails


def get_last_attempt_shrinkage(last_attempt_minutes, previous_attempts):
    """
    Transforma last_attempt en valor de shrinkage usando modelo XGB.

    Parameters
    ----------
    last_attempt_minutes : float or None
        Minutos desde el último intento del usuario
        
    Returns
    -------
    float
        Valor de shrinkage correspondiente
    """
    art = load_artifacts()

    # Si el modelo no está disponible, retornar valor por defecto
    if art.last_attempt_model is None or art.last_attempt_artifacts is None:
        # print("⚠️  Modelo last_attempt no disponible, usando valor por defecto")
        return 0.31  # Media global

    # Manejar valores nulos
    if pd.isna(last_attempt_minutes):
        return art.last_attempt_artifacts['global_mean']

    # Transformación log (igual que en entrenamiento)
    last_attempt_log = np.log1p(max(0, last_attempt_minutes))

    # Predicción con modelo XGB
    X_input = [[last_attempt_log, previous_attempts]]
    prob = art.last_attempt_model.predict_proba(X_input)[0, 1]

    # Asignar flag según umbrales
    thresholds = art.last_attempt_artifacts['thresholds']
    q1, q2, q3 = thresholds['q1'], thresholds['q2'], thresholds['q3']

    if prob <= q1:
        flag = "LOW_DR"
    elif prob <= q2:
        flag = "LOW_NORMAL_DR"
    elif prob <= q3:
        flag = "HIGH_NORMAL_DR"
    else:
        flag = "HIGH_DR"

    # Obtener valor de shrinkage para ese flag
    shrinkage_values = art.shrinkage.get('last_attempt', {})
    shrinkage_value = shrinkage_values[flag]

    return shrinkage_value