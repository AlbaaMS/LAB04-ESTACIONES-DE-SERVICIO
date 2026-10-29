from collections import namedtuple
from math import *

EstacionSevici = namedtuple("EstacionSevici", 
    "nombre, direccion, latitud, longitud, capacidad, puestos_libres, bicicletas_disponibles")

def selecciona_color(estacion:EstacionSevici) -> str:
    """
    Devuelve el color en que debe pintarse cada estación según su disponibilidad.

    Parámetros:
    estacion: EstacionSevici

    Devuelve:
    str: "green", "orange", "red" o "gray"
    """

    if estacion.capacidad == 0:
        return "gray"
    else:
        disponibilidad = estacion.bicicletas_disponibles/estacion.capacidad
        if disponibilidad >= 2/3:
            return "green"
        elif disponibilidad >= 1/3:
            return "orange"
        else:
            return "red"


def calcula_estadisticas(estaciones: list[EstacionSevici]) -> tuple[int, int, float, int]:
    """
    Calcula estadísticas de las estaciones.
    Parametros:
    estaciones: lista de EstacionSevici
    Devuelve:
    tupla con (total de bicicletas libres, total de capacidad, porcentaje de ocupación, total de estaciones)
    """
    total_bicis_libres = 0
    total_capacidad = 0
    porcentaje_ocupacion = 0
    total_estaciones = 0
    for estacion in estaciones:
        total_estaciones += 1
        total_bicis_libres += estacion.bicicletas_disponibles
        total_capacidad += estacion.capacidad
        if total_bicis_libres == estacion.capacidad:
            porcentaje_ocupacion = 0.0
        elif total_bicis_libres == 0:
            porcentaje_ocupacion = 100.0
        else:
            porcentaje_ocupacion = (1-(total_bicis_libres/ total_capacidad))*100

    return(total_bicis_libres, total_capacidad, porcentaje_ocupacion, total_estaciones)

def busca_estaciones_direccion(estaciones: list[EstacionSevici], direccion_parcial: str) -> list[EstacionSevici]:
    """
    Busca las estaciones que contengan en su dirección (subcadena, sin distinguir mayúsculas/minúsculas) la dirección parcial dada.    

    Parametros:
    estaciones: lista de EstacionSevici
    direccion_parcial: subcadena a buscar en la dirección de las estaciones

    Devuelve:
    lista de EstacionSevici que cumplen el criterio
    """
    res = []
    for estacion in estaciones:
        if direccion_parcial.lower() in estacion.direccion.lower():
            res.append(estacion)
    return res

def busca_estaciones_con_disponibilidad(estaciones:list[EstacionSevici], min_disponibilidad: float = 0.5) -> list[EstacionSevici]:
    """
    Devuelve una lista de EstacionSevici con al menos el porcentaje mínimo de bicicletas disponible
    indicado.

    Parametros:
    estaciones: lista de EstacionSevici
    min_disponibilidad: porcentaje mínimo de bicicletas disponibles (0.0 a 1.0)
    
    Devuelve:
    lista de EstacionSevici
    """
    res = []
    for estacion in estaciones:
        if estacion.capacidad !=0:
            disponibilidad = estacion.bicicletas_disponibles/estacion.capacidad
            if disponibilidad >= min_disponibilidad:
                res.append(estacion)
    return res

def calcula_distancia(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calcula la distancia euclídea entre dos puntos (latitud, longitud).

    Parámetros:
    p1: tupla (latitud, longitud) del primer punto
    p2: tupla (latitud, longitud) del segundo punto

    Devuelve:
    float: distancia euclídea--pitagorás entre los dos puntos
    """
    res = 0
    dist_i= abs(p1[0]-p2[0])
    dist_j= abs(p1[1]-p2[1])
    res = sqrt(dist_i**2 + dist_j**2)
    return res
    
def busca_estacion_mas_cercana(estaciones:list[EstacionSevici], punto:tuple[float, float]) -> EstacionSevici | None:
    """
    Devuelve la estación más cercana al punto dado (latitud, longitud) que tenga al menos una bicicleta disponible.
    
    Parametros:
    estaciones: lista de EstacionSevici
    punto: tupla (latitud, longitud)

    Devuelve:
    EstacionSevici más cercana con al menos una bicicleta disponible, o None si no hay ninguna.
    """ 
    res = None
    for estacion in estaciones:
        if res == None:
            res = estacion
        else:
            if calcula_distancia((punto[0],punto[1]), (estacion[2], estacion[3])) < calcula_distancia((punto[0], punto[1]) , (res[2], res[3])):
                res = estacion
    return res

def calcula_ruta(estaciones:list[EstacionSevici], origen:tuple[float, float], destino:tuple[float, float]) -> tuple[EstacionSevici | None, EstacionSevici | None]   :
    """
    Devuelve las estaciones más cercanas al punto de origen y destino dados, que tengan al menos una bicicleta disponible.

    Parametros: 
    estaciones: lista de EstacionSevici
    origen: tupla (latitud, longitud) del punto de origen
    destino: tupla (latitud, longitud) del punto de destino

    Devuelve:
    tupla con (estacion_origen, estacion_destino)
    """
    res1 = busca_estacion_mas_cercana(estaciones,origen)
    res2 = busca_estacion_mas_cercana(estaciones,destino)
    return res1, res2

