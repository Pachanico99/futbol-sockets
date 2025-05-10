from api.model.sector.SectorPelota import SectorPelota
from api.model.sector.sector import Sector
from api.model.equipo.EquipoCancha import EquipoCancha

class Cancha:
    def __init__(self, tipo: str, id: int, equipo_1: EquipoCancha, equipo_2: EquipoCancha, sectores: list[Sector], ubicacion_pelota: SectorPelota, time_stamp: int):
        self.tipo = tipo
        self.id = id
        self.equipo_1 = equipo_1
        self.equipo_2 = equipo_2
        self.sectores = sectores
        self.ubicacion_pelota = ubicacion_pelota
        self.time_stamp = time_stamp
    