Quiero armar una app cliente-servidor que permita el monitoreo de recursos de red de multiples sistemas de manera concurrente. El servidor recopilara informacion de los clientes, realizara analisis y proporcionara resultados a traves de una interfaz web.
Los clientes enviarán datos de monitoreo al servidor de manera concurrente, y el servidor analizará los datos de forma paralela. La comunicacion entre cliente y servidor se realizara a traves de sockets
Esto incluira la supervision de la carga de la red, uso del procesador, memoria y otros recursos criticos.
Se utilizara el patron de diseño Observer donde el servidor actuaría como el "sujeto" y los clientes como "observadores".

1.Sujeto (Servidor de Monitoreo):
    -El servidor sería el sujeto que mantiene una lista de observadores (clientes).
    -Cuando el servidor recibe nuevos datos de un cliente, notifica a todos los observadores (clientes) registrados.
2.Observadores (Clientes de Monitoreo):
    -Los clientes se registran como observadores al servidor.
    -Cuando un cliente envía datos al servidor, este notifica a todos los demás clientes registrados sobre la actualización.

# Descripción Verbal de la Aplicación

## Objetivo del Proyecto:
El objetivo es desarrollar una aplicación cliente-servidor para el monitoreo concurrente de recursos de red en múltiples sistemas. El servidor recopilará datos de los clientes, realizará análisis y presentará resultados a través de una interfaz web.

## Arquitectura General:
La aplicación seguirá un enfoque cliente-servidor. Los clientes enviarán datos al servidor de manera concurrente, y el servidor analizará estos datos de forma paralela. La comunicación entre clientes y servidor se llevará a cabo mediante sockets para garantizar una conexión eficiente y bidireccional.

## Funcionalidades Clave:
- Supervisión de la carga de la red.
- Análisis del uso del procesador, memoria y otros recursos críticos.

## Patrón de Diseño:
Se aplicará el patrón de diseño Observer, donde el servidor actuará como el "sujeto" que mantiene una lista de observadores (clientes). Cuando el servidor reciba nuevos datos, notificará a todos los observadores registrados.

# Funcionalidades de la Aplicación

## Cliente:
- Envia datos de monitoreo al servidor de manera concurrente.
- Gestiona conexiones concurrentes.
- Responde a comandos específicos del servidor.

## Servidor:
- Recibe datos de múltiples clientes de manera concurrente.
- Realiza análisis de recursos de red de forma paralela.
- Envía resultados a los clientes.

