import pandas as pd
import numpy as np
import unicodedata

from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from rapidfuzz import process, fuzz


@dataclass(frozen=True)
class orig_city_info:
    df_geonames: Optional[pd.DataFrame]

_ORIG_CITY_INFO: Optional[orig_city_info] = None


def normalize_text(x):
    if pd.isna(x):
        return None
    x = str(x).strip().lower()
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8")
    x = " ".join(x.split())
    return x


def load_orig_city():
    """
    Función encargada de cargar la informacion de las ciudades indicadas por los usuarios en el proceso de registro.

    Parameters
    ----------
        - None:.

    Returns
    -------
        orig_city_info: Dataclass que contiene las BBDD para hacer consultas sobre la ciudad origeny el ASN de la ip del usuario.
    """
    # Cargamos la informacion de las ciudades obtenidos de https://download.geonames.org/export/dump/
    city_path = Path(__file__).resolve().parent.parent / "data/datos/cities500.txt"

    # Declaramos las columnas del df de geonames
    cols = [
        "geonameid", "name", "asciiname", "alternatenames",
        "lat", "lon", "feature_class", "feature_code",
        "country_code", "cc2", "admin1_code", "admin2_code",
        "admin3_code", "admin4_code", "population",
        "elevation", "dem", "timezone", "modification_date"
    ]   

    # declaramos el df que contendra toda la informacion de las ciudades
    geonames = pd.read_csv(
        city_path,
        sep="\t",
        names=cols,
        low_memory=False
    )

    geonames["name_norm"] = geonames["name"].apply(normalize_text)
    geonames["asciiname_norm"] = geonames["asciiname"].apply(normalize_text)

    geo_name = geonames[[
    "name_norm", "country_code", "lat", "lon", "population"
    ]].copy()

    geo_ascii = geonames[[
        "asciiname_norm", "country_code", "lat", "lon", "population"
    ]].rename(columns={"asciiname_norm": "name_norm"}).copy()

    geo_all = pd.concat([geo_name, geo_ascii], ignore_index=True)
    geo_all = geo_all.dropna(subset=["name_norm", "country_code", "lat", "lon"])

    geo_all = (
        geo_all.sort_values(["country_code", "name_norm", "population"], ascending=[True, True, False])
            .drop_duplicates(subset=["country_code", "name_norm"], keep="first")
    )

    geo_spain = geo_all[geo_all["country_code"] == "ES"].copy()

    # Para el ahorro de memoria eliminamos todas las variables temporales auxiliares creadas
    del geo_all, geo_ascii, geo_name, geonames

    return orig_city_info(df_geonames = geo_spain)


def get_geoname_info():
    """
    Funcion encargada de inicializar la dataclass orig_city_info 
    """

    global _ORIG_CITY_INFO

    if _ORIG_CITY_INFO is None:
        _ORIG_CITY_INFO = load_orig_city()
        
    return _ORIG_CITY_INFO


# Para cada ciudad sin match, buscar la más similar
def find_closest_city(city_name, valid_cities, threshold=85):
    """
    Encuentra la ciudad más parecida usando fuzzy matching
    threshold: score mínimo de similitud (0-100)
    """
    if pd.isna(city_name):
        return None
    
    match = process.extractOne(
        city_name, 
        valid_cities,
        scorer=fuzz.ratio,
        score_cutoff=threshold
    )
    
    if match:
        return match[0] 
         # Retorna la mejor coincidencia
    return None


def haversine_np(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia del gran círculo entre dos puntos en la superficie de la Tierra
    utilizando la fórmula de Haversine vectorizada.

    Esta implementación utiliza NumPy para permitir el cálculo eficiente tanto de
    puntos individuales como de arrays de coordenadas (Series de Pandas).

    Parameters
    ----------
    lat1 : float o array-like
        Latitud del primer punto (en grados decimales).
    lon1 : float o array-like
        Longitud del primer punto (en grados decimales).
    lat2 : float o array-like
        Latitud del segundo punto (en grados decimales).
    lon2 : float o array-like
        Longitud del segundo punto (en grados decimales).

    Returns
    -------
    distancia : float 
        Distancia entre los puntos en kilómetros (km).
    """

    R = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2.0) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c

    
def consistency_score(dist_km, tau=100.1518898):
    """
    Calcula un score de confianza basado en la proximidad geográfica mediante
    un decaimiento exponencial de la distancia.

    Parameters
    ----------
    dist_km : float or np.array
        Distancia en kilómetros entre la ubicación de registro y la IP.
    tau : float, optional
        Constante de suavizado calibrada para garantizar que el umbral de 
        confianza (half-distance) se sitúe exactamente en 69.420 km.
        Default: 100.1518898.

    Returns
    -------
    float or np.array
        Score normalizado en el rango (0, 1].
    """
    # Aplicar decaimiento exponencial: score = exp(-d / tau)
    score = np.exp(-dist_km / tau)
    
    return score


def calculate_geo_consistency_score(city_name, lat_ip, lon_ip):
    """
    Calcula un score de consistencia geográfica aplicando un decaimiento exponencial 
    sobre la distancia entre la ciudad de registro y la ubicación de la IP. 
    
    El score se normaliza entre 0 y 1 mediante la función de base radial: 
    exp(-distancia / tau). 

    Parameters
    ----------
    city_name : str
        Nombre de la ciudad de residencia del usuario.
    lat_ip : float
        Latitud de la ubicación detectada por IP.
    lon_ip : float
        Longitud de la ubicación detectada por IP.

    Returns
    -------
    float
        Score de confianza en el rango (0, 1].
    """
    # 1. Aquí deberías obtener las coordenadas de city_name (lat_res, lon_res)
    geo_name = get_geoname_info()
    df = geo_name.df_geonames
    # Obtenemos la lista de ciudades validas en el territorio español
    lst_valid_cities = df['name_norm'].unique().tolist()

    # Normalizamos la direccion del usuario
    norm_city_name = normalize_text(city_name)

    # Encotnramos la ciudad valida mas similar
    closest = find_closest_city(norm_city_name, lst_valid_cities)

    # Obtenemos la latitud y longitud del usuario 
    lat_user = df.loc[df['name_norm'] == closest,'lat'].iloc[0]
    lon_user = df.loc[df['name_norm'] == closest,'lon'].iloc[0]

    #  distancia usando Haversine (dist_km)
    dist_km = haversine_np(lat_ip, lon_ip, lat_user, lon_user)
    
    # Score segun la distancia entre ciudades
    score = consistency_score(dist_km)
    
    return float(score)