def proceso_registrar_venta(conn_notificador):
    """
    Este proceso se bloquea esperando un mensaje de la cocina (conn_notificador).
    Cuando recibe un pedido finalizado, lo escribe en un archivo de ventas.
    Si recibe 'FIN', se cierra.
    """
    ventas_filename = "ventas_del_dia.txt"
    
    while True:
        mensaje = conn_notificador.recv()  # Bloqueante
        if mensaje == "FIN":
            print("[Notificador] Recibido FIN, cerrando notificador...")
            break
        
        # Se asume que el mensaje incluye la info del pedido finalizado
        print(f"[Notificador] Recibido pedido finalizado: {mensaje}")
        
        # 1) Guardar info en un archivo de ventas
        with open(ventas_filename, "a", encoding="utf-8") as f:
            f.write(mensaje + "\n")

    # Cierre de la conexión (opcional para limpieza)
    conn_notificador.close()
    print("[Notificador] Notificador cerrado.")
