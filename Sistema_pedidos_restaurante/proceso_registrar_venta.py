def proceso_registrar_venta(child_conn):
  
    ventas_filename = "ventas_del_dia.txt"
    
    while True:
        try:
            mensaje = child_conn.recv() 
            print(f"Pedido recibido desde Cocina (parent_conn): {mensaje}")

            with open(ventas_filename, "a", encoding="utf-8") as f:
                f.write(mensaje + "\n")

        except EOFError:
            print("[Notificador] Pipe cerrado, finalizando el proceso...")
            break  

    print("[Notificador] Notificador cerrado.")

