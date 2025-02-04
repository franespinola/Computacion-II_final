from servidor import server
from cocina import iniciar_cocina

def main():
    server() # 1. Iniciar el servidor en hilos
    iniciar_cocina()# 2. Iniciar la cocina

if __name__ == "__main__":
    main()
