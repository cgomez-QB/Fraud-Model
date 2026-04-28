import numpy as np
import pandas as pd
import mysql.connector as sq
from datetime import date, timedelta
import os
from inference.artifacts import get_previous_attempts


def _normalize_dni(dni):
  if pd.isna(dni) or dni is None:
      return ""
  dni = str(dni).strip()
  dni = ''.join(c for c in dni if c.isalnum())
  return dni.upper()

  
def _normalize_email(email):
  if pd.isna(email) or email is None:
      return ""
  return str(email).strip().lower()


def _normalize_cell_phone(phone):
  if pd.isna(phone) or phone is None:
      return ""
  phone = str(phone).strip()
  phone = ''.join(c for c in phone if c.isdigit())
  if phone.startswith('0034'):
      phone = phone[4:]
  elif phone.startswith('34'):
      phone = phone[2:]
  if phone.startswith('0') and len(phone) == 10:
      phone = phone[1:]
  return phone


def get_df_attempts(dni, email, cell_phone, created_at = pd.to_datetime(date.today(), errors="coerce")):
    """
    Función encargada de generar la query y el df con los intentos previos fallidos con el mismo dni, email o cell_phone

    Parameters
    ----------
    dni : str
        Dni del cliente.
    email : str
        Email del cliente.
    cell_phone : str
        Número de telefono del cliente.
    created_at: pd.datetime
        Fecha en la cual se creo la solicitud de préstamo
    
    Returns
    -------
    pandas.DataFrame
        Dataframe con todos los intentos anteriores fallidos
    
    """

    # Cargamos los datos de todos los intentos previos fallidos. 
    df_attempts = get_previous_attempts()

    # Normalizacion de los datos
    for col in [dni, email, cell_phone]:
        if 'deleted' in col:
            col = col[26:]

    dni = _normalize_dni(dni)
    email = _normalize_email(email)
    # cell_phone = _normalize_cell_phone(cell_phone)

    df_attempts["created_at"] = pd.to_datetime(df_attempts["created_at"], errors="coerce")

    # Filtramos por dni, email o cell_phone
    df_attempts = df_attempts[
        (
            (df_attempts['dni'] == dni) |
            (df_attempts['email'] == email) |
            (df_attempts['cell_phone'] == cell_phone)
        )&
        (df_attempts["created_at"] < created_at)
    ]

    return df_attempts

def get_df_attempts_req_ip(ip_adress, created_at):
    """
    Función encargada de generar la query y el df con los intentos previos fallidos con el mismo dni, email o cell_phone

    Parameters
    ----------
    dni : str
        Dni del cliente.
    email : str
        Email del cliente.
    cell_phone : str
        Número de telefono del cliente.
    created_at: pd.datetime
        Fecha en la cual se creo la solicitud de préstamo
    
    Returns
    -------
    pandas.DataFrame
        Dataframe con todos los intentos anteriores fallidos
    
    """
    # Cargamos los datos de todos los intentos previos fallidos. 
    df_attempts = get_previous_attempts()

    # Filtramos el numero de ip iguales que sean anteriores a la solicitud actual
    mask = (
        (df_attempts["ip_address"] == ip_adress) &
        (df_attempts["created_at"] < created_at)
    )

    return int(mask.sum())

def transform(dni, email, cell_phone, ip_address, created_at):
    """
    Funcion encargada de devolver todos los calculos relacionados con las variables de numero de intentos, diferencia
    de tiempo entre solicitudes.

    La función devuelve un diccionario con todos los recuentos de intentos anteriores

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
        Fecha en la cual se creo la solicitud de préstamo

    Returns
    -------
    dict
        Devuelve 1 si existe coincidencia parcial entre los nombres;
        devuelve 0 en caso contrario.
    """
    # Declaramos las variables en caso de que no encuentre intentos previos 
    num_attempts = 0
    diff_days_last_attempt = np.nan
    last_attempt = 0
    created_at = pd.to_datetime(created_at)

    # Obtenemos los intentos fallidos previos
    df_attempts = get_df_attempts(dni, email, cell_phone, created_at)
    
    if not df_attempts.empty:
        # Calculamos las diferentes metricas
        num_attempts = df_attempts.shape[0]
        diff_days_last_attempt = (created_at - df_attempts['created_at'].max()).days
        last_attempt = (created_at - df_attempts["created_at"].max()).total_seconds() / 60
    
    # Obtenemos los intentos fallidos previos con la misma ip
    req_ip = get_df_attempts_req_ip(ip_address, created_at)

    return{
        'num_attempts':num_attempts,
        'diff_days_last_attemtp': diff_days_last_attempt,
        'last_attempt': last_attempt,
        'req_ip': req_ip
    }

