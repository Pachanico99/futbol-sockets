
from api.model.jugador.Jugador import Jugador
from api.model.sector.Posicion import Posicion

class Sector(Posicion):
    def __init__(self, id: int, x: int, y: int, ocupantes: list[Jugador]):
        super().__init__(x, y)
        self.id = id
        self.ocupantes = ocupantes