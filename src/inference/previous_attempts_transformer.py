import numpy as np
import pandas as pd
import mysql.connector as sq
from datetime import date, timedelta
import os


def get_connection():
    """
    Establece y devuelve una conexión a la base de datos MySQL utilizando las variables de entorno definidas.

    Returns
    -------
    mysql.connector.connection.MySQLConnection
        Objeto de conexión activo a la base de datos MySQL.
    """
    return sq.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        use_pure=True,   
    )

def get_querys(lst_query):
    """
    Función encargada de realizar las querys y devolver los datos de estas consultas en formato de DataFrame.
    
    Parameters
    ----------
    lst_query (list): Lista con todas las querys que vamos a realizar.

    Returns
    -------
    pandas.DataFrame: DataFrame con los resultados de las consultas.
    """
    print("Comenzamos a hacer las consultas")
    # Lista con todos los df
    lst_df = []
    # Establecemos la conexion
    conn = get_connection()
    # Creamos el cursor para ejecutar las queries
    cur = conn.cursor()

    for query in lst_query:
        cur.execute(query)
        # Guardamos el resultado
        table_result = cur.fetchall()
        column_names = [desc[0] for desc in cur.description] # Guardamos los nombres de las columnas
        # Creamos un df a partir del resultado
        lst_df.append(pd.DataFrame(table_result, columns=column_names))

    cur.close()
    conn.close()

    print("✅ Consultas finalizadas")
    return lst_df

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
    df_attempts = pd.read_csv("../data/datos/df_attempts.csv")

    for col in ['dni', 'email', 'cell_phone']:
        mask = df_attempts[col].astype(str).str.contains('deleted', na=False)
        df_attempts.loc[mask, col] = df_attempts.loc[mask, col].astype(str).apply(lambda x: x[26:])

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

def transform(dni, email, cell_phone, created_at) -> dict:
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

    # Obtenemos los intentos fallidos previos
    df_attempts = get_df_attempts(dni, email, cell_phone, created_at)
    
    if not df_attempts.empty:
        # Calculamos las diferentes metricas
        num_attempts = df_attempts.shape[0]
        diff_days_last_attempt = (created_at - df_attempts['created_at'].max()).days
        last_attempt = (created_at - df_attempts["created_at"].max()).total_seconds() / 60

    return{
        'num_attempts':num_attempts,
        'diff_days_last_attemtp': diff_days_last_attempt,
        'last_attempt': last_attempt
    }

