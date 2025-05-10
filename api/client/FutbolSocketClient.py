import asyncio
import websockets
import json
import sys
import uuid
from api.client.WebSocketMessage import WebSocketMessage

# Importar las clases de mensajes actualizadas
from messages import (
    WebSocketMessage,
    RegistrarRequest,
    PatearRequest,
    PasarPelotaRequest,
    CorrerRequest,
    MarcarAdversarioRequest,
    OKMessage,
    ErrorMessage,
    TienesLaPelotaMessage,
    ReaccionarMessage,
    JugadorRegistro,
    EquipoRegistroData,
    CanchaData,
    RelojData,
    JugadorData,
    SectorData,
    EquipoData,
    UbicacionPelotaData
)

class FutbolSocketClient:
    def __init__(self, uri: str, team_id: str, team_name: str, players_config: List[Dict[str, Any]], formation: str):
        self.uri = uri
        self.websocket = None
        self.team_id = team_id # El ID que usarás para registrarte
        self.team_name = team_name
        self.players_config = players_config # Configuración inicial de jugadores
        self.formation = formation
        self.team_token = None # El token que asigna el servidor
        self.player_id = None # Aunque el token identifica al equipo, podrías necesitar el ID del jugador dentro de tu lógica

    async def connect(self):
        """Establece la conexión WebSocket segura (wss://)."""
        print(f"Intentando conectar a {self.uri}...")
        try:
            # Usamos websockets.connect() con la URI segura
            self.websocket = await websockets.connect(self.uri)
            print("Conexión establecida.")
            return True
        except ConnectionRefusedError:
            print(f"Error: Conexión rechazada por el servidor en {self.uri}")
            return False
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    async def disconnect(self):
        """Cierra la conexión WebSocket."""
        if self.websocket and self.websocket.open:
            await self.websocket.close()
            print("Conexión cerrada.")
        self.websocket = None
        self.team_token = None
        self.player_id = None


    async def send_message(self, message: WebSocketMessage):
        """Envía un mensaje al servidor."""
        if self.websocket and self.websocket.open:
            try:
                json_message = message.to_json()
                print(f"Enviando: {json_message}") # Imprime el mensaje JSON enviado
                await self.websocket.send(json_message)
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
        else:
            print("No hay conexión para enviar mensaje.")

    async def receive_message(self) -> Optional[WebSocketMessage]:
        """Espera y recibe un mensaje del servidor."""
        if self.websocket and self.websocket.open:
            try:
                json_string = await self.websocket.recv()
                print(f"Recibido: {json_string}") # Imprime el mensaje JSON recibido
                # Usar el método from_json de la clase base para deserializar
                message = WebSocketMessage.from_json(json_string)
                return message

            except websockets.exceptions.ConnectionClosedOK:
                print("Conexión cerrada limpiamente por el servidor.")
                await self.disconnect()
                return None
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Conexión cerrada con error: {e}")
                await self.disconnect()
                return None
            except Exception as e:
                print(f"Error al recibir mensaje: {e}")
                # Considera si quieres desconectar en otros errores de recepción
                # await self.disconnect()
                return None
        else:
            # print("No hay conexión para recibir mensaje.")
            return None # Retorna None si no hay conexión

    async def register_team(self):
        """Envía la petición de registro del equipo."""
        jugadores_registro = [JugadorRegistro(**p) for p in self.players_config]
        equipo_registro = EquipoRegistroData(
            id=self.team_id,
            nombre=self.team_name,
            jugadores=jugadores_registro,
            formacion=self.formation
        )
        request = RegistrarRequest(datos={"equipo": equipo_registro})
        await self.send_message(request)

    async def handle_server_message(self, message: WebSocketMessage):
        """Maneja los diferentes tipos de mensajes recibidos del servidor."""
        if isinstance(message, OKMessage):
            self.team_token = message.token
            print(f"Registro exitoso. Token del equipo: {self.team_token}")
            # Aquí puedes considerar que estás listo para que empiece el juego

        elif isinstance(message, ErrorMessage):
            print(f"Error del servidor: Tipo='{message.datos.tipo}', Descripción='{message.datos.descripcion}'")
            # Dependiendo del tipo de error, podrías intentar registrar de nuevo
            # o simplemente terminar. Si es "Ya está completo el registro...", no podrás unirte ahora.
            if "completo el registro" in message.datos.descripcion:
                 print("El partido ya está completo. Inténtalo más tarde.")
                 await self.disconnect() # Desconectar si no puedes unirte

        elif isinstance(message, TienesLaPelotaMessage):
            print("¡Tenemos la pelota! Es nuestro turno de actuar.")
            # Extraer datos de la cancha y el reloj
            cancha_data = None
            reloj_data = None
            for item in message.datos:
                if isinstance(item, CanchaData):
                    cancha_data = item
                elif isinstance(item, RelojData):
                    reloj_data = item

            if cancha_data and reloj_data:
                print(f"Estado del juego - Tiempo restante: {reloj_data.reloj}s, Puntaje: {cancha_data.equipo1.goles} - {cancha_data.equipo2.goles}")
                # --- Implementa tu lógica de juego aquí ---
                # Decide qué acción tomar (PATEAR, CORRER, PASAR_PELOTA, MARCAR_ADVERSARIO)
                # Basado en el estado de la cancha (posición de jugadores, pelota, rivales, etc.)

                # Ejemplo: Intentar CORRER con un jugador (esto es solo un placeholder)
                # Deberías tener lógica real para decidir a dónde correr o qué hacer.
                if self.team_token:
                    # Encuentra la posición actual de uno de tus jugadores para moverlo
                    jugador_a_mover_numero = 10 # Número de jugador para este ejemplo
                    current_pos = None
                    for sector in cancha_data.sectores:
                         for ocupante in sector.ocupantes:
                              if ocupante.equipo_id == f"equipo:{self.team_token}" and ocupante.numero == jugador_a_mover_numero:
                                   current_pos = (sector.x, sector.y)
                                   break
                         if current_pos:
                             break

                    if current_pos:
                        # Ejemplo simple: intentar moverlo un poco hacia adelante (ajusta la lógica)
                        new_x = current_pos[0] # Mantener la misma columna
                        new_y = current_pos[1] + 1 # Mover una fila hacia adelante (asumiendo que tu arco está en y=0)
                        print(f"Intentando mover jugador {jugador_a_mover_numero} a ({new_x}, {new_y})")
                        await self.send_message(CorrerRequest(
                            token=self.team_token,
                            datos={"movimientos": [{"jugador_numero": jugador_a_mover_numero, "x": new_x, "y": new_y}]}
                        ))
                    else:
                        print(f"No se encontró la posición del jugador {jugador_a_mover_numero} para mover.")

            else:
                print("Mensaje TIENES_LA_PELOTA no contiene datos de cancha o reloj.")


        elif isinstance(message, ReaccionarMessage):
            print("El adversario tiene la pelota. Es nuestro turno de reaccionar.")
            # Extraer datos de la cancha y el reloj
            cancha_data = None
            reloj_data = None
            for item in message.datos:
                if isinstance(item, CanchaData):
                    cancha_data = item
                elif isinstance(item, RelojData):
                    reloj_data = item

            if cancha_data and reloj_data:
                print(f"Estado del juego - Tiempo restante: {reloj_data.reloj}s, Puntaje: {cancha_data.equipo1.goles} - {cancha_data.equipo2.goles}")
                # --- Implementa tu lógica de reacción aquí ---
                # Decide qué acción tomar (CORRER, PASAR_PELOTA - si recuperaste, MARCAR_ADVERSARIO)
                # Basado en el estado de la cancha y la posición de los rivales.

                # Ejemplo: Intentar MARCAR_ADVERSARIO (placeholder)
                if self.team_token:
                     # Encuentra a un jugador rival para marcar
                     rival_a_marcar_numero = None
                     for sector in cancha_data.sectores:
                         for ocupante in sector.ocupantes:
                             # Asumimos que el equipo rival es el que no es el nuestro
                             if ocupante.equipo_id != f"equipo:{self.team_token}":
                                 rival_a_marcar_numero = ocupante.numero
                                 break
                         if rival_a_marcar_numero:
                              break

                     if rival_a_marcar_numero:
                          # Elige uno de tus jugadores para realizar la marca (placeholder)
                          jugador_marcador_numero = 4 # Ejemplo: un defensor
                          print(f"Intentando que jugador {jugador_marcador_numero} marque a adversario {rival_a_marcar_numero}")
                          await self.send_message(MarcarAdversarioRequest(
                              token=self.team_token,
                              datos={"jugador_numero": jugador_marcador_numero, "adversario_numero": rival_a_marcar_numero}
                          ))
                     else:
                          print("No se encontraron jugadores rivales para marcar.")


            else:
                print("Mensaje REACCIONAR no contiene datos de cancha o reloj.")


        # Puedes añadir manejo para otros tipos de mensajes del servidor, como "GOL"
        # elif isinstance(message, GolMessage):
        #     print("¡GOL!")
        #     # Actualizar el estado del juego según la información del gol


        else:
            print(f"Mensaje recibido de tipo desconocido (mensaje_id: {message.mensaje_id})")
            # Puedes inspeccionar el mensaje base si necesitas ver los datos crudos
            # print(message)


    async def game_loop(self):
        """Bucle principal para recibir y procesar mensajes del juego."""
        print("Iniciando bucle de juego...")
        while self.websocket and self.websocket.open:
            message = await self.receive_message()
            if message:
                await self.handle_server_message(message)

            # Pequeña pausa para no saturar el bucle
            await asyncio.sleep(0.01)


    async def run(self):
        """Ejecuta el cliente: conecta, registra el equipo y entra al bucle principal."""
        if await self.connect():
            await self.register_team()
            # Esperar un poco a que llegue la respuesta de registro (OK o ERROR)
            await asyncio.sleep(1) # Ajusta si es necesario

            # Solo iniciar el bucle de juego si el registro fue exitoso (tenemos un token)
            if self.team_token:
                 await self.game_loop()
            else:
                 print("No se pudo registrar el equipo. Terminando.")

            await self.disconnect()
