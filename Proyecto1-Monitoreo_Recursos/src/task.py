from celery import Celery
from cliente import Cliente

app = Celery('tasks', broker='pyamqp://guest@localhost//')

# Define la tarea Celery para enviar datos de monitoreo
@app.task
def tarea_enviar_datos_monitoreo(servidor_ip, servidor_puerto):
    cliente = Cliente(servidor_ip, servidor_puerto)
    return cliente.enviar_datos_monitoreo()
