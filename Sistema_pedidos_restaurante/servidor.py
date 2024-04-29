import socket
import pickle
from Cliente import Cliente

def main():
    HOST = 'localhost'
    PORT = 50007

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión establecida desde {addr}")
                data = conn.recv(1024)
                method, args = pickle.loads(data)

                if method == "mostrar_carta":
                    response = Cliente.mostrar_carta()
                elif method == "tomar_pedido":
                    response = Cliente.tomar_pedido(*args)
                elif method == "mostrar_pedido":
                    response = Cliente.mostrar_pedido(*args)
                elif method == "modificar_pedido":
                    response = Cliente.modificar_pedido(*args)
                elif method == "eliminar_pedido":
                    response = Cliente.eliminar_pedido(*args)
                else:
                    response = "Método no válido"

                conn.sendall(pickle.dumps(response))

if __name__ == "__main__":
    main()





    


