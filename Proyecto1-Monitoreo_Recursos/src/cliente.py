import socket
import psutil
from celery import Celery

# Configuración de Celery
app = Celery('cliente', broker='pyamqp://guest@localhost//')

class Cliente:
    def __init__(self, servidor_ip, servidor_puerto):
        # Implementa la lógica del cliente
        self.servidor_ip = servidor_ip
        self.servidor_puerto = servidor_puerto
    
    def obtener_datos_monitoreo(self):
        # Utiliza la biblioteca psutil para obtener datos del sistema
        carga_red = psutil.net_io_counters()
        uso_cpu = psutil.cpu_percent(interval=1)
        uso_memoria = psutil.virtual_memory()
        uso_disco = psutil.disk_usage('/')

        # Retorna los datos formateados como una cadena
        return f"Carga de Red: {carga_red.bytes_sent}/{carga_red.bytes_recv}\n" \
               f"Uso de CPU: {uso_cpu}%\n" \
               f"Uso de Memoria: {uso_memoria.percent}%\n" \
               f"Uso de Disco: {uso_disco.percent}%"
    
    def enviar_datos_monitoreo(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.servidor_ip, self.servidor_puerto))
            
            # Obtén los datos de monitoreo
            datos_monitoreo = self.obtener_datos_monitoreo()

            # Envía los datos al servidor
            s.sendall(datos_monitoreo.encode())
            data = s.recv(1024)

        return data.decode()

    def recibir_resultados(self):
        # Implementa la recepción de resultados del servidor
        pass
