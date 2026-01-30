import pandas as pd
import numpy as np
from inference.artifacts import get_shrinkage
from inference.binning import *

def bank_name_shrinkage(bank_name: str) :
    """
    Aplica el shrinkage correspondiente al banco del usuario.

    Parameters
    ----------
    bank_name : str
        Nombre del banco del usuario.

    Returns
    -------
    float
        Valor de shrinkage asociado al banco.  
        Si el banco no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage("bank_name", bank_name, default=1.0)

def os_family_shrinkage(os_family: str):
    """
    Aplica el shrinkage correspondiente a la familia del sistema operativo del usuario.

    Parameters
    ----------
    os_family : str
        Familia del sistema operativo (por ejemplo: 'iOS', 'Android', 'Windows').

    Returns
    -------
    float
        Valor de shrinkage asociado a la familia del sistema operativo.  
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage("os_family", os_family, default=1.0)

def tramo_days_shrinkage(tramo_days):
    """
    Aplica el shrinkage correspondiente al tramos de días en los cuales el usuario tiene pensado devolver los prestamos en el plazo de 2 años.

    Parameters
    ----------
    tramo_days : str
        Tramos de días en los cuales el usuario tiene pensado devolver los prestamos.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo de días de devolución de prestamos.  
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """

    return get_shrinkage("tramos_days", tramo_days, default=1.0)

def tramo_days_shrinkage(days):
    """
    Aplica el shrinkage correspondiente al tramos de días en los cuales el usuario tiene pensado devolver los prestamos en el plazo de 2 años.

    Parameters
    ----------
    tramo_days : int
        Días en los cuales el usuario tiene pensado devolver los prestamos.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo de días de devolución de prestamos.  
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    tramo_days = get_tramo_days(days)
    return get_shrinkage("tramos_days", tramo_days, default=1.0)

def tramo_amount_2_shrinkage(tramo_amount_2: str) -> float:
    """
    Aplica el shrinkage correspondiente al tramo del importe solicitado.

    Parameters
    ----------
    tramo_amount_2 : str
        Tramo del importe del crédito solicitado.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo de importe.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage("tramo_amount_2", tramo_amount_2, default=1.0)

def ip_asn_flag_shrinkage(ip_asn_flag: str) -> float:
    """
    Aplica el shrinkage correspondiente al flag de ASN de la IP del usuario.

    Parameters
    ----------
    ip_asn_flag : str
        Flag asociado al ASN de la IP.

    Returns
    -------
    float
        Valor de shrinkage asociado al flag de ASN.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage("ip_asn_flag", ip_asn_flag, default=1.0)

def ip_city_flag_shrinkage(ip_city_flag: str) -> float:
    """
    Aplica el shrinkage correspondiente al flag de ciudad de la IP del usuario.

    Parameters
    ----------
    ip_city_flag : str
        Flag asociado a la ciudad de la IP.

    Returns
    -------
    float
        Valor de shrinkage asociado al flag de ciudad.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage("ip_city_flag", ip_city_flag, default=1.0)


def tramo_platforms_shrinkage(tramo_platforms: str) -> float:
    """
    Aplica el shrinkage correspondiente al tramo de plataformas utilizadas por el usuario.

    Parameters
    ----------
    tramo_platforms : str
        Tramo de plataformas.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo de plataformas.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage("tramo_platforms", tramo_platforms, default=1.0)


def tramo_platforms_network_tools_shrinkage(tramo_platforms_network_tools: str) -> float:
    """
    Aplica el shrinkage correspondiente al uso de herramientas de red en plataformas.

    Parameters
    ----------
    tramo_platforms_network_tools : str
        Tramo de uso de herramientas de red.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage(
        "tramo_platforms_network_tools",
        tramo_platforms_network_tools,
        default=1.0,
    )


def tramo_good_behavioral_apps_shrinkage(tramo_good_behavioral_apps: str) -> float:
    """
    Aplica el shrinkage correspondiente al comportamiento positivo en apps.

    Parameters
    ----------
    tramo_good_behavioral_apps : str
        Tramo de comportamiento positivo en aplicaciones.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage(
        "tramo_good_behavioral_apps",
        tramo_good_behavioral_apps,
        default=1.0,
    )


def tramo_platforms_comercial_shrinkage(tramo_platforms_comercial: str) -> float:
    """
    Aplica el shrinkage correspondiente al uso comercial de plataformas.

    Parameters
    ----------
    tramo_platforms_comercial : str
        Tramo de uso comercial de plataformas.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    return get_shrinkage(
        "tramo_platforms_comercial",
        tramo_platforms_comercial,
        default=1.0,
    )


