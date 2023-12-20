from cliente import Cliente
from servidor import Servidor
from observador import Observador

def main():
    # Implementa el código principal del programa
    cliente = Cliente("127.0.0.1", 12345)
    respuesta = cliente.enviar_datos_monitoreo()
    print(f"Respuesta del servidor: {respuesta}")

if __name__ == "__main__":
    main()
