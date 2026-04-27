import pandas as pd
from typing import Dict, Optional
# Reglas de normalización de bancos
BANK_NORMALIZATION_RULES = {
  "santander": "BANCO SANTANDER",
  "bilbao": "BBVA",
  "caixabank": "CAIXA BANK",
  "bankia": "CAIXA BANK",
  "ing ": "ING DIRECT",
  "sabadell": "BANCO SABADELL",
  "revolut": "REVOLUT BANK",
  "open": "OPEN BANK",
  "unicaja": "BANCO UNICAJA",
  "liber": "BANCO UNICAJA",
  "rural": "CAJA RURAL",
  "caja r": "CAJA RURAL",
  "credito social": "CAJA RURAL",
  "n26": "N26 BANK",
  "ibercaja": "BANCO IBERCAJA",
  "deutsche": "DEUTSCHE BANK",
  "ncg": "BANCO ABANCA",
  "abanca": "BANCO ABANCA",
  "kutxa": "KUTXABANK",
  "servired": "Métodos de Pago",
  "paysafe": "Métodos de Pago",
  "viacajas": "Métodos de Pago"
}

def normalize_bank_name(bank_name, rules = None):
  """
  Normaliza un nombre de banco individual usando reglas basadas en patrones.
  
  Esta es la versión para procesar UN banco a la vez (usado en inference/scoring).
  
  Parameters
  ----------
  bank_name : str
      Nombre del banco original
  rules : dict, optional
      Diccionario {pattern: normalized_name}.
      Si no se proporciona, usa BANK_NORMALIZATION_RULES por defecto.
  
  Returns
  -------
  str
      Nombre normalizado del banco
  """
  if rules is None:
      rules = BANK_NORMALIZATION_RULES
  
  if not isinstance(bank_name, str):
      return str(bank_name)
  
  bank_lower = bank_name.lower()
  
  # Aplicar reglas en orden
  for pattern, normalized_name in rules.items():
      if pattern in bank_lower:
          return normalized_name
  
  # Si no hay match, devolver original
  return bank_name