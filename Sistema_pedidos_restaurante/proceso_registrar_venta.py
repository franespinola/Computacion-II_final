def proceso_registrar_venta(child_conn):
    """
    Este proceso se bloquea esperando pedidos de la cocina (child_conn).
    Cuando recibe un pedido finalizado, lo escribe en un archivo de ventas.
    Se mantiene en ejecución hasta que el proceso principal (servidor) finalice.
    """
    ventas_filename = "ventas_del_dia.txt"
    
    while True:
        try:
            mensaje = child_conn.recv()  # Bloqueante hasta recibir datos
            print(f"Pedido recibido desde Cocina (parent_conn): {mensaje}")

            # Guardar la información en un archivo de ventas
            with open(ventas_filename, "a", encoding="utf-8") as f:
                f.write(mensaje + "\n")

        except EOFError:
            print("[Notificador] Pipe cerrado, finalizando el proceso...")
            break  # Finalizar proceso cuando la tubería se cierra al apagar el servidor

    print("[Notificador] Notificador cerrado.")

