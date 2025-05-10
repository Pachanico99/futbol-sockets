from api.model.Jugador import Jugador

class Equipo:
    def __init__(self,id: int, nombre: str, jugadores: list[Jugador], formacion:str):
        self.id = id
        self.nombre = nombre
        self.jugadores = jugadores
        self.formacion = formacion
