
from api.model.sector.Posicion import Posicion

class EquipoCancha:
    def __init__(self, id: str, nombre: str, formacion:str, rol:int, goles:int, arco:list[Posicion]):
        self.id = id
        self.nombre = nombre
        self.formacion = formacion
        self.rol = rol
        self.goles = goles
        self.arco = arco

