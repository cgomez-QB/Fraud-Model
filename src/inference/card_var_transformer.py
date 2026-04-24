import pandas as pd


def calcular_concentracion_fastloans(fastloans_n_meses_activo, created_at):
    """
    Analiza el histórico de solicitudes para calcular métricas de concentración 
    temporal y velocidad de solicitud (velocity checks).

    Parameters
    ----------
    fastloans_n_meses_activo : str or list
        Histórico de fechas de solicitudes previas. Puede ser una lista de 
        strings/datetimes o un string representando una lista (formato JSON/literal).
    created_at : datetime
        Fecha y hora de la solicitud de crédito actual que se está evaluando.

    Returns
    -------
    concentracion_7d : int
        Número de solicitudes realizadas en los últimos 7 días respecto a `created_at`.
    min_distancia_horas : float
        Tiempo mínimo (en horas) transcurrido entre la solicitud actual y la 
        solicitud previa más cercana. Retorna 9999 si no hay registros previos.
    """

    # La columna contiene strings que parecen listas, o listas reales
    solicitudes = fastloans_n_meses_activo
    
    # Si es un string que representa una lista, lo convertimos (eval o similar)
    # Si ya es lista, nos saltamos este paso.
    if isinstance(solicitudes, str):
        import ast
        try:
            solicitudes = ast.literal_eval(solicitudes)
        except:
            return pd.Series([0, 0, 0])
    
    if not solicitudes or not isinstance(solicitudes, list):
        return pd.Series([0, 0, 0])
    
    # Convertir todas las fechas de la lista a datetime
    fechas_previas = pd.to_datetime(solicitudes)
    fecha_actual =  pd.to_datetime(created_at)
    
    # Calculamos la diferencia de tiempo
    # Solo nos interesan solicitudes ANTES de la actual (o el mismo día)
    diffs = (fecha_actual - fechas_previas).total_seconds() / 3600 # Diferencia en horas
    
    # Filtramos solo las que ocurrieron en el pasado (evitar fugas de datos)
    diffs = diffs[diffs >= 0]
    
    # 2. Definir las ventanas de concentración (en horas)
    concentracion_7d = (diffs <= 24 * 7).sum()
    
    # 3. Calcular la velocidad (tiempo min entre la solicitud actual y la anterior)
    # Si no hay previas, ponemos un valor alto (ej. 9999 horas)
    min_distancia_horas = diffs.min() if len(diffs) > 0 else 9999
    
    return concentracion_7d, min_distancia_horas

def get_fastloan_vars(fastloans_n_meses_activo, fastloans_n_entidades_distintas, n_meses_actividad, created_at, amount):
    """
    Genera variables derivadas de 'Fast Loans' para el modelo de scoring, 
    relacionando concentración, exposición por monto y ratio de entidades.

    Parameters
    ----------
    fastloans_n_meses_activo : str or list
        Histórico de fechas de solicitudes de préstamos rápidos.
    fastloans_n_entidades_distintas : int
        Número total de entidades financieras diferentes identificadas.
    n_meses_actividad : int
        Número de meses que el usuario lleva activo en el sistema o histórico.
    created_at : datetime
        Timestamp de la solicitud actual.
    amount : float
        Monto solicitado en el crédito actual.

    Returns
    -------
    fl_min_diff_hours : float
        Horas transcurridas desde la solicitud de 'fast loan' más reciente.
    amount_vs_fl_conc_7d : float
        Ratio entre el número de solicitudes en la última semana y el monto solicitado.
    ratio_fl_concentration : float
        Densidad de entidades distintas por mes de actividad del usuario.
    """
    
    # Variables 
    fl_conc_7d, fl_min_diff_hours = calcular_concentracion_fastloans(fastloans_n_meses_activo, created_at)
    amount_vs_fl_conc_7d =  fl_conc_7d / amount 
    ratio_fl_concentration = fastloans_n_entidades_distintas / n_meses_actividad

    return fl_min_diff_hours, amount_vs_fl_conc_7d, ratio_fl_concentration


def get_bizzum_vars(n_bizzums, n_categorias_distintas, gambling_por_mes, total_transacciones, n_meses_actividad, salary_existe):
    """
    Calcula variables avanzadas de comportamiento transaccional (Bizzum) para la 
    detección de anomalías y perfiles de riesgo (Mule detection).

    Parameters
    ----------
    n_bizzums : int
        Número total de transacciones tipo Bizzum identificadas.
    n_categorias_distintas : int
        Diversidad de categorías de gasto en el historial del usuario.
    gambling_por_mes : float
        Promedio mensual de transacciones relacionadas con juegos de azar/apuestas.
    total_transacciones : int
        Volumen total de movimientos en la cuenta del usuario.
    n_meses_actividad : int
        Antigüedad del usuario en meses dentro de la plataforma.
    salary_existe : int (0 o 1)
        Flag booleano que indica la presencia de nómina detectada en la cuenta.

    Returns
    -------
    bizzum_ratio : float
        Proporción de Bizzums sobre el total de transacciones.
    bizzum_intensity_velocity : float
        Intensidad de uso de Bizzum normalizada por la antigüedad del usuario.
    mule_purity_check : float
        Indicador de riesgo de "cuenta mula" basado en la relación entre Bizzums, 
        apuestas y baja diversidad de categorías.
    bizzum_no_salary_risk : float
        Factor de riesgo que penaliza el uso intensivo de Bizzum en ausencia de nómina.
    """

    bizzum_ratio = n_bizzums / total_transacciones
    bizzum_intensity_velocity = n_bizzums / (n_meses_actividad + 1)
    mule_purity_check = n_bizzums / (gambling_por_mes + n_categorias_distintas)
    bizzum_no_salary_risk = bizzum_ratio * (1 - salary_existe)

    return bizzum_ratio, bizzum_intensity_velocity, mule_purity_check, bizzum_no_salary_risk