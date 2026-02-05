from numba.core.ir import Var
import pandas as pd
import numpy as np
from inference.artifacts import get_shrinkage, get_ip_flag
from inference.binning import get_tramos_days, get_tramos_amount, get_tramo_comercial, get_tramo_professional_network_tool
from inference.user_agent_parser import parse_user_agent
from inference.ip_info import get_asn_org, get_city
from inference.trustfull_platform_transformer import calculate_num_prof_net_tools, calculate_digital_score, calculate_num_com, masked_email_match, match_2_last_numbers


def bank_name_shrinkage(bank_name) :
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

    return get_shrinkage(
        "bank_name",
        bank_name, 
        default=1.0
    )


def os_family_shrinkage(user_agent):
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

    os_family = parse_user_agent(user_agent)["os_family"]
    return get_shrinkage(
        "os_family",
        os_family,
        default=1.0
    )


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

    tramo_days = get_tramos_days(days)
    return get_shrinkage(
        "tramos_days",
        tramo_days,
        default=1.0
    )


def tramo_amount_2_shrinkage(amount):
    """
    Aplica el shrinkage correspondiente al tramo del importe solicitado.

    Parameters
    ----------
    amount : int
        Cantidad de dinero solicitada por el usuario.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo de importe.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """

    tramo_amount_2 = get_tramos_amount(amount)
    return get_shrinkage(
        "tramo_amount_2",
        tramo_amount_2,
        default=1.0
    )


def ip_asn_flag_shrinkage(ip):
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
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).`
    """

    asn_org = get_asn_org(ip)
    ip_asn_flag = get_ip_flag("ip_asn_org", asn_org, default="NORMAL")
    return get_shrinkage(
        "ip_asn_flag",
        ip_asn_flag,
        default=1.0
    )


def ip_city_flag_shrinkage(ip):
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

    city = get_city(ip)
    ip_city_flag = get_ip_flag("ip_city", city, default="NORMAL")

    return get_shrinkage(
        "ip_city_flag",
        ip_city_flag,
        default=1.0
    )


def tramo_platforms_shrinkage(tramo_platforms):
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
    return get_shrinkage(
        "tramo_platforms",
        tramo_platforms,
        default=1.0
    )


def tramo_platforms_network_tools_shrinkage(df):
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

    num_platf_net = calculate_num_prof_net_tools(df)
    tramo_platforms_network= get_tramo_professional_network_tool(num_platf_net)
    
    return get_shrinkage(
        "tramo_platforms_network_tools",
        tramo_platforms_network,
        default=1.0,
    )


def tramo_good_behavioral_apps_shrinkage(tramo_good_behavioral_apps):
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


def tramo_platforms_comercial_shrinkage(df):
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

    num_platf_com = calculate_num_com(df)
    tramo_platforms_comercial= get_tramo_comercial(num_platf_com)
    
    return get_shrinkage(
        "tramo_platforms_comercial",
        tramo_platforms_comercial,
        default=1.0,
    )


def promo_code(promo_code_id):
    """
    Función encargada de ver si el usuario ha utilizado o no un código de promoción. 

    Parameters
    ----------
    promo_code_id : str
        Codigo de promoción utilizado por el usuario.

    Returns
    -------
    int
        valor binario 1 si el usuario ha utilizado un código de promoción, 0 en caso contrario.
    """

    if promo_code_id is not None:
        return 1
    else: 
        return 0


def get_digital_score(df):
    """
    Calcula el digital score de un usuario a partir de su número de
    herramientas profesionales de red.

    Esta función actúa como un wrapper que calcula el número de plataformas
    profesionales de red asociadas al usuario y devuelve dicho valor como
    digital score.

    Parameters
    ----------
    df : pandas.DataFrame
    DataFrame que contiene la información digital del usuario.

    Returns
    -------
    float
    Digital score calculado para el usuario. El valor corresponde a la
    primera fila del DataFrame.
    """

    digital_score = calculate_digital_score(df)

    return digital_score


def match_emails(real_email, partials_list_email):
    """
    Comprueba si un email real coincide con alguno de los emails
    parcialmente enmascarados de la lista partials_list_email obtenida en trustfull .

    La función evalúa el email real frente a cada uno de los patrones
    enmascarados proporcionados y devuelve un indicador binario de coincidencia.

    Parameters
    ----------
    real_email : str
        Dirección de correo electrónico completa del usuario.
    partials_list_email : str
        Cadena de emails parcialmente enmascarados separados por comas asociados al telefono del usuario.

    Returns
    -------
    int
        Devuelve 1 si existe al menos una coincidencia entre el email real
        y alguno de los emails enmascarados; devuelve 0 en caso contrario.
    """
    
    lst_emails = partials_list_email.split(",")

    for email in lst_emails:
        if masked_email_match(real_email, email):
            return 1
    return 0


def match_phones(cell_phone, partials_list_phone):
    """
    Comprueba si un numero móvil real coincide con alguno de los emails
    parcialmente enmascarados de la lista partials_list_email obtenida en trustfull .

    La función evalúa el movil real frente a cada uno de los patrones
    enmascarados proporcionados y devuelve un indicador binario de coincidencia.

    Parameters
    ----------
    real_email : str
        Dirección de correo electrónico completa del usuario.
    partials_list_phone : str
        Cadena de emails parcialmente enmascarados separados por comas asociados al telefono del usuario.

    Returns
    -------
    int
        Devuelve 1 si existe al menos una coincidencia entre el móvil real
        y alguno de los móviles enmascarados; devuelve 0 en caso contrario.
    """
    return match_2_last_numbers(partials_list_phone, cell_phone)


def safe_bool(var):
    """

    """
    # Normaliza None / bool / 0-1 / "true"/"false"
    if var is None:
        return 0

    if isinstance(var, bool):
        return int(var)

    if isinstance(var, (int, float)):
        return int(var != 0)

    if isinstance(var, str):
        return int(var.strip().lower() in ("1", "true", "yes", "y", "t"))

    return int(bool(var))


def tele_privacy_status(var):
    """
    Indica si el estado de privacidad es privado.

    Parameters
    ----------
    var : str
        Estado de privacidad del usuario.

    Returns
    -------
    int
        Devuelve 1 si el estado es 'private'; 0 en caso contrario.
    """
    return np.select((var =='private'), 1, 0)


def has_information_flag(var):
    """
    Indica si existe información de privacidad asociada a WhatsApp.

    Parameters
    ----------
    var : any
        Valor asociado al estado de privacidad o uso de código promocional.

    Returns
    -------
    int
        Devuelve 1 si el valor no es None; 0 en caso contrario.
    """
    return 0 if var is None else 1


def match_names( name1, name2):
    """
    Comprueba si dos nombres coinciden parcialmente entre sí.

    La función devuelve una coincidencia positiva si uno de los nombres
    está contenido dentro del otro.

    Parameters
    ----------
    name1 : str
        Primer nombre a comparar.
    name2 : str
        Segundo nombre a comparar.

    Returns
    -------
    int
        Devuelve 1 si existe coincidencia parcial entre los nombres;
        devuelve 0 en caso contrario.
    """
    if name1 in name2:
        return 1
    elif name2 in name1:
        return 1
    return 0 