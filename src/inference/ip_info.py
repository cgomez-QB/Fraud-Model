from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import geoip2.database
from geoip2.errors import AddressNotFoundError  # ← NUEVO IMPORT

@dataclass(frozen=True)
class IpInfo:
    reader_city: Optional[geoip2.database.Reader]
    reader_asn: Optional[geoip2.database.Reader]

_IP_INFO: Optional[IpInfo] = None 

def load_databases():
    """
    Función encargada de cargar las bases de datos de la libreria geoip2.
    """
    db_city_path = Path(__file__).resolve().parent.parent / "data/datos/GeoLite2-City.mmdb"
    db_asn_path = Path(__file__).resolve().parent.parent / "data/datos/GeoLite2-ASN.mmdb"

    reader_city = geoip2.database.Reader(db_city_path)
    reader_asn = geoip2.database.Reader(db_asn_path)
    return IpInfo(reader_city=reader_city, reader_asn=reader_asn)


def get_info_geoip():
    """
    Funcion encargada de inicializar la dataclass IpInfo.
    """
    global _IP_INFO 

    if _IP_INFO is None:
        _IP_INFO = load_databases()
        
    return _IP_INFO


def get_asn_org(ip: str, default: str = "UNKNOWN") -> str:
    """
    Obtiene el ASN de la IP del usuario.
    
    Parameters
    ----------
    ip : str
        Dirección IP a consultar.
    default : str, optional
        Valor a retornar si la IP no se encuentra en la base de datos.
    
    Returns
    -------
    str
        Nombre de la organización ASN o el valor por defecto.
    """
    try:
        ip_info = get_info_geoip()
        return ip_info.reader_asn.asn(ip).autonomous_system_organization
    except AddressNotFoundError:
        return default
    except Exception as e:
        # Log o manejo de otros errores (opcional)
        return default


def get_city(ip: str, default: str = "UNKNOWN") -> str:
    """
    Obtiene la ciudad de la IP del usuario.
    
    Parameters
    ----------
    ip : str
        Dirección IP a consultar.
    default : str, optional
        Valor a retornar si la IP no se encuentra en la base de datos.
    
    Returns
    -------
    str
        Nombre de la ciudad o el valor por defecto.
    """
    try:
        ip_info = get_info_geoip()
        return ip_info.reader_city.city(ip).subdivisions.most_specific.name
    except (AddressNotFoundError, AttributeError):
        # AttributeError puede ocurrir si subdivisions.most_specific es None
        return default
    except Exception as e:
        return default


def get_lat(ip: str, default: float = 0.0) -> float:
    """
    Obtiene la latitud de la IP.
    
    Parameters
    ----------
    ip : str
        Dirección IP a consultar.
    default : float, optional
        Valor a retornar si la IP no se encuentra en la base de datos.
    
    Returns
    -------
    float
        Latitud o el valor por defecto.
    """
    try:
        ip_info = get_info_geoip()
        return ip_info.reader_city.city(ip).location.latitude
    except (AddressNotFoundError, AttributeError):
        return default
    except Exception as e:
        return default


def get_lon(ip: str, default: float = 0.0) -> float:
    """
    Obtiene la longitud de la IP.
    
    Parameters
    ----------
    ip : str
        Dirección IP a consultar.
    default : float, optional
        Valor a retornar si la IP no se encuentra en la base de datos.
    
    Returns
    -------
    float
        Longitud o el valor por defecto.
    """
    try:
        ip_info = get_info_geoip()
        return ip_info.reader_city.city(ip).location.longitude
    except (AddressNotFoundError, AttributeError):
        return default
    except Exception as e:
        return default