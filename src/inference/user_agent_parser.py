from user_agents import parse


def parse_user_agent(ua_string):
    """
    Analiza una cadena de User Agent y devuelve un diccionario con la información relevante.

    Parameters
    ----------
    ua_string : str
        Cadena de User Agent a analizar.

    Returns
    -------
    dict:
        Diccionaroio con la información extraida del User Agent del usuario. 
    """
    try:
        ua = parse(ua_string)
        device = ""
        if ua.is_mobile:
            device = "mobile"
        if ua.is_tablet:
            device = "tablet"
        if ua.is_pc:
            device = "pc"

        return {
        "device": device,
        "browser_family": ua.browser.family,
        "browser_version": ua.browser.version_string,
        "os_family": ua.os.family,
        "os_version": ua.os.version_string,
        "device_family": ua.device.family
        }   
        
    except:
        return {
            "device":None,
            "browser_family": None,
            "browser_version": None,
            "os_family": None,
            "os_version": None,
            "device_family": None
        }