import asyncio
from api.client.FutbolSocketClient import FutbolSocketClient

async def main():
    server_uri = "wss://machuca.com.ar:4000"

    # Define un ID de equipo único. Puedes generarlo o usar uno fijo para pruebas.
    # team_id = str(uuid.uuid4()) # Generar un ID único
    team_id = "MiEquipoPython" # O usa un ID fijo para facilitar pruebas

    team_name = "Los Pythonicos"
    formation = "4-4-2" # Elige una formación válida de la lista documentada

    # Define tus jugadores. Asegúrate de tener 11 jugadores y configurar
    # es_el_crack y tiene_la_pelota (inicialmente solo uno puede tenerla al registrar).
    players_config = [
        {"numero": 1, "nombre": "Portero", "equipo_id": team_id},
        {"numero": 2, "nombre": "Defensa1", "equipo_id": team_id},
        {"numero": 3, "nombre": "Defensa2", "equipo_id": team_id},
        {"numero": 4, "nombre": "Defensa3", "equipo_id": team_id},
        {"numero": 5, "nombre": "Defensa4", "equipo_id": team_id},
        {"numero": 6, "nombre": "Medio1", "equipo_id": team_id},
        {"numero": 7, "nombre": "Medio2", "equipo_id": team_id},
        {"numero": 8, "nombre": "Medio3", "equipo_id": team_id},
        {"numero": 9, "nombre": "Delantero1", "equipo_id": team_id},
        {"numero": 10, "nombre": "Delantero2", "equipo_id": team_id, "es_el_crack": True},
        {"numero": 11, "nombre": "Delantero3", "equipo_id": team_id, "tiene_la_pelota": True},
    ]

    client = FutbolSocketClient(
        uri=server_uri,
        team_id=team_id,
        team_name=team_name,
        players_config=players_config,
        formation=formation
    )

    await client.run()

if __name__ == "__main__":
    # Ejecuta la función principal asíncrona
    asyncio.run(main())