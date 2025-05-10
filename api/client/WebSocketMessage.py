
class WebSocketMessage:
    """Clase base para todos los mensajes WebSocket."""
    def __init__(self, mensaje_id: str, destinatario: Optional[str] = None, datos: Optional[Any] = None):
        self.mensaje_id = mensaje_id
        self.destinatario = destinatario
        self.datos = datos

    def to_json(self) -> str:
        """Convierte la instancia del mensaje a una cadena JSON."""
        # asdict convierte dataclasses anidadas también
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(json_string: str) -> Optional[Union["WebSocketMessage", "OKMessage", "ErrorMessage", "TienesLaPelotaMessage", "ReaccionarMessage"]]:
        """Crea una instancia de mensaje desde una cadena JSON."""
        try:
            data = json.loads(json_string)
            mensaje_id = data.get("mensaje_id")

            if not mensaje_id:
                print("Advertencia: Mensaje JSON sin campo 'mensaje_id'.")
                return None

            # Deserialización basada en el mensaje_id
            if mensaje_id == "OK":
                return OKMessage(**data)
            elif mensaje_id == "ERROR":
                return ErrorMessage(**data)
            elif mensaje_id == "TIENES_LA_PELOTA":
                 # Los datos de TIENES_LA_PELOTA y REACCIONAR son listas que contienen cancha y reloj
                cancha_data = None
                reloj_data = None
                if isinstance(data.get("datos"), list):
                    for item in data["datos"]:
                        if isinstance(item, dict):
                            if item.get("tipo") == "cancha":
                                # Serializar y deserializar para instanciar correctamente las subclases
                                try:
                                     cancha_data = CanchaData(**item)
                                except TypeError as e:
                                     print(f"Error deserializando CanchaData: {e} - data: {item}")
                                     # Puedes decidir qué hacer con datos inválidos
                            elif item.get("tipo") == "reloj":
                                try:
                                    reloj_data = RelojData(**item)
                                except TypeError as e:
                                     print(f"Error deserializando RelojData: {e} - data: {item}")
                                     # Puedes decidir qué hacer con datos inválidos


                # Recrear el campo datos como una lista de los objetos instanciados
                instantiated_datos = []
                if cancha_data:
                    instantiated_datos.append(cancha_data)
                if reloj_data:
                     instantiated_datos.append(reloj_data)

                return TienesLaPelotaMessage(
                    mensaje_id=mensaje_id,
                    destinatario=data.get("destinatario"),
                    datos=instantiated_datos
                )

            elif mensaje_id == "REACCIONAR":
                 # Similar a TIENES_LA_PELOTA, los datos son una lista con cancha y reloj
                cancha_data = None
                reloj_data = None
                if isinstance(data.get("datos"), list):
                     for item in data["datos"]:
                         if isinstance(item, dict):
                             if item.get("tipo") == "cancha":
                                try:
                                     cancha_data = CanchaData(**item)
                                except TypeError as e:
                                     print(f"Error deserializando CanchaData en REACCIONAR: {e} - data: {item}")
                             elif item.get("tipo") == "reloj":
                                try:
                                     reloj_data = RelojData(**item)
                                except TypeError as e:
                                     print(f"Error deserializando RelojData en REACCIONAR: {e} - data: {item}")

                instantiated_datos = []
                if cancha_data:
                    instantiated_datos.append(cancha_data)
                if reloj_data:
                    instantiated_datos.append(reloj_data)

                return ReaccionarMessage(
                    mensaje_id=mensaje_id,
                    destinatario=data.get("destinatario"),
                    datos=instantiated_datos
                )
            # Añadir más casos para otros tipos de mensajes del servidor si se documentan
            # elif mensaje_id == "GOL":
            #    return GolMessage(**data)

            else:
                # Para mensajes desconocidos, devolver la estructura base con los datos crudos
                print(f"Mensaje recibido con mensaje_id desconocido: {mensaje_id}")
                return WebSocketMessage(**data)

        except json.JSONDecodeError:
            print(f"Error al decodificar JSON: {json_string}")
            return None
        except TypeError as e:
            print(f"Error de tipo al deserializar mensaje: {e} - data: {json_string}")
            return None
        except Exception as e:
            print(f"Error inesperado al deserializar mensaje: {e} - data: {json_string}")
            return None