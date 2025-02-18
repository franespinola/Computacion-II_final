from servidor import server
from cocina import iniciar_cocina
from proceso_registrar_venta import proceso_registrar_venta
import multiprocessing

def main():
    
    parent_conn, child_conn = multiprocessing.Pipe() 
    
    notificador_process = multiprocessing.Process(target=proceso_registrar_venta, args=(child_conn,)) 
    notificador_process.start()

    server() 

    iniciar_cocina(parent_conn) 
    
    notificador_process.join()

if __name__ == "__main__":
    main()
