import asyncio
import websockets

class FutbolWebsocketsClient:
    def __init__(self, uri: str):
        self.uri = uri
        self.websocket = None

    async def connect(self):
        print(f">>> Intentando conectar a {self.uri}")
        try:
            self.websocket = await websockets.connect(self.uri)
            print("Conexion establecida con exito")
        except ConnectionRefusedError:
            raise Exception(f"La conexion fue rechazada por el servidor {self.uri}")
        except Exception as e:
            raise Exception(f"{e}")

    async def disconnect(self):
        if self.websocket and self.websocket.open:  
            print("Cerrando la conexion...")
            await self.websocket.close()
            print("Conexion cerrada")
        self.websocket = None

    async def run(self):
        try:
            await self.connect()

            while self.websocket and self.websocket.open:
                try:
                    message = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                    print(f"Recibido un mensaje: {message}")

                except asyncio.TimeoutError:
                    pass
                except websockets.exceptions.ConnectionClosed:
                    print("Conexion cerrada por el servidor mientras esperaba mensaje.")
                    break
                except Exception as e:
                    print(f"Fallo al recibir mensaje (saliendo del bucle): {e}")
                    break 

            print(">>> Saliendo del bucle principal")
        except asyncio.CancelledError:
                print("Tarea cancelada")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await self.disconnect()
