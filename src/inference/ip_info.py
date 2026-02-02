from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import geoip2.database

@dataClass(frozen=True)
class IpInfo:

    reader_city: Optional[geoip2.database.Reader]
    reader_asn: Optional[geoip2.database.Reader]

_IP_INFO: Optional[IpInfo] = None 

def load_databases():
    """
    Función encargada de cargar las bases de datos de la la libreria geoip2.

    Parameters
    ----------
        - None: No se necesitan parametros.

    Returns
    -------
        IpInfo: Dataclass que contiene las BBDD para hacer consultas sobre la ciudad origeny el ASN de la ip del usuario.
    """

    db_city_path = Path(__file__).resolve().parent.parent / "data/GeoLite2-City.mmdb"
    db_asn_path = Path(__file__).resolve().parent.parent / "data/GeoLite2-ASN.mmdb"

    reader_city = geoip2.database.Reader(db_city_path)
    reader_asn = geoip2.database.Reader(db_asn_path)
    return IpInfo(reader_city = reader_city, reader_asn = reader_asn)


def load_databases():
"""
Funcion encargada de inicializar la dataclass IpInfo.
"""
    global _IP_INFO 

    if _IP_INFO is None:
        _IP_INFO = load_databases()
        
    return _IP_INFO


def get_asn_org(ip):
    """
    Funcion encargada de obtener el ASN de la ip del usuario.
    """
    ip_info = load_databases()
    return ip_info.reader_asn.asn(ip).autonomous_system_organization

def get_city(ip):
    """
    Funcion encargada de obtener la ciudad de la ip del usuario.
    """
