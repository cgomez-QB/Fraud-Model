from numba.core.ir import Var
import pandas as pd
import numpy as np
from inference.artifacts import get_shrinkage, get_var_flag, get_last_attempt_shrinkage
from inference.binning import *
from inference.user_agent_parser import parse_user_agent
from inference.ip_info import get_asn_org, get_city, get_lat, get_lon

from inference.trustfull_platform_transformer import calculate_num_prof_net_tools, calculate_digital_score, calculate_num_com, masked_email_match, match_2_last_numbers
from inference.previous_attempts_transformer import transform
from inference.emailsimilarity_transformer import transform_single
from inference.geo_consistency_score import calculate_geo_consistency_score
from inference.card_var_transformer import get_fastloan_vars, get_bizzum_vars
from inference.bank_name_normalizer import normalize_bank_name


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
    norm_bank_name = normalize_bank_name(bank_name)

    return get_shrinkage(
        "bank_name",
        norm_bank_name, 
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
        "tramo_days",
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
        str(tramo_amount_2),
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

    ip_asn_flag = get_var_flag("ip_asn_org", asn_org, default="NORMAL")

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
    ip_city_flag = get_var_flag("ip_city", city, default="NORMAL")

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

    if pd.notna(promo_code_id):
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
    Indica si el estado de privacidad de telegram es publico o no.

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


def tramo_num_attempts(num_attempts):
    """
    Aplica el shrinkage correspondiente a numero de intentos anteriores fallidos del usuario segun su dni, email o cell_phone.

    Parameters
    ----------
    num_attempts : int
        Número anterios de intentos fallidos.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    tramo_num_attempts = get_tramo_num_attempts(num_attempts)
    
    return get_shrinkage(
        "tramo_num_attempts",
        tramo_num_attempts,
        default=1.0,
    )


def tramo_days_last_attempt(diff_days_last_attempt):
    """
    Aplica el shrinkage correspondiente a numero de intentos anteriores fallidos del usuario segun su dni, email o cell_phone.

    Parameters
    ----------
    num_attempts : int
        Número anterios de intentos fallidos.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    tramo_days_last_attempt = get_tramo_days_last_attempt(diff_days_last_attempt)

    return get_shrinkage(
        "tramo_days_last_attempt",
        tramo_days_last_attempt,
        default=np.nan,
    )


def last_attempt_prob_xgb_flag(last_attempt, previous_attempts):
    """
    Aplica el shrinkage correspondiente al tiempo desde el ultimo intento.

    Parameters
    ----------
    num_attempts : int
        Número anterios de intentos fallidos.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    
    """

    return get_last_attempt_shrinkage(last_attempt, previous_attempts)


def req_ip_bin(req_ip):
    """
    Aplica el shrinkage correspondiente al numero de intentos de solicitudes fallidas con esa misma ip.

    Parameters
    ----------
    num_attempts : int
        Número anterios de intentos fallidos.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    
    """
    req_ip_bin = get_req_ip_bin(req_ip)

    return get_shrinkage(
        "req_ip_bin",
        req_ip_bin,
        default=1,
    )


def variables_attempts(dni, email, cell_phone, ip_address, created_at):
    """
    Funcion encargada de calcular todas las variables de intentos previos fallidos de cada usuario segun su dni, email o num de teléfono.
    Calcula el numero de intentos previos, dias desde el ultimo intento fallido, prob de fraude segun los minutos desde el ultimo intento 
    y numero de veces que la IP sale repetida en intentos previos fallidos.

    Parameters
    ----------
    dni : str
        Dni del cliente.
    email : str
        Email del cliente.
    cell_phone : str
        Número de telefono del cliente.
    ip_address: str
        Dirección IP del dispositivo con el cual el usuario a realizado la solicitud de crédito.
    created_at: pd.datetime
        Fecha en la cual se creo la solicitud de préstamo.

    Returns
    -------
    dict
        Diccionario con las diferentes variables realacionadas con intentos previos fallidos de los usuarios news.
    
    """
    dct_result = transform(dni, email, cell_phone, ip_address, created_at)

    # Calculamos las diferentes variables relacionadas con intentos previos 
    num_attempts = dct_result['num_attempts']
    diff_days_last_attempt = dct_result['diff_days_last_attemtp']
    last_attempt = dct_result['last_attempt']
    previous_attempts = 1 if num_attempts > 0 else 0
    req_ip = dct_result['req_ip']

    # Obtenemos los valores de los tramos y su respectivo shrinkage
    tramos_num_attempts_shrinkage = tramo_num_attempts(num_attempts)
    tramo_days_last_attempt_shrinkage = tramo_days_last_attempt(diff_days_last_attempt) 
    last_attempt_prob_xgb_oof_flag_shrinkage = last_attempt_prob_xgb_flag(last_attempt, previous_attempts)
    req_ip_bin_shrinkage = req_ip_bin(req_ip)

    return {
        'tramo_num_attempts_shrinkage': tramos_num_attempts_shrinkage,
        'tramo_days_last_attempt_shrinkage' : tramo_days_last_attempt_shrinkage,
        'last_attempt_prob_xgb_oof_flag_shrinkage': last_attempt_prob_xgb_oof_flag_shrinkage,
        'req_ip_bin_shrinkage': req_ip_bin_shrinkage
    }


def hour_of_loan_flag(hour_of_loan):
    """
    Aplica el shrinkage correspondiente al tiempo desde el ultimo intento.

    Parameters
    ----------
    hour_of_loan : int
        Hora en la que solicita el credito.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    
    """
    # Obtenemos el flag de la hora
    hour_loan_flag = get_var_flag("hour_loan", hour_of_loan, default="NORMAL")
    return (
        get_shrinkage(
            "hour_loan_flag",
            hour_loan_flag,
            default=1.0
        ) ,
        hour_loan_flag
    )


def day_of_week_flag(day_week_flag):
    """
    Aplica el shrinkage correspondiente al tiempo desde el ultimo intento.

    Parameters
    ----------
    day_week_flag : str
        String del dia de la semana mas flag de la hora de la solicitud.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    
    """

    return get_shrinkage(
        "day_week_flag",
        day_week_flag,
        default=1.0
    )


def day_hour_flag(day_hour_loan):
    """
    Aplica el shrinkage correspondiente a la construcción hora dia.

    Parameters
    ----------
    day_hour_loan : int
        Hora  y dia en la que solicita el credito.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).
    """
    # Obtenemos el flag de la hora-dia
    hour_loan_flag = get_var_flag("day_hour_loan", day_hour_loan, default="NORMAL")
    return get_shrinkage(
            "day_hour_loan_flag",
            hour_loan_flag,
            default=1.0
        ) 


def get_temporal_vars(created_at):
    """
    Funcion encargada de generar las variables relacionadas con el tiempo en la que se solicitan los prestamos.
    Parameters
    ----------
    created_at : pd.datetime
        Fecha de cración de la solicitud del prestamo.
   
    Returns
    -------
    dict
        Diccionario con las diferentes variables realacionadas con las variables temporales.
    """

    if isinstance(created_at, str):
      created_at = pd.to_datetime(created_at)

    # Obtenemos los valores base de cada una de las variables 
    hour_of_loan = created_at.hour
    hour_of_loan = str(hour_of_loan) # Transformamos a tipo str
    week_day = created_at.day_name()
    day_hour_loan = created_at.strftime("%d_%H")
    
    # Obtenemos los shrinkage de todas las variables
    hour_loan_flag_shrinkage, hour_loan_flag = hour_of_loan_flag(hour_of_loan)

    day_week_flag= week_day + "_" + hour_loan_flag
    day_week_flag_shrinkage = day_of_week_flag(day_week_flag)

    day_hour_loan_flag_shrinkage = day_hour_flag(day_hour_loan)

    return {
        'hour_loan_flag_shrinkage': hour_loan_flag_shrinkage,
        'day_week_flag_shrinkage': day_week_flag_shrinkage,
        'day_hour_loan_flag_shrinkage': day_hour_loan_flag_shrinkage,
        'diff_minutes_flag_shrinkage': np.nan,  
    }


def device_browser_ver_flag(user_agent):
    """
    Funcion encargada de generar el flag para el dispositivo el buscador y su version para encontrar posibles patrones de fraude
    ----------
    user_agent : str
        Cadena de texto enviada por el buscador para ser identificados en sitios web.
   
    Returns
    -------
    dict
        Diccionario con las diferentes variables realacionadas con las variables temporales.
    """
    dct_parsed = parse_user_agent(user_agent)

    device_browser_ver = dct_parsed['device'] + " " +  dct_parsed['browser_family'] + " " + dct_parsed['browser_version']

    device_browser_ver_flag = get_var_flag("device_browser_ver", device_browser_ver, default="NORMAL")
    return get_shrinkage(
            "device_browser_ver_flag",
            device_browser_ver_flag,
            default=1.0
        ) 


def email_similarity(email):
    """
    Funcion encargada de calcular las similitudes con los emails marcados en la lista negra. 
    ----------
    email : str
        Email del usuarios que solicita el credito.
   
    Returns
    -------
    dict
        Diccionario con las diferentes variables realacionadas con las variables de similitud.
    """

    return transform_single(email)


def get_geo_consistency_score(ip, city_name):
    """
    Funcion encargada de llamar todos los calculos con respecto al score de distancia entre la direccion del usuarios y la 
    direccion de ip.

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
    
    # Calculamos la latitud y longitud de la ip desde la cual se realzia la solicitud de credito
    ip_lat = get_lat(ip)
    ip_lon = get_lon(ip)

    # Calculamos el score de distancia entre la ciudad de residencia y el origen de la ip
    score = calculate_geo_consistency_score(city_name, ip_lat, ip_lon)
    
    return score


def tramo_n_categorias_distintas(n_categorias):
    """
    Aplica el shrinkage correspondiente al tramo segun el número de categorias diferentes de movimientos de tarjeta.

    Parameters
    ----------
    n_categorias : int
        Número de categorias diferenes de movimientos de tarjeta.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo de numero de categorias.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).`
    """

    tramo_n_categorias_distintas = get_tramo_n_categorias_distintas(n_categorias)

    return get_shrinkage(
        "tramo_n_categorias_distintas",
        tramo_n_categorias_distintas,
        default=1,
    )


def tramo_fastloans_n_entidades_distintas(fastloans_n_entidades_distintas):
    """
    Aplica el shrinkage correspondiente al tramo segun el número de categorias diferentes de movimientos de tarjeta.

    Parameters
    ----------
    fastloans_n_entidades_distintas : int
        Número de categorias diferenes de movimientos de tarjeta.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo de numero de categorias.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).`
    """

    tramo_fastloans_n_entidades_distintas = get_tramo_fastloans_n_entidades_distintas(fastloans_n_entidades_distintas)

    return get_shrinkage(
        "tramo_fastloans_n_entidades_distintas",
        tramo_fastloans_n_entidades_distintas,
        default=1,
    )


def fastloan_vars(df):
    """
    Funcion encargada de llamar a todos los calculos de variables relacionadas con

    Parameters
    ----------
    fastloans_n_entidades_distintas : int
        Número de categorias diferenes de movimientos de tarjeta.

    Returns
    -------
    float
        Valor de shrinkage asociado al tramo de numero de categorias.
        Si la categoría no existe en los artefactos, se devuelve el valor por defecto (1.0).`
    """

    # Variables de fast loans

    fl_min_diff_hours = np.nan
    amount_vs_fl_conc_7d = np.nan
    ratio_fl_concentration = np.nan

    fastloans_n_meses_activo = df['fastloans_n_meses_activo']
    fastloans_n_entidades_distintas = df['fastloans_n_entidades_distintas']
    n_meses_actividad = df['n_meses_actividad']
    created_at = df['created_at']
    amount = df['amount']

    
    fl_min_diff_hours, amount_vs_fl_conc_7d, ratio_fl_concentration = get_fastloan_vars(
        fastloans_n_meses_activo,
        fastloans_n_entidades_distintas,
        n_meses_actividad,
        created_at,
        amount
    )
   
    return {
        'fl_min_diff_hours': fl_min_diff_hours, 
        'amount_vs_fl_conc_7d':amount_vs_fl_conc_7d, 
        'ratio_fl_concentration':ratio_fl_concentration
    }


def bizzum_vars(df):
    """
    Wrapper de conveniencia para la extracción de métricas de Bizzum.

    Esta función actúa como interfaz principal para el cálculo de variables de 
    comportamiento, delegando la lógica matemática a `get_bizzum_vars`.

    Parameters
    ----------
    n_bizzums : int
        Número de Bizzums.
    n_categorias_distintas : int
        Número de categorías de gasto.
    gambling_por_mes : float
        Transacciones de gambling al mes.
    total_transacciones : int
        Total de transacciones históricas.
    n_meses_actividad : int
        Meses desde la primera transacción.
    salary_existe : int
        Presencia de nómina (1: Sí, 0: No).

    Returns
    -------
    tuple
        Contiene (bizzum_ratio, bizzum_intensity_velocity, mule_purity_check, bizzum_no_salary_risk).
    """

    # Obtenemos las variables 

    n_bizzums = df['n_bizzums']
    n_categorias_distintas = df['n_categorias_distintas']
    gambling_por_mes = df['gambling_por_mes']
    total_transacciones = df['total_transacciones']
    n_meses_actividad = df['n_meses_actividad']
    salary_existe = df['salary_existe']

    bizzum_ratio, bizzum_intensity_velocity, mule_purity_check, bizzum_no_salary_risk = 0, 0, 0, 0
    bizzum_ratio, bizzum_intensity_velocity, mule_purity_check, bizzum_no_salary_risk = get_bizzum_vars(
        n_bizzums, n_categorias_distintas,
        gambling_por_mes,
        total_transacciones,
        n_meses_actividad, salary_existe
    )

    return {
        'bizzum_ratio': bizzum_ratio, 
        'bizzum_intensity_velocity':bizzum_intensity_velocity, 
        'mule_purity_check': mule_purity_check,
        'bizzum_no_salary_risk': bizzum_no_salary_risk
    }


def same_name_phone_database(phone_first_name, db_first_name):
    """
    Funcion encargada de devolver si el nombre asociado el numero de telefono segun trustfull coincide con el que
    el usuario indica en el proceso de registro.

    Parameters
    ----------
    phone_first_name : str
        Nombre asociado al num de teléfono segun Trustfull
    db_first_name : str
        Nombre del usuarios facilitado durante el proceso de registro. 

    Returns
    -------
    int
        Devuelve 1 para cuando coinciden 0 para cuando no .
    """
    # Normalizamos los dos nombres
    if isinstance(phone_first_name, str):
        name1 = phone_first_name.strip().lower()

    if isinstance(db_first_name, str):
        name2 = db_first_name.strip().lower()

    # Normalizamos 
    if name1 in name2:
        return 1
    elif name2 in name1:
        return 1
    return 0 
    

    