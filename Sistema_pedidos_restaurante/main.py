from servidor import server
from cocina import iniciar_cocina
from proceso_registrar_venta import proceso_registrar_venta
import multiprocessing
import signal
import sys

def signal_handler(sig, frame):
    print("\nServidor cerrado.")
    sys.exit(0)

def main():
    parent_conn, child_conn = multiprocessing.Pipe() 
    notificador_process = multiprocessing.Process(target=proceso_registrar_venta, args=(child_conn,)) 
    notificador_process.start()

    try:
        server() 
        iniciar_cocina(parent_conn)
    except KeyboardInterrupt:
        print("\nServidor cerrado.")
    finally:
        # Asegurar que los procesos hijos terminan correctamente
        notificador_process.terminate()
        notificador_process.join()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Manejo de Ctrl+C en Windows
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor cerrado.")
