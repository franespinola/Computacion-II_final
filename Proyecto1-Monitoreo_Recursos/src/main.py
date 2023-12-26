from task import tarea_enviar_datos_monitoreo

def main():
    # Configura los datos del servidor
    servidor_ip = "127.0.0.1"
    servidor_puerto = 12345

    # Ejecuta la tarea Celery para enviar datos de monitoreo
    resultado = tarea_enviar_datos_monitoreo.delay(servidor_ip, servidor_puerto)

    # Espera la finalización de la tarea y obtén el resultado
    respuesta = resultado.get()

    # Imprime la respuesta del servidor
    print(f"Respuesta del servidor: {respuesta}")

if __name__ == "__main__":
    main()

