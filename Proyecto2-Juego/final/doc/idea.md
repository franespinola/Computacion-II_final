El servidor tal como está configurado en el ejemplo está escuchando en la dirección IP 127.0.0.1, que es la dirección de bucle local o loopback, lo que significa que solo será accesible desde la misma máquina en la que se está ejecutando el servidor. Esta configuración es adecuada para pruebas locales o desarrollo.

Si deseas que el servidor sea accesible desde cualquier lugar, deberías cambiar la dirección IP a la dirección IP pública de tu máquina o configurar el servidor en 0.0.0.0, que escuchará en todas las interfaces de red disponibles. Debes tener en cuenta que exponer un servidor directamente a Internet puede tener implicaciones de seguridad, y es recomendable tomar precauciones adicionales, como configurar firewalls y usar conexiones seguras (por ejemplo, HTTPS).

Para cambiar la dirección IP a 0.0.0.0, modifica la línea donde se enlaza el socket en el servidor:
self.socket_servidor.bind(("0.0.0.0", self.port))

Esto permitirá que el servidor escuche en todas las interfaces de red y, por lo tanto, sea accesible desde cualquier lugar si se permite el tráfico en el puerto especificado. Sin embargo, ten en cuenta las consideraciones de seguridad mencionadas anteriormente.
