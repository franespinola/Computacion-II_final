from servidor import server
from cocina import iniciar_cocina
from proceso_registrar_venta import proceso_registrar_venta
import multiprocessing

def main():
    
    parent_conn, child_conn = multiprocessing.Pipe() # Creamos el pipe: parent_conn para la cocina, child_conn para el notificador
    
    notificador_process = multiprocessing.Process(target=proceso_registrar_venta, args=(child_conn,)) # Creo el proceso notificador
    notificador_process.start()

    server() # 1. Iniciar el servidor 

    iniciar_cocina(parent_conn) #Inicio la cocina y le paso la conexion al notificador

    # 3. Cuando hayas terminado (o quieras cerrar), envía "FIN" 
    parent_conn.send("FIN")

    # Esperar a que el proceso notificador termine
    notificador_process.join()

if __name__ == "__main__":
    main()
