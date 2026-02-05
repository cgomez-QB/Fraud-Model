from dataclasses import dataclass
from typing import Optional, Dict
import pandas as pd


@dataclass(frozen=True)
class DigitalScoreData:
    lst_cols_comunication: Optional[list[str]]
    lst_cols_comercial: Optional[list[str]]
    lst_cols_identity: Optional[list[str]]
    lst_cols_network_tools: Optional[list[str]]
    lst_cols_trust: Optional[list[str]]
    weights: Optional[Dict[str,float]]


_DIGITAL_SCORE: Optional[DigitalScoreData] = None


def load_digital_score_data():
    global _DIGITAL_SCORE

    if _DIGITAL_SCORE is None:
        _DIGITAL_SCORE = DigitalScoreData(
            lst_cols_comunication=[
                'phone_has_whatsapp', 'phone_has_instagram', 
                'phone_has_telegram', 'phone_has_twitter', 'phone_has_weibo',
                'email_has_pinterest'
            ] ,
            lst_cols_comercial=[
                'phone_has_aliexpress','email_has_spotify', 'email_has_deliveroo',
                'email_has_disney_plus',  'email_has_duolingo', 'has_amazon'
            ],
            lst_cols_identity=[
                'email_has_gravatar', 'email_has_google',
                'has_facebook', 'has_apple'
            ],
            lst_cols_network_tools=[
                'email_has_linkedin', 'email_has_wordpress', 'email_has_hubspot',
                'email_has_atlassian', 'email_has_adobe', 'email_has_freelancer',
                'email_has_github', 'has_office365'
            ], 
            lst_cols_trust=[
                'phone_has_whatsapp', 'phone_has_instagram', 'phone_has_aliexpress',
                'phone_has_telegram', 'phone_has_twitter', 'phone_has_weibo',
                'email_has_spotify', 'email_has_linkedin', 'email_has_deliveroo',
                'email_has_pinterest', 'email_has_wordpress', 'email_has_hubspot',
                'email_has_gravatar', 'email_has_atlassian', 'email_has_lastpass',
                'email_has_adobe', 'email_has_freelancer', 'email_has_github',
                'email_has_disney_plus', 'email_has_google', 'email_has_duolingo',
                'has_facebook', 'has_apple', 'has_amazon', 'has_office365'
            ],
            weights={
                "comunication": 0.5,
                "comercial": 1.0,
                "identity": 0.5,
                "network_tools": 1.1
            }
        )
    return _DIGITAL_SCORE

def calculate_digital_score(df):
    """
    Calcula el digital presence score de un usuario a partir de sus señales
    de presencia y actividad digital en distintas plataformas.

    El score se obtiene como la suma ponderada de un conjunto de variables
    relacionadas con comunicación, comercio, identidad y herramientas de red.
    Cada variable aporta al score según el peso asignado a su grupo.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame que contiene la información digital del usuario.
        Debe incluir las columnas definidas en `lst_cols_trust`.

    Returns
    -------
    float
        Digital presence score calculado para el usuario.
    """
    
    # Cargamos los datos para calcular el digital score
    digi = load_digital_score_data()

    # Diccionaro que contendra todas las puntuaciones segun el grupo de la plataforma

    col_weights = {}

    for col in digi.lst_cols_trust:
        if col in digi.lst_cols_comunication:
            col_weights[col] = digi.weights["comunication"]
        elif col in digi.lst_cols_comercial:
            col_weights[col] = digi.weights["comercial"]
        elif col in digi.lst_cols_identity:
            col_weights[col] = digi.weights["identity"]
        elif col in digi.lst_cols_network_tools:
            col_weights[col] = digi.weights["network_tools"]
        else:
            col_weights[col] = 0.0

    weights = pd.Series(col_weights)

    print("Llego hasta aqui")
    df["digital_presence_score"] = (
        df[digi.lst_cols_trust]
        .fillna(0)
        .mul(weights, axis=1)
        .sum(axis=1)
    )

    
    return df["digital_presence_score"].iloc[0]

def calculate_num_platforms(df, lst_cols, var_name):
    """
    Calcula el número de plataformas activas para un usuario a partir de un
    conjunto de variables binarias y guarda el resultado en una nueva columna.

    El cálculo consiste en sumar, por fila, los valores de las columnas
    especificadas, asumiendo que cada columna indica la presencia (1) o
    ausencia (0) del usuario en una plataforma determinada.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame que contiene la información del usuario.
    lst_cols : list of str
        Lista de nombres de columnas binarias que se utilizarán para el cálculo.
    var_name : str
        Nombre de la columna donde se almacenará el número total de plataformas.

    Returns
    -------
    pandas.DataFrame
        DataFrame original con una nueva columna que contiene el número de
        plataformas activas para el usuario.
    """

    df[var_name] = (
        df[lst_cols]
        .fillna(0)
        .astype("int8")
        .sum(axis=1)
    )

    return df

def calculate_num_prof_net_tools(df):
    """
    Calcula el número de herramientas profesionales de red utilizadas por
    el usuario.

    Esta función utiliza el conjunto de columnas definidas como herramientas
    profesionales de red y devuelve el número total de plataformas activas
    asociadas a este grupo para el usuario.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame que contiene la información digital del usuario.

    Returns
    -------
    float
        Número total de herramientas profesionales de red asociadas al usuario.
        El valor corresponde a la primera fila del DataFrame.
    """

    # Cargamos los datos para calcular el digital score
    digi = load_digital_score_data()

    df = calculate_num_platforms(df, digi.lst_cols_network_tools, "num_professional_network_tools")

    return df["num_professional_network_tools"].iloc[0].astype(float)

def calculate_num_com(df):
    """
    Calcula el número de herramientas profesionales de red utilizadas por
    el usuario.

    Esta función utiliza el conjunto de columnas definidas como herramientas
    profesionales de red y devuelve el número total de plataformas activas
    asociadas a este grupo para el usuario.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame que contiene la información digital del usuario.

    Returns
    -------
    float
        Número total de herramientas profesionales de red asociadas al usuario.
        El valor corresponde a la primera fila del DataFrame.
    """

    # Cargamos los datos para calcular el digital score
    digi = load_digital_score_data()

    print(digi.lst_cols_comercial)
    print(type(digi.lst_cols_comercial))


    df = calculate_num_platforms(df, digi.lst_cols_comercial, "num_plataformas_comercial")

    return df["num_plataformas_comercial"].iloc[0].astype(float)

def masked_email_match(real_email, masked_email):
    """
    Comprueba si un email real coincide con un email parcialmente enmascarado.

    La comparación se realiza verificando los fragmentos no censurados del
    email enmascarado (antes del '@', dominio y extensión) contra el email real.

    Parameters
    ----------
    real_email : str
        Dirección de correo electrónico completa del usuario.
    masked_email : str
        Dirección de correo electrónico parcialmente enmascarada, donde los
        caracteres ocultos se representan con '*'.

    Returns
    -------
    bool
        True si el email real coincide con el patrón del email enmascarado,
        False en caso contrario o si alguno de los valores no es una cadena.
    """
    if not isinstance(real_email, str) or not isinstance(masked_email, str):
        return False

    real_email = real_email.lower().strip()
    masked_email = masked_email.lower().strip()

    # separamos en los 2-3 componentes que no estan censurados dentro de masked_email
    lst = masked_email.split("*")
    lst_component_email = [x for x in lst if x not in (None, "", [], ".")] 
    is_equal = False

    for i, component in enumerate(lst_component_email):
        len_comp = len(component)
        if i == 0: # Comparamos si ambos correos comienzan igual
            is_equal = component == real_email[:len_comp]

        elif i == 1:# Comparamos el dominio de ambos correo para ver si coinciden
            find = real_email.find("@")
            is_equal = component == real_email[find:(find + len_comp)]

        elif i == 2: # Comparamos si el tipo de dominio es el mismo (.com, .es, ...)
            is_equal = component == real_email[-len_comp:]

    return is_equal


def match_2_last_numbers(cell_phone, partials_list_phone ):
    """
    Comprueba si los dos últimos dígitos de un número de teléfono coinciden
    con alguno de los teléfonos parcialmente enmascarados de una lista de telefonos asociados al email del usuario.

    La función compara los dos últimos caracteres del número de teléfono
    completo con los dos últimos caracteres de cada uno de los teléfonos
    proporcionados en la lista.

    Parameters
    ----------
    partials_list_phone : str
        Cadena de números de teléfono (parciales o completos) separados por comas.
    cell_phone : str
        Número de teléfono completo del usuario.

    Returns
    -------
    int
        Devuelve 1 si existe al menos una coincidencia en los dos últimos
        dígitos; devuelve 0 en caso contrario.
    """
    lst_phones = partials_list_phone.split(",")

    for phone in lst_phones:
        
        if phone[-2:] == cell_phone[-2:]:
            return 1
    return 0




