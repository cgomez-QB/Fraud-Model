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
    return np.select(lst_cond, lst_choice, 'N/A').item()    

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

    return np.select(lst_cond, lst_choice, 'N/A').item()

def get_tramo_professional_network_tool(num_platf_net):
    
    lst_cond = [
        num_platf_net<=0,
        num_platf_net==1,
        num_platf_net==2,
        num_platf_net==3,
        (num_platf_net>=4) & (num_platf_net<=8)
    ]

    lst_choices = [
        "0 plat. network/tools",
        "1 plat. network/tools",
        "2 plat. network/tools",
        "3 plat. network/tools",
        "4-8 plat. network/tools"    
    ]

    return np.select(lst_cond, lst_choices, 'N/A').item()

def get_tramo_comercial(num_platf_net):
    
    lst_cond = [
        num_platf_net<=0,
        num_platf_net==1,
        num_platf_net==2,
        num_platf_net==3,
        (num_platf_net>=4) & (num_platf_net<=8)
    ]

    lst_choices = [
        "0 plat. network/tools",
        "1 plat. network/tools",
        "2 plat. network/tools",
        "3 plat. network/tools",
        "4-8 plat. network/tools"    
    ]

    return np.select(lst_cond, lst_choices, 'N/A').item()

def get_tramo_num_attempts(num_attempts):
    """
        
    """
    # Lista de las condiciones
    lst_cond = [
        num_attempts == 0,
        num_attempts == 1,
        2 <= num_attempts <= 10,
        num_attempts > 10
    ]

    # Lista de variables a escoger
    lst_choices = [
        "0 intentos",
        "1 intento previo",
        "2-10 intentos",
        "más de 10 intentos"
    ] 

    return np.select(lst_cond, lst_choices, 'N/A').item()

def get_tramo_days_last_attempt(diff_days):
    lst_cond = [
        diff_days == 0,
        (diff_days >= 1) & (diff_days <= 9),
        (diff_days >= 10) & (diff_days <= 109),
        diff_days >= 110
    ]

    lst_choices = [
        "0 días diff",
        "1-9 días diff",
        "10-109 días diff",
        "110 días o más"
    ]

    return np.select(lst_cond, lst_choices, "N/A").item()

def get_req_ip_bin(req_ip):

    # Lista de las condiciones
    lst_cond = [
        req_ip == 0,
        1 <= req_ip <= 2,
        req_ip > 2
    ]

    # Lista de variables a escoger
    lst_choices = [
        '0 req ip',
        '1-2 req ip',
        '>2 req ip'
    ]
     
    return np.select(lst_cond, lst_choices, '0 req ip').item()


def get_tramo_fastloans_n_entidades_distintas(n_categorias):

    # Lista de las condiciones
    lst_cond = [
        n_categorias <=1,
        n_categorias == 2,
        3 <= n_categorias <= 21,
        n_categorias > 22
    ]

    # Lista de variables a escoger
    lst_choices = [
        "0-1 entidades diferentes",
        "2 entidades diferentes",
        "3-21 entidades diferentes",
        "más de 21 entidades diferentes",
    ]
     
    return np.select(lst_cond, lst_choices, "N/A").item()

def get_tramo_n_categorias_distintas(n_categorias):

    # Lista de las condiciones
    lst_cond = [
       1 <= n_categorias <= 16,
       17 <= n_categorias <= 19,
       20 <= n_categorias <= 22,
       23 <= n_categorias <= 24,
       n_categorias > 24,
    ]

    # Lista de variables a escoger
    lst_choices = [
        "(0.999, 16.0]",
        "(16.0, 19.0]",
        "(19.0, 22.0]",
        "(22.0, 24.0]",
        "(24.0, 33.0]",
    ]
     
    return np.select(lst_cond, lst_choices, "N/A").item()