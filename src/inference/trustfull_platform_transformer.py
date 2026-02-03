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

def calculate_num_platforms(df, lst_cols_trust, var_name):
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
    lst_cols_trust : list of str
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
        df[lst_cols_trust]
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






