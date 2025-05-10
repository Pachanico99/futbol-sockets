from api.model.sector.Posicion import Posicion

class SectorPelota(Posicion):
    def __init__(self, id: int, x: int, y: int, esta_la_pelota: bool):
        super().__init__(x, y)
        self.id = id
        self.esta_la_pelota = esta_la_pelota
    