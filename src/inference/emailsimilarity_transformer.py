"""
Email Similarity Transformer
Calcula features de similitud de emails usando blocking con prefix/suffix.
"""

import pandas as pd
import numpy as np
import Levenshtein as lv
from typing import Dict, List
import re
from inference.artifacts import get_bad_emails_blocks

K_PREFIX = 4
K_SUFFIX = 4

"""
pd.DataFrame({
    'email_norm': self.bad_emails_normalized,
    'block_prefix': self.bad_emails_normalized.apply(
        lambda e: self._block_key_prefix(e, self.k_prefix)
    ),
    'block_suffix': self.bad_emails_normalized.apply(
        lambda e: self._block_key_suffix(e, self.k_suffix)
)
})

"""


def _normalize_email(email: str) -> str:
    """
    Normaliza un email para comparación.
    
    - Lowercase
    - Elimina +tags de Gmail
    - Elimina puntos en Gmail
    - Colapsa separadores repetidos
    """
    if not isinstance(email, str) or '@' not in email:
        return ""
    
    email = email.strip().lower()
    local, domain = email.split('@', 1)
    
    # Quitar +tag
    local = local.split('+', 1)[0]
    
    # Regla de puntos solo para Gmail/Googlemail
    if domain in ("gmail.com", "googlemail.com"):
        local = local.replace('.', '')
    
    # Colapsar separadores repetidos
    local = re.sub(r'[\._-]+', '.', local)
    
    return f"{local}@{domain}"


def _block_key_prefix(email_norm: str, k: int) -> str:
    """Crea block key basado en dominio + prefijo del local."""
    if '@' not in email_norm:
        return ""
    local, domain = email_norm.split('@', 1)
    return f"{domain}|{local[:k]}"


def _block_key_suffix(email_norm: str, k: int) -> str:
    """Crea block key basado en dominio + sufijo del local."""
    if '@' not in email_norm:
        return ""
    local, domain = email_norm.split('@', 1)
    suffix = local[-k:] if len(local) >= k else local
    return f"{domain}|{suffix}"


def transform_single( email: str):
    """
    Calcula features de similitud para UN email.
    
    Parameters
    ----------
    email : str
        Email a transformar
        
    Returns
    -------
    dict
        Diccionario con features calculadas
    """
    # Normalizar email
    email_norm = _normalize_email(email)

    # Cargamos los datos de los bad emails
    df_bad_emails_block = get_bad_emails_blocks()
    
    if not email_norm:
        return _default_features()
    
    # Calcular blocks del email
    block_prefix = _block_key_prefix(email_norm, K_PREFIX)
    block_suffix = _block_key_suffix(email_norm, K_SUFFIX)
    
    # Obtener emails en el mismo block
    emails_in_prefix_block = df_bad_emails_block.loc[df_bad_emails_block['block_prefix'] == block_prefix, 'email_norm'].to_list()
    emails_in_suffix_block = df_bad_emails_block.loc[df_bad_emails_block['block_suffix'] == block_suffix, 'email_norm'].to_list()
    
    # Calcular features PREFIX
    features_prefix = _calculate_block_features(email_norm, emails_in_prefix_block)
    
    # Calcular features SUFFIX
    features_suffix = _calculate_block_features(email_norm, emails_in_suffix_block)
    
    return {
        'email_min_lev_block_prefix': features_prefix['min_dist'],
        'email_cnt_lev_le_1_block_prefix': features_prefix['cnt_le_1'],
        'email_block_size_prefix': features_prefix['block_size'],
        'email_min_lev_block_suffix': features_suffix['min_dist'],
        'email_cnt_lev_le_1_block_suffix': features_suffix['cnt_le_1'],
        'email_block_size_suffix': features_suffix['block_size'],
    }

def _calculate_block_features( email_norm: str, block_emails: List[str]) -> Dict[str, int]:
    """
    Calcula features de similitud dentro de un bloque.
    
    Parameters
    ----------
    email_norm : str
        Email normalizado a evaluar
    block_emails : list
        Lista de emails en el mismo bloque
        
    Returns
    -------
    dict
        Features: min_dist, cnt_le_1, block_size
    """
    if not block_emails:
        return {'min_dist': 99, 'cnt_le_1': 0, 'block_size': 0}
    
    min_dist = 99
    cnt_le_1 = 0
    
    for bad_email in block_emails:
        # if bad_email == email_norm:
        #     continue
            
        dist = lv.distance(email_norm, bad_email)
        
        if dist < min_dist:
            min_dist = dist
        
        if dist <= 1:
            cnt_le_1 += 1
    
    return {
        'min_dist': min_dist,
        'cnt_le_1': cnt_le_1,
        'block_size': len(block_emails)
    }

def _default_features() -> Dict[str, float]:
    """Retorna features por defecto cuando el email es inválido."""
    return {
        'email_min_lev_block_prefix': 99,
        'email_cnt_lev_le_1_block_prefix': 0,
        'email_block_size_prefix': 0,
        'email_min_lev_block_suffix': 99,
        'email_cnt_lev_le_1_block_suffix': 0,
        'email_block_size_suffix': 0,
    }

def transform(emails: pd.Series) -> pd.DataFrame:
    """
    Transforma una Serie de emails.
    
    Parameters
    ----------
    emails : pd.Series
        Serie de emails a transformar
        
    Returns
    -------
    pd.DataFrame
        DataFrame con features de similitud
    """
    results = []
    
    for email in emails:
        features = transform_single(email)
        results.append(features)
    
    return pd.DataFrame(results)