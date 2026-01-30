import pandas as pd
import numpy as np

_BANK_NAME_SHRINKAGE = None
_TRAMO_AMOUNT_2_SHRINKAGE = None
_TRAMO_DAYS_SHRINKAGE = None
_IP_ASN_FLAG_SHRINKAGE = None
_IP_CITY_FLAG_SHRINKAGE =None
_OS_FAMILY_SHRINKAGE = None
_TRAMO_PLATFORM_SHRINKAGE = None
_TRAMO_PLATFORM_NETWORK_TOOLS_SHRINKAGE = None
_TRAMO_GOOD_BEHAVIORAL_APPS_SHRINKAGE = None
_TRAMO_PLATFORM_COMERCIAL_SHRINKAGE = None

def cold_start_shrinkage(bank_name):
    """
    Función encargada de aplicar el shrinkage a la variable bank_name.

    Parameters
    ----------
    Ban_name (str): Nombre del banco el usuario

    Returns
    -------
    Bank_name_shrinkage (float): Valor del shrinkage aplicado a la variable bank_name.
    """
    _BANK_NAME_SHRINKAGE = get_artifacts("bank_name_shrinkage")
    _TRAMO_AMOUNT_2_SHRINKAGE = get_artifacts("tramo_amount_2_shrinkage")
    _TRAMO_DAYS_SHRINKAGE = get_artifacts("tramo_days_shrinkage")
    _IP_ASN_FLAG_SHRINKAGE = get_artifacts("ip_asn_flag_shrinkage")
    _IP_CITY_FLAG_SHRINKAGE = get_artifacts("ip_city_flag_shrinkage")
    _OS_FAMILY_SHRINKAGE = get_artifacts("os_family_shrinkage")
    _TRAMO_PLATFORM_SHRINKAGE = get_artifacts("tramo_platforms_shrinkage")
    _TRAMO_PLATFORM_NETWORK_TOOLS_SHRINKAGE = get_artifacts("tramo_platforms_network_tools_shrinkage")
    _TRAMO_GOOD_BEHAVIORAL_APPS_SHRINKAGE = get_artifacts("tramo_good_behavioral_apps_shrinkage")
    _TRAMO_PLATFORM_COMERCIAL_SHRINKAGE = get_artifacts("tramo_platforms_comercial_shrinkage")
