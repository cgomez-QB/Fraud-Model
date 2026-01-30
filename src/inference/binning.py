import numpy as np

def get_tramos_days(days):
    """
    Asigna el tramo de días de devolución a partir del número de días.

    Parameters
    ----------
    days : int
        Número de días de devolución del préstamo.

    Returns
    -------
    str
        Tramo de días asignado según el análisis de entrenamiento.
    """
    lst_cond = [
        days <= 14,
    (days >= 15) & (days <= 25),
    (days >= 26) & (days <= 29),
    days == 30,
    (days >= 31) & (days <= 35),
    (days >= 36) & (days <= 43),

    ]

    lst_choice=[
        '1-14 días',
        '15-25 días',
        '26-29 días',
        '30 días',
        '31-35 días',
        '36-43 días'
    ]
    return np.select(lst_cond, lst_choice, 'N/A')    

def get_tramos_amount(amount):
    """
    Asigna el tramo de amount solicitado por el usuario.

    Parameters
    ----------
    days : int
        Cantidad de dinero solicitada por el usuario.

    Returns
    -------
    str
        Tramo de amount asignado según el análisis de entrenamiento.
    """

    lst_cond=[
        amount<=50,
        (amount>=51) & (amount<=99),
        (amount>=100) & (amount<=101),
        (amount>=102) & (amount<=199),
        (amount>=200) & (amount<=300),
    ]

    lst_choice=[
        "50€",
        "51€-99€",
        "100€-101€",
        "102-199€",
        "200-300€"
    ]

    return np.select(lst_cond, lst_choice, 'N/A')