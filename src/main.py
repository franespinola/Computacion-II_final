from cliente import Cliente
from servidor import Servidor
from observador import Observador

def main():
    # Implementa el código principal del programa
    cliente = Cliente("127.0.0.1", 12345)
    datos_a_enviar = "Datos de monitoreo desde el cliente"
    respuesta = cliente.enviar_datos(datos_a_enviar)
    print(f"Respuesta del servidor: {respuesta}")

if __name__ == "__main__":
    main()
