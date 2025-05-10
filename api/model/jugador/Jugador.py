class Jugador:
    def __init__(self, numero: int, nombre: str, equipo_id: int, es_el_crack: bool, tiene_la_pelota: bool, sector_id: int):
        self.numero = numero
        self.nombre = nombre
        self.equipo_id = equipo_id
        self.sector_id = sector_id
        self.es_el_crack = es_el_crack
        self.tiene_la_pelota = tiene_la_pelota